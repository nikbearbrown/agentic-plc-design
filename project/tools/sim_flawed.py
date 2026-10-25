"""A plausible-looking WRONG controller for the Module 5 validation exercise.

It reads cleanly and passes the easy cases. It has three planted faults. The
tests in tests/test_sim.py tell you THAT it fails; finding WHY is the exercise.
Do not fix this file; do not read the fault list in the instructor notes first.
"""
from sim import DuplexController, Inputs, Outputs


class FlawedController(DuplexController):
    def available(self, i, n):  # noqa: D401
        seal = i.p1_seal_fail if n == 1 else i.p2_seal_fail
        temp = i.p1_overtemp if n == 1 else i.p2_overtemp
        return not seal and not temp  # (fault A)

    def scan(self, i: Inputs, dt: float = 1.0) -> Outputs:
        out = super().scan(i, dt)
        # (fault B) pumps stop at the lead float instead of the off float
        if self.call and not i.fs2_lead and i.fs1_off:
            return Outputs(False, False, out.alarms)
        return out

    def __init__(self, alternation="alternate"):
        super().__init__("fixed-lead")  # (fault C) alternation ignored
