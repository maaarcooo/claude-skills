---
name: handoff
description: >
  Create a structured handoff document for Codex task continuity, capturing
  decisions, rationale, failed approaches, current state, and next steps so a
  fresh task can continue without re-explanation. Use when explicitly invoked
  with $handoff; text supplied alongside the invocation may identify a focus.
---

# Session Handoff

Generate a handoff document capturing the session state that is not visible
from the codebase alone: intent, decisions, rationale, failed approaches, and
next steps. The codebase shows **what** changed. The handoff explains **why**
and **what's next**.

If the user supplies a focus alongside `$handoff`, focus the document on that
aspect of the task. Otherwise, generate a full-task handoff.

## Previous handoffs

Use the available file-search or shell tools to list up to five Markdown files
in `.codex/handoffs/`, newest first. If the directory does not exist or contains
no handoffs, continue without a previous-session reference.

If previous handoffs exist, read the most recent one and reference it
at the top of the new handoff under a "Previous Session" heading.

**Carryover rule:** the "Previous Session" note must *restate* any context
from earlier sessions that is still live — open questions, unresolved bugs,
standing constraints, conventions being followed — not merely link to the
previous file. Each handoff must be self-sufficient: a session reading only
the newest handoff should have everything still relevant. Context that is no
longer live should be dropped, so stale items do not propagate forever.

**Retention:** if more than ~10 handoffs have accumulated in
`.codex/handoffs/`, suggest to the user that older ones be archived or
deleted — superseded handoffs add noise when listing and resuming.

## Coverage rule

**No discussed topic disappears.** Every substantive discussion thread in the
session must map to exactly one of:

- **Decisions Made** — an outcome was reached: record it with rationale and
  provenance
- **Approaches That Did Not Work** — a direction was rejected: record it with
  the reason (technical failure or user veto)
- **Open Discussions** — explored but not concluded: record the topic, the
  positions considered, and why it was left unresolved

When unsure whether a discussion was substantive enough to record, include
its conclusion — a one-line entry costs little, a lost thread costs the user
a re-explanation. Capture the *residue* of each discussion (what was
concluded and why, or why nothing was concluded), never the back-and-forth
itself.

## Process

1. Create `.codex/handoffs/` if it does not exist
2. Classify the work type and complexity to determine structure and depth
3. If previous handoffs exist, read the most recent one and apply the
   carryover rule above
4. Generate the handoff document, applying the coverage rule
5. Save to `.codex/handoffs/[YYYY-MM-DD]-[description].md`

---

## Work type classification

Classify the session to determine which structural sections are most relevant.
If a session spans multiple types, use the primary type and pull in relevant
sections from secondary types.

### Feature Implementation
Building new functionality, adding endpoints, creating components.

**Key sections:** Objective, Implementation State, Architecture/Design
Decisions, Files Modified, Remaining Work, Issues Encountered.

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

**Key sections:** Objective, Options Considered, Decisions Made (with
rationale), Constraints, Design Artefacts (diagrams, schemas), Open Design
Questions.

### Testing
Writing or fixing tests, improving coverage, test infrastructure.

**Key sections:** Objective, Test Strategy, Tests Written, Coverage Gaps
Remaining, Test Failures Under Investigation.

### Mixed / General
Sessions spanning multiple types or not fitting neatly into one category.

**Key sections:** Use the universal structure and pull in type-specific
sections as needed.

---

## Depth sizing

Assess the complexity of the work to determine how comprehensive the handoff
should be. The codebase provides significant context, so the handoff captures
what the code cannot: intent, rationale, failed approaches, and session-specific
state. Be complete on decisions, rationale, and failed approaches; ruthless on
everything else. The coverage rule takes precedence over the word counts: if
recording every discussion's residue pushes past a tier's range, that is
acceptable — trim narrative, never conclusions.

### Light (roughly 200-400 words)
Simple, focused tasks. One file or a small change, few decisions, clear next
steps.

Examples: fixing a straightforward bug, adding a simple utility function,
updating a config value.

### Standard (roughly 400-800 words)
Moderate tasks touching several files. Meaningful decisions made, some
investigation involved.

Examples: implementing a new API endpoint, debugging an intermittent test
failure, setting up a new build tool.

### Deep (roughly 800-1500 words)
Complex work with significant decision-making, multiple files involved,
established patterns or conventions being followed.

Examples: implementing a multi-component feature, resolving a complex bug
after several failed hypotheses, refactoring a module with many dependents.

### Extended (roughly 1500+ words)
Use sparingly. For sessions with extensive investigation, large architectural
decisions, or multiple interconnected workstreams.

These word counts are calibration guidelines, not targets to fill.

---

## Document structure

Every handoff follows this skeleton. Include or exclude sections based on work
type and relevance. Do not include empty sections. Reference files by path
rather than reproducing content.

```markdown
# Handoff: [Descriptive Title]

> **Resumption instruction:** Read this handoff, review the listed files,
> then confirm your understanding in 2-3 sentences before proceeding.
> Items marked (user) are user-stated: decisions so marked are fixed and
> must not be revisited without asking; steps so marked must be prompted
> to the user, not attempted.

**Date:** [YYYY-MM-DD]
**Project:** [project path]
**Work type:** [Feature / Bug Fix / Refactoring / Config / Architecture / Testing / Mixed]
**Status:** [In Progress / Paused / Nearing Completion / Blocked]

## Previous Session
<!-- Only if prior handoffs exist -->
- Handoff: `.codex/handoffs/[previous-filename].md`
- Live carryover: [restate everything from earlier sessions that is still
  relevant — open questions, constraints, conventions. Self-sufficient, not
  just a pointer.]

---

## Objective

[What we are trying to accomplish and why. Include enough context that a fresh
session understands both the task and its motivation.]

## Current State

[Precise snapshot of where the work stands. Not a summary of the conversation,
but the actual state. What works, what doesn't, what is partially complete.
Not "we worked on the API" but "the /users endpoint returns 200 with correct
data, the /auth endpoint throws a 401 on valid tokens, investigation ongoing."]

## What Was Done

[Concrete actions taken this session. Focus on outcomes, not conversation
history.]

- [Action] — [outcome or result]
- [Action] — [outcome or result]

## Decisions Made

[Each decision with its rationale AND its origin. Mark decisions that came
from the user — explicit requirements, directions, vetoes, stated opinions —
with **(user)**: these are fixed, and the receiving session must not revisit
them without asking. Unmarked decisions are session choices, revisable with
good reason. The user accepting a Codex proposal counts as unmarked unless
the user added a reason of their own.]

- **(user)** **[Requirement/direction]** — [The user's stated reason, if given]
- **[Decision]** — [Why this was chosen. What alternatives were considered.]

## Approaches That Did Not Work

[Directions explored and rejected. Include what was tried and why it failed
or was abandoned. Distinguish HOW it was rejected: if it failed technically,
give the failure; if the user rejected it, say so and capture their stated
reason — a user veto is not evidence the approach cannot work, and the
receiving session needs to know the difference.]

- **[Approach]** — [Why it did not work]
- **[Approach]** — Rejected by user: [their stated reason]

## Open Discussions

[Topics discussed but not concluded. For each: the topic, the positions or
options considered, and why it was left unresolved (ran out of time, needs
information, user undecided). Without this section, unconcluded threads
vanish and the next session unknowingly starts them from scratch.]

- **[Topic]** — Considered: [positions/options]. Unresolved because: [reason]

## Files Modified

[Files changed during this session, with a brief note on what and why. The
new session can read these files directly.]

- `path/to/file.ext` — [What was changed and the intent]

## Issues / Errors Encountered

[Specific error messages, unexpected behaviours, or blockers. Include exact
error text where relevant — these are hard to rediscover.]

## Open Questions

[Unresolved items needing attention. Frame as specific questions, not vague
areas.]

- [ ] [Specific question]

## Next Steps

[Ordered list of what to do next. The first item is the very next action.
Clear enough that the receiving session knows exactly what to do first. Mark
any step only the user can perform with **(user)** — the receiving session
should prompt for these, not attempt them.]

1. [First action — specific and concrete]
2. **(user)** [Action the user must perform, e.g. reviewing output, merging,
   publishing a release]
3. [Third action]

## Possible Directions

[Use INSTEAD of Next Steps when the user has deliberately not chosen what to
work on next. State "Direction undecided" and list the candidate directions as
options with a one-line case for each. The receiving session should present
these as choices, not pick one and proceed.]

- **[Candidate direction]** — [Why it might be next]

## Files to Review on Resume

[Key files the new session should read to get up to speed. Only include files
that are central to understanding the current state of the work.]

- `path/to/file.ext` — [Why this file matters]
```

---

## Content guidelines

### Always include

1. **Objective with motivation** — A fresh session with no conversation history
   needs to understand not just the task but why it matters and the scope.
2. **Precise current state** — Where exactly the work stands right now as a
   state description, not a narrative. What exists, what works, what is broken,
   what is incomplete.
3. **Decisions with rationale and provenance** — The reasoning behind decisions
   is more valuable than the decisions themselves, and the origin determines
   how the receiving session treats them: user-stated requirements are fixed,
   session choices are revisable.
4. **User-stated requirements, directions, constraints, and opinions** —
   Everything the user said about what they want, what is off-limits, and how
   they want the work done that is not obvious from the code. These carry
   the **(user)** marker wherever they appear.
5. **Failed approaches, with how they failed** — Technical failure vs user
   rejection, each with its reason. This prevents the most common failure mode
   in session handoffs: the new session retrying something already ruled out —
   or wrongly treating a user veto as a technical impossibility.
6. **Every substantive discussion's residue** — Per the coverage rule: as a
   decision, a rejected approach, or an open discussion. No thread vanishes.
7. **Actionable next steps** — Clear enough that the receiving session knows
   exactly what to do first without asking. User-only actions marked
   **(user)**. If direction is genuinely undecided, use Possible Directions
   instead — do not invent a priority the user never set.
8. **Files modified and files to review** — The new session can read these
   immediately to rebuild context from the code.

### Include when relevant

- **Exact error messages** — Hard to rediscover, easy to lose. Include the
  full error text when it is central to ongoing debugging.
- **Reproduction steps** — For bugs or issues still under investigation, the
  exact steps to reproduce the problem.
- **Key code patterns** — When a convention or pattern was established that
  future code should follow (e.g. "all new endpoints use the `withAuth`
  middleware wrapper").
- **Interface contracts** — When an API shape, data format, or type signature
  was agreed upon but not yet fully implemented.
- **Environment-specific details** — Ports, config values, paths, service URLs,
  environment variables that affect the work.

### Exclude

- **File contents** — The new session can read files directly. Do not reproduce
  code blocks unless they capture something not obvious from the file itself
  (e.g. a subtle bug, a specific pattern being followed, a key interface
  contract).
- **General knowledge** — Do not explain frameworks, libraries, or concepts
  Codex already knows. "We discussed how middleware works" adds nothing.
  "Decided to use middleware over route-level auth because [reason]" adds value.
- **Conversational narrative** — Capture each discussion's residue, not its
  back-and-forth. Not "we discussed whether to use middleware, first
  considering X, then the user said Y..." but "decided to use middleware
  because [reason]" — or, if unconcluded, an Open Discussions entry.
- **Verbose command output** — Summarise results, do not paste full terminal
  output or tool responses.
- **Intermediate reasoning** — If reasoning reached a conclusion, capture the
  conclusion and rationale, not every step of the reasoning process.

---

## Quality checklist

Before saving the handoff, verify:

- [ ] A fresh session reading this document could continue without asking the
      user to re-explain anything
- [ ] Every substantive discussion from the session appears as a decision, a
      rejected approach, or an open discussion — no thread has vanished
- [ ] The current state is a precise snapshot, not a vague summary
- [ ] Every decision includes its rationale, and user-originated decisions,
      requirements, and vetoes carry the **(user)** marker
- [ ] Failed approaches are documented with reasons, distinguishing technical
      failure from user rejection
- [ ] The "Previous Session" carryover (if present) restates live context
      rather than only linking the previous file
- [ ] Next steps are specific and immediately actionable, with user-only
      actions marked **(user)** — or Possible Directions used if direction
      is undecided
- [ ] File paths are accurate and complete
- [ ] No code is reproduced that the new session could read from disk
- [ ] No empty sections are included
- [ ] No conversational narrative or filler is present
- [ ] The document is appropriately sized for the complexity of the work
