## Executive summary

Run real IEC function blocks for a rising edge, event count and on-delay timer. Measure the boundary at 499 and 500 milliseconds. This lab prevents the common mistake of giving a timer a full scan of credit on its first TRUE sample. Time: 90 minutes. Prerequisite: [scan and state](01-scan-and-state.md).

## Three different questions

`R_TRIG` asks "did the Boolean signal just become TRUE?" Its Q output lasts one scan. `CTU` counts rising transitions; holding TRUE for ten scans is one event. `TON` asks "has this condition stayed TRUE for the preset elapsed duration?" Its IN input going FALSE clears Q and elapsed time. `PT` is preset time, `ET` elapsed time, and `Q` the done output.

The `Timing` block in `labs/plc/foundations.st` calls all three. It exposes edge, count, done and elapsed time. The standard block implementations come from the pinned MatIEC library, not Python substitutes.

## Predict

The first scan observes signal TRUE at t=0. Predict done at t=499, t=500 and t=600 if the last scan sets signal FALSE. Predict the counter after a second rising edge and after reset. Check the [scenario](scenarios/timer.json) only after writing your predictions.

## Run

```sh
python3 scripts/lab.py replay labs/scenarios/timer.json --output build/reference/timer.csv
cat build/reference/timer.csv
```

Expected CSV:

```csv
ms,edge,count,done,elapsed_ms
0,1,1,0,0
100,0,1,0,100
499,0,1,0,499
500,0,1,1,500
600,0,1,0,0
700,1,2,0,0
800,0,0,0,0
```

The harness supplies the clock; nothing sleeps. Sampling at 499 then 500 ms does not prove a 1 ms scan is achievable in production. It precisely tests library behavior at the selected timestamps.

## Challenge

On a copy of the scenario, move the t=500 scan to t=501 and retain the expected done value. Then invent a false input at t=400 followed by true at t=450. Predict the next done timestamp. Ask the agent to create the JSON copy under `scratch/`, read back the diff, and replay it with `--output build/reference/timer-challenge.csv`. This changes test input data, not the program. Keep the baseline scenario.

If the counter resets while its input remains TRUE, do not assume it counts another event next scan. The edge detector still remembers the high input. Include an intervening FALSE scan when you want a second edge.

## Assessment

Explain why six sampled TRUE values at 0,100,200,300,400,500 ms span 500 ms. Explain how a Python model that adds 100 ms on every TRUE scan would differ. Name the test you would add for a one-scan glitch, and show expected output before executing. Reference answers are in [solutions](solutions/README.md); use them after attempting the prediction. Stop for review.
