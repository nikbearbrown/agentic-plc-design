"""Edit drawing text and title blocks in a DXF file with ezdxf (open source, MIT).

This is the agent-runnable counterpart of the AutoLISP exercise (Module 4). Same safety
pattern, different language:

  * PLAN by default: it prints what would change and writes nothing.
  * APPLY writes a NEW file (--out). It refuses to overwrite the input or any existing file.
  * After writing it reloads the new file and checks that ONLY the planned text changed.
  * Every applied run leaves <out>.changes.json, an audit log of old and new values.

Run it with the isolated interpreter (see scripts/dxf_setup.py):
  .toolchain/venv-dxf/bin/python project/tools/dxf_edit.py --help
It is also reachable as:  python3 project/tools/apd.py dxf --help

NOT VERIFIED: DWG files (ezdxf reads DXF only), DraftSight/AutoCAD round-trips, and drawings
with proxy objects, external references or heavily formatted MTEXT. Test on a copy.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

try:
    import ezdxf
except ImportError:  # pragma: no cover - message path
    sys.exit("ezdxf is not installed in this interpreter. Run: python3 scripts/dxf_setup.py --apply "
             "and use .toolchain/venv-dxf/bin/python (or python3 project/tools/apd.py dxf ...).")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import design  # noqa: E402

DEFAULT_TAGS = {"job_name": "JOBNAME", "job_number": "JOBNUMBER", "revision": "REV",
                "voltage": "VOLTAGE", "pump_hp": "PUMPHP"}


# ---------- text-bearing entities --------------------------------------------------------

class Slot:
    """One editable string in the drawing: a TEXT, an MTEXT, or an ATTRIB on a block reference."""

    def __init__(self, entity, kind, owner_handle=None):
        self.entity, self.kind, self.owner_handle = entity, kind, owner_handle

    @property
    def handle(self):
        return self.entity.dxf.handle

    @property
    def layer(self):
        return self.entity.dxf.layer

    @property
    def text(self):
        return self.entity.text if self.kind == "MTEXT" else self.entity.dxf.text

    @text.setter
    def text(self, value):
        if self.kind == "MTEXT":
            self.entity.text = value
        else:
            self.entity.dxf.text = value


def slots(doc):
    """All editable strings in model space and every paper-space layout. Block definitions
    (templates) are deliberately NOT included: editing a definition changes every reference."""
    out = []
    for layout in doc.layouts:
        for e in layout:
            t = e.dxftype()
            if t == "TEXT":
                out.append(Slot(e, "TEXT"))
            elif t == "MTEXT":
                out.append(Slot(e, "MTEXT"))
            elif t == "INSERT":
                for a in e.attribs:
                    out.append(Slot(a, "ATTRIB", owner_handle=e.dxf.handle))
    return out


# ---------- plans ------------------------------------------------------------------------

def change(slot, new, reason):
    return {"handle": slot.handle, "kind": slot.kind, "layer": slot.layer,
            "old": slot.text, "new": new, "reason": reason}


def plan_title(doc, variant, block="TITLEBLOCK", tags=None):
    tagmap = {**DEFAULT_TAGS, **(tags or {})}
    j, p, pw = variant["job"], variant["pumps"], variant["power"]
    values = {tagmap["job_name"]: j["name"], tagmap["job_number"]: j["number"],
              tagmap["revision"]: j["revision"],
              tagmap["voltage"]: f"{pw['voltage']}V {pw['phase']}PH {pw['hz']}HZ",
              tagmap["pump_hp"]: f"{p['hp']} HP"}
    plan, found = [], 0
    for layout in doc.layouts:
        for e in layout:
            if e.dxftype() == "INSERT" and e.dxf.name == block:
                found += 1
                for a in e.attribs:
                    want = values.get(a.dxf.tag.upper())
                    if want is not None and a.dxf.text != want:
                        plan.append(change(Slot(a, "ATTRIB", e.dxf.handle), want, f"title block {a.dxf.tag}"))
    return plan, [] if found else [f"no block named {block} found"]


def plan_replace(doc, old, new, exclude_layers=()):
    skip = {s.upper() for s in exclude_layers}
    plan = []
    for s in slots(doc):
        if s.layer.upper() in skip:
            continue
        if old in s.text:
            plan.append(change(s, s.text.replace(old, new), f"replace '{old}'"))
    return plan, []


def plan_renumber(doc, layer, prefix, start, pattern=r"W\d+"):
    """Renumber wire labels on LAYER whose whole text matches PATTERN. Order is top-to-bottom,
    then left-to-right by insertion point, so it is repeatable (unlike selection-set order)."""
    rx = re.compile(rf"^{pattern}$")
    picked = [s for s in slots(doc) if s.kind == "TEXT" and s.layer.upper() == layer.upper() and rx.match(s.text)]
    picked.sort(key=lambda s: (-round(s.entity.dxf.insert.y, 3), round(s.entity.dxf.insert.x, 3)))
    plan, n = [], start
    for s in picked:
        new = f"{prefix}{n:03d}"
        if new != s.text:
            plan.append(change(s, new, f"renumber {layer}"))
        n += 1
    return plan, []


# ---------- extract (feeds crosscheck.py) ---------------------------------------------------

def extract(doc, block="DEVICE", tag_attr="TAG", desc_attr="DESC"):
    rows = []
    for layout in doc.layouts:
        for e in layout:
            if e.dxftype() == "INSERT" and e.dxf.name == block:
                vals = {a.dxf.tag.upper(): a.dxf.text for a in e.attribs}
                if vals.get(tag_attr):
                    rows.append({"tag": vals[tag_attr].strip(), "description": vals.get(desc_attr, "").strip()})
    return rows


# ---------- apply + verify --------------------------------------------------------------

def check_paths(src, out):
    src, out = Path(src).resolve(), Path(out).resolve()
    if out == src:
        raise SystemExit("refused: --out is the input file. Edits go to a NEW copy.")
    if out.exists():
        raise SystemExit(f"refused: {out} already exists. Choose a new name; nothing is overwritten.")
    if not out.parent.is_dir():
        raise SystemExit(f"refused: folder {out.parent} does not exist.")
    return src, out


def apply_plan(src, out, plan):
    """Edit a fresh load of SRC, save to OUT, reload OUT and prove only planned text changed."""
    src, out = check_paths(src, out)
    doc = ezdxf.readfile(src)
    by_handle = {s.handle: s for s in slots(doc)}
    for c in plan:
        slot = by_handle[c["handle"]]
        if slot.text != c["old"]:
            raise SystemExit(f"refused: {c['handle']} changed since the plan was made")
        slot.text = c["new"]
    doc.saveas(out)
    problems = verify(src, out, plan)
    log = {"input": str(src), "output": str(out), "changes": plan, "verification_problems": problems}
    Path(str(out) + ".changes.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
    return problems


def verify(src, out, plan):
    """Reload both files; only the planned strings may differ and no entity may appear or vanish."""
    before = {s.handle: s.text for s in slots(ezdxf.readfile(src))}
    after = {s.handle: s.text for s in slots(ezdxf.readfile(out))}
    expected = dict(before)
    expected.update({c["handle"]: c["new"] for c in plan})
    problems = []
    if set(before) != set(after):
        problems.append(f"entity set changed: {len(set(before) ^ set(after))} handle(s) differ")
    for h, text in after.items():
        if h in expected and text != expected[h]:
            problems.append(f"{h}: expected {expected[h]!r}, found {text!r}")
    return problems


def report(plan, notes, applied):
    for n in notes:
        print(f"NOTE   {n}")
    for c in plan:
        print(f"{'CHANGED' if applied else 'WOULD CHANGE'}  {c['kind']:6} layer={c['layer']:12} "
              f"handle={c['handle']:>4}  {c['old']!r} -> {c['new']!r}")
    print(f"{len(plan)} change(s) {'applied' if applied else 'planned; nothing written (add --apply --out NEW.dxf)'}")


# ---------- CLI ---------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("dxf")
        p.add_argument("--apply", action="store_true", help="write the change to --out (default: plan only)")
        p.add_argument("--out", help="NEW file to write; must not exist")

    t = sub.add_parser("title", help="fill title block attributes from a variant")
    common(t)
    t.add_argument("--variant", required=True)
    t.add_argument("--block", default="TITLEBLOCK")
    t.add_argument("--tag", action="append", default=[], help="field=ATTRIBUTE_TAG, repeatable")
    r = sub.add_parser("replace", help="replace text everywhere (TEXT, MTEXT, ATTRIB)")
    common(r)
    r.add_argument("old")
    r.add_argument("new")
    r.add_argument("--exclude-layer", action="append", default=[], help="leave this layer alone, repeatable")
    n = sub.add_parser("renumber", help="renumber wire labels on one layer")
    common(n)
    n.add_argument("--layer", required=True)
    n.add_argument("--prefix", default="W")
    n.add_argument("--start", type=int, default=1)
    x = sub.add_parser("extract", help="write tag,description CSV from DEVICE block attributes")
    x.add_argument("dxf")
    x.add_argument("--block", default="DEVICE")
    a = ap.parse_args(argv)

    doc = ezdxf.readfile(a.dxf)
    if a.cmd == "extract":
        w = csv.DictWriter(sys.stdout, fieldnames=["tag", "description"], lineterminator="\n")
        w.writeheader()
        w.writerows(extract(doc, a.block))
        return 0
    if a.cmd == "title":
        plan, notes = plan_title(doc, design.load_toml(a.variant), a.block, dict(s.split("=", 1) for s in a.tag))
    elif a.cmd == "replace":
        plan, notes = plan_replace(doc, a.old, a.new, a.exclude_layer)
    else:
        plan, notes = plan_renumber(doc, a.layer, a.prefix, a.start)

    if not a.apply:
        report(plan, notes, applied=False)
        return 0
    if not a.out:
        raise SystemExit("refused: --apply needs --out NEW.dxf")
    problems = apply_plan(a.dxf, a.out, plan)
    report(plan, notes, applied=True)
    print(f"audit log: {a.out}.changes.json")
    if problems:
        print("VERIFICATION FAILED:")
        for p in problems:
            print("  -", p)
        return 1
    print("verified: reloaded output; only the planned text differs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
