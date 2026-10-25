(* Reference for synthetic contract labs/SPEC.md, not a field design.
   Separate from the original unreviewed project/plc/lead_lag.st.
   R1 sample image; R2 inhibit; R3 demand; R4 selection;
   R5 lag TON; R6 alarms; R7 nonretentive restart. *)
FUNCTION_BLOCK Station
VAR_INPUT
  fs1_off, fs2_lead, fs3_lag, fs4_high : BOOL;
  p1_auto, p2_auto : BOOL;
  p1_seal_fail, p2_seal_fail, p1_overtemp, p2_overtemp : BOOL;
END_VAR
VAR_OUTPUT
  p1_run, p2_run, high_alarm, invalid_alarm, no_pump_alarm : BOOL;
  lead : INT := 1;
  demand, lag_latched : BOOL;
END_VAR
VAR
  available1, available2, previous_demand : BOOL;
  delay : TON;
END_VAR
high_alarm := fs4_high;
invalid_alarm := (fs4_high AND NOT fs3_lag) OR
                 (fs3_lag AND NOT fs2_lead) OR
                 (fs2_lead AND NOT fs1_off);
available1 := p1_auto AND NOT p1_seal_fail AND NOT p1_overtemp;
available2 := p2_auto AND NOT p2_seal_fail AND NOT p2_overtemp;
previous_demand := demand;
IF invalid_alarm OR NOT fs1_off THEN
  demand := FALSE;
ELSIF fs2_lead THEN
  demand := TRUE;
END_IF;
(* Only a valid drained cycle alternates; invalid sensors do not count. *)
IF previous_demand AND NOT demand AND NOT invalid_alarm THEN
  IF lead = 1 THEN lead := 2; ELSE lead := 1; END_IF;
END_IF;
delay(IN := demand AND fs3_lag AND (available1 OR available2), PT := T#5s);
IF NOT demand THEN
  lag_latched := FALSE;
ELSIF delay.Q THEN
  lag_latched := TRUE;
END_IF;
p1_run := FALSE;
p2_run := FALSE;
no_pump_alarm := demand AND NOT (available1 OR available2);
IF demand THEN
  IF lead = 1 THEN
    p1_run := available1;
    p2_run := available2 AND (NOT available1 OR lag_latched);
  ELSE
    p2_run := available2;
    p1_run := available1 AND (NOT available2 OR lag_latched);
  END_IF;
END_IF;
END_FUNCTION_BLOCK
