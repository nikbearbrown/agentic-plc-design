(* Synthetic teaching functions. No physical I/O addresses. *)
FUNCTION_BLOCK Starter
VAR_INPUT
  start_button, stop_ok, motor_healthy : BOOL;
END_VAR
VAR_OUTPUT
  motor_run : BOOL;
END_VAR
(* Stop and health dominate a simultaneous start. *)
motor_run := (motor_run OR start_button) AND stop_ok AND motor_healthy;
END_FUNCTION_BLOCK

FUNCTION_BLOCK Timing
VAR_INPUT
  signal : BOOL;
  reset_count : BOOL;
END_VAR
VAR_OUTPUT
  edge : BOOL;
  count : INT;
  done : BOOL;
  elapsed : TIME;
END_VAR
VAR
  rising : R_TRIG;
  events : CTU;
  delay : TON;
END_VAR
rising(CLK := signal);
events(CU := signal, R := reset_count, PV := 3);
delay(IN := signal, PT := T#500ms);
edge := rising.Q;
count := events.CV;
done := delay.Q;
elapsed := delay.ET;
END_FUNCTION_BLOCK
