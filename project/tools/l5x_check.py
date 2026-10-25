"""Read-only cross-check of a Studio 5000 L5X export against the I/O list.

Never writes to a PLC and never edits the L5X. Finds: I/O points the logic never
mentions, tags the logic uses that are not defined anywhere, and outputs driven by
more than one OTE (the classic double-coil bug).
"""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter

import design

INSTR = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\(([^()]*)\)")
IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*")


def read_l5x(path):
    root = ET.parse(path).getroot()
    defined = {t.get("Name") for t in root.iter("Tag")}
    rungs = []
    for r in root.iter("Rung"):
        txt = r.findtext("Text") or ""
        rungs.append(txt.strip())
    return defined, rungs


def analyse(defined, rungs, io_tags):
    used, coils = set(), Counter()
    for text in rungs:
        for op, args in INSTR.findall(text):
            for a in args.split(","):
                m = IDENT.match(a.strip())
                if m:
                    used.add(m.group(0))
                    if op in ("OTE",):
                        coils[m.group(0)] += 1
    findings = []
    for t in sorted(set(io_tags) - used):
        findings.append(f"IO-NOT-USED     {t}: in the I/O list, never referenced in the logic")
    for t in sorted(used - defined - set(io_tags)):
        findings.append(f"UNDEFINED-TAG   {t}: used in logic, not defined in the file or the I/O list")
    for t, n in sorted(coils.items()):
        if n > 1:
            findings.append(f"DOUBLE-COIL     {t}: driven by {n} OTE instructions")
    return findings


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    variant = design.load_toml(argv[0])
    defined, rungs = read_l5x(argv[1])
    io_tags = [r["tag"] for r in design.build_io(variant)]
    res = analyse(defined, rungs, io_tags)
    print("\n".join(res) if res else "No findings.")
    return 1 if res else 0


if __name__ == "__main__":
    sys.exit(main())
