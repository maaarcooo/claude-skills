---
description: Ask clarifying questions and discuss direction before starting work. Use when the user wants to discuss requirements, clarify scope, or seek direction before Claude starts a task.
when_to_use: |
  Trigger when the user invokes "/discuss" or "discuss-first", or asks Claude to discuss, clarify, or ask questions before proceeding. Natural phrasings include "let's discuss before proceeding", "ask me questions for clarification or direction", and "let's discuss and make a plan first".
  Do NOT trigger on general conversational use of "discuss" where the user wants Claude to explain or talk about a topic and there is no task being held back.
argument-hint: [plan]
---

When invoked, treat this as the start of a genuine discussion about the
task, not a clarification checklist.

Before doing any work:

1. **Ground yourself first, if the task touches existing code.** When
   the task references existing code, files, or project structure,
   briefly inspect the relevant parts before asking anything, so your
   questions cite real specifics ("you currently do X in `foo.ts`, do
   you want this to change?") rather than abstractions. Keep the scan
   light — enough to ask informed questions, not a full audit. Skip
   this for greenfield or non-code tasks.
2. **Share your initial read.** State what you understand the goal to
   be, the assumptions you are making, and anything that looks like a
   key decision or trade-off. Engage with the specifics of this task.
3. **Ask focused questions that target real forks in direction.**
   Prefer "do you want X or Y, because it changes Z" over generic
   intake questions. Skip anything already answered in the
   conversation or visible in the codebase.
4. **Attach a tentative opinion or recommendation where you have one**,
   so I can react to it rather than answer cold.

Delivery style is your judgement. Default to one small batch of 3-5
questions. Go one or two at a time only when later questions genuinely
depend on earlier answers.

Do not start the task until I have responded. After my answers:

- For complex or multi-step tasks, propose a concise plan and wait for
  confirmation.
- For simple tasks, proceed directly once clarified.
- If the argument "plan" is provided (`/discuss plan`), always propose
  a plan after gathering answers, regardless of task complexity.
- Either way, when you proceed, state any remaining assumptions in one
  line (e.g. "proceeding with X and Y assumed") so nothing slips
  through silently.

Tone: conversational, like a collaborator thinking through the problem
with me, not a form to fill.
