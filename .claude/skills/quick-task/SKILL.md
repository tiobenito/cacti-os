---
name: quick-task
description: "Quick task capture. Use when the user says '/quick-task', 'add a task', 'remind me to', 'todo', 'I need to', or wants to capture something quickly."
argument-hint: "<task description> [project] !priority"
allowed-tools: ["Read", "Write", "Edit"]
---

# /quick-task — Task Capture

Append a task to `tasks.md`. Zero friction.

## Input Parsing

Parse the user's input for:
- **Task description** — the main text
- **Project tag** — in `[brackets]`, resolve via `knowledge/registry.md` if possible
- **Priority** — `!high`, `!medium`, `!low` (default: medium)
- **Due date** — if mentioned ("by Friday" → convert to YYYY-MM-DD)

## Examples

| Input | Parsed |
|-------|--------|
| `/quick-task Review Q3 roadmap [work] !high` | Task: Review Q3 roadmap, Project: work, Priority: high |
| `/quick-task Call dentist by Friday` | Task: Call dentist, Due: [next Friday], Priority: medium |
| `/quick-task Buy coffee beans` | Task: Buy coffee beans, Project: none, Priority: medium |

## Workflow

1. Read `tasks.md`
2. Parse the input
3. Append to the Inbox section: `- [ ] {description} [{project}] !{priority} ({date-added})`
4. Confirm: "Added: {description}"

## Format

```markdown
- [ ] Review Q3 roadmap [work] !high (2026-03-19)
- [ ] Call dentist !medium due:2026-03-21 (2026-03-19)
- [ ] Buy coffee beans !medium (2026-03-19)
```

No confirmation dialogs. Just append and confirm in one line.
