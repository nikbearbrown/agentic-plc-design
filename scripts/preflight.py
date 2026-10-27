#!/usr/bin/env python3
"""Can this computer run the course labs? Read-only. Works on macOS, Linux, WSL and says so on Windows.

    python3 scripts/preflight.py

Checks the operating system, Python version, the build tools the lab installer needs, the folder the
course sits in, and free disk space. For anything missing it prints the exact command for this system.
It installs nothing and changes nothing. Exit 0 means ready; exit 1 means a blocker was found.

Written to run on old Pythons (3.6+) so it can give a useful answer before the right Python exists.
Standard library only.
"""
from __future__ import print_function

import os
import platform
import shutil
import subprocess
import sys

MIN_PY = (3, 12)          # scripts/bootstrap.py needs safe archive extraction (3.12+)
MIN_FREE_GB = 3.0         # source builds and generated files; the measured install used well under 1 GB
TOOLS = ("make", "cc", "c++", "flex", "perl", "curl", "git")


def os_kind(system=None, release_text=None, osrelease_path="/proc/sys/kernel/osrelease"):
    """Return 'windows', 'wsl', 'macos' or 'linux'."""
    system = system or platform.system()
    if system == "Windows":
        return "windows"
    if system == "Darwin":
        return "macos"
    text = release_text
    if text is None:
        try:
            with open(osrelease_path) as f:
                text = f.read()
        except (IOError, OSError):
            text = ""
    if "microsoft" in text.lower():
        return "wsl"
    return "linux"


def parse_os_release(text):
    out = {}
    for line in text.splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def distro_family(info):
    ids = ((info.get("ID", "") + " " + info.get("ID_LIKE", "")).lower()).split()
    if "debian" in ids or "ubuntu" in ids:
        return "debian"
    if "fedora" in ids or "rhel" in ids or "centos" in ids:
        return "fedora"
    if "arch" in ids:
        return "arch"
    return "other"


def install_hint(kind, family, missing, py_ok):
    """The exact command(s) for this system; empty list if nothing is needed."""
    if not missing and py_ok:
        return []
    if kind == "macos":
        lines = []
        if missing:
            lines.append("xcode-select --install     (installs Apple's command-line developer tools: make, cc, flex, perl, git, curl)")
        if not py_ok:
            lines.append("Install Python 3.12 or newer from https://www.python.org/downloads/ (or: brew install python), "
                         "then open a NEW Terminal window")
        return lines
    if kind in ("linux", "wsl"):
        if family == "debian":
            lines = []
            if missing or not py_ok:
                lines.append("sudo apt update && sudo apt install -y build-essential flex curl git perl python3 python3-venv python3-pip")
            if not py_ok:
                lines.append("If python3 is still older than 3.12, this Linux is too old: use Ubuntu 24.04 or newer")
            return lines
        if family == "fedora":
            return ["sudo dnf install -y gcc gcc-c++ make flex curl git perl python3 python3-pip"]
        if family == "arch":
            return ["sudo pacman -S --needed base-devel flex curl git perl python"]
        return ["Install: a C and C++ compiler, make, flex, perl, curl, git, and Python 3.12+ with venv, using your system's package manager"]
    return []


def windows_message():
    return [
        "This is Windows without Linux. The lab tools are Linux-style programs; the supported route on Windows is WSL (Ubuntu inside Windows).",
        "1. Open PowerShell as administrator and run:  wsl --install -d Ubuntu-24.04   then restart.",
        "2. Open the Ubuntu app from the Start menu, then follow SETUP.md from there.",
        "(If a company policy blocks WSL or administrator rights, stop and ask your IT team.)",
    ]


def check_path(path):
    """Problems with where the course folder lives."""
    probs = []
    if " " in path:
        probs.append("the course folder path contains a space; the compiler build scripts break on spaces. Move or re-clone the course to a path without spaces")
    if path.startswith("/mnt/c") or path.startswith("/mnt/d"):
        probs.append("the course is on the Windows drive (/mnt/c...); this is slow and breaks file permissions. Clone it inside your Ubuntu home folder (cd ~) instead")
    return probs


def py_version_ok(vi=None):
    vi = vi or sys.version_info
    return (vi[0], vi[1]) >= MIN_PY


def free_gb(path):
    try:
        st = os.statvfs(path)
        return st.f_bavail * st.f_frsize / 1e9
    except (AttributeError, OSError):
        return None


def run_checks(root):
    kind = os_kind()
    report = {"kind": kind, "blockers": [], "warnings": [], "fixes": [], "ok": []}
    report["ok"].append("system: %s (%s %s)" % (kind, platform.system(), platform.machine()))
    if kind == "windows":
        report["blockers"].append("Windows without WSL")
        report["fixes"] = windows_message()
        return report

    info = {}
    if kind in ("linux", "wsl"):
        try:
            with open("/etc/os-release") as f:
                info = parse_os_release(f.read())
        except (IOError, OSError):
            pass
        report["ok"].append("distribution: %s" % info.get("PRETTY_NAME", "unknown"))
    family = distro_family(info)

    pv = "%d.%d.%d" % sys.version_info[:3]
    py_ok = py_version_ok()
    (report["ok"] if py_ok else report["blockers"]).append(
        "python3 %s%s" % (pv, "" if py_ok else " (need %d.%d or newer)" % MIN_PY))
    try:
        import ensurepip  # noqa: F401  (Debian/Ubuntu ship it in the python3-venv package)
        report["ok"].append("python venv support present")
    except ImportError:
        report["blockers"].append("python venv support missing (needed for the drawing lab)")
        py_ok = False

    missing = [t for t in TOOLS if shutil.which(t) is None]
    for t in TOOLS:
        if t in missing:
            report["blockers"].append("missing tool: %s" % t)
        else:
            report["ok"].append("tool: %s" % t)

    for p in check_path(root):
        report["blockers"].append(p)
    gb = free_gb(root)
    if gb is not None:
        if gb < MIN_FREE_GB:
            report["blockers"].append("only %.1f GB free; need about %.0f GB" % (gb, MIN_FREE_GB))
        else:
            report["ok"].append("free disk: %.0f GB" % gb)
    if kind == "macos" and platform.machine() not in ("arm64",):
        report["warnings"].append("Intel Mac: not tested; expected to work")
    if kind == "linux":
        report["warnings"].append("Linux: not tested by the course author; expected to work")
    if kind == "wsl":
        report["warnings"].append("WSL: not tested by the course author; you may be the first")
    report["fixes"] = install_hint(kind, family, missing, py_ok)
    return report


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    r = run_checks(root)
    print("Course preflight (read-only; nothing is installed or changed)\n")
    for line in r["ok"]:
        print("  ok       " + line)
    for line in r["warnings"]:
        print("  note     " + line)
    for line in r["blockers"]:
        print("  BLOCKER  " + line)
    if r["fixes"]:
        print("\nWhat to do:")
        for line in r["fixes"]:
            print("  " + line)
        print("\nThen run this check again.")
    if r["blockers"]:
        print("\nNOT READY.")
        return 1
    print("\nREADY. Next: python3 scripts/bootstrap.py   (prints a plan; nothing is changed until you add --apply)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
