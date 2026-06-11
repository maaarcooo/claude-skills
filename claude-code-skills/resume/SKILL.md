---
description: >
  Resume work from the most recent handoff document. Reads the handoff,
  verifies it against the current state of the codebase, summarises where
  things stand, and continues from the next step.
disable-model-invocation: true
argument-hint: "[optional handoff filename]"
allowed-tools: Bash(ls *) Bash(cat *) Bash(find *) Bash(git log *) Bash(git status *) Bash(git diff *) Read
---

# Resume Session

Load a handoff document, verify it is still accurate, and resume where the
previous session left off.

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

1. **Verify against reality** — Treat the handoff's "Current State" as a
   claim, not a fact. The codebase may have changed since it was written
   (another session, a merge, manual edits). Check for drift:
   - If the project is a git repository (`git status` succeeds), run
     `git log --oneline --since="<handoff date>"` and `git status` to see
     commits and uncommitted changes made after the handoff.
   - If it is not a git repository, compare file modification times against
     the handoff file instead:
     `find . -newer .claude/handoffs/<handoff-file> -type f -not -path "./.claude/*" -not -path "./node_modules/*" -not -path "./.git/*"`
   - If drift is found, flag it explicitly in the summary and prefer the
     actual state of the files over the handoff's description wherever they
     disagree.
2. **Review key files** — Read each file listed in "Files to Review on Resume"
   to rebuild context from the code.
3. **Check the chain** — If the handoff has a "Previous Session" reference
   with live carryover, note it.
4. **Present a brief summary:**
   - Where we left off (current state from the handoff)
   - Any drift detected between the handoff and the actual codebase
   - The immediate next step
   - Any blockers, open questions, or warnings
5. **Confirm and proceed** — Confirm understanding in 2-3 sentences, state
   the first next step, then proceed with it unless the user redirects. If
   significant drift was detected, or the handoff is more than a few days
   old, pause and ask the user to confirm the next step is still the right
   one before starting work.

Keep the summary concise. The goal is to get productive immediately, not to
restate the entire handoff document.
