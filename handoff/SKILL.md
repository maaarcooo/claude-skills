---
name: handoff
description: >
  Create a structured handoff document for seamless continuity across Claude
  conversations. Use when the user explicitly asks to create a handoff, handover,
  or session transfer document. Trigger phrases include: "create a handoff",
  "handoff document", "handover", "save session", "continue later", "session
  handoff", "transfer context", or "/handoff". Do NOT trigger for general
  conversation summaries, meeting notes, or when the user simply asks "summarise
  this conversation" without handoff/continuity intent.
---

# Session Handoff Skill

Create a structured markdown document that enables a fresh Claude conversation to continue the current task seamlessly. The handoff captures the full working state: goals, progress, decisions, context, and next steps, so the receiving session can pick up exactly where this one left off.

## When to Use

- The user explicitly requests a handoff or handover document
- Before ending a long or complex conversation that has unfinished work
- When switching focus to a different task and wanting to return later
- When approaching context limits and needing to start fresh

## Process

### Step 1: Analyse the Session

Before generating, silently assess:

1. **Work type** — What category does this session fall into? (see Work Type Classification below)
2. **Complexity tier** — How deep and multi-faceted is the work? (see Depth Sizing below)
3. **Active state** — What is the current task, and where exactly did we stop?
4. **Accumulated context** — What knowledge, constraints, preferences, and decisions were established during this conversation that would be costly to re-establish?

### Step 2: Check for User Instructions

If the user included specific instructions in their handoff request (e.g. "create a handoff, make sure to include X"), incorporate those. Do not ask for confirmation or clarification before generating. Produce the best handoff possible from the conversation, and let the user request edits afterwards.

### Step 3: Generate the Handoff Document

Build the document using the adaptive structure matching the work type and complexity tier. Follow the format and content guidelines below.

### Step 4: Output

Save the handoff as a markdown file:

**Filename:** `handoff-[brief-description].md`
Use a short, descriptive slug (e.g. `handoff-epq-silicon-anode-research.md`, `handoff-website-results-page.md`).

Present the file for download.

---

## Work Type Classification

Classify the session into one of these categories to determine which structural sections are most relevant. If a session spans multiple types, use the primary type and pull in relevant sections from secondary types.

### Research / Investigation
Exploring a topic, gathering sources, evaluating information, forming conclusions.

**Key sections:** Objective, Findings So Far, Sources and Evidence, Open Questions, Methodology/Approach, Conclusions Reached, Gaps Remaining.

### Writing / Drafting
Producing or editing text: essays, applications, emails, articles, documentation.

**Key sections:** Objective, Current Draft State (what exists, what stage it is at), Tone and Style Decisions, Structural Outline, Content Completed vs Remaining, Feedback Incorporated, Editorial Decisions.

### Planning / Strategy
Designing plans, making decisions, evaluating options, setting direction.

**Key sections:** Objective, Options Considered, Decisions Made (with rationale), Constraints and Requirements, Current Plan State, Unresolved Questions, Dependencies.

### Building / Technical
Creating something: websites, apps, designs, configurations, data work.

**Key sections:** Objective, Architecture/Structure Decisions, What Has Been Built, Technical Choices (with rationale), File and Asset References, Issues Encountered, Remaining Implementation.

### Learning / Exploration
Understanding a concept, working through problems, studying material.

**Key sections:** Objective, Concepts Covered, Key Takeaways, Areas of Confusion Remaining, Resources Used, Practice Problems Attempted, Topics Still to Cover.

### Problem-Solving / Debugging
Diagnosing an issue, troubleshooting, iterating toward a solution.

**Key sections:** Objective, Problem Description, Hypotheses Tested, What Worked / What Did Not, Current Diagnosis, Remaining Approaches to Try.

### Mixed / General
Sessions that do not fit neatly into one category, or span several.

**Key sections:** Use the universal structure (see below) and pull in type-specific sections as needed.

---

## Depth Sizing

Assess the complexity of the work to determine how comprehensive the handoff should be. The handoff should be thorough enough that a fresh session can continue without asking the user to re-explain anything, but should not include filler or information Claude would already know.

### Light (roughly 300–600 words)
Simple, focused tasks nearing completion. One clear objective, few decisions made, minimal accumulated context.

Examples: drafting a short email, answering a factual question with follow-ups, a quick calculation or lookup with discussion.

### Standard (roughly 600–1200 words)
Moderate tasks with meaningful progress and several decisions. Some established context that would take effort to rebuild.

Examples: editing and refining a personal statement section, researching university entry requirements across several institutions, planning a website page layout.

### Deep (roughly 1200–2500 words)
Complex, multi-faceted work with significant accumulated context. Many decisions, established constraints, domain knowledge built up during the session, or long iterative work.

Examples: extensive EPQ research session with source evaluation, multi-page website build with design system decisions, detailed UCAS strategy planning across multiple universities, a long debugging session with multiple failed approaches.

### Extended (roughly 2500+ words)
Use sparingly. For sessions where the conversation itself has been the workspace: extensive back-and-forth producing refined outputs, large accumulated decision chains, or sessions covering multiple interconnected workstreams.

These word counts are guidelines, not hard limits. Prioritise completeness over brevity. A handoff that is slightly too long is far less costly than one that is too short and forces the user to re-explain context.

---

## Handoff Document Structure

Every handoff document follows this skeleton. Sections are included or excluded based on work type and relevance. Do not include empty sections.

```markdown
# Handoff: [Descriptive Title]

> **Resumption instruction:** Review this document, then confirm your
> understanding in 2–3 sentences before proceeding with the next step.

**Date:** [DD-MM-YYYY]
**Work type:** [Research / Writing / Planning / Building / Learning / Problem-Solving / Mixed]
**Status:** [In Progress / Paused / Nearing Completion / Blocked]

---

## Objective

[Clear statement of what we are trying to accomplish. This is the north star
for the receiving session. Include enough context that a fresh session
understands not just WHAT but WHY.]

## Current State

[Where exactly we stopped. Not a summary of the conversation, but a precise
snapshot of the working state. What exists right now? What stage is the work
at? If there is a draft, describe its current form. If there is a plan,
describe how far through it we are.]

## Progress

[What has been accomplished in this session. Concrete outputs and milestones,
not a narrative of the conversation. Use concise entries.]

## Decisions Made

[Decisions established during this session, each with its rationale. The
rationale is critical — it prevents the new session from relitigating settled
questions.]

- **[Decision]** — [Why this was chosen over alternatives]

## Approaches That Did Not Work

[Things we tried that failed, or directions we explored and rejected. Include
why they were rejected. This prevents the new session from wasting time
re-exploring dead ends.]

## Project Context

[Stable background information, constraints, preferences, and domain knowledge
that was established or referenced during the session. This is the equivalent
of the "reference document" in a two-file system — the information that does
not change between sessions but is essential for the work.

Only include this section when there is meaningful context beyond what is
obvious from the objective. Skip for simple tasks.]

## Open Questions

[Unresolved items that need attention. Frame these as specific questions, not
vague areas.]

- [ ] [Specific question needing resolution]

## Next Steps

[Ordered list of what to do next. These should be immediately actionable by
the receiving session. The first item should be the very next thing to do.]

1. [First action — specific and concrete]
2. [Second action]
3. [Third action]

## Key References

[Links, file names, sources, or other materials that are relevant to
continuing the work. Only include if there are meaningful references.]
```

---

## Content Guidelines

### Always Include

1. **The objective with enough context to understand the "why"** — A fresh session with no conversation history needs to understand not just the task but the motivation and scope.
2. **Precise current state** — Where exactly the work stands right now. Not "we discussed the layout" but "the layout is finalised as a two-column grid with sidebar navigation, and the header component is built but the footer is not."
3. **Decisions with rationale** — The reasoning behind decisions is more valuable than the decisions themselves. Without rationale, the new session may unknowingly reverse a carefully considered choice.
4. **Failed approaches** — What was tried and rejected, and why. This is one of the highest-value sections because it prevents the most common failure mode: the new session repeating work that has already been done.
5. **Actionable next steps** — Clear enough that the receiving session knows exactly what to do first without asking.

### Include When Relevant

- **Tone, style, or voice decisions** — For writing tasks where these were explicitly established.
- **Structural outlines or plans** — When a plan or structure has been agreed upon and guides the remaining work.
- **User preferences or constraints** — Things the user stated about how they want the work done (but do not duplicate information that is already in Claude's memory system).
- **Technical specifics** — Exact values, configurations, or specifications that would be hard to rediscover.
- **Source evaluations** — For research tasks, which sources were found useful and which were not.

### Exclude

- **Conversational narrative** — Do not retell the conversation. The handoff captures state, not history.
- **General knowledge** — Do not explain concepts or background that Claude already knows. "We discussed how spaced repetition works" adds nothing. "We decided to use 2-day initial intervals based on the user's revision schedule" adds value.
- **Intermediate reasoning** — If a line of reasoning reached a conclusion, capture the conclusion and rationale, not every step of the reasoning.
- **Verbose tool output** — Do not reproduce long outputs, search results, or file contents. Summarise or reference them.
- **Pleasantries and meta-discussion** — Nothing about the conversation itself.

---

## Verification Instruction

Every handoff document begins with this resumption instruction immediately after the title:

```
> **Resumption instruction:** Review this document, then confirm your
> understanding in 2–3 sentences before proceeding with the next step.
```

This serves as a lightweight check. The receiving session reads the handoff, confirms its understanding in a brief statement, and then proceeds with the first next step. This catches misinterpretations before they compound, at the cost of only one short exchange.

---

## Quality Checklist

Before outputting the handoff, verify:

- [ ] A fresh session reading this document would understand the objective without any additional explanation
- [ ] The current state is a precise snapshot, not a vague summary
- [ ] Every decision includes its rationale
- [ ] Failed approaches are documented to prevent re-exploration
- [ ] Next steps are specific and immediately actionable
- [ ] No empty sections are included
- [ ] No conversational narrative or filler is present
- [ ] Stable project context is included where it would otherwise need to be re-established
- [ ] The document is appropriately sized for the complexity of the work (not over-compressed for token efficiency, not padded with unnecessary detail)
