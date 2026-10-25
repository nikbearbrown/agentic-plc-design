# Syllabus

## Executive summary

Thirteen modules, about 40 to 50 hours of hands-on work, designed to be done over 8 to 12 weeks alongside a full-time job. Each module takes 2 to 5 hours. You build one project (a duplex lift station workflow) and learn the agent skills by using them on it. The course assumes you can read a ladder schematic and know what a panel is for. It assumes no programming.

## Prerequisites

- You can read an electrical ladder schematic and a panel layout.
- You are comfortable with a spreadsheet.
- A computer where you may install software, and Python 3.11+.
- A habit of checking things. That is the actual prerequisite.

## Sequence and time

| Module | Hours | Depends on | Evidence you finished |
|---|---|---|---|
| 00 Orientation | 2 | none | `./check.sh` passes; first agent session logged |
| 01 Teach the agent your trade | 3 | 00 | Your corrected control narrative |
| 02 The 10 percent | 3 | 01 | A new variant file that passes `apd.py check`, and one rule you added |
| 03 Lists that cannot drift | 4 | 02 | I/O list, BOM and a cross-check report for a variant |
| 04 Drawing edits by script | 4 | 03 | A dry-run log from a copy of a real or sample drawing |
| 05 The oracle | 3 | 01 | A test table you wrote yourself, and the flawed controller's faults named |
| 06 Logic you can read | 5 | 05 | Test vectors run against a compiled program, or a recorded reason they could not |
| 07 Check the math | 3 | 02 | `nec-extracts.toml` verified and signed, or a list of corrections |
| 08 Read the spec | 3 | none | A checklist where every row survives `apd.py spec` |
| 09 The 2 AM call | 3 | 05 | A field runbook and a triage of the sample log |
| 10 Build your own agent kit | 4 | 00-09 | Your own skill, hook and reviewer subagent |
| 11 Capstone: a new job | 6 | all | A review packet for a real job from your shop, gates signed by you |
| 12 Staying current | 2 | all | A completed tool-intake sheet for one new tool |

## How you are assessed

There are no grades in this repo. The assessment is the work product and the **AI Use Disclosure** at the end of each module: two sentences saying what the AI produced and one thing it could not determine that needed your judgment. If an instructor runs this as a course, the instructor reads the disclosures and the signed gates; those carry the grade.

## Pace

If you only have an hour a night, do one lab step a night and stop at the "Done when." Never skip the validation exercise to save time: it is the part that prepares you for the day the tools change.

## Executable expansion and teaching order

Add about 18–24 hours using [the ten-lab spine](labs/README.md), for roughly 60–75 hours total including the original design work. These are teaching estimates, not measured learner completion times. Insert Lab 00 after orientation; Labs 01–03 alongside Modules 05–06; Lab 04 with incident diagnosis; Labs 05–07 with agent-kit work; and Lab 08 as the synthetic, account-free capstone. The legacy customer-job capstone remains optional and requires company-policy permission.

Use the [100-point rubric](labs/08-capstone.md) for a classroom assessment. The original modules' AI Use Disclosures remain required. A passing grade does not sign STATUS gates. The electrical-table and CAD branches remain unverified until reviewed/run by the appropriate human; they do not block the simulation-only spine.

## End-of-course case studies

Finish with [four case studies](case-studies/README.md): TIA Portal Openness MCP, totally-integrated-claude, TwinCAT agent, and the adjacent evidence-driven repair workflow. Allow another 3–4 hours for intake comparisons and local executable adaptations. Vendor tools are discussed and attributed; only the course's simulation exercises run here.
