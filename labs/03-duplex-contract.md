## Executive summary

Trace a duplex station from an explicit specification to compiled behavior. Run a complete cycle, pump fallback, invalid floats and restart. Then exhaustively check 1024 fresh input images and targeted stateful sequences. This is evidence for a synthetic contract, not validation of a field station. Time: 2–3 hours. Prerequisites: Labs 01–02 and the original Module 01 narrative exercise.

## Read the contract first

Read [SPEC.md](SPEC.md), sections R1–R7. Copy the exact R2 sentence into your review notes before saying the controller "must" stop for inconsistent floats. That requirement belongs to this teaching contract. An actual owner's specification may make a different tradeoff.

Read `labs/plc/station.st` in this order: alarm assignments; available-pump calculation; demand latch; alternation; timer; output assignments. Notice that every scan first writes both outputs FALSE and then conditionally sets them. This gives the code one clear place to decide each command. It does not prove a physical contactor stopped.

## Predict a cycle

Use the eight scans in [cycle.json](scenarios/cycle.json). Before revealing expected fields, predict the two pump outputs, lead selection and three alarms. At only the off float, a running cycle stays running. At no floats, it ends and changes lead. When pump 2 trips on the next cycle, pump 1 takes over in that scan. When both trip, demand remains but no pump can run.

```sh
python3 scripts/lab.py replay labs/scenarios/cycle.json --output build/reference/cycle.csv
cat build/reference/cycle.csv
python3 scripts/lab.py station
```

Expected replay: eight scans. The station test ends with `PASS station: cycle, alternation, fallback, faults, restart, 5s boundary, chatter, 1024 input images`.

## What the 1024 cases do and do not mean

Ten Boolean inputs give 2^10 = 1024 possible input images. Each enumeration resets the instance and checks independent properties: an unavailable pump never receives a run command, contradictory floats inhibit commands, and high alarm equals the high input. These are not all possible histories. Timing, latching, alternation and fault recovery require the separate multi-scan tests.

A test that recomputes the entire control algorithm using identical code can reproduce the same mistake. Prefer a small invariant such as "p1_run implies p1_auto and no p1 fault", together with hand-worked sequences. Even independent-looking tests can share a bad specification.

## Deliberate investigations

1. Add a replay copy where the lead pump trips after both pumps run, then recovers. Explain whether lag stays latched. Reference R4 and R5 exactly.
2. Add a case where floats are contradictory during an active cycle, then become consistent. Predict lead selection. R3 excludes invalid shutdown from alternation.
3. Reset at high level. R7 permits a first-scan start; the timer begins again. Explain why this is a classroom policy requiring human review for a real installation.
4. Add a case where no pump is available before the lag timer completes, then availability returns. The test suite already checks timer reset; explain the expected 5000 ms interval from the return scan.

Ask the agent to write scenario copies in `scratch/`, not change the contract to fit outputs. If it finds ambiguity, record `CANNOT-DETERMINE` and ask the human to decide before implementing behavior.

## Agent prompt

> Read AGENTS.md and labs/SPEC.md. Review labs/plc/station.st against R2–R7. For each claim, quote the specification sentence and name its section, identify the code location, and give a concrete test input sequence. Run scripts/lab.py station against the existing compiled build. Report expected versus actual outputs and the build receipt. Do not sign gates, access devices, or call a Python model a PLC runtime.

## Assessment

Submit a traceability row for every requirement, three added sequences, and one missing field requirement. Explain why input exhaustion is not exhaustive verification of a stateful controller. Stop for the +1's review of the contract and limitations; passing software tests does not sign G2 or G4.
