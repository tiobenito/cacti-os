---
name: log
description: "Log a note or event. Use when the user says '/log', 'log this', 'note that', 'I just had a call', 'meeting with', 'just talked to', or wants to record something that happened."
argument-hint: "<note>"
allowed-tools: ["Read", "Write", "Edit"]
---

# /log — Note Capture

Append a timestamped note to today's daily file.

## Workflow

1. Get current date and time
2. Read or create `daily/YYYY-MM-DD.md`
3. Append the note under a `## Log` section:

```markdown
## Log

- **14:32** — Had a call with Jordan — wants the new onboarding flow spec by Friday
- **16:15** — Sent proposal to Tanya, waiting for response
```

4. **Task detection** — if the note implies a task ("wants X by Y", "need to", "should"), offer to add it:
   > "Sounds like a task: 'Write onboarding flow spec by Friday'. Add it?"

5. **Contact detection** — if the note mentions a person not in `knowledge/contacts.md`, or adds context about an existing contact, update contacts.md silently.

6. **Knowledge detection** — if the note contains a decision, deadline, or goal-relevant update, update the relevant knowledge file silently.

## Daily File Format

If the file doesn't exist yet:

```markdown
# [Day of Week], [Month] [Day] [Year]

## Log

- **HH:MM** — {note}
```

If it already exists, append to the `## Log` section. Create the section if missing.

## Rules

- Don't ask for confirmation on the log entry
- Only offer task detection when it's clearly a task
- Contact and knowledge updates are silent
- Confirm: "Logged. [+ any silent updates made]"
