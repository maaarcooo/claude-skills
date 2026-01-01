---
name: anki-flashcard-generator
description: Generate Anki flashcard decks from PDF or Markdown study materials. Use only when "Anki flashcard" or "Anki deck" is explicitly mentioned. Do not trigger for generic flashcard requests. Outputs in Anki-importable text format (Question | Answer).
---

# Anki Flashcard Generator

Generate study flashcards from PDF or Markdown content in Anki-importable format.

## Process

1. Read the source file (PDF or Markdown) thoroughly
2. Identify all key content: **bolded terms**, highlighted text, and Higher Tier material
3. Generate flashcards covering all essential topic content
4. Output as text file: one card per line, format `Question | Answer`

## Card Design Rules

**Atomic**: One fact per card. Split complex concepts into multiple cards.

**Concise**: Use simple, direct language. Avoid unnecessary words.

**Reverse cards**: For key definitions, create both directions:
```
What is [term]? | [definition]
[definition] — what term describes this? | [term]
```

**Exclude**: Questions requiring diagrams or visual answers.

## Output Format

**File naming**: Name the output file after the source file (e.g., `Physics_Chapter_5.pdf` → `Physics_Chapter_5.txt`)
```
Question | Answer
```

Example output:
```
What is the unit of electrical resistance? | Ohm (Ω)
A material that allows electric current to flow through it is called what? | A conductor
What happens to resistance when temperature increases in a metal? | Resistance increases
Define specific heat capacity | The energy required to raise the temperature of 1 kg of a substance by 1°C
The energy required to raise 1 kg of a substance by 1°C — what quantity is this? | Specific heat capacity
```

## Quality Checklist

- [ ] All bolded/highlighted terms covered
- [ ] Higher Tier content included
- [ ] No multi-fact cards
- [ ] Reverse cards for definitions
- [ ] No diagram-dependent questions
- [ ] Clear, unambiguous phrasing
