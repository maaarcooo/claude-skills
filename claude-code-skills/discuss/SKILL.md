---
description: Ask clarifying questions before proceeding with a task. Use when the user wants to discuss requirements, clarify scope, or seek direction before Claude starts work.
when_to_use: |
  Trigger when the user writes "discuss-first" in their message, or explicitly asks Claude to ask questions, clarify, or discuss direction before starting work.
  Do NOT trigger on general conversational use of "discuss" where the user wants Claude to explain or talk about a topic.
argument-hint: [plan]
---

When invoked, ask me questions for clarification or direction before proceeding with the task. Do not start any work until I've answered.

For complex or multi-step tasks, propose a concise plan after gathering my answers, then proceed after confirmation. For simple tasks, proceed directly once clarified.

If the argument "plan" is provided (`/discuss plan`), always propose a plan after gathering answers, regardless of task complexity.
