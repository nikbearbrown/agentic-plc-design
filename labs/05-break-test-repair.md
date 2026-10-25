## Executive summary

Prove the tests can reject wrong compiled logic. Build three deliberate faults on disposable copies, inspect counterexamples, then repair one learner copy and rerun the unchanged tests. This is the agent's generate–inspect–test–repair loop with concrete evidence. Time: 2–3 hours. Prerequisite: Lab 03.

## Why deliberately break a correct program?

A *mutation* is a small planted code defect. If the tests still pass, either the defect is harmless under the contract or the suite is missing a case. A test suite that never rejects anything is weak evidence.

Three mutations are supplied: ignore pump 1 health, set lag delay to zero, and keep pump 1 as lead every cycle. They are made only in `build/reference/mutants/<mutation>/combined.st`. Source files remain unchanged.

## Predict and execute

For each mutation, write the smallest distinguishing input sequence and the violated quoted contract sentence. Then:

```sh
python3 scripts/lab.py mutations
python3 scripts/lab.py mutations --apply
```

The first command reports a dry run. The second compiles each faulty ST copy and runs the real native tests. Expected: three `KILLED` lines followed by `PASS mutations: all 3 compiled faults rejected`. In this vocabulary "killed" means a test caught the fault. A compiler error is not counted as a successful mutation test; compilation must succeed first.

Read each mutant's `compile.log`, `build.json` and `combined.st`. An assertion without a useful input is only the start of debugging. Reproduce the smallest failed sequence in a JSON replay and explain the mismatch.

## Repair a learner copy

Ask the agent to create `scratch/station-repair.st` as a copy of `labs/plc/station.st` and change only the copied `PT := T#5s` to `PT := T#0s`. Before applying, it must show the intended diff and confirm the target is the scratch copy. Then run:

```sh
python3 scripts/lab.py build --source scratch/station-repair.st --build-dir build/repair --apply
python3 scripts/lab.py station --build-dir build/repair
```

The second command should fail with `lag too early`. Save that failure. Ask the agent to propose the smallest correction with the R5 quote, show the diff, apply to the scratch copy, rebuild and rerun the same command. The expected repaired result is the station PASS line. Do not change expected outputs to obtain a pass. Run `./check.sh` after the repair.

## A useful agent work order

> Work only on scratch/station-repair.st. First reproduce the failing native test and record compiler/source hashes. Quote the requirement it violates. Propose the smallest patch and explain why it changes the observed failure. Apply only to the copy after the diff has been reviewed. Recompile and run the unchanged station tests. Report the original failure, repair diff, passing result, and what remains untested. Stop at the module boundary. Do not edit STATUS.md or any reference table.

## Assessment

Provide the before/after trace and a one-paragraph root cause. Distinguish fixing syntax, behavior and the test's own mistake. Name a defect that the current suite could miss (for example a long-running counter overflow or a feedback failure the contract never specified). No number of caught mutations proves complete coverage. Stop for review.
