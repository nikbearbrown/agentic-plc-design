# Module 12 — Staying current

## Executive summary

**What you do:** build a routine for evaluating the next AI tool (or the next vendor claim) quickly and honestly: a tool-intake sheet, a same-task test, and a 90-day review habit. You apply it to one real tool or announcement.

**Why:** everything in this course will date. The agentic tool names will change, vendors will ship agents that do part of what you built by hand, and some of your workflow will become a product. The durable skill is deciding, with evidence, what to adopt, what to pilot, and what to ignore, while keeping the part of the work that stays yours. The people who stay valuable are those who can check the machine and who know the field.

**What you leave with:** one completed intake sheet, a calendar habit, and a personal plan for the next two years. Time: about 2 hours.

---

## The idea

### Claims are not evidence

A vendor says its agent turns a spec into working control logic and flags gaps. Another says its tool makes engineers "3 to 5 times faster." Neither sentence is useful until you know: *what was measured, on what task, by whom, against what baseline, and with what checking?* The tool-intake sheet (`reference/tool-intake.md`) is eleven questions that force those answers.

The most important question is the **oracle question**: *How will I know it is wrong?* If the answer is "I'll look at it and see if it seems right," you have no way to know. You built oracles in this course: a reference model, a quote checker, a cross-check, a linter. A new tool is only as safe as the checker you can point at it.

### Re-run your own tests on new tools

The test suite and the sample artifacts from this course are now a benchmark you own. A new tool that claims to write PLC logic should be handed the Module 5 narrative and judged by the Module 5 vectors. A new tool that claims to review specs should be handed the synthetic spec and judged against the planted errors. The results are *your* data, not the vendor's.

### What stays yours

At each step the work moved a little: the agent generates, the checker verifies, you decide. The pattern holds as tools improve: the generating gets cheaper, the verifying and deciding get more valuable. Be specific about what you want to be known for: commissioning, field diagnosis, the customer's trust, the sequence that works at 2 AM. The less of that an AI can do, the more of your career belongs there.

---

## Lab

### Step 1 — Pick a real target

One tool or claim from the last month. For example: a vendor's AI engineering agent from an announcement; an agent feature in your CAD or PLC software; a new general-purpose agent release. Do not pick anything you cannot get hands on or at least read the documentation for. If you want a worked example first, read the three in [case-studies/](../case-studies/README.md), which apply this same sheet to real PLC tools.

### Step 2 — Fill in the intake sheet

Copy `reference/tool-intake.md` to `scratch/intake-<toolname>-<date>.md` and answer every question. Leave blanks where you do not know. Count the blanks.

### Step 3 — Run the same-task test

Choose a task from the course. Run it on the tool three times, record results, and compare to the course's tools. If you cannot run the tool, write why and what you would need.

### Step 4 — Decide and schedule

Give a verdict (adopt / pilot / watch / ignore), put a review date 90 days out in your calendar, and write one sentence about what would change your mind.

### Step 5 — Write your two-year plan

On one page: the things you will practice (name the field work and programming skills you want), the tasks you will automate yourself first, what you want to be the person who checks, and the first three things you will do next month. Keep it in `scratch/two-year-plan.md`.

---

## Five-part exercise

### 1 — When to use AI

- **Summarising documentation and release notes for a new tool** — *why it works:* extractive; verify against the source.
- **Drafting test cases for the tool from your existing benchmark** — *why it works:* you already have an oracle to judge the results.
- **Comparing two tools on features you list** — *why it works:* structured comparison with your criteria.

**The tell:** the comparison is built on your test results, not on marketing text.

### 2 — When NOT to use AI

- **Deciding which tool to adopt for work with customer data.** *Why it fails:* policy, contract and risk.
- **Predicting where the field is going.** *Why it fails:* speculation formatted as forecast; any year-by-year table of the future is a guess.
- **Deciding your career.** *Why it fails:* depends on your goals (income, body, growth, security), which no tool knows; each points to a different answer.

**The tell:** you are following a confident timeline from a tool.

**Series tier:** *Tier 7, wisdom* — deciding under uncertainty, with the humility to schedule a review rather than pretend to know.

### 3 — LLM exercise

**You are building:** a skeptical read of a claim.
**Tool:** Claude chat.

```
Below is a claim from a vendor announcement about an AI engineering tool for industrial control systems. I am an experienced control panel builder and I want to judge it, not be sold it. Do these things only. 1: Rewrite the claim as the most specific testable statement it could be, and list the words in the original that carry no measurable meaning. 2: List the questions I would need answered to know if it is true for my work: what was measured, on what task, compared with what, by whom, and who bears the cost when it is wrong. 3: Propose three small tests I could run in an afternoon with files I already have, each with a way to tell whether the tool passed that does not depend on the tool's own judgment. 4: List what would have to be true for this tool to be safe to use on a real project. Do not say whether the claim is true. Do not use any information you are not sure about; say you do not know. [PASTE THE CLAIM HERE, WITH ITS SOURCE]
```

**Adapt it:** paste any claim, from any source.

**Produces:** a testable restatement and an afternoon test plan. Run one.

### 4 — CLI exercise

**You are building:** your own benchmark folder from the course.
**Tool:** Claude Code. **Level:** intermediate.

```
Read AGENTS.md. Create a folder benchmark/ in this repository containing a README.md and a run.sh. The README must open with an Executive summary: this folder collects the course's oracles so a new AI tool can be tested against the same cases. It must list, for each of these, the input file, the oracle (the checker or test that judges the output), and the planted errors a tool should find: the narrative draft and my corrected narrative; the reference model with its tests and the flawed controller; the spec excerpt and its checklist checker; the drawing extract and the cross-check; the L5X sample and its checker; the risky AutoLISP sample and the linter. Do not copy any file; reference them by path. run.sh must run ./check.sh and then each checker on its sample and print one line per oracle saying what it found, without exiting early on an expected failure. Do not read or reproduce anything in scratch/ or instructor/. Run run.sh and show me the output. State what you ran and what you did not.
```

**Expected:** a `benchmark/` folder whose `run.sh` demonstrates every oracle on the planted samples.
**Inspect:** run `run.sh` yourself. Does it list the planted errors without leaking the answer key? Would a new tool know how to be scored from it?
**If it goes wrong:** the agent may copy the instructor key's contents into the README. Check: that file is private to instructors and must not appear in the benchmark.
**Standing rule:** *"Keep a benchmark of my own planted-error cases; test every new tool against it."*

### 5 — AI validation exercise

**You are validating:** a vendor-style claim, and the AI's analysis of it.
**Type:** factual claim / reasoning. **Risk:** medium (the cost is time and misplaced trust).

```
□ Correctness: is the restated claim really what the original says, or did the AI sharpen it?
□ Completeness: what question about cost of error was NOT asked?
□ Scope: did the AI use outside facts about the product that it cannot know?
□ Test quality: for each proposed afternoon test, is the pass condition independent of the tool?
□ Failure mode check: the AI sounding more sure than the claim's source; an invented statistic;
   a test whose pass condition is "the tool says it worked."
```

**AI Use Disclosure** (two sentences).

---

## Done when

- You have a completed intake sheet with a verdict and a review date.
- You have a `benchmark/` that you can hand a new tool.
- You have a two-year plan that names what you will practice, what you will automate, and what you will be known for.

## After the course

Re-run `./check.sh` every time you change a tool or a model. Re-read `reference/ai-exposure-map.md` every six months and correct it where your own experience disagrees. When this course is out of date, fix it; the habits are what lasts.
