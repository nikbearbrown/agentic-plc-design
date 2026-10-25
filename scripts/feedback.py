#!/usr/bin/env python3
"""Feedback ledger tools: new entry, validate, regenerate the index.

  python3 scripts/feedback.py new --lab lab-09 --section 3 --reporter JP --kind wrong --severity major
  python3 scripts/feedback.py check
  python3 scripts/feedback.py index

An entry is feedback/entries/FB-NNNN.md: simple `key: value` front matter, then sections.
`check` enforces the traceability rules in feedback/README.md; it never edits an entry.
Standard library only.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FB = ROOT / "feedback"
ENTRIES = FB / "entries"
KINDS = ("wrong", "unclear", "missing", "works", "idea")
SEVERITIES = ("blocker", "major", "minor", "nit")
STATUSES = ("open", "accepted", "rejected", "fixed", "wont-fix")
DECIDED = ("accepted", "rejected", "fixed", "wont-fix")
PLACEHOLDER = "(JP's words go here"
SECTIONS = ("What was done", "What JP said, verbatim", "What the tutorial or agent had claimed", "Decision", "Change")


def parse(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return None, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith("#"):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    return meta, m.group(2)


def section(body: str, name: str) -> str:
    m = re.search(rf"^## {re.escape(name)}\s*\n(.*?)(?=^## |\Z)", body, re.S | re.M)
    return m.group(1).strip() if m else ""


def git_has_commit(h: str) -> bool:
    r = subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", f"{h}^{{commit}}"], capture_output=True)
    return r.returncode == 0


def validate(entries_dir: Path = ENTRIES, check_git: bool = True) -> list[str]:
    problems, seen = [], set()
    for p in sorted(entries_dir.glob("FB-*.md")):
        meta, body = parse(p)
        where = p.name
        if meta is None:
            problems.append(f"{where}: no front matter")
            continue
        if meta.get("id") != p.stem:
            problems.append(f"{where}: id '{meta.get('id')}' does not match the file name")
        if meta.get("id") in seen:
            problems.append(f"{where}: duplicate id")
        seen.add(meta.get("id"))
        for key, allowed in (("kind", KINDS), ("severity", SEVERITIES), ("status", STATUSES)):
            if meta.get(key) not in allowed:
                problems.append(f"{where}: {key} must be one of {allowed}, got '{meta.get(key)}'")
        for key in ("date", "lab", "reporter"):
            if not meta.get(key):
                problems.append(f"{where}: {key} is empty")
        for s in SECTIONS:
            if not section(body, s):
                problems.append(f"{where}: section '{s}' is missing or empty")
        said = section(body, "What JP said, verbatim")
        if PLACEHOLDER in said:
            problems.append(f"{where}: the verbatim section still holds the template placeholder")
        status = meta.get("status")
        if status in DECIDED and not meta.get("decided_by"):
            problems.append(f"{where}: status {status} needs decided_by (a human; the agent leaves it blank)")
        if status == "fixed":
            commit = meta.get("tutorial_commit", "")
            files = [f for f in meta.get("tutorial_files", "").split(",") if f.strip()]
            if not commit:
                problems.append(f"{where}: fixed needs tutorial_commit")
            elif check_git and not git_has_commit(commit):
                problems.append(f"{where}: tutorial_commit {commit} is not a commit in this repository")
            if not files:
                problems.append(f"{where}: fixed needs tutorial_files")
            for f in files:
                if not (ROOT / f.strip()).exists():
                    problems.append(f"{where}: tutorial file '{f.strip()}' does not exist")
        if status not in ("fixed",) and meta.get("tutorial_commit"):
            problems.append(f"{where}: tutorial_commit is set but status is {status}")
    return problems


def index_text(entries_dir: Path = ENTRIES) -> str:
    rows = []
    for p in sorted(entries_dir.glob("FB-*.md")):
        meta, body = parse(p)
        if not meta:
            continue
        said = " ".join(section(body, "What JP said, verbatim").split())
        said = (said[:90] + "...") if len(said) > 90 else said
        rows.append(f"| [{meta['id']}](entries/{p.name}) | {meta.get('date','')} | {meta.get('lab','')} §{meta.get('section','')} | "
                    f"{meta.get('kind','')} | {meta.get('severity','')} | {meta.get('status','')} | {said} | "
                    f"{meta.get('tutorial_commit','') or '—'} |")
    head = ("# Ledger\n\n## Executive summary\n\nThe index of everything JP (and other expert reviewers) told the course, one row per "
            "entry, with its status and the tutorial change that answered it. Generated by `python3 scripts/feedback.py index`; "
            "do not edit by hand. "
            + ("**No entries yet.** Nobody who works in this trade has run these labs; until an entry exists below, every claim in the "
               "tutorials is the author's, not an expert's.\n\n" if not rows else f"{len(rows)} entr{'y' if len(rows)==1 else 'ies'}.\n\n")
            + "| Entry | Date | Where | Kind | Severity | Status | JP said (start) | Fixed in |\n|---|---|---|---|---|---|---|---|\n")
    return head + ("\n".join(rows) + "\n" if rows else "")


def next_id(entries_dir: Path = ENTRIES) -> str:
    nums = [int(m.group(1)) for p in entries_dir.glob("FB-*.md") if (m := re.match(r"FB-(\d+)$", p.stem))]
    return f"FB-{(max(nums) + 1 if nums else 1):04d}"


def cmd_new(a):
    fid = next_id()
    from datetime import date
    text = (FB / "TEMPLATE.md").read_text(encoding="utf-8")
    text = (text.replace("id: FB-0000", f"id: {fid}").replace("date: YYYY-MM-DD", f"date: {a.date or date.today().isoformat()}")
            .replace("lab: lab-00", f"lab: {a.lab}").replace("section: 0", f"section: {a.section}")
            .replace("reporter: JP", f"reporter: {a.reporter}").replace("kind: wrong", f"kind: {a.kind}")
            .replace("severity: major", f"severity: {a.severity}"))
    out = ENTRIES / f"{fid}.md"
    out.write_text(text, encoding="utf-8")
    print(out)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new")
    n.add_argument("--lab", required=True)
    n.add_argument("--section", default="0")
    n.add_argument("--reporter", default="JP")
    n.add_argument("--kind", choices=KINDS, default="wrong")
    n.add_argument("--severity", choices=SEVERITIES, default="major")
    n.add_argument("--date")
    sub.add_parser("check")
    sub.add_parser("index")
    a = ap.parse_args(argv)
    if a.cmd == "new":
        return cmd_new(a)
    if a.cmd == "check":
        probs = validate()
        for p in probs:
            print("PROBLEM", p)
        n_entries = len(list(ENTRIES.glob("FB-*.md")))
        print(f"{n_entries} entr{'y' if n_entries == 1 else 'ies'} checked; {len(probs)} problem(s)")
        stale = (FB / "LEDGER.md").read_text(encoding="utf-8") != index_text() if (FB / "LEDGER.md").exists() else True
        if stale:
            print("PROBLEM LEDGER.md is stale; run: python3 scripts/feedback.py index")
        return 1 if probs or stale else 0
    (FB / "LEDGER.md").write_text(index_text(), encoding="utf-8")
    print(FB / "LEDGER.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
