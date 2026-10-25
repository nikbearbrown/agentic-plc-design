# STATUS

## Executive summary

This file records which review gates for the course have been signed, and by whom. **None are signed yet.** The course was drafted and built by an AI agent on 2026-10-25; the tools and tests were run, but no domain expert has reviewed the control logic, the reference tables, the AutoLISP or the lesson content. Until a gate below carries a human's initials and date, treat that part as a draft.

Only a human signs a gate. An agent that writes initials here has broken the rules in `AGENTS.md`.

## Gates

| Gate | What the +1 attests | Signed by | Date |
|---|---|---|---|
| G1 Reference tables | I checked every number in `project/data/nec-extracts.toml` against the adopted NEC edition and set `verified = true` | _unsigned_ | |
| G2 Control narrative and reference model | `modules/01` narrative and `project/tools/sim.py` describe correct duplex lead/lag behavior for my kind of station | _unsigned_ | |
| G3 AutoLISP | I ran `apd-lib.lsp` on a copy of a drawing in DraftSight; dry run and apply both behaved as described | _unsigned_ | |
| G4 Structured Text | `plc/lead_lag.st` compiled in OpenPLC or Studio 5000 and matched the test vectors, or I recorded where it did not | _unsigned_ | |
| G5 Lesson accuracy | I read each module and corrected anything a working panel builder would call wrong | _unsigned_ | |
| G6 Release | I authorize sharing this course beyond myself | _unsigned_ | |

## Initial draft build record (2026-10-25, before executable expansion)

- Tests: 31 pass; the flawed controller fails 3 of 12 as designed (`./check.sh`).
- Generated AutoLISP passes `lisp_lint.py`. Not run in DraftSight.
- Structured Text: written, not compiled.
- Synthetic L5X: hand-written, never opened in Studio 5000.
- Nothing pushed to GitHub. No publishing done.

## Executable expansion record (2026-10-25; no gate signatures)

The original Structured Text was subsequently compiled unchanged by MatIEC and executed through a local course C scan harness. Two pump-output timing differences from the old Python model were observed in 37 vector rows; no vendor-runtime equivalence is claimed. New starter, timer/counter/edge and duplex examples, deterministic toy-plant tests and compiled mutation tests are documented in [labs/VERIFICATION.md](labs/VERIFICATION.md).

All gates above remain **unsigned**. No OpenPLC, Beremiz runtime/IDE, DraftSight, Studio 5000 or real hardware was run. The original build record is preserved as history, not as the current compilation status. This expansion is local and has not been pushed or deployed by this task.
