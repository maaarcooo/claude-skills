# Claude Skills

A collection of Claude Agentic Skills for intelligent document processing, study material generation, PDF extraction, and session continuity.

## Overview

This repository contains specialized skills for Claude and Claude Code. Skills are organized into two categories: **General Claude Skills** for document processing, study material generation, and session handoff (works in any Claude interface) and **Claude Code Skills** providing slash commands for session continuity in the Claude Code CLI.

## Skills Overview

### General Claude Skills

| Skill | Purpose | Status |
|-------|---------|--------|
| [extracting-pdfs](#extracting-pdfs) | Extract and clean PDF content to markdown | Active |
| [anki-flashcard-generator](#anki-flashcard-generator) | Generate Anki-importable flashcard decks | Active |
| [revision-notes-generator](#revision-notes-generator) | Create concise revision notes from study materials | Active |
| [handoff](#handoff) | Create structured handoff documents for session continuity | Active |

### Claude Code Skills

| Skill | Purpose | Status |
|-------|---------|--------|
| [handoff (Claude Code)](#handoff-claude-code) | `/handoff` slash command for session handoff | Active |
| [resume](#resume) | `/resume` slash command to continue from a handoff | Active |

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
│   ├── README.md                       # Skill documentation
│   ├── SKILL.md                        # Skill definition & workflow
│   ├── cleanup-patterns.md             # Reference: noise patterns to remove
│   ├── image-handling.md               # Reference: processing extracted images
│   ├── sentence-reflow.md              # Reference: fixing fragmented text
│   └── table-formatting.md             # Reference: reconstructing malformed tables
├── anki-flashcard-generator/           # Anki flashcard generation skill
│   ├── README.md                       # Skill documentation
│   └── SKILL.md
├── revision-notes-generator/           # Revision notes generation skill
│   ├── README.md                       # Skill documentation
│   └── SKILL.md
├── handoff/                            # Session handoff skill (General Claude)
│   ├── README.md
│   └── SKILL.md
├── claude-code-skills/                 # Claude Code slash commands
│   ├── handoff/                        # /handoff command
│   │   ├── README.md
│   │   └── SKILL.md
│   └── resume/                         # /resume command
│       ├── README.md
│       └── SKILL.md
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

The primary skill for extracting PDF content to clean, organized markdown. Uses a 5-step workflow (Extract, Analyse, Clean, Organise, Output) with dual extraction methods, comprehensive image handling, and reference guides for common challenges.

> **Full documentation:** See [`extracting-pdfs/README.md`](extracting-pdfs/README.md) for the complete workflow, CLI usage, dependencies, and reference guide details.

**Sample prompt:**

```
<pathname>
Use "extracting-pdfs" skill to convert this pdf into a markdown file.
```

---

### Anki Flashcard Generator

Generate study flashcards from PDF or Markdown content in Anki-importable format. Card design follows evidence-based principles with six specialised card types, built-in interference checking, and coverage guidance prioritised by examinability.

> **Full documentation:** See [`anki-flashcard-generator/README.md`](anki-flashcard-generator/README.md) for design principles, card types, output format, and card design rules.

**Sample prompt for claude.ai:**

```
Use "anki-flashcard-generator" skill to create an Anki flashcard deck of the study materials.
Output the flashcards as a text file. Name the file after the source file (e.g., Physics_Chapter_5.pdf → Physics_Chapter_5.txt).
```

**Sample prompt for Claude API:**

```
Use "anki-flashcard-generator" skill to create an Anki flashcard deck of the study materials.
Output only the flashcard lines in the format "Question | Answer", one per line.
Do not include any preamble, headers, explanations, markdown formatting,
or code fences. The raw output will be saved directly to a text file.
```

---

### Revision Notes Generator

Generate concise, accurate revision notes from PDF or Markdown study materials. Covers a 5-step process from reading through verification to structured markdown output, with writing guidelines prioritising conciseness, completeness, and accuracy.

> **Full documentation:** See [`revision-notes-generator/README.md`](revision-notes-generator/README.md) for writing guidelines, output format, and the full process.

**Sample prompts:**

```
Use "revision-notes-generator" skill to create revision notes of the study materials.
```

```
Use "revision-notes-generator" skill to create revision notes of the study materials with title "<title>".
```

---

### Handoff

Create structured handoff documents for seamless continuity across Claude conversations. When a session ends, the handoff captures the full working state — objective, decisions with rationale, failed approaches, and next steps — so a fresh conversation can continue without re-explanation.

The skill adapts its structure and depth to the type of work (research, writing, planning, building, learning, problem-solving) and the complexity of the session.

> **Full documentation:** See [`handoff/README.md`](handoff/README.md) for work types, depth tiers, document structure, and usage instructions.

---

## Claude Code Skills

Slash commands designed for the Claude Code CLI. These are installed at user-level (`~/.claude/skills/`) and invoked with `/command` syntax.

---

### Handoff (Claude Code)

A `/handoff` slash command for Claude Code that generates structured handoff documents optimised for coding sessions. Captures implementation decisions, failed approaches, error messages, and file-level state that the codebase alone does not preserve. Each handoff references the previous one, creating a traceable handover chain across sessions.

> **Full documentation:** See [`claude-code-skills/handoff/README.md`](claude-code-skills/handoff/README.md) for work types, depth tiers, the handover chain, and installation instructions.

---

### Resume

A `/resume` slash command that loads a handoff document and gets you productive immediately. Companion to `/handoff` — it finds the most recent handoff (or a specific one you name), reads it, reviews the key files listed in it, and continues from the next step.

> **Full documentation:** See [`claude-code-skills/resume/README.md`](claude-code-skills/resume/README.md) for usage and the handoff/resume workflow.

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

## Design Philosophy

- **Extract everything** — No hardcoded cleanup rules during extraction
- **Preserve raw content** — Keep data intact for intelligent post-processing
- **Rich metadata** — Provide comprehensive context for document understanding
- **Manual over automated** — Complex decisions handled manually for better results
- **Atomic flashcards** — One fact per card for effective learning
- **Accuracy first** — Verify and correct information in study materials
- **Structured continuity** — Capture working state, not conversation summaries, so sessions can resume without re-explanation

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
