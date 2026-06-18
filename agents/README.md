# Agents

Autonomous domain agents that monitor specific areas of your work and life. Each agent runs on a schedule, checks its data sources, and writes a report for the system to synthesize during `/today`.

## Architecture

```
Chief of Staff (orchestrator)
 |
 |-- reads agent reports during /today
 |-- routes your decisions back to agents
 |
 +-- agents/
      +-- example/   Template — copy this to create your own agents
      +-- work/      (your agent, once created)
      +-- finance/   (your agent, once created)
```

## How Agents Work

1. A scheduled trigger runs the agent on its cadence
2. The agent reads its `AGENT.md` (identity, scope, data sources)
3. The agent reads its `state.md` (what it flagged last time, pending decisions)
4. The agent checks its data sources (files, Linear, Slack, GitHub, Gmail)
5. The agent writes `latest-report.md` (what `/today` reads)
6. The agent updates `state.md` (what to remember for next run)
7. The agent archives the report to `reports/YYYY-MM-DD.md`

## Conventions

- **Agents never duplicate project data.** They read from project folders; they don't copy into their own.
- **Agents are read-only by default.** They surface and recommend — they don't execute unless you give explicit permission.
- **Reports are concise.** Action items first, context second. Max 30 lines for the summary section.
- **State tracks decisions.** When you say "defer X" or "ignore Y," the agent records it in `state.md` so it doesn't re-flag.

## Report Format

```markdown
# [Agent Name] Report — YYYY-MM-DD

## Needs Your Attention
- [urgent/decision-needed items]

## Status Updates
- [what changed since last report]

## Standing Down
- [things checked that are fine — brief]

## Recommendations
- [proactive suggestions, if any]
```

## Running an Agent

To run an agent manually, open Claude Code from `~/cacti/` and say:

> "Run the work agent" or "Run the finance agent"

Claude will read the agent's `AGENT.md`, check its data sources, and write a report.

## Adding a New Agent

1. Copy `agents/example/` to `agents/<name>/` — e.g. `agents/work/`, `agents/finance/`, `agents/health/`
2. Edit `AGENT.md` to define the scope, data sources, and what to flag
3. Set up a scheduled trigger with the appropriate cadence (see Scheduling section below)
4. Mention the agent in your `CLAUDE.md` so `/today` picks it up

## Scheduling Agents

To run an agent automatically on a schedule, use Claude Code's `/schedule` command:

```
/schedule "run the finance agent" every Sunday at 8pm
```

See `docs/customizing.md` for more on scheduling.
