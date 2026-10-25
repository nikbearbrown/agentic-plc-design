## Executive summary

The expanded course was executed on 2026-10-25 with actual MatIEC-compiled Structured Text, native LLVM machine code and a deterministic course C scan harness on Apple Silicon macOS. An independent learner completed Labs 00–08 and all four case-study adaptations, found five substantive issues, and reran the repairs. Final checks pass with documented compiler/test warnings. No production PLC runtime, vendor IDE, field device or human engineering gate was claimed verified.

Repository root: `/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design`. Final execution source checkpoint: **`316e68e4a90ee66aff773d9720ee7e269ae755fb`**. Later evidence/documentation commits do not change tested implementation. Exact commands, exits, source hashes and UTC execution time are in [verification.json](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/verification.json). The learner began at `a934e37` and independently reran coordinated repairs.

## Executed commands and results

| Command (from repository root) | Actual result | Saved output |
|---|---|---|
| `python3 scripts/bootstrap.py` | Dry-run plan; no installation | Described in setup/learner report |
| `python3 scripts/bootstrap.py --apply --offline` | Author source-built all five pinned packages under `.toolchain/`; final and learner reruns verified cached archives and reused installed tools; exit 0 | [final reuse log](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/run-00.txt) |
| `python3 scripts/lab.py build --apply` | MatIEC translated ST; LLVM compiled native executable; exit 0 | [build log](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/run-01.txt), [build receipt](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/build.json) |
| `REQUIRE_COMPILED=1 ./check.sh` | 31 original tests; flawed original controller rejected; LISP lint; course metadata/links; malformed input rejection; actual native and plant tests all passed; exit 0 | [full final check](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/run-02.txt) |
| `python3 scripts/lab.py mutations --apply` | Three deliberately faulty ST copies compiled and were rejected by behavioral assertions; exit 0 | [mutation log](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/run-03.txt) |
| `python3 scripts/lab.py plant --fault pump1-trip ...` and `--fault blocked-pump1 ...` | 1800 native-control/plant scans each; exit 0 | [trip](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/run-04.txt), [blocked flow](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/run-05.txt) |
| Case-study cycle, legacy comparison and timer replays | Eight-row cycle; exact two known mismatches; seven-row timer; all expected outcomes observed, exit 0 | [case 1](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/run-06.txt), [case 2](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/run-07.txt), [case 3](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/run-08.txt) |
| `python3 scripts/view_trace.py ...` | Offline HTML generated; embedded data equals CSV; JavaScript syntax parses | [generation](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/run-09.txt), [static check](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/viewer-static-check.txt) |
| Learner scratch repairs and capstone commands | Zero-delay defect and an independent suppressed-high-alarm defect reproduced, repaired on copies and passed unchanged tests; original design check/I/O/BOM ran | [learner report](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/LEARNER-REPORT.md), [actual command log](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/learner/commands.jsonl) |

The complete compiled suite includes starter truth table and seal-in, R_TRIG/CTU/TON, 499/500 ms and 4900/5000 ms boundaries, alternating cycles, availability/fallback, contradictory inputs, cold restart, interrupted timing, 1024 fresh Boolean input images, deterministic repeat traces, expected spill scenarios and the legacy-model discrepancy. It does not exhaust all state histories. Expected failing exercises have nonzero subprocess exits preserved in the learner log; they are not silently renamed passes.

## Tested environment and source identity

macOS **26.5.1 build 25F80**, arm64; Python **3.14.6**; native-code compiler **Homebrew Clang 22.1.7**; source-build host compiler **Apple Clang 21.0.0**; Make **3.81**; Flex **2.6.4 Apple build**; Perl **5.34.1**; curl **8.7.1**. Newly downloaded/source-built tools: M4 **1.4.20**, Autoconf **2.72**, Automake **1.18.1**, Bison **3.8.2**, MatIEC commit **`3a41303bcb4e50403417bc39c63f88981d7d961e`**.

Official URLs, archive hashes and licenses are in [toolchain.lock.json](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/toolchain.lock.json) and [toolchain provenance](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/reference/open-source-toolchain.md). Author installation used downloaded official archives; learner installation reused them and existing stamps. A blank-machine prerequisite/SDK installation is **NOT VERIFIED**. No system package, privilege, account, secret or network-service setup was needed. No background service remains running.

## Observed control and plant results

- Original ST/Python comparison: **37 rows, exactly two pump-command differences**, T02 and T07 at t=5 s: Python `(1,1)`, compiled ST `(1,0)`. Original source/model unchanged. The new guard checks exact scenarios/times/values, not just mismatch count. Alarm interfaces are not fully equivalent.
- Normal toy plant: **1800 scans**, maximum **72500 mL**, spill **0**, pump 1 on **648** scans, pump 2 on **563**. Repeated output is byte-identical.
- Both-trip: **84400 mL** simulated spill, **355** high-alarm scans and **315** no-pump-alarm scans.
- Bad float: **84400 mL** simulated spill, **315** invalid-alarm scans. CSV now records actual fault-injected inputs separately from physical level.
- Pump 1 trip and blocked-flow scenarios: no simulated spill in the selected run; blocked flow is not directly diagnosed because feedback is absent. These are invented teaching quantities, not equipment sizing or values from electrical reference tables.

Selected CSVs and JSON summaries are in `/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/`. Complete generated builds/logs and the offline viewer are in `/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/build/reference/`.

## Learner-discovered repairs

1. Integrated compiled checks into the advertised main check command; `REQUIRE_COMPILED=1` prevents an absent binary from silently satisfying it.
2. Made mutation builds honor the requested output directory.
3. Corrected the plant CSV to show actual sensed inputs after fault injection, with separate physical-level data; added regression assertions.
4. Rejected misspelled input keys, invalid level values and non-Boolean overrides before execution.
5. Strengthened comparison from a mismatch-count check to exact expected mismatch tuples.

The learner reran each affected path and added a fourth mutation independently. Its report discloses predictions, an initially wrong zero-preset timer assumption, answer exposure from instructional prose, cached setup, and remaining limits. It is a second AI reader, not a human panel-builder approval.

## Warnings, failures and NOT VERIFIED

The initial harness probe failed until the required MatIEC accessor header was included. A subsequent counter assertion exposed uninitialized C function-block storage; zero-initializing it repaired the integration. Expected values were not weakened. MatIEC generic headers/generated C still produce compiler warnings, summarized in the provenance note and retained in `build/reference/compile.log`. Three existing Python ResourceWarnings remain; passing is not warning-free.

**Denied action:** opening `file:///Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/build/reference/plant.html` in the in-app browser. **Reason:** browser URL policy permits HTTP/HTTPS but blocks `file:`. **Outcome:** denied before viewing; no workaround, alternate browser surface, server bypass or screenshot was attempted. HTML generation, JavaScript syntax and CSV data checks completed. Browser layout, slider/buttons, accessibility and screenshots remain **NOT VERIFIED**.

Also **NOT VERIFIED:** OpenPLC runtime/editor, Beremiz IDE/runtime, DraftSight, Studio 5000, TwinCAT, Siemens TIA Portal, real PLC/RTU/VFD/SCADA I/O, fieldbus behavior, actual pumps/hydraulics/wiring, hard-real-time scheduling, safety certification, complete IEC conformance, Linux/Windows/Intel macOS. Electrical reference tables remain **unverified**. The feedback-timeout extension is only proposed. Human gates remain unsigned. This task made no push or deployment.
