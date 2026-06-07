# Extracting PDFs

Extract and clean PDF content to organized markdown format.

## The Problem

PDFs are hostile to structured data extraction. Content arrives with repeated headers, footers, watermarks, and page numbers scattered throughout. Sentences fragment across line breaks and page boundaries. Tables lose their structure. Images need to be extracted, filtered, and repositioned. Automated cleanup rules miss context-dependent issues, producing output that still needs significant manual correction.

## The Solution

A 5-step workflow that combines automated extraction with manual, context-aware cleanup. Rather than trying to automate everything, the skill uses Python for reliable raw extraction and then applies intelligent manual rewriting for the parts that require human-level judgement — noise removal, sentence reflow, table reconstruction, and heading hierarchy.

Two extraction methods are available with automatic fallback, so both text-based and scanned/image-based PDFs are handled.

## Key Features

- **Dual extraction methods** — `pymupdf4llm` as primary (better markdown/table formatting), `pymupdf` as fallback (for scanned/image-based PDFs)
- **Comprehensive image extraction** — Filters by size, extracts to a dedicated folder, converts references to markdown image syntax
- **Rich metadata** — YAML frontmatter and JSON metadata for every extraction
- **Reference guides** — Four supplementary documents covering common extraction challenges (cleanup patterns, sentence reflow, table formatting, image handling)
- **Manual over automated** — Complex cleanup decisions handled manually for better results

## When to Use

When a user uploads a PDF and wants to convert it to clean, readable markdown. The skill handles textbooks, research papers, reports, and any document where preserving structure and accuracy matters.

## How It Works

1. **Extract** — Run the Python script to get raw content, metadata, and images
2. **Analyse** — Review the YAML frontmatter and identify noise patterns, structural issues, and content that needs attention
3. **Clean** — Manually rewrite to remove noise (no automated scripts) — use reference guides for common patterns
4. **Organise** — Apply proper heading hierarchy, paragraph flow, and image placement
5. **Output** — Deliver clean markdown with images, validated against a quality checklist

## Dependencies

```bash
pip install pymupdf pymupdf4llm
```

## Usage

### PDF Extraction (Command Line)

```bash
python extract_pdf.py <input_pdf> [output_folder] [options]
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

The skill includes reference guides for handling common extraction challenges:

| Document | Purpose |
|----------|---------|
| `cleanup-patterns.md` | Identifies noise patterns: headers, footers, page numbers, watermarks |
| `sentence-reflow.md` | Techniques for fixing fragmented text across line/page breaks |
| `table-formatting.md` | Methods for reconstructing malformed tables |
| `image-handling.md` | Guide for processing and positioning extracted images |

## Sample Prompt

```
<pathname>
Use "extracting-pdfs" skill to convert this pdf into a markdown file.
```

## Installation

Place the skill files in your Claude skills directory:

```
skills/
└── extracting-pdfs/
    ├── SKILL.md
    ├── cleanup-patterns.md
    ├── image-handling.md
    ├── sentence-reflow.md
    └── table-formatting.md
```

Then trigger by uploading a PDF and asking Claude to extract it.
