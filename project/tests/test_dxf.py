"""Tests for dxf_edit.py. Run with the isolated interpreter that has ezdxf:
   .toolchain/venv-dxf/bin/python -m unittest discover -s project/tests -p test_dxf.py
Skipped (not failed) under an interpreter without ezdxf, so ./check.sh stays green on a fresh clone."""
import csv, hashlib, io, json, shutil, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "project" / "tools"))
try:
    import ezdxf
    import dxf_edit
except SystemExit:  # dxf_edit exits when ezdxf is missing
    ezdxf = None
except ImportError:
    ezdxf = None
import design

FIXTURE = ROOT / "labs" / "dxf" / "station-a.dxf"
VARIANT = ROOT / "project" / "variants" / "a-baseline.toml"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


@unittest.skipUnless(ezdxf, "ezdxf not installed in this interpreter (python3 scripts/dxf_setup.py --apply)")
class TestDxfEdit(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.doc = ezdxf.readfile(FIXTURE)

    def texts(self, path):
        return {s.handle: s.text for s in dxf_edit.slots(ezdxf.readfile(path))}

    def test_plan_changes_nothing_on_disk(self):
        before = sha(FIXTURE)
        plan, _ = dxf_edit.plan_replace(self.doc, "7.5 HP", "10 HP")
        self.assertTrue(plan)
        self.assertEqual(sha(FIXTURE), before)

    def test_replace_hits_text_mtext_and_attrib_but_not_cable_length(self):
        plan, _ = dxf_edit.plan_replace(self.doc, "7.5 HP", "10 HP")
        kinds = {c["kind"] for c in plan}
        self.assertEqual(kinds, {"TEXT", "MTEXT", "ATTRIB"})
        self.assertFalse(any("CABLE LENGTH" in c["old"] for c in plan))  # "7.5 FT" is not a rating

    def test_exclude_layer_protects_revision_history(self):
        plan, _ = dxf_edit.plan_replace(self.doc, "7.5 HP", "10 HP", exclude_layers=["REV-HISTORY"])
        self.assertFalse(any(c["layer"] == "REV-HISTORY" for c in plan))
        full, _ = dxf_edit.plan_replace(self.doc, "7.5 HP", "10 HP")
        self.assertEqual(len(full) - len(plan), 1)

    def test_apply_writes_new_file_original_untouched_and_verified(self):
        before = sha(FIXTURE)
        plan, _ = dxf_edit.plan_replace(self.doc, "7.5 HP", "10 HP", ["REV-HISTORY"])
        out = self.tmp / "out.dxf"
        self.assertEqual(dxf_edit.apply_plan(FIXTURE, out, plan), [])
        self.assertEqual(sha(FIXTURE), before)
        new, old = self.texts(out), self.texts(FIXTURE)
        changed = {h for h in new if new[h] != old[h]}
        self.assertEqual(changed, {c["handle"] for c in plan})
        log = json.loads(Path(str(out) + ".changes.json").read_text())
        self.assertEqual(len(log["changes"]), len(plan))

    def test_refuses_to_overwrite_input_or_existing_file(self):
        plan, _ = dxf_edit.plan_replace(self.doc, "7.5 HP", "10 HP")
        with self.assertRaises(SystemExit):
            dxf_edit.apply_plan(FIXTURE, FIXTURE, plan)
        existing = self.tmp / "exists.dxf"
        existing.write_text("x")
        with self.assertRaises(SystemExit):
            dxf_edit.apply_plan(FIXTURE, existing, plan)
        self.assertEqual(existing.read_text(), "x")

    def test_verify_catches_an_unplanned_change(self):
        plan, _ = dxf_edit.plan_replace(self.doc, "7.5 HP", "10 HP")
        out = self.tmp / "out.dxf"
        dxf_edit.apply_plan(FIXTURE, out, plan)
        doc = ezdxf.readfile(out)
        victim = next(s for s in dxf_edit.slots(doc) if s.text == "W014")
        victim.text = "W999"  # tamper with something the plan never touched
        doc.saveas(out)
        problems = dxf_edit.verify(FIXTURE, out, plan)
        self.assertTrue(any("W999" in p for p in problems))

    def test_title_block_filled_from_variant(self):
        plan, notes = dxf_edit.plan_title(self.doc, design.load_toml(VARIANT))
        self.assertEqual(notes, [])
        new = {c["new"] for c in plan}
        self.assertEqual(new, {"Demo Lift Station A", "DEMO-0001", "A", "460V 3PH 60HZ", "7.5 HP"})

    def test_title_block_missing_name_is_reported_not_silent(self):
        plan, notes = dxf_edit.plan_title(self.doc, design.load_toml(VARIANT), block="NO_SUCH_BLOCK")
        self.assertEqual(plan, [])
        self.assertTrue(notes)

    def test_renumber_is_ordered_and_skips_non_wires(self):
        plan, _ = dxf_edit.plan_renumber(self.doc, "WIRES", "W", 1)
        self.assertEqual([(c["old"], c["new"]) for c in plan],
                         [("W014", "W001"), ("W003", "W002"), ("W009", "W003"), ("W001", "W004"), ("W020", "W005")])
        self.assertEqual(plan, dxf_edit.plan_renumber(ezdxf.readfile(FIXTURE), "WIRES", "W", 1)[0])  # repeatable

    def test_extract_feeds_crosscheck_with_the_same_three_findings(self):
        import crosscheck
        rows = dxf_edit.extract(self.doc)
        res = crosscheck.crosscheck(design.load_toml(VARIANT), rows)
        self.assertEqual(len(res), 3)
        self.assertTrue(any(r.startswith("MISSING-ON-DRAWING  P2_OL1") for r in res))
        self.assertTrue(any(r.startswith("NOT-IN-DESIGN       P3_K1") for r in res))
        self.assertTrue(any("RATING-MISMATCH     P1_K1" in r for r in res))

    def test_blocks_definitions_are_never_edited(self):
        plan, _ = dxf_edit.plan_replace(self.doc, "UNSET", "X")  # ATTDEF default text lives in the block definition
        self.assertEqual(plan, [])


if __name__ == "__main__":
    unittest.main()
