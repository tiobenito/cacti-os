---
name: today
description: "Morning briefing. Trigger on 'what's my day', 'today', 'morning brief', 'plan my day', 'what should I focus on'."
allowed-tools: ["Read", "Bash", "Glob"]
---

# /today — Morning Briefing

Produce a concise morning briefing. Under 20 lines. Action-oriented.

## Steps

1. **Read `HANDOVER.md`** — what's open, what's pending, what needs a decision
2. **Read `tasks.md`** — what's active and what's in the inbox
3. **Check calendar** — if Google Calendar MCP is connected, get today's events; if not, check `knowledge/calendar.md` for standing meetings
4. **Check inbox** — if Gmail MCP is connected, scan for unread that need action today
5. **Read agent reports** — if `agents/*/latest-report.md` files exist and were updated in the last 48 hours, include a one-line summary of anything flagged
6. **Assemble the briefing**

## Output Format

```
Good morning. Here's your day.

**Open threads:** [N items from HANDOVER needing attention, or "none"]

**Today's tasks:**
- [Task 1] — [status]
- [Task 2] — [status]

**Calendar:**
- [HH:MM] — [event]
- [HH:MM] — [event]
(or: "No calendar connected — check knowledge/calendar.md for standing meetings")

**Inbox (worth acting on):**
- [sender]: [subject]
(or: "No Gmail connected")

**Agent flags:**
- [finance agent]: [one-line flag]
(or: skip this section if no fresh agent reports)

**Focus:** [One recommended deep-work block based on open threads + tasks]
```

## Rules

- Keep it scannable — no paragraphs
- Skip empty sections entirely (no "Calendar: nothing today")
- If a thread in HANDOVER has a "Next:" action, show that as the first task
- If no MCPs are connected, brief from files only — say clearly what's missing
- Never fabricate calendar events or emails that weren't in the data
