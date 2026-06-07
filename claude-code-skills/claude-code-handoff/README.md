# Handoff (Claude Code)

Create structured handoff documents for seamless continuity across Claude Code sessions.

## The Problem

Claude Code sessions don't persist. When a session ends, everything accumulated during the conversation is lost: the reasoning behind implementation choices, the approaches tried and rejected, the debugging hypotheses explored, and the precise state of in-progress work.

The codebase preserves **what** changed, but not **why**. Starting a new session means re-explaining intent, re-establishing constraints, and risking the new session repeating failed approaches that the previous session already ruled out.

## The Solution

The handoff skill generates a structured markdown document that captures everything a fresh Claude Code session needs that the codebase alone cannot provide: the objective and motivation, decisions with their rationale, failed approaches, exact error messages, and clear next steps.

The document is saved to `.claude/handoffs/` within the project. The new session reads it, confirms understanding, and continues.

## Key Features

- **Adaptive structure** — The document structure changes based on the type of coding work (feature implementation, debugging, refactoring, configuration, architecture, testing), so each handoff captures what matters for that kind of task.
- **Adaptive depth** — Simple fixes produce lean handoffs (200-400 words). Complex multi-file work produces thorough ones (800-1500+ words). Sized to complement the codebase, not duplicate it.
- **Reference, don't reproduce** — Files are referenced by path, not copied into the handoff. The new session can read them directly. Code snippets are included only when they capture something non-obvious from the file.
- **Dead-end capture** — Failed approaches and rejected hypotheses are explicitly documented, preventing the new session from re-exploring them.
- **Built-in verification** — Each handoff includes a resumption instruction prompting the new session to confirm understanding before proceeding.

## When to Use

- **Before ending a coding session** — Capture state before wrapping up unfinished work.
- **Approaching context limits** — When the conversation is getting long and you need to start fresh.
- **Switching between tasks** — Save state before moving to a different feature or project.
- **After a long debugging session** — Especially valuable when multiple hypotheses have been tested. Without a handoff, the new session will retry them.

## How It Works

1. **Trigger** — Ask Claude to create a handoff (e.g. "create a handoff", "/handoff"). Include any specific instructions about what to capture.
2. **Classification** — Claude analyses the session to determine the work type and complexity tier, then selects the appropriate document structure.
3. **Generation** — Claude produces the handoff, capturing objective, current state, decisions with rationale, failed approaches, files modified, errors encountered, and next steps.
4. **Output** — The handoff is saved to `.claude/handoffs/[YYYY-MM-DD]-[description].md`.

No confirmation step. Claude generates the best handoff it can from the session. Request edits if needed.

## Work Types

The skill classifies sessions and selects structurally appropriate sections:

| Work Type | Focus Areas |
|---|---|
| Feature Implementation | Implementation state, design decisions, files modified, remaining work |
| Bug Fixing / Debugging | Problem description, reproduction steps, hypotheses tested, root cause |
| Refactoring | Strategy, patterns being applied, files remaining, regressions to watch |
| Configuration / Setup | Config changes, what works now, what doesn't, environment details |
| Architecture / Design | Options considered, decisions made, constraints, open design questions |
| Testing | Test strategy, tests written, coverage gaps, failures under investigation |
| Mixed / General | Universal structure with type-specific sections pulled in as needed |

## Depth Tiers

| Tier | Approximate Size | When It Applies |
|---|---|---|
| Light | 200–400 words | Simple fix, config change, single-file task |
| Standard | 400–800 words | New endpoint, moderate debugging, build tool setup |
| Deep | 800–1500 words | Multi-component feature, complex bug, module refactor |
| Extended | 1500+ words | Large architectural decisions, multiple interconnected workstreams |

Leaner than a general-purpose handoff because the codebase itself provides significant context. The handoff captures what the code cannot: intent, rationale, and failed approaches.

## Document Structure

Every handoff follows this skeleton, with sections included or excluded based on relevance:

```
# Handoff: [Descriptive Title]

> Resumption instruction (verification prompt for the receiving session)

Date / Project / Work type / Status

## Objective
## Current State
## What Was Done
## Decisions Made
## Approaches That Did Not Work
## Files Modified
## Issues / Errors Encountered
## Open Questions
## Next Steps
## Files to Review on Resume
```

## Resuming from a Handoff

In the new Claude Code session:

1. Tell Claude to read the handoff file (e.g. "Read `.claude/handoffs/2026-06-07-auth-middleware.md` and continue")
2. The receiving session reads the document, reviews the listed files, and confirms understanding
3. Work continues from the first next step

## What Gets Captured vs What Doesn't

**Captured:** Objective and motivation, decisions with rationale, failed approaches and why they failed, exact error messages, file paths, reproduction steps, key patterns established, interface contracts, environment details, ordered next steps.

**Not captured:** File contents (readable from disk), general framework knowledge, conversational narrative, verbose terminal output, intermediate reasoning that reached conclusions.

## Installation

Place the `SKILL.md` file in your Claude Code skills directory:

```
.claude/skills/
└── handoff/
    └── SKILL.md
```

Handoff documents are saved to:

```
.claude/handoffs/
├── 2026-06-07-auth-middleware.md
├── 2026-06-08-api-rate-limiting.md
└── ...
```

Then trigger with "create a handoff", "/handoff", or similar phrasing in any session.
