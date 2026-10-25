import json, subprocess, sys, tempfile, unittest
from pathlib import Path

GUARD = Path(__file__).resolve().parent.parent.parent / "scripts" / "guard.py"


def run_guard(path):
    p = subprocess.run([sys.executable, str(GUARD)], input=json.dumps({"tool_input": {"file_path": str(path)}}),
                       capture_output=True, text=True)
    return p.returncode, p.stderr


class TestGuard(unittest.TestCase):
    def test_blocks_verified_table_and_allows_unverified(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "nec-extracts.toml"
            f.write_text("[meta]\nverified = true\n")
            code, err = run_guard(f)
            self.assertEqual(code, 2)
            self.assertIn("BLOCKED", err)
            f.write_text("[meta]\nverified = false\n")
            self.assertEqual(run_guard(f)[0], 0)

    def test_ignores_other_files(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "notes.md"
            f.write_text("verified = true\n")
            self.assertEqual(run_guard(f)[0], 0)

    def test_survives_garbage_input(self):
        p = subprocess.run([sys.executable, str(GUARD)], input="not json", capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)


if __name__ == "__main__":
    unittest.main()
