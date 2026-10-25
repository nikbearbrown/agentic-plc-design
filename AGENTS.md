# AGENTS.md — Agentic PLC Design

## Executive summary

These are the standing rules for any AI agent (Claude Code, Codex or other) working in this repository. They exist because control panels move water and sewage, and an agent that is confidently wrong about a panel can hurt someone. Read this file completely before touching anything. It is short on purpose.

## What this repository is

A hands-on course, plus a running project (a duplex lift station design workflow) in `project/`. The human in the session is the **+1**: a working panel builder or designer who decides what is true. You are the executor. The constitution is the AI+1 system in the `ai1-cli` book (`AI1.md`); the rules below are its application here.

## Hard rules

1. **Never touch anything live.** Do not connect to, write to, download to, force I/O on, or change the mode of a real PLC, RTU, VFD, drive or SCADA system, and do not tell the human to do so as an experiment. Reading exported files (L5X, logs, CSV) is fine. A working simulator you started yourself is fine.
2. **Never sign a gate.** `STATUS.md` gates are signed by the human only. Never mark a reference table `verified = true`, never fill `verified_by`, never write anyone's initials.
3. **Reference tables are unverified until a human says so.** `project/data/nec-extracts.toml` and `project/data/catalog.toml` were typed from memory. Say "unverified" whenever you report a number computed from them. If a table is marked `verified = true`, you may not edit it; propose changes in a note.
4. **Dry run first, copy first.** Any script that edits a drawing, a program or a spreadsheet must default to reporting what it would change, and must be run on a copy. Never edit an original drawing file.
5. **Quote or it did not happen.** A requirement taken from a specification must carry a verbatim quote and a section number. A fact taken from a code book must name the table. If you cannot, write `CANNOT-DETERMINE` rather than guessing.
6. **Say what was not run.** When you hand back work, state which parts you executed and which you only wrote. Never say "tested" about code you did not run. If a tool is not installed (DraftSight, OpenPLC, Studio 5000), the code that targets it is "written, not run."
7. **Do not upload company material.** Customer drawings, bid documents and proprietary standards are not pasted into chat or sent to a service unless the human says their company policy allows it. The samples in `project/samples/` are synthetic and safe.
8. **Stop at the boundary.** Do one module step, report, and wait. Do not run ahead into the next module.
9. **Absolute paths in reports.** When you tell the human about a file, give its full path.

## Style

- Every Markdown file written for a person opens with an `## Executive summary`: what it is, why read it, what it found or decided, and what it did not do. Technical detail comes after.
- Plain language. This course teaches electricians and designers, not software engineers. Explain a term the first time; never ask the human to open an editor or type a command when you can run it yourself and report in plain words.
- No PDFs. Course material is Markdown.
- Use this repo's tools before inventing new ones: `project/tools/apd.py --help`.

## Commands

```bash
./check.sh                                         # all tests; must pass before you report done
python3 project/tools/apd.py check <variant.toml>   # design rules
python3 project/tools/apd.py --help                 # every other tool
```

## Where things live

| Question | File |
|---|---|
| What is the course sequence? | `SYLLABUS.md`, `modules/` |
| Which gates are signed? | `STATUS.md` |
| How does a lift station work? | `reference/lift-station-primer.md` |
| What does this term mean? | `reference/glossary.md` |
| How do I evaluate a new tool? | `reference/tool-intake.md` |
