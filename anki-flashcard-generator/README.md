# Anki Flashcard Generator

> **Source:** Evolved from [anki-flashcard/prompt-v4.txt](https://github.com/maaarcooo/llm-custom-instructions/blob/main/anki-flashcard/prompt-v4.txt). Current skill version: **v3.6**. A standalone fallback prompt with full instruction parity is maintained as `anki-flashcard-prompt-v5.md` for when the skill feature is unavailable.

Generate study flashcards from PDF or Markdown content in Anki-importable format. Cards are terse, exam-aligned, and quick to self-grade during review.

## The Problem

Creating effective flashcards manually is time-consuming and inconsistent. Poor card design — ambiguous phrasing, recognition-based questions, answers that leak other cards' content — undermines spaced repetition rather than supporting it. Factual errors in source notes get cemented through months of reviews. And model defaults drift across versions: the same prompt that produced clean, terse decks on one model produces padded, over-elaborated decks on the next.

## The Solution

A deliberately small rule set, split into two types:

- **Defect-blocking rules** (strict): no yes/no questions, no pipe characters in content, no diagram-dependent cards, no circular answers, accuracy verification with error flagging. These prevent objective failures and never shape style.
- **Style conveyed by example** (flexible): the terse register, bundling judgment, and card-type selection are taught through concrete example cards rather than prescriptive principles, leaving the model room to adapt per situation.

This split is the result of testing across model versions: prescriptive style rules (rigid atomicity targets, mandatory "why/how" framing, universal bidirectional cards) were found to globally distort deck character, while defect-blocking rules cost nothing. Output is in Anki's native import format (`Question | Answer`, one card per line).

## Key Features

- **Flexible atomicity** — One idea per card, but a definition may bundle one directly associated detail (formula, unit, key property) when naturally recalled together
- **Bundle or split, not both** — A bundled detail never also gets its own card; no answer contains another card's answer
- **Accuracy verification** — Clear factual errors are fixed; possible syllabus-level simplifications are kept and flagged in chat, never silently rewritten
- **Constrained interference check** — Exactly two passes: resolve contradicting cards, and add one compare card per pair the source itself contrasts
- **Six card types** — Definition (with scoped reverse cards), recall, formula application, cloze, explain, enumeration
- **Content-driven deck size** — No card-count targets; the material decides

## When to Use

Only when "Anki flashcard" or "Anki deck" is explicitly mentioned. The skill does not trigger for generic flashcard requests.

## How It Works

1. **Read** the source file (PDF or Markdown) thoroughly
2. **Verify** accuracy: fix clear factual errors; keep and flag possible intentional simplifications (flags go in the chat response, never the output file)
3. **Identify** key content: definitions, laws, equations, units, standard values, conditions, named processes, and common explain/justify points
4. **Generate** cards covering all essential topic content
5. **Check** the finished set for contradictions and source-contrasted pairs only
6. **Format** output as one card per line: `Question | Answer`

## Card Style

The terse register is the priority — when any rule conflicts with brevity, brevity wins.

- **One idea per card, judged flexibly**: answers are one to two short sentences; a definition may bundle one directly associated detail, never a reasoning chain or a second independent concept
- **Bundle or split, not both**: each detail lives in exactly one place in the deck
- **No rationale padding**: no "because..." justifications appended to recall answers — if reasoning matters, it gets its own card
- **Production over recognition**: no yes/no or true/false questions; rephrase so the answer must be generated
- **Unambiguous**: each question has exactly one correct answer
- **Plain language**: simple, direct wording matched to the source's syllabus level

## Card Types

- **Definition**: forward card always; reverse card as a separate line for key terms only (terms the exam asks candidates to define)
- **Recall**: single facts, values, units, equations
- **Formula application**: alongside a formula card, optionally one single-step application — never multi-step
- **Cloze**: one deletion per card, used sparingly, only where context cues recall without giving the answer away
- **Explain**: only where the source itself explains the reasoning and it is a likely exam point; mechanism stated in at most two sentences
- **Enumeration**: one card per list item; a list answer may contain at most 3 items, and only if the source treats them as a single fact

Compare/contrast cards are not a free card type — they are generated only by the interference check below.

## Interference Check

After generating, the deck is scanned for exactly two failure modes:

1. **Contradictions** — cards whose answers conflict as phrased (e.g. "Which radiation is most ionising?" answered differently under unstated contexts); each question is rephrased to name its context
2. **Source-contrasted pairs** — where the source explicitly contrasts two concepts, one compare card states the specific point of divergence

No other compare cards are generated, and never two compare cards for the same distinction.

## Exclusions

- Questions requiring a diagram or visual to answer (factual content from diagrams is converted to text cards)
- Multi-step calculations
- Yes/no or true/false questions
- Answers that merely restate the question (omitted and flagged instead)
- Cards for content the source does not adequately explain
- The `|` character inside any question or answer

## Output Format

One card per line, question and answer separated by a single pipe. No preamble, headers, blank lines, or markdown in the output file.

```
What is the unit of electrical resistance? | Ohm (Ω)
Define specific heat capacity | The energy required to raise the temperature of 1 kg of a substance by 1 °C
The energy required to raise the temperature of 1 kg of a substance by 1 °C — what quantity is this? | Specific heat capacity
What is the equation for kinetic energy? | Ek = ½mv²
The SI unit of energy is the [...] | joule (J)
What is an alpha particle? | Two protons and two neutrons (a helium-4 nucleus). Stopped by a few centimetres of air
What is impulse? | The change in momentum of an object when a force acts on it, equal to force × time (Ft = Δp)
What is the worst-case time complexity of binary search? | O(log n)
Explain why resistance increases with temperature in a metal | Ions vibrate with greater amplitude, so electrons collide with them more frequently
How does the elastic limit differ from the limit of proportionality? | Limit of proportionality: extension stops being proportional to force. Elastic limit: material stops returning to its original shape. Proportionality limit is reached first
```

## Sample Prompts

**claude.ai:**

```
Create an Anki flashcard deck from the attached study materials using the "anki-flashcard-generator" skill.
Output the deck as a .txt file named after the source file (e.g. Physics_Chapter_5.pdf → Physics_Chapter_5.txt).
```

**Claude API:**

```
Create an Anki flashcard deck from the attached study materials using the "anki-flashcard-generator" skill.
Output only the flashcard lines in the format "Question | Answer", one per line.
Do not include any preamble, headers, explanations, markdown formatting,
or code fences. The raw output will be saved directly to a text file.
```

## Installation

Place the `SKILL.md` file in your Claude skills directory:

```
skills/
└── anki-flashcard-generator/
    └── SKILL.md
```

Then trigger by mentioning "Anki flashcard" or "Anki deck" in your conversation.

## Version Notes

- **v3.6** — Rebuilt around the defect-blocking vs style-prescribing rule split. Softened atomicity to permit definition + associated-detail bundling, added bundle-or-split, banned circular answers, constrained the interference check to two cases, removed card-count anchors, scoped reverse cards to key terms, removed GCSE-era "Higher Tier" references, added the pipe-character exclusion. Validated on A-Level Physics sources inside and outside projects with convergent output
- **v3.3–v3.5** — Principle-heavy versions (depth of processing, universal bidirectional cards, personal connection); produced over-elaborated decks and were superseded
