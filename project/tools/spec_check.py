"""Quote-or-it-didn't-happen: verify that every requirement in a checklist really is in the spec.

Checklist CSV columns: id,requirement,section,quote. A row passes only if the quote
appears verbatim (whitespace- and case-insensitive) in the spec text, and, when a
section number is given, after a heading line containing that number.
"""
from __future__ import annotations

import csv
import re
import sys


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def mark_headings(text: str) -> str:
    """Turn lines like '2.3 PUMP CONTROLS' into a ' §2.3§ ' marker; only line-start numbers count."""
    lines = []
    for ln in text.splitlines():
        m = re.match(r"^\s*(\d+(?:\.\d+)+)\s+\S", ln)
        lines.append((f" \u00a7{m.group(1)}\u00a7 " if m else "") + ln)
    return "\n".join(lines)


def check(spec_text: str, rows: list[dict]) -> list[str]:
    flat = norm(mark_headings(spec_text))
    out = []
    for r in rows:
        q = norm(r.get("quote", ""))
        if not q:
            out.append(f"NO-QUOTE      {r['id']}: '{r['requirement']}' cites nothing")
            continue
        if q not in flat:
            out.append(f"NOT-IN-SPEC   {r['id']}: quote not found: '{r['quote']}'")
            continue
        sec = r.get("section", "").strip()
        if sec:
            idx = flat.index(q)
            headings = list(re.finditer("\u00a7(\\d+(?:\\.\\d+)+)\u00a7", flat[: idx + 1]))
            last = headings[-1].group(1) if headings else ""
            if last != sec:
                out.append(f"WRONG-SECTION {r['id']}: cited {sec}, quote sits under {last or 'no section'}")
    return out


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    spec = open(argv[0], encoding="utf-8").read()
    rows = list(csv.DictReader(open(argv[1], encoding="utf-8")))
    res = check(spec, rows)
    print("\n".join(res) if res else f"All {len(rows)} rows verified against the spec text.")
    return 1 if res else 0


if __name__ == "__main__":
    sys.exit(main())
