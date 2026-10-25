# Module 07 — Check the math

## Executive summary

**What you do:** audit the reference tables the tools use (motor current, conductor ampacity, breaker sizes), correct what is wrong, and sign them. Then audit the sizing logic itself and write down every place it is a simplification.

**Why:** an AI will give a number that looks exactly like a code-book number. Whether it *is* one is invisible without the book. This module makes the tools refuse to look authoritative until a human has verified the source data, and teaches you to audit calculations rather than trust them. It is also the module where the cost of a wrong value is highest: wire and breaker sizes are safety items.

**What you leave with:** a verified (or corrected-and-flagged) `nec-extracts.toml`, a list of sizing simplifications, and the habit of reading the banner. This closes **Gate G1**. Time: about 3 hours.

---

## The idea

Run it:

```bash
python3 project/tools/apd.py size project/variants/a-baseline.toml
```

The first line is `*** UNVERIFIED REFERENCE TABLES ... ***`. The second is a result like `{'fla': 11.0, 'awg': '14', 'breaker_a': 25, ...}`. Everything after the banner is computed from `project/data/nec-extracts.toml`.

That file says in its header: *typed by an AI from memory; not checked.* That is the honest state. The values may be right; many probably are. But "probably right" is not the bar for a safety table, and the *tools cannot tell the difference between a right table and a wrong one.* Only your code book can.

### Three layers of risk

1. **The data.** Is 7.5 HP at 460 V really 11 A in the table your jurisdiction has adopted? Is 12 AWG really 25 A in the 75°C column?
2. **The method.** The tool uses 125 percent of FLA for conductors and 250 percent for the breaker's maximum. The real rules have conditions: terminal temperature ratings, the next-size-up exception, motor-specific overload and protection requirements, and (for panels) UL 508A requirements that interact with the listed components.
3. **The selection.** The catalog logic picks a contactor by amps alone. Your shop picks by horsepower rating at the voltage, duty class, and maybe coordination with the protective device. The tool is simpler than reality **on purpose**, so you can find the difference.

### What the tool deliberately does not do

It does not compute **SCCR** (short-circuit current rating), voltage drop, derating for ambient temperature or conductor count, or arc-flash. Those need the real design data and the engineer's judgment. If an agent offers to "just calculate SCCR for you" from the BOM, the right reaction is suspicion: SCCR is set by the weakest listed component and the protection arrangement, and that depends on manufacturer data the agent does not have.

---

## Lab

### Step 1 — Verify the data, line by line

Open `project/data/nec-extracts.toml` next to your copy of the code book. For each value, tick or correct:

- `[fla_230]` and `[fla_460]`: HP to full-load amps.
- `[[conductor]]`: ampacity for each AWG at the 75°C column.
- `[breaker] standard_sizes`.
- `[breaker] max_multiple` and `conductor_multiple`: do they match the rules you apply?

Do this **yourself**, with a pencil and the book. It takes less than an hour and no AI is involved. That is the point.

### Step 2 — Correct and sign

Fix any wrong values. Then in the `[meta]` table set:

```toml
verified = true
verified_by = "your initials"
verified_date = "2026-..."
edition_checked = "NEC 20xx"
```

Run `python3 project/tools/apd.py size project/variants/a-baseline.toml` again. The banner disappears. From this point the hook in `.claude/settings.json` blocks any agent edit to this file, which is what "verified" means: the agent appends evidence elsewhere, it does not overwrite your signature.

If you are not able to check against the book right now, **leave it unverified** and write in `scratch/g1-notes.md` what you did check. Partial verification is honest; a signature is not.

### Step 3 — Audit the method

Pick two motors from your own jobs. Size them by hand the way you do on the job. Compare with `apd.py size`. Where do they differ? List each difference as *tool too simple / tool wrong / my habit not required by code*.

### Step 4 — Hunt for what is missing

Write the list of things a real motor-branch design considers that the tool ignores. Start from: terminal temperature rating, overload relay selection from nameplate, short-circuit rating, voltage drop, ambient derating, the specific starter type's own requirements (soft starters and VFDs have their own sizing and protection rules).

---

## Five-part exercise

### 1 — When to use AI

- **Writing a spreadsheet that applies your verified rules to a list of motors** — *why it works:* you checked the rules; the AI only repeats arithmetic, and you spot-check results by hand.
- **Explaining why a rule exists** (what the 125 percent factor is for) — *why it works:* explanation you can check against the book's text.
- **Producing a table of motors from a nameplate photo you transcribed** — *why it works:* you compare each row to the nameplate.

**The tell:** every input is in a file you verified, and every output is something you can recompute.

### 2 — When NOT to use AI

- **Supplying code values from memory.** *Why it fails:* plausible numbers, wrong edition, wrong column, wrong footnote. The most dangerous kind of fluent.
- **Deciding SCCR, coordination, or protection for a panel.** *Why it fails:* depends on listed component data and design intent; the AI has neither.
- **Declaring a calculation "per code."** *Why it fails:* compliance is a licensed person's judgment on the adopted edition and local amendments.

**The tell:** a number appears with no table name and no page.

**Series tier:** *Tier 4*, supervision of fluent numerical output; and a shot of *Tier 7*, because someone's name goes on the result.

### 3 — LLM exercise

**You are building:** a list of rules the sizing tool is probably missing.
**Tool:** Claude chat.

```
I build UL 508A industrial control panels for pumping stations. A script I use sizes a motor branch circuit like this: full-load current from the NEC three-phase motor table for the horsepower and voltage; conductor ampacity needed = 125 percent of that current, picked from the 75 degree C copper column; maximum inverse-time circuit breaker = 250 percent of the full-load current, rounded down to the next standard size; contactor chosen as the smallest one whose current rating is at least the full-load current. List the conditions, exceptions and additional requirements that a careful designer would check that this method ignores. For each, say which part of the method it affects, how sure you are that it applies (high/medium/low), and what exact section of what document I should open to confirm it. Do not give me any numeric values. If you are not sure of a section number, say so rather than guessing.
```

**Adapt it:** list your shop's own sizing practice in place of the method described.

**Produces:** a checklist of things to open the book for. Every section reference is a hypothesis, not a fact.

### 4 — CLI exercise

**You are building:** a test that fails if a table is changed without re-verifying.
**Tool:** Claude Code. **Level:** intermediate.

Setup: you have signed `nec-extracts.toml` (or left it unverified, deliberately).

```
Read AGENTS.md. In project/tests/test_design.py there is a test that checks the reference tables are flagged unverified. Add a new test file project/tests/test_tables.py with tests that: (1) load project/data/nec-extracts.toml and check that every FLA value in [fla_230] and [fla_460] is positive and increases with horsepower, (2) check that the [[conductor]] ampacities increase as the wire gets larger, (3) check that the breaker standard_sizes list is strictly increasing, and (4) check that if [meta] verified is true then verified_by, verified_date and edition_checked are all non-empty. Do not put any code-book values in the tests; the tests check shape only. Do not edit nec-extracts.toml or any existing test. Run ./check.sh and show me the output. Tell me clearly what these tests cannot catch.
```

**Expected:** one new test file; `./check.sh` passes. The agent should say these tests catch typos and ordering mistakes, **not** wrong values.
**Inspect:** try breaking the table: swap two values and confirm a test fails. Then restore it (`git restore project/data/nec-extracts.toml`; if you verified it and committed, restore from your commit).
**If it goes wrong:** if the agent writes tests that assert specific code-book numbers, those tests would simply echo the table. Reject: shape checks only.
**Standing rule:** *"Never write a code-book value into a test or a script from memory."*

### 5 — AI validation exercise

**You are validating:** a calculation the AI did for you.
**Type:** factual claim / structured data. **Risk:** high.

Setup: ask any AI: *"For a 15 HP, 460 V, three-phase induction motor, give the NEC full-load current, the minimum conductor ampacity, the conductor size, and the maximum inverse-time breaker size."* Save its answer in `scratch/ai-calc.md`.

```
□ Correctness: look up each number in your code book. Which match? Which don't?
□ Completeness: did it state its assumptions (75 C column? copper? which edition?)?
□ Scope: did it answer the question asked, or add conditions you did not ask about?
□ Citation check: did it name a table or section? Does that table say what it claims?
□ Method vs data: if a value is wrong, is it a data error (wrong amps) or a method error
   (wrong multiple, wrong column)?
□ Failure mode check: a confident number with no source; a right number for the wrong edition;
   rounding to a size that doesn't exist.
```

**AI Use Disclosure** (two sentences).

---

## Done when

- You have verified `nec-extracts.toml` against the book and signed it, or you recorded precisely what is and is not checked.
- You have a written list of at least five ways the sizing method is simpler than your shop's.
- You caught (or confirmed the absence of) an error in an AI's numerical answer.

## Gate G1

Sign G1 in `STATUS.md` only after Step 2: every value checked against your adopted NEC edition and `verified = true` set in the file. If any value was only "looks right," do not sign.
