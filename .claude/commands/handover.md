# Update Active Context

Runs automatically before `/compact`. Keeps HANDOVER.md current so the next session starts with accurate context, then compiles knowledge into persistent files.

**Normal workflow:** user runs `/compact` → this runs first → context is compressed → next session reads the updated HANDOVER.md.

## Step 1: Update HANDOVER.md

Read the existing `HANDOVER.md` and update based on this session's work:

**Open Threads:**
- Add new threads for multi-session workstreams that emerged this session
- Update existing threads with new status, last-touched date
- Mark threads `Resolved` if work is complete
- A thread is a multi-session workstream. One-off tasks go in `tasks.md`, not as threads.

**Triage:**
- Short-lived buffer for things that came up but need routing before becoming a task
- At each `/today`, empty this: promote real items to `tasks.md`, drop the rest
- Default: leave empty. Bias toward dropping, not capturing.
- Never duplicate items already in `tasks.md`.

**Recent Decisions:**
- Add decisions made this session with date
- Remove decisions older than 7 days (they should already be compiled)

**Session Log:**
- Add one-line entry for this session (date, summary)
- Keep only the last 7 entries

## Step 2: Prune

- Remove threads marked `Resolved` — append to the current week's archive file (see below)
- Flag (don't remove) threads untouched for 14+ days — add `[STALE]` to status
- When dropping session log entries beyond the last 7, append them to the week's archive
- Keep HANDOVER.md under 80 lines. If growing past that, threads need resolution or decisions need compiling.

**Archive:** `handover/YYYY-MM-DD.md` where the date is the most recent Monday.
- One file per week. Append pruned content to the current week's file.
- Create the file if it doesn't exist. Never delete archive files.
- Header: `# Handover Archive — Week of YYYY-MM-DD`

## Step 3: Knowledge Compilation Pass

Scan this session for knowledge to compile into persistent files:

| Signal | Target | Action |
|--------|--------|--------|
| Strategic or architectural decision | `life/decisions/log.md` | Add entry (What/Optimizing for/Trade-off) |
| Project status changed | `knowledge/goals.md` | Update project row |
| New person mentioned | `knowledge/contacts.md` | Add row |
| Contact's role/context changed | `knowledge/contacts.md` | Update row |
| Goal achieved or revised | `life/goals/2026.md` | Update in place |
| Recurring meeting changed | `knowledge/calendar.md` | Update |
| Non-obvious lesson or feedback | `memory/<topic>.md` | Add entry, update MEMORY.md index |

After compiling, mark decisions in HANDOVER.md as compiled.

## Step 4: Confirm

Output a brief summary:
```
Context saved. [N threads active]
Knowledge compiled: [files updated, or "none this session"]
```

## HANDOVER.md Format

```markdown
# Active Context

Last updated: YYYY-MM-DD

## Open Threads

### [Thread Name]
**Status:** In progress | Blocked | Waiting on [X] | Resolved — **Since:** YYYY-MM-DD
- Current state bullets
- Key files: [paths]

## Triage

Short-lived buffer. Items either get promoted to `tasks.md` or dropped at next `/today`.

_(empty)_

## Recent Decisions
- YYYY-MM-DD: [Decision summary] → compiled to [file] / awaiting compilation

## Session Log
- YYYY-MM-DD: One-line session summary
- YYYY-MM-DD: Another session
```

## Rules

- **Under 80 lines.** Working document, not a report.
- **Threads persist until resolved**, not until midnight.
- **Thread ≠ task.** Threads are multi-session context. Tasks live in `tasks.md`.
- **Triage is a buffer, not storage.** Empty it at each `/today`.
- **Always run the knowledge compilation pass**, even if nothing to compile.
- **Archive, never delete.** Pruned content goes to `handover/YYYY-MM-DD.md`.
- **Skip for trivial sessions** — quick lookups don't need a handover update.
