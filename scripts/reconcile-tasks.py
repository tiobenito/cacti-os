#!/usr/bin/env python3
"""Reconcile dashboard state with tasks.md + propagate to downstream files.

Reads today's `daily/YYYY-MM-DD-tasks-state.json`, compares each entry to the
corresponding row in `tasks.md`, and applies any missing updates. Then
for rows with `origin:` markers pointing to other files (HANDOVER.md or a
project TASKS.md), propagates the current status there.

Prints a JSON summary to stdout. Exits non-zero only on hard failures.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

CACTI = Path(__file__).resolve().parent.parent
TASKS_MD = CACTI / "tasks.md"
DAILY = CACTI / "daily"
HANDOVER = CACTI / "HANDOVER.md"

ID_MARKER_RE = re.compile(r"<!--\s*id:([A-Za-z0-9_\-]+)(?:\s+origin:([^\s>]+))?\s*-->")


def load_state_for_today():
    today = date.today().isoformat()
    p = DAILY / f"{today}-tasks-state.json"
    if not p.exists():
        return today, {}
    try:
        return today, json.loads(p.read_text() or "{}")
    except json.JSONDecodeError:
        return today, {}


INBOX_BULLET_RE = re.compile(r"^(\s*- \[)([ xX])(\]\s+)(.*)$")


def parse_tasks_md():
    """Return task rows from Active table AND Inbox bullets."""
    if not TASKS_MD.exists():
        return []
    rows = []
    section = None
    in_table = False
    for i, line in enumerate(TASKS_MD.read_text().splitlines()):
        if line.startswith("## Active"):
            section = "active"
            in_table = False
            continue
        if line.startswith("## Inbox"):
            section = "inbox"
            in_table = False
            continue
        if line.startswith("## "):
            section = None
            in_table = False
            continue

        if section == "active":
            if line.strip().startswith("| Task"):
                in_table = True
                continue
            if line.strip().startswith("|------"):
                continue
            if not in_table or not line.startswith("|"):
                continue
            m = ID_MARKER_RE.search(line)
            if not m:
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 4:
                continue
            rows.append({
                "line_index": i,
                "id": m.group(1),
                "origin": m.group(2) or "cacti",
                "task": cells[0],
                "status": cells[1],
                "due": cells[2],
                "notes": cells[3],
                "kind": "table",
            })
        elif section == "inbox":
            bm = INBOX_BULLET_RE.match(line)
            if not bm:
                continue
            m = ID_MARKER_RE.search(line)
            if not m:
                continue
            is_checked = bm.group(2).lower() == "x"
            body = bm.group(4)
            title_clean = re.sub(r"<!--.*?-->", "", body).strip()
            rows.append({
                "line_index": i,
                "id": m.group(1),
                "origin": m.group(2) or "cacti",
                "task": title_clean,
                "status": "done" if is_checked else "not started",
                "due": "",
                "notes": "",
                "kind": "bullet",
            })
    return rows


STATUS_UI_TO_MD = {
    "not_started": "not started",
    "in_progress": "in progress",
    "done": "done",
    "on_hold": "on hold",
}


def desired_status_from_state(task_id: str, state: dict):
    if state.get("deleted", {}).get(task_id):
        return None, True
    ui_status = state.get("status", {}).get(task_id)
    if ui_status:
        return STATUS_UI_TO_MD.get(ui_status, ui_status), False
    if state.get("done", {}).get(task_id):
        return "done", False
    return None, False


def propagate_to_handover(row) -> bool:
    if not HANDOVER.exists():
        return False
    text = HANDOVER.read_text()
    lines = text.splitlines(keepends=True)
    title = re.sub(r"<!--.*?-->", "", row["task"]).strip().strip("*")
    keywords = [w for w in re.split(r"[\s,.:;()]+", title) if len(w) > 3][:3]
    if not keywords:
        return False
    want_checked = row["status"] == "done"
    for i, line in enumerate(lines):
        if not re.match(r"^\s*- \[[ x]\]", line):
            continue
        if not all(k.lower() in line.lower() for k in keywords):
            continue
        is_checked = "[x]" in line.lower()[:8]
        if is_checked == want_checked:
            return False
        if want_checked:
            lines[i] = re.sub(r"\[ \]", "[x]", line, count=1)
        else:
            lines[i] = re.sub(r"\[x\]", "[ ]", line, count=1, flags=re.IGNORECASE)
        HANDOVER.write_text("".join(lines))
        return True
    return False


def propagate_to_project(row) -> bool:
    origin = row["origin"]
    if not origin.startswith("/"):
        return False
    target = Path(origin)
    if not target.exists():
        return False
    text = target.read_text()
    lines = text.splitlines(keepends=True)
    title = re.sub(r"<!--.*?-->", "", row["task"]).strip().strip("*")
    title_key = title[:60].lower()
    changed = False
    for i, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        if title_key not in line.lower():
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        if cells[1] == row["status"]:
            return False
        cells[1] = row["status"]
        lines[i] = "| " + " | ".join(cells) + " |\n"
        changed = True
        break
    if changed:
        target.write_text("".join(lines))
    return changed


def main():
    today, state = load_state_for_today()
    rows = parse_tasks_md()
    rows_by_id = {r["id"]: r for r in rows}

    synced_md = []
    synced_handover = []
    synced_projects = []
    unmatched = []

    for task_id, ui_status in (state.get("status") or {}).items():
        row = rows_by_id.get(task_id)
        if not row:
            unmatched.append({"id": task_id, "reason": "no row in tasks.md"})
            continue
        md_status = STATUS_UI_TO_MD.get(ui_status, ui_status)
        if row["status"] == md_status:
            continue
        row["status"] = md_status

    for task_id, _ in (state.get("deleted") or {}).items():
        pass

    rows = parse_tasks_md()
    for row in rows:
        if propagate_to_handover(row):
            synced_handover.append({"id": row["id"], "status": row["status"]})
        if row["origin"].startswith("/"):
            if propagate_to_project(row):
                synced_projects.append({
                    "id": row["id"],
                    "origin": row["origin"],
                    "row": row["task"][:60],
                    "status": row["status"],
                })

    print(json.dumps({
        "date": today,
        "synced_to_tasks_md": synced_md,
        "synced_to_handover": synced_handover,
        "synced_to_projects": synced_projects,
        "unmatched": unmatched,
    }, indent=2))


if __name__ == "__main__":
    main()
