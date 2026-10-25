#!/usr/bin/env python3
"""Create the isolated ezdxf environment for the drawing-edit lab.

Default is a DRY RUN that prints the plan. --apply creates .toolchain/venv-dxf and installs the
pinned packages from labs/dxf/requirements.txt (network needed). Nothing is installed system-wide,
no privileges are used, and the folder is git-ignored and disposable.
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENV = ROOT / ".toolchain" / "venv-dxf"
REQ = ROOT / "labs" / "dxf" / "requirements.txt"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    py = VENV / "bin" / "python"
    print(f"plan: python3 -m venv {VENV}")
    print(f"plan: {py} -m pip install -r {REQ}")
    if not a.apply:
        print("DRY RUN: nothing created. Add --apply to install.")
        return 0
    if sys.version_info < (3, 11):
        sys.exit("Python 3.11+ required")
    if not py.exists():
        subprocess.run([sys.executable, "-m", "venv", str(VENV)], check=True)
    subprocess.run([str(py), "-m", "pip", "install", "--quiet", "-r", str(REQ)], check=True)
    out = subprocess.run([str(py), "-c", "import ezdxf; print(ezdxf.__version__)"],
                         capture_output=True, text=True, check=True)
    print(f"READY: ezdxf {out.stdout.strip()} in {VENV}")
    print(f"run tools with: {py}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
