import sys, unittest
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
import design


class TestDesign(unittest.TestCase):
    def v(self, n):
        return design.load_toml(HERE / "variants" / f"{n}.toml")

    def test_baseline_has_no_errors(self):
        errs = [f for f in design.check_variant(self.v("a-baseline")) if f.level == "ERROR"]
        self.assertEqual(errs, [])

    def test_vfd_variant_has_no_errors(self):
        errs = [f for f in design.check_variant(self.v("b-vfd-transducer")) if f.level == "ERROR"]
        self.assertEqual(errs, [])

    def test_invalid_variant_is_caught(self):
        rules = {f.rule for f in design.check_variant(self.v("c-invalid")) if f.level == "ERROR"}
        self.assertTrue({"R05-fla", "R06-analog-needs-controller", "R09-alarm-pump", "R10-high-level"} <= rules)

    def test_io_tags_unique(self):
        for n in ("a-baseline", "b-vfd-transducer"):
            tags = [r["tag"] for r in design.build_io(self.v(n))]
            self.assertEqual(len(tags), len(set(tags)))

    def test_bom_covers_every_device(self):
        v = self.v("a-baseline")
        tags = {t for r in design.build_bom(v) for t in r["tags"].split()}
        self.assertEqual(tags, {d.tag for d in design.build_devices(v)})

    def test_sizing_uses_table(self):
        tables, _ = design.load_tables()
        sz = design.size_motor_circuit(self.v("a-baseline"), tables)
        self.assertEqual(sz["fla"], 11.0)
        self.assertEqual(sz["awg"], "14")  # 11 A * 1.25 = 13.75 A needs 20 A column

    def test_banner_matches_verification_state(self):
        tables, _ = design.load_tables()
        verified = bool(tables["meta"].get("verified"))
        self.assertEqual(bool(design.unverified_banner(tables)), not verified)
        if verified:  # a signature needs a name, a date and an edition
            for k in ("verified_by", "verified_date", "edition_checked"):
                self.assertTrue(tables["meta"].get(k), f"verified = true but {k} is empty")


if __name__ == "__main__":
    unittest.main()
