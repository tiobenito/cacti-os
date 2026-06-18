# Customizing Cacti OS

## Adding a Project to the Registry

The registry (`knowledge/registry.md`) maps project names to file paths. Add a row:

```markdown
| newsletter, sage-writes | ~/projects/newsletter/ | personal | Weekly newsletter |
```

Now when you say "work on the newsletter", Claude routes to `~/projects/newsletter/` and picks up that project's `CLAUDE.md` if it exists.

You can also just tell Claude: "Add my newsletter project at ~/projects/newsletter/ to the registry" and it'll do it.

## Setting Up a Project's Context

Any project directory can have its own `CLAUDE.md` with project-specific instructions. Claude reads it when you're working in that directory.

A good project CLAUDE.md includes:
- What this project is and why it exists
- How to run it (setup, start server, run tests)
- Key architectural decisions
- What to avoid or watch out for

Example:
```markdown
# Newsletter

Weekly PM newsletter at newsletter.example.com.

## Stack
Ghost CMS, custom templates, Mailchimp for sending.

## How to run locally
npm start — runs at localhost:2368

## Publishing workflow
1. Write draft in Ghost admin
2. Review preview
3. Schedule for Tuesday 8am

## Conventions
- Drafts go in `drafts/` as markdown before moving to Ghost
- Each issue gets a folder: `issues/YYYY-MM-DD/`
```

## Writing a Custom Skill

Skills live in `.claude/skills/<skill-name>/SKILL.md`. The format:

```markdown
---
name: skill-name
description: "When to trigger this skill — what the user might say"
allowed-tools: ["Read", "Write", "Edit", "Bash"]
---

# Skill Title

What this skill does in one sentence.

## Steps

1. [Step 1]
2. [Step 2]

## Output

[What format the output should take]
```

To use it: type `/skill-name` in Claude Code.

Example use cases for custom skills:
- `/client-update` — generates a weekly status update email for a specific client
- `/sprint-review` — summarizes the week's engineering work for a team
- `/prep-call` — pulls context before a meeting with someone in your contacts

## Adding an Agent

1. Create the directory: `agents/<name>/`
2. Create `AGENT.md` — use `agents/work/AGENT.md` as a template
3. Create `state.md` — empty initially
4. Create `reports/` directory (empty)
5. Mention the agent in your `CLAUDE.md` so `/today` knows to include its reports

Template `AGENT.md` structure:
```markdown
# [Domain] Agent

## Identity
What this agent monitors, what it's trying to surface.

## Scope
What it watches. What goals it measures against.

## Data Sources
Files, APIs, MCP tools it checks.

## Cadence
Daily / Weekly / etc.

## Permissions
Read-only to data sources. Write only to this agent's directory.

## What to Flag
Urgent / Attention / Proactive criteria.
```

## Scheduling Agents

Use Claude Code's built-in `/schedule` command:

```
/schedule "run the finance agent and write a report" every Sunday at 8pm
```

Or for the work agent:
```
/schedule "run the work agent" every weekday at 7am
```

Claude Code handles the scheduling — no cron setup needed.

## Setting Up MCP Servers

MCPs connect Claude to external tools. The `.mcp.json` in this repo has commented configs for common servers. Uncomment what you use and add the required env vars.

**GitHub:**
```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
  }
}
```
Get a token at: github.com/settings/tokens (scope: `repo`)

**Slack:**
```json
"slack": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-slack"],
  "env": {
    "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
    "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
  }
}
```

**Notion:**
```json
"notion": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-notion"],
  "env": {
    "NOTION_API_TOKEN": "${NOTION_API_TOKEN}"
  }
}
```

Full list of available MCP servers: [modelcontextprotocol.io/servers](https://modelcontextprotocol.io/servers)

After adding servers, restart Claude Code for them to take effect.

## Multi-Machine Setup

The system is designed for a single machine. If you use multiple machines:

1. Push this repo to a private GitHub repo
2. Clone it on each machine: `git clone <url> ~/cacti`
3. The knowledge files sync via git — commit and push regularly
4. Daily files, logs, and agent reports are gitignored (machine-specific)

The memory system (`~/.claude-personal/`) doesn't sync — it's intentionally local.

## Keeping the System Healthy

Run `/weekly-review` at the end of each week. It:
- Surfaces what was accomplished
- Flags goals that are off track
- Suggests pruning stale HANDOVER threads
- Checks if your Life OS files need updating

The system works best when `HANDOVER.md` is kept clean. Long-resolved threads should be removed. Decisions that are settled should be compiled to knowledge files, not left in HANDOVER.

Claude does this automatically at session end — but a weekly review is a good forcing function to catch anything that slipped through.
