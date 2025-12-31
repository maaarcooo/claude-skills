#!/usr/bin/env python3
"""
PDF Content Extractor for Claude Skill
=======================================

A comprehensive PDF extraction tool designed to extract maximum detail from PDF files.
Outputs raw content for Claude to interpret and clean, rather than applying hardcoded
cleaning rules.

DESIGN PHILOSOPHY:
    - Extract everything possible: text, images, metadata, structure
    - Preserve raw content without cleaning (Claude handles cleanup)
    - Provide rich metadata to help Claude understand document structure
    - Simple interface, robust error handling

DEPENDENCIES:
    pip install pymupdf pymupdf4llm

USAGE:
    # Basic usage (auto-generates output folder)
    python extract_pdf.py document.pdf
    
    # Specify output folder
    python extract_pdf.py document.pdf ./output/
    
    # Extract specific pages (1-indexed)
    python extract_pdf.py document.pdf --pages 1-10
    
    # Force specific extraction method
    python extract_pdf.py document.pdf --method pymupdf4llm
    python extract_pdf.py document.pdf --method pymupdf

OUTPUT STRUCTURE:
    output_folder/
    ├── document.md          # Main extracted markdown with YAML frontmatter
    ├── metadata.json        # Structured extraction metadata
    └── images/              # Extracted images (if any)
        ├── page001_img001.png
        └── page002_img001.png

CLAUDE SKILL WORKFLOW:
    1. User uploads PDF
    2. Claude calls: python extract_pdf.py /path/to/input.pdf /path/to/output/
    3. Claude reads output markdown and metadata
    4. Claude cleans/processes based on content patterns and user needs
    5. Claude outputs final result

Author: Claude Skill
Version: 1.0.0
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any

# PDF libraries
import pymupdf  # Also known as fitz
import pymupdf4llm

# =============================================================================
# CONFIGURATION
# =============================================================================

VERSION = "1.0.0"

# Minimum character threshold for auto fallback.
# If pymupdf4llm extracts fewer characters than this, try pymupdf as fallback.
# This catches scanned/image-based PDFs where pymupdf4llm may fail.
FALLBACK_THRESHOLD = 5000

# Minimum image dimensions to extract (skip tiny artifacts)
MIN_IMAGE_WIDTH = 10
MIN_IMAGE_HEIGHT = 10

# =============================================================================
# EXCEPTIONS
# =============================================================================

class ExtractionError(Exception):
    """
    Custom exception for PDF extraction errors.
    
    Provides structured error information for better debugging and
    user-friendly error messages.
    
    Attributes:
        message: Human-readable error description
        stage: Which extraction stage failed ('validation', 'open', 'extract', 'images', 'save')
        original_error: Underlying exception if any
    
    Example:
        >>> raise ExtractionError("Cannot open file", stage="open", original_error=e)
    """
    
    def __init__(self, message: str, stage: str = None, original_error: Exception = None):
        self.message = message
        self.stage = stage
        self.original_error = original_error
        super().__init__(self.message)
    
    def __str__(self):
        if self.stage:
            return f"[{self.stage}] {self.message}"
        return self.message


# =============================================================================
# PDF EXTRACTOR CLASS
# =============================================================================

class PDFExtractor:
    """
    Comprehensive PDF content extractor.
    
    Extracts text, images, metadata, structure, and annotations from PDF files.
    Designed for maximum fidelity - preserves all extractable information.
    
    Usage:
        >>> with PDFExtractor("document.pdf") as pdf:
        ...     content, method = pdf.extract_content()
        ...     images = pdf.extract_images("./output/images/")
        ...     metadata = pdf.get_pdf_metadata()
    
    The class supports context manager protocol for clean resource handling.
    
    Attributes:
        pdf_path: Path to the source PDF file
        doc: PyMuPDF document handle (available after opening)
        page_count: Total number of pages in the document
    """
    
    def __init__(self, pdf_path: str):
        """
        Initialize extractor with PDF path.
        
        Args:
            pdf_path: Path to the PDF file to extract
        
        Raises:
            ExtractionError: If file doesn't exist or isn't a valid PDF
        """
        self.pdf_path = Path(pdf_path).resolve()
        self.doc = None
        self.page_count = 0
        
        # Validate and open immediately
        self._validate_pdf()
        self._open_pdf()
    
    def _validate_pdf(self) -> None:
        """
        Validate that the file exists and appears to be a valid PDF.
        
        Checks:
        1. File exists
        2. File is readable
        3. File has PDF magic header (%PDF-)
        
        Raises:
            ExtractionError: If validation fails
        """
        if not self.pdf_path.exists():
            raise ExtractionError(
                f"File not found: {self.pdf_path}",
                stage="validation"
            )
        
        if not self.pdf_path.is_file():
            raise ExtractionError(
                f"Not a file: {self.pdf_path}",
                stage="validation"
            )
        
        # Check PDF magic header
        try:
            with open(self.pdf_path, 'rb') as f:
                header = f.read(5)
                if header != b'%PDF-':
                    raise ExtractionError(
                        f"Invalid PDF header (expected %PDF-, got {header!r})",
                        stage="validation"
                    )
        except PermissionError as e:
            raise ExtractionError(
                f"Permission denied: {self.pdf_path}",
                stage="validation",
                original_error=e
            )
        except IOError as e:
            raise ExtractionError(
                f"Cannot read file: {e}",
                stage="validation",
                original_error=e
            )
    
    def _open_pdf(self) -> None:
        """
        Open the PDF document with PyMuPDF.
        
        Raises:
            ExtractionError: If the document cannot be opened
        """
        try:
            self.doc = pymupdf.open(self.pdf_path)
            self.page_count = len(self.doc)
        except Exception as e:
            raise ExtractionError(
                f"Cannot open PDF: {e}",
                stage="open",
                original_error=e
            )
    
    def close(self) -> None:
        """Close the PDF document and release resources."""
        if self.doc:
            self.doc.close()
            self.doc = None
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures document is closed."""
        self.close()
        return False  # Don't suppress exceptions
    
    # -------------------------------------------------------------------------
    # Metadata Extraction Methods
    # -------------------------------------------------------------------------
    
    def get_file_metadata(self) -> Dict[str, Any]:
        """
        Get file-level metadata (not PDF internal metadata).
        
        Returns:
            Dictionary containing:
            - path: Absolute path to the file
            - filename: Just the filename
            - size_bytes: File size in bytes
            - size_human: Human-readable file size (e.g., "2.4 MB")
        
        Example:
            >>> pdf.get_file_metadata()
            {'path': '/path/to/doc.pdf', 'filename': 'doc.pdf', 
             'size_bytes': 2457600, 'size_human': '2.4 MB'}
        """
        size_bytes = self.pdf_path.stat().st_size
        
        # Convert to human-readable
        size_human = size_bytes
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_human < 1024:
                size_human = f"{size_human:.1f} {unit}"
                break
            size_human /= 1024
        else:
            size_human = f"{size_human:.1f} TB"
        
        return {
            "path": str(self.pdf_path),
            "filename": self.pdf_path.name,
            "size_bytes": size_bytes,
            "size_human": size_human
        }
    
    def get_pdf_metadata(self) -> Dict[str, Any]:
        """
        Extract PDF internal metadata.
        
        Returns:
            Dictionary containing standard PDF metadata fields:
            - title: Document title
            - author: Author name
            - subject: Document subject
            - keywords: Keywords string
            - creator: Application that created the document
            - producer: PDF producer (usually the PDF library)
            - creation_date: When the PDF was created (ISO format or raw)
            - modification_date: When the PDF was last modified
            - pdf_version: PDF specification version (e.g., "1.7")
            - page_count: Total number of pages
            - encrypted: Whether the PDF is encrypted
        
        Note:
            Dates are attempted to be parsed to ISO format. If parsing fails,
            the raw string is returned.
        """
        meta = self.doc.metadata
        
        def parse_pdf_date(date_str: str) -> str:
            """
            Attempt to parse PDF date format to ISO.
            
            PDF dates are typically in format: D:YYYYMMDDHHmmSS+HH'mm'
            Returns ISO format if parseable, otherwise returns raw string.
            """
            if not date_str:
                return ""
            
            # Remove 'D:' prefix if present
            if date_str.startswith("D:"):
                date_str = date_str[2:]
            
            try:
                # Try to parse basic format YYYYMMDDHHMMSS
                if len(date_str) >= 14:
                    dt = datetime.strptime(date_str[:14], "%Y%m%d%H%M%S")
                    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                elif len(date_str) >= 8:
                    dt = datetime.strptime(date_str[:8], "%Y%m%d")
                    return dt.strftime("%Y-%m-%d")
            except ValueError:
                pass
            
            return date_str  # Return raw if parsing fails
        
        # Extract PDF version from format field (e.g., "PDF 1.7" -> "1.7")
        format_str = meta.get("format", "")
        pdf_version = ""
        if format_str.startswith("PDF "):
            pdf_version = format_str[4:]  # Remove "PDF " prefix
        
        return {
            "title": meta.get("title", ""),
            "author": meta.get("author", ""),
            "subject": meta.get("subject", ""),
            "keywords": meta.get("keywords", ""),
            "creator": meta.get("creator", ""),
            "producer": meta.get("producer", ""),
            "creation_date": parse_pdf_date(meta.get("creationDate", "")),
            "modification_date": parse_pdf_date(meta.get("modDate", "")),
            "pdf_version": pdf_version,
            "page_count": self.page_count,
            "encrypted": self.doc.is_encrypted
        }
    
    def get_page_info(self) -> List[Dict[str, Any]]:
        """
        Get detailed information for each page.
        
        Returns:
            List of dictionaries, one per page, containing:
            - number: Page number (1-indexed)
            - width_pts: Width in points (72 pts = 1 inch)
            - height_pts: Height in points
            - width_mm: Width in millimetres
            - height_mm: Height in millimetres
            - rotation: Page rotation in degrees (0, 90, 180, 270)
            - has_text: Whether page contains extractable text
            - char_count: Approximate character count
            - has_images: Whether page contains images
            - image_count: Number of images on page
            - annotation_count: Number of annotations on page
        
        Note:
            This method iterates through all pages, which may be slow for
            very large documents. Consider caching the result if needed.
        """
        pages_info = []
        
        for i, page in enumerate(self.doc):
            rect = page.rect
            
            # Get text to check if page has content
            text = page.get_text()
            
            # Count images on this page
            image_list = page.get_images(full=True)
            
            # Count annotations
            annot_count = 0
            for _ in page.annots():
                annot_count += 1
            
            pages_info.append({
                "number": i + 1,
                "width_pts": round(rect.width, 2),
                "height_pts": round(rect.height, 2),
                "width_mm": round(rect.width * 25.4 / 72, 1),
                "height_mm": round(rect.height * 25.4 / 72, 1),
                "rotation": page.rotation,
                "has_text": bool(text.strip()),
                "char_count": len(text),
                "has_images": len(image_list) > 0,
                "image_count": len(image_list),
                "annotation_count": annot_count
            })
        
        return pages_info
    
    def get_outline(self) -> List[Dict[str, Any]]:
        """
        Extract document outline (bookmarks/table of contents).
        
        Returns:
            List of outline entries, each containing:
            - level: Nesting level (0 = top level)
            - title: Bookmark title text
            - page: Target page number (1-indexed), or None if external link
        
        Example:
            >>> pdf.get_outline()
            [
                {'level': 0, 'title': '1. Introduction', 'page': 1},
                {'level': 1, 'title': '1.1 Overview', 'page': 1},
                {'level': 1, 'title': '1.2 Objectives', 'page': 2},
                {'level': 0, 'title': '2. Main Content', 'page': 3}
            ]
        
        Note:
            Not all PDFs have an outline. Returns empty list if none exists.
        """
        outline = []
        toc = self.doc.get_toc(simple=True)  # Returns [level, title, page]
        
        for item in toc:
            level, title, page = item
            outline.append({
                "level": level - 1,  # Convert to 0-indexed
                "title": title,
                "page": page if page > 0 else None
            })
        
        return outline
    
    def get_annotations(self) -> List[Dict[str, Any]]:
        """
        Extract all annotations from the document.
        
        Captures comments, highlights, underlines, strikethroughs, sticky notes,
        and other annotation types.
        
        Returns:
            List of annotations, each containing:
            - page: Page number (1-indexed)
            - type: Annotation type (Highlight, Text, Underline, etc.)
            - content: Annotation content/comment text
            - subject: Annotation subject line (if any)
            - author: Who created the annotation
            - created: Creation date
            - modified: Last modification date
            - rect: Bounding box [x0, y0, x1, y1]
            - color: RGB color tuple if available
        
        Note:
            Annotations are often used for review comments and highlights.
            This data can help Claude understand which parts of the document
            were marked as important by previous readers.
        """
        annotations = []
        
        for page_num, page in enumerate(self.doc):
            for annot in page.annots():
                annot_info = {
                    "page": page_num + 1,
                    "type": annot.type[1] if annot.type else "Unknown",
                    "content": annot.info.get("content", ""),
                    "subject": annot.info.get("subject", ""),
                    "author": annot.info.get("title", ""),  # 'title' is actually author in PDF spec
                    "created": annot.info.get("creationDate", ""),
                    "modified": annot.info.get("modDate", ""),
                    "rect": list(annot.rect) if annot.rect else None
                }
                
                # Try to get color
                if annot.colors:
                    annot_info["color"] = annot.colors.get("stroke") or annot.colors.get("fill")
                
                annotations.append(annot_info)
        
        return annotations
    
    def get_links(self) -> List[Dict[str, Any]]:
        """
        Extract all hyperlinks from the document.
        
        Returns:
            List of links, each containing:
            - page: Page number (1-indexed)
            - type: Link type ('uri' for external, 'goto' for internal)
            - uri: URL for external links
            - target_page: Target page for internal links
            - rect: Bounding box [x0, y0, x1, y1]
            - text: Text in the link area (approximate)
        
        Note:
            Link text extraction is approximate as links don't directly
            store their display text. We extract text from the link's
            bounding box area.
        """
        links = []
        
        for page_num, page in enumerate(self.doc):
            page_links = page.get_links()
            
            for link in page_links:
                link_info = {
                    "page": page_num + 1,
                    "rect": list(link.get("from", [])),
                }
                
                # Determine link type and target
                if "uri" in link:
                    link_info["type"] = "uri"
                    link_info["uri"] = link["uri"]
                elif "page" in link:
                    link_info["type"] = "goto"
                    link_info["target_page"] = link["page"] + 1  # Convert to 1-indexed
                else:
                    link_info["type"] = "other"
                
                # Try to extract text from link area
                if link_info["rect"]:
                    try:
                        rect = pymupdf.Rect(link_info["rect"])
                        link_info["text"] = page.get_text("text", clip=rect).strip()
                    except:
                        link_info["text"] = ""
                
                links.append(link_info)
        
        return links
    
    def get_fonts(self) -> List[Dict[str, Any]]:
        """
        Extract font information from the document.
        
        Useful for understanding document structure - headers often use
        different fonts than body text.
        
        Returns:
            List of unique fonts, each containing:
            - name: Font name (e.g., "Arial-Bold")
            - type: Font type (TrueType, Type1, etc.)
            - encoding: Character encoding
            - pages_used: List of page numbers where font appears
        
        Note:
            This aggregates fonts across all pages. The same font appearing
            on multiple pages is reported once with all page numbers listed.
        """
        fonts_dict = {}  # font_name -> font_info
        
        for page_num, page in enumerate(self.doc):
            font_list = page.get_fonts(full=True)
            
            for font in font_list:
                # font = (xref, ext, type, basefont, name, encoding, ...)
                xref, ext, font_type, basefont, name, encoding = font[:6]
                
                font_name = name or basefont or f"Unknown-{xref}"
                
                if font_name not in fonts_dict:
                    fonts_dict[font_name] = {
                        "name": font_name,
                        "type": font_type,
                        "encoding": encoding,
                        "pages_used": []
                    }
                
                if page_num + 1 not in fonts_dict[font_name]["pages_used"]:
                    fonts_dict[font_name]["pages_used"].append(page_num + 1)
        
        return list(fonts_dict.values())
    
    # -------------------------------------------------------------------------
    # Content Extraction Methods
    # -------------------------------------------------------------------------
    
    def extract_images(self, output_folder: str) -> List[Dict[str, Any]]:
        """
        Extract all embedded images from the PDF.
        
        Saves images to the specified folder with consistent naming:
        page{NNN}_img{NNN}.{ext}
        
        Args:
            output_folder: Directory to save extracted images.
                          Will be created if it doesn't exist.
        
        Returns:
            List of image metadata, each containing:
            - id: Unique identifier (e.g., "page001_img001")
            - page: Source page number (1-indexed)
            - filename: Saved filename
            - filepath: Full path to saved file
            - width: Image width in pixels
            - height: Image height in pixels
            - colorspace: Color space (RGB, CMYK, Gray, etc.)
            - bits_per_component: Color depth
            - size_bytes: File size after saving
            - position: Bounding box on page [x0, y0, x1, y1]
        
        Notes:
            - Skips very small images (< MIN_IMAGE_WIDTH x MIN_IMAGE_HEIGHT)
              as these are often artifacts or spacers
            - Attempts to preserve original format (JPEG/PNG)
            - CMYK images are converted to RGB for compatibility
            - Returns empty list if no images found
        
        Example:
            >>> images = pdf.extract_images("./output/images/")
            >>> print(f"Extracted {len(images)} images")
        """
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
        
        extracted_images = []
        
        for page_num, page in enumerate(self.doc):
            image_list = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list):
                xref = img[0]  # Image reference number
                
                try:
                    # Extract image data
                    base_image = self.doc.extract_image(xref)
                    
                    if not base_image:
                        continue
                    
                    image_bytes = base_image["image"]
                    image_ext = base_image.get("ext", "png")
                    width = base_image.get("width", 0)
                    height = base_image.get("height", 0)
                    colorspace = base_image.get("colorspace", 0)
                    bpc = base_image.get("bpc", 8)
                    
                    # Skip tiny images (likely artifacts)
                    if width < MIN_IMAGE_WIDTH or height < MIN_IMAGE_HEIGHT:
                        continue
                    
                    # Generate filename
                    image_id = f"page{page_num + 1:03d}_img{img_index + 1:03d}"
                    filename = f"{image_id}.{image_ext}"
                    filepath = output_path / filename
                    
                    # Save image
                    with open(filepath, "wb") as f:
                        f.write(image_bytes)
                    
                    # Get image position on page (approximate from image rectangle)
                    # This requires finding where the image is placed
                    position = None
                    try:
                        for img_rect in page.get_image_rects(xref):
                            position = list(img_rect)
                            break
                    except:
                        pass
                    
                    # Determine colorspace name
                    cs_name = str(colorspace) if isinstance(colorspace, int) else colorspace
                    
                    extracted_images.append({
                        "id": image_id,
                        "page": page_num + 1,
                        "filename": filename,
                        "filepath": str(filepath),
                        "width": width,
                        "height": height,
                        "colorspace": cs_name,
                        "bits_per_component": bpc,
                        "size_bytes": len(image_bytes),
                        "position": position
                    })
                    
                except Exception as e:
                    # Log warning but continue with other images
                    print(f"Warning: Failed to extract image {xref} from page {page_num + 1}: {e}", 
                          file=sys.stderr)
                    continue
        
        return extracted_images
    
    def extract_text_pymupdf4llm(self, pages: Tuple[int, int] = None) -> str:
        """
        Extract text using pymupdf4llm (primary method).
        
        pymupdf4llm produces better markdown formatting, including:
        - Proper header detection
        - Table structure preservation
        - List formatting
        - Text styling (bold, italic)
        
        Args:
            pages: Optional tuple (start, end) for page range, 1-indexed.
                   Example: (1, 10) extracts pages 1 through 10.
                   None extracts all pages.
        
        Returns:
            Extracted markdown text.
        
        Raises:
            ExtractionError: If extraction fails.
        """
        try:
            kwargs = {}
            if pages:
                # pymupdf4llm uses 0-indexed page list
                kwargs['pages'] = list(range(pages[0] - 1, pages[1]))
            
            return pymupdf4llm.to_markdown(str(self.pdf_path), **kwargs)
        
        except Exception as e:
            raise ExtractionError(
                f"pymupdf4llm extraction failed: {e}",
                stage="extract",
                original_error=e
            )
    
    def extract_text_pymupdf(self, pages: Tuple[int, int] = None) -> str:
        """
        Extract text using basic pymupdf (fallback method).
        
        This method is more reliable for scanned documents or PDFs with
        unusual encoding, but produces simpler output without markdown
        formatting.
        
        Args:
            pages: Optional tuple (start, end) for page range, 1-indexed.
                   Example: (1, 10) extracts pages 1 through 10.
                   None extracts all pages.
        
        Returns:
            Extracted text with basic page markers.
        
        Note:
            Output format includes page markers:
            <!-- PAGE N START -->
            [page content]
            <!-- PAGE N END -->
        """
        if pages:
            start_page = pages[0] - 1  # Convert to 0-indexed
            end_page = pages[1]
        else:
            start_page = 0
            end_page = self.page_count
        
        text_parts = []
        
        for i in range(start_page, end_page):
            page = self.doc[i]
            page_text = page.get_text()
            
            # Add page markers
            text_parts.append(f"<!-- PAGE {i + 1} START -->")
            text_parts.append(page_text)
            text_parts.append(f"<!-- PAGE {i + 1} END -->")
            text_parts.append("")  # Blank line between pages
        
        return "\n".join(text_parts)
    
    def extract_content(self, pages: Tuple[int, int] = None, 
                        method: str = "auto") -> Tuple[str, str]:
        """
        Extract text content from PDF as markdown.
        
        This is the main extraction function. It attempts pymupdf4llm first
        (which produces better markdown formatting with tables and structure),
        then falls back to pymupdf if the result is too short (likely a
        scanned/image-based PDF that pymupdf4llm can't handle well).
        
        Args:
            pages: Optional tuple (start, end) for page range, 1-indexed.
                   Example: (1, 10) extracts pages 1-10.
                   None extracts all pages.
            method: Extraction method to use:
                   - "auto": Try pymupdf4llm, fallback to pymupdf if needed
                   - "pymupdf4llm": Force pymupdf4llm only
                   - "pymupdf": Force basic pymupdf only
        
        Returns:
            Tuple of (extracted_content: str, method_used: str)
            method_used indicates which extractor produced the result:
            - "pymupdf4llm": Primary method succeeded
            - "pymupdf": Basic method used (forced or fallback)
            - "pymupdf (fallback)": Fell back from pymupdf4llm
        
        Raises:
            ExtractionError: If extraction fails with all attempted methods.
        
        Example:
            >>> with PDFExtractor("doc.pdf") as pdf:
            ...     content, method = pdf.extract_content(pages=(1, 5))
            ...     print(f"Extracted with {method}")
        
        Notes for Claude skill usage:
            - The returned content is raw/unprocessed
            - Footer patterns, watermarks, etc. are preserved
            - Claude should post-process to clean up repeated elements
            - Use insert_image_markers() to add image references
        """
        if method == "pymupdf":
            return self.extract_text_pymupdf(pages), "pymupdf"
        
        elif method == "pymupdf4llm":
            return self.extract_text_pymupdf4llm(pages), "pymupdf4llm"
        
        else:  # auto
            try:
                text = self.extract_text_pymupdf4llm(pages)
                
                # Check if we got meaningful content
                if len(text.strip()) >= FALLBACK_THRESHOLD:
                    return text, "pymupdf4llm"
                
                # Try fallback
                text_fallback = self.extract_text_pymupdf(pages)
                
                # Use whichever got more content
                if len(text_fallback.strip()) > len(text.strip()):
                    return text_fallback, "pymupdf (fallback)"
                
                return text, "pymupdf4llm"
            
            except ExtractionError:
                # pymupdf4llm failed, try fallback
                try:
                    return self.extract_text_pymupdf(pages), "pymupdf (fallback)"
                except Exception as e:
                    raise ExtractionError(
                        f"All extraction methods failed: {e}",
                        stage="extract",
                        original_error=e
                    )


# =============================================================================
# OUTPUT BUILDING FUNCTIONS
# =============================================================================

def insert_image_markers(content: str, images: List[Dict[str, Any]]) -> str:
    """
    Insert image reference markers into the extracted content.
    
    Adds HTML comments indicating where images should appear. Since exact
    positioning is difficult, images are grouped by page and listed at
    page boundaries.
    
    Args:
        content: Extracted markdown content
        images: List of image metadata from extract_images()
    
    Returns:
        Content with image markers inserted.
    
    Note:
        Markers are HTML comments so they don't affect rendering:
        <!-- IMAGE: images/page001_img001.png (400x300px) -->
    """
    if not images:
        return content
    
    # Group images by page
    images_by_page = {}
    for img in images:
        page = img["page"]
        if page not in images_by_page:
            images_by_page[page] = []
        images_by_page[page].append(img)
    
    # Build image marker strings for each page
    lines = content.split('\n')
    result_lines = []
    current_page = 0
    
    for line in lines:
        result_lines.append(line)
        
        # Check if this is a page marker
        if line.startswith("<!-- PAGE ") and "START" in line:
            try:
                page_num = int(line.split()[2])
                current_page = page_num
                
                # Add image markers for this page
                if page_num in images_by_page:
                    result_lines.append("")
                    result_lines.append(f"<!-- IMAGES ON PAGE {page_num}: -->")
                    for img in images_by_page[page_num]:
                        marker = f"<!-- IMAGE: {img['filename']} ({img['width']}x{img['height']}px) -->"
                        result_lines.append(marker)
                    result_lines.append("")
            except (ValueError, IndexError):
                pass
    
    return '\n'.join(result_lines)


def build_yaml_header(
    file_meta: Dict[str, Any],
    pdf_meta: Dict[str, Any],
    extraction_info: Dict[str, Any],
    structure_info: Dict[str, Any]
) -> str:
    """
    Build YAML frontmatter header for the markdown output.
    
    Creates a comprehensive metadata block at the top of the markdown file.
    Uses YAML format for easy parsing.
    
    Args:
        file_meta: From get_file_metadata()
        pdf_meta: From get_pdf_metadata()
        extraction_info: Extraction method, date, pages, etc.
        structure_info: Outline, annotations, images counts, etc.
    
    Returns:
        YAML frontmatter string including --- delimiters.
    """
    lines = ["---"]
    
    # Extraction information
    lines.append("# Extraction Information")
    lines.append(f"source_file: \"{file_meta['filename']}\"")
    lines.append(f"source_path: \"{file_meta['path']}\"")
    lines.append(f"extraction_date: \"{extraction_info['date']}\"")
    lines.append(f"extraction_method: \"{extraction_info['method']}\"")
    if extraction_info.get('pages'):
        lines.append(f"extracted_pages: \"{extraction_info['pages'][0]}-{extraction_info['pages'][1]}\"")
    else:
        lines.append(f"extracted_pages: \"1-{pdf_meta['page_count']}\"")
    lines.append(f"script_version: \"{VERSION}\"")
    lines.append("")
    
    # File information
    lines.append("# File Information")
    lines.append(f"file_size_bytes: {file_meta['size_bytes']}")
    lines.append(f"file_size_human: \"{file_meta['size_human']}\"")
    lines.append(f"total_pages: {pdf_meta['page_count']}")
    if pdf_meta.get('pdf_version'):
        lines.append(f"pdf_version: \"{pdf_meta['pdf_version']}\"")
    lines.append("")
    
    # PDF metadata
    lines.append("# PDF Metadata")
    if pdf_meta.get('title'):
        lines.append(f"pdf_title: \"{pdf_meta['title']}\"")
    if pdf_meta.get('author'):
        lines.append(f"pdf_author: \"{pdf_meta['author']}\"")
    if pdf_meta.get('subject'):
        lines.append(f"pdf_subject: \"{pdf_meta['subject']}\"")
    if pdf_meta.get('creator'):
        lines.append(f"pdf_creator: \"{pdf_meta['creator']}\"")
    if pdf_meta.get('producer'):
        lines.append(f"pdf_producer: \"{pdf_meta['producer']}\"")
    if pdf_meta.get('creation_date'):
        lines.append(f"pdf_creation_date: \"{pdf_meta['creation_date']}\"")
    if pdf_meta.get('modification_date'):
        lines.append(f"pdf_modification_date: \"{pdf_meta['modification_date']}\"")
    lines.append("")
    
    # Structure information
    lines.append("# Document Structure")
    lines.append(f"has_outline: {str(structure_info.get('has_outline', False)).lower()}")
    lines.append(f"outline_items: {structure_info.get('outline_count', 0)}")
    lines.append(f"has_annotations: {str(structure_info.get('has_annotations', False)).lower()}")
    lines.append(f"annotation_count: {structure_info.get('annotation_count', 0)}")
    lines.append(f"has_links: {str(structure_info.get('has_links', False)).lower()}")
    lines.append(f"link_count: {structure_info.get('link_count', 0)}")
    lines.append(f"total_images: {structure_info.get('image_count', 0)}")
    if structure_info.get('image_count', 0) > 0:
        lines.append(f"image_folder: \"./images/\"")
    
    lines.append("---")
    return '\n'.join(lines)


def build_outline_section(outline: List[Dict[str, Any]]) -> str:
    """
    Build markdown section displaying the document outline.
    
    Args:
        outline: From get_outline()
    
    Returns:
        Markdown formatted outline section, or empty string if no outline.
    """
    if not outline:
        return ""
    
    lines = ["", "# Document Outline (Bookmarks)", ""]
    
    for item in outline:
        indent = "  " * item["level"]
        page_ref = f" [page {item['page']}]" if item['page'] else ""
        lines.append(f"{indent}- {item['title']}{page_ref}")
    
    lines.append("")
    return '\n'.join(lines)


def build_annotations_section(annotations: List[Dict[str, Any]]) -> str:
    """
    Build markdown section displaying annotations.
    
    Args:
        annotations: From get_annotations()
    
    Returns:
        Markdown formatted annotations table, or empty string if none.
    """
    if not annotations:
        return ""
    
    lines = ["", "# Annotations", ""]
    lines.append("| Page | Type | Content | Author |")
    lines.append("|------|------|---------|--------|")
    
    for annot in annotations:
        content = annot.get('content', '').replace('\n', ' ').strip()
        if len(content) > 50:
            content = content[:47] + "..."
        content = content.replace('|', '\\|')  # Escape pipes
        
        author = annot.get('author', '')
        
        lines.append(f"| {annot['page']} | {annot['type']} | {content} | {author} |")
    
    lines.append("")
    return '\n'.join(lines)


def build_links_section(links: List[Dict[str, Any]]) -> str:
    """
    Build markdown section displaying hyperlinks.
    
    Args:
        links: From get_links()
    
    Returns:
        Markdown formatted links table, or empty string if none.
    """
    # Filter to only external links with URIs
    external_links = [l for l in links if l.get('type') == 'uri' and l.get('uri')]
    
    if not external_links:
        return ""
    
    lines = ["", "# Hyperlinks", ""]
    lines.append("| Page | Text | URL |")
    lines.append("|------|------|-----|")
    
    for link in external_links:
        text = link.get('text', '').replace('\n', ' ').strip()
        if len(text) > 40:
            text = text[:37] + "..."
        text = text.replace('|', '\\|')
        
        uri = link.get('uri', '')
        if len(uri) > 60:
            uri = uri[:57] + "..."
        
        lines.append(f"| {link['page']} | {text} | {uri} |")
    
    lines.append("")
    return '\n'.join(lines)


def build_full_markdown(
    content: str,
    file_meta: Dict[str, Any],
    pdf_meta: Dict[str, Any],
    extraction_info: Dict[str, Any],
    outline: List[Dict[str, Any]],
    annotations: List[Dict[str, Any]],
    links: List[Dict[str, Any]],
    images: List[Dict[str, Any]]
) -> str:
    """
    Build the complete markdown output file.
    
    Combines all sections:
    1. YAML frontmatter with metadata
    2. Document outline (if present)
    3. Annotations table (if present)
    4. Hyperlinks table (if present)
    5. Main extracted content
    
    Args:
        content: Extracted text content
        file_meta: File metadata
        pdf_meta: PDF internal metadata
        extraction_info: Extraction details
        outline: Document outline
        annotations: Annotation list
        links: Hyperlink list
        images: Extracted image list
    
    Returns:
        Complete markdown document as string.
    """
    # Calculate structure info for header
    structure_info = {
        "has_outline": len(outline) > 0,
        "outline_count": len(outline),
        "has_annotations": len(annotations) > 0,
        "annotation_count": len(annotations),
        "has_links": len([l for l in links if l.get('type') == 'uri']) > 0,
        "link_count": len([l for l in links if l.get('type') == 'uri']),
        "image_count": len(images)
    }
    
    # Build sections
    parts = []
    
    # YAML header
    parts.append(build_yaml_header(file_meta, pdf_meta, extraction_info, structure_info))
    
    # Outline
    outline_section = build_outline_section(outline)
    if outline_section:
        parts.append(outline_section)
    
    # Annotations
    annotations_section = build_annotations_section(annotations)
    if annotations_section:
        parts.append(annotations_section)
    
    # Links
    links_section = build_links_section(links)
    if links_section:
        parts.append(links_section)
    
    # Separator before main content
    parts.append("")
    parts.append("---")
    parts.append("")
    parts.append("# Extracted Content")
    parts.append("")
    
    # Main content with image markers
    content_with_images = insert_image_markers(content, images)
    parts.append(content_with_images)
    
    return '\n'.join(parts)


def build_metadata_json(
    file_meta: Dict[str, Any],
    pdf_meta: Dict[str, Any],
    extraction_info: Dict[str, Any],
    pages_info: List[Dict[str, Any]],
    outline: List[Dict[str, Any]],
    annotations: List[Dict[str, Any]],
    links: List[Dict[str, Any]],
    fonts: List[Dict[str, Any]],
    images: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Build the complete metadata JSON structure.
    
    Creates a comprehensive JSON object containing all extracted metadata.
    This can be used programmatically by Claude or other tools.
    
    Returns:
        Complete metadata dictionary ready for JSON serialization.
    """
    return {
        "extraction": {
            "source_file": file_meta["filename"],
            "source_path": file_meta["path"],
            "output_folder": extraction_info.get("output_folder", ""),
            "extraction_date": extraction_info["date"],
            "extraction_method": extraction_info["method"],
            "extracted_pages": extraction_info.get("pages"),
            "script_version": VERSION,
            "pymupdf_version": pymupdf.version[0],
        },
        "file": {
            "size_bytes": file_meta["size_bytes"],
            "size_human": file_meta["size_human"],
            "page_count": pdf_meta["page_count"],
            "pdf_version": pdf_meta.get("pdf_version", "")
        },
        "pdf_metadata": {
            "title": pdf_meta.get("title", ""),
            "author": pdf_meta.get("author", ""),
            "subject": pdf_meta.get("subject", ""),
            "keywords": pdf_meta.get("keywords", ""),
            "creator": pdf_meta.get("creator", ""),
            "producer": pdf_meta.get("producer", ""),
            "creation_date": pdf_meta.get("creation_date", ""),
            "modification_date": pdf_meta.get("modification_date", ""),
            "encrypted": pdf_meta.get("encrypted", False)
        },
        "structure": {
            "has_outline": len(outline) > 0,
            "outline_items": len(outline),
            "has_annotations": len(annotations) > 0,
            "annotation_count": len(annotations),
            "has_links": len(links) > 0,
            "link_count": len(links),
            "has_images": len(images) > 0,
            "image_count": len(images),
            "font_count": len(fonts)
        },
        "pages": pages_info,
        "outline": outline,
        "annotations": annotations,
        "links": links,
        "fonts": fonts,
        "images": images
    }


# =============================================================================
# MAIN FUNCTION
# =============================================================================

def main():
    """
    Main entry point for the PDF extraction script.
    
    Parses command-line arguments, runs the extraction pipeline,
    and saves output files.
    
    Exit codes:
        0: Success
        1: Error (message printed to stderr)
    """
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Extract PDF content to markdown with maximum fidelity.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python extract_pdf.py document.pdf
  python extract_pdf.py document.pdf ./output/
  python extract_pdf.py document.pdf --pages 1-10
  python extract_pdf.py document.pdf --method pymupdf

Output:
  Creates a folder containing:
  - {filename}.md      Main extracted markdown
  - metadata.json      Structured metadata
  - images/            Extracted images (if any)
        """
    )
    
    parser.add_argument(
        "input_pdf",
        help="Path to the PDF file to extract"
    )
    
    parser.add_argument(
        "output_folder",
        nargs="?",
        default=None,
        help="Output folder (default: {input_name}_extracted/)"
    )
    
    parser.add_argument(
        "--pages",
        type=str,
        default=None,
        metavar="START-END",
        help="Page range to extract, e.g., '1-10' (default: all pages)"
    )
    
    parser.add_argument(
        "--method",
        choices=["auto", "pymupdf4llm", "pymupdf"],
        default="auto",
        help="Extraction method (default: auto)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}"
    )
    
    args = parser.parse_args()
    
    # Parse page range
    pages = None
    if args.pages:
        try:
            parts = args.pages.split("-")
            if len(parts) == 2:
                pages = (int(parts[0]), int(parts[1]))
            else:
                print(f"Error: Invalid page range format: {args.pages}", file=sys.stderr)
                print("Use format: START-END (e.g., 1-10)", file=sys.stderr)
                sys.exit(1)
        except ValueError:
            print(f"Error: Invalid page range: {args.pages}", file=sys.stderr)
            sys.exit(1)
    
    # Determine output folder
    input_path = Path(args.input_pdf)
    if args.output_folder:
        output_folder = Path(args.output_folder)
    else:
        output_folder = input_path.parent / f"{input_path.stem}_extracted"
    
    # Create output folder
    output_folder.mkdir(parents=True, exist_ok=True)
    images_folder = output_folder / "images"
    
    print(f"PDF Extractor v{VERSION}")
    print(f"Input: {input_path}")
    print(f"Output: {output_folder}")
    print()
    
    try:
        # Open and extract
        with PDFExtractor(str(input_path)) as pdf:
            print(f"Opened PDF: {pdf.page_count} pages")
            
            # Get all metadata
            print("Extracting metadata...")
            file_meta = pdf.get_file_metadata()
            pdf_meta = pdf.get_pdf_metadata()
            pages_info = pdf.get_page_info()
            outline = pdf.get_outline()
            annotations = pdf.get_annotations()
            links = pdf.get_links()
            fonts = pdf.get_fonts()
            
            print(f"  - Outline items: {len(outline)}")
            print(f"  - Annotations: {len(annotations)}")
            print(f"  - Links: {len(links)}")
            print(f"  - Fonts: {len(fonts)}")
            
            # Extract images
            print("Extracting images...")
            images = pdf.extract_images(str(images_folder))
            print(f"  - Images extracted: {len(images)}")
            
            # Remove images folder if empty
            if not images:
                try:
                    images_folder.rmdir()
                except:
                    pass
            
            # Extract content
            print(f"Extracting content (method: {args.method})...")
            content, method_used = pdf.extract_content(pages=pages, method=args.method)
            print(f"  - Method used: {method_used}")
            print(f"  - Content length: {len(content):,} characters")
        
        # Build extraction info
        extraction_info = {
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "method": method_used,
            "pages": pages,
            "output_folder": str(output_folder)
        }
        
        # Build and save markdown
        print("Building output files...")
        markdown_content = build_full_markdown(
            content=content,
            file_meta=file_meta,
            pdf_meta=pdf_meta,
            extraction_info=extraction_info,
            outline=outline,
            annotations=annotations,
            links=links,
            images=images
        )
        
        md_path = output_folder / f"{input_path.stem}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"  - Saved: {md_path.name}")
        
        # Build and save metadata JSON
        metadata = build_metadata_json(
            file_meta=file_meta,
            pdf_meta=pdf_meta,
            extraction_info=extraction_info,
            pages_info=pages_info,
            outline=outline,
            annotations=annotations,
            links=links,
            fonts=fonts,
            images=images
        )
        
        json_path = output_folder / "metadata.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        print(f"  - Saved: {json_path.name}")
        
        # Summary
        print()
        print("Extraction complete!")
        print(f"  Output folder: {output_folder}")
        print(f"  Markdown file: {md_path.name}")
        print(f"  Metadata file: {json_path.name}")
        if images:
            print(f"  Images folder: images/ ({len(images)} files)")
        
        sys.exit(0)
        
    except ExtractionError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
