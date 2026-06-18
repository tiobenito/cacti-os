---
name: onboarding
description: "First-run setup interview. Use when the user says '/onboarding', 'set up my system', 'configure cacti', or is running for the first time."
allowed-tools: ["Read", "Write", "Edit", "Bash"]
---

# /onboarding — First-Run Interview

Welcome the user, then conduct a structured interview to populate their knowledge files. The goal: Claude should know who they are, what they're working on, and what they care about by the end.

**Take it conversational, not form-like.** Ask questions naturally. Follow up where interesting. Don't make it feel like filling out a form.

---

## Opening

Greet the user:

> "Welcome to Cacti OS. I'm going to ask you a series of questions to configure your personal AI chief of staff. It takes about 10 minutes, and afterwards I'll have enough context to be genuinely useful from day one.
>
> Ready? Let's start with who you are."

---

## Phase 1 — Identity (2 questions)

**Q1.** "What's your name, and what's your primary role or job right now?"

**Q2.** "What city and country are you in? (This helps with timezone and local context.)"

→ **Write to:**
- `life/profile.md` — name, role, location
- `CLAUDE.md` — update the identity section with their name

---

## Phase 2 — Projects (3 questions)

**Q3.** "What are your main work projects or responsibilities right now? Name them — even informal names are fine. For example: 'I run a newsletter, I'm building a SaaS, I do PM work at Company X.'"

**Q4.** "Any significant personal projects? Moving, learning something, a side business, a health goal — anything you want tracked and not forgotten?"

**Q5.** "Are these projects in local folders on your computer? If yes, what's the root path where you keep your code or project files? (For example: ~/projects/, ~/code/, ~/work/)"

→ **Write to:**
- `knowledge/registry.md` — add each project to the project map
- `life/projects/index.md` — populate the projects table
- If they gave a root path, update `scripts/discover-projects.sh` with their actual scan directories

---

## Phase 3 — Goals (2 questions)

**Q6.** "What are you trying to accomplish this year? Work and personal — just list them, doesn't need to be polished."

**Q7.** "What does 'winning' look like for you in 3-5 years? Not aspirational — what does a good version of your life actually look like?"

→ **Write to:**
- `life/goals/2026.md` — this year's goals
- `life/goals/long-term.md` — 3-5 year horizon
- `knowledge/goals.md` — concise goals summary

---

## Phase 4 — People (1 question)

**Q8.** "Who do you work with most? Colleagues, collaborators, clients — whoever you'd want Claude to know about. Name + role + how you interact with them."

→ **Write to:**
- `knowledge/contacts.md` — populate contacts table

---

## Phase 5 — Tools (1 question)

**Q9.** "What tools do you use daily for work? Tell me which of these apply:
- GitHub (code hosting)
- Slack (team messaging)
- Gmail / Google Calendar
- Notion
- Linear or Jira (project tracking)
- Anything else important?"

→ **Write to:**
- `.mcp.json` — uncomment the relevant MCP server configs
- `CLAUDE.md` Tool Routing section — add routing for their tools

**Note on MCP setup:** After the interview, tell them which MCP servers they'll want to install and point them to `docs/customizing.md` for setup instructions. Don't try to install MCPs automatically.

---

## Phase 6 — Skills Selection

Walk through each skill, explain what it does and what it needs, and ask if they want it configured.

**Script:**
> "This system ships with a few skills — Claude Code slash commands. Let me walk you through each one and we can figure out which ones make sense for you."

For each skill below:
1. Describe what it does in one sentence
2. Say what it requires (tools, setup)
3. Ask: "Does that sound useful?"
4. If yes, note it as active. If no, skip.

**Skills:**

| Skill | What it does | Requirements |
|-------|-------------|-------------|
| `/today` | Morning briefing — reads HANDOVER, tasks, calendar, inbox | Works immediately; better with Calendar/Gmail MCP |
| `/quick-task` | Capture a task in 2 seconds | No setup needed |
| `/log` | Log a note, meeting, or event to today's daily file | No setup needed |
| `/weekly-review` | Weekly synthesis — what happened, what's next, git activity | Works immediately; better with GitHub MCP |

All four are safe to enable — they read files and won't do anything destructive.

**If they want all four** (common): "Great, all four are ready to use."

**If they're unsure about any**: "You can always run any of these anytime — they're just there when you need them. No configuration required."

---

## Post-Interview: Write All Files

After completing all phases, write the populated versions of:
1. `life/profile.md` — name, role, location, anything personal they shared
2. `knowledge/registry.md` — their projects mapped out
3. `life/projects/index.md` — projects table
4. `life/goals/2026.md` — this year's goals
5. `life/goals/long-term.md` — long-term vision
6. `knowledge/goals.md` — concise goals summary
7. `knowledge/contacts.md` — their key people
8. `.mcp.json` — uncomment relevant servers
9. `CLAUDE.md` — update identity section

Each file should have a `<!-- POPULATED BY /onboarding — YYYY-MM-DD -->` comment at the top.

---

## Closing Summary

Print a summary:

```
Your system is configured. Here's what I set up:

Files populated: [list them]
Projects registered: [N]
Skills ready: /today, /quick-task, /log, /weekly-review

Next steps:
1. Try /today to see your morning briefing
2. Set up MCP servers for [their tools] — see docs/customizing.md
3. Run /log to capture notes as you work

Your registry, contacts, and knowledge files will improve automatically as you use the system.
```

---

## Design Notes

- **Don't over-generate.** Write seeded files, not perfect ones. The first week of use fills in the rest.
- **Don't ask for confirmation on every file write.** Write everything at the end, then show the summary.
- **Match their energy.** If they give terse answers, don't fish for more. If they're expansive, let it run.
- **No judgment.** Someone with 0 personal projects and 1 work goal is fine. Configure what's there.
