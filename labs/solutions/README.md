## Executive summary

These are reference answers for the synthetic labs. Use them after predicting behavior and running the commands. They explain the supplied implementation and tests; they are not engineering approval, a field safety policy or a replacement for a human review.

## 01 — Scan and state

From a reset state, only start=1, stop_ok=1, motor_healthy=1 starts the motor. The stateful sequence produces `1,1,0,0,0`. Resetting every scan loses the seal-in state. Moving the start OR outside the stop/health AND group can allow a start to bypass a permission. A run output is a command, not proof of contact closure or flow.

## 02 — Timer and counter

The timing replay produces count=1 at the first rising edge; keeping the input TRUE does not keep incrementing it. TON's elapsed time begins at zero and reaches 500 ms at the t=500 scan. A FALSE input clears elapsed time. A new rising edge after FALSE increments the count. If the input drops at 400 ms and rises at 450 ms, done is first possible at 950 ms, assuming a scan samples that time with the input still TRUE. With 100 ms sampling offset from 450, that is also an actual sample.

## 03 — Station

The eight-scan replay pump pairs are `00,10,10,00,01,10,00,00`; lead becomes 2 on the drained scan. The last row has high and invalid alarms together; no-pump alarm is clear because invalid floats cleared demand. The 5 s lag test has pump 2 off at 4900 ms and on at 5000 ms. Interrupted one-second lag-float pulses never accumulate to five seconds. Cold reset starts a new cycle with lead 1 and may command it immediately if inputs request it.

A healthy-pump invariant does not prove eventual drainage. The plant might have more inflow than both pumps can remove, or a command may not produce outflow. A finite set of input histories does not prove all possible histories.

## 04 — Plant reference results

Normal reference run: 1800 scans; maximum volume 72500 mL; spill 0; pump 1 on for 648 scans and pump 2 for 563. Both-trip run: maximum 100000 mL; spill 84400 mL; high alarm on for 355 scans; no-pump alarm on for 315 scans. These are actual observed toy-simulation results, not equipment capacities or electrical design values. Fault timing and plant arithmetic are defined in SPEC R8.

A blocked pump cannot be directly identified from the existing inputs. The controller may eventually call for lag as volume rises, but that is response to level, not diagnosis of a failed pump. A feedback requirement would need a sensor, startup allowance, timeout, reset policy and consequences approved by the human.

## 05 — Mutations and repair

`ignore-health` violates R2 availability; `instant-lag` violates R5 elapsed time; `no-alternation` violates R3. The learner repair restores the copied delay from T#0s to T#5s and reruns the unchanged tests. A syntax failure is a different failure class and does not prove those behavioral tests work.

## 06 — Two oracles

There are 37 legacy vector rows. Pump commands differ twice: T02 t=5 and T07 t=5. Python predicts both pumps; compiled ST predicts lead only. The first TRUE scan is at t=1; actual TON needs until t=6 for five elapsed seconds. The Python model credited time at the first observation. Alarm comparison is incomplete because the interfaces differ. Invalid-input behavior in the new Station contract also intentionally differs from the old block.

## 07–08 — Review and capstone

A credible packet includes quoted requirements, hashes, actual commands, outputs, fault counterexamples and unresolved decisions. It labels the reference tables unverified, the plant synthetic, and DraftSight/OpenPLC/Studio 5000/hardware NOT VERIFIED. It does not sign a gate or substitute a classroom rubric score for engineering approval.

The supplied `labs/plc/station.st` is the reference implementation for the assigned contract. The capstone does not require a different algorithm; it requires independently explaining and challenging this one with new evidence. The feedback-timeout extension is not supplied or verified.
