---
name: handoff
description: >
  Create a structured handoff document for seamless continuity across Claude
  conversations. Use when the user explicitly asks to create a handoff, handover,
  or session transfer document, or signals they want to stop now and continue
  this work in a future conversation. Trigger phrases include: "create a handoff",
  "handoff document", "handover", "save session", "continue later", "session
  handoff", "transfer context", "let's pick this up tomorrow", "save this so we
  can continue next time", or "/handoff". Do NOT trigger for general
  conversation summaries, meeting notes, or when the user simply asks "summarise
  this conversation" without handoff/continuity intent. Do NOT trigger when the
  user uploads an existing handoff document to resume from — handoff documents
  are self-contained and carry their own resumption instructions; this skill is
  for creating them only.
---

# Session Handoff Skill

Create a structured markdown document that enables a fresh Claude conversation to continue the current task seamlessly. The handoff captures working state — goals, progress, decisions, context, and next steps — so the receiving session picks up exactly where this one left off.

## When to Use

- The user explicitly requests a handoff or handover document
- The user signals they are stopping now and want to continue the work in a later conversation
- Before ending a long or complex conversation with unfinished work
- When approaching context limits and needing to start fresh

**Not for resuming.** If the user has uploaded a handoff document and wants to continue from it, the document itself contains everything needed — follow its embedded resumption instruction and do not use this skill.

## Coverage Rule

**No discussed topic disappears.** Every substantive discussion thread in the session must map to exactly one of:

- **Decisions Made** — an outcome was reached: record it with rationale and provenance
- **Approaches That Did Not Work** — a direction was rejected: record it with the reason (it failed, or the user rejected it)
- **Open Discussions** — explored but not concluded: record the topic, the positions considered, and why it was left unresolved

When unsure whether a discussion was substantive enough to record, include its conclusion — a one-line entry costs little, a lost thread costs the user a re-explanation. Capture the *residue* of each discussion (what was concluded and why, or why nothing was concluded), never the back-and-forth itself.

## Process

### Step 1: Analyse the Session

Silently assess:

1. **Work type** — Which category fits? (see Work Type Classification)
2. **Complexity tier** — How deep is the work? (see Depth Sizing)
3. **Active state** — What is the current task, and where exactly did we stop?
4. **Accumulated context** — What knowledge, constraints, and decisions were established that would be costly to re-establish? What did the user state about requirements, direction, and preferences?

### Step 2: Check for User Instructions

If the user included specific instructions in their handoff request (e.g. "create a handoff, make sure to include X", or a stated direction for the next session), incorporate those.

### Step 3: Clarify Ambiguities (Conditional)

**Skip this step entirely if the session state is clear.** Ask **at most 2-3 short, specific questions** only when a genuine ambiguity would produce a materially different handoff:

- **Scope** — The session covered multiple distinct topics and it is unclear which the handoff should cover.
- **Decision status** — Something was discussed at length but not clearly resolved. Unclear whether to record it as settled or open. (If genuinely unconcluded, it belongs in Open Discussions — only ask when the conversation suggests it *was* settled but the outcome is ambiguous.)
- **Priority / direction** — Ask only when the conversation suggests the user already has a preferred next direction that was left unstated, and the ordering would materially change the handoff. **An undecided direction is a valid end state, not an ambiguity.** If the user simply has not chosen what to work on next, do not ask — record it (see Possible Directions below).

**Do not ask:** open-ended questions ("anything specific you want me to capture?", "what do you want to work on next?"), questions answered or implied in the conversation, or questions about minor details that would not change the handoff's usefulness.

### Step 4: Generate the Handoff Document

Build the document using the adaptive structure matching the work type and complexity tier, applying the Coverage Rule.

### Step 5: Output

Save as a markdown file and present it for download.

**Filename:** `YYYY-MM-DD-handoff-[brief-description].md`
Use today's date and a short descriptive slug (e.g. `2026-06-11-handoff-epq-silicon-anode-research.md`). The date prefix keeps multiple handoffs sortable and prevents collisions.

---

## Work Type Classification

Classify the session to determine which structural sections are most relevant. If a session spans multiple types, use the primary type and pull in sections from secondary types.

### Research / Investigation
Exploring a topic, gathering sources, evaluating information, forming conclusions.
**Key sections:** Objective, Findings So Far, Sources and Evidence, Open Questions, Methodology, Conclusions Reached, Gaps Remaining.

### Writing / Drafting
Producing or editing text: essays, applications, emails, articles, documentation.
**Key sections:** Objective, Current Draft State, Tone and Style Decisions, Structural Outline, Content Completed vs Remaining, Editorial Decisions.

### Planning / Strategy
Designing plans, making decisions, evaluating options, setting direction.
**Key sections:** Objective, Options Considered, Decisions Made (with rationale), Constraints, Current Plan State, Unresolved Questions, Dependencies.

### Building / Technical
Creating something: websites, apps, designs, configurations, data work.
**Key sections:** Objective, Architecture/Structure Decisions, What Has Been Built, Technical Choices (with rationale), File and Asset References, Issues Encountered, Remaining Implementation.

### Learning / Exploration
Understanding a concept, working through problems, studying material.
**Key sections:** Objective, Concepts Covered, Key Takeaways, Areas of Confusion Remaining, Resources Used, Topics Still to Cover.

### Problem-Solving / Debugging
Diagnosing an issue, troubleshooting, iterating toward a solution.
**Key sections:** Objective, Problem Description, Hypotheses Tested, What Worked / What Did Not, Current Diagnosis, Remaining Approaches to Try.

### Mixed / General
Use the universal structure and pull in type-specific sections as needed.

---

## Depth Sizing

Size the handoff to the complexity of the work. Be **complete on decisions, rationale, and failed approaches; ruthless on everything else**. The receiving session pays to read every word, and an overlong handoff buries the next-step signal. The handoff fails only if the user has to re-explain something — not if it omits things Claude already knows.

The Coverage Rule takes precedence over the word counts: if recording every discussion's residue pushes past a tier's range, that is acceptable — trim narrative, never conclusions.

- **Light (roughly 300–600 words)** — Simple, focused tasks nearing completion. One clear objective, few decisions, minimal accumulated context.
- **Standard (roughly 600–1200 words)** — Moderate tasks with meaningful progress and several decisions. Some context that would take effort to rebuild.
- **Deep (roughly 1200–2500 words)** — Complex, multi-faceted work: many decisions, established constraints, domain knowledge built up during the session, or long iterative work.
- **Extended (roughly 2500+ words)** — Use sparingly. For sessions where the conversation itself has been the workspace: large decision chains or multiple interconnected workstreams.

These counts are calibration guidelines, not targets to fill.

---

## Handoff Document Structure

Every handoff follows this skeleton. Include or exclude sections based on work type and relevance. **Never include empty sections.**

```markdown
# Handoff: [Descriptive Title]

> **Resumption instruction:** Review this document, then confirm your
> understanding in 2–3 sentences before proceeding with the next step.
> This document is self-contained — do not consult or load the handoff
> skill; it is for creating handoffs, not resuming from them.
> Items marked (user) are user-stated: decisions so marked are fixed and
> must not be revisited without asking; steps so marked must be prompted
> to the user, not attempted.

**Date:** [YYYY-MM-DD]
**Work type:** [Research / Writing / Planning / Building / Learning / Problem-Solving / Mixed]
**Status:** [In Progress / Paused / Nearing Completion / Blocked]

---

## Objective

[What we are trying to accomplish and why. The north star for the receiving
session — enough context to understand motivation and scope, not just the task.]

## Current State

[A precise snapshot of where the work stands right now — not a summary of the
conversation. Not "we discussed the layout" but "the layout is finalised as a
two-column grid with sidebar navigation; the header is built, the footer is not."]

## Progress

[Concrete outputs and milestones accomplished this session. Concise entries,
not narrative.]

## Decisions Made

[Each decision with its rationale AND its origin. Mark decisions that came
from the user — explicit requirements, directions, vetoes, stated opinions —
with **(user)**: these are fixed, and the receiving session must not revisit
them without asking. Unmarked decisions are session choices, revisable with
good reason. The user accepting a Claude proposal counts as unmarked unless
the user added a reason of their own.]

- **(user)** **[Requirement/direction]** — [The user's stated reason, if given]
- **[Decision]** — [Why this was chosen over alternatives]

## Approaches That Did Not Work

[Directions tried and rejected, with reasons. Distinguish HOW each was
rejected: if it failed on its merits, give the reason; if the user rejected
it, say so and capture their stated reason — a user veto is not evidence the
approach cannot work, and the receiving session needs to know the difference.
Prevents the most common failure mode: re-exploring dead ends.]

- **[Approach]** — [Why it did not work]
- **[Approach]** — Rejected by user: [their stated reason]

## Open Discussions

[Topics discussed but not concluded. For each: the topic, the positions or
options considered, and why it was left unresolved (ran out of time, needs
information, user undecided). Without this section, unconcluded threads
vanish and the next session unknowingly starts them from scratch.]

- **[Topic]** — Considered: [positions/options]. Unresolved because: [reason]

## Project Context

[Stable background: constraints, preferences, and domain knowledge established
during the session that does not change between sessions. Only include when
there is meaningful context beyond the objective. Do not duplicate information
already in Claude's memory system.]

## Open Questions

- [ ] [Specific question needing resolution — not a vague area]

## Next Steps

[Ordered and immediately actionable. The first item is the very next thing to
do. Mark any step only the user can perform with **(user)** — the receiving
session should prompt for these, not attempt them.]

1. [First action — specific and concrete]
2. **(user)** [Action the user must perform, e.g. reviewing output, publishing]

## Possible Directions

[Use INSTEAD of Next Steps when the user has deliberately not chosen what to
work on next. State "Direction undecided" and list the candidate directions as
options with a one-line case for each. The receiving session should present
these as choices, not pick one and proceed.]

- **[Candidate direction]** — [Why it might be next]

## Key References

[Links, file names, or sources relevant to continuing. Every artifact produced
in this session (scripts, files, documents) must be referenced by a retrievable
location — a path, URL, or repo — or explicitly marked as not preserved. A
reference the receiving session cannot retrieve is not a reference.]
```

---

## Content Guidelines

**Include:**
- User-stated requirements, directions, constraints, and opinions — everything the user said about what they want, what is off-limits, and how they want the work done. These carry the **(user)** marker wherever they appear
- Tone, style, or voice decisions explicitly established during writing tasks
- Agreed structural outlines or plans that guide remaining work
- Technical specifics (exact values, configurations) that would be hard to rediscover
- Source evaluations for research tasks: which sources proved useful and which did not

**Exclude:**
- **Conversational narrative** — capture each discussion's residue, not its back-and-forth. Not "we discussed the layout, first considering X, then the user said Y..." but "decided on two-column layout because [reason]" — or, if unconcluded, an Open Discussions entry
- **General knowledge** — "We discussed how spaced repetition works" adds nothing. "Decided on 2-day initial intervals to fit the revision schedule" adds value
- **Intermediate reasoning** — capture conclusions and rationale, not every step
- **Verbose tool output** — summarise or reference, never reproduce
- **Pleasantries and meta-discussion**

---

## Quality Checklist

Before outputting, verify:

- [ ] A fresh session could continue without asking the user to re-explain anything
- [ ] Every substantive discussion from the session appears as a decision, a rejected approach, or an open discussion — no thread has vanished
- [ ] Current State is a precise snapshot, not a vague summary
- [ ] Every decision includes its rationale, and user-originated decisions, requirements, and vetoes carry the **(user)** marker
- [ ] Failed approaches are documented with reasons, distinguishing genuine failure from user rejection
- [ ] Next steps are specific and immediately actionable, with user-only actions marked **(user)** — or Possible Directions used if direction is undecided
- [ ] Every in-session artifact has a retrievable location or is marked not preserved
- [ ] No empty sections, no narrative filler, no duplicated memory content
- [ ] Sized to the work: complete on decisions and rationale, lean everywhere else — conclusions never trimmed for length
