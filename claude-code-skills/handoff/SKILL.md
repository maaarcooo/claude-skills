---
description: >
  Generate a structured handoff document for session continuity.
  Captures decisions, rationale, failed approaches, and next steps
  so a fresh session can continue without re-explanation.
disable-model-invocation: true
argument-hint: "[optional focus scope]"
allowed-tools: Bash(mkdir *) Bash(ls *)
---

# Session Handoff

Generate a handoff document capturing the session state that is not visible
from the codebase alone: intent, decisions, rationale, failed approaches, and
next steps. The codebase shows **what** changed. The handoff explains **why**
and **what's next**.

If arguments are provided ($ARGUMENTS), focus the handoff on that specific
aspect of the session. Otherwise, generate a full-session handoff.

## Previous handoffs

!`ls -1t .claude/handoffs/*.md 2>/dev/null | head -5`

If previous handoffs exist above, reference the most recent one at the top of
the new handoff under a "Previous Session" heading with a key carryover note.

## Process

1. Create `.claude/handoffs/` if it does not exist: `mkdir -p .claude/handoffs`
2. Classify the work type and complexity to determine structure and depth
3. If previous handoffs exist, read the most recent one to identify carryover
4. Generate the handoff document
5. Save to `.claude/handoffs/[YYYY-MM-DD]-[description].md`

## Work type classification

Select the primary type. Pull in sections from secondary types if the session
spans multiple.

- **Feature** — Implementation state, design decisions, files modified, remaining work
- **Bug fix** — Problem description, reproduction steps, hypotheses tested, root cause, fix status
- **Refactoring** — Strategy, patterns applied, files remaining, regressions to watch
- **Config/Setup** — Changes made, what works, what doesn't, environment details
- **Architecture** — Options considered, decisions made, constraints, open design questions
- **Testing** — Strategy, tests written, coverage gaps, failures under investigation
- **Mixed** — Universal structure with type-specific sections as needed

## Depth sizing

Scale to complexity. The codebase provides significant context, so the handoff
captures only what the code cannot.

- **Light (200-400 words)** — Simple fix, config change, single-file task
- **Standard (400-800 words)** — New endpoint, moderate debugging, tool setup
- **Deep (800-1500 words)** — Multi-component feature, complex bug, module refactor
- **Extended (1500+ words)** — Large architectural decisions, multiple workstreams

Prioritise decisions and rationale over brevity.

## Document structure

Include or exclude sections based on relevance. No empty sections. Reference
files by path rather than reproducing content.

```markdown
# Handoff: [Descriptive Title]

> **Resumption instruction:** Read this handoff, review the listed files,
> then confirm your understanding in 2-3 sentences before proceeding.

**Date:** [YYYY-MM-DD]
**Project:** [project path]
**Work type:** [Feature / Bug Fix / Refactoring / Config / Architecture / Testing / Mixed]
**Status:** [In Progress / Paused / Nearing Completion / Blocked]

## Previous Session
<!-- Only if prior handoffs exist -->
- Handoff: `.claude/handoffs/[previous-filename].md`
- Key carryover: [what is still relevant from the previous session]

---

## Objective

[What we are trying to accomplish and why.]

## Current State

[Precise snapshot of where the work stands. What works, what doesn't,
what is partially complete.]

## What Was Done

- [Action] — [outcome]
- [Action] — [outcome]

## Decisions Made

- **[Decision]** — [Rationale. Alternatives considered.]

## Approaches That Did Not Work

- **[Approach]** — [Why it failed or was rejected]

## Files Modified

- `path/to/file` — [What changed and why]

## Issues / Errors Encountered

[Exact error messages, unexpected behaviours, reproduction steps.]

## Open Questions

- [ ] [Specific question]

## Next Steps

1. [First action — specific and concrete]
2. [Second action]
3. [Third action]

## Files to Review on Resume

- `path/to/file` — [Why this file matters for continuing]
```

## Content rules

**Always include:** Objective with motivation. Precise current state. Decisions
with rationale. Failed approaches with reasons. Actionable next steps. Files
modified and files to review.

**Include when relevant:** Exact error messages. Reproduction steps. Key
patterns or conventions established. Interface contracts not yet implemented.
Environment-specific details (ports, config values, service URLs).

**Exclude:** File contents (the new session reads files directly). General
framework knowledge. Conversational narrative. Verbose terminal output.
Intermediate reasoning that reached conclusions.

## Quality check

Before saving, verify:

- A fresh session could continue without asking for re-explanation
- Every decision includes rationale
- Failed approaches are documented
- Next steps are immediately actionable
- File paths are accurate
- No code is reproduced that could be read from disk
