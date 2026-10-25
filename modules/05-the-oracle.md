# Module 05 — The oracle

## Executive summary

**What you do:** correct a small reference model of lift station control until it matches how your station really behaves, write your own test cases for it, and use those tests to find three planted faults in a plausible-looking but wrong controller.

**Why:** when an AI writes control logic, "it looks right" is worthless and "it compiled" is almost as bad. The only evidence is behaviour on cases you chose. A reference model plus a table of test cases is the cheapest honest way to judge any PLC program, whether an AI wrote it, a colleague wrote it, or a vendor tool generated it.

**What you leave with:** a corrected reference model, a test table of your own, and practice finding bugs from failing tests. This closes **Gate G2**. Time: about 3 hours.

---

## The idea

A **reference model** (an *oracle*) is a short program that says what the controller *should* do for any set of inputs. Ours is `project/tools/sim.py`: about 100 lines of Python that takes float states and pump faults and returns which pumps run and which alarms are on.

A **test vector** is one row: *these inputs, this long, should give these outputs.* `apd.py vectors` prints eight scenarios as a table. In Module 6 you will force the same inputs on a real or simulated PLC and compare.

Three rules keep this honest:

1. **The oracle is trusted only after you correct it.** It was written by an AI from a general description. The first job is to find where it is wrong *for your station*.
2. **Tests come from you.** An AI can write many tests, but if it writes the model and the tests, they agree with each other and with nothing else. Your cases are the independent evidence.
3. **A passing test proves little; a failing test proves a lot.** Passing says "no known case breaks it." Failing says "here is a specific input that gives the wrong behaviour." That is why this module's most valuable object is a controller that *fails*.

---

## Lab

### Step 1 — Run the tests and meet the flawed controller

```bash
./check.sh
APD_TEST_FLAWED=1 python3 -m unittest discover -s project/tests -p test_sim.py -v
```

The second command runs the *same tests* against `project/tools/sim_flawed.py`. Three fail. Read the names of the failing tests. **Do not open `sim_flawed.py` yet.**

### Step 2 — Predict the faults from the failures

For each failing test, write a sentence: *"The flawed controller does X in situation Y, where it should do Z."* Then read `sim_flawed.py` and find the lines. You will find three faults. (An answer key exists in `instructor/` for instructors.)

### Step 3 — Where does the model differ from your station?

Return to your Module 1 narrative's "Where this differs" section. For each difference, change the model in `project/tools/sim.py` through the agent (CLI exercise) so it matches **your** narrative. Examples: your station alternates on every start; your lag delay is 10 seconds; a high-level float starts both pumps immediately.

### Step 4 — Write ten test cases yourself

In `scratch/my-cases.md`, write ten cases in plain words:

> *Case 4: P1 in Off, P2 healthy, level rises to the lead float, then to lag. Expect: P2 runs alone; P1 never runs; no lag start because only one pump is available.*

Include at least: a case where order matters (the second cycle), a case with two faults, a case with a stuck float, and one that "should never happen" but might.

### Step 5 — Turn the cases into vectors

Have the agent turn your ten cases into entries in `project/tools/vectors.py` and tests in `project/tests/test_sim.py` (CLI exercise). When they all pass on the corrected model, and the flawed one still fails them, the oracle is ready.

---

## Five-part exercise

### 1 — When to use AI

- **Turning your plain-language cases into test code** — *why it works:* translation; you can read each test and each case side by side.
- **Suggesting cases you did not think of** (power restore mid-cycle, both pumps unavailable then one returns) — *why it works:* generating options; you decide which are real.
- **Explaining why a test fails** — *why it works:* the failure is concrete and the explanation can be checked by changing one line.

**The tell:** each test has a one-line reason a reader can trace to your narrative.

### 2 — When NOT to use AI

- **Deciding what the expected output is.** *Why it fails:* if the AI decides what is right and also writes the code, nothing is independent. The expectation must be yours.
- **"Fixing" a failing test by changing the expectation.** *Why it fails:* this converts a bug report into silence.
- **Concluding the logic is correct because all tests pass.** *Why it fails:* tests cover the cases someone thought of.

**The tell:** you cannot say which of your narrative's sentences a test is checking.

**Series tier:** *Tier 5, causal reasoning* — tests as interventions that distinguish a working design from one that happens to look right.

### 3 — LLM exercise

**You are building:** a list of edge cases you may not have thought of.
**Tool:** Claude chat.

```
Here is the control narrative for a duplex lift station panel, written by me, an experienced panel builder: [PASTE THE TEXT OF project/narrative.md HERE]. I have a reference model that takes four float states (off, lead, lag, high), a Hand-Off-Auto state for each pump, and seal-fail and over-temperature signals for each pump, and returns whether each pump runs and which alarms are on. I will judge every answer myself. Do not tell me what the right behaviour is. Instead, list 20 specific situations, each as a one-line combination of inputs and sequence of events, that you think a test suite for this controller should include and a tired designer is likely to forget. Group them: sequencing, faults, float problems, mode changes (selector switches moved while running), and power events. For each, add the question I should ask my narrative: "what should happen here?" Mark which ones you think my narrative does not answer.
```

**Adapt it:** paste your actual narrative where the prompt says to (this is the one place the prompt needs your text, because it is the point). Keep customer names out.

**Produces:** a list of cases and a list of gaps in your narrative. The gaps are the real output.

### 4 — CLI exercise

**You are building:** your corrected model and your ten tests.
**Tool:** Claude Code (plan mode). **Level:** intermediate.

Setup: `scratch/my-cases.md` has ten cases in plain words; `project/narrative.md` is yours; `./check.sh` passes.

```
Read AGENTS.md, project/narrative.md and scratch/my-cases.md. Step 1: do not change any file; read project/tools/sim.py and list every place where it behaves differently from project/narrative.md, quoting the narrative sentence and the line of sim.py. Show me that list and wait for my approval. Step 2, only after I say go: change sim.py to match the narrative, changing nothing else, and add one unittest to project/tests/test_sim.py for each of my ten cases, named test_case_N_<short description>, with a docstring quoting my case in my words. Do not change any existing test or any expectation in an existing test. Run ./check.sh, and also run APD_TEST_FLAWED=1 python3 -m unittest discover -s project/tests -p test_sim.py and tell me which tests fail on the flawed controller. Show git diff --stat.
```

**Expected:** a list of differences first (stop and read it!), then a small diff to `sim.py` and ten new tests.
**Inspect:** for each of the agent's changes to `sim.py`, find the sentence in your narrative that justifies it. For each new test, check that the expected values are *yours*, not whatever the model happens to output.
**If it goes wrong:** the classic failure is the agent writing the tests by *running the model and copying its outputs as the expectation.* To catch it: pick two tests and change the model's behaviour on purpose; a good test fails, a copied one may not. Tell the agent: "Expected values come from my cases file, not from running sim.py."
**Standing rule:** *"Expected values in a test come from the human's cases, never from running the code under test."*

### 5 — AI validation exercise

**You are validating:** the flawed controller, and your agent's new tests.
**Type:** code / agentic output. **Risk:** high.

```
□ Correctness: name the three faults in sim_flawed.py in a sentence each, and the test that caught each.
□ Completeness: is there a fault the tests did NOT catch? Think of a fourth bug and add a
   case that would catch it. (If you cannot think of one, ask: what has the suite never seen?)
□ Scope: did the agent's sim.py edit change anything not in the difference list you approved?
□ Independence: for two new tests, change the expectation to the wrong value. Does the test fail?
   Change the model to be wrong. Does the test fail? Both must.
□ Failure mode check: tests that copy the model's output as truth (circular), tests that always pass,
   tests that depend on a previous test's state.
```

**AI Use Disclosure** (two sentences).

---

## Done when

- `./check.sh` passes with your corrected model and your ten tests, and the flawed controller still fails.
- You can name the three planted faults and one more you invented.
- Your narrative and the model agree, and you have read both.

## Gate G2

G2 in `STATUS.md` says the control narrative and the reference model describe correct behaviour for your kind of station. Sign it if you read both end to end and they agree. If you hesitated on any behaviour, do not sign: write the open question in `scratch/g2-open.md` and resolve it with whoever sets the owner's standard.
