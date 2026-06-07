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
objective, decisions with rationale, failed approaches, exact error messages,
and clear next steps.

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
- **Handover chain** — Each handoff references the most recent previous one,
  creating a traceable session history with key carryover notes.
- **Reference, don't reproduce** — Files are referenced by path. The new
  session reads them directly. Code is included only when it captures
  something non-obvious.
- **Dead-end capture** — Failed approaches are explicitly documented,
  preventing the new session from retrying them.
- **Built-in verification** — Each handoff includes a resumption instruction
  prompting the new session to confirm understanding before proceeding.
- **Dynamic context** — Automatically detects existing handoffs in the project
  using shell injection, so the chain is maintained without manual tracking.
- **Manual-only invocation** — The skill never triggers automatically. You
  control when to create a handoff.

## How It Works

1. **Invoke** `/handoff` (with optional focus scope).
2. Claude creates `.claude/handoffs/` if it doesn't exist.
3. Claude checks for previous handoffs and reads the most recent one for
   chain continuity.
4. Claude classifies the session's work type and complexity.
5. Claude generates the handoff and saves it to
   `.claude/handoffs/[YYYY-MM-DD]-[description].md`.

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

## Document Structure

```
# Handoff: [Descriptive Title]

> Resumption instruction

Date / Project / Work type / Status

## Previous Session (if chain exists)
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

## The Handover Chain

Each handoff references the most recent previous one:

```markdown
## Previous Session
- Handoff: `.claude/handoffs/2026-06-05-auth-endpoints.md`
- Key carryover: JWT validation works, refresh token endpoint still needed
```

This creates a queryable history. When something breaks sessions later, you
can trace back through the chain to understand how the project evolved.

## File Structure

```
.claude/
├── handoffs/
│   ├── 2026-06-05-auth-endpoints.md
│   ├── 2026-06-06-rate-limiting.md
│   └── 2026-06-07-error-handling.md
└── skills/
    └── ...
```

Handoff files are saved per-project in `.claude/handoffs/`. The skill itself
lives at user-level in `~/.claude/skills/handoff/`.

## Resuming from a Handoff

In the new Claude Code session, tell Claude to read the handoff:

```
Read .claude/handoffs/2026-06-07-error-handling.md and continue from where
the last session left off.
```

The receiving session reads the document, reviews the listed files, confirms
understanding, and continues with the first next step.
