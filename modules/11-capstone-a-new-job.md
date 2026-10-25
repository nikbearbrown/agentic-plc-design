# Module 11 — Capstone: a new job

## Executive summary

**What you do:** take one real job from your own shop (or a realistic one you invent) from a specification to a review packet, using every tool and habit from the course, with a second agent reviewing the first one's work, and sign the gates you can honestly sign.

**Why:** the modules taught the parts. The capstone tests whether you can run the whole workflow under realistic pressure, where the spec is imperfect, the variant does not quite fit the template, and a plausible AI answer is waiting at every step. The product is not the code; it is a packet a licensed person could review in an hour, with every claim traced to evidence and every unknown labeled.

**What you leave with:** a complete, honest review packet for one job, and a written account of where the workflow held and where it broke. Time: about 6 hours.

---

## The task

You are the designer of record for a new duplex lift station. Choose one:

- **A.** A real job of yours (company-policy permitting; scrub customer names), or
- **B.** An invented one: a station with a feature that does **not** fit the template (a third pump, a different voltage, a flow meter, a different alarm set).

Option B is recommended the first time. The point is to find where the template ends.

## The workflow

Work through these stages in order. Each stage ends with something observable. If a stage fails, stop and write down why; a failure documented is worth more than a hidden one.

| Stage | Work | Evidence |
|---|---|---|
| 1. Spec | Run Module 8's workflow on the job's spec (real or synthetic). | A checklist where every row passes `apd.py spec`, plus a list of gaps |
| 2. Narrative | Adapt your Module 1 narrative to this job. | `scratch/capstone-narrative.md`, every step traceable |
| 3. Variant | Write the variant file. Run `apd.py check`. | A variant with no ERROR and a "does not fit" list |
| 4. Lists | Generate devices, I/O, BOM with **your** catalog. Cross-check against the drawing extract (real, or build a sample). | Lists, the banner status, a cross-check report |
| 5. Drawings | Generate the AutoLISP job script, lint it, dry-run on a copy. | Linted script, dry-run log |
| 6. Logic | Update the model and tests for the job's differences; get an AI to draft the logic; run the vectors. | Test table with verdicts; any compile or simulator log |
| 7. Math | Size the motors with the verified tables; list what the tool ignores for this job. | Sizing output, gap list |
| 8. Review | Run the `panel-reviewer` subagent on each artifact in a fresh session. | The reviewer's report; your response to each finding |
| 9. Packet | Assemble the review packet (below). | `scratch/capstone-packet.md` |
| 10. Debrief | Write what held and what broke. | `scratch/capstone-debrief.md` |

## The review packet

A single Markdown file that opens with an Executive summary a reviewer can read in two minutes, then contains, in order:

1. What this job is and what was *not* done.
2. The spec checklist and its coverage gaps.
3. The narrative.
4. The variant and the rule-check output.
5. The I/O list and BOM, with their basis columns and the banner status.
6. The cross-check report.
7. The AutoLISP script's lint output and dry-run log.
8. The test table with verdicts.
9. The sizing output and the list of what the tool does not compute.
10. The reviewer agent's findings and your disposition of each (accepted, rejected with reason, open).
11. **A "Not verified" table**: every artifact and what has not been run or checked. If this is empty, you are lying to yourself.
12. The gate status and the signatures that were actually earned.

---

## Five-part exercise

(Applied to the capstone as a whole.)

### 1 — When to use AI

Across the capstone, AI earns its place on: extracting and tabulating spec requirements, drafting the variant and narrative from your answers, generating lists and scripts from the variant, writing test harness glue, drafting the packet's structure, and running as an independent reviewer. In each, a checker, a log or an oracle tells you whether it worked.

**The tell:** each AI-produced artifact has a named check next to it in the packet.

### 2 — When NOT to use AI

Across the capstone, these stay with you: deciding what the sequence is; verifying and signing tables; deciding what a failure should do; choosing a component for the duty; interpreting an ambiguous spec requirement; running anything against a live controller; signing a gate.

**The tell:** the packet contains a judgment with no named human behind it.

**Series tier:** all of *Tiers 4, 5, 6 and 7* — supervision, causal reasoning, collective accountability and wisdom.

### 3 — LLM exercise

**You are building:** the skeleton of your packet's Executive summary and "Not verified" table.
**Tool:** Claude chat, after you have the stage evidence.

```
I have finished the design workflow for a duplex lift station and I am assembling a review packet for a licensed reviewer. Below is a list of each artifact I produced, what check I ran on it, and the result. Write two things and nothing else. First, an Executive summary of at most 200 words in plain language: what the job is, what was done, what was found, and what was NOT done or NOT verified. Second, a table titled "Not verified" with one row for every artifact, with columns: artifact, what has been checked, what has NOT been checked, who must check it. Rules: use only the information I give you; do not describe any artifact as tested, verified or compliant unless my list says so; if my list is silent on whether something was run, write UNKNOWN in the table; do not soften anything. [PASTE YOUR ARTIFACT LIST WITH CHECKS AND RESULTS HERE]
```

**Adapt it:** list your real artifacts and results in a simple table.

**Produces:** an honest summary and a "Not verified" table. If it comes back sounding too good, tighten the list, not the prompt.

### 4 — CLI exercise

**You are building:** the reviewer's report.
**Tool:** Claude Code, in a **fresh session** that did not write the work, using the `panel-reviewer` subagent.

```
Use the panel-reviewer subagent. Give it these artifacts to review without telling it what I concluded: the variant file at scratch/capstone-variant.toml, the BOM and I/O list generated from it, the AutoLISP job script scratch/capstone-job.lsp, and the test table at scratch/capstone-tests.md. For each artifact, run the matching tool in project/tools and quote its output, then report PASS, FAIL or CANNOT-DETERMINE with a reason, and end with the one question a licensed panel builder should answer before signing. The subagent must not edit any file. Save its full report to scratch/reviewer-report.md. Then tell me which of its findings you could confirm yourself by running a tool and which rest on judgment alone.
```

**Expected:** a reviewer report with at least one real finding.
**Inspect:** for each FAIL, reproduce it. For each PASS, ask what the reviewer cannot see. Compare its list with your own: did it miss something *you* caught? Did it flag something that is not a problem?
**If it goes wrong:** a reviewer that agrees with everything is not reviewing. Re-run with a deliberately broken artifact to confirm it can fail.
**Standing rule:** *"The agent that wrote it does not review it."*

### 5 — AI validation exercise

**You are validating:** your own packet, as if you were the licensed reviewer.
**Type:** all. **Risk:** high.

```
□ Traceability: pick three claims in the packet. Follow each to its evidence. Do all three hold?
□ Honesty: is anything described as tested that was only written? Check each against your logs.
□ Completeness: what would a reviewer want that is not here?
□ "Not verified": is it long enough? Would a reviewer be surprised by anything not listed in it?
□ Signatures: is every gate you signed backed by something you actually did? Unsign any that are not.
□ Failure mode check: confidence drift (the executive summary sounds more certain than the body);
   evidence with no owner; "all tests pass" with no test list.
```

**AI Use Disclosure:** for the capstone, write a half-page: what the AI produced across the whole workflow, where you overrode it, and one decision that only you could have made.

---

## Done when

- Your packet exists, opens with an executive summary, and has a non-empty "Not verified" table.
- You have a reviewer report from an agent that did not write the work, and a disposition for each finding.
- You have a debrief naming the step where the workflow broke or where the AI most nearly fooled you.

## Gates

Review `STATUS.md`. Sign only the gates you earned, with date and initials. Leave the rest blank and write beside each what is still needed. G5 (lesson accuracy) and G6 (release) belong to whoever is deciding whether to share this course; that may be you.
