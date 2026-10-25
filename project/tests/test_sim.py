import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from sim import DuplexController, Inputs
from sim_flawed import FlawedController

FLAWED = __import__("os").environ.get("APD_TEST_FLAWED") == "1"
CTL = FlawedController if FLAWED else DuplexController


def run(ctl, steps):
    """steps: list of (Inputs, seconds). Returns the last Outputs."""
    out = None
    for inp, secs in steps:
        for _ in range(int(secs)):
            out = ctl.scan(inp, 1.0)
    return out


def lvl(n, **kw):
    return Inputs(fs1_off=n >= 1, fs2_lead=n >= 2, fs3_lag=n >= 3, fs4_high=n >= 4, **kw)


class TestLeadLag(unittest.TestCase):
    def test_idle_nothing_runs(self):
        o = run(CTL(), [(lvl(0), 3)])
        self.assertEqual((o.p1_run, o.p2_run), (False, False))

    def test_lead_starts_at_lead_float(self):
        o = run(CTL(), [(lvl(2), 1)])
        self.assertEqual((o.p1_run, o.p2_run), (True, False))

    def test_lag_waits_for_delay(self):
        c = CTL()
        o = run(c, [(lvl(3), 4)])
        self.assertEqual((o.p1_run, o.p2_run), (True, False))
        o = run(c, [(lvl(3), 2)])
        self.assertEqual((o.p1_run, o.p2_run), (True, True))

    def test_pump_down_continues_below_lead_float(self):
        c = CTL()
        run(c, [(lvl(2), 1)])
        o = run(c, [(lvl(1), 1)])  # level fell below lead float, still above off float
        self.assertTrue(o.p1_run, "pump must keep running until the OFF float drops")

    def test_stops_at_off_float(self):
        c = CTL()
        run(c, [(lvl(2), 1)])
        o = run(c, [(lvl(0), 1)])
        self.assertEqual((o.p1_run, o.p2_run), (False, False))

    def test_alternates_each_cycle(self):
        c = CTL()
        run(c, [(lvl(2), 1), (lvl(0), 1)])
        o = run(c, [(lvl(2), 1)])
        self.assertEqual((o.p1_run, o.p2_run), (False, True))

    def test_hoa_off_pump_never_runs(self):
        o = run(CTL(), [(lvl(2, p1_auto=False), 1)])
        self.assertEqual((o.p1_run, o.p2_run), (False, True))

    def test_seal_fail_pump_never_runs_and_alarms(self):
        o = run(CTL(), [(lvl(2, p1_seal_fail=True), 1)])
        self.assertEqual((o.p1_run, o.p2_run), (False, True))
        self.assertIn("seal_fail_p1", o.alarms)

    def test_overtemp_pump_never_runs(self):
        o = run(CTL(), [(lvl(2, p1_overtemp=True), 1)])
        self.assertFalse(o.p1_run)

    def test_both_faulted_alarms(self):
        o = run(CTL(), [(lvl(2, p1_seal_fail=True, p2_overtemp=True), 1)])
        self.assertEqual((o.p1_run, o.p2_run), (False, False))
        self.assertIn("no_pump_available", o.alarms)

    def test_high_level_alarm(self):
        o = run(CTL(), [(lvl(4), 1)])
        self.assertIn("high_level", o.alarms)

    def test_float_fault_detected(self):
        o = run(CTL(), [(Inputs(fs1_off=False, fs2_lead=True), 1)])
        self.assertIn("float_fault", o.alarms)


if __name__ == "__main__":
    unittest.main()
