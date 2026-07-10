---
name: resume
description: >
  Resume a Codex task from a handoff document by verifying it against the
  current codebase, summarising the actual state, and continuing from the next
  step. Use when explicitly invoked with $resume; text supplied alongside the
  invocation may name a handoff file or partial filename.
---

# Resume Session

Load a handoff document, verify it is still accurate, and resume where the
previous session left off.

## Available handoffs

Use the available file-search or shell tools to list up to ten Markdown files
from `handoffs/`, root-level `*-handoff-*.md`, `.claude/handoffs/`, and
`.codex/handoffs/`, newest first.

If no handoffs exist, tell the user there are no handoff documents
to resume from and suggest creating one with `$handoff` at the end of a
session.

## Which handoff to load

If the user supplies a filename or partial filename alongside `$resume`, read
the matching file from those listed above. Accept either the full filename or
a unique partial match. If no unique match is found, list the available
handoffs and ask the user to specify one.

If the user does not specify a handoff, read the most recent one.

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
     `find . -newer <selected-handoff-path> -type f -not -path "./handoffs/*" -not -path "./.claude/*" -not -path "./.codex/*" -not -path "./node_modules/*" -not -path "./.git/*"`
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

   **Exceptions — do not proceed automatically:**
   - If the first next step is marked **(user)**, it is an action only the
     user can perform. Prompt the user to do it (or to skip to the next
     Codex-executable step) instead of attempting it.
   - If the handoff lists **Possible Directions** instead of Next Steps, the
     previous session ended with direction deliberately undecided. Present
     the candidate directions as choices and wait for the user to pick one.

Keep the summary concise. The goal is to get productive immediately, not to
restate the entire handoff document.
