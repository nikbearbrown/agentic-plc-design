## Executive summary

An independent learner agent followed Labs 00–08 and all four executable case-study adaptations on 2026-10-25, starting from source checkpoint `a934e37`, followed by the coordinated author repairs recorded below. The parent reported that another session captured the implementation/evidence in commit `316e68e`; this learner did not commit or modify that commit. The supplied course commands executed locally with MatIEC-compiled Structured Text (ST) and a native C scan harness. Added scenarios, three supplied compiled mutations, two scratch repairs, the original-tools capstone, and the final complete check ran. Five substantive learner findings were repaired by the author and independently rerun. No reference program, live device, engineering gate, verified table or vendor project was changed by this learner.

This is a software-learning report, not human engineering approval. Clean tool installation, browser viewing/interaction, vendor runtimes, real hardware, electrical-code correctness, and real hydraulic behavior remain **NOT VERIFIED**. The parent explicitly authorized complete-course learner verification despite the normal module stopping rule. I did not appoint myself as the +1 or sign a gate.

## Environment and reproducibility

Working directory: `/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design`. Python 3.14.6; macOS 26.5.1 ARM64; existing Apple Clang 21.0.0 host tools, Make 3.81, Flex 2.6.4, Perl 5.34.1, curl 8.7.1. The build selected existing Homebrew Clang 22.1.7, not the Apple `cc` shown by the environment probe. MatIEC commit: `3a41303bcb4e50403417bc39c63f88981d7d961e`.

I ran `python3 --version`, `cc --version`, `c++ --version`, `make --version`, `flex --version`, `perl -v`, `curl --version`, the documented `apd.py --help`, bootstrap dry run, and `python3 scripts/bootstrap.py --apply --offline`. The latter verified cached archive hashes, found all five installed stamps and printed `Already built` for M4, Autoconf, Automake, Bison and MatIEC, then `READY`. I separately checked each cached archive and stamp hash against the lock. **Reused:** all source-built tools and the host SDK/compiler prerequisites. **Not run:** fresh downloads, extraction, configure, make, install, clean-machine setup, paid accounts or secret setup. No vendor package was installed.

Fresh control builds did run in `/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/build/learner`. MatIEC translated ST to C, then Clang compiled the generated C and course harness into a native executable. Python drove input images and checked native outputs; Python did not execute the control algorithm. Source and executable identities are in [learner build receipt](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/learner/build.json) and [file hashes](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/learner/file-hashes.json). Initial/final native executable SHA-256: `597255c20c4f990e4e567f1572d4cb24fc898b6e5d779b482ccc1550fded34ce`. ST reference source SHA-256: `2ad97d9fd2923e9c4869cebf5cdf45b5e45f108ad92c4cc35f44646312183161`.

The command log [actual commands, exits, stdout and stderr](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/learner/commands.jsonl) contains the core build, replay, plant, mutations, repairs, capstone and rerun commands. Paths in those command arrays were relative to the absolute working directory above. Early version probes and the first original-only `./check.sh` are summarized here; they predate creation of that log. The log deliberately preserves expected failures; exit 1 is not automatically a course failure.

## Results by lab

| Lab | Executed work and observed result |
|---|---|
| 00 | Bootstrap dry run; offline cached-tool reuse; build dry run then native build with `--build-dir build/learner`; foundations PASS. |
| 01 | Eight fresh starter combinations and stateful sequence passed. Direct native stdin protocol returned `1`, `1`, `0` for the documented three scans. |
| 02 | Seven-row timer replay matched; copied 501 ms boundary and a FALSE-at-400/TRUE-at-450 glitch scenario passed, with done at 950 ms and not 949 ms. |
| 03 | Eight-row cycle and station suite passed: alternation, availability/fallback, faults, cold restart, five-second boundary, chatter, 1,024 fresh input images. Four added replays passed for recovery after lag latches, invalid-float recovery without alternation, total availability outage resetting timing, and cold start at high level. |
| 04 | Normal plus pump1-trip, both-trip, bad-float and blocked-pump1 ran for 1,800 scans each. Repeat CSV compared byte-identical with `cmp` exit 0. Offline HTML was generated and source inspected; browser UI not exercised. After the input-image bug was repaired, all five traces were regenerated. |
| 05 | Mutation dry run then actual builds rejected ignore-health, instant-lag and no-alternation. Scratch zero-delay program compiled successfully, station test failed `lag too early`, restoring only the preset passed the same station suite. Minimal counterexamples were run independently. |
| 06 | Original unchanged ST compared against Python across 37 rows; exactly two pump-command mismatches observed: T02 and T07 at t=5 s. |
| 07 | Fresh rebuild, complete native `test`, mutation suite, complete check, evidence packet and unsupported-claim review completed. |
| 08 | Baseline `apd.py check`, `io` and `bom` all exited 0; original I/O/BOM inspected; all required plant faults and compiled behavior included. Electrical catalog/sizing values remain **unverified**. No construction package or engineering approval produced. |

Final `env REQUIRE_COMPILED=1 ./check.sh` exited 0 after the author repairs. It ran 31 original unit tests, expected failure of the flawed original model, AutoLISP generation/lint, manifest/link checks, scenario-input rejection, malformed native-frame rejection, optimized-Python rejection and compiled scan/plant/comparison tests. The native suite was also run separately against the independent learner build. Top-level check uses the existing reference build and writes its generated test traces; that final command was specifically requested by the parent. Three pre-existing `ResourceWarning: unclosed file` messages in original tests remain visible in stderr; this is a passing run with warnings, not warning-free output.

## Predictions and learning

Predictions were saved in [predictions.md](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/scratch/learner/predictions.md), before solutions were opened. Fresh-state truth outputs were predicted off except 111; stateful outputs `1,1,0,0,0`; timer at 499 ms off/500 ms on; glitch reset completion 950 ms; invalid shutdown preserves lead; availability recovery starts a new timer. Execution supported these predictions. Resetting every scan would lose the seal-in at the second scan; a start OR outside stop/health parentheses can defeat stop precedence. A command does not determine welded-contact behavior: **CANNOT-DETERMINE**.

Two limits to independence are explicit. First, lab prose already reveals several answers, so this was not a blind examination. Second, while trying to strip expected fields from the cycle JSON I filtered `expect` instead of `expected`, accidentally revealing those fields; broad cycle predictions had been written, but a complete blind eight-row answer had not. I did not read the solutions until after baseline predictions, native tests, extra scenarios and the first repair.

My proposed one-scan instant-lag counterexample was wrong: this MatIEC TON with a zero preset remains incomplete on the first TRUE invocation and finishes on the next TRUE scan. The one-scan replay passed; a revised two-scan sequence at 0 and 100 ms failed with actual `(1,1)` versus expected `(1,0)`. This correction is preserved rather than claiming the initial prediction succeeded. The original station suite already caught the defect at 4,900 ms.

All scenario copies are under `/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/scratch/learner`. Timer and added station CSV evidence is under `/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/learner`; their full traces are also under `/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/build/learner`.

## Plant observations

All quantities below are invented simulation outputs under synthetic R8, not equipment sizing or values taken from electrical reference tables.

| Scenario | First relevant alarm | First spill | Total spill | Interpretation |
|---|---|---|---:|---|
| Normal | None | None | 0 mL | First demand 16.7 s, first drained/lead-2 transition 33.4 s, first lag latch 83.4 s. Maximum 72,500 mL. |
| Pump 1 trip | No exposed high/invalid/no-pump alarm | None | 0 mL | Availability logic excludes tripped pump and permits fallback; individual trip alarm is not exposed by this sample. |
| Both trips | No-pump 58.5 s, high 69.6 s | 72.9 s | 84,400 mL | Specified plant failure was observed. No-pump waits for demand; fault window starts earlier at 40.0 s. |
| Bad float | Invalid 58.5 s, high 69.6 s | 72.9 s | 84,400 mL | Controller stops for contradictory sensed inputs. Initially a false low float alone can look like a valid low level; fault onset need not immediately cause invalid_alarm. |
| Blocked pump 1 | None | None | 0 mL | Initiating blocked-flow fault has no direct feedback and is not diagnosed. |

Blocked-pump total simulated outflow was 368,100 mL versus 387,900 mL if every command had produced the nominal toy outflow. This is the concrete distinction between a command and actual modeled effect. The first spill row records volume before the scan's update; spill belongs to the update after that row's command. Details: [plant-events.json](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/learner/plant-events.json).

Proposed feedback requirement, **HUMAN DECISION PENDING**: after a run command and an approved startup allowance, require independently measured run/flow feedback within a human-selected timeout; define alarm, fallback, reset and restart policies explicitly. No numeric production timeout was invented, implemented or approved.

## Failure, repair and case-study evidence

The zero-delay repair changed only `PT := T#0s` back to `PT := T#5s` in `/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/scratch/learner/station-repair.st`. A zero preset contradicts R5's five elapsed seconds; it was a behavioral defect, not a syntax error. Both builds compiled; the failing build receipt, exact failing station output, [minimal diff](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/evidence/learner/repair.diff) and passing unchanged test are retained. A compiler error would not count as rejection by a behavioral test. Reference ST and expected values were unchanged.

Case 1's blueprint cycle replay produced eight rows, then a copy with an intentionally wrong second-cycle pump expectation failed at row 4 (expected pump 1, actual pump 2). Case 2 reproduced the legacy mismatch and passed the new station suite. Case 3 ran foundations and the portable timer replay. Case 4 repeated the mutation/repair approach and added a fourth mutation: force high_alarm FALSE. One high-level scan failed its explicit expected high alarm; the existing station suite also rejected it. Restoring the original high alarm assignment in `/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/scratch/learner/station-fourth.st`, rebuilding, and rerunning both tests passed. Thus this fourth fault was a code defect that existing tests already detected, not a coverage gap.

The adjacent test-driven-development and systematic-debugging source definitions named by Case 4 were read as course source material. The local fail–repair–rerun adaptation ran; neither full upstream vendor product nor an entire upstream skill protocol was installed or claimed executed. No strict test-first authorship claim is made for the existing course.

| Transfer/context item | Supported evidence | Limit |
|---|---|---|
| ST language subset | Starter, Timing, Station and original DuplexLeadLag compiled and ran with pinned MatIEC. | TwinCAT ExST and Siemens language extensions **NOT VERIFIED**. |
| Compiler | Native receipts and compiler logs present. | TIA/TwinCAT vendor compilation **NOT VERIFIED**. |
| Runtime | Local course C harness and 37 legacy observations present. | Vendor scheduling, online operations and PLC hardware configuration absent. |
| Host | Native ARM64 macOS run observed. | Windows/Linux setup and Windows vendor automation **NOT VERIFIED**. |
| License | Course inventory distinguishes compiler dependencies and vendor/adjacent-source licenses. | No fresh legal assessment or independent upstream license verification by this learner; vendor-use permission **CANNOT-DETERMINE**. |

Confirmed finding for Case 2: t=5 pump mismatch in two legacy scenarios. Limitation: comparison covers pump commands only, not full alarm equivalence. Human question: what timing convention and inconsistent-sensor behavior does the actual owner approve? A workflow manipulating TIA Portal requires its engineering environment; a skill or MCP interface does not supply an open-source macOS PLC runtime.

## Requirement-to-evidence matrix

All quotes below are verbatim from [SPEC.md](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/SPEC.md) sections R1–R8. These are synthetic requirements, not code-book facts.

| Section and exact quote | Code location | Test evidence | Limitation |
|---|---|---|---|
| R1: “Each scan shall read one complete Boolean input image, compute the control logic once, and expose one output image. A TRUE float means liquid is at or above its threshold. Tests shall provide monotonic integer milliseconds; a reset starts a new simulated run.” | [harness.c](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/runtime/harness.c) | Native frames and protocol rejection | No field sampling/scheduling evidence |
| R2: “A pump is available only when its Auto input is TRUE and neither its seal-failure nor overtemperature input is TRUE. An upper float TRUE with the adjacent lower float FALSE shall raise invalid_alarm and inhibit both pump commands in that scan.” | [station.st](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/plc/station.st) | 1024 fresh images, invalid replay and health mutation | Synthetic inhibition policy may worsen overflow |
| R3: “With consistent floats, the lead float shall set demand. Demand shall remain set while only the off float remains TRUE and shall clear when the off float is FALSE. On a valid demand-to-no-demand transition, the lead selection shall alternate once. Invalid sensors shall clear demand without alternating the lead.” | [station.st](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/plc/station.st) | Cycle, invalid recovery, no-alternation mutation | Not all stored-state histories |
| R4: “During demand the selected available lead pump shall run. If it is unavailable, the other available pump shall run immediately. Neither pump shall run while unavailable. If neither is available during demand, no_pump_alarm shall be TRUE.” | [station.st](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/plc/station.st) | Fallback, availability and post-lag recovery replays | No run/flow feedback |
| R5: “With demand, the lag float TRUE, and at least one available pump, a TON shall measure elapsed time beginning at the first scan that observes those conditions. At 5000 ms elapsed, the second available pump shall join. The lag request shall then remain latched until demand clears. Before completion, a FALSE timer input shall reset elapsed time.” | [station.st](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/plc/station.st) | 4900/5000 boundary, chatter/outage, delay mutation/repair | No real scan jitter/hardware timer evidence |
| R6: “high_alarm shall equal fs4_high independently of pump availability. invalid_alarm shall indicate contradictory adjacent floats. no_pump_alarm shall indicate demand with neither pump available. Alarms shall clear when their conditions clear.” | [station.st](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/plc/station.st) | High/invalid/no-pump assertions and fourth mutation | No alarm acknowledgement/history |
| R7: “A cold reset shall clear latch and timer state, select pump 1 as lead, and then evaluate the new input image. If valid start conditions are present, a pump may run in that first scan.” | [harness.c](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/labs/runtime/harness.c) | Cold high-level start and station reset tests | No warm/retained restart model |
| R8: “The plant shall update after each controller scan using integer millilitres. The next volume shall equal the current volume plus inflow minus actual outflow, clamped at zero and at 100000 mL. Volume above that ceiling shall be recorded as spill.” | [lab.py](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/scripts/lab.py) | Repeat plant traces and first-spill observations | Toy integer volume, no real hydraulics |

## Original-model review and capstone interface

At first lag TRUE t=1 s, the legacy Python model adds one second immediately; at t=5 it has counted five seconds and requests both pumps. MatIEC TON has seen only four elapsed seconds and waits until t=6. New R5 explicitly chooses elapsed time from the first observed qualifying scan. The old synthetic narrative's Sequence of operation item 4 says, “If the level continues to rise to the Lag float, the lag pump starts immediately to prevent overflow.” That draft is explicitly planted with errors, not an approved five-second sampling convention. Approval for changing the old model is **CANNOT-DETERMINE**. A proposed correction would store the first TRUE timestamp, calculate elapsed time from it, and revise T02/T07 expectations at t=5 only after a human settles the narrative. It was written here, not implemented.

Original I/O and BOM: [io.csv](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/scratch/learner/capstone/io.csv) and [bom.csv](/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/scratch/learner/capstone/bom.csv). The BOM retains its **unverified** banner and invented part numbers; no numbers were verified against a code book. The original I/O includes running feedback, fail lights, beacon and silence input absent from the compiled interface. Its DI/DO labels are document assignments, not real inspected I/O addresses. The simulation has Auto booleans but no Hand control, acknowledgement, real feedback, real wiring, retained restart state or certified safety functions. The original variant system's options are not all implemented by this controller.

## Findings and author repairs

| Finding | Before | Independent rerun after repair |
|---|---|---|
| Top-level check claim exceeded execution | README promised executable checks, but check.sh ended after the original tests and LISP lint. | `REQUIRE_COMPILED=1 ./check.sh` passed full native and metadata/protocol checks; missing compiled build cannot silently satisfy this mode. |
| Mutation directory option ignored | `--build-dir` parsed but outputs hard-coded to build/<mutant>. This conflicted with isolated learner work. | Dry run and actual mutations stayed under `/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/build/learner-mutations/mutants`. |
| Fault trace displayed wrong sensor image | At 58,500 ms bad-float CSV displayed fs1=1, fs2=1 with invalid_alarm=1 although controller received fs1_off=0. | CSV now separates physical level and all actual inputs; same row has physical_level_index=2, fs1_off=0, fs2_lead=1, invalid_alarm=1. All fault traces regenerated; native full suite checks their consistency. Before/after rows preserved. |
| Misspelled scenario inputs ignored | `p1_overtemper=1` was silently discarded and replay passed a healthy-pump expectation. | Same scenario exits 1 with `Unknown input keys: p1_overtemper`. Valid scenarios still pass; invalid value/level checks also run in full check. |

Minor root-relative path ambiguity in lab README/SPEC was also reported and corrected by the author. The fifth finding was a weak legacy-comparison guard: it checked mismatch count alone. The author changed it to assert the exact two scenario/time/output tuples. A final independent comparison rerun and full check both passed with T02/T07 at t=5, Python (1,1), compiled (1,0). Thus a future relocation with the same mismatch count cannot silently pass this guard. No legacy program/model behavior was changed.

## Unsupported-claim critique

| Synthetic claim | Judgment |
|---|---|
| “The motor ran for ten seconds, so the pump moved the required flow.” | **CANNOT-DETERMINE** from commands. Simulated blocked-flow experiment is a counterexample to the inference. |
| “The AI's Python simulator proves the PLC is safe.” | Contradicted as an evidence claim: this is a toy plant and limited native behavior, without field validation. |
| “All 1024 combinations passed, so all possible histories were covered.” | Contradicted: fresh images do not exhaust stored-state/time histories. |
| “The NEC table is correct because the checker used it.” | **CANNOT-DETERMINE**; arithmetic on an unverified source leaves its values unverified. |
| “OpenPLC was tested because the ST compiled.” | Contradicted: the executed runtime was the course C harness; OpenPLC did not run. |

## Remaining limits and handoff

**NOT VERIFIED:** fresh installation; Windows/Linux setup; browser render, slider and buttons; DraftSight execution; OpenPLC/Beremiz runtime; Studio 5000/TIA/TwinCAT; live hardware/fieldbus; electrical tables and catalog correctness; real pumps, wiring, hydraulic capacity, watchdog/real-time behavior, retained/warm restart, fault tolerance or certification. Full original alarm equivalence is not established. Long-duration/overflow conditions outside the chosen tests remain untested. The feedback extension is only a proposal. Software passes cannot sign G2/G4 or any gate.

Browser action status: the parent attempted to open `file:///Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/build/reference/plant.html` in IAB and received an explicit **DENIED** URL-policy result permitting only HTTP/HTTPS, including an instruction not to work around that denial. I did not retry, switch surfaces, or serve the file as a bypass. HTML generation, static source inspection and underlying CSV validation completed; visual/interaction verification remains blocked. This is a tool-policy denial, not evidence of a viewer bug.

The review packet is `/Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design/scratch/learner/review-packet`. Engineering questions remain for the human, especially whether invalid-sensor inhibition, automatic cold start, fallback/recovery and the absent feedback strategy are appropriate for any real installation. No gate was signed and no deployment was attempted.

AI Use Disclosure: An AI learner executed local commands, wrote scenario copies and this report, and challenged course claims with observed outputs. Human engineering judgment, reference-table verification and field acceptance were not performed by that agent.
