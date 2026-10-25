## Executive summary

This is a **synthetic classroom specification**, version 1.0, for the new compiled labs. It makes the expected behavior precise enough to test. It is not a customer specification, an electrical code requirement, or a recommended field safety strategy. In particular, inhibiting pumps on inconsistent floats can cause overflow. A qualified human must decide real failure behavior. Nothing here signs G2 or G4.

## R1 — Input image and time

> "Each scan shall read one complete Boolean input image, compute the control logic once, and expose one output image. A TRUE float means liquid is at or above its threshold. Tests shall provide monotonic integer milliseconds; a reset starts a new simulated run."

The normal scan is 100 ms. Time is simulated, so 180 seconds of station behavior can execute much faster than 180 seconds. No claim of real-time scheduling is made. Sparse timestamp tests intentionally probe boundary semantics; they do not simulate every intervening input change.

Inputs in order: `fs1_off`, `fs2_lead`, `fs3_lag`, `fs4_high`, `p1_auto`, `p2_auto`, `p1_seal_fail`, `p2_seal_fail`, `p1_overtemp`, `p2_overtemp`. There is no Hand mode, motor contactor feedback, network input, analog sensor or physical I/O address.

## R2 — Availability and contradictory sensors

> "A pump is available only when its Auto input is TRUE and neither its seal-failure nor overtemperature input is TRUE. An upper float TRUE with the adjacent lower float FALSE shall raise invalid_alarm and inhibit both pump commands in that scan."

No debouncing is implied. The classroom inhibition policy is deliberately easy to inspect; it can make flooding worse. A contradictory sensor is not proof that the wet well is empty. The highest float still controls the high alarm.

## R3 — Demand and alternation

> "With consistent floats, the lead float shall set demand. Demand shall remain set while only the off float remains TRUE and shall clear when the off float is FALSE. On a valid demand-to-no-demand transition, the lead selection shall alternate once. Invalid sensors shall clear demand without alternating the lead."

A *latch* is state that stays set after its initiating input drops. A *scan* is one pass through the logic. A persistent function block instance stores the latch between scans. Recreating that instance every scan destroys the behavior we are trying to test.

## R4 — Selection and fallback

> "During demand the selected available lead pump shall run. If it is unavailable, the other available pump shall run immediately. Neither pump shall run while unavailable. If neither is available during demand, no_pump_alarm shall be TRUE."

Recovery of the selected lead restores the selected-lead rule immediately; this sample has no anti-short-cycle lockout, minimum run time or duty-hour balancing. Those are missing design decisions, not hidden features.

## R5 — Lag timing

> "With demand, the lag float TRUE, and at least one available pump, a TON shall measure elapsed time beginning at the first scan that observes those conditions. At 5000 ms elapsed, the second available pump shall join. The lag request shall then remain latched until demand clears. Before completion, a FALSE timer input shall reset elapsed time."

TON means on-delay timer. The scan that first sees the condition establishes time zero; it does not receive a whole scan's time credit. At t=4900 ms the lag pump is still off; at t=5000 ms it may join. After lag latches, a pump recovering from a fault may join immediately.

## R6 — Alarms

> "high_alarm shall equal fs4_high independently of pump availability. invalid_alarm shall indicate contradictory adjacent floats. no_pump_alarm shall indicate demand with neither pump available. Alarms shall clear when their conditions clear."

These are Boolean indications, not a complete alarm-management system. There is no acknowledgement, horn, history retention, priority or remote delivery. Motor trips are inputs; they are not separately exposed as alarm outputs in this sample.

## R7 — Cold restart

> "A cold reset shall clear latch and timer state, select pump 1 as lead, and then evaluate the new input image. If valid start conditions are present, a pump may run in that first scan."

This is a declared classroom choice. There is no retained memory, battery, warm restart or power-loss model. The assessment asks what must change if an owner requires manual restart approval.

## R8 — Toy plant

> "The plant shall update after each controller scan using integer millilitres. The next volume shall equal the current volume plus inflow minus actual outflow, clamped at zero and at 100000 mL. Volume above that ceiling shall be recorded as spill."

The four thresholds are 10000, 40000, 65000 and 85000 mL. These are invented teaching values, not derived from the unverified electrical tables. Each commanded working pump removes 300 mL per 100 ms scan. Inflow is 120 mL per scan except scans 600–1099 inclusive, when it is 450 mL. A selected fault is active at scans 400–899 inclusive. Initial volume is 20000 mL. No hydraulic head, inertia, switch hysteresis, pump curve, solids, pipe losses, electrical dynamics or sensor noise is modeled.

## Traceability

| Requirement | Reference implementation | Evidence |
|---|---|---|
| R1 | `labs/runtime/harness.c` line protocol | timestamps and CSV replay |
| R2 | `labs/plc/station.st` availability / invalid input | 1024 fresh input combinations + fault traces |
| R3–R4 | `labs/plc/station.st` demand / lead | cycle replay, fallback, alternation mutant |
| R5 | MatIEC TON called by `labs/plc/station.st` | before/at/after deadline, chatter, outage reset, instant-lag mutant |
| R6 | `labs/plc/station.st` alarm assignments | high/invalid/no-pump assertions |
| R7 | function block initialization in harness | cold-reset assertion |
| R8 | `scripts/lab.py` plant function | repeated identical CSVs, spill scenario |

The source is this file, sections R1–R8. Whenever a lab reports compliance, cite the section and its exact quoted sentence. Passing these tests is evidence about this contract and this sample only.
