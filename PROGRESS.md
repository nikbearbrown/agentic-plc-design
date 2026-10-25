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
