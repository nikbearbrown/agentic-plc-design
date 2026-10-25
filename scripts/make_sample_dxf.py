"""Builds labs/dxf/station-a.dxf: a SYNTHETIC drawing sheet for the ezdxf lab.

Run with the isolated interpreter:  .toolchain/venv-dxf/bin/python scripts/make_sample_dxf.py
Deterministic content; the committed file is the fixture. Nothing here is a customer drawing.

Planted for the lab (answer key is in the lab, after the prediction step):
  * device P2_OL1 is missing, P3_K1 is extra, P1_K1 says 10 HP (design says 7.5 HP)  [cross-check]
  * "7.5 HP" appears in a note, an MTEXT, a nameplate attribute, a revision-history line
    AND next to a number that is not a rating ("CABLE LENGTH 7.5 FT")                  [replace]
  * wire labels are out of order and one label is not a wire number                   [renumber]
"""
import sys
from pathlib import Path

import ezdxf

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "project" / "tools"))
import design  # noqa: E402

OUT = ROOT / "labs" / "dxf" / "station-a.dxf"


def build():
    variant = design.load_toml(ROOT / "project" / "variants" / "a-baseline.toml")
    doc = ezdxf.new("R2018")
    doc.header["$HANDSEED"] = "100"
    for name in ("TITLE", "DEVICES", "NOTES", "WIRES", "REV-HISTORY"):
        doc.layers.add(name)
    msp = doc.modelspace()

    tb = doc.blocks.new("TITLEBLOCK")
    for i, tag in enumerate(("JOBNAME", "JOBNUMBER", "REV", "VOLTAGE", "PUMPHP")):
        tb.add_attdef(tag, (1, 1 + 4 * i), "UNSET", dxfattribs={"height": 2.5, "layer": "TITLE"})
    msp.add_blockref("TITLEBLOCK", (400, 0), dxfattribs={"layer": "TITLE"}).add_auto_attribs(
        {"JOBNAME": "PROJECT NAME", "JOBNUMBER": "00-0000", "REV": "-", "VOLTAGE": "000V 0PH 0HZ", "PUMPHP": "0 HP"})

    dev = doc.blocks.new("DEVICE")
    dev.add_attdef("TAG", (0, 0), "TAG", dxfattribs={"height": 2.5})
    dev.add_attdef("DESC", (0, -4), "DESC", dxfattribs={"height": 2.0})
    devices = [(d.tag, d.description) for d in design.build_devices(variant)]
    devices = [(t, dsc) for t, dsc in devices if t != "P2_OL1"]                 # planted: missing
    devices = [(t, dsc.replace("7.5 HP", "10 HP") if t == "P1_K1" else dsc) for t, dsc in devices]  # planted
    devices.append(("P3_K1", "Pump 3 contactor (7.5 HP, 460 V)"))               # planted: extra
    for i, (tag, desc) in enumerate(devices):
        msp.add_blockref("DEVICE", (10 + 45 * (i % 8), 200 - 20 * (i // 8)),
                         dxfattribs={"layer": "DEVICES"}).add_auto_attribs({"TAG": tag, "DESC": desc})

    notes = [
        ("NOTES", (10, 60), "PUMPS: (2) 7.5 HP, 460 V, 3 PH SUBMERSIBLE"),
        ("NOTES", (10, 55), "CABLE LENGTH 7.5 FT FROM JUNCTION BOX TO PUMP"),
        ("REV-HISTORY", (10, 40), "REV A  INITIAL ISSUE - 7.5 HP PUMPS"),
    ]
    for layer, pos, text in notes:
        msp.add_text(text, height=2.5, dxfattribs={"layer": layer}).set_placement(pos)
    msp.add_mtext("MOTOR DATA:\\P7.5 HP, 460 V\\PSEE SCHEDULE", dxfattribs={
        "layer": "NOTES", "insert": (10, 80), "char_height": 2.5})

    for label, pos in (("W014", (10, 30)), ("W003", (40, 30)), ("W009", (10, 25)), ("W001", (40, 25)),
                       ("WIRE NOTE", (10, 20)), ("W020", (40, 20))):
        msp.add_text(label, height=2.0, dxfattribs={"layer": "WIRES"}).set_placement(pos)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(OUT)
    return OUT


if __name__ == "__main__":
    print(build())
