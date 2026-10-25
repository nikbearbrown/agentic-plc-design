## Executive summary

This is the executable open-source spine of Agentic PLC Design: nine guided labs, real Structured Text compilation, native scan execution, deterministic plant traces, deliberately faulty programs, repairs, assessments and a capstone. It extends the original thirteen modules without replacing their design-document and human-review work. All equipment is simulated. The selected stack needs no paid service, account or secret.

## Start and pace

Begin with [00 Setup](00-setup.md), then work down the table. Read the [synthetic specification](SPEC.md) before interpreting station behavior. The agent can execute the commands for you. A learner stops at each module's review point; an author or instructor may run the full regression suite without pretending to sign engineering gates.

| Lab | What you produce | Approximate hours | Original module connection |
|---|---|---:|---|
| [00 Setup](00-setup.md) | Official source build, tool versions, native executable receipt | 1 | 00, 12 |
| [01 Scan and state](01-scan-and-state.md) | Truth table and start/stop latch trace | 1–1.5 | 05, 06 |
| [02 Timers and edges](02-timers-and-edges.md) | R_TRIG, CTU, TON boundary evidence | 1.5 | 05, 06 |
| [03 Duplex contract](03-duplex-contract.md) | Requirement-to-test matrix, fault and restart cases | 2–3 | 01, 05, 06 |
| [04 Closed-loop plant](04-closed-loop-plant.md) | Offline trace viewer and failure experiments | 2–3 | 09 |
| [05 Break, test, repair](05-break-test-repair.md) | Three rejected compiled mutations, one repaired copy | 2–3 | 10 |
| [06 Two oracles](06-two-oracles.md) | Actual legacy Python/ST discrepancy report | 1.5 | 05, 06 |
| [07 Agent evidence](07-agent-evidence.md) | Review packet and independent learner handoff | 2 | 08, 10 |
| [08 Capstone](08-capstone.md) | Synthetic end-to-end submission, rubric | 4–6 | 11 |

## What actually executes

```text
ST source --MatIEC--> generated C --LLVM/host C compiler--> native executable
Python test driver --stdin scan images--> native C harness --stdout--> actual output CSV
Python toy plant <--> that same native controller
```

MatIEC is a real IEC language compiler. The course harness invokes compiled function blocks with simulated time. It is **not** the OpenPLC or Beremiz runtime and has no fieldbus, device drivers, hard-real-time scheduler, watchdog, retained memory or certified safety functions. The Python plant and old Python oracle are pedagogical simulations. The browser viewer only replays CSV evidence.

## Navigation and evidence

- [Toolchain sources and licenses](../reference/open-source-toolchain.md)
- [Verification ledger](VERIFICATION.md): actual execution, known warnings, platform limits
- [Independent learner report](LEARNER-REPORT.md): fresh-reader findings and repairs
- [Solutions and reference answers](solutions/README.md): read after predictions
- [BearBrown PLC workflow inventory](../reference/bearbrown-plc-inventory.md)
- [Machine-readable manifest](manifest.json): content IDs, paths, prerequisites, execution kind and status

The reference implementations are `plc/foundations.st`, `plc/station.st`, `runtime/harness.c` and `scripts/lab.py` at repository root. `scenarios/` contains hand-specified JSON expected values. `evidence/` stores selected real outputs; complete generated builds stay in ignored `build/`.

No commercial CAD tool is required for this spine. The original DraftSight exercise remains an optional, written-not-run branch of the wider course. No electrical-code adoption or verification is implied by executing software tests.
