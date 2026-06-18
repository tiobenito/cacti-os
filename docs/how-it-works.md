# How Cacti OS Works

## The Core Idea

Claude Code reads files from its working directory at session start. Cacti OS is a structured set of files that gives Claude everything it needs to act as a persistent, context-aware chief of staff — not just a chat interface.

When you open Claude Code from `~/cacti/`, it reads `CLAUDE.md` first. That file tells it:
- Who you are and what your role is
- What projects you're working on and where they live
- How to behave (when to push back, when to just execute)
- What skills are available
- What to do at session start and end

Then it reads `HANDOVER.md` — your active context file — which tells it where you left off.

The result: every session starts with full context, without you re-explaining anything.

## The Three-Layer Model

```
Layer 1: ~/cacti/        — strategy, knowledge, cross-project context
Layer 2: ~/projects/...  — individual project code and context
Layer 3: ~/.claude/      — Claude Code preferences, global skills
```

**Layer 1 (this repo)** is the chief of staff. It has the 10,000-foot view: your goals, your people, your projects, your open decisions.

**Layer 2** is where work happens. Each project can have its own `CLAUDE.md` with project-specific context — coding conventions, architecture decisions, how to run tests. When you navigate to a project directory, Claude picks up that context automatically.

**Layer 3** is your global Claude Code setup — API keys, personal preferences, skills you use across all projects.

## The Knowledge Files

```
knowledge/registry.md   — project map and routing table
knowledge/goals.md      — unified work + personal goals
knowledge/contacts.md   — key people
knowledge/calendar.md   — standing meetings and recurring dates
```

These are the reference files Claude checks when you ask things like "what am I supposed to be working toward?" or "who is Jordan?". They're plain markdown — update them directly or let Claude update them silently as you work.

The registry is special: it maps aliases to file paths. When you say "work on the newsletter", Claude looks up "newsletter" in the registry and knows to navigate to `~/projects/newsletter/`. It also knows which GitHub account to use and what MCP servers are relevant.

## The Life OS

```
life/profile.md          — who you are, what you love, non-negotiables
life/vision.md           — 3-10 year north star
life/goals/2026.md       — this year's goals
life/goals/long-term.md  — 3-5 year horizon
life/projects/index.md   — all life projects with status
life/projects/backburner.md — ideas on hold
life/decisions/log.md    — major decisions: what, why, optimizing-for
```

The Life OS is what makes Claude more than a task manager. When you're evaluating an opportunity, deciding whether to take on a new project, or making a tradeoff between work and personal life — Claude can reference what you've told it matters to you.

These files are yours to write. The Sage examples in each file show the format; delete them and replace with your own.

## HANDOVER.md — The Active Context File

This is the most important file in the system. It's the running record of:
- **Open threads** — everything in flight that Claude needs to know about
- **Pending actions** — things with explicit next steps
- **Recent decisions** — so Claude doesn't re-litigate settled questions
- **Session log** — a brief record of what happened each session

Claude updates this automatically at session end. You never need to maintain it manually — though you can add to it directly if something important happens outside of a session.

Think of it as the briefing document you'd hand to a new employee before every meeting: "here's what's going on, here's what we need to decide, here's what we already decided."

## Agents

Agents are scheduled Claude instances that monitor specific domains and write reports.

The `work/` agent checks your active work projects daily. The `finance/` agent reviews your financial picture weekly. Each writes a `latest-report.md` that `/today` picks up and includes in your morning briefing.

To run an agent: open Claude Code and say "run the work agent" or "run the finance agent." To schedule it automatically, use Claude Code's `/schedule` command.

See `agents/README.md` for the full architecture.

## Skills

Skills are Claude Code slash commands — structured prompts stored in `.claude/skills/`. When you type `/today`, Claude reads `.claude/skills/today/SKILL.md` and follows the instructions there.

The system ships with 5 skills:
- `/onboarding` — first-run setup
- `/today` — morning briefing
- `/quick-task` — fast task capture
- `/log` — note logging
- `/weekly-review` — weekly synthesis

You can write your own — see `docs/customizing.md`.

## The Self-Improvement Loop

The system is designed to get better as you use it:

- **Registry growth** — whenever you mention a project Claude doesn't know about, it asks once and registers it
- **Contact updates** — new people mentioned in logs get added to contacts.md silently
- **Knowledge compilation** — decisions and goal updates from conversations get written to the right files at session end

You don't maintain the system. The system maintains itself.
