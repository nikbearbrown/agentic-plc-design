"""Export test vectors from the reference model as CSV, one row per scan.

Force the inputs column-by-column in OpenPLC / Studio 5000 emulator and compare the
exp_* columns with what your program does. The reference model is the oracle only
until a human corrects it.
"""
from __future__ import annotations

import csv
import sys

from sim import DuplexController, Inputs

LEVELS = {0: dict(), 1: dict(fs1_off=True), 2: dict(fs1_off=True, fs2_lead=True),
          3: dict(fs1_off=True, fs2_lead=True, fs3_lag=True),
          4: dict(fs1_off=True, fs2_lead=True, fs3_lag=True, fs4_high=True)}

# (name, [(level, seconds, extra_input_overrides)])
SCENARIOS = [
    ("T01 normal cycle, lead only", [(0, 2, {}), (2, 3, {}), (1, 2, {}), (0, 2, {})]),
    ("T02 lag joins after 5 s", [(3, 7, {}), (1, 2, {}), (0, 2, {})]),
    ("T03 alternation on second cycle", [(2, 1, {}), (0, 1, {}), (2, 1, {}), (0, 1, {})]),
    ("T04 pump 1 seal fail", [(2, 2, dict(p1_seal_fail=True))]),
    ("T05 pump 1 in Off", [(2, 2, dict(p1_auto=False))]),
    ("T06 both pumps faulted", [(2, 2, dict(p1_seal_fail=True, p2_overtemp=True))]),
    ("T07 high level", [(4, 6, {})]),
    ("T08 float fault (lead float up, off float down)", [(2, 1, dict(fs1_off=False))]),
]

COLS = ["scenario", "t_s", "fs1_off", "fs2_lead", "fs3_lag", "fs4_high", "p1_auto", "p2_auto",
        "p1_seal_fail", "p2_seal_fail", "p1_overtemp", "p2_overtemp", "exp_p1_run", "exp_p2_run", "exp_alarms"]


def generate():
    rows = []
    for name, steps in SCENARIOS:
        ctl, t = DuplexController(), 0
        for lvl, secs, extra in steps:
            for _ in range(secs):
                t += 1
                kw = {**LEVELS[lvl], **extra}
                inp = Inputs(**kw)
                out = ctl.scan(inp, 1.0)
                row = {"scenario": name, "t_s": t}
                for c in COLS[2:12]:
                    row[c] = int(getattr(inp, c))
                row.update(exp_p1_run=int(out.p1_run), exp_p2_run=int(out.p2_run),
                           exp_alarms=" ".join(sorted(out.alarms)))
                rows.append(row)
    return rows


def main(argv=None):
    w = csv.DictWriter(sys.stdout, fieldnames=COLS, lineterminator="\n")
    w.writeheader()
    w.writerows(generate())


if __name__ == "__main__":
    main()
