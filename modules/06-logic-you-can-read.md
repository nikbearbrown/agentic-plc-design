# Module 06 — Logic you can read

## Executive summary

**What you do:** have an AI write a PLC program in Structured Text, run the oracle's test vectors against it in a simulator, and then use a script to cross-check a Studio 5000 export against your I/O list, looking for the bugs AI-written (and human-written) ladder logic really has: double coils, undefined tags, and I/O never used.

**Why:** vendors now sell agents that go from a written spec to working control logic, and a general agent can draft logic too. Your leverage is not writing it; it is reading it and proving it. You already read ladder schematics; PLC ladder was designed to imitate them, so that skill transfers directly. This module trains you to be the reviewer who catches what the generator cannot see.

**What you leave with:** a process for judging any generated program, a vectors-to-simulator workflow, and a read-only L5X checker. The new native laboratory path below has been executed; vendor IDE/runtime branches remain NOT VERIFIED. **Gate G4.** Time: about 5 hours.

---

## The idea

### Structured Text is for the agent to write and you to read

Structured Text (ST) is the text language in the IEC 61131-3 standard. It reads like simple pseudocode:

```
IF lvl >= 2 THEN call := TRUE; ELSIF lvl < 1 THEN call := FALSE; END_IF;
```

Open `project/plc/lead_lag.st`. It is the reference model's logic in ST, originally written by an AI without compilation, now compiled unchanged through the [native lab harness](../labs/06-two-oracles.md). Its original status comment is retained as historical provenance. You can read it, even if you have never written ST: it is the narrative, line by line. Compare it to `sim.py`; they should say the same thing.

Studio 5000 supports ST alongside ladder; OpenPLC (free, open source) runs ST on a laptop. You do not need Rockwell hardware to practice. You do need a simulator or emulator to *run* what the agent writes.

### Three kinds of evidence, in increasing order of value

1. **It compiles.** Necessary, nearly worthless.
2. **It passes the oracle's vectors** in a simulator. Real evidence on the cases you chose.
3. **A human with field knowledge reads it** and cannot find what is missing. The only one that catches a missing safety function.

### Reading a Studio 5000 export

Studio 5000 can export a project as an **L5X** file, which is XML (text). A script can read it without touching a controller. `project/tools/l5x_check.py` does three checks: I/O points the logic never mentions, tags the logic uses but nobody defined, and outputs driven by more than one `OTE` coil (the "double coil," a classic bug where two rungs fight over one output).

`project/samples/synthetic.L5X` is a small hand-written file with planted problems. **It is not a real Studio 5000 export.** Real exports have far more structure; the checker only looks for rung text, which is the same in both.

This is the same job Rockwell advertises for its AI agents ("compare existing programs against a spec to flag gaps"): a spec-to-code gap check. You are building a small, inspectable version so you can judge what a vendor's version is really doing.

---

## Lab

### Step 1 — Read the ST against the model

Read `project/plc/lead_lag.st` next to `project/tools/sim.py`. On paper, write the correspondences: *level index* (both), *call latch*, *alternation*, *lead fallback*, *lag timer*. Mark any line you think differs in behaviour. (There is a subtle one about *when* the lag pump turns on relative to the model: think about what a real timer does on the scan it starts, versus the model adding one second per scan. Predict which vector row will differ before you run it.)

### Step 2 — Use the executable open-source path

Complete [Lab 00](../labs/00-setup.md), then [Labs 01–03](../labs/README.md). These provide exact setup, real MatIEC compilation, native scan execution and deterministic checks. No vendor IDE, account or paid service is required. The harness is course code, not an OpenPLC runtime.

### Step 3 — Observe the legacy comparison

Follow [Lab 06: Two oracles](../labs/06-two-oracles.md). The comparison runs 37 legacy vector rows and exposes two actual pump-command differences at the five-second timer boundary. Preserve the output CSV. Individual alarm coverage also differs; no full equivalence is claimed.

### Step 4 — Review the discrepancy

Decide with the human whether the implementation, the Python model or the narrative's timing convention should change. The course preserves the old files rather than silently declaring a winner. The new compiled Station example follows its separately quoted synthetic contract. OpenPLC Editor and Studio 5000 remain optional platform-transfer investigations: installation, vendor compilation, runtime scheduling and hardware I/O are **NOT VERIFIED**. Do not force or download to real equipment.

### Step 5 — Check an export

```bash
python3 project/tools/apd.py l5x project/variants/a-baseline.toml project/samples/synthetic.L5X
```

Read the output. Which findings are real bugs? Which are only because the sample is a partial program? (Find the one where the checker is "right" but the finding is not a bug; this teaches the limit of automated checks.)

If you have a real Studio 5000 project you may use, export it as L5X to a **copy**, check your company's policy first, and run the checker locally. The tool reads the file and prints findings; it sends nothing anywhere and cannot write to a controller.

---

## Five-part exercise

### 1 — When to use AI

- **Drafting Structured Text from a narrative you wrote** — *why it works:* a spec-to-code translation with an oracle to judge the result.
- **Explaining an existing program rung by rung** — *why it works:* explanation you can verify by tracing signals yourself.
- **Writing a test harness that applies the vectors to a simulator** — *why it works:* mechanical glue code whose results you watch.

**The tell:** you have vectors and a verdict for each row before you believe the program.

### 2 — When NOT to use AI

- **Deciding the failure behaviour of the station** (what pumps do on loss of the level signal). *Why it fails:* a safety and permit decision tied to the owner and the regulator.
- **Adding interlocks and permissives the narrative did not specify.** *Why it fails:* a "helpful" interlock may also stop a pump when it must run.
- **Downloading to, or forcing I/O on, a live controller.** *Why it fails:* consequences are physical. This course does not do it. See `AGENTS.md` rule 1.

**The tell:** the program does something no sentence in your narrative asks for.

**Series tier:** *Tier 7, wisdom* — the judgment that some things stay with the person who answers for them.

### 3 — LLM exercise

**You are building:** a line-by-line explanation of an unfamiliar program, to check your own reading.
**Tool:** Claude chat.

```
Here is a Structured Text function block for duplex lift station pump control. I am an experienced panel builder who reads ladder fluently but does not write Structured Text. Explain it to me as a sequence of plain-language statements, in the order the code executes, using only what is literally in the code. Mark each statement with the line it comes from. Where the code does something I might not expect, say so. Do NOT tell me whether it is correct. Then list three things a lift station controller normally needs that this code does not do, if any, and three things the code does that are not in a basic lead/lag sequence, if any. [PASTE THE TEXT OF project/plc/lead_lag.st HERE]
```

**Adapt it:** paste your own program (a copy, with company policy checked) to understand an unfamiliar one.

**Produces:** an explanation you can compare with your own reading. Where they differ, one of you is wrong; find out which by tracing signals.

### 4 — CLI exercise

**You are building:** a compiled, tested ST program, with an honest log.
**Tool:** any available local agent. **Level:** advanced; the agent can run the native lab tools for you.

Setup: use the copy-only repair workflow in [Lab 05](../labs/05-break-test-repair.md). The following legacy vendor-error prompt applies only if you independently have a permitted vendor simulator and recorded its exact diagnostics; it is not the default executable path.

```
Read AGENTS.md. Read project/plc/lead_lag.st and scratch/compile-errors.txt, which has the exact errors OpenPLC Editor reported when I compiled it. Do not run any PLC tools; you cannot. For each error, tell me (a) which line it refers to, (b) what you think the cause is and how sure you are, and (c) the smallest change that would fix it. Do not apply any change yet. After I approve, apply only the approved changes to project/plc/lead_lag.st, and record each change in project/plc/CHANGES.md with the error text it addresses. Do not change the logic of the program. If a fix would change behaviour, flag it and wait. State clearly at the end that you have not compiled or run the result.
```

**Expected:** a table of errors with causes and minimal fixes; after approval, a small diff and a `CHANGES.md`.
**Inspect:** compare each diff hunk to the error it claims to address. Re-compile yourself. If new errors appear, repeat.
**If it goes wrong:** the main risk is the agent "fixing" a compile error by changing logic. `git diff project/plc/lead_lag.st` should show only syntax-shaped changes. A behaviour change must be a separate, visible decision.
**Standing rule:** *"A fix to make code compile must not change what it does. Behaviour changes are separate."*

### 5 — AI validation exercise

**You are validating:** the program (after compile) against the vectors, and the L5X checker output.
**Type:** code / agentic output. **Risk:** high.

```
□ Correctness: how many vector rows match? List every row that differs and your verdict
   (program wrong / oracle wrong / narrative silent).
□ Completeness: what does the program NOT do that the narrative requires?
   (Check alarms, float fault, both-pumps-unavailable, and power restore.)
□ Scope: does the program do anything no sentence in your narrative asks for?
□ Timing: the lag delay and the scan time. Does the simulator's scan match what you set?
□ L5X check: for each finding, label it real bug / artifact of a partial sample / false alarm.
□ Failure mode check: double coil; a latch with no unlatch; a timer reset by something unintended;
   a fail-safe that fails the wrong way; a test that passes because both sides share the same mistake.
```

**AI Use Disclosure** (two sentences).

---

## Done when

- `lead_lag.st` compiles in a real tool you ran (or you recorded the blocker), and you have a verdict for every vector row you ran.
- You have run `apd.py l5x` and can explain each finding, including one that is not a bug.
- You wrote down at least one behaviour the narrative should have specified and did not.

## Gate G4

Sign G4 in `STATUS.md` only when you compiled and ran `lead_lag.st`, or recorded precisely where it could not be, and `scratch/g4-notes.md` lists each difference between the program and the vectors with your verdict. A compile alone is not G4.
