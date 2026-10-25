# Module 04 — Drawing edits by script

## Executive summary

**What you do:** use an AI agent to produce a small AutoLISP script that fills in a title block and swaps a pump rating across a drawing, run it safely on a *copy* in dry-run mode, read the log it prints, and then judge a risky script an AI wrote without those safeguards.

**Why:** editing existing drawings for a system that is 90 percent already designed is the most automatable task in a design office. Scripting is how the person doing the editing becomes the person who owns the automation. The danger is that a script runs against every object in a drawing in a second, so a wrong one does a day's damage instantly. The safe pattern (dry run, copy, lint, log) is the skill.

**What you leave with:** the dry-run/apply pattern, a script generated from a variant, a linter that rejects dangerous scripts, and the habit of never running AI-written drawing code unread. Time: about 4 hours. **Gate G3 lives here:** only you can sign it, after running on a copy in your own CAD program.

---

> **Agent-runnable twin.** If you do not have DraftSight, or want an AI agent to run and prove these edits itself, do [Lab 09: drawing edits with ezdxf](../labs/09-drawing-edits-ezdxf.md). It uses the same plan-then-copy safety pattern in open-source Python on a synthetic DXF. It does not replace running the AutoLISP route in your own CAD program (Gate G3).

## The idea

AutoLISP is the scripting language built into AutoCAD decades ago; many AutoCAD-compatible programs, including DraftSight in its Professional edition (check your own edition and version), run it. Because it is old, public, and everywhere, AI agents write it well *in the common cases* and badly in the unusual ones.

A script is just text. The design here keeps it dull and safe:

1. **Plain AutoLISP only.** No ActiveX/COM calls, no file deletion, no shelling out, no `command` calls that can erase or purge.
2. **Dry run by default.** Nothing changes unless a flag is on. The script prints "this attribute 'A' would become 'B'."
3. **Every write is guarded** by `(if *APD-APPLY* ...)`. A linter (`project/tools/lisp_lint.py`) refuses scripts with an unguarded write.
4. **Generated, not hand-edited.** `lisp_gen.py` writes the job-specific script from the variant, so the title block always matches the design.

The library `project/lisp/apd-lib.lsp` holds the helpers (set an attribute, replace text). It was written by an AI and checked only by a linter. **It has never been run in a CAD program by its author.** That is why the gate is yours.

---

## Lab

### Step 1 — Read the library

Open `project/lisp/apd-lib.lsp`. You do not need to read LISP. Read the comments and the `apd-log` lines. Note the one global switch, `*APD-APPLY*`, and that it starts as `nil` (off).

### Step 2 — Generate a job script and lint it

```bash
python3 project/tools/apd.py lisp project/variants/a-baseline.toml --swap "7.5 HP=10 HP" > scratch/apd-job-a.lsp
python3 project/tools/apd.py lint project/lisp/apd-lib.lsp scratch/apd-job-a.lsp
```

If your title block is not called `TITLEBLOCK` or your attributes have different names, add `--block YOUR_BLOCK_NAME` and `--tag job_name=YOUR_TAG` (repeat for `job_number`, `revision`, `voltage`, `pump_hp`). Add `--lib "C:/full/path/apd-lib.lsp"` if the loader cannot find the library by name. Look inside your own title block to learn the real block name and attribute tags.

### Step 3 — Make a copy of a drawing

**Never run a script on the original.** Copy a drawing you have permission to use, or a sample drawing you made. Name the copy `COPY-do-not-use.dwg`. Open the copy.

### Step 4 — Load and dry-run

In DraftSight, load a LISP file from the Tools or Application menu, or with the `APPLOAD` command (confirm in your DraftSight help; names differ by version). Load `apd-lib.lsp`, then your job script, then type:

```
APD-DRYRUN
```

Read the command-line log. Does it find your title block? Does it list the attributes it would change, with old and new values? Does it list text objects that would change? Are there any you did not expect?

If nothing happens or you see an error, write down the **exact** message. Do not retry blindly. This is the moment a real person learns whether the author's assumptions about your CAD program hold.

### Step 5 — Apply, check, undo

Only if the dry run matched your expectations, type `APD-APPLY`. Inspect the title block and the changed text. Then type `U` (undo) and confirm the drawing returns. A script you cannot undo is a script you do not run.

### Step 6 — Review a risky script

Read `project/samples/ai-written-risky.lsp.txt`. It is what an AI wrote when asked for "a script to update the drawing for a 10 HP pump." **Do not run it.** Run the linter on it:

```bash
python3 project/tools/apd.py lint project/samples/ai-written-risky.lsp.txt
```

Before reading the linter's verdict, list for yourself what each line would do to a real drawing. Then compare.

---

## Five-part exercise

### 1 — When to use AI

- **Writing a first version of a script that edits attributes or text** — *why it works:* narrow, well-documented, and the dry-run log shows what it would do.
- **Explaining what an unfamiliar LISP file does, line by line** — *why it works:* you can test the explanation against the dry-run log.
- **Adding a new helper (renumber wires, swap a symbol) to the library** — *why it works:* new code goes through the same lint and dry-run gates.

**The tell:** you read the dry-run log and recognize every line.

### 2 — When NOT to use AI

- **Running an AI-written script on an original drawing.** *Why it fails:* irreversible damage is possible; there is no ground truth for what the script does until it has run on a copy.
- **Choosing which text to replace.** `7.5 HP` may appear in a note, a nameplate schedule and a title block, and a different "7.5" may be a wire length. *Why it fails:* meaning depends on the drawing; only you know which hits are real.
- **Signing the script as correct because the lint passes.** *Why it fails:* lint finds known-dangerous patterns, not wrong behaviour.

**The tell:** you ran it because it "looked fine."

**Series tier:** *Tier 4*, supervision, and *Tier 7*, wisdom about when speed is not worth the risk.

### 3 — LLM exercise

**You are building:** a second helper function in plain AutoLISP.
**Tool:** Claude chat.

```
Write ONE AutoLISP function named apd-renumber-wires for DraftSight Professional. It must use plain AutoLISP only: ssget, entget, entmod, assoc, subst, strcat, itoa, while, setq. It must NOT use the command function, vlax or any ActiveX call, entdel, file functions or startapp. It takes a string prefix, a starting integer, and a layer name. It finds all single-line TEXT objects on that layer whose content is exactly 'W###' (the letter W followed by digits), and replaces their content with the prefix followed by the next number, in the order they come back from the selection set. It must be DRY-RUN by default: it only prints "old -> new" with (princ) unless the global variable *APD-APPLY* is T, and every entmod must be written exactly as (if *APD-APPLY* (entmod ...)). Return the count of text objects it would change or changed. Before the code, state three assumptions you are making about DraftSight's LISP support that I should verify, and after the code, list two ways it could do the wrong thing on a real drawing. Do not claim it has been tested.
```

**Adapt it:** replace the pattern `W###` with your wire-number convention. Paste only the function into `scratch/`, not into the library, until it has passed the lint and a dry run.

**Produces:** a function and an honest list of assumptions.

### 4 — CLI exercise

**You are building:** a script generated for your own title block, plus a lint-gated workflow.
**Tool:** Claude Code. **Level:** intermediate.

Setup: write `scratch/my-titleblock.txt` yourself, with your title block's real block name and attribute tags (open a drawing, select the title block, look at its attributes), one `field=value` per line.

```
Read AGENTS.md. Read scratch/my-titleblock.txt, which lists my title block's block name and attribute tags, one per line, such as block=TB_ELEC and job_name=PROJ_TITLE. Use project/tools/lisp_gen.py to generate an AutoLISP job script for project/variants/a-baseline.toml using exactly those values (--block for the block name, one --tag option per mapping line). Write the output to scratch/apd-job-mine.lsp. Then run python3 project/tools/apd.py lint on project/lisp/apd-lib.lsp and scratch/apd-job-mine.lsp and show me the output. Do not edit apd-lib.lsp or lisp_gen.py. Do not run anything that opens a CAD program. If lint fails, show me the failure and stop. Then tell me which parts of this you ran and which you only wrote.
```

**Expected:** `scratch/apd-job-mine.lsp`, a lint `OK`, and an honest "I did not run it in DraftSight."
**Inspect:** open the file. Is your block name there? Your tags? Search for the words `command`, `delete`, `entdel` yourself (the linter does too, but you should know what you are looking for).
**If it goes wrong:** if the agent changes the library to make lint pass, reject it: `git restore project/lisp`. If lint fails on your generated script, that is a bug in the generator; report it, do not patch around it.
**Standing rule:** *"Never run a script on an original drawing. Dry run on a copy."*

### 5 — AI validation exercise

**You are validating:** the risky script in `project/samples/ai-written-risky.lsp.txt` **and** your dry-run log.
**Type:** code / agentic output. **Risk:** high — drawings are deliverables.

```
□ Correctness: in the risky script, what does each line do to a real drawing?
   (purge, erase every TEXT, then edit one object repeatedly.)
□ Completeness: what does it fail to do that the request asked for ("update the drawing for a 10 HP pump")?
□ Scope: how many objects does it touch that it was never asked to touch?
□ Reversibility: could you recover from running it? How?
□ Dry-run check (your script): did the dry-run log list every change you expected and nothing else?
□ Failure mode check: destructive default (acts without asking), silent scope creep
   (changes more than requested), no preview, no log, unreadable by a human reviewer.
```

**AI Use Disclosure** (two sentences).

---

## Done when

- You have a linted job script for your title block, and you ran its dry run on a copy and understood the log.
- You can say what each dangerous line in the risky sample would have done.
- You recorded what worked and failed in your CAD program in `scratch/g3-notes.md`.

## Gate G3

Sign G3 in `STATUS.md` **only** if you ran `APD-DRYRUN` and `APD-APPLY` on a copy and both behaved as described, and you recorded the DraftSight version. If something failed, record the exact error and what you changed. Do not sign on the strength of a lint.
