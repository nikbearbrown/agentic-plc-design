# Glossary

## Executive summary

Plain-language definitions of the terms the course uses, in two groups: the trade terms the agent must get right, and the AI terms you need to direct it. Look here first when a module uses a word you want pinned down.

## Trade terms

- **ACE3600 / MOSCAD**: Motorola Solutions RTU family and its programming environment, common in municipal water and wastewater SCADA.
- **AutoLISP / Visual LISP**: scripting language built into AutoCAD and supported by several compatible CAD programs, including DraftSight (check your edition). Used here to edit drawings by script.
- **BOM**: bill of materials.
- **Contactor**: electrically operated switch that connects a motor to power.
- **FLA**: full-load current, the current a motor draws at rated load. Code tables give standard FLA by horsepower and voltage; the nameplate governs for the overload.
- **HOA**: Hand-Off-Auto selector.
- **I/O list**: list of every input and output the controller sees, with tag, type and field device.
- **IS (intrinsically safe)**: circuit designed so it cannot release enough energy to ignite a hazardous atmosphere.
- **L5X**: XML export format for Rockwell Studio 5000 projects. Readable by scripts.
- **Lead / lag**: first pump to start / second pump that assists.
- **NFPA 820**: standard on fire protection in wastewater facilities, including area classification.
- **PLC / RTU**: programmable logic controller / remote terminal unit.
- **SCCR**: short-circuit current rating of an industrial control panel. Depends on the weakest listed component and the protection chosen. A UL 508A item; this course's tools do not compute it.
- **Seal fail**: a probe in a submersible pump detects water in the seal chamber.
- **Structured Text (ST)**: IEC 61131-3 text language for PLC programs.
- **UL 508A**: standard for industrial control panels.
- **VFD**: variable frequency drive.

## AI terms

- **Agent**: a language model that can use tools (read files, run commands, edit files) in a loop to finish a task.
- **AGENTS.md / CLAUDE.md**: plain-text instruction files an agent reads at the start of a session. Standing rules live here.
- **Dry run**: run that reports what *would* change without changing anything.
- **Hook**: a small program the agent tool runs automatically at a defined moment (for example, before every file edit). The tool runs it, not the model, so it cannot be talked out of it.
- **Hallucination**: fluent, confident output that is not true. In this course: a requirement not in the spec, a rating not in the code book, a tag not on the drawing.
- **MCP**: Model Context Protocol, a standard for connecting agents to outside tools and data.
- **Oracle**: a trusted reference used to judge another output. Here, the reference model in `project/tools/sim.py`, trusted only after a human corrects it.
- **Plan mode**: an agent mode where it proposes steps and waits for approval before acting.
- **Skill**: a packaged set of instructions an agent loads when a task matches.
- **Subagent**: a second agent with its own fresh context, used for independent review.
- **Verified artifact**: a file a human has checked and signed; agents may not overwrite it.
