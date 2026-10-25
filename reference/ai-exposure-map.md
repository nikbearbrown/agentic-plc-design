# Where AI actually touches panel and PLC work

## Executive summary

An honest map of which parts of a controls career are most and least exposed to AI automation, and what that means for what you practice. It is a judgment from the course author, built from the vendors' own announcements and the structure of the work, not a forecast with numbers. The headline: the most exposed work is editing existing drawings for systems that are 90 percent designed already; the least exposed is physical, custom, field and commissioning work. The hedge is to become the person who can direct the automation and check it.

## The map

| Work | Exposure | Why | What to practice |
|---|---|---|---|
| Editing existing drawings for repeat designs | **High** | Template-based, rule-based, scriptable even without AI | Script it yourself (Module 4) before someone else does |
| I/O lists, BOMs, wire lists from a spec | **High** | Derived data; one source of truth beats retyping | Variant files (Modules 2-3) |
| First-draft PLC logic for standard sequences | **High and rising** | Vendors ship agents that go from spec to logic | Reading and testing logic (Modules 5-6) |
| Spec review and submittal checklists | **Medium-high** | Long documents, extractable requirements | Quote-checked checklists (Module 8) |
| Checking someone else's design | **Medium** | AI can flag, cannot attest | Being the checker (all modules) |
| Wiring and building panels in the shop | **Low** | Physical, custom, low volume | Keep the hands skills |
| Commissioning and field troubleshooting | **Low** | Real world, ambiguity, accountability | Read-only AI assistance (Module 9) |
| Customer and inspector conversations | **Low** | Trust, context, liability | Be the human in the room |

## Reasons the pace may be slower than the headlines

- The AI tools in the news cost real money and need design standards in digital form. Many small shops do not have those yet.
- Utilities are conservative buyers; consulting engineers write specs, jobs are bid publicly, and submittals are reviewed.
- Niche proprietary platforms have far less public training data than mainstream ones, so general-purpose AI is weaker there.
- Failures are regulatory events (a sewage overflow is a permit violation), so nobody ships unchecked work.

## Reasons not to relax

- Template work is automated first, with or without fancy products. Anyone who can script can absorb much of it.
- The risk to a small team is headcount, not the individual: the same five people may handle more work with agents, or fewer people the same work.
- Checking is a real job, but it takes fewer people than generating. The ones who stay are those who know the field, the customers and the failure modes.

## What this means

Spend your first two years closing the distance to commissioning, field work and programming, not settling in as a drafter. Use the agents to move faster at the template work so you can spend your time on the 10 percent and on the field.

## Sources and caution

This map draws on vendor announcements (Rockwell's FactoryTalk Design Studio AI agents, Siemens' engineering agent shown at Hannover Messe 2026, EPLAN's automated layout features) and on DraftSight's published Visual LISP support. Vendor claims are marketing until you test them. Re-check these links and the facts yourself; products and prices change faster than this file.
