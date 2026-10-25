"""Builds samples/station-log-synthetic.csv. SYNTHETIC: invented story, deterministic."""
import csv
from datetime import datetime, timedelta

t0 = datetime(2026, 3, 14, 0, 0, 0)
ev = []

def add(minutes, tag, state):
    ev.append(((t0 + timedelta(seconds=minutes * 60)).isoformat(), tag, state))

# 00:00-02:00 healthy: pumps alternate, one run every ~15 min, ~4.5 min each
m, p = 5.0, 1
while m < 120:
    add(m, f"P{p}_RUN_FB", 1)
    add(m + 4.5, f"P{p}_RUN_FB", 0)
    p = 2 if p == 1 else 1
    m += 15
# 02:00-02:12 pump 1 short cycles (float chatter)
m = 120.0
for _ in range(6):
    add(m, "P1_RUN_FB", 1); add(m + 0.4, "P1_RUN_FB", 0); m += 2.0
# 02:14 pump 2 seal fail; pump 2 never runs again
add(134.0, "P2_SEAL_FAIL", 1)
# 02:20 and 02:30 pump 1 runs normally
add(140.0, "P1_RUN_FB", 1); add(145.0, "P1_RUN_FB", 0)
add(150.0, "P1_RUN_FB", 1); add(155.0, "P1_RUN_FB", 0)
# 02:41 high level; pump 1 runs 45 minutes alone
add(161.0, "ALM_HIGH_LEVEL", 1)
add(161.5, "P1_RUN_FB", 1); add(206.5, "P1_RUN_FB", 0)
add(210.0, "ALM_HIGH_LEVEL", 0)
ev.sort()
with open("samples/station-log-synthetic.csv", "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["timestamp", "tag", "state"])
    w.writerows(ev)
print(len(ev), "events")
