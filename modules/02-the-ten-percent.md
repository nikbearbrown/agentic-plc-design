# Module 02 — The 10 percent that varies

## Executive summary

**What you do:** capture what changes from job to job as a small text file (a *variant*), run a rule checker against it, and add one rule of your own.

**Why:** about 90 percent of lift station designs are repeats; the 10 percent that varies is where the mistakes live. If that 10 percent is written down as data, an agent can build everything else from it, a script can check it, and a designer can review one page instead of forty drawings. This is the same move that lets one person automate the repetitive edits instead of being replaced by them.

**What you leave with:** your own variant file, one new rule in the checker, and a clear sense of which rules are physics and which are only your shop's habits. Time: about 3 hours.

---

## The idea

Open `project/variants/a-baseline.toml`. It is about 30 lines. It says: 460 V, two 7.5 HP pumps, across-the-line starters, floats, relay control, a hazardous wet well, no generator. Everything about the station that is *not* in that file is the 90 percent that is the same every time.

Three things make a variant file powerful:

1. **One source of truth.** The drawing set, the I/O list and the BOM are all generated from it (Module 3). They cannot drift apart.
2. **It is checkable.** `project/tools/apd.py check` runs rules like "a 4–20 mA transducer needs a PLC or RTU" and "every station needs a high-level alarm." A rule is a sentence you already say out loud to apprentices, turned into code.
3. **It is small enough to review.** A reviewer reads 30 lines instead of hunting through a drawing set.

The format is TOML, a plain text format that looks like an INI file. You do not need to learn it; copy a variant and change values. The agent will edit it for you, and you check the result.

### Rules are the valuable part

The rules in `project/tools/design.py` (`check_variant`) are the author's guesses at what a duplex template should enforce. Some are physics ("analog input needs something to read it"). Some are policy ("VFD with relay control: who sets speed?" is only a warning, because some shops do exactly that). Which is which is *your* call, and it is the call this module trains.

---

## Lab

### Step 1 — Run the checker on the three examples

```bash
python3 project/tools/apd.py check project/variants/a-baseline.toml
python3 project/tools/apd.py check project/variants/b-vfd-transducer.toml
python3 project/tools/apd.py check project/variants/c-invalid.toml
```

Read the output for `c-invalid.toml`. **Before** you run it the first time, open the file and write down every problem you can see. Compare your list with the checker's.

### Step 2 — Predict, then check

Make a copy and break it on purpose in a way you predict:

```bash
cp project/variants/a-baseline.toml scratch/my-test.toml
```

Edit `scratch/my-test.toml`: change `hp` to `20`, `voltage` to `230`, and `method` to `"transducer"`. Predict which rules will fire. Then run the checker. Were you right? Which rule surprised you?

### Step 3 — Make your own variant

Pick a station you have actually built or are building. Write its variant in `scratch/my-station.toml`, starting from the closest example. If a real field does not fit (three pumps? a different voltage?), do not force it: write down what does not fit. Those misfits are the template's real limits, and the checker's `R01-duplex` rule is telling you about one.

### Step 4 — Write a rule

Think of a rule you enforce every time and the checker does not know. Examples: "a hazardous wet well with a VFD needs a line reactor," "generator transfer requires a run-permissive contact," "alarm beacon is required if SCADA is absent." State it in one sentence in `scratch/my-rule.md`, then have the agent add it (CLI exercise below).

---

## Five-part exercise

### 1 — When to use AI

- **Turning a station description into a variant file** — *why it works:* it is a form-filling task and you can read 30 lines in a minute.
- **Translating a rule you state in words into a checker function** — *why it works:* code you can test with a good case and a bad case.
- **Listing variant fields you did not think of** (VFD output filter, motor space heaters) — *why it works:* generating options; you accept or reject each.

**The tell:** you can say what the rule does without reading the code, and a test proves it.

### 2 — When NOT to use AI

- **Deciding which rules are errors and which are warnings.** *Why it fails:* a judgment about consequences in your customers' systems.
- **Inventing rules from "best practice."** *Why it fails:* an unsourced rule that sounds authoritative is the most dangerous kind; it will be enforced as fact.
- **Declaring a variant "valid."** *Why it fails:* passing a checker means no known rule fired, not that the station is correct.

**The tell:** you cannot say where a rule came from. Delete it or source it.

**Series tier:** this trains *Tier 5, causal reasoning* — knowing why a rule exists, not just that it does.

### 3 — LLM exercise

**You are building:** a first-draft variant file for a station you know.
**Tool:** Claude chat.

```
Here is an example variant file for a duplex lift station design workflow. It is TOML. I want you to write a new variant file for the following station and nothing else.

--- example ---
[job]
name = "Demo Lift Station A"
number = "DEMO-0001"
revision = "A"
[power]
voltage = 460
phase = 3
hz = 60
[pumps]
count = 2
hp = 7.5
starter = "across-the-line"
alternation = "alternate"
[level]
method = "floats"
hazardous_wet_well = true
[control]
platform = "relay"
[alarms]
points = ["high_level", "float_fault", "seal_fail_p1", "seal_fail_p2", "overtemp_p1", "overtemp_p2"]
[options]
generator_transfer = false
--- end example ---

My station: two 10 HP pumps at 230 V three-phase, soft starters, a 4-20 mA level transducer with a backup high-level float, a PLC, a generator with automatic transfer switch, hazardous wet well, with power-fail and generator-running alarms in addition to the standard ones. Use only the field names and allowed values shown (starter: across-the-line, soft-start or vfd; level method: floats or transducer; control platform: relay, plc or rtu). If something I described does not fit any field, do not invent a field; list it afterward under "Does not fit the template." Do not add comments claiming the design is correct.
```

**Adapt it:** replace the station description with a real job of yours (remove customer names). For ChatGPT or Gemini the prompt works unchanged.

**Produces:** a variant file plus a "does not fit" list. Save as `scratch/my-station.toml`; run `apd.py check` on it.

### 4 — CLI exercise

**You are building:** one new rule in the checker, with tests.
**Tool:** Claude Code (plan mode first). **Level:** intermediate; you read the diff, you do not write the code.

Setup: `./check.sh` passes; your branch is clean; write your rule in one sentence in `scratch/my-rule.md`.

```
Read AGENTS.md and scratch/my-rule.md. Add exactly the one rule described there to check_variant in project/tools/design.py: give it the next free id of the form R12-name, choose the level (ERROR or WARN) I specify in the rule file, and write the message in plain words a panel builder would say. Then add two tests to project/tests/test_design.py: one variant dict that triggers the rule and one that does not. If the rule needs a new field in the variant files, STOP and ask me instead of inventing the field. Do not edit any other rule, any variant, or any reference table. Run ./check.sh and show me the full output. Then show me git diff --stat.
```

**Expected:** `design.py` gains one block, `test_design.py` gains two tests; `./check.sh` passes.
**Inspect:** read the diff yourself. Does the rule fire when it should and stay silent when it should? Is it ERROR or WARN as you specified? Did the agent touch anything else?
**If it goes wrong:** the likely failure is the agent weakening an existing test to make its rule pass. `git diff project/tests` will show a deleted or loosened assertion. Reject the diff (`git restore .`) and rerun with "Do not modify existing tests."
**Standing rule to add (Module 10):** *"Never edit an existing test to make a new change pass."*

### 5 — AI validation exercise

**You are validating:** the rule and tests the agent wrote.
**Type:** code. **Risk:** medium — a rule that never fires looks exactly like a rule that works.

```
□ Correctness: run the "does trigger" test case by hand: apd.py check on a variant that should fire it.
   Does it fire, at the level you specified?
□ Completeness: is there a variant that SHOULD trigger it and doesn't? Try one more case than the agent did.
□ Scope: git diff --stat shows only design.py and test_design.py?
□ Silent-pass check: temporarily change the rule to `if False:` — does a test fail?
   If no test fails, the tests do not protect the rule.
□ Failure mode check: a rule that is too broad (fires on valid stations), too narrow (misses the case),
   or has the wrong level (ERROR where your shop would only warn).
```

**AI Use Disclosure** (two sentences).

---

## Done when

- You can predict `apd.py check` output for a variant before running it, most of the time.
- Your branch contains your station's variant (in `scratch/`, not committed) and one tested rule.
- You can name one rule in `design.py` that you now think should be a warning, not an error (or vice versa), and why.
