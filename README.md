# Agent Skills

A collection of skills for Claude.ai, Claude Code, ChatGPT, and Codex, covering document processing, study material generation, PDF extraction, discussion workflows, and session continuity.

## Overview

Skills are grouped by target platform. Each platform directory contains independently installable skill packages and may adapt shared workflows to the conventions of that platform.

## Skills Overview

### Claude.ai Skills

| Skill | Purpose | Current Version | Status |
|-------|---------|-----------------|--------|
| [extracting-pdfs](#extracting-pdfs) | Extract and clean PDF content to markdown | - | Active |
| [flashcard-generator](#flashcard-generator) | Generate flashcard decks from study materials | flashcard-v3.7 | Active |
| [revision-notes-generator](#revision-notes-generator) | Create concise revision notes from study materials | notes-v3.6 | Active |
| [handoff](#handoff) | Create structured handoff documents for session continuity | - | Active |
| [discuss](#discuss) | Discuss and clarify direction before starting work | - | Active |
| [learn](#learn) | Support conceptual learning and understanding | - | Active |

### Claude Code Skills

| Skill | Purpose | Status |
|-------|---------|--------|
| [discuss (Claude Code)](#discuss-claude-code) | `/discuss` command for clarifying direction before work | Active |
| [handoff (Claude Code)](#handoff-claude-code) | `/handoff` slash command for session handoff | Active |
| [resume](#resume) | `/resume` slash command to continue from a handoff | Active |

### ChatGPT Skills

| Skill | Purpose | Status |
|-------|---------|--------|
| [anki-flashcard-generator (ChatGPT)](#chatgpt-skills) | Generate flashcard decks from study materials | Active |
| [handoff (ChatGPT)](#chatgpt-skills) | Create structured session handoffs | Active |
| [learn (ChatGPT)](#chatgpt-skills) | Support conceptual learning and understanding | Active |
| [revision-notes-generator (ChatGPT)](#chatgpt-skills) | Create concise revision notes from study materials | Active |

### Codex Skills

| Skill | Purpose | Status |
|-------|---------|--------|
| [discuss (Codex)](#codex-skills) | Discuss and clarify direction before implementation | Active |
| [handoff (Codex)](#codex-skills) | Capture task state for continuation | Active |
| [resume (Codex)](#codex-skills) | Resume work from a handoff document | Active |

### Archived Skills

| Skill | Purpose | Status |
|-------|---------|--------|
| [pdf-extract](#pdf-extract) | PDF extraction (development version) | Archived |
| [pdf-to-markdown-converter](#pdf-to-markdown-converter) | Legacy PDF conversion | Archived |

## Project Structure

```
agent-skills/
├── README.md
├── claude-ai-skills/                  # Skills for Claude.ai
│   ├── flashcard-generator/
│   ├── discuss/
│   ├── extracting-pdfs/
│   ├── handoff/
│   ├── learn/
│   └── revision-notes-generator/
├── claude-code-skills/                 # Claude Code slash commands
│   ├── discuss/
│   ├── handoff/
│   └── resume/
├── chatgpt-skills/                    # Skills exported from ChatGPT
│   ├── anki-flashcard-generator/
│   ├── handoff/
│   ├── learn/
│   └── revision-notes-generator/
├── codex-skills/                      # Skills for Codex
│   ├── discuss/
│   ├── handoff/
│   └── resume/
└── archive/
    └── claude-ai/                    # Archived Claude.ai skills
        ├── pdf-extract/
        └── pdf-to-markdown-converter/
```

## Claude.ai Skills

### Extracting PDFs

The primary skill for extracting PDF content to clean, organized markdown. Uses a 5-step workflow (Extract, Analyse, Clean, Organise, Output) with dual extraction methods, comprehensive image handling, and reference guides for common challenges.

> **Full documentation:** See [`claude-ai-skills/extracting-pdfs/README.md`](claude-ai-skills/extracting-pdfs/README.md) for the complete workflow, CLI usage, dependencies, and reference guide details.

**Sample prompt:**

```
<pathname>
Use "extracting-pdfs" skill to convert this pdf into a markdown file.
```

---

### Flashcard Generator

Generate study flashcards from PDF or Markdown content. Card design follows evidence-based principles with six specialised card types, built-in interference checking, coverage guidance prioritised by examinability, and LaTeX equation support (KaTeX-compatible).

**Current version:** `flashcard-v3.7`

> **Full documentation:** See [`claude-ai-skills/flashcard-generator/README.md`](claude-ai-skills/flashcard-generator/README.md) for design principles, card types, output format, and card design rules.

**Sample prompt for claude.ai:**

```
Create a flashcard deck from the attached study materials using the "flashcard-generator" skill.
Output the deck as a .txt file named after the source file (e.g. Physics_Chapter_5.pdf → Physics_Chapter_5.txt).
```

**Sample prompt for Claude API:**

```
Create a flashcard deck from the attached study materials using the "flashcard-generator" skill.
Output only the flashcard lines in the format "Question | Answer", one per line.
Do not include any preamble, headers, explanations, markdown formatting,
or code fences. The raw output will be saved directly to a text file.
```

---

### Revision Notes Generator

Generate concise, accurate revision notes from PDF or Markdown study materials. Covers a 5-step process from reading through verification to structured markdown output, with writing guidelines prioritising conciseness, completeness, and accuracy.

**Current version:** `notes-v3.6`

> **Full documentation:** See [`claude-ai-skills/revision-notes-generator/README.md`](claude-ai-skills/revision-notes-generator/README.md) for writing guidelines, output format, and the full process.

**Sample prompts:**

```
Use "revision-notes-generator" skill to create revision notes of the study materials.
```

```
Create revision notes from the attached study materials using the "revision-notes-generator" skill.
Title the notes after the topic in the source, and output a .md file named after the source file (e.g. Physics_Chapter_5.pdf → Physics_Chapter_5.md).
```

---

### Handoff

Create structured handoff documents for seamless continuity across Claude conversations. When a session ends, the handoff captures the full working state — objective, decisions with rationale, failed approaches, and next steps — so a fresh conversation can continue without re-explanation.

The skill adapts its structure and depth to the type of work (research, writing, planning, building, learning, problem-solving) and the complexity of the session.

> **Full documentation:** See [`claude-ai-skills/handoff/README.md`](claude-ai-skills/handoff/README.md) for work types, depth tiers, document structure, and usage instructions.

---

### Discuss

Pause before starting work to clarify requirements, surface assumptions, and agree on direction.

---

### Learn

Support requests for intellectual understanding with explanations adapted to the learner and topic.

---

## Claude Code Skills

Slash commands designed for the Claude Code CLI. These are installed at user-level (`~/.claude/skills/`) and invoked with `/command` syntax.

---

### Discuss (Claude Code)

A `/discuss` command that pauses implementation so requirements and direction can be clarified first.

---

### Handoff (Claude Code)

A `/handoff` slash command for Claude Code that generates structured handoff documents optimised for coding sessions. Captures implementation decisions, failed approaches, error messages, and file-level state that the codebase alone does not preserve. Each handoff references the previous one, creating a traceable handover chain across sessions.

> **Full documentation:** See [`claude-code-skills/handoff/README.md`](claude-code-skills/handoff/README.md) for work types, depth tiers, the handover chain, and installation instructions.

---

### Resume

A `/resume` slash command that loads a handoff document and gets you productive immediately. Companion to `/handoff` — it finds the most recent handoff (or a specific one you name), reads it, reviews the key files listed in it, and continues from the next step.

> **Full documentation:** See [`claude-code-skills/resume/README.md`](claude-code-skills/resume/README.md) for usage and the handoff/resume workflow.

---

## ChatGPT Skills

The `chatgpt-skills/` directory contains the skill packages uploaded to and exported from ChatGPT, including the generated `agents/openai.yaml` metadata and icons.

The collection currently includes Anki Flashcard Generator, Handoff, Learn, and Revision Notes Generator.

---

## Codex Skills

The `codex-skills/` directory contains Codex adaptations of the coding workflow skills. They are installed under `~/.codex/skills/` and can be invoked by name, such as `$handoff` and `$resume`.

The collection currently includes Discuss, Handoff, and Resume.

---

## Archived Skills

The following Claude.ai skills have been moved to `archive/claude-ai/`. They are preserved for reference but are no longer actively maintained.

---

### PDF Extract

> **Location:** `archive/claude-ai/pdf-extract/`

The development/original version of the PDF extraction skill. Contains the core Python extraction script.

> **Note:** For production use, see [extracting-pdfs](#extracting-pdfs) which is the current active version.

**Features:**

- Same extraction capabilities as extracting-pdfs
- Contains `extract_pdf.py` script (1,500+ lines)
- Full reference documentation included

---

### PDF to Markdown Converter

> **Location:** `archive/claude-ai/pdf-to-markdown-converter/`

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

This repository uses per-skill version labels. The current study-generation labels are `flashcard-v3.7` for `flashcard-generator` and `notes-v3.6` for `revision-notes-generator`. See [Releases](../../releases) for version history.

## License

This work is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) - you're free to share and adapt with attribution.
