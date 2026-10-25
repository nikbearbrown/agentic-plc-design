## Executive summary

Compile the original course's `DuplexLeadLag` block and compare its pump commands with the existing Python model. Observe the real disagreement at the five-second boundary instead of silently rewriting either side. This is a debugging lab about the limits of an oracle. Time: 90 minutes. Prerequisites: Labs 02–03 and original Module 05.

## Preserve the original evidence

The normal build includes the original `project/plc/lead_lag.st` unchanged in a generated copy. It also includes the new `Station` block. They implement different classroom policies, especially on inconsistent floats. Do not confuse their outputs or substitute one for the other.

```sh
python3 scripts/lab.py compare --output build/reference/original-comparison.csv
cat build/reference/original-comparison.csv
```

Expected: 37 vector rows and two pump-command disagreements, in scenarios T02 and T07 at t=5 seconds. The command reports the exact observed count; if it changes, investigate before updating these instructions. The comparison explicitly compares the two pump commands only. Python exposes individual seal and temperature alarms; the original ST exposes only three aggregate alarm outputs. Full alarm equivalence is **NOT VERIFIED** and is not claimed.

## Trace the disagreement

The legacy Python model adds one second on the first TRUE scan. The compiled TON records its start time at that scan. With first input at t=1, the Python model reaches five seconds at t=5; the timer reaches five elapsed seconds at t=6. Both implementations can look reasonable if the narrative never defines the sampling convention.

The new contract R5 defines the convention explicitly. It does not retroactively approve changes to the legacy model. Preserve the mismatch CSV as evidence and ask the human which convention belongs in their own narrative.

## An oracle is a witness, not an authority

An *oracle* is the source of expected results in a test. A Python model can have bugs. A compiler can have bugs. A written requirement can be incomplete. Agreement between implementations is useful, but it does not resolve a shared misunderstanding.

Build a four-column review: exact requirement quote and section; expected event time; each observed event time; human decision needed. If the old narrative does not specify the timing convention, write `CANNOT-DETERMINE` rather than invent a quote.

## Assessment

Explain the discrepancy using timestamps, not the phrase "off by one" alone. Identify two other non-equivalences: alarm coverage and inconsistent-float policy. Write a proposed model correction on paper, with the tests it would change. Do not change the original program, model or G4 signature as part of this lab. Stop for review.
