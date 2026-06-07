# Resume (Claude Code)

A `/resume` slash command that loads a handoff document and gets you
productive immediately. Companion to the `/handoff` skill.

## The Problem

Starting a new Claude Code session after a handoff requires manually telling
Claude which file to read, what to review, and where to pick up. Even with a
well-structured handoff document, the first few exchanges are spent on
orientation rather than work.

## The Solution

`/resume` automates the pickup. It finds the most recent handoff (or a
specific one you name), reads it, reviews the key files listed in it, and
presents a brief summary of where you are and what to do next, then
continues working.

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

1. Lists available handoffs in `.claude/handoffs/` (via dynamic shell
   injection at load time)
2. Reads the most recent handoff, or the one matching your argument
3. Reads each file listed in "Files to Review on Resume" from the handoff
4. Checks the handover chain for relevant carryover from earlier sessions
5. Presents a brief summary: current state, immediate next step, any
   blockers or warnings
6. Confirms understanding and proceeds with the first next step

## The Handoff/Resume Workflow

```
End of session:    /handoff              → saves .claude/handoffs/2026-06-07-auth.md
Start of session:  /resume               → loads the handoff, reviews files, continues
```

Together, `/handoff` and `/resume` create a two-command workflow for session
continuity. `/handoff` captures state. `/resume` restores it.

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
└── .claude/
    └── handoffs/
        ├── 2026-06-05-auth-endpoints.md
        ├── 2026-06-06-rate-limiting.md
        └── 2026-06-07-error-handling.md
```
