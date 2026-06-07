---
name: handoff
description: >
  Create a structured handoff document for seamless continuity across Claude Code
  sessions. Use when the user explicitly asks to create a handoff, handover, or
  session transfer document. Trigger phrases include: "create a handoff", "handoff
  document", "handover", "save session", "continue later", "session handoff",
  "transfer context", or "/handoff". Do NOT trigger for general conversation
  summaries or when the user simply asks "summarise this session" without
  handoff/continuity intent.
---

# Claude Code Session Handoff Skill

Create a structured markdown document that enables a fresh Claude Code session to
continue the current task seamlessly. The handoff captures session-specific state
that is not visible from the codebase alone: the intent behind changes, decisions
and their rationale, failed approaches, and exactly where to resume.

The codebase shows **what** changed. The handoff explains **why** and **what's next**.

## When to Use

- The user explicitly requests a handoff or handover document
- Before ending a long or complex coding session that has unfinished work
- When approaching context limits and needing to start fresh
- When switching to a different task and wanting to return later

## Core Principle: Reference, Don't Reproduce

The receiving session has full access to the project filesystem. The handoff
should **reference files by path**, not reproduce their content. Include code
snippets only when they capture something not obvious from the file itself (e.g.
a specific pattern being followed, a subtle bug, a key interface contract).

---

## Process

### Step 1: Analyse the Session

Before generating, silently assess:

1. **Work type** — What category does this session fall into? (see Work Type
   Classification)
2. **Complexity tier** — How deep is the work? (see Depth Sizing)
3. **Active state** — What is the current task, and where exactly did we stop?
4. **Decision chain** — What decisions were made and what was the reasoning?
5. **Dead ends** — What approaches were tried and rejected?

### Step 2: Check for User Instructions

If the user included specific instructions in their handoff request (e.g.
"create a handoff, make sure to include the rate limiting discussion"),
incorporate those. Do not ask for confirmation before generating. Produce the
best handoff possible from the session, and let the user request edits
afterwards.

### Step 3: Generate the Handoff Document

Build the document using the adaptive structure matching the work type and
complexity tier. Follow the format and content guidelines below.

### Step 4: Output

Save the handoff as a markdown file:

**Path:** `.claude/handoffs/[YYYY-MM-DD]-[description].md`

Create the `.claude/handoffs/` directory if it does not exist.

Use a short, descriptive slug for the filename (e.g.
`2026-06-07-auth-middleware.md`, `2026-06-07-api-rate-limiting.md`).

---

## Work Type Classification

Classify the session to determine which structural sections are most relevant.
If a session spans multiple types, use the primary type and pull in sections
from secondary types.

### Feature Implementation
Building new functionality, adding endpoints, creating components.

**Key sections:** Objective, Implementation State, Architecture/Design Decisions,
Files Modified, Remaining Work, Issues Encountered.

### Bug Fixing / Debugging
Diagnosing and fixing issues, investigating unexpected behaviour.

**Key sections:** Problem Description, Reproduction Steps, Hypotheses Tested,
Root Cause (if found), Fix Applied (if any), Remaining Hypotheses.

### Refactoring
Restructuring existing code without changing behaviour.

**Key sections:** Objective, Refactoring Strategy, What Has Been Refactored,
Patterns Being Applied, Files Remaining, Regressions to Watch For.

### Configuration / Setup
Environment setup, dependency management, build configuration, tooling.

**Key sections:** Objective, Configuration Changes Made, What Works Now, What
Does Not Work Yet, Environment-Specific Details.

### Architecture / Design
High-level design discussions, structural decisions, API design.

**Key sections:** Objective, Options Considered, Decisions Made (with rationale),
Constraints, Design Artefacts (diagrams, schemas), Open Design Questions.

### Testing
Writing or fixing tests, improving coverage, test infrastructure.

**Key sections:** Objective, Test Strategy, Tests Written, Coverage Gaps
Remaining, Test Failures Under Investigation.

### Mixed / General
Sessions spanning multiple types or not fitting neatly into one category.

**Key sections:** Use the universal structure and pull in type-specific sections
as needed.

---

## Depth Sizing

The codebase itself provides significant context. The handoff captures what the
codebase cannot: intent, rationale, failed approaches, and session-specific
state. Size accordingly.

### Light (roughly 200–400 words)
Simple, focused tasks. One file or a small change, few decisions, clear next
steps.

Examples: fixing a straightforward bug, adding a simple utility function,
updating a config value.

### Standard (roughly 400–800 words)
Moderate tasks touching several files. Meaningful decisions made, some
investigation involved.

Examples: implementing a new API endpoint, debugging an intermittent test
failure, setting up a new build tool.

### Deep (roughly 800–1500 words)
Complex work with significant decision-making, multiple files involved,
established patterns or conventions being followed.

Examples: implementing a multi-component feature, resolving a complex bug after
several failed hypotheses, refactoring a module with many dependents.

### Extended (roughly 1500+ words)
Use sparingly. For sessions with extensive investigation, large architectural
decisions, or multiple interconnected workstreams.

These are guidelines. Prioritise capturing decisions and rationale thoroughly
over hitting a word count. A handoff that explains *why* a decision was made in
two extra sentences is better than one trimmed for brevity.

---

## Handoff Document Structure

Every handoff follows this skeleton. Sections are included or excluded based on
work type and relevance. Do not include empty sections.

```markdown
# Handoff: [Descriptive Title]

> **Resumption instruction:** Read this handoff, review the listed files,
> then confirm your understanding in 2–3 sentences before proceeding.

**Date:** [YYYY-MM-DD]
**Project:** [project path or name]
**Work type:** [Feature / Bug Fix / Refactoring / Config / Architecture / Testing / Mixed]
**Status:** [In Progress / Paused / Nearing Completion / Blocked]

---

## Objective

[What we are trying to accomplish and why. Enough context that a fresh session
understands both the task and its motivation.]

## Current State

[Precise snapshot of where the work stands right now. What exists, what works,
what does not. This is a state description, not a narrative.]

## What Was Done

[Concrete actions taken this session. Focus on outcomes, not conversation
history.]

- [Action] — [outcome or result]
- [Action] — [outcome or result]

## Decisions Made

[Each decision with its rationale. The rationale prevents the new session from
relitigating settled questions.]

- **[Decision]** — [Why this was chosen. What alternatives were considered.]

## Approaches That Did Not Work

[Directions explored and rejected. Include what was tried and why it failed or
was abandoned. This is one of the highest-value sections — it prevents the new
session from repeating failed work.]

- **[Approach]** — [Why it did not work]

## Files Modified

[Files changed during this session, with a brief note on what and why. The
new session can read these files directly.]

- `path/to/file.ext` — [What was changed and the intent]

## Issues / Errors Encountered

[Specific error messages, unexpected behaviours, or blockers. Include exact
error text where relevant — these are hard to rediscover.]

## Open Questions

[Unresolved items needing attention.]

- [ ] [Specific question]

## Next Steps

[Ordered list of what to do next. The first item is the very next action.]

1. [First action — specific and concrete]
2. [Second action]
3. [Third action]

## Files to Review on Resume

[Key files the new session should read to get up to speed. Only include files
that are central to understanding the current state of the work.]

- `path/to/file.ext` — [Why this file matters]
```

---

## Content Guidelines

### Always Include

1. **Objective with motivation** — The fresh session needs to understand both
   the task and why it matters.
2. **Precise current state** — Not "we worked on the API" but "the
   `/users` endpoint returns 200 with correct data, the `/auth` endpoint
   throws a 401 on valid tokens, investigation ongoing."
3. **Decisions with rationale** — Without the "why", the new session may
   unknowingly reverse a carefully considered choice.
4. **Failed approaches** — The most common failure mode in session handoffs is
   the new session retrying something that has already been tried and rejected.
   Document what did not work and why.
5. **Actionable next steps** — Clear enough that the receiving session knows
   exactly what to do first.
6. **Files modified and files to review** — The new session can read these
   immediately to rebuild context from the code.

### Include When Relevant

- **Exact error messages** — Hard to rediscover, easy to lose.
- **Reproduction steps** — For bugs or issues still under investigation.
- **Key code patterns** — When a convention or pattern was established that
  future code should follow (e.g. "all new endpoints use the `withAuth`
  middleware wrapper").
- **Interface contracts** — When an API shape, data format, or type signature
  was agreed upon but not yet fully implemented.
- **Environment-specific details** — Ports, config values, paths, service
  URLs that affect the work.

### Exclude

- **File contents** — The new session can read files directly. Do not
  reproduce code blocks unless they capture something non-obvious.
- **General knowledge** — Do not explain frameworks, libraries, or concepts
  Claude already knows.
- **Conversational narrative** — Capture state, not history. Not "we discussed
  whether to use middleware" but "decided to use middleware because [reason]."
- **Verbose command output** — Summarise results, do not paste full terminal
  output.
- **Intermediate reasoning** — If reasoning reached a conclusion, capture the
  conclusion and rationale, not every step.

---

## Quality Checklist

Before saving the handoff, verify:

- [ ] A fresh session reading this document could continue without asking the
      user to re-explain anything
- [ ] The current state is a precise snapshot, not a vague summary
- [ ] Every decision includes its rationale
- [ ] Failed approaches are documented with reasons for rejection
- [ ] Next steps are specific and immediately actionable
- [ ] File paths are accurate and complete
- [ ] No code is reproduced that the new session could read from disk
- [ ] No empty sections are included
- [ ] The document is appropriately sized for the complexity (lean but
      thorough on decisions and rationale)
