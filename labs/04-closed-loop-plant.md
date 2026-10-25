## Executive summary

Connect the compiled controller to an observable, deterministic toy wet well. Watch simulated water rise and fall, inject faults, and separate a command from actual simulated outflow. The controller is compiled ST; the plant physics is a simple Python teaching simulation. Time: 2–3 hours. Prerequisite: Lab 03.

## Understand the loop

One scan samples floats from the current volume, sends those bits to the native controller, reads its outputs, then updates the plant volume. That order matters: the CSV row's volume is **before** the output takes effect. The next row reflects the result. The equations and invented quantities are in SPEC R8; none comes from the unverified NEC or catalog tables.

```text
current volume -> float image -> compiled ST -> pump commands
      ^                                           |
      +--- next volume <- toy inflow/outflow <-----+
```

An *open-loop* replay supplies predetermined inputs. A *closed-loop* simulation lets the controller's outputs influence the next inputs. Passing replay tests does not establish that a plant drains; passing this toy simulation does not establish real pump capacity.

## Run and observe

```sh
python3 scripts/lab.py plant --output build/reference/plant.csv
python3 scripts/view_trace.py build/reference/plant.csv --output build/reference/plant.html
```

The first command writes 1800 rows (180 simulated seconds), prints counts and spill, and writes a JSON summary. The second creates an offline HTML viewer. Ask the agent to open the generated file and inspect it with you. The viewer is a replay of recorded native-controller outputs; it cannot change I/O or connect to equipment. It uses no external scripts, server, CDN or account.

Read the first demand onset, first drained cycle, lead change and lag join. Use the time slider to compare volume, actual sensed input image, pump commands and alarms. `physical_level_index` describes the unfaulted threshold state; `fs1_off` through `fs4_high` and the pump-permission/trip columns record the exact input bits sent to compiled ST after fault injection. Predict which threshold is crossed next. Inspect the raw CSV whenever the picture is uncertain.

## Faults are experiments on the toy plant only

```sh
python3 scripts/lab.py plant --fault pump1-trip --output build/reference/pump1-trip.csv
python3 scripts/lab.py plant --fault both-trip --output build/reference/both-trip.csv
python3 scripts/lab.py plant --fault bad-float --output build/reference/bad-float.csv
python3 scripts/lab.py plant --fault blocked-pump1 --output build/reference/blocked-pump1.csv
```

Fault window: 40.0 through 89.9 seconds. Inflow surge: 60.0 through 109.9 seconds. Compare each JSON summary with normal operation. The both-trip scenario should produce spill, high-level indication and no-pump indication. This is an expected **plant failure**, not a passing safety design. The test passes because it observes and reports the specified failure.

The blocked-pump fault removes pump 1's actual outflow without changing its command or trip inputs. This controller has no run/flow feedback, so it cannot directly diagnose that fault. Compare command time and pumped volume. An agent claiming "the motor is running" from `p1_run=1` has overstated the evidence.

## Repeatability

```sh
python3 scripts/lab.py plant --output build/reference/plant-repeat.csv
cmp build/reference/plant.csv build/reference/plant-repeat.csv
```

Expected: no `cmp` output, exit 0. The model uses integer millilitres and a fixed clock, with no randomness. Repeatability helps regression testing. It does not improve the model's hydraulic fidelity.

## Assessment

Submit one normal trace and two fault traces. Mark the first alarm and first spill in each. Explain whether the initiating problem was detected, merely inferred, or invisible. Propose a feedback requirement with a timeout, but label it a proposal until the human decides. Do not turn the suggested timeout into a real design value. Stop for review.
