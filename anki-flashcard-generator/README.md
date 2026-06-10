# Anki Flashcard Generator

> **Source:** Converted from [anki-flashcard/prompt-v4.txt](https://github.com/maaarcooo/llm-custom-instructions/blob/main/anki-flashcard/prompt-v4.txt)

Generate study flashcards from PDF or Markdown content in Anki-importable format.

## The Problem

Creating effective flashcards manually is time-consuming and inconsistent. Poor card design — multi-fact cards, ambiguous phrasing, recognition-based questions — undermines spaced repetition rather than supporting it. Students also miss confusable pairs between cards, leading to interference that degrades recall as the deck matures.

## The Solution

Evidence-based card design following six core principles optimised for active recall and long-term retention under spaced repetition scheduling. Six specialised card types are matched to different knowledge types, and a built-in interference check scans for confusable pairs. Output is in Anki's native import format (`Question | Answer`, one card per line).

## Key Features

- **Six core design principles** — Understand-first, atomicity, production over recognition, depth of processing, dual coding, personal connection
- **Six card types** — Definition, explain/justify, cloze-style, compare/contrast, formula/equation, enumeration
- **Interference management** — Dedicated compare/contrast cards for confusable pairs
- **Coverage guidance** — Prioritised by examinability: definitions, laws, key equations, and explain/justify points first
- **Quality checklist** — Validates completeness, atomicity, phrasing, and exclusions

## When to Use

Only when "Anki flashcard" or "Anki deck" is explicitly mentioned. The skill does not trigger for generic flashcard requests.

## How It Works

1. **Read** the source file (PDF or Markdown) thoroughly
2. **Verify** accuracy of all information in the source — correct any errors
3. **Identify** all key content: bolded terms, highlighted text, and Higher Tier material
4. **Generate** flashcards covering all essential topic content, selecting the most effective card type for each piece of knowledge
5. **Check** for interference: scan the full card set for confusable pairs and add discriminative cards where needed
6. **Format** output as one card per line: `Question | Answer`

## Core Design Principles

Ordered by impact on retention:

- **Understand-first rule**: Never create cards for content the learner has not yet studied — cards consolidate existing understanding, they don't teach new concepts
- **Minimum information (atomicity)**: Each card tests exactly one atomic piece of knowledge, answerable in under 6 seconds
- **Production over recognition**: Cards require producing an answer from memory, not merely recognising it — no yes/no or true/false questions
- **Depth of processing**: Frame questions using "why," "how," or "explain" to force elaborative processing rather than rote retrieval
- **Dual coding**: Extract factual content from diagrams/visuals into text-based cards; the learner may attach images manually in Anki after import
- **Personal connection**: Where content allows, frame cards using concrete, relatable scenarios rather than abstract statements

## Card Types

- **Definition** (forward + reverse): Both directions for key terms to build bidirectional retrieval links
- **Explain/justify**: Full cause-and-effect chains for reasoning-based exam questions
- **Cloze-style**: Facts embedded in context with exactly one keyword deleted per card
- **Compare/contrast**: For commonly confused concepts — highlights the specific point of divergence
- **Formula/equation**: Formula recall plus at least one application card for when/why to use it
- **Enumeration**: Individual cards per list item rather than testing entire lists at once

## Card Design Rules

- **Concise**: Simple, direct language; aim for answers under 25 words for factual cards
- **Unambiguous**: Each question must have exactly one correct answer
- **Bidirectional**: Both forward and reverse cards for key definitions
- **Interference management**: Dedicated compare/contrast cards for confusable pairs
- **Exclusions**: No diagram-dependent questions, multi-step calculations, yes/no questions, or cards listing more than 3 items

## Output Format

One card per line, question and answer separated by a pipe:

```
What is the unit of electrical resistance? | Ohm (Ω)
Define specific heat capacity | The energy required to raise the temperature of 1 kg of a substance by 1°C
The energy required to raise 1 kg of a substance by 1°C — what quantity is this? | Specific heat capacity
The SI unit of energy is the [...] | joule (J)
Explain why resistance increases with temperature in a metal | At higher temperatures, metal ions vibrate with greater amplitude, so conduction electrons collide more frequently with ions, transferring less charge per unit time
How does electrical conduction differ between metals and semiconductors? | In metals, resistance increases with temperature (more ion vibrations impede electron flow). In semiconductors, resistance decreases with temperature (more electrons gain enough energy to enter the conduction band, increasing the number of charge carriers)
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
