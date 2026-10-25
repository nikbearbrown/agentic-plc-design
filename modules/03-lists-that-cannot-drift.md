# Module 03 — Lists that cannot drift

## Executive summary

**What you do:** generate the device list, I/O list and bill of materials from a variant file, then cross-check them against what is actually on a drawing set. You learn to make a spreadsheet-shaped checker.

**Why:** most panel errors are two lists that disagree: the BOM says 7.5 HP, the drawing says 10 HP; a device on the schematic that never reached the order. When every list is derived from one source, drift becomes impossible, and the leftover risk is the one place a human still types: the drawing. That is where the cross-check earns its keep.

**What you leave with:** the commands to produce an I/O list and a BOM from a variant, a drawing-extract workflow, and a cross-check report that finds planted discrepancies. Time: about 4 hours.

---

## The idea

`project/tools/design.py` builds one thing first: a **device list** (every tag the station needs, with a catalog part and a reason). The I/O list and the BOM are views of it.

```bash
python3 project/tools/apd.py devices project/variants/a-baseline.toml
python3 project/tools/apd.py io project/variants/a-baseline.toml
python3 project/tools/apd.py bom project/variants/a-baseline.toml
```

Look at the BOM's `basis` column. It says *why* each line is what it is ("smallest contactor ≥ 11 A"). A number with no stated basis is a number you cannot audit; every generated number here has one.

**Two honesty points.**

- The catalog (`project/data/catalog.toml`) uses invented part numbers (`GEN-...`). Replace it with your shop's real catalog in the CLI exercise; that is where this tool becomes yours.
- The BOM prints a banner while the reference tables are unverified. That banner is a feature (Module 7).

### The drawing side

The tools cannot read your DraftSight files. What they *can* read is a **tag list extracted from the drawing**: a CSV with a `tag` column and a `description` column. Drawing programs have a data/attribute extraction function that writes this from the attributes on your symbols. The exact command name and menu differ by product and version; look in your program's help for "attribute extraction" or "data extraction," or ask your agent to search its documentation. The point is the *shape* of the output, not the menu path.

`project/samples/drawing-extract-a.csv` is a synthetic extract for variant A with three planted problems.

```bash
python3 project/tools/apd.py crosscheck project/variants/a-baseline.toml project/samples/drawing-extract-a.csv
```

The report has three kinds of finding: **MISSING-ON-DRAWING** (the design needs it, the drawing lacks it), **NOT-IN-DESIGN** (the drawing has it, the design does not), **RATING-MISMATCH** (same tag, different numbers).

---

## Lab

### Step 1 — Generate and read

Generate the device list, I/O list and BOM for variants A and B. For each, answer on paper: How many digital inputs? How many outputs? How many PLC cards does B need and why? Which lines in the BOM change between A and B, and which do not? (That difference *is* the 10 percent.)

### Step 2 — Find the planted errors yourself first

Open `project/samples/drawing-extract-a.csv` and the device list for variant A side by side. Find the discrepancies by eye. Count them and time yourself. Then run the cross-check. Compare. Note which kind you missed.

### Step 3 — Round-trip through Excel

Save the I/O list as a CSV and open it in Excel:

```bash
python3 project/tools/apd.py io project/variants/a-baseline.toml > scratch/io-a.csv
```

Open `scratch/io-a.csv` in Excel. Add a column. Sort by `type`. This is the file you would hand a programmer or a technician. Note: **edits made in Excel do not flow back** to the variant. The variant file is the source; the spreadsheet is a printout. If someone fixes the spreadsheet, the fix is lost the next time you regenerate. Decide as a team where fixes get made. (The answer is almost always "in the variant," and a rule that says so belongs in your instruction file.)

### Step 4 — Make it yours

Replace the invented catalog with a handful of lines from your shop's real parts. Do not paste your entire catalog into a chat. Do it in `scratch/my-catalog.toml` using the same shape as `project/data/catalog.toml`, then point the agent at it in the CLI exercise.

---

## Five-part exercise

### 1 — When to use AI

- **Building a lookup (device to part number) from a spreadsheet you give it** — *why it works:* mechanical transformation; you can spot-check rows against the source.
- **Writing a cross-check between two CSV files** — *why it works:* the output is a list of specific differences you can verify one by one.
- **Producing a clean BOM layout for a customer** — *why it works:* formatting, with the numbers coming from the tool, not from the AI.

**The tell:** every number in the output comes from a file or a tool, not from the AI's memory.

### 2 — When NOT to use AI

- **Choosing the actual component for a duty** (a contactor for a pump motor starting under load). *Why it fails:* selection depends on the manufacturer's HP rating at your voltage, the duty, the available fault current and your standards.
- **Filling in missing part numbers from memory.** *Why it fails:* a plausible-looking part number that does not exist is the textbook hallucination.
- **Deciding the drawing is right because the lists match.** *Why it fails:* a cross-check finds disagreement, not error. Two wrong lists can agree.

**The tell:** you are about to order a part the AI named but a catalog or a vendor never confirmed.

**Series tier:** *Tier 4, metacognitive supervision* — distrust of derived output that merely looks complete.

### 3 — LLM exercise

**You are building:** a plan for extracting a tag list from your own drawings.
**Tool:** Claude chat.

```
I use DraftSight to edit electrical control panel schematics. My symbols carry attributes: a TAG (like P1_K1) and a DESCRIPTION (like "Pump 1 contactor, 7.5 HP, 460 V"). I want to export a CSV with exactly two columns, tag and description, one row per symbol, from a drawing set, so a script can compare it to a design. I do not know DraftSight's exact feature names. Tell me what DraftSight's attribute or data extraction capability is likely called and where it is likely found, say how sure you are of each statement on a scale of high/medium/low, and give me a short checklist to verify the output CSV is complete (including the three ways extraction typically misses things: attributes on nested blocks, tags typed as plain text rather than attributes, and symbols drawn on frozen or off layers). Also tell me what I should look up in DraftSight's own help to confirm each point. Do not tell me a menu path as fact unless you are certain.
```

**Adapt it:** use your CAD program's name if different; add what your symbols actually carry.

**Produces:** a list of things to look up. Treat every menu path as a hypothesis until you see it on your screen.

### 4 — CLI exercise

**You are building:** a BOM drawn from your shop's real parts.
**Tool:** Claude Code. **Level:** intermediate.

Setup: `scratch/my-catalog.toml` exists with at least a dozen real lines in the same shape as `project/data/catalog.toml` (a `[meta]` table with `verified = false`, `[[contactor]]` rows with `part` and `amps`, and a `[fixed]` table).

```
Read AGENTS.md. Read scratch/my-catalog.toml and project/data/catalog.toml. The BOM tool accepts a catalog path in the APD_CATALOG environment variable (see load_tables in project/tools/design.py). Run: APD_CATALOG=scratch/my-catalog.toml python3 project/tools/apd.py bom project/variants/a-baseline.toml and show me the output. Then list every BOM line whose part still starts with GEN- (meaning my catalog did not cover it). Do not guess any part numbers; for each uncovered line, write "NEEDS PART: <description>". Do not modify any tracked file. Report the exact output.
```

**Expected:** a BOM where covered lines show your parts and the rest say `NEEDS PART`.
**Inspect:** `git status` shows no tracked file changed. Cross-check three part numbers against your own catalog by hand. Did the agent copy them exactly?
**If it goes wrong:** if you see a part number that is not in your file, the agent made one up. That is the single most important failure to catch. Re-run with "Every part number must be copied character-for-character from my-catalog.toml; if absent, write NEEDS PART."
**Note:** if your catalog uses different table names than the default, the tool will fail with a clear error; fix the catalog, not the tool.
**Standing rule:** *"Never write a part number that is not in a file I gave you."*

### 5 — AI validation exercise

**You are validating:** the BOM from exercise 4, and a cross-check report.
**Type:** structured data. **Risk:** high — an order is placed from a BOM.

```
□ Correctness: spot-check 5 BOM lines against your catalog. Part number, description, quantity.
□ Completeness: does the BOM include the IS barriers for a hazardous well? A beacon?
   Terminal blocks, wire, enclosure, and panel hardware are NOT in the generated BOM (the tool does not
   know them). List what else you would add. A BOM that looks complete is not.
□ Scope: git status clean for tracked files?
□ Basis check: pick the contactor. The basis says "smallest contactor >= 11 A".
   Is that how YOU size a contactor for a pump motor? (It is a simplification on purpose; Module 7.)
□ Failure mode check: invented part number (a part that is not in either catalog);
   silent default (a line that silently fell back to GEN- instead of being flagged).
```

**AI Use Disclosure** (two sentences).

---

## Done when

- You can produce an I/O list and BOM from any valid variant and explain each line's basis.
- You found the three planted discrepancies by eye or by tool and know which kind you tend to miss.
- You have a real-parts catalog fragment in `scratch/` and a BOM that flags what is not covered instead of guessing.
