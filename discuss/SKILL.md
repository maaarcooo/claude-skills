---
name: discuss
description: Ask clarifying questions and discuss direction before starting work. Trigger whenever the user asks Claude to discuss, clarify, or ask questions before proceeding with a task. Natural phrasings include "let's discuss before proceeding", "ask me questions for clarification or direction", "let's discuss and make a plan first", "clarify the direction before starting", and "feel free to ask me anything before you start". Also trigger on the explicit keyword "discuss-first". Do NOT trigger on conversational uses of "discuss" where the user simply wants Claude to explain or talk about a topic and there is no task being held back.
---

When triggered, treat this as the start of a genuine discussion about the
task, not a clarification checklist.

Before doing any work:

1. **Share your initial read.** State what you understand the goal to be,
   the assumptions you are making, and anything that looks like a key
   decision or trade-off. Engage with the specifics of this task, not
   the category of task.
2. **Ask focused questions that target real forks in direction.** Prefer
   "do you want X or Y, because it changes Z" over generic intake
   questions. Skip anything already answered in the conversation, the
   uploaded files, or memory.
3. **Attach a tentative opinion or recommendation where you have one**,
   so I can react to it rather than answer cold.

Delivery style is your judgement. Default to one small batch of 3-5
questions. Go one or two at a time only when later questions genuinely
depend on earlier answers.

Do not start the task until I have responded. After my answers:

- For complex or multi-step tasks, propose a concise plan and wait for
  confirmation.
- For simple tasks, proceed directly once clarified.
- Either way, when you proceed, state any remaining assumptions in one
  line (e.g. "proceeding with X and Y assumed") so nothing slips
  through silently.

Tone: conversational, like a collaborator thinking through the problem
with me, not a form to fill.
