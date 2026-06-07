---
name: discuss
description: Prompt Claude to ask clarifying questions before proceeding with a task. Trigger when the user writes "discuss-first" or explicitly asks Claude to ask questions, clarify, or discuss direction before starting work. Do NOT trigger on general conversational use of "discuss" where the user wants Claude to explain or talk about a topic.
---

When triggered, **do not proceed with the task immediately**. Instead:

1. Ask focused clarifying questions about scope, requirements, constraints, preferences, or direction. Let complexity guide the number of questions.
2. Wait for answers before doing any work.
3. Then decide based on task complexity:
   - **Simple tasks**: Proceed directly with the clarified requirements.
   - **Complex or multi-step tasks**: Propose a concise plan first, then proceed after confirmation.
