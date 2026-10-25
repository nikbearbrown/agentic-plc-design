"""Facts from a station event log, so the AI reasons from numbers instead of guessing.

Log CSV columns: timestamp (ISO 8601), tag, state (1/0). Reports per-pump starts,
total and longest run, short cycles, and alarm edges.
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from datetime import datetime

SHORT_CYCLE_S = 60


def parse(rows):
    ev = [(datetime.fromisoformat(r["timestamp"]), r["tag"], int(r["state"])) for r in rows]
    return sorted(ev, key=lambda e: e[0])


def summarise(events):
    runs = defaultdict(list)
    started = {}
    alarms = defaultdict(list)
    for t, tag, st in events:
        if tag.endswith("_RUN_FB"):
            if st == 1:
                started[tag] = t
            elif tag in started:
                runs[tag].append((started.pop(tag), t))
        elif tag.startswith(("ALM_", "P1_SEAL", "P2_SEAL", "P1_OVERTEMP", "P2_OVERTEMP")) and st == 1:
            alarms[tag].append(t)
    lines = []
    for tag in sorted(runs):
        durs = [(b - a).total_seconds() for a, b in runs[tag]]
        short = sum(d < SHORT_CYCLE_S for d in durs)
        lines.append(f"{tag}: {len(durs)} runs, {sum(durs)/60:.1f} min total, longest {max(durs)/60:.1f} min, "
                     f"{short} short cycles (< {SHORT_CYCLE_S} s)")
    for tag in sorted(alarms):
        lines.append(f"{tag}: raised {len(alarms[tag])}x, first {alarms[tag][0].isoformat(sep=' ')}")
    order = [tag for _, tag, st in events if tag.endswith("_RUN_FB") and st == 1]
    lines.append("start order: " + " ".join(t.split("_")[0] for t in order))
    return lines


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    rows = list(csv.DictReader(open(argv[0], encoding="utf-8")))
    print("\n".join(summarise(parse(rows))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
