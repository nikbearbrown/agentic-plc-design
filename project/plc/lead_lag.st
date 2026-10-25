(* Duplex lead/lag pump control, IEC 61131-3 Structured Text.
   Written by an AI from the reference model in tools/sim.py.
   STATUS: UNCOMPILED. Not yet run on any PLC, emulator or OpenPLC. Module 6 is where you
   compile it, run tools/vectors.py against it, and decide whether it is right.
   Float inputs are TRUE when liquid is ABOVE that float. *)

FUNCTION_BLOCK DuplexLeadLag
  VAR_INPUT
    fs1_off, fs2_lead, fs3_lag, fs4_high : BOOL;
    p1_auto, p2_auto : BOOL;
    p1_seal_fail, p2_seal_fail : BOOL;
    p1_overtemp, p2_overtemp : BOOL;
  END_VAR
  VAR_OUTPUT
    p1_run, p2_run : BOOL;
    alm_high_level, alm_float_fault, alm_no_pump : BOOL;
  END_VAR
  VAR
    lead : INT := 1;
    lvl : INT;
    call, call_prev, lag_enabled : BOOL;
    avail1, avail2, lead_ok, other_ok : BOOL;
    lead_n, other_n : INT;
    lag_timer : TON;
  END_VAR

  (* level index: 0 none, 1 off float, 2 lead, 3 lag, 4 high *)
  IF fs4_high THEN lvl := 4;
  ELSIF fs3_lag THEN lvl := 3;
  ELSIF fs2_lead THEN lvl := 2;
  ELSIF fs1_off THEN lvl := 1;
  ELSE lvl := 0;
  END_IF;

  alm_high_level := (lvl = 4);
  alm_float_fault := (fs4_high AND NOT fs3_lag) OR (fs3_lag AND NOT fs2_lead) OR (fs2_lead AND NOT fs1_off);

  avail1 := p1_auto AND NOT p1_seal_fail AND NOT p1_overtemp;
  avail2 := p2_auto AND NOT p2_seal_fail AND NOT p2_overtemp;

  (* call latch: set at the lead float, cleared only when the off float drops *)
  call_prev := call;
  IF lvl >= 2 THEN
    call := TRUE;
  ELSIF lvl < 1 THEN
    call := FALSE;
  END_IF;

  IF call_prev AND NOT call THEN
    lag_enabled := FALSE;
    IF lead = 1 THEN lead := 2; ELSE lead := 1; END_IF;  (* alternate each cycle *)
  END_IF;

  (* pick the lead; fall back to the other pump if the lead is unavailable *)
  IF lead = 1 THEN
    lead_n := 1; other_n := 2; lead_ok := avail1; other_ok := avail2;
  ELSE
    lead_n := 2; other_n := 1; lead_ok := avail2; other_ok := avail1;
  END_IF;
  IF NOT lead_ok THEN
    lead_n := other_n;
    IF lead_n = 1 THEN other_n := 2; ELSE other_n := 1; END_IF;
    lead_ok := other_ok;
    other_ok := FALSE;  (* the failed original lead *)
  END_IF;

  lag_timer(IN := call AND lead_ok AND (lvl >= 3), PT := T#5s);
  IF lag_timer.Q THEN
    lag_enabled := TRUE;
  END_IF;

  p1_run := FALSE;
  p2_run := FALSE;
  alm_no_pump := FALSE;
  IF call THEN
    IF lead_ok THEN
      IF lead_n = 1 THEN p1_run := TRUE; ELSE p2_run := TRUE; END_IF;
      IF lag_enabled AND other_ok THEN
        IF other_n = 1 THEN p1_run := TRUE; ELSE p2_run := TRUE; END_IF;
      END_IF;
    ELSE
      alm_no_pump := TRUE;
    END_IF;
  END_IF;
END_FUNCTION_BLOCK
