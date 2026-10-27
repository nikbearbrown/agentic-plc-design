import importlib.util, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
spec = importlib.util.spec_from_file_location("preflight", ROOT / "scripts" / "preflight.py")
pf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pf)


class TestPreflight(unittest.TestCase):
    def test_os_detection(self):
        self.assertEqual(pf.os_kind(system="Windows"), "windows")
        self.assertEqual(pf.os_kind(system="Darwin"), "macos")
        self.assertEqual(pf.os_kind(system="Linux", release_text="5.15.153.1-microsoft-standard-WSL2"), "wsl")
        self.assertEqual(pf.os_kind(system="Linux", release_text="6.8.0-31-generic"), "linux")

    def test_distro_family(self):
        ubuntu = pf.parse_os_release('NAME="Ubuntu"\nID=ubuntu\nID_LIKE=debian\nPRETTY_NAME="Ubuntu 24.04 LTS"\n')
        self.assertEqual(pf.distro_family(ubuntu), "debian")
        self.assertEqual(pf.distro_family(pf.parse_os_release("ID=fedora\n")), "fedora")
        self.assertEqual(pf.distro_family({}), "other")

    def test_python_floor_is_3_12(self):
        self.assertFalse(pf.py_version_ok((3, 11, 9)))
        self.assertTrue(pf.py_version_ok((3, 12, 0)))
        self.assertTrue(pf.py_version_ok((3, 14, 6)))

    def test_bad_folders_are_blockers(self):
        self.assertTrue(pf.check_path("/home/jp/my course/agentic-plc-design"))
        self.assertTrue(pf.check_path("/mnt/c/Users/jp/agentic-plc-design"))
        self.assertEqual(pf.check_path("/home/jp/agentic-plc-design"), [])

    def test_install_hints_are_system_specific_and_empty_when_ready(self):
        self.assertEqual(pf.install_hint("linux", "debian", [], True), [])
        self.assertIn("apt", pf.install_hint("wsl", "debian", ["flex"], True)[0])
        self.assertIn("xcode-select", pf.install_hint("macos", "", ["make"], True)[0])
        self.assertIn("python.org", pf.install_hint("macos", "", [], False)[0])
        self.assertIn("dnf", pf.install_hint("linux", "fedora", ["make"], True)[0])

    def test_windows_message_points_to_wsl(self):
        self.assertTrue(any("wsl --install" in l for l in pf.windows_message()))

    def test_script_in_a_folder_with_a_space_reports_a_blocker(self):
        with tempfile.TemporaryDirectory() as d:
            sub = Path(d) / "has space" / "scripts"
            sub.mkdir(parents=True)
            shutil.copy(ROOT / "scripts" / "preflight.py", sub / "preflight.py")
            r = subprocess.run([sys.executable, str(sub / "preflight.py")], capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)
            self.assertIn("contains a space", r.stdout)

    def test_it_changes_nothing(self):
        before = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain"], capture_output=True, text=True).stdout
        subprocess.run([sys.executable, str(ROOT / "scripts" / "preflight.py")], capture_output=True)
        after = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain"], capture_output=True, text=True).stdout
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
