# Case study 3 — twincat-agent

## Executive summary

**What it is.** A Claude Code and GitHub Copilot CLI plugin for Beckhoff TwinCAT 3 development: a dedicated `twincat` agent, skills with rules for IEC 61131-3 Structured Text and naming conventions, a local MCP server that automates the TwinCAT XAE engineering environment on Windows, and a hosted MCP server that searches Beckhoff's InfoSys documentation and symbols.

**Why it matters for this course.** It targets the same language the course uses for its logic (Structured Text) and is the most explicit about being a *rules-first* agent: strict conventions and syntax checks around the model, rather than a bare tool. It is also the only one of the three whose license restricts commercial use, a fact that matters in a company.

**What we found.** Smaller and quieter than the others (about 33 stars; last push 2026-06-04). It is licensed under PolyForm Noncommercial 1.0.0, so commercial use needs a separate license from the author; using it at work for paid projects is not covered by default. It describes "safe activation/login sequence" and "safe project validation workflows" as features. The README does not show how they are implemented or tested.

**What this does not establish.** Nobody installed or ran it. It needs Windows x64, TwinCAT 3.1 Build 4026 or later, and the XAE shell.

---

## What it is

According to its README:

- A `twincat` agent plus skills and operating rules, packaged as a plugin.
- A local MCP server (a bundled Windows executable) that automates TwinCAT XAE: initialize automation, inspect the PLC tree, edit.
- A remote MCP server with tools such as `infosys_search` and `infosys_search_symbols`, usable on its own without the rest of the repo.
- The workflow: open a folder containing a `.plcproj`, select the agent, give a task such as creating a state machine in the main program.

## What the site's audit established

- `CLEARED_STATIC`, catalog version 2026.06.04. Static checks only.
- The catalog entry's description and readme snapshot are nearly empty and receipts are empty. The audit tells you almost nothing here beyond "nothing alarming was found in a static pass."
- The license field in the catalog is blank. The actual license is restrictive: this is a case where an audit's missing field hides the most important fact for a company.

## What the upstream project says (read 2026-10-25)

- License: PolyForm Noncommercial 1.0.0. Personal, academic and non-commercial use are allowed; commercial use requires a separate license.
- A prebuilt executable is committed in the repository.
- Features named in the README include naming conventions, PLC-aware operations, syntax checks, and a safe activation and login sequence. Their implementation is not shown.
- The README advises Copilot CLI users to enable a broad "allow-all" mode. That is the opposite of this course's advice; see below.
- The hosted documentation server is a third-party service run by the author. Its terms, uptime, and what it logs are not stated.
- No statement about automated tests of the agent's output.

## Against the course rules

| Rule | Measure |
|---|---|
| Never touch anything live | "Login" and "activation" are exactly the words that can mean connecting to and starting a runtime on a target. Read what the activation sequence does before you let an agent run it, and do it first with a local simulator or an empty runtime. |
| Permissions | Advice to allow everything removes the human from the loop. Do not follow it on a machine that can reach a controller. |
| Copy first | Work on a clone of the project folder under version control. |
| Do not upload company material | The documentation server is remote. Queries (symbol names, code snippets) leave your machine. |
| License | Commercial use is not covered by default. A company decision, not an engineer's. |

## What it would take to trust it

1. **Settle the license first.** If you work for a company, this question decides whether you may use it at all. Ask whoever signs software agreements.
2. **Read the rules before the model does.** The value of a rules-first agent is in the rules. Read its rules and skills files and ask whether *you* agree with each one. A naming convention that differs from your shop's is not a safety feature.
3. **Test the validation claim.** Give it a deliberately broken Structured Text file and see whether its "syntax checks" catch the break. Then give it a program that compiles but does the wrong thing and see whether anything catches that. The second is the real test, and an oracle like Module 5's is what you need.
4. **Decide about the executable.** A committed binary has no source for you to read. Prefer a build from source if available, or run it on an isolated machine first.

## Your turn

Copy `../reference/tool-intake.md` to `scratch/intake-twincat-agent.md`. Pre-filled:

| Question | Pre-filled (verify) |
|---|---|
| 1. What is it | An agent plus rules and an engineering-automation server for TwinCAT 3 Structured Text projects |
| 4. Needs | Windows x64, TwinCAT 3.1 Build 4026+, XAE Shell, Claude Code or Copilot CLI |
| 5. Data | Documentation queries go to a remote server operated by the author |
| 11. Verdict | **You fill this in** |

**Validation checklist (from the repository alone):**

```
□ Open the license file. Can your employer use this on a paid project without asking?
□ Find the "safe activation" or "safe validation" behaviour in the rules or skills files. What exactly does it do?
□ What would the agent do if asked to activate a configuration on a real target? What stops it?
□ Which statements in the README are verifiable from the repo, and which are only claims?
□ Failure mode check: a license that makes the tool unusable at work; a safety feature that is a word, not a mechanism;
  advice to disable permissions.
```

Write a two-sentence AI Use Disclosure if an AI helped you answer.
