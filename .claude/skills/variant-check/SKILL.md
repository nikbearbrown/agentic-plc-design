---
name: variant-check
description: Check a lift-station variant file against the course rules and derive its I/O list, BOM and cross-checks. Use when the user edits or asks about anything in project/variants/, or asks whether a station design is consistent.
---

# variant-check

Run from the repo root. Read-only: this skill never edits a variant, a table or a drawing.

1. `python3 project/tools/apd.py check project/variants/<file>.toml`. Report every ERROR and WARN exactly as printed. Do not soften them.
2. If there are no ERRORs, run `apd.py io` and `apd.py bom` on the same file and report the point counts and the BOM line count.
3. If the BOM output starts with `UNVERIFIED REFERENCE TABLES`, say so first, in the first sentence of your reply. A BOM from unverified tables is a draft.
4. If the user supplied a drawing extract CSV, run `apd.py crosscheck` and list each discrepancy with its tag.
5. Stop. Never fix a variant to make a rule pass. Say which rule failed and why a designer might disagree with the rule; the human decides whether the variant or the rule is wrong.
