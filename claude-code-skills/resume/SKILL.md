---
description: >
  Resume work from the most recent handoff document. Reads the handoff,
  summarises current state, reviews key files, and continues from the
  next step.
disable-model-invocation: true
argument-hint: "[optional handoff filename]"
allowed-tools: Bash(ls *) Bash(cat *)
---

# Resume Session

Load a handoff document and resume where the previous session left off.

## Available handoffs

!`ls -1t .claude/handoffs/*.md 2>/dev/null | head -10`

If no handoffs are listed above, tell the user there are no handoff documents
to resume from and suggest creating one with `/handoff` at the end of a
session.

## Which handoff to load

If arguments are provided ($ARGUMENTS), read that file from `.claude/handoffs/`.
Accept either the full filename or a partial match against the files listed
above. If no match is found, list the available handoffs and ask the user to
specify.

If no arguments are provided, read the most recent handoff (first file listed
above).

## Resume process

After reading the handoff document:

1. **Review key files** — Read each file listed in "Files to Review on Resume"
   to rebuild context from the code
2. **Check the chain** — If the handoff has a "Previous Session" reference and
   carryover context that still matters, note it
3. **Present a brief summary:**
   - Where we left off (current state from the handoff)
   - The immediate next step
   - Any blockers, open questions, or warnings
4. **Confirm understanding** in 2-3 sentences, then proceed with the first
   next step

Keep the summary concise. The goal is to get productive immediately, not to
restate the entire handoff document.
