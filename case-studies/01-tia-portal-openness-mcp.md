# Case study 1 — TIA Portal Openness MCP

## Executive summary

**What it is.** An open-source (MIT) server that lets an AI client drive Siemens TIA Portal V20 or V21 through the MCP protocol: create projects, add hardware, generate PLC objects (tags, UDTs, data blocks, SCL and ladder), build WinCC Unified HMI screens, compile and report diagnostics, and save. It also ships a command-line mode where an AI writes a YAML or JSON spec and an engineer runs one command.

**Why it matters for this course.** It is the clearest real example of "spec in, PLC project out," and its README even shows a demo of writing a duty/standby rotation function block for two pumps, which is this course's lift station problem. It also shows the central safety lesson: **who stops a bad write is not the same in the free server and the paid app.**

**What we found.** It is popular (about 350 stars on 2026-10-25) and actively maintained. The site's audit graded it `CLEARED_STATIC` with empty receipts, meaning nothing about how it behaves was tested. In the open-source server, write safety is stated to be "up to your client." The approval-before-every-write behavior the README advertises belongs to the author's separate commercial desktop edition, which has a free trial and a license key.

**What this does not establish.** Nobody ran it. It needs Windows, TIA Portal and a Siemens Openness setup; the course author has none.

---

## What it is

A bundle containing a compiled runtime, an MCP server (stdio or HTTP), a CLI named `tia` with verbs such as `gen`, `patch`, `compile`, `describe`, `export` and `import`, templates, and a capability matrix. According to its README it exposes 235 tools across project, hardware, PLC, HMI and online operations. It supports a read-only "online" mode for reading values from a running controller (by S7 addresses or OPC UA) and a "doctor" command that checks the environment.

## What the site's audit established

- Grade `CLEARED_STATIC` (audited 2026-08-07, version 2.2.5 in the catalog). On bearbrown.co that means static checks passed at one commit; **behavioural assessment was not performed**.
- Receipts are empty in the catalog entry (no commit hash, no sandbox run).
- The catalog entry's description and tags are broader than any test (tags include "legal" and "security"), which is a reminder that tags are not verification.

## What the upstream project says (read 2026-10-25)

- MIT license; the server "runs with no license key."
- The README calls itself the "engine" and says you bring your own AI client.
- A table contrasts the open server with the author's commercial desktop app: write safety is "up to your client" in the open server; in the app, every write waits for approval, irreversible operations are confirmed separately, and there is a hash-chained audit log.
- Online values are read-only in the open server; symbolic writes exist only in the commercial app, off by default.
- A block must compile before it can be exported; a companion tool auto-exports after each successful compile and commits to git.
- The runtime is prebuilt; you download it rather than build it.
- The README also promotes the commercial product and gives a contact address for a trial. That is marketing inside documentation. Read it as such.
- Security policy: private vulnerability reporting, and "a read-only path that in fact writes" is listed as an in-scope bug class. Good sign that the author thought about it; still a statement of intent.

## Against the course rules

| Rule | How this tool measures up, from what is public |
|---|---|
| Never touch anything live | The open server's online mode is described as read-only. The tool list is large enough that you cannot assume nothing can download or write to a controller; read the tool list before connecting to anything real. |
| Dry run first, copy first | `describe` and `export` suggest read paths; `gen` and `patch` change a project. Use a copy of a project, always. |
| Human signs, agent never | Write approval is up to your client. If your client auto-approves tool calls, nobody is signing anything. |
| Quote or it did not happen | Compile diagnostics are a real oracle for syntax and type errors. They say nothing about whether the sequence is right. |
| Say what was not run | The README demo shows a compile cleanup from warnings to zero. A clean compile is Module 6's weakest kind of evidence. |
| Do not upload company material | The open server is local. The commercial app can use cloud or local models; where project data goes depends on what you configure. |

## What it would take to trust it

1. **A prebuilt executable is code you run next to your engineering project.** Check the release provenance and checksums, or build from source if offered, and run it first on a throwaway project in a virtual machine.
2. **A behavioural oracle.** Generate the Module 5 lead/lag block through it, then run the Module 5 vectors in a PLC simulator (S7-PLCSIM or equivalent). If it passes only the compile, it has passed nothing that matters.
3. **A client that asks.** Configure your AI client to require approval for every tool call. Test that it does by asking for a harmless write.
4. **A written failure list.** After trying it on three different tasks, write what it got wrong. If the list is empty, you did not look hard enough.

## Your turn

Copy `../reference/tool-intake.md` to `scratch/intake-tia-mcp.md`. Pre-filled from public sources, for you to check:

| Question | Pre-filled (verify) |
|---|---|
| 1. What is it | Server and CLI that drives Siemens TIA Portal engineering from an AI client |
| 2. The claim | "Drive Siemens TIA Portal V20/V21 from any MCP client; create projects, generate PLC & HMI, compile & diagnose." Source: its README |
| 5. Where does data go | Open server: local. Commercial app: your choice of model provider or local model |
| 11. Verdict | **You fill this in**, after items 6 to 10 |

**Validation checklist (answer from the public README alone):**

```
□ Can you tell, from the README, which tools in the open server can change a controller (not just a project)?
□ Where in the README does it say who approves a write? Is that the open server or the paid app?
□ What is the strongest evidence of correctness the README gives? Is it independent of the tool?
□ What would you need to see to trust a generated duty/standby block with a real pump?
□ Failure mode check: marketing inside documentation; a safety feature that belongs to a different product than the one you install.
```

Write a two-sentence AI Use Disclosure if an AI helped you answer.
