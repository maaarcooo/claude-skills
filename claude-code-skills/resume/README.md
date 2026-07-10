# Resume (Claude Code)

A `/resume` slash command that loads a handoff document and gets you
productive immediately. Companion to the `/handoff` skill.

## The Problem

Starting a new Claude Code session after a handoff requires manually telling
Claude which file to read, what to review, and where to pick up. Even with a
well-structured handoff document, the first few exchanges are spent on
orientation rather than work. And the handoff itself may be stale: the
codebase can change between sessions through merges, other sessions, or
manual edits.

## The Solution

`/resume` automates the pickup. It finds the most recent handoff (or a
specific one you name), reads it, verifies it against the actual state of
the codebase, reviews the key files listed in it, and presents a brief
summary of where you are and what to do next, then continues working.

## Installation

Place the skill at user-level alongside `/handoff`:

```bash
mkdir -p ~/.claude/skills/resume
# Copy SKILL.md to ~/.claude/skills/resume/SKILL.md
```

## Usage

```
/resume                              Load the most recent handoff
/resume 2026-06-07-auth-middleware   Load a specific handoff by filename
/resume auth                         Partial match against available handoffs
```

## What It Does

1. Lists available handoffs in `handoffs/` (via dynamic shell injection at
   load time)
2. Reads the most recent handoff, or the one matching your argument
3. Verifies the handoff against reality: in a git repository it checks
   `git log` and `git status` for changes made after the handoff date; in a
   non-git project it compares file modification times against the handoff
   file. Detected drift is flagged, and the actual files win over the
   handoff's description wherever they disagree
4. Reads each file listed in "Files to Review on Resume" from the handoff
5. Checks the handover chain for relevant carryover from earlier sessions
6. Presents a brief summary: current state, any drift detected, immediate
   next step, blockers or warnings
7. Confirms understanding and proceeds with the first next step

## When It Pauses Instead of Proceeding

`/resume` proceeds automatically in the normal case, but stops and asks you
first when:

- **Significant drift** was detected between the handoff and the codebase,
  or the handoff is more than a few days old
- **The first next step is marked (user)** — an action only you can perform
  (reviewing output, merging, publishing). Claude prompts you rather than
  attempting it
- **The handoff lists Possible Directions instead of Next Steps** — the
  previous session ended with direction deliberately undecided, so Claude
  presents the candidates for you to choose from

## The Handoff/Resume Workflow

```
End of session:    /handoff              → saves handoffs/2026-06-07-auth.md
Start of session:  /resume               → loads, verifies, reviews files, continues
```

Together, `/handoff` and `/resume` create a two-command workflow for session
continuity. `/handoff` captures state. `/resume` restores and verifies it.

## File Structure

Both skills are installed at user-level:

```
~/.claude/skills/
├── handoff/
│   └── SKILL.md
└── resume/
    └── SKILL.md
```

Handoff documents are saved per-project:

```
your-project/
└── handoffs/
    ├── 2026-06-05-auth-endpoints.md
    ├── 2026-06-06-rate-limiting.md
    └── 2026-06-07-error-handling.md
```

## Note on Non-Git Projects

The drift check falls back to file modification times when the project is
not a git repository. This is reliable in normal single-machine use, but
copying a project between machines resets modification times and can cause
missed or spurious drift warnings. In git projects the check uses commit
history and is unaffected.
