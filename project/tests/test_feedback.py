import importlib.util, subprocess, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
spec = importlib.util.spec_from_file_location("feedback", ROOT / "scripts" / "feedback.py")
fb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fb)

HEAD = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()


def entry(**over):
    meta = dict(id="FB-0001", date="2026-10-26", lab="lab-09", section="3", reporter="JP", kind="wrong",
                severity="major", status="open", decided_by="", tutorial_commit="", tutorial_files="")
    meta.update(over)
    body = over.pop("_body", None)
    front = "\n".join(f"{k}: {v}" for k, v in meta.items() if not k.startswith("_"))
    sections = {"What was done": "Ran step 3 on Windows.", "What JP said, verbatim": "that is not how we number wires",
                "What the tutorial or agent had claimed": "labs/09 line 40", "Decision": "Open.", "Change": "None yet."}
    if body:
        sections.update(body)
    return f"---\n{front}\n---\n\n" + "\n\n".join(f"## {k}\n\n{v}" for k, v in sections.items()) + "\n"


class TestFeedback(unittest.TestCase):
    def check(self, text, name="FB-0001.md", git=False):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / name).write_text(text)
            return fb.validate(Path(d), check_git=git)

    def test_valid_open_entry_passes(self):
        self.assertEqual(self.check(entry()), [])

    def test_template_placeholder_is_rejected(self):
        t = entry(_body={"What JP said, verbatim": "(JP's words go here exactly as he said them)"})
        self.assertTrue(any("placeholder" in p for p in self.check(t)))

    def test_decided_entry_needs_a_named_human(self):
        self.assertTrue(any("decided_by" in p for p in self.check(entry(status="accepted"))))
        self.assertEqual(self.check(entry(status="accepted", decided_by="Bear")), [])

    def test_fixed_needs_a_real_commit_and_real_files(self):
        base = dict(status="fixed", decided_by="Bear")
        self.assertTrue(any("tutorial_commit" in p for p in self.check(entry(**base))))
        bad = entry(**base, tutorial_commit="0000000000000000000000000000000000000000", tutorial_files="labs/09-drawing-edits-ezdxf.md")
        self.assertTrue(any("not a commit" in p for p in self.check(bad, git=True)))
        nofile = entry(**base, tutorial_commit=HEAD, tutorial_files="labs/no-such-file.md")
        self.assertTrue(any("does not exist" in p for p in self.check(nofile, git=True)))
        good = entry(**base, tutorial_commit=HEAD, tutorial_files="labs/README.md")
        self.assertEqual(self.check(good, git=True), [])

    def test_commit_without_fixed_status_is_flagged(self):
        self.assertTrue(any("status is open" in p for p in self.check(entry(tutorial_commit=HEAD))))

    def test_id_must_match_filename_and_values_must_be_known(self):
        self.assertTrue(any("does not match" in p for p in self.check(entry(id="FB-0002"))))
        self.assertTrue(any("kind must be" in p for p in self.check(entry(kind="rant"))))

    def test_index_says_no_entries_yet_when_empty(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertIn("No entries yet", fb.index_text(Path(d)))

    def test_index_quotes_jp_not_a_summary(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "FB-0001.md").write_text(entry())
            self.assertIn("that is not how we number wires", fb.index_text(Path(d)))

    def test_committed_ledger_is_current_and_valid(self):
        self.assertEqual(fb.validate(), [])
        self.assertEqual((ROOT / "feedback" / "LEDGER.md").read_text(), fb.index_text())


if __name__ == "__main__":
    unittest.main()
