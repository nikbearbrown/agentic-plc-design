# Module 08 — Read the spec

## Executive summary

**What you do:** turn a long municipal-style bid specification into a requirements checklist in which every row carries a verbatim quote and a section number, then run a checker that rejects any row whose quote is not really in the spec.

**Why:** spec review is one of the best early uses of AI in this trade: the documents are long, repetitive and full of "shall." It is also where AI hurts people most quietly, because a requirement that was invented or misquoted looks just like a real one, and a missed requirement becomes a rejected submittal or a change order. The rule is *quote it or it does not exist*, and this module gives you a tool that enforces it.

**What you leave with:** a repeatable spec-to-checklist workflow, a "quote-or-it-didn't-happen" checker, and a submittal matrix pattern. Time: about 3 hours.

---

## The idea

A municipal spec section for pump station control panels might run 15 to 40 pages, with references to other sections, standards and drawings. A submittal reviewer (an engineer working for the owner) checks your submittal against it, line by line. Everything you can catch before they do saves a resubmittal cycle.

An AI can read the whole thing in seconds and produce a checklist. The failure modes:

1. **Invented requirement.** "Provide an audible horn" when the spec never says so.
2. **Misattributed requirement.** Right requirement, wrong section; you cite 2.3 and the reviewer looks in 2.3 and cannot find it.
3. **Dropped requirement.** The one that costs you.
4. **Softened language.** "Shall" becomes "should"; "only" disappears.

The first two are caught mechanically: the checker (`project/tools/spec_check.py`) confirms every quote appears verbatim in the spec text and sits under the cited section. The third and fourth need you.

```bash
python3 project/tools/apd.py spec project/samples/spec-excerpt-synthetic.md project/samples/spec-checklist-ai.csv
```

The sample spec is **synthetic** (invented for training; not from any real project). The sample checklist is an AI draft with planted problems. Run it and read what is flagged.

### Checklist file format

A CSV with four columns: `id`, `requirement` (your paraphrase), `section` (like `2.3`), `quote` (copied exactly from the spec). The checker normalises whitespace and case but nothing else.

### Company and customer documents

A real bid spec is usually public, but your company's rules on what may be sent to an AI service still apply, and some documents (customer standards, proprietary details) are not public. Read `scratch/my-ai-rules.md` from Module 0 and, if unsure, ask. Do the lab on the synthetic spec first. The checker runs locally and sends nothing anywhere.

---

## Lab

### Step 1 — Find the planted problems by hand

Read `project/samples/spec-excerpt-synthetic.md`. Then read `project/samples/spec-checklist-ai.csv`. Without running the checker, mark each row: **genuine / invented / wrong section / no source**. Time yourself.

### Step 2 — Run the checker and compare

Which problems did you catch that the checker did not? (None, hopefully, for *these* kinds.) Which did the checker catch that you missed? Now look at row R4 and R8: they **passed** the checker. Is each a faithful statement of the requirement? A quote that exists in the spec can still be used to support a requirement the quote does not say. The checker proves *presence*, not *meaning*.

### Step 3 — Find what is missing

List the requirements in the sample spec that are **not** in the checklist. (There are several; the spec has submittal, enclosure, power, pump controls, alarms and testing requirements.) Missing rows are the checker's blind spot.

### Step 4 — Build a submittal matrix

For each checklist row, add columns: *where we comply* (drawing number or BOM line), *how we know* (a test, a datasheet), *deviation?* Leave the evidence blank where you do not have it. A blank is information.

---

## Five-part exercise

### 1 — When to use AI

- **Extracting every "shall" sentence from a long spec into a list with section numbers** — *why it works:* mechanical, extractive, and the quotes are checkable by a script.
- **Grouping requirements by discipline** (electrical, controls, SCADA, testing) — *why it works:* sorting, easy to audit.
- **Drafting questions for the engineer where the spec is ambiguous or conflicts with a referenced standard** — *why it works:* generates leads; you decide which are real.

**The tell:** every row survives `apd.py spec`.

### 2 — When NOT to use AI

- **Interpreting an ambiguous requirement.** *Why it fails:* a contract interpretation; only the engineer of record decides.
- **Deciding that a requirement does not apply to you.** *Why it fails:* a commercial and legal decision.
- **Signing a compliance statement.** *Why it fails:* a signature is a human attestation.
- **Trusting a summary of a spec you have not skimmed.** *Why it fails:* you cannot detect what was dropped without a map of the document.

**The tell:** you cannot point to the page.

**Series tier:** *Tier 4*, and *Tier 6, collective* judgment — the shared accountability among contractor, engineer and owner.

### 3 — LLM exercise

**You are building:** a quote-backed checklist from a spec excerpt.
**Tool:** Claude chat (or a Claude Project holding the spec). Use the synthetic spec until your company policy covers real ones.

```
Below is a specification section for industrial control panels. Produce a requirements checklist as CSV with exactly these columns: id, requirement, section, quote. Rules: (1) include a row for every sentence that contains the words shall, must, or required, and every sentence that states a number, a standard, or a prohibition; (2) the quote column must be copied character-for-character from the spec, between double quotes, with no edits and no ellipsis; (3) the section column must be the number of the nearest numbered heading above the quote, such as 2.3; (4) the requirement column is a paraphrase of at most 15 words that does not add anything the quote does not say; (5) if a sentence is ambiguous, still include it and put the word AMBIGUOUS at the start of the requirement; (6) do not include any row that you cannot support with a verbatim quote, and do not add requirements from your general knowledge of such panels, even common ones. At the end, list in plain text any numbered heading you did not extract anything from. [PASTE THE TEXT OF project/samples/spec-excerpt-synthetic.md HERE]
```

**Adapt it:** paste another spec section. For a very long spec, run it section by section so quotes stay precise.

**Produces:** a CSV. Save as `scratch/checklist.csv` and run `apd.py spec` on it.

### 4 — CLI exercise

**You are building:** a verified checklist and a matrix.
**Tool:** Claude Code. **Level:** intermediate.

Setup: `scratch/checklist.csv` from exercise 3 (or any spec checklist).

```
Read AGENTS.md. Run python3 project/tools/apd.py spec project/samples/spec-excerpt-synthetic.md scratch/checklist.csv and show me the output. For each flagged row, quote the row and tell me which kind of problem it is (NO-QUOTE, NOT-IN-SPEC, WRONG-SECTION). Do not fix any row yet. Then create scratch/matrix.csv with the columns id, requirement, section, quote, comply_where, evidence, deviation, copying only the rows that passed the checker, with the last three columns empty. List the headings in the spec that have no row in the matrix. Do not edit the spec, the sample checklist, or the tool. Tell me exactly what the checker can and cannot prove.
```

**Expected:** a flagged-rows report, a `matrix.csv` of only verified rows, and a list of unrepresented headings.
**Inspect:** for three passed rows, read the quote in the spec: does it support the paraphrase? For the unrepresented headings, decide if each is a real gap.
**If it goes wrong:** the agent may offer to "fix" flagged rows by rewriting the quote to match the spec. That is allowed only if the *requirement* is genuinely in the spec; if it was invented, delete the row. Read each fix.
**Standing rule:** *"A requirement without a verbatim quote and a section number does not go in a checklist."*

### 5 — AI validation exercise

**You are validating:** the AI draft `spec-checklist-ai.csv` and your own exercise 3 output.
**Type:** factual claim. **Risk:** high.

```
□ Correctness: for each row the checker passed, does the quote actually support the requirement as paraphrased?
   (Look hard at R4 and R8.)
□ Completeness: which "shall" sentences in the spec have no row?
□ Scope: did the AI add requirements from "typical practice" that are not in the document?
□ Softening: is any "only", "all", "each", or number missing from a paraphrase?
□ Section check: do the cited sections match the headings in the document?
□ Failure mode check: invented requirement (R7), misattributed section (R9), no source (R10),
   plausible paraphrase that shifts meaning.
```

**AI Use Disclosure** (two sentences).

---

## Done when

- You can explain what the checker proves and does not prove.
- Your own checklist passes `apd.py spec`, and you have listed the requirements it missed.
- You have a draft submittal matrix with honest blanks.
