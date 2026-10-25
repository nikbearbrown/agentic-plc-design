# Module 09 — The 2 AM call

## Executive summary

**What you do:** build a field troubleshooting aid from event logs: a script that turns a station's raw alarm/run log into hard numbers, an AI-written list of hypotheses to be tested against those numbers, and a one-page runbook for the person on the phone at 2 AM.

**Why:** commissioning and troubleshooting are the least automatable parts of this work and the best place to prove your value. AI can help a lot *if it reasons from facts you extracted rather than guesses*, and *if it never touches the live system*. The skill here is the discipline: read-only assistance, evidence before story.

**What you leave with:** a log summariser, the habit of asking "what does the data support?" before "what is the fix?", and a runbook template. Time: about 3 hours.

---

## The idea

A pump station calls at 02:41: high level. Someone has to decide whether to dispatch a crew, and what to tell them to bring. The data is an event log: when each pump ran, when each alarm came in.

If you paste a raw log into a chat and ask "what's wrong?", the answer will be a fluent story. It may even be right. It will not tell you which parts the data supports and which it made up. So the pattern is:

1. **Extract facts with a script** (run counts, run times, short cycles, alarm times, start order). A script does arithmetic correctly; a language model estimating it does not always.
2. **Ask the AI for hypotheses given those facts**, and for what *additional* data would distinguish them.
3. **You decide what to check first**, and you decide what to do at the station.
4. **Never write to the live system from the AI loop.** Reading exported logs is fine; changing setpoints, forcing I/O or resetting alarms is not.

```bash
python3 project/tools/apd.py log project/samples/station-log-synthetic.csv
```

The sample log is **synthetic**: an invented night at an invented station. The output tells a story: pump 1 short cycles for twelve minutes, pump 2 has a seal-fail alarm and never runs again, then a high level alarm with pump 1 alone running 45 minutes. Many causes could produce it. The log narrows them; it does not choose.

---

## Lab

### Step 1 — Read the facts

Run the summariser. Write the timeline in your own words, one line per event. Do not explain yet.

### Step 2 — Your hypotheses first

On paper, list at least three possible causes for the pump 1 short cycling and what you would look for to tell them apart. (Think floats, level sensing, check valve, pump hydraulics, control logic.) *Then* ask the AI (LLM exercise). Compare. Did it give you something you did not think of? Did it give you something you can rule out right now with the facts?

### Step 3 — Triage

Rank what to check first, given: the seal-fail alarm on P2 (a pump out of service), a high-level condition, a crew that takes 40 minutes to arrive, and one pump. This is a judgment about risk (overflow, permit), not a technical one. Write your ranking and your reasoning.

### Step 4 — Write the runbook

Produce a one-page runbook for a fictional on-call technician: what the alarm means, what to check from the phone, what to check on site, what not to touch, who to call. Use the AI to draft; you rewrite to match your owner's actual procedure.

---

## Five-part exercise

### 1 — When to use AI

- **Summarising and tabulating log data via a script** — *why it works:* the arithmetic is checked by running the same script twice or by hand on a slice.
- **Generating a hypothesis list from the extracted facts** — *why it works:* brainstorming with the facts in front of it; you filter.
- **Drafting a runbook skeleton from your notes** — *why it works:* formatting and completeness prompts; you supply the content.

**The tell:** each hypothesis names the data that would confirm or kill it.

### 2 — When NOT to use AI

- **Issuing commands to the station** (reset an alarm, change a setpoint, force a pump). *Why it fails:* physical consequences, no undo, and you may not know the plant's real state.
- **Telling a crew the cause as if it were known.** *Why it fails:* a hypothesis presented as a fact sends people to the wrong place.
- **Deciding the risk tolerance** (wait for morning or dispatch now). *Why it fails:* a human decision about overflow, permits and people.
- **Diagnosing safety-critical faults without a person on site.** *Why it fails:* ambiguity plus accountability.

**The tell:** the AI said "the cause is" and you have not seen the evidence.

**Series tier:** *Tier 7, wisdom* — the judgment about when acting beats waiting.

### 3 — LLM exercise

**You are building:** a hypothesis list that is tied to the data.
**Tool:** Claude chat.

```
I troubleshoot municipal duplex lift stations. Here are facts extracted by a script from one night's event log. They are exact; do not recompute them.

P1_RUN_FB: 13 runs, 75.4 min total, longest 45.0 min, 6 short cycles (under 60 s)
P2_RUN_FB: 4 runs, 18.0 min total, longest 4.5 min, 0 short cycles
P2_SEAL_FAIL: raised once at 02:14
ALM_HIGH_LEVEL: raised once at 02:41, cleared 03:30
Timeline notes: for the first two hours the pumps alternated about every 15 minutes with runs of about 4.5 minutes. Between 02:00 and 02:12 pump 1 started and stopped six times, about 24 seconds each run. After 02:14 pump 2 never ran. At 02:41 the high-level alarm came in while pump 1 ran alone for 45 minutes.

Give me a table of five or six hypotheses. Columns: hypothesis, which facts above support it, which facts above it does NOT explain, what single piece of additional data would confirm or rule it out, and whether I could get that data remotely or only on site. Mark any hypothesis you cannot support with at least one fact from the list as SPECULATION. Do not recommend a repair. Do not say what the cause is. Do not invent facts such as pump curves, inflow rates, or float positions.
```

**Adapt it:** replace the facts with those from your own station's log summary. Remove any station or customer names.

**Produces:** a hypothesis table. Check the "does NOT explain" column against the facts; AI often overclaims explanatory power.

### 4 — CLI exercise

**You are building:** a log summary report and the start of a runbook.
**Tool:** Claude Code. **Level:** beginner.

Setup: `project/samples/station-log-synthetic.csv` exists; `./check.sh` passes.

```
Read AGENTS.md. Run python3 project/tools/apd.py log project/samples/station-log-synthetic.csv and save the output verbatim to scratch/log-facts.txt. Then create scratch/runbook-draft.md with these sections: Executive summary; What the facts say (copy only numbers and times from log-facts.txt, adding nothing); Hypotheses (each tied to a fact from log-facts.txt, with what data would confirm or rule it out, and marked REMOTE or ON-SITE); First five minutes from the phone; On site: look-before-you-touch checklist; Do not touch (list anything that changes the live system); Who to call. Mark every item in the last four sections that comes from general knowledge rather than from the facts as GENERAL so I can review it. Do not claim to know the cause. Do not write or run any command that touches a station, a controller or a network. Tell me which items you could not support and why.
```

**Expected:** `log-facts.txt` identical to the tool output; a runbook draft with REMOTE/ON-SITE and GENERAL tags.
**Inspect:** diff `log-facts.txt` against the script's output. Check the numbers in "What the facts say" against it, character for character. Read every GENERAL item and rewrite it to your owner's real procedure.
**If it goes wrong:** the agent may paraphrase the numbers or round them. Re-run with "Copy numbers exactly; do not round."
**Standing rule:** *"Numbers from a tool are copied exactly, never retyped or rounded by the AI."*

### 5 — AI validation exercise

**You are validating:** the hypothesis table from exercise 3 and the runbook draft from exercise 4.
**Type:** reasoning chain. **Risk:** high — people act on it at night.

```
□ Correctness: for each hypothesis, are the "supporting facts" really in the list, and do they really support it?
□ Completeness: which fact is unexplained by every hypothesis? What would explain it?
□ Scope: did the AI add numbers or equipment details that were not in the facts (pump curves, float heights, inflow)?
□ Remote vs on-site: for each "remote" item, could you really get it without being there?
□ Safety: does the runbook ever tell the technician to do something that changes the station
   (reset, bypass, force) without saying who authorizes it?
□ Failure mode check: story-shaped certainty (explains everything neatly); an overclaiming "does NOT explain" column;
   confident wrong numbers; a step that is safe in the abstract and unsafe at this station.
```

**AI Use Disclosure** (two sentences).

---

## Done when

- You have `log-facts.txt`, a ranked list of what to check first, and your own rewritten runbook page.
- You can name one hypothesis the data rules out and one it cannot.
- You can explain, to a manager, why the AI never touches the live system.
