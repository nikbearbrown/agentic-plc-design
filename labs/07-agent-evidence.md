## Executive summary

Turn an agent's plausible answer into a reviewable engineering work product. Separate specification, implementation, tests and human decisions; preserve failures as evidence. This lab uses the working compiler and local tests, with no required AI API, paid subscription or new account. Time: 2 hours. Prerequisites: Labs 03, 05 and 06.

## The workflow

A useful agent work order names the source, permitted change, expected evidence and stopping point. The agent can draft a specification from synthetic notes, generate a program, compile copies, inspect diagnostics, run tests and propose repairs. It cannot decide actual safety behavior, verify code-table values from memory, certify a controller or sign a gate.

| Stage | Agent artifact | Human question |
|---|---|---|
| Specify | Requirement ID + verbatim quote + section | Is this what the owner asked for? |
| Generate | Copy-only ST diff linked to requirement | Did it add hidden behavior? |
| Inspect | Data/state/timing review | Are inputs and state interpreted correctly? |
| Test | Commands, source hash, expected/actual trace | Did the intended binary actually run? |
| Repair | Minimal diff and repeated unchanged test | Did the patch fix the cause? |
| Review | Coverage gaps and unsigned decision list | What still needs qualified judgment? |

## Make an evidence packet

Ask the agent to create a new `scratch/review-packet/` directory and copy the build receipt, cycle trace, timer trace, original comparison and chosen plant fault trace there. Ask it to write `review.md` opening with an Executive summary. The note must include exact command lines, actual exits/results, requirement quotes, file hashes and limitations. It must label the Python plant as a pedagogical simulation and the control logic as MatIEC-compiled ST in a course C harness.

Run these commands rather than trusting a prior chat claim:

```sh
python3 scripts/lab.py build --apply
python3 scripts/lab.py test
python3 scripts/lab.py mutations --apply
./check.sh
```

The generated build receipt is useful because a stale executable can pass while an edited source was never compiled. A log without a source identity cannot settle that question. Rebuilding under a different compiler may legitimately produce a different binary hash.

## Challenge an agent's unsupported claims

Give the agent this synthetic review and ask it to mark each claim supported, contradicted, or CANNOT-DETERMINE:

> "The motor ran for ten seconds, so the pump moved the required flow. The AI's Python simulator proves the PLC is safe. All 1024 combinations passed, so all possible histories were covered. The NEC table is correct because the checker used it. OpenPLC was tested because the ST compiled."

Every sentence overstates the available evidence. A command is not feedback, a toy plant is not hydraulic validation, input combinations are not histories, unverified table arithmetic remains unverified, and MatIEC compilation is not OpenPLC runtime execution.

## Independent learner handoff

Give a fresh agent only this repository path, AGENTS.md, README and labs/README. Ask it to follow the documented steps, record every missing prerequisite or unexpected output, and avoid private author knowledge. It should first attempt each prediction, then inspect solutions. It may use cached official tool archives, but must say so. Run in a separate build directory or a temporary local clone when another agent is working.

A learner agent is a useful second reader, not a human instructor or panel-builder signatory. Its findings belong in `labs/LEARNER-REPORT.md`. Human gates stay unsigned even if it reports a clean run.

## Assessment

Submit the evidence packet and the unsupported-claim critique. Include two sentences on what the agent produced and what still needs human judgment. Read [the BearBrown inventory](../reference/bearbrown-plc-inventory.md) and explain why a workflow that manipulates TIA Portal is not automatically an open-source macOS PLC stack. Stop for review.
