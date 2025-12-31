# Claude-Skills

A collection of Claude AI skills for intelligent PDF document processing and extraction.

## Overview

This repository contains specialized skills that enable Claude to extract content from PDF documents and convert them to clean, readable markdown format. The skills provide automated extraction combined with intelligent manual cleanup workflows.

## Project Structure

```
claude-skills/
├── README.md
├── pdf-extract/                        # Main PDF extraction skill (Active)
│   ├── SKILL.md                        # Skill definition & workflow
│   ├── extract_pdf.py                  # Core Python extraction script
│   ├── cleanup-patterns.md             # Reference: noise patterns to remove
│   ├── image-handling.md               # Reference: processing extracted images
│   ├── sentence-reflow.md              # Reference: fixing fragmented text
│   └── table-formatting.md             # Reference: reconstructing malformed tables
└── pdf-to-markdown-converter/          # Legacy skill (Deprecated)
    └── SKILL.md
```

## Skills

### PDF Extract (Active)

The primary skill for extracting PDF content to markdown format with a sophisticated multi-step workflow.

**Workflow Stages:**

1. **Extract** — Automated Python script extracts raw content and metadata
2. **Analyse** — Review extracted content for patterns and issues
3. **Clean** — Manual rewriting to remove noise without scripts
4. **Organise** — Structure content with proper heading hierarchy
5. **Output** — Deliver clean markdown with images and metadata

**Key Features:**

- Dual extraction methods with automatic fallback
  - `pymupdf4llm`: Primary method for better markdown/table formatting
  - `pymupdf`: Fallback for scanned/image-based PDFs
- Comprehensive image extraction with filtering
- Rich metadata extraction (YAML frontmatter + JSON)
- Document structure preservation (outlines, annotations, links)

### PDF to Markdown Converter (Legacy)

The original PDF conversion skill, now superseded by the more sophisticated `pdf-extract` skill.

## Dependencies

```bash
pip install pymupdf pymupdf4llm
```

## Usage

### Command Line

```bash
python pdf-extract/extract_pdf.py <input_pdf> [output_folder] [options]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--pages START-END` | Extract specific page range |
| `--method {auto\|pymupdf4llm\|pymupdf}` | Force extraction method |
| `--min-image-size PIXELS` | Filter small images (default: 10) |
| `--version` | Show script version |

### Output Structure

```
output_folder/
├── {filename}.md       # Markdown with YAML frontmatter
├── metadata.json       # Full extraction metadata
└── images/             # Extracted images
```

## Reference Documentation

The `pdf-extract` skill includes reference guides for handling common extraction challenges:

| Document | Purpose |
|----------|---------|
| `cleanup-patterns.md` | Identifies noise patterns like headers, footers, page numbers, watermarks |
| `sentence-reflow.md` | Techniques for fixing fragmented text across line/page breaks |
| `table-formatting.md` | Methods for reconstructing malformed tables |
| `image-handling.md` | Guide for processing and positioning extracted images |

## Design Philosophy

- **Extract everything** — No hardcoded cleanup rules during extraction
- **Preserve raw content** — Keep data intact for intelligent post-processing
- **Rich metadata** — Provide comprehensive context for document understanding
- **Manual over automated** — Complex decisions are handled manually for better results

## Technologies

- **Python 3** — Core scripting language
- **PyMuPDF (fitz)** — Low-level PDF reading and image extraction
- **PyMuPDF4LLM** — Enhanced markdown formatting with table support
- **YAML/JSON** — Metadata formats
- **Markdown** — Output format
