import csv, sys, unittest
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
import crosscheck, design, l5x_check, lisp_gen, lisp_lint, log_summary, spec_check, vectors


class TestLisp(unittest.TestCase):
    def test_library_and_generated_job_pass_lint(self):
        self.assertEqual(lisp_lint.lint((HERE / "lisp" / "apd-lib.lsp").read_text()), [])
        job = lisp_gen.generate(design.load_toml(HERE / "variants" / "a-baseline.toml"), swaps=[("7.5 HP", "10 HP")])
        self.assertEqual(lisp_lint.lint(job), [])
        self.assertIn("DEMO-0001", job)

    def test_risky_script_is_rejected(self):
        probs = lisp_lint.lint((HERE / "samples" / "ai-written-risky.lsp.txt").read_text())
        self.assertTrue(any("command" in p for p in probs))
        self.assertTrue(any("not guarded" in p for p in probs))

    def test_unbalanced_parens(self):
        self.assertTrue(lisp_lint.lint("(defun c:x () (princ)"))

    def test_quotes_in_values_are_escaped(self):
        v = design.load_toml(HERE / "variants" / "a-baseline.toml")
        v["job"]["name"] = 'Bad "name" \\ here'
        self.assertEqual(lisp_lint.lint(lisp_gen.generate(v)), [])


class TestCheckers(unittest.TestCase):
    def test_crosscheck_finds_planted_discrepancies(self):
        v = design.load_toml(HERE / "variants" / "a-baseline.toml")
        rows = list(csv.DictReader(open(HERE / "samples" / "drawing-extract-a.csv")))
        res = crosscheck.crosscheck(v, rows)
        self.assertEqual(len(res), 3)
        self.assertTrue(any(r.startswith("MISSING-ON-DRAWING  P2_OL1") for r in res))
        self.assertTrue(any(r.startswith("NOT-IN-DESIGN       P3_K1") for r in res))
        self.assertTrue(any("RATING-MISMATCH     P1_K1" in r for r in res))

    def test_spec_check_catches_hallucination(self):
        spec = (HERE / "samples" / "spec-excerpt-synthetic.md").read_text()
        rows = list(csv.DictReader(open(HERE / "samples" / "spec-checklist-ai.csv")))
        res = spec_check.check(spec, rows)
        ids = {r.split()[1].rstrip(":") for r in res}
        self.assertEqual(ids, {"R7", "R9", "R10"})

    def test_l5x_finds_double_coil_and_undefined(self):
        defined, rungs = l5x_check.read_l5x(HERE / "samples" / "synthetic.L5X")
        io = [r["tag"] for r in design.build_io(design.load_toml(HERE / "variants" / "a-baseline.toml"))]
        res = l5x_check.analyse(defined, rungs, io)
        self.assertTrue(any(r.startswith("DOUBLE-COIL") and "P2_RUN_CMD" in r for r in res))
        self.assertTrue(any(r.startswith("UNDEFINED-TAG") and "HIGH_LEVEL_ALM" in r for r in res))

    def test_log_summary_numbers(self):
        rows = list(csv.DictReader(open(HERE / "samples" / "station-log-synthetic.csv")))
        text = "\n".join(log_summary.summarise(log_summary.parse(rows)))
        self.assertIn("P1_RUN_FB: 13 runs", text)
        self.assertIn("6 short cycles", text)
        self.assertIn("P2_SEAL_FAIL: raised 1x", text)


class TestVectors(unittest.TestCase):
    def test_vectors_cover_all_scenarios_and_are_stable(self):
        rows = vectors.generate()
        self.assertEqual({r["scenario"][:3] for r in rows}, {f"T0{i}" for i in range(1, 9)})
        self.assertEqual(rows, vectors.generate())


if __name__ == "__main__":
    unittest.main()
