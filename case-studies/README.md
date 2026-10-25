# Case studies: agentic tools for PLC design in the wild

## Executive summary

**What this is.** Three real, public, agentic tools for PLC engineering that appear in the bearbrown.co audited directory, written up as case studies to be read against this course's rules. Two drive Siemens TIA Portal (an MCP server and a Claude Code plugin); one drives Beckhoff TwinCAT. They are exactly the kind of tool the course is preparing you to judge.

**Why read it.** These tools already exist and are what "Rockwell, Siemens and others will ship agents" looks like in practice from third-party tool authors (with different license terms). Reading them with the course's questions (what does it write, what stops it writing something dangerous, how would I know it was wrong) is the quickest way to practice Module 12's tool-intake habit on real products.

**What we found.**
- bearbrown.co's catalog has **only three** PLC-design entries out of about 1,650 audited. All three carry the grade `CLEARED_STATIC`, which on that site means automated static checks passed and **no behavioural testing was done**. Their receipts (commit, date, sandbox) are empty in the catalog.
- **The direct catalog entries target Siemens and Beckhoff.** The executable course now uses MatIEC with a local C scan harness; vendor-specific integrations are separate investigations, not prerequisites.
- The audit snapshots are **stale for at least one entry**: `totally-integrated-claude` was audited at v4.3.2 on 2026-08-07; upstream is at v4.6.x. A claim in the audit snapshot (a write-confirmation hook) is not in the current README.
- Write safety differs a lot between tools, and the difference is the lesson: one leaves it "up to your client," one says it blocks writes without a server-issued token (in the older snapshot), one describes "safe" workflows without showing how.

**What this does not do.** Nobody installed or ran these tools. All of it is read from public READMEs, repository metadata and the site's catalog on 2026-10-25. Nothing here is a test result, a security review or a recommendation to adopt. A claim in a README is a claim.

---

## The three cases

| # | Case | Platform | Kind | Site grade | License |
|---|---|---|---|---|---|
| 1 | [TIA Portal Openness MCP](01-tia-portal-openness-mcp.md) | Siemens TIA Portal V20/V21 | MCP server + CLI, prebuilt runtime | CLEARED_STATIC | MIT |
| 2 | [totally-integrated-claude](02-totally-integrated-claude.md) | Siemens TIA Portal (Python and C# Openness) | Claude Code plugin of routed skills | CLEARED_STATIC | MIT |
| 3 | [twincat-agent](03-twincat-agent.md) | Beckhoff TwinCAT 3 (IEC 61131-3 ST) | Agent, skills and MCP servers | CLEARED_STATIC | PolyForm Noncommercial 1.0.0 |

## How to read a case study

Each follows the same frame, which is the course's judgment frame:

1. **What it is** in one paragraph, without the README's adjectives.
2. **What the site's audit established** and what it did not.
3. **What the upstream project says** (checked 2026-10-25), separated from what it shows.
4. **Against the course rules**: dry run, copy first, never live, quote-or-it-didn't-happen, human signs.
5. **What it would take to trust it**: the oracle question.
6. **Your turn**: a pre-filled intake sheet (from `../reference/tool-intake.md`) with the blanks only you can fill, and a short validation checklist.

## Patterns across the three

| Question | TIA MCP | totally-integrated-claude | twincat-agent |
|---|---|---|---|
| Can it change a project? | Yes, generates and edits PLC and HMI objects, compiles | Yes, through scripting and Openness skills | Yes, edits the PLC project, per README |
| What stops a bad write? | "Up to your client" in the open-source server; approvals are a feature of the author's commercial edition | Not described in the current README; an older audited snapshot described a confirm-and-token hook | Described as safe activation and validation workflows; implementation not shown |
| Can it touch a live controller? | Online values are read-only by default in the open server; the README describes a download capability among the tools | Docs MCP does not connect to a live TIA Portal; Openness skills can | README mentions login and activation sequences |
| Is there a test oracle? | A compile step; no behavioural oracle described | CI validates committed API evidence, not live runs | Not stated |
| Who is accountable? | You | You | You |

The last row is the point of the course. The tools differ; the accountability does not.

## Not covered

Rockwell Studio 5000 and FactoryTalk Design Studio agents, Siemens' own announced engineering agent, EPLAN's automation, Codesys tooling, and anything for Motorola MOSCAD. None appear in the bearbrown.co catalog. They are vendor products whose claims you should handle with `../reference/tool-intake.md` before believing, and they are the natural next case studies when someone has real access to them.

## Sources

- bearbrown.co catalog entries (`data/catalog/audit-entries.json`, ids `TechIndustryX__twincat-agent`, `bulaofen0036-coder__tia_portal_openness_mcp`, `czarnak__totally-integrated-claude`) and the site's Corpus page for what `CLEARED_STATIC` means.
- Upstream repositories and their READMEs, read 2026-10-25: github.com/bulaofen0036-coder/TIA_Portal_Openness_MCP, github.com/Czarnak/totally-integrated-claude, github.com/TechIndustryX/twincat-agent.
- Repository figures (stars, push dates) are from the GitHub API on the same day and change daily.

## End-of-course executable case-study sequence

After [Lab 08 capstone](../labs/08-capstone.md), complete the local adaptation appended to each direct case above, then [Case 4: evidence-driven repair](04-evidence-driven-repair.md). The first three are direct PLC-domain tools; the fourth uses adjacent general testing/debugging skills. The local adaptations run this course's own compiler and harness, not those vendor products. All vendor execution remains NOT VERIFIED.

See the [read-only source inventory](../reference/bearbrown-plc-inventory.md) for exact BearBrown file paths, search scope, source revision and license distinctions. Selected actual execution output lives in `labs/evidence/`; the [ledger](../labs/VERIFICATION.md) distinguishes read-only research from executed lab adaptations.
