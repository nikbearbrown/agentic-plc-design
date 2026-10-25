## Executive summary

A read-only audit found **three direct PLC tools** in BearBrown's 1,646-entry audit catalog, plus general testing/debugging skills useful for PLC agent workflows. They are now taught in the [end-of-course case studies](../case-studies/README.md), including local executable adaptations. No vendor tool was installed or run, no credential was read or copied, and the BearBrown repository was not edited. A website catalog badge is not execution evidence.

## Exact source inventory

Source repository: `/Users/bear/Documents/CoWork/bear-textbooks/books/bearbrown_co`, revision `4c5785dda2decb0a63b1a5677be3fcfb347cf74d`. The machine-readable inventory is [bearbrown-inventory.json](../labs/evidence/bearbrown-inventory.json). These are findings from the inspected snapshot, not a claim to have searched every public workflow on the internet.

| Item | Exact local evidence | Classification and source |
|---|---|---|
| `TechIndustryX__twincat-agent` | `/Users/bear/Documents/CoWork/bear-textbooks/books/bearbrown_co/data/catalog/audit-entries.json`, entry ID shown | Direct PLC: agent/skills/MCP integration for Beckhoff ST. [Upstream](https://github.com/TechIndustryX/twincat-agent), [current license](https://github.com/TechIndustryX/twincat-agent/blob/main/LICENSE): PolyForm Noncommercial 1.0.0. Read, not installed; not included as an unrestricted open-source dependency. |
| `bulaofen0036-coder__tia_portal_openness_mcp` | Same absolute catalog file, entry ID shown | Direct PLC: executable MCP server/CLI and engineering templates for Siemens TIA. [Upstream](https://github.com/bulaofen0036-coder/TIA_Portal_Openness_MCP). MIT project claim; vendor TIA prerequisites are separate. Catalog snapshot and source README inspected, not executed. |
| `czarnak__totally-integrated-claude` | Same absolute catalog file, entry ID shown | Direct PLC: routed skill/plugin framework. [Upstream](https://github.com/Czarnak/totally-integrated-claude), [MIT license](https://github.com/Czarnak/totally-integrated-claude/blob/main/LICENSE). Its actual [plc-code-analysis definition](https://github.com/Czarnak/totally-integrated-claude/blob/main/skills/plc-code-analysis/SKILL.md) reviews exported ST/SCL/XML with context and evidence limits. No vendor execution. |
| `test-driven-development` | `/Users/bear/Documents/CoWork/bear-textbooks/books/bearbrown_co/content/skills/test-driven-development/SKILL.md` | Adjacent: human/agent procedure, not a PLC runtime or runnable script. Front matter says MIT. [BearBrown skill page](https://bearbrown.co/skills/test-driven-development). Read actual definition; transfer the fail–repair–rerun idea to native mutation tests. |
| `systematic-debugging` | `/Users/bear/Documents/CoWork/bear-textbooks/books/bearbrown_co/content/skills/systematic-debugging/SKILL.md` | Adjacent: evidence-first diagnosis protocol. Front matter says MIT. [BearBrown skill page](https://bearbrown.co/skills/systematic-debugging). Read actual definition; use the timer/oracle discrepancy as the local worked problem. |

The three direct entries have `CLEARED_STATIC` grades and empty execution receipts in the local catalog. The TwinCAT catalog's license field is empty; the current upstream license supplies the noncommercial restriction. Do not equate an empty field with permission to copy.

## Searches beyond names

Searched actual descriptions/definitions for PLC, IEC 61131, Structured Text, Ladder logic and industrial automation. Inspected the actual upstream `plc-code-analysis/SKILL.md` plus project README/license material; the other direct entries are catalog records, not locally installed vendor skills.

- `data/skills/catalog.json`: 51 entries; no direct PLC-specific match. Actual local testing/debugging skill definitions were read.
- `data/agents/catalog.json` and `data/agents/details.json`: 1,877 entries each; no direct industrial PLC match in the search terms.
- `data/n8n/details.json`: 1,876 entries; no direct industrial PLC match.
- `public/n8n/workflows/`: a "structured text" hit described document parsing, not IEC Structured Text. It uploads to LlamaParse and uses Gmail/Drive/Sheets/Telegram; it was not imported or run. Other PLC string hits referred to decentralized identifiers such as `did:plc`, not programmable controllers.

"Automation" alone is not an industrial-control match. None of the business workflow counts is advertised as PLC coverage. Metadata counts may include duplicated agent/workflow records.

## Reuse decision

We discuss and link the vendor projects, retaining attribution and license distinctions. We do not copy their code, install unrecognized servers, enable blanket approvals or reach industrial endpoints. The end-of-course exercises adapt their **workflow ideas** using this course's own synthetic specification, native MatIEC compiler and tests. The adapted exercises are executable here; the vendor products remain **NOT VERIFIED**.

The repository retains its existing course copyright. A generic testing procedure inspired by a source is not a claim that the source's whole skill was installed or executed, and we do not claim the entire expansion was authored with strict test-first development.
