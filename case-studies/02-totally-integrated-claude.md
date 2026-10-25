# Case study 2 — totally-integrated-claude

## Executive summary

**What it is.** An MIT-licensed plugin for Claude Code (and installable for Codex, VS Code/GitHub Copilot and Copilot CLI) that packages Siemens TIA Portal engineering knowledge as routed skills: one entry-point skill chooses between Python TIA Scripting and C# Openness and loads the right domain skill. It also bundles a read-only environment check and a documentation-search MCP.

**Why it matters for this course.** It is the best real example of the *skill* layer from Module 10: instead of giving an agent a tool and hoping, it packages the procedure, the routing and a diagnostic. It also teaches the opposite lesson about audits: the site's record of it is out of date.

**What we found.** About 74 stars, 15 forks and active releases (v4.6.1 upstream on 2026-10-25). The bearbrown.co audit graded it `CLEARED_STATIC` at **v4.3.2 on 2026-08-07**, so it describes a version two minor releases behind. That older snapshot's description mentions "MCP write safety hooks" that block writes without `confirm=true` and a server-issued `safetyToken`; **the current README does not mention this**, so we cannot say whether it was removed, moved, or is simply documented elsewhere. A reader must go check.

**What this does not establish.** Nobody installed or ran it. It needs TIA Portal V21, Openness, and Siemens' Python wheel; none is available to the course author.

---

## What it is

A skill framework, not a server. According to the README:

- `tia-openness-roadmap` is the entry point and routes tasks to Python, C#, the Module Builder, a diagnostic, or Add-In development.
- `tia-python` covers PLC blocks and tags, HMI access and export through Siemens' scripting wrapper.
- A set of C# skills covers devices, networks, drives, import/export, and more advanced services, built on one common foundation skill.
- `plc-code-analysis` is a standalone skill for reviewing raw SCL/ST or exported XML. It is the one most relevant to a reviewer.
- `tia-doctor` is a read-only PowerShell probe that checks prerequisites and prints fixes without changing the machine.
- A Siemens documentation MCP searches the public docs site; it does not connect to a live TIA Portal.

## What the site's audit established

- `CLEARED_STATIC`, audited 2026-08-07, catalog version 4.3.2. Static checks only.
- Receipts empty.
- The audit's readme snapshot included the write-safety hook claim. It is the only place in this study where a *specific safety mechanism* was claimed, which makes its absence from the current page notable.
- **The audit is a photograph, not a feed.** Lesson for your intake sheet: record the version and date you looked at, and re-check before relying on it.

## What the upstream project says (read 2026-10-25)

- Install targets include Claude Code and Codex. MIT license.
- Prerequisites are heavy and specific: TIA Portal V21, .NET Framework, Python 3.12 to 3.14 with the matching Siemens wheel, and extra tooling for Add-Ins.
- Continuous integration validates committed API evidence without TIA Portal on the runner. That means the *documentation and API facts* are checked mechanically, but **generated engineering work is not tested against a live TIA Portal in CI.**
- The routing table is explicit about when to use which path, and honors an explicit user choice of implementation.

## Against the course rules

| Rule | Measure |
|---|---|
| Never touch anything live | The docs MCP does not. The Openness skills can reach a project and, depending on your setup, a device. Treat every Openness script as write-capable. |
| Dry run, copy first | Not a built-in property of the plugin. You supply it: run only on a copy of a project. |
| Hooks beat rules | A write-confirmation hook is the right layer (see Module 10). If the plugin still has one, test it by trying to bypass it. If it no longer does, you must install your own. |
| Human signs | Skills guide a procedure; nothing in a skill signs for you. |
| Read-only first | `tia-doctor` and `plc-code-analysis` are the best entry points. Both are read-first by design. |

## What it would take to trust it

1. **Pick the read-only skills first.** Use `plc-code-analysis` on a program you know cold, and see whether it finds what you know is wrong and invents nothing.
2. **Verify the hook claim yourself.** Read the plugin's hook configuration in the repository. Ask the agent to perform a write and watch whether anything blocks it.
3. **Pin the version.** Note the exact release you tested. A plugin that changes under you is a different tool every month.
4. **Test routing.** Give it the same task twice with different phrasing; does it route to the same path? Inconsistent routing is a reliability finding.

## Your turn

Copy `../reference/tool-intake.md` to `scratch/intake-totally-integrated-claude.md`. Pre-filled:

| Question | Pre-filled (verify) |
|---|---|
| 1. What is it | A packaged set of skills that guides an AI agent through TIA Portal automation |
| 4. Needs | TIA Portal V21, Openness, .NET Framework, Python with Siemens' wheel |
| 7. Oracle | **Open.** README says CI checks API evidence, not live runs. What is *your* oracle? |
| 11. Verdict | **You fill this in** |

**Validation checklist (from the repository alone):**

```
□ What version did the site audit, and what version is upstream now? Do the two descriptions of safety agree?
□ Open the repository's hook or settings files. Is there a confirm-before-write mechanism today? Quote where.
□ Which skills only read, and which can write?
□ What does CI actually check? Could it pass while generated logic is wrong?
□ Failure mode check: audit drift; documentation that describes a feature the code no longer has;
  skills that route confidently to the wrong API.
```

Write a two-sentence AI Use Disclosure if an AI helped you answer.
