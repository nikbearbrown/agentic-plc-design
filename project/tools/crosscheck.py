"""Compare the devices a variant implies against a tag list extracted from a drawing.

The drawing side is a CSV with columns tag,description (what an attribute/data
extraction of the drawing set gives you; Module 3 shows how to produce it).
Reports: on the design but not the drawing, on the drawing but not the design,
and same tag with different numbers in the description (ratings).
"""
from __future__ import annotations

import csv
import re
import sys

import design


def numbers(s: str) -> list[str]:
    s = re.sub(r"(?i)\bpump\s*\d\b", "pump", s)
    return re.findall(r"\d+(?:\.\d+)?", s)


def crosscheck(variant: dict, extract_rows: list[dict]) -> list[str]:
    devs = {d.tag: d for d in design.build_devices(variant)}
    drw = {r["tag"].strip(): r["description"].strip() for r in extract_rows}
    out = []
    for t in sorted(set(devs) - set(drw)):
        out.append(f"MISSING-ON-DRAWING  {t}: {devs[t].description}")
    for t in sorted(set(drw) - set(devs)):
        out.append(f"NOT-IN-DESIGN       {t}: {drw[t]}")
    for t in sorted(set(devs) & set(drw)):
        if numbers(devs[t].description) != numbers(drw[t]):
            out.append(f"RATING-MISMATCH     {t}: design '{devs[t].description}' vs drawing '{drw[t]}'")
    return out


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    variant = design.load_toml(argv[0])
    rows = list(csv.DictReader(open(argv[1], encoding="utf-8")))
    res = crosscheck(variant, rows)
    print("\n".join(res) if res else "No discrepancies.")
    return 1 if res else 0


if __name__ == "__main__":
    sys.exit(main())
