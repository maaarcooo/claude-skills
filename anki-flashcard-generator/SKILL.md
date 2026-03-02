---
name: anki-flashcard-generator
description: Generate Anki flashcard decks from PDF or Markdown study materials. Use only when "Anki flashcard" or "Anki deck" is explicitly mentioned. Do not trigger for generic flashcard requests. Outputs in Anki-importable text format (Question | Answer).
---

# Anki Flashcard Generator

Generate study flashcards from PDF or Markdown content in Anki-importable format.

## Process

1. Read the source file (PDF or Markdown) thoroughly
2. Verify accuracy of all information in the source — correct any errors
3. Identify all key content: **bolded terms**, highlighted text, and Higher Tier material
4. Generate flashcards covering all essential topic content
5. Output as text file: one card per line, format `Question | Answer`

## Card Types

### Definition cards
For key terms and concepts. Create both forward and reverse directions so the learner can recall the term from the definition and vice versa:
```
What is [term]? | [definition]
[definition] — what term describes this? | [term]
```

### Explain/justify cards
For concepts where understanding the reasoning matters, not just the fact. These target common "explain" and "justify" style exam questions (typically 2-4 marks).

Answers must include the full cause-and-effect chain, not just restate the fact. The goal is to train the learner to reproduce the reasoning under exam conditions.
```
Explain why [phenomenon occurs] | [reasoning with cause-and-effect chain]
Why does [X] lead to [Y]? | [mechanism/reasoning]
```

### Compare/contrast cards
For related concepts that are commonly confused or examined together. Both sides of the comparison must be addressed in the answer so the learner understands the actual distinction.
```
How does [concept A] differ from [concept B]? | [key differences]
What is the similarity between [A] and [B]? | [shared properties]
```

## Card Design Rules

**Atomic**: One fact or one explanation per card. Split complex concepts into multiple cards. This matters because Anki's spaced repetition algorithm schedules each card independently — multi-fact cards create ambiguous reviews where you half-know the answer, making scheduling unreliable and gaps harder to identify.

**Concise**: Use simple, direct language. Avoid unnecessary words. Short answers are easier to judge during review and reduce the temptation to passively read rather than actively recall.

**Explain cards need full reasoning**: "Because of temperature" is not an acceptable answer. State the mechanism: what happens, why it happens, and what effect it produces. If the chain has multiple steps, include all of them.

**Compare cards must be specific**: State the actual difference with both sides addressed. "They are different" is not useful — the answer should make clear what each concept does and how they diverge.

**Exclude**:
- Questions that depend on interpreting a diagram or visual to answer (however, factual content shown in diagrams should still be converted into text-based cards where possible)
- Multi-step numerical calculations. Simple formula recall (e.g., "What is the equation for kinetic energy?") and single-step unit or value recall are fine.

## Coverage Guidance

Aim for thorough coverage of the source material. As a rough guide, a typical A-level topic page should yield 10-25 cards depending on density. Prioritise content that is examinable: definitions, laws, key relationships, common explain/justify points, and frequently confused pairs. Do not pad with trivial or redundant cards.

## Output Format

**File naming**: Name the output file after the source file (e.g., `Physics_Chapter_5.pdf` → `Physics_Chapter_5.txt`)

```
Question | Answer
```

**Example output:**
```
What is the unit of electrical resistance? | Ohm (Ω)
A material that allows electric current to flow through it is called what? | A conductor
Define specific heat capacity | The energy required to raise the temperature of 1 kg of a substance by 1°C
The energy required to raise 1 kg of a substance by 1°C — what quantity is this? | Specific heat capacity
Explain why resistance increases with temperature in a metal | At higher temperatures, metal ions vibrate with greater amplitude, so conduction electrons collide more frequently with ions, transferring less charge per unit time
How does electrical conduction differ between metals and semiconductors? | In metals, resistance increases with temperature (more ion vibrations impede electron flow). In semiconductors, resistance decreases with temperature (more electrons gain enough energy to move into the conduction band, increasing the number of charge carriers)
What is the equation for kinetic energy? | Ek = ½mv²
```

## Quality Checklist

- [ ] All bolded/highlighted terms covered
- [ ] Higher Tier content included
- [ ] No multi-fact cards
- [ ] Reverse cards for definitions
- [ ] Explain cards include full cause-and-effect reasoning
- [ ] Compare cards address both sides of the comparison
- [ ] No diagram-dependent or multi-step calculation questions
- [ ] Simple formula recall cards included where relevant
- [ ] Clear, unambiguous phrasing
