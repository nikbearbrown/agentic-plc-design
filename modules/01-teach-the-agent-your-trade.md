# Module 01 — Teach the agent your trade

## Executive summary

**What you do:** have an AI interview you about how a duplex lift station panel should behave, turn your answers into a written *control narrative*, then catch the mistakes in an AI-written draft.

**Why:** a control narrative is the specification every later artifact (drawings, I/O, PLC logic, tests) is judged against. An agent can write a fluent one in ten seconds, and it will be subtly wrong. Writing it *with* the agent, from your knowledge, and then correcting it, is the most valuable skill in the course: you become the source of truth the tools cannot supply themselves.

**What you leave with:** a corrected control narrative in your own words (`project/narrative.md`) and a list of what the AI got wrong. Time: about 3 hours. **Gate G2 starts here.**

---

## The idea

When an experienced panel builder looks at a ladder schematic, they hold a whole sequence of operation in their head: *the pumps run down to the off float; the lag pump waits; a bad seal takes that pump out of the rotation; if both are out, somebody gets paged.* None of that is on the drawing. It is "tribal knowledge," and it is exactly what an AI agent lacks.

An agent given only "write the control logic for a duplex lift station" will produce the *average of the internet*: a plausible sequence that is right most of the time and wrong in the ways that matter (it stops at the lead float, short-cycles the pump, or lets a seal-failed pump keep running). The fix is not a cleverer prompt. The fix is to get the sequence out of your head and into a file, once, and make every later step cite that file.

Two ways to do that with an agent:

1. **Let it interview you.** You are the expert; make it ask the questions. This surfaces rules you forgot you knew.
2. **Let it draft, then you red-pen.** Faster, but you must read carefully, because fluent text is easy to skim past.

You will do both.

---

## Lab

### Step 1 — Read the primer

Read [reference/lift-station-primer.md](../reference/lift-station-primer.md) and the reference model's behaviour in `project/tools/sim.py`. The primer is the author's version of the sequence. **It may be wrong for your station.** Mark anything that differs from how your shop builds it.

### Step 2 — Red-pen the AI draft (before you do any interviewing)

Open `project/samples/narrative-ai-draft.md`. It is a synthetic draft an AI wrote from a one-line description. Read it twice. On paper or in a copy of the file, mark:

- every statement you believe is **wrong**,
- every statement that is **a policy choice** (could go either way depending on the owner),
- everything **missing** that the sequence needs.

Do this *before* reading the rest of this module. Write down how many errors you found and how long it took. If you found fewer than four, read it again, slower.

### Step 3 — Be interviewed

Start a chat (Claude, or `claude` in the repo) and send the LLM exercise prompt below. Answer from your own experience, in your own words, including the unglamorous details (what the beacon does, what happens in Hand, what the owner always asks for).

### Step 4 — Write the narrative

Have the agent assemble your interview answers into `project/narrative.md`. Then **you** edit the file. Delete anything you did not say. Add what it missed.

### Step 5 — Compare to the reference model

Run the model on a few cases and see if it agrees with your narrative:

```bash
python3 project/tools/apd.py vectors | head -30
```

Each row is one second of a scenario: the float and fault inputs on the left, what the model says the pumps and alarms do on the right. Pick three scenarios you know cold. Does the model do what your station does? Anywhere it does not, **your narrative wins and the model is wrong** — write the difference in `project/narrative.md` under a heading "Where the reference model differs." You will fix the model in Module 5.

---

## Five-part exercise

### 1 — When to use AI

- **Interviewing you for details you forgot to mention** — *why it works:* the agent has no ego about asking "what happens when…?" ten times; every answer is yours.
- **Turning your answers into a tidy document structure** — *why it works:* reformatting you can read in two minutes.
- **Listing edge cases to ask about** (both pumps down, float order wrong, power loss and restore) — *why it works:* generating options; you decide which apply.

**The tell:** every sentence in the final narrative is one you could defend to an inspector.

### 2 — When NOT to use AI

- **Deciding what the sequence is.** *Why it fails:* there is no ground truth in the model's training for *your* owner's standard; it will average.
- **Choosing alarm acknowledge and reset policy.** *Why it fails:* a values and contract question between you and the owner.
- **Deciding the lag delay, pump-down floor or alternation rule.** *Why it fails:* these are numbers and rules from the specification and the hydraulics, not from fluent text.

**The tell:** you accepted a sentence because it sounded right. Mark it and verify it.

**Series tier:** this trains *Tier 4, metacognitive supervision* — knowing when the machine's fluent answer needs outside grounding.

### 3 — LLM exercise

**You are building:** the raw material for your control narrative.
**Tool:** Claude chat (a Claude Project is better if you want it to remember your answers across days).

```
I design and build duplex submersible lift station control panels for municipal wastewater utilities. I want you to interview me to produce a control narrative, which is a written sequence of operation. Rules for you: ask ONE question at a time. Never answer your own question. Never fill in a detail I did not give you; if you need it, ask. Start with the physical station (pumps, floats or transducer, selectors, lights, alarms). Then walk the sequence: normal filling and pump-down, lag operation, alternation, a pump unavailable (Off, seal fail, over-temperature), both pumps unavailable, floats out of order, power loss and restore, Hand mode, high-level alarm and what resets it, and what the owner's SCADA sees. After each of my answers, restate it in one line so I can correct you. Stop after about 25 questions and write the narrative as numbered steps in my words, with a separate list titled "Things you assumed that I did not tell you." That list must not be empty if you have been honest.
```

**Adapt it:** replace "municipal wastewater utilities" with your customer type; add "our shop standard is…" lines for any rules you already have. In a Claude Project, paste this as project instructions and use the chat for the answers.

**Produces:** a numbered narrative plus an honest list of assumptions. Keep both.

### 4 — CLI exercise

**You are building:** `project/narrative.md`, committed to your branch.
**Tool:** Claude Code or Codex. **Level:** beginner.

Setup: your interview transcript saved as `scratch/my-interview.md` (the `scratch/` folder is git-ignored, so private notes never get committed).

```
Read AGENTS.md. Then read scratch/my-interview.md, which is my interview about how a duplex lift station panel should work. Create project/narrative.md containing: an Executive summary section (what this is, why it matters, what it does not cover); then the sequence of operation as numbered steps that use only facts from scratch/my-interview.md, each step ending with a bracketed reference like [Q7] to the interview question it came from; then a section "Assumptions I could not confirm" listing anything you inferred; then a section "Where this differs from project/tools/sim.py", comparing my narrative to the reference model by reading sim.py. Do not edit sim.py or any other file. Do not invent a step that has no [Q#] reference. Stop when done and tell me how many steps cite which questions.
```

**Expected:** one new file. Every step has a `[Q#]`.
**Inspect:** pick five steps at random and look up the cited question: does the interview say that? Look for steps with no citation. Check the "differs from sim.py" section against the code.
**If it goes wrong:** if steps appear that you never said, tell the agent "Delete every step that does not trace to a quoted line of scratch/my-interview.md," and rerun. If it edited `sim.py`, `git restore project/tools/sim.py`.
**Standing rule:** add to your own notes: *"Anything in a narrative must trace to something I said."* In Module 10 you will put this in your project instruction file.

### 5 — AI validation exercise

**You are validating:** the AI-written draft in `project/samples/narrative-ai-draft.md` (which you red-penned in Step 2) *and* your agent's `project/narrative.md`.
**Type:** reasoning chain / factual claim. **Risk:** high — a wrong sequence propagates into every later artifact.

```
□ Correctness: for each numbered step, is the described behaviour what a real station does?
   (In the draft: steps 3, 4, 5 and 6 each contain a claim to test.)
□ Completeness: is each of these covered? float order wrong / both pumps unavailable /
   power restore / Hand mode / what the owner sees on SCADA
□ Scope: does the narrative stay about the station, or has it drifted into design choices
   (enclosure, wire sizes) that belong elsewhere?
□ Traceability: does every step in YOUR narrative cite a question? Any that don't?
□ Failure mode check: fluent but wrong (a sequence that sounds right, would short-cycle a pump);
   confident silence (the draft never mentions a failure case at all);
   missing ground truth (the draft states a lag delay or alarm reset policy nobody gave it).
```

Compare your list of draft errors with a classmate's or the instructor's key. Count: errors you found / errors that exist. The goal is not a perfect score; it is to learn how *you* skim.

**AI Use Disclosure** (two sentences): what the AI produced and how you used it; one thing it could not determine that needed your judgment.

---

## Done when

- `project/narrative.md` exists, every step in it traces to something you said, and you have read it end to end.
- You can state, without notes, the four errors in the draft's steps 3–6.
- You have a "where the model differs" list for Module 5.

## Gate G2 (starts here, closes in Module 5)

G2 in `STATUS.md` is the +1's attestation that the control narrative *and* the reference model describe correct behaviour for your kind of station. You cannot sign it yet; the model is not corrected until Module 5. Read it now so you know what you are working toward.
