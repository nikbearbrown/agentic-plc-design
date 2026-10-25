## Executive summary

Use a start/stop circuit to understand scan images and memory. You will execute eight input combinations, then observe a latch across scans. The result is actual MatIEC-compiled ST; there is no relay hardware. Time: 60–90 minutes after [setup](00-setup.md).

## The idea, with a familiar circuit

A maintained command can be expressed as:

```text
motor_run := (motor_run OR start_button) AND stop_ok AND motor_healthy;
```

`:=` assigns the value on the right to the variable on the left. `motor_run` on the right is the previous value because this assignment has not happened yet. `AND` requires both conditions; `OR` requires at least one. The function block stores its output across calls. This is a software seal-in circuit, not a safety-rated stop circuit.

Read `labs/plc/foundations.st`, function block `Starter`. There are no physical addresses. `stop_ok=TRUE` means the simulation's stop permission is present, not that a normally closed field circuit has been inspected.

## Predict before executing

Write eight rows for all combinations of start, stop permission and motor health. Assume the instance starts off each row. Only `(1,1,1)` should start. Now predict a stateful sequence: start; release start; press start while stop permission is absent; restore stop permission without start; start while unhealthy. Explain why a truth table alone cannot verify the latch.

## Execute and inspect

```sh
python3 scripts/lab.py foundations
```

The test resets the function block for each truth-table row, then preserves it for the stateful sequence. Expected motor outputs are `1,1,0,0,0`. To observe the native protocol directly:

```sh
printf '0 1 1 1 1 0 0 0 0 0 0 0\n100 0 0 1 1 0 0 0 0 0 0 0\n200 0 1 0 1 0 0 0 0 0 0 0\n' | build/reference/plc-sim starter
```

Expected lines: `1`, `1`, `0`. Each line contains milliseconds, reset flag and ten Boolean input slots. Starter uses only the first three slots: start, stop permission, health. Zero-fill the unused slots. A reset initializes state **before** that scan evaluates inputs; it does not force outputs to zero afterward.

The harness rejects a non-increasing timestamp within a run or a non-Boolean input. A reset permits a new time origin. That is a test-driver guard, not a controller safety function.

## Debugging exercise

Ask the agent: "If the function block were initialized every scan, which output in the sequence would first differ? Explain from stored state before changing anything." Answer: releasing start at the second scan would stop the motor. Ask for a second counterexample: an expression where `OR start_button` is outside the stop permission parentheses can defeat stop precedence.

Make a learner copy before experimenting. Do not edit the reference program or weaken the expected values. In this lab a written counterexample is sufficient; executable repair follows in Lab 05.

## Assessment and handoff

Explain the difference between resetting a test fixture and scanning it. Show evidence for simultaneous start/stop precedence and release-of-start latching. Identify one real motor-starter issue this logic cannot represent (for example welded contact feedback). State "CANNOT-DETERMINE" for actual equipment behavior. Save a two-sentence AI Use Disclosure and stop for review.
