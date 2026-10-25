"""Reference model of duplex lead/lag pump control (the control narrative as code).

This is the oracle the course uses to judge generated PLC logic: if a generated
program disagrees with this model on a test vector, one of them is wrong and a
human decides which. The model itself is the +1's to correct (Module 1, 5).

Inputs are float states: True means liquid is above that float.
Level index: 0 none, 1 off-float, 2 lead-on, 3 lag-on, 4 high.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Inputs:
    fs1_off: bool = False
    fs2_lead: bool = False
    fs3_lag: bool = False
    fs4_high: bool = False
    p1_auto: bool = True
    p2_auto: bool = True
    p1_seal_fail: bool = False
    p2_seal_fail: bool = False
    p1_overtemp: bool = False
    p2_overtemp: bool = False


@dataclass
class Outputs:
    p1_run: bool = False
    p2_run: bool = False
    alarms: frozenset = frozenset()

    def key(self):
        return (self.p1_run, self.p2_run, tuple(sorted(self.alarms)))


class DuplexController:
    LAG_DELAY_S = 5.0

    def __init__(self, alternation: str = "alternate"):
        self.alternation = alternation
        self.lead = 1
        self.call = False
        self.lag_timer = 0.0
        self.lag_enabled = False

    # -- helpers
    @staticmethod
    def level_index(i: Inputs) -> int:
        if i.fs4_high:
            return 4
        if i.fs3_lag:
            return 3
        if i.fs2_lead:
            return 2
        if i.fs1_off:
            return 1
        return 0

    @staticmethod
    def float_fault(i: Inputs) -> bool:
        return (i.fs4_high and not i.fs3_lag) or (i.fs3_lag and not i.fs2_lead) or (i.fs2_lead and not i.fs1_off)

    @staticmethod
    def available(i: Inputs, n: int) -> bool:
        auto = i.p1_auto if n == 1 else i.p2_auto
        seal = i.p1_seal_fail if n == 1 else i.p2_seal_fail
        temp = i.p1_overtemp if n == 1 else i.p2_overtemp
        return auto and not seal and not temp

    def scan(self, i: Inputs, dt: float = 1.0) -> Outputs:
        lvl = self.level_index(i)
        alarms = set()
        if lvl == 4:
            alarms.add("high_level")
        if self.float_fault(i):
            alarms.add("float_fault")
        for n in (1, 2):
            if (i.p1_seal_fail, i.p2_seal_fail)[n - 1]:
                alarms.add(f"seal_fail_p{n}")
            if (i.p1_overtemp, i.p2_overtemp)[n - 1]:
                alarms.add(f"overtemp_p{n}")

        was_call = self.call
        if lvl >= 2:
            self.call = True
        elif lvl < 1:
            self.call = False
        if was_call and not self.call:
            self.lag_enabled = False
            self.lag_timer = 0.0
            if self.alternation == "alternate":
                self.lead = 2 if self.lead == 1 else 1

        run = {1: False, 2: False}
        if self.call:
            lead = self.lead
            other = 2 if lead == 1 else 1
            if not self.available(i, lead):
                lead, other = other, lead
            if self.available(i, lead):
                run[lead] = True
                if lvl >= 3:
                    self.lag_timer += dt
                    if self.lag_timer >= self.LAG_DELAY_S:
                        self.lag_enabled = True
                else:
                    self.lag_timer = 0.0
                if self.lag_enabled and self.available(i, other):
                    run[other] = True
            else:
                alarms.add("no_pump_available")
        return Outputs(run[1], run[2], frozenset(alarms))
