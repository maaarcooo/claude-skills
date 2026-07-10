# Handoff (Claude Code)

A `/handoff` slash command for Claude Code that generates structured handoff
documents for seamless session continuity.

## The Problem

Claude Code sessions don't persist. When a session ends, everything
accumulated during the conversation is lost: the reasoning behind
implementation choices, the approaches tried and rejected, the debugging
hypotheses explored, and the precise state of in-progress work.

The codebase preserves **what** changed, but not **why**. Starting a new
session means re-explaining intent, re-establishing constraints, and risking
the new session repeating failed approaches.

## The Solution

The `/handoff` command generates a structured markdown document that captures
everything a fresh session needs that the codebase alone cannot provide:
objective, decisions with rationale and origin, failed approaches, open
discussions, exact error messages, and clear next steps.

Each handoff references the previous one, creating a **handover chain** that
gives any session a traceable history of the project's evolution across
sessions.

## Installation

Place the skill at user-level so it's available across all projects:

```bash
mkdir -p ~/.claude/skills/handoff
# Copy SKILL.md to ~/.claude/skills/handoff/SKILL.md
```

The command becomes available as `/handoff` in any Claude Code session.

## Usage

```
/handoff                          Full-session handoff
/handoff auth-middleware          Handoff focused on auth middleware work
/handoff "API rate limiting"      Handoff focused on a specific task
```

When no arguments are provided, a full-session handoff is generated. When
arguments are provided, the handoff focuses on that specific aspect of the
session.

## Key Features

- **Adaptive structure** — Document structure changes based on work type
  (feature, bug fix, refactoring, config, architecture, testing).
- **Adaptive depth** — Simple fixes produce lean handoffs (200-400 words).
  Complex multi-file work produces thorough ones (800-1500+ words).
- **Complete discussion coverage** — Every substantive discussion thread is
  captured as its residue: a decision with rationale, a rejected approach
  with reason, or an open discussion. No thread silently vanishes between
  sessions.
- **Decision provenance** — Decisions that came from you (requirements,
  directions, vetoes, opinions) are marked **(user)** and treated as fixed by
  the receiving session. Unmarked decisions are session choices, revisable
  with good reason.
- **Handover chain** — Each handoff restates the still-live context from the
  previous one, so the newest handoff is always self-sufficient while the
  chain remains traceable.
- **Reference, don't reproduce** — Files are referenced by path. The new
  session reads them directly. Code is included only when it captures
  something non-obvious.
- **Dead-end capture** — Failed approaches are explicitly documented with how
  they failed: technical failure and user rejection are distinguished, so a
  veto is never mistaken for an impossibility.
- **Actor-aware next steps** — Steps only the user can perform (reviewing,
  merging, publishing) are marked **(user)**, so the receiving session
  prompts for them instead of attempting them.
- **Undecided direction supported** — When the user has deliberately not
  chosen what to work on next, the handoff records candidate directions as
  options rather than inventing a priority.
- **Built-in verification** — Each handoff includes a resumption instruction
  prompting the new session to confirm understanding before proceeding.
- **Dynamic context** — Automatically detects existing handoffs in the project
  using shell injection, so the chain is maintained without manual tracking.
- **Manual-only invocation** — The skill never triggers automatically
  (`disable-model-invocation`). You control when to create a handoff, and a
  resuming session can never mistakenly load it.

## How It Works

1. **Invoke** `/handoff` (with optional focus scope).
2. Claude creates `handoffs/` at the repository root if it doesn't exist.
3. Claude checks for previous handoffs and reads the most recent one for
   chain continuity, restating any still-live carryover.
4. Claude classifies the session's work type and complexity.
5. Claude generates the handoff — applying the coverage rule so every
   discussion lands as a decision, rejected approach, or open discussion —
   and saves it to `handoffs/[YYYY-MM-DD]-[description].md`.

## Work Types

| Work Type | Focus Areas |
|---|---|
| Feature | Implementation state, design decisions, files modified, remaining work |
| Bug Fix | Problem description, reproduction steps, hypotheses tested, root cause |
| Refactoring | Strategy, patterns applied, files remaining, regressions to watch |
| Config/Setup | Changes made, what works/doesn't, environment details |
| Architecture | Options considered, decisions made, constraints, open design questions |
| Testing | Strategy, tests written, coverage gaps, failures under investigation |
| Mixed | Universal structure with type-specific sections as needed |

## Depth Tiers

| Tier | Approximate Size | When It Applies |
|---|---|---|
| Light | 200-400 words | Simple fix, config change, single-file task |
| Standard | 400-800 words | New endpoint, moderate debugging, tool setup |
| Deep | 800-1500 words | Multi-component feature, complex bug, module refactor |
| Extended | 1500+ words | Large architectural decisions, multiple workstreams |

Sizing principle: complete on decisions, rationale, and failed approaches;
ruthless on everything else. The coverage rule takes precedence over the word
counts — conclusions are never trimmed for length, narrative always is.

## Document Structure

```
# Handoff: [Descriptive Title]

> Resumption instruction

Date / Project / Work type / Status

## Previous Session (if chain exists — restates live carryover)
## Objective
## Current State
## What Was Done
## Decisions Made          (user-originated decisions marked (user))
## Approaches That Did Not Work  (technical failure vs user veto)
## Open Discussions        (explored but unconcluded threads)
## Files Modified
## Issues / Errors Encountered
## Open Questions
## Next Steps              (user-only actions marked (user))
## Possible Directions     (replaces Next Steps when direction is undecided)
## Files to Review on Resume
```

## The Handover Chain

Each handoff restates the still-live context from the most recent previous
one:

```markdown
## Previous Session
- Handoff: `handoffs/2026-06-05-auth-endpoints.md`
- Live carryover: JWT validation works, refresh token endpoint still needed
```

This creates a queryable history. When something breaks sessions later, you
can trace back through the chain to understand how the project evolved.
Context that is no longer live is dropped at each link, so stale items do not
propagate, and once around ~10 handoffs accumulate the skill suggests
archiving older ones.

## File Structure

```
handoffs/
├── 2026-06-05-auth-endpoints.md
├── 2026-06-06-rate-limiting.md
└── 2026-06-07-error-handling.md
```

Handoff files are saved per-project in `handoffs/`. The skill itself lives at
user-level in `~/.claude/skills/handoff/`.

## Resuming from a Handoff

Use the companion `/resume` command, or tell Claude to read the handoff
directly:

```
Read handoffs/2026-06-07-error-handling.md and continue from where
the last session left off.
```

The receiving session reads the document, reviews the listed files, confirms
understanding, and continues with the first next step. Decisions marked
**(user)** are treated as fixed. Steps marked **(user)** are prompted to you
rather than attempted, and if the handoff records Possible Directions instead
of Next Steps, the session presents them for you to choose from.
