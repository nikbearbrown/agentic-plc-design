## Executive summary

The course expansion is being authored on `course/open-source-plc-labs`. The original working tree was clean at `05044ce`; all 31 original tests passed. Work is local only. No gates are signed, and no industrial endpoint is used.

## Checkpoint 1 — 2026-10-25

- Inspected README, syllabus, all module headings, existing Structured Text, Python model, tests, repository and ancestor instructions, local `.agents/skills` inventory, and Codex memory directory (empty). The available local skills concern media generation and do not apply to this course build.
- Selected official Beremiz MatIEC for a native IEC Structured Text-to-C experiment. Downloaded commit `3a41303bcb4e50403417bc39c63f88981d7d961e` and pinned GNU build dependencies. macOS ships Bison 2.3; MatIEC requires at least 2.4. Isolated tools are being built in `.toolchain/`.
- Source material remains in `modules/`, `project/`, and `reference/`. New runnable spine will be in `labs/`; machine-readable index will be `labs/manifest.json`. The companion website may ingest these files read-only.
- The user's full-course authoring request supersedes the one-step learner pace for this authoring task. Human engineering decisions and all existing unsigned gates remain human-only.
- Next: compile native control code, record a first executable milestone, expand lab instructions, run an independent learner review, repair and rerun, then commit locally.

## Boundaries

DraftSight, OpenPLC, Studio 5000 and real hardware are NOT VERIFIED. Electrical reference tables remain unverified. Compiled logic in a course scan harness is not a production PLC runtime or a safety certification.

## Checkpoint 2 — native execution and complete lab draft

The pinned installer completed. Actual MatIEC-compiled starter, timer/counter/edge, duplex and legacy programs ran through the native C harness. The station suite exercised 1024 fresh input images plus stateful histories; three compiled mutations were rejected. Normal toy-plant run had zero spill; both-trip produced 84400 mL simulated spill. Legacy comparison found two timing differences in 37 rows. See labs/VERIFICATION.md.

Nine lab documents now live in labs/, with manifest.json, source examples, expected scenarios, solutions and an offline trace viewer. End-of-course case studies include local executable adaptations for three direct PLC tools and an adjacent testing/debugging workflow. BearBrown source audit is recorded under reference/ and labs/evidence/. A concurrently supplied checkpoint commit 8449838 included the first lab files and three case studies; it is preserved.

Next: independent learner run, repairs, browser check, final regression and execution ledger. No hardware, publication or engineering gate signatures.

## Final checkpoint — independent learner and verification complete

Nine executable labs and four end-of-course case studies are complete as simulation-only teaching drafts. The independent learner completed the documented path and supplied predictions, extra scenarios, copied repairs, a fourth mutation and a review packet. Five reported defects were repaired and independently rerun. Final execution used implementation commit `316e68e4a90ee66aff773d9720ee7e269ae755fb`; that concurrently supplied byline commit and the earlier case-study commit were preserved.

`REQUIRE_COMPILED=1 ./check.sh` and the compiled mutation suite passed. Execution receipts, hashes, raw outputs, selected CSVs, platform/limitations and learner findings are under `labs/evidence/`, `labs/VERIFICATION.md` and `labs/LEARNER-REPORT.md`. The browser denied a file-URL view of the offline HTML, so visual interaction remains NOT VERIFIED; generation/data/syntax checks completed without bypassing policy. Vendor runtimes, real devices, electrical tables and human review remain unverified/unsigned.

Website integration handoff: read `labs/manifest.json` plus `case-studies/README.md` at the final committed course revision. New paths requiring an explicit website import-allowlist decision are `labs/*.md`, `labs/solutions/README.md`, `labs/scenarios/*.json`, `labs/plc/*.st`, `labs/toolchain.lock.json`, selected `labs/evidence/*`, `case-studies/*.md`, `reference/open-source-toolchain.md`, and `reference/bearbrown-plc-inventory.md`. Source executable scripts stay in the course repository unless separately reviewed for downloads. No website files were changed by this task.

Remaining next action belongs to the human: review the synthetic failure/restart policy and teaching content, without mistaking software execution for field approval. No pending author code fix is known. No publication, device action, reference-table verification or gate signature was performed.
