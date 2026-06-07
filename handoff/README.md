# Handoff

Create structured handoff documents for seamless continuity across Claude conversations.

## The Problem

Claude conversations don't carry forward. When a session ends and a new one begins, everything built up during the conversation is lost: the decisions made and why, the approaches tried and rejected, the constraints established, and the precise state of the work. Starting fresh means re-explaining everything, often losing important nuance in the process.

This is most painful with long, complex tasks: multi-session research, iterative writing, ongoing project planning, or any work where the conversation itself has been the workspace. The longer the session, the more context is at stake.

## The Solution

The handoff skill generates a structured markdown document that captures everything a fresh conversation needs to continue where the current one left off. Rather than summarising the conversation, it captures the **working state**: what the objective is, where the work stands, what was decided and why, what was tried and failed, and exactly what to do next.

The handoff is designed to be downloaded and uploaded directly into a new conversation, giving the receiving session full situational awareness without any re-explanation from the user.

## Key Features

- **Adaptive structure** — The document structure changes based on the type of work (research, writing, planning, building, learning, problem-solving), so each handoff captures what actually matters for that kind of task.
- **Adaptive depth** — Simple tasks produce lean handoffs. Complex multi-faceted sessions produce comprehensive ones, scaled across four depth tiers.
- **Integrated project context** — Stable background information (constraints, preferences, domain knowledge) is folded into the document when relevant, avoiding the need for a separate reference file.
- **Built-in verification** — Each handoff includes a resumption instruction that prompts the receiving session to confirm its understanding before proceeding, catching misinterpretations early.
- **Dead-end capture** — Failed approaches and rejected directions are explicitly documented, preventing the new session from re-exploring them.

## When to Use

- **Before ending a long session** — Capture state before closing a conversation with unfinished work.
- **Approaching context limits** — When a conversation is getting long and quality may degrade, hand off to a fresh session.
- **Switching focus** — Save state before moving to a different task, so you can return later.
- **Multi-session projects** — Any work that spans more than one conversation benefits from structured continuity.

## How It Works

1. **Trigger** — Ask Claude to create a handoff (e.g. "create a handoff", "/handoff"). Include any specific instructions about what to capture.
2. **Classification** — Claude analyses the session to determine the work type and complexity tier, then selects the appropriate document structure.
3. **Clarification (conditional)** — If the session contains genuine ambiguities (e.g. multiple topics with unclear scope, unsettled decisions, competing priorities for next steps), Claude asks at most 2-3 short, targeted questions before generating. If the session state is clear, this step is skipped entirely.
4. **Generation** — Claude produces the handoff document, capturing objective, current state, progress, decisions with rationale, failed approaches, open questions, next steps, and any relevant project context.
5. **Output** — The handoff is saved as a downloadable markdown file (`handoff-[description].md`).

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

The skill prioritises completeness over compression. A handoff that is slightly too long is far less costly than one that forces the user to re-explain context.

## Document Structure

Every handoff follows this skeleton, with sections included or excluded based on relevance:

```
# Handoff: [Descriptive Title]

> Resumption instruction (verification prompt for the receiving session)

Date / Work type / Status

## Objective
## Current State
## Progress
## Decisions Made
## Approaches That Did Not Work
## Project Context
## Open Questions
## Next Steps
## Key References
```

## Resuming from a Handoff

1. Start a fresh Claude conversation
2. Upload or paste the handoff markdown file
3. The receiving session reads the document, confirms its understanding in 2–3 sentences, then continues with the first next step

The handoff is designed so that no additional explanation is needed from the user. The receiving session should be able to proceed immediately after the brief verification exchange.

## Installation

Place the `SKILL.md` file in your Claude skills directory:

```
skills/
└── handoff/
    └── SKILL.md
```

Then trigger with "create a handoff", "/handoff", or similar phrasing in any conversation.
