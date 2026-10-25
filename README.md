# Agentic PLC Design

## Executive summary

**What this is.** A hands-on course for people who already build and test control panels and want to direct AI coding agents (Claude Code, Codex and their successors) to do the repetitive engineering around them: drawing edits, I/O lists, bills of materials, test plans, PLC logic, spec reviews and field troubleshooting. You do not need to be a programmer. You need to know what a correct duplex lift station panel looks like, because that knowledge is the one thing the agent does not have and cannot check for itself.

**Why take it.** Panel and PLC engineering is changing. Vendors now sell agents that turn a written spec into a project plan and working control logic. Whatever happens to those products, the work they automate is the template-driven 90 percent of design. The people who stay valuable are the ones who can set the agent up, point it at the 10 percent that varies, and *catch it when it is wrong*. This course trains exactly that, on one running project, with tools that run on your own machine and checks that fail loudly when the AI is wrong.

**What you end with.** A working agent-driven design workflow for a duplex lift station: one variant file in, and out come a rule check, an I/O list, a bill of materials, an AutoLISP script that edits a copy of a drawing, a Structured Text program, a test-vector table, a spec checklist with every requirement quoted, and a review packet a licensed person can sign. Plus the habits that let you rebuild that workflow when the tools change.

**What it does not do.** It does not replace a licensed engineer, a code book, a UL 508A listing process or a commissioning visit. Every reference table in the repo is marked UNVERIFIED until *you* check it against your code book and sign it. Nothing here has been run against a live panel, a real PLC or a real DraftSight install by the author; each module says what has been tested and what is waiting for you.

**Who built it.** This is an AI+1 course: an AI agent did the drafting and building, and the +1, the human expert, decides what is true and signs every gate. See `STATUS.md` for which gates are signed (none yet) and `AI1.md` in the `ai1-cli` book for the rules.

---

## How the course works

Every module has the same shape:

1. **The idea** in a page or less.
2. **The lab**: you run real commands against real files in `project/`.
3. **The five-part exercise** (the AI+1 pattern):
   1. *When to use AI* on this module's work,
   2. *When NOT to use AI*,
   3. *LLM exercise*: a prompt for Claude or another chat model,
   4. *CLI exercise*: a task for Claude Code or Codex working in the repo,
   5. *AI validation exercise*: you judge AI output against a checklist, and write a two-sentence AI Use Disclosure.
4. **Done when**: observable evidence, not a feeling.

The prompts are domain-specific on purpose. There are no generic "write me a PLC program" prompts in this course.

## Start here

```bash
cd agentic-plc-design
./check.sh
```

That runs the original 31 design tests and the executable-course checks. Start the new hands-on path at [labs/README.md](labs/README.md), beginning with the pinned open-source setup. The original [orientation](modules/00-orientation.md) remains useful for agent and review habits.

## New executable course spine

The course now includes nine detailed labs: native MatIEC setup; scan/state; IEC timers and edges; duplex requirements and tests; closed-loop plant simulation; deliberate compiled faults and repairs; Python-versus-ST discrepancy analysis; agent evidence; and a synthetic capstone with a grading rubric. See [the lab sequence](labs/README.md), [actual verification ledger](labs/VERIFICATION.md), [independent learner report](labs/LEARNER-REPORT.md), and [machine-readable manifest](labs/manifest.json).

The control code is translated by MatIEC and compiled to native machine code. A course C harness supplies deterministic simulated scans; Python drives tests and the toy plant. This is actual ST execution, but it is not OpenPLC, a production PLC runtime or real hardware. No account or paid service is needed for the executable labs.

## The modules

| # | Module | You build or learn |
|---|---|---|
| 00 | [Orientation](modules/00-orientation.md) | Install, first agent session, the rules of the road |
| 01 | [Teach the agent your trade](modules/01-teach-the-agent-your-trade.md) | A control narrative the agent interviews out of you |
| 02 | [The 10 percent that varies](modules/02-the-ten-percent.md) | Variant files and a rule checker |
| 03 | [Lists that cannot drift](modules/03-lists-that-cannot-drift.md) | I/O list, BOM, drawing cross-check |
| 04 | [Drawing edits by script](modules/04-drawing-edits-by-script.md) | Safe AutoLISP for DraftSight |
| 05 | [The oracle](modules/05-the-oracle.md) | A reference model and test vectors |
| 06 | [Logic you can read](modules/06-logic-you-can-read.md) | Structured Text, Studio 5000 exports, gap checks |
| 07 | [Check the math](modules/07-check-the-math.md) | Sizing tables you verify and sign |
| 08 | [Read the spec](modules/08-read-the-spec.md) | Bid spec to checklist, every row quoted |
| 09 | [The 2 AM call](modules/09-the-2am-call.md) | Log triage and read-only field help |
| 10 | [Build your own agent kit](modules/10-build-your-agent-kit.md) | CLAUDE.md, skills, hooks, subagents |
| 11 | [Capstone: a new job](modules/11-capstone-a-new-job.md) | A real job through the whole workflow |
| 12 | [Staying current](modules/12-staying-current.md) | Judging new tools and vendor claims |

Three real tools from the wild, written up against the course's rules, are in [case-studies/](case-studies/README.md): a Siemens TIA Portal MCP server, a TIA Portal skills plugin, and a Beckhoff TwinCAT agent. Read them after Module 12, or earlier as a preview of what you will be judging.

See [SYLLABUS.md](SYLLABUS.md) for time estimates and prerequisites, [AGENTS.md](AGENTS.md) for the standing rules every agent in this repo follows, and [reference/](reference/) for the lift-station primer, glossary, an honest AI-exposure map, and a cheat sheet for Claude Code and Codex.

## What is in the repo

| Path | Contents |
|---|---|
| `modules/` | The thirteen lessons |
| `project/variants/` | Three example stations: baseline, VFD with transducer, and a deliberately broken one |
| `project/tools/` | Python tools (standard library only): rule check, devices, I/O, BOM, sizing, AutoLISP generator and linter, cross-checks, L5X reader, spec checker, log summariser, test vectors |
| `project/data/` | Reference tables (UNVERIFIED until you sign them) and a generic parts catalog with invented part numbers |
| `project/plc/` | Original `lead_lag.st`, now compiled unchanged by the new lab harness; legacy timing mismatch preserved |
| `labs/` | Nine executable labs, synthetic contract, ST examples, scenarios, solutions and evidence |
| `scripts/` | Pinned local source installer, native compiler/test driver and offline trace viewer |
| `project/lisp/` | `apd-lib.lsp`, the safe-by-default AutoLISP helpers |
| `project/samples/` | Synthetic specs, extracts, logs and an AI-written risky script, each with planted errors |
| `project/tests/` | The test suite |
| `.claude/` | A skill, a reviewer subagent and a hook, as worked examples for Module 10 |
| `case-studies/` | Three public agentic PLC tools read against the course rules (nothing installed or run) |
| `reference/` | Primer, glossary, exposure map, tool-intake checklist, CLI cheat sheet |

## Requirements

- A Mac, Windows or Linux computer with Python 3.11 or newer.
- Claude Code and/or Codex installed (Module 00 walks through checking this). Any agentic CLI works; the prompts are written for Claude Code and carry Codex notes.
- For the executable spine: Python 3.12+, a working C/C++ toolchain/SDK, Make, Flex, Perl and curl. [Setup](labs/00-setup.md) builds pinned GNU tools and MatIEC locally.
- Optional legacy branches: DraftSight, OpenPLC Editor, Studio 5000. These have **not** been installed or run here; the new compiled labs do not require them.

## Honesty ledger

- **Tested here:** the Python tools and the 31 tests; the AutoLISP *generator* and *linter*; the hook script.
- **Executed in the expansion:** MatIEC-compiled starter, edge/counter/timer and duplex logic; native test scans; a Python toy plant driven by actual compiled outputs. The original ST was compiled unchanged and has two pump-output differences from its Python oracle across 37 rows. See the detailed ledger.
- **Written but not run:** the AutoLISP in `apd-lib.lsp`; no DraftSight, OpenPLC or Studio 5000 execution. The synthetic L5X remains hand-written, not a vendor export.
- **Invented:** every part number, the sample spec, the sample logs, the sample station. Nothing is a real vendor's catalog or a real customer's project.
- **Unverified:** every number in `project/data/nec-extracts.toml`. See Module 7.

## License

All rights reserved, Bear Brown, LLC, until the author says otherwise.
