---
name: weekly-review
description: "Weekly synthesis and planning. Use when the user says '/weekly-review', 'how was my week', 'weekly review', 'week in review', 'what did I do this week'."
allowed-tools: ["Bash", "Read", "Glob", "Grep", "Write"]
---

# /weekly-review — Weekly Synthesis

Produce a weekly review and forward plan. Save to `daily/weekly/YYYY-WXX.md`.

## Data Sources

Gather all of these (parallel where possible):

1. All daily files from past 7 days: `daily/YYYY-MM-DD.md`
2. `logs/activity.jsonl` — filter to past 7 days for git activity summary
3. `knowledge/goals.md` — targets to measure against
4. `HANDOVER.md` — active threads, recent decisions
5. `tasks.md` — what was added vs. completed this week
6. GitHub MCP (if connected) — PRs merged, opened, review activity
7. Calendar MCP (if connected) — meetings that happened this week

## Output Format

```markdown
# Week in Review — W{XX} ({Mon date} – {Sun date})

## Accomplishments
- [Completed items, shipped things, moved things forward]

## Personal Progress
- [Personal goals, habits, side projects — anything from daily logs]

## What Didn't Get Done
- [Planned but not completed]
- [Overdue items from tasks.md]

## Git Activity
| Repo | Commits | Key Changes |
|------|---------|-------------|
| [repo] | N | [summary] |

## Goals Check-in
| Goal | Status | Trend |
|------|--------|-------|
| [goal from knowledge/goals.md] | [on track / at risk / done] | [↑↓→] |

## Next Week Priorities
1. [Based on open threads + goals + what slipped]
2. [...]
3. [...]

## Open Questions
- [Anything that needs a decision]
- [Ambiguities noticed during the week]
```

## Save

Write to `daily/weekly/YYYY-WXX.md` (ISO week number).

## After Review

Offer to:
- Clear completed items from `tasks.md`
- Update `knowledge/goals.md` if anything shifted
- Flag any goal at risk
- Prune stale HANDOVER threads (untouched 14+ days)

## Life OS Check

Check if life files are getting stale:

```bash
for f in life/profile.md life/goals/2026.md life/goals/long-term.md life/projects/index.md; do
  echo "$f: $(stat -f '%Sm' -t '%Y-%m-%d' "$f" 2>/dev/null || echo 'not found')"
done
```

If any file is more than 21 days old without an update, suggest a quick review:
> "Your [profile / goals] hasn't been updated in [N] days. Want to do a quick check-in?"

Suggest once per weekly review. Don't repeat if they say not now.
