# Revision Notes Generator

> **Source:** Converted from [revision-notes/prompt-v2.txt](https://github.com/maaarcooo/llm-custom-instructions/blob/main/revision-notes/prompt-v2.txt)

Generate accurate, self-contained revision notes from PDF or Markdown study materials.

## The Problem

Study materials are often dense, poorly organised, or contain errors. Condensing them manually is slow and risks missing key content or carrying forward inaccuracies. LLM-generated notes have their own failure modes: coverage drifts between runs, knowledge gets silently added from outside the source, and "verify accuracy" instructions produce no observable behaviour. Students need notes that are complete, honest about their sources, and usable without referring back to the original material.

## The Solution

Automated generation of revision notes with verified coverage and full source transparency. The skill builds a coverage map of the source before writing, runs a mandatory verification pass before output, and marks every claim that goes beyond the source. Source errors are flagged rather than silently corrected, so nothing changes invisibly between the original material and the notes.

## Key Features

- **Coverage map** — Every subheading, method, equation, and condition in the source is listed before writing and checked against before output, eliminating run-to-run coverage drift
- **Flagged additions** — Knowledge added beyond the source is marked inline with `*(Beyond source: ...)*`, never inserted silently
- **Error flagging** — Statements that conflict with standard treatment are kept and flagged with `⚠ Check`, never silently corrected
- **Worked example policy** — Examples that teach reusable methods are compressed and retained, while pure number-substitution examples are dropped
- **Signal density** — Every sentence must define, explain, or connect a concept, with no length cap, so conciseness means zero noise rather than brevity
- **Self-contained** — Diagram content is translated into prose or tables, with no "see source" references
- **Mandatory verification** — An explicit checklist pass before output, covering coverage, accuracy, internal consistency, and formatting

## When to Use

When asked to create revision notes, study notes, topic summaries, or condensed notes from educational PDFs, Markdown files, textbooks, or course materials.

## How It Works

1. **Read** the attached source in full, including figures, diagrams, tables, and worked examples
2. **Map** the source structure into a coverage checklist
3. **Write** the notes following the content rules
4. **Verify** against the mandatory checklist and fix any failures
5. **Output** as a markdown file with the exact specified title

## Content Rules

- **Coverage (the floor)**: Every item in the source map appears in the notes, however compressed
- **Signal density (the style)**: No filler, no restated headings, no redundancy
- **Self-contained**: Complete understanding from the notes alone
- **Fidelity with flagged additions**: Faithful to the source, with marked additions only where needed
- **Error flagging**: Keep and flag, never silently correct
- **Worked examples**: Keep methods, drop number substitution
- **Tier labelling**: (HT) marking applies to GCSE sources only

## Output Format

Markdown with the title as H1, source section numbering retained for cross-referencing, key terms in bold on first definition, equations in LaTeX, and tables for comparative content. Ends with a Key Equations Summary, plus a Key Constants table where the source provides constants.

```markdown
# Topic Title

### 4.1.3 Section Heading

**Key term** is the definition or explanation.

$$F = ma$$

*(Beyond source: an added fact, marked inline.)*

> ⚠ Check: source states X; standard treatment is Y.
```

## Sample Prompts

```
Use the "revision-notes-generator" skill to create revision notes from the attached study materials.
Title the notes after the topic in the source, and output a .md file named after the source file
(e.g. Physics_Chapter_5.pdf → Physics_Chapter_5.md).
```

To override the title for a specific run, append:

```
Title: "Your Exact Title"
```

## Installation

Place the `SKILL.md` file in your Claude skills directory:

```
skills/
└── revision-notes-generator/
    └── SKILL.md
```

Then trigger by asking Claude to create revision notes, study notes, or topic summaries.

## Known Limitations

- Source-internal contradictions (the source disagreeing with itself across sections) can occasionally pass verification
- The worked-example filter occasionally retains a trivial number-substitution example
