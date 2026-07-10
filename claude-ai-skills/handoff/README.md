# Handoff

Create structured handoff documents for seamless continuity across Claude conversations.

## The Problem

Claude conversations don't carry forward. When a session ends and a new one begins, everything built up during the conversation is lost: the decisions made and why, the approaches tried and rejected, the constraints established, and the precise state of the work. Starting fresh means re-explaining everything, often losing important nuance in the process.

This is most painful with long, complex tasks: multi-session research, iterative writing, ongoing project planning, or any work where the conversation itself has been the workspace. The longer the session, the more context is at stake.

## The Solution

The handoff skill generates a structured markdown document that captures everything a fresh conversation needs to continue where the current one left off. Rather than summarising the conversation, it captures the **working state**: what the objective is, where the work stands, what was decided and why (and by whom), what was tried and failed, what was discussed but not concluded, and exactly what to do next.

The handoff is designed to be downloaded and uploaded directly into a new conversation, giving the receiving session full situational awareness without any re-explanation from the user.

## Key Features

- **Adaptive structure** — The document structure changes based on the type of work (research, writing, planning, building, learning, problem-solving), so each handoff captures what actually matters for that kind of task.
- **Adaptive depth** — Simple tasks produce lean handoffs. Complex multi-faceted sessions produce comprehensive ones, scaled across four depth tiers.
- **Complete discussion coverage** — Every substantive discussion thread is captured as its residue: a decision with rationale, a rejected approach with reason, or an open discussion. No thread silently vanishes between sessions.
- **Decision provenance** — Decisions that came from you (requirements, directions, vetoes, opinions) are marked **(user)** and treated as fixed by the receiving session. Unmarked decisions are session choices, revisable with good reason.
- **Integrated project context** — Stable background information (constraints, preferences, domain knowledge) is folded into the document when relevant, avoiding the need for a separate reference file.
- **Built-in verification** — Each handoff includes a resumption instruction that prompts the receiving session to confirm its understanding before proceeding, catching misinterpretations early.
- **Dead-end capture** — Failed approaches are explicitly documented with how they failed: genuine failure and user rejection are distinguished, so a veto is never mistaken for an impossibility.
- **Actor-aware next steps** — Steps only the user can perform are marked **(user)**, so the receiving session prompts for them instead of attempting them.
- **Undecided direction supported** — When the user has deliberately not chosen what to work on next, the handoff records candidate directions as options rather than inventing a priority. The receiving session presents them as choices.
- **Self-contained resumption** — The document carries its own resumption instructions, including the meaning of the **(user)** markers. The receiving session does not need (and is instructed not to load) this skill.

## When to Use

- **Before ending a long session** — Capture state before closing a conversation with unfinished work.
- **Approaching context limits** — When a conversation is getting long and quality may degrade, hand off to a fresh session.
- **Switching focus** — Save state before moving to a different task, so you can return later.
- **Multi-session projects** — Any work that spans more than one conversation benefits from structured continuity.

The skill triggers on creation requests only. Uploading an existing handoff to resume from it does not (and should not) trigger the skill.

## How It Works

1. **Trigger** — Ask Claude to create a handoff (e.g. "create a handoff", "/handoff"). Include any specific instructions about what to capture, or a chosen direction for the next session if you have one.
2. **Classification** — Claude analyses the session to determine the work type and complexity tier, then selects the appropriate document structure.
3. **Clarification (conditional)** — If the session contains genuine ambiguities (e.g. multiple topics with unclear scope, or a discussion that appears settled but with an ambiguous outcome), Claude asks at most 2-3 short, targeted questions before generating. An undecided next direction is not treated as an ambiguity: Claude records the candidate directions instead of asking you to choose. Genuinely unconcluded discussions are recorded as open discussions, not asked about. If the session state is clear, this step is skipped entirely.
4. **Generation** — Claude produces the handoff document, applying the coverage rule: every substantive discussion lands as a decision (with rationale and origin), a rejected approach (with how it was rejected), or an open discussion (with positions considered and why unresolved) — alongside objective, current state, progress, open questions, next steps (or possible directions), and relevant project context.
5. **Output** — The handoff is saved as a downloadable markdown file (`YYYY-MM-DD-handoff-[description].md`). The date prefix keeps multiple handoffs sortable and prevents filename collisions.

## Work Types

The skill classifies sessions into one of seven categories, each with structurally appropriate sections:

| Work Type | Focus Areas |
|---|---|
| Research / Investigation | Findings, sources, methodology, gaps remaining |
| Writing / Drafting | Draft state, tone/style decisions, structural outline, content status |
| Planning / Strategy | Options considered, decisions made, constraints, plan state |
| Building / Technical | Architecture, what has been built, technical choices, issues encountered |
| Learning / Exploration | Concepts covered, key takeaways, areas of confusion, topics remaining |
| Problem-Solving / Debugging | Problem description, hypotheses tested, what worked/failed, current diagnosis |
| Mixed / General | Universal structure with type-specific sections pulled in as needed |

## Depth Tiers

| Tier | Approximate Size | When It Applies |
|---|---|---|
| Light | 300–600 words | Simple, focused tasks nearing completion |
| Standard | 600–1200 words | Moderate tasks with meaningful progress and several decisions |
| Deep | 1200–2500 words | Complex work with significant accumulated context and many decisions |
| Extended | 2500+ words | Extensive sessions with large decision chains or multiple workstreams |

Sizing principle: complete on decisions, rationale, and failed approaches; ruthless on everything else. The coverage rule takes precedence over the word counts — conclusions are never trimmed for length, narrative always is.

## Document Structure

Every handoff follows this skeleton, with sections included or excluded based on relevance:

```
# Handoff: [Descriptive Title]

> Resumption instruction (verification prompt; notes the document is
> self-contained and defines the (user) marker semantics)

Date / Work type / Status

## Objective
## Current State
## Progress
## Decisions Made          (user-originated decisions marked (user))
## Approaches That Did Not Work  (genuine failure vs user veto)
## Open Discussions        (explored but unconcluded threads)
## Project Context
## Open Questions
## Next Steps              (user-only actions marked (user))
## Possible Directions     (replaces Next Steps when direction is undecided)
## Key References          (every in-session artifact gets a retrievable location)
```

## Resuming from a Handoff

1. Start a fresh Claude conversation
2. Upload or paste the handoff markdown file
3. The receiving session reads the document, confirms its understanding in 2–3 sentences, then continues with the first next step — or, if the handoff records Possible Directions instead, presents them for you to choose from

The handoff is self-contained: no additional explanation is needed from the user, and the handoff skill itself is not required in the receiving conversation. Decisions marked **(user)** are treated as fixed. Steps marked **(user)** will be prompted to you rather than attempted by Claude.

## Installation

Place the `SKILL.md` file in your Claude skills directory:

```
skills/
└── handoff/
    └── SKILL.md
```

Then trigger with "create a handoff", "/handoff", or similar phrasing in any conversation.
