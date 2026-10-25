## Executive summary

Predictions written before opening solutions or expected scenario fields. No field behavior is asserted.

Lab 01: fresh rows 000,001,010,011,100,101,110 all off; 111 on. Stateful outputs 1,1,0,0,0. Resetting every scan loses the latch at the second scan. `(old AND stop_ok AND healthy) OR start` incorrectly permits a start with absent stop permission. Welded contacts cannot be determined from this command.

Lab 02: initial TRUE at 0 means ET=0, Q=0; at 499 Q=0, at 500 Q=1; FALSE at 600 Q=0 ET=0; next rising edge count 2; reset count 0. Moving 500 to 501 remains done. FALSE at 400 then TRUE at 450 moves completion to 950 ms, with 949 still off. A one-scan glitch must reset the timer; six samples 0..500 span five intervals, 500 ms.

Lab 03 general: valid demand starts pump 1, lag joins at first qualifying scan+5000 ms; off float alone sustains demand; empty clears and alternates to 2. Pump 2 trip after next-cycle start falls back to 1; both trips leaves demand but no commands, no-pump alarm true. Invalid sensors clear demand without alternating; valid start afterward keeps the selected lead. A cold reset at high starts pump 1 and high alarm immediately but no lag until five seconds later. No availability before completion resets elapsed; return establishes a new zero.

Lab 04: both-trip accumulates volume and should spill; no-pump alarm starts upon demand, high at high threshold. Blocked pump 1 still receives commands but contributes no actual outflow during its fault: command cannot prove flow. No flow feedback means the initiating failure is invisible directly.

Lab 05 smallest counterexamples: ignore-health: reset with lead demand and pump 1 fault -> reference pump 2 only, mutant pump 1 wrongly on (R2/R4). Instant lag: reset with three floats -> only pump 1, mutant both (R5). No alternation: lead-demand scan then empty -> lead 2 expected, mutant 1 (R3).

Lab 06: legacy Python credits its first TRUE scan one second, so t=1 onset produces join t=5 versus compiled TON t=6. Old narrative exact convention needs evidence; cannot infer approval to change it.

Case 4 fourth mutation prediction: high_alarm forced FALSE violates R6 on a single consistent all-four-floats input. This is a code bug, not an absent requirement.

Observed correction: the zero-preset MatIEC TON does not finish on its initial TRUE scan. My one-scan instant-lag counterexample survived; revised distinguishing sequence keeps lag TRUE at t=100 ms, still before the required 5000 ms. Predictions are not proof. The baseline cycle expected fields were accidentally displayed while trying to strip the wrong key (expect versus expected); broad cycle predictions preceded that display, but an independent eight-row blind prediction was not completed.
