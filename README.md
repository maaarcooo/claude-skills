# Claude Skills

A collection of Claude Agentic Skills for intelligent document processing, study material generation, and PDF extraction.

## Overview

This repository contains specialized skills that enable Claude to process documents and generate study materials. Skills include PDF-to-markdown conversion, Anki flashcard generation, and revision notes creation.

## Skills Overview

| Skill | Purpose | Status |
|-------|---------|--------|
| [extracting-pdfs](#extracting-pdfs) | Extract and clean PDF content to markdown | Active |
| [anki-flashcard-generator](#anki-flashcard-generator) | Generate Anki-importable flashcard decks | Active |
| [revision-notes-generator](#revision-notes-generator) | Create concise revision notes from study materials | Active |

### Archived Skills

| Skill | Purpose | Status |
|-------|---------|--------|
| [pdf-extract](#pdf-extract) | PDF extraction (development version) | Archived |
| [pdf-to-markdown-converter](#pdf-to-markdown-converter) | Legacy PDF conversion | Archived |

## Project Structure

```
claude-skills/
├── README.md
├── extracting-pdfs/                    # PDF extraction skill (Active)
│   ├── SKILL.md                        # Skill definition & workflow
│   ├── cleanup-patterns.md             # Reference: noise patterns to remove
│   ├── image-handling.md               # Reference: processing extracted images
│   ├── sentence-reflow.md              # Reference: fixing fragmented text
│   └── table-formatting.md             # Reference: reconstructing malformed tables
├── anki-flashcard-generator/           # Anki flashcard generation skill
│   └── SKILL.md
├── revision-notes-generator/           # Revision notes generation skill
│   └── SKILL.md
└── archive/                            # Archived/legacy skills
    ├── pdf-extract/                    # PDF extraction (development version)
    │   ├── SKILL.md
    │   ├── extract_pdf.py              # Core Python extraction script
    │   ├── cleanup-patterns.md
    │   ├── image-handling.md
    │   ├── sentence-reflow.md
    │   └── table-formatting.md
    └── pdf-to-markdown-converter/      # Legacy skill (Deprecated)
        └── SKILL.md
```

## Skills

### Extracting PDFs

The primary skill for extracting PDF content to clean, organized markdown format. This is the production-ready version with a sophisticated multi-step workflow.

**Trigger:** When a user uploads a PDF and wants to convert it to markdown.

**Workflow:**

1. **Extract** — Run Python script to get raw content and metadata
2. **Analyse** — Review extracted content for patterns and issues
3. **Clean** — Manually rewrite to remove noise (no automated scripts)
4. **Organise** — Apply formatting with proper heading hierarchy
5. **Output** — Deliver clean markdown with images

**Key Features:**

- Dual extraction methods with automatic fallback
  - `pymupdf4llm`: Primary method for better markdown/table formatting
  - `pymupdf`: Fallback for scanned/image-based PDFs
- Comprehensive image extraction with filtering
- Rich metadata extraction (YAML frontmatter + JSON)
- Reference guides for handling common extraction challenges

**Prompt:**

```
<pathname>
Use "extracting-pdfs" skill to convert this pdf into a markdown file.
```

---

### Anki Flashcard Generator

> **Source:** Converted from [anki-flashcard/prompt-v4.txt](https://github.com/maaarcooo/llm-custom-instructions/blob/main/anki-flashcard/prompt-v4.txt)

Generate study flashcards from PDF or Markdown content in Anki-importable format.

**Trigger:** Only when "Anki flashcard" or "Anki deck" is explicitly mentioned.

**Process:**

1. Read the source file (PDF or Markdown) thoroughly
2. Identify key content: bolded terms, highlighted text, Higher Tier material
3. Generate atomic flashcards covering essential topic content
4. Output as text file with `Question | Answer` format

**Card Design Rules:**

- **Atomic**: One fact per card
- **Concise**: Simple, direct language
- **Reverse cards**: Both directions for key definitions
- **No visuals**: Excludes questions requiring diagrams

**Output Format:**

```
What is the unit of electrical resistance? | Ohm (Ω)
Define specific heat capacity | The energy required to raise the temperature of 1 kg of a substance by 1°C
```

---

### Revision Notes Generator

> **Source:** Converted from [revision-notes/prompt-v2.txt](https://github.com/maaarcooo/llm-custom-instructions/blob/main/revision-notes/prompt-v2.txt)

Generate concise, accurate revision notes from PDF or Markdown content.

**Trigger:** When asked to create revision notes, study notes, topic summaries, or condensed notes.

**Process:**

1. Read the source file thoroughly
2. Identify key content and Higher Tier material
3. Verify accuracy of all information
4. Write concise notes covering essential knowledge
5. Output as structured markdown file

**Writing Guidelines:**

- **Concise**: Condense to essential points
- **Complete**: Cover all necessary knowledge
- **Accurate**: Cross-check and correct errors
- **Structured**: Clear headings and logical organisation
- **Higher Tier**: Include and optionally mark with (HT)

**Output Format:** Markdown with title, section headings, bold key terms, and equations in code blocks.

---

## Archived Skills

The following skills have been moved to the `archive/` folder. They are preserved for reference but are no longer actively maintained.

---

### PDF Extract

> **Location:** `archive/pdf-extract/`

The development/original version of the PDF extraction skill. Contains the core Python extraction script.

> **Note:** For production use, see [extracting-pdfs](#extracting-pdfs) which is the current active version.

**Features:**

- Same extraction capabilities as extracting-pdfs
- Contains `extract_pdf.py` script (1,500+ lines)
- Full reference documentation included

---

### PDF to Markdown Converter

> **Location:** `archive/pdf-to-markdown-converter/`

The original PDF conversion skill using visual PDF understanding.

> **Status:** Deprecated. Superseded by the more sophisticated `extracting-pdfs` skill.

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

The PDF extraction skills include reference guides for handling common challenges:

| Document | Purpose |
|----------|---------|
| `cleanup-patterns.md` | Identifies noise patterns: headers, footers, page numbers, watermarks |
| `sentence-reflow.md` | Techniques for fixing fragmented text across line/page breaks |
| `table-formatting.md` | Methods for reconstructing malformed tables |
| `image-handling.md` | Guide for processing and positioning extracted images |

## Design Philosophy

- **Extract everything** — No hardcoded cleanup rules during extraction
- **Preserve raw content** — Keep data intact for intelligent post-processing
- **Rich metadata** — Provide comprehensive context for document understanding
- **Manual over automated** — Complex decisions handled manually for better results
- **Atomic flashcards** — One fact per card for effective learning
- **Accuracy first** — Verify and correct information in study materials

## Technologies

- **Python 3** — Core scripting language
- **PyMuPDF (fitz)** — Low-level PDF reading and image extraction
- **PyMuPDF4LLM** — Enhanced markdown formatting with table support
- **YAML/JSON** — Metadata formats
- **Markdown** — Output format

## Versioning

This repository uses unified versioning. All skills share a single version number. See [Releases](../../releases) for version history.

## License

This work is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) - you're free to share and adapt with attribution.
