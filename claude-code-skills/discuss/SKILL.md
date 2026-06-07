---
description: Ask clarifying questions before proceeding with a task. Use when the user wants to discuss requirements, clarify scope, or seek direction before Claude starts work.
when_to_use: |
  Trigger when the user writes "discuss-first" in their message, or explicitly asks Claude to ask questions, clarify, or discuss direction before starting work.
  Do NOT trigger on general conversational use of "discuss" where the user wants Claude to explain or talk about a topic.
argument-hint: [plan]
---

When invoked, **do not proceed with the task immediately**. Instead:

1. Ask focused clarifying questions about scope, requirements, constraints, preferences, or direction. Let complexity guide the number of questions.
2. Wait for answers before doing any work.
3. Then decide based on task complexity:
   - **Simple tasks**: Proceed directly with the clarified requirements.
   - **Complex or multi-step tasks**: Propose a concise plan first, then proceed after confirmation.

If the argument "plan" is provided (`/discuss plan`), always propose a plan after gathering answers, regardless of task complexity.
