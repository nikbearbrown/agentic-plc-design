"""Variant -> checks -> devices -> I/O list -> BOM.

Everything is derived from one variant file (TOML) so the drawing set, the
I/O list and the BOM cannot drift apart. Stdlib only (Python 3.11+).
"""
from __future__ import annotations

import csv
import io
import math
import os
import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

STARTERS = ("across-the-line", "soft-start", "vfd")
LEVEL_METHODS = ("floats", "transducer")
PLATFORMS = ("relay", "plc", "rtu")
ALARMS_BASE = ("high_level", "float_fault")


def load_toml(path) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


def load_tables():
    """Reference tables and parts catalog. Set APD_CATALOG to a file path to use your own catalog."""
    cat = os.environ.get("APD_CATALOG") or (DATA / "catalog.toml")
    return load_toml(DATA / "nec-extracts.toml"), load_toml(cat)


def unverified_banner(tables: dict) -> str:
    if tables["meta"].get("verified"):
        return ""
    return ("*** UNVERIFIED REFERENCE TABLES: the numbers below came from an AI's memory, "
            "not from your code book. Check data/nec-extracts.toml, then sign it. ***")


@dataclass
class Finding:
    level: str  # ERROR | WARN | INFO
    rule: str
    message: str

    def __str__(self):
        return f"{self.level:5} {self.rule}: {self.message}"


def fla(variant: dict, tables: dict):
    volts = variant["power"]["voltage"]
    hp = str(variant["pumps"]["hp"])
    table = tables.get(f"fla_{volts}")
    if table is None:
        return None
    return table.get(hp)


def check_variant(variant: dict) -> list[Finding]:
    """Rules a designer would apply before drawing anything. Add your own."""
    out: list[Finding] = []
    tables, _ = load_tables()
    pumps, level, ctl = variant["pumps"], variant["level"], variant["control"]
    power = variant["power"]
    alarms = variant.get("alarms", {}).get("points", [])
    opts = variant.get("options", {})

    if pumps["count"] != 2:
        out.append(Finding("ERROR", "R01-duplex", f"template is duplex; pumps.count={pumps['count']}"))
    if pumps["starter"] not in STARTERS:
        out.append(Finding("ERROR", "R02-starter", f"unknown starter '{pumps['starter']}'"))
    if level["method"] not in LEVEL_METHODS:
        out.append(Finding("ERROR", "R03-level", f"unknown level method '{level['method']}'"))
    if ctl["platform"] not in PLATFORMS:
        out.append(Finding("ERROR", "R04-platform", f"unknown platform '{ctl['platform']}'"))
    if fla(variant, tables) is None:
        out.append(Finding("ERROR", "R05-fla",
                           f"no FLA for {pumps['hp']} HP at {power['voltage']} V in nec-extracts.toml"))
    if level["method"] == "transducer" and ctl["platform"] == "relay":
        out.append(Finding("ERROR", "R06-analog-needs-controller",
                           "a 4-20 mA transducer needs a PLC/RTU (or a stand-alone level controller, "
                           "which this template does not include)"))
    if pumps["starter"] == "vfd" and ctl["platform"] == "relay":
        out.append(Finding("WARN", "R07-vfd-relay",
                           "VFD with relay-only control: who sets speed? Confirm a fixed-speed run command is intended"))
    if level.get("hazardous_wet_well") and level["method"] == "floats":
        out.append(Finding("INFO", "R08-is-barriers",
                           "hazardous wet well: float circuits need intrinsically safe barriers (added to BOM)"))
    if level.get("hazardous_wet_well") and level["method"] == "transducer":
        out.append(Finding("INFO", "R08-is-barriers", "hazardous wet well: analog loop needs an IS barrier (added to BOM)"))
    for a in alarms:
        m = re.fullmatch(r"(seal_fail|overtemp)_p(\d+)", a)
        if m:
            if int(m.group(2)) not in (1, 2):
                out.append(Finding("ERROR", "R09-alarm-pump", f"alarm '{a}' references a pump that does not exist"))
        elif a not in ALARMS_BASE + ("power_fail", "gen_running"):
            out.append(Finding("WARN", "R09-alarm-name", f"alarm '{a}' is not in the template's alarm list"))
    if "high_level" not in alarms:
        out.append(Finding("ERROR", "R10-high-level", "every station needs a high_level alarm"))
    if opts.get("generator_transfer") and "gen_running" not in alarms:
        out.append(Finding("WARN", "R11-generator", "generator_transfer is on but gen_running is not an alarm point"))
    return out


# ---------- devices -------------------------------------------------------

@dataclass
class Device:
    tag: str
    kind: str
    description: str
    part: str
    qty: int = 1
    basis: str = ""


def _pick(rows, amps):
    for r in sorted(rows, key=lambda r: r["amps"]):
        if r["amps"] >= amps:
            return r["part"]
    return None


def size_motor_circuit(variant: dict, tables: dict) -> dict:
    f = fla(variant, tables)
    b = tables["breaker"]
    cond_need = f * b["conductor_multiple"]
    awg = next((c["awg"] for c in tables["conductor"] if c["amps"] >= cond_need), None)
    max_bkr = f * b["max_multiple"]
    bkr = max([s for s in b["standard_sizes"] if s <= max_bkr], default=None)
    return {"fla": f, "conductor_need_a": round(cond_need, 2), "awg": awg,
            "max_breaker_a": round(max_bkr, 1), "breaker_a": bkr}


def build_devices(variant: dict) -> list[Device]:
    tables, cat = load_tables()
    fx = cat["fixed"]
    pumps, level, ctl = variant["pumps"], variant["level"], variant["control"]
    opts = variant.get("options", {})
    alarms = variant.get("alarms", {}).get("points", [])
    sz = size_motor_circuit(variant, tables)
    f = sz["fla"]
    hp, v = pumps["hp"], variant["power"]["voltage"]
    d: list[Device] = []

    for n in (1, 2):
        d.append(Device(f"P{n}_MPCB", "protection", f"Pump {n} motor circuit protector",
                        fx["motor_protector"], 1,
                        f"max {sz['max_breaker_a']} A from {f} A FLA; std size {sz['breaker_a']} A; wire {sz['awg']} AWG"))
        if pumps["starter"] == "across-the-line":
            d.append(Device(f"P{n}_K1", "starter", f"Pump {n} contactor ({hp} HP, {v} V)",
                            _pick(cat["contactor"], f) or "NO-PART", 1, f"smallest contactor >= {f} A"))
            d.append(Device(f"P{n}_OL1", "overload", f"Pump {n} overload relay, set to nameplate", "GEN-OL-ADJ", 1,
                            f"FLA {f} A (nameplate governs)"))
        elif pumps["starter"] == "soft-start":
            d.append(Device(f"P{n}_SS1", "starter", f"Pump {n} soft starter ({hp} HP, {v} V)",
                            _pick(cat["soft_starter"], f) or "NO-PART", 1, f"smallest soft starter >= {f} A"))
        else:
            d.append(Device(f"P{n}_VFD1", "starter", f"Pump {n} VFD ({hp} HP, {v} V)",
                            _pick(cat["vfd"], f) or "NO-PART", 1, f"smallest VFD >= {f} A"))
        d.append(Device(f"P{n}_HOA", "operator", f"Pump {n} Hand-Off-Auto", fx["hoa_switch"]))
        d.append(Device(f"P{n}_RUN_PL", "operator", f"Pump {n} run light", fx["run_light"]))
        d.append(Device(f"P{n}_FAIL_PL", "operator", f"Pump {n} fail light", fx["fail_light"]))

    if level["method"] == "floats":
        for tag, desc in (("FS1_OFF", "Pumps-off float"), ("FS2_LEAD", "Lead-on float"),
                          ("FS3_LAG", "Lag-on float"), ("FS4_HIGH", "High-level float")):
            d.append(Device(tag, "level", desc, fx["float_switch"]))
        if level.get("hazardous_wet_well"):
            d.append(Device("IS1", "barrier", "Intrinsically safe relay, 2 channel (floats 1-2)", fx["is_barrier_2ch"]))
            d.append(Device("IS2", "barrier", "Intrinsically safe relay, 2 channel (floats 3-4)", fx["is_barrier_2ch"]))
    else:
        d.append(Device("LT1", "level", "Submersible level transducer 4-20 mA", fx["level_transducer"]))
        if level.get("hazardous_wet_well"):
            d.append(Device("IS1", "barrier", "IS barrier, analog loop", fx["is_barrier_analog"]))
        d.append(Device("FS4_HIGH", "level", "High-level float (independent backup)", fx["float_switch"]))

    d.append(Device("BCN1", "alarm", "Alarm beacon", fx["alarm_beacon"]))
    d.append(Device("PB_SIL", "alarm", "Alarm silence", fx["alarm_silence"]))
    if ctl["platform"] == "relay":
        d.append(Device("ALT1", "control", "Duplex alternator relay", fx["alternator_relay"]))
    elif ctl["platform"] == "plc":
        d.append(Device("PLC1", "control", "PLC CPU", fx["plc_cpu"]))
        io_rows = build_io(variant)
        di = sum(1 for r in io_rows if r["type"] == "DI")
        do = sum(1 for r in io_rows if r["type"] == "DO")
        ai = sum(1 for r in io_rows if r["type"] == "AI")
        d.append(Device("PLC1_DI", "control", "PLC 16-pt digital input card", fx["plc_di_16"], math.ceil(di / 16) or 1,
                        f"{di} DI points"))
        d.append(Device("PLC1_DO", "control", "PLC 16-pt digital output card", fx["plc_do_16"], math.ceil(do / 16) or 1,
                        f"{do} DO points"))
        if ai:
            d.append(Device("PLC1_AI", "control", "PLC 4-ch analog input card", fx["plc_ai_4"], math.ceil(ai / 4),
                            f"{ai} AI points"))
    else:
        d.append(Device("RTU1", "control", "RTU base unit", fx["rtu"]))
    if opts.get("generator_transfer"):
        d.append(Device("K_GEN", "interface", "Generator-running interface relay", fx["ats_interface_relay"]))
    return d


# ---------- I/O list -------------------------------------------------------

def build_io(variant: dict) -> list[dict]:
    level = variant["level"]
    opts = variant.get("options", {})
    alarms = variant.get("alarms", {}).get("points", [])
    rows: list[tuple[str, str, str, str]] = []  # tag, type, description, field device
    for n in (1, 2):
        rows += [
            (f"P{n}_RUN_FB", "DI", f"Pump {n} running feedback", f"P{n}_K1 aux" if variant["pumps"]["starter"] == "across-the-line" else f"P{n} starter run relay"),
            (f"P{n}_HOA_AUTO", "DI", f"Pump {n} HOA in Auto", f"P{n}_HOA"),
            (f"P{n}_SEAL_FAIL", "DI", f"Pump {n} seal fail", f"P{n} moisture probe"),
            (f"P{n}_OVERTEMP", "DI", f"Pump {n} motor over-temperature", f"P{n} thermal switch"),
            (f"P{n}_RUN_CMD", "DO", f"Pump {n} run command", f"P{n} starter coil/run input"),
            (f"P{n}_FAIL_PL", "DO", f"Pump {n} fail light", f"P{n}_FAIL_PL"),
        ]
    if level["method"] == "floats":
        rows += [("FS1_OFF", "DI", "Pumps-off float", "FS1_OFF"), ("FS2_LEAD", "DI", "Lead-on float", "FS2_LEAD"),
                 ("FS3_LAG", "DI", "Lag-on float", "FS3_LAG"), ("FS4_HIGH", "DI", "High-level float", "FS4_HIGH")]
    else:
        rows += [("LT1_LEVEL", "AI", "Wet well level 4-20 mA", "LT1"), ("FS4_HIGH", "DI", "High-level float (backup)", "FS4_HIGH")]
    rows.append(("BCN1_CMD", "DO", "Alarm beacon", "BCN1"))
    rows.append(("PB_SIL", "DI", "Alarm silence pushbutton", "PB_SIL"))
    if "power_fail" in alarms:
        rows.append(("PWR_FAIL", "DI", "Utility power fail", "phase monitor relay"))
    if opts.get("generator_transfer"):
        rows.append(("GEN_RUN", "DI", "Generator running", "K_GEN"))
    out, counters = [], {"DI": 0, "DO": 0, "AI": 0}
    for tag, typ, desc, dev in rows:
        counters[typ] += 1
        out.append({"tag": tag, "type": typ, "address": f"{typ}{counters[typ]:02d}",
                    "description": desc, "field_device": dev})
    return out


def csv_text(rows: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


# ---------- BOM ------------------------------------------------------------

def build_bom(variant: dict) -> list[dict]:
    agg: dict[str, dict] = {}
    for dev in build_devices(variant):
        row = agg.setdefault(dev.part, {"part": dev.part, "description": dev.description, "qty": 0, "tags": [], "basis": dev.basis})
        row["qty"] += dev.qty
        row["tags"].append(dev.tag)
    rows = []
    for r in sorted(agg.values(), key=lambda r: r["part"]):
        rows.append({"part": r["part"], "description": re.sub(r"Pump \d", "Pump", r["description"]), "qty": r["qty"],
                     "tags": " ".join(r["tags"]), "basis": r["basis"]})
    return rows
