# AR-0001: agent run of lab 09 (ezdxf drawing edits)

## Executive summary

A record of an AI agent (Claude) running `labs/09-drawing-edits-ezdxf.md` end to end on 2026-10-25, written so JP's run can be compared with it and so any film of this lab is made from what really happened. It found that the lab's commands do what the lab says on a synthetic DXF. It did **not** open any file in DraftSight or AutoCAD, and no human expert has reviewed the lab. Status: awaiting JP.

## Environment

- macOS arm64, Python 3.14.6, ezdxf 1.4.5 (fonttools 4.67.0, numpy 2.5.4, pyparsing 3.3.3, typing_extensions 4.16.0) in `.toolchain/venv-dxf`.
- Repository at commit `1f296d9` plus the uncommitted lab 09 files.
- Fixture: `labs/dxf/station-a.dxf`, SHA-256 `1eee76c72fd93eb20fcb9e84cfd15101c070b8abfdc6aeb8fd0bf0a4afd9b863`, unchanged after every command below.

## What was run and what happened

| Step | Command (abridged) | Result |
|---|---|---|
| Tests | `.toolchain/venv-dxf/bin/python -m unittest discover -s project/tests -p test_dxf.py` | 11 tests OK. Under system python3 (no ezdxf) the same tests skip |
| 1 | `apd.py dxf extract` then `apd.py crosscheck` | 3 findings: P2_OL1 missing on drawing; P3_K1 not in design; rating mismatch on P1_K1 (10 HP vs 7.5 HP) |
| 2 | `dxf replace "7.5 HP" "10 HP"` (plan) | 5 planned changes (2 attributes, 2 TEXT, 1 MTEXT), nothing written. "CABLE LENGTH 7.5 FT" untouched |
| 2b | same with `--exclude-layer REV-HISTORY` | 4 planned changes |
| 3 | same with `--apply --out scratch/station-a-10hp.dxf` | 4 changes applied; tool printed "verified: reloaded output; only the planned text differs"; audit log written |
| 3b | `--out` set to the input file | refused: "--out is the input file" |
| 3c | `--out` set to the existing output | refused: "already exists" |
| 4 | `dxf title ... --block NO_SUCH_BLOCK` | "no block named NO_SUCH_BLOCK found", 0 changes (not silent) |
| 4 | `dxf renumber --layer WIRES` (plan) | 5 relabels in top-to-bottom, left-to-right order; "WIRE NOTE" skipped |

The 5-change plan without the exclusion was: two device-description attributes (P2_K1, P3_K1), the pump note (TEXT), the revision-history line (TEXT) and the motor-data note (MTEXT). The plan changed P3_K1 as well because the fixture's extra device carries 7.5 HP in its description.

## Not run

DraftSight and AutoCAD (none installed); the AutoLISP route of Module 4; DWG files; any real drawing; Windows or Linux; a human reading the output. The lab's section 6 (comparing with AutoLISP) is for a person with DraftSight.

## Questions for JP

1. Does the edited DXF open in DraftSight with the title block and notes looking right?
2. Is rewriting the revision-history line ever right in your shop? The lab says the tool should not decide.
3. Would you number wires top-to-bottom, left-to-right, or by some other rule?
4. Does DraftSight's own attribute extraction give the same device list as `dxf extract`?
5. What on a real sheet would this tool miss (symbols drawn as blocks with text inside, xrefs, text in other layouts)?
