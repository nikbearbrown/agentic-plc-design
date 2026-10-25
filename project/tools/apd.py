"""One front door:  python3 tools/apd.py <command> ...   (run from project/)"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import design  # noqa: E402

USAGE = """commands:
  check VARIANT              rule check; exit 1 on ERROR
  devices VARIANT            device list
  io VARIANT                 I/O list (CSV)
  bom VARIANT                bill of materials (CSV) with the unverified-table banner
  size VARIANT               motor circuit sizing from the reference tables
  lisp VARIANT [--swap a=b]  AutoLISP job file (dry-run by default)
  lint FILE...               AutoLISP safety lint
  crosscheck VARIANT EXTRACT.csv
  l5x VARIANT FILE.L5X
  spec SPEC.md CHECKLIST.csv
  log LOG.csv
  vectors                    reference-model test vectors (CSV)
  dxf ...                    edit a DXF copy with ezdxf (plan by default); needs scripts/dxf_setup.py --apply
"""


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(USAGE)
        return 0
    cmd, rest = argv[0], argv[1:]
    if cmd == "check":
        fs = design.check_variant(design.load_toml(rest[0]))
        print("\n".join(map(str, fs)) or "No findings.")
        return 1 if any(f.level == "ERROR" for f in fs) else 0
    if cmd == "devices":
        for d in design.build_devices(design.load_toml(rest[0])):
            print(f"{d.tag:12} {d.part:20} x{d.qty}  {d.description}")
        return 0
    if cmd == "io":
        print(design.csv_text(design.build_io(design.load_toml(rest[0]))), end="")
        return 0
    if cmd == "bom":
        tables, _ = design.load_tables()
        b = design.unverified_banner(tables)
        if b:
            print("# " + b)
        print(design.csv_text(design.build_bom(design.load_toml(rest[0]))), end="")
        return 0
    if cmd == "size":
        tables, _ = design.load_tables()
        b = design.unverified_banner(tables)
        if b:
            print(b)
        print(design.size_motor_circuit(design.load_toml(rest[0]), tables))
        return 0
    if cmd == "dxf":
        import subprocess
        venv_py = Path(__file__).resolve().parent.parent.parent / ".toolchain" / "venv-dxf" / "bin" / "python"
        if not venv_py.exists():
            print("ezdxf environment missing. Run: python3 scripts/dxf_setup.py --apply")
            return 2
        return subprocess.run([str(venv_py), str(Path(__file__).resolve().parent / "dxf_edit.py"), *rest]).returncode
    mods = {"lisp": "lisp_gen", "lint": "lisp_lint", "crosscheck": "crosscheck", "l5x": "l5x_check",
            "spec": "spec_check", "log": "log_summary", "vectors": "vectors"}
    if cmd in mods:
        m = __import__(mods[cmd])
        return m.main(rest) or 0
    print(USAGE)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
