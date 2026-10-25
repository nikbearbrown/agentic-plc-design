# Module 10 — Build your own agent kit

## Executive summary

**What you do:** write the standing instructions, a skill, a safety hook and an independent reviewer for your own agent setup, using the repo's `.claude/` folder as a worked example, and then test that each one actually works.

**Why:** the tools will change, and a person who only knows one product's menus starts over every time. What carries over is knowing *what to put in the agent's environment*: rules it must read, procedures it can reuse, checks that run whether or not the model remembers, and a second pair of eyes that did not write the work. Those four things work, with different spellings, in Claude Code, Codex and whatever comes next.

**What you leave with:** your own `AGENTS.md` rules, a skill for your most repeated job, a hook that blocks one dangerous action, and a reviewer agent, each tested by trying to break it. Time: about 4 hours.

---

## The idea

Four layers, from soft to hard:

| Layer | What it does | How strong |
|---|---|---|
| **Instruction file** (`AGENTS.md` / `CLAUDE.md`) | Standing rules the agent reads at the start | Persuasive; the model may forget or misread |
| **Skill** (`.claude/skills/<name>/SKILL.md`) | A reusable procedure for a recurring job, loaded when relevant | Persuasive; guides method |
| **Hook** (`.claude/settings.json` + a script) | A program the *tool* runs at a fixed moment, such as before every file edit | **Enforced**; the model cannot talk its way past it |
| **Reviewer subagent** (`.claude/agents/<name>.md`) | A second agent with fresh context, read-only, that checks work it did not do | Independent; catches what the writer is blind to |

The rule of thumb: **put a thing in the strongest layer that fits.** "Never mark a table verified" is a rule the agent might still break, so it is in the instruction file *and* enforced by a hook. "How to check a variant" is a procedure, so it is a skill.

Look at what already exists in this repo:

- `AGENTS.md`: nine hard rules and a style guide.
- `.claude/skills/variant-check/SKILL.md`: a five-step procedure that ends with "stop; never fix a variant to make a rule pass."
- `scripts/guard.py` + `.claude/settings.json`: the hook that blocks edits to a verified table.
- `.claude/agents/panel-reviewer.md`: a read-only reviewer with a "CANNOT-DETERMINE is a valid answer" rule.

Product names and file locations change. If you use Codex, the equivalent of `CLAUDE.md` is `AGENTS.md` itself, and the other layers may be spelled differently in your version; check its documentation and write down the mapping in `reference/cli-cheatsheet.md`. The ideas are the portable part.

---

## Lab

### Step 1 — Gather your standing rules

Open your notes from each module. Every "Standing rule" line is a candidate. Add rules from your own near-misses. Write them in `scratch/my-rules.md` in plain sentences. Keep them short, specific and testable. "Be careful" is not a rule; "never run a script on an original drawing" is.

### Step 2 — Pick the job you repeat most

Think about what you do every week that follows the same steps: check a new job's variant, prepare a submittal package, triage a fault log. Write the steps in `scratch/my-job.md`. The shortest honest version is your skill.

### Step 3 — Pick one thing that must never happen

Examples: an edit to a signed table; a script run without a dry run; a file written outside the project folder; a commit containing a customer name. Choose one. Write one sentence in `scratch/my-never.md`: *"The tool must refuse to ___."*

### Step 4 — Try to break each layer

For each thing you build, try to make the agent violate it. Record what happened. A rule the agent obeys when asked politely and breaks when you rush it is not a rule; it is a hope.

---

## Five-part exercise

### 1 — When to use AI

- **Drafting your instruction file from the rules you listed** — *why it works:* compression and tidy phrasing; you can compare line by line with your list.
- **Writing the first version of a hook script** — *why it works:* small, testable code with an obvious pass/fail.
- **Drafting a skill's steps from your description of the job** — *why it works:* structure and checklists.

**The tell:** you can say what each layer would do on a case you chose.

### 2 — When NOT to use AI

- **Deciding what the dangerous actions are.** *Why it fails:* this is risk knowledge from your experience and near-misses.
- **Testing your own agent kit by asking the agent if it works.** *Why it fails:* a model will say yes. You have to try to break it.
- **Granting the agent broad permissions "to save time."** *Why it fails:* permission is a risk decision with your name on it.

**The tell:** you did not try to break it.

**Series tier:** *Tier 4*, metacognitive supervision, applied to your own setup.

### 3 — LLM exercise

**You are building:** a first draft of your instruction file.
**Tool:** Claude chat.

```
I am a control panel designer setting up a repository for working with an AI coding agent. Below are my working rules, written by me from experience. Turn them into an AGENTS.md file with these sections: Executive summary (what this repository is, why an agent reading it needs these rules, what the rules do not cover), Hard rules (numbered, each one sentence, each one testable), Style, and Where things live. Rules for you: do not add any rule I did not write; do not soften any rule; if two of my rules conflict, point it out instead of resolving it; if a rule is too vague to test, list it under "Needs sharpening" with a question for me. Then give me five tests: for each, one message I could send the agent that tries to make it break one of my rules, and what a correct response looks like. [PASTE THE CONTENTS OF scratch/my-rules.md HERE]
```

**Adapt it:** use your real rules. For Codex, the file is called `AGENTS.md` directly; for Claude Code, `CLAUDE.md` can import it with the line `@AGENTS.md`.

**Produces:** an instruction file draft plus five adversarial test messages.

### 4 — CLI exercise

**You are building:** one skill, one hook, one reviewer.
**Tool:** Claude Code (plan mode first). **Level:** advanced.

Setup: `scratch/my-rules.md`, your job description from Step 2, and your never-happens sentence from Step 3.

```
Read AGENTS.md, .claude/skills/variant-check/SKILL.md, .claude/agents/panel-reviewer.md, .claude/settings.json and scripts/guard.py as worked examples. Then, create these, touching only new files: (1) .claude/skills/my-skill/SKILL.md from the job description in scratch/my-job.md, following the structure of variant-check, with a final step that says when to stop; (2) scripts/my_guard.py, a PreToolUse hook script that reads the hook JSON on stdin and exits with status 2 and a clear stderr message when the action in scratch/my-never.md would happen, and exits 0 otherwise; (3) a unit test for the hook in project/tests/test_my_guard.py that pipes sample JSON to the script and checks both the blocking and the allowing case; (4) .claude/agents/my-reviewer.md for the artifacts in scratch/my-job.md, read-only tools only. Do not edit the existing skill, agent, guard or settings.json; instead print the exact JSON I should add to settings.json to register my_guard.py and wait for me to apply it. Run ./check.sh and the new test and show me the output.
```

**Expected:** four new files and a test. You then add the hook registration yourself (an edit to the settings file is a permission change, so it is yours).
**Inspect:** read the hook script: does it block only what you intended? Try the test yourself in a terminal: pipe a JSON line into it.
**If it goes wrong:** a hook that blocks everything makes the tool unusable; one that blocks nothing is worse because it looks like protection. Test both cases. If you lock yourself out, remove the hook entry from the settings file.
**Standing rule:** *"Every hook has a test for the allowing case and the blocking case."*

### 5 — AI validation exercise

**You are validating:** your instruction file, your skill, your hook, your reviewer.
**Type:** agentic output. **Risk:** high — this is the safety system for everything else.

```
□ Rules: send each of the five adversarial messages from exercise 3. Record the agent's actual response.
   Did it refuse every one? Which one did it get around, and how?
□ Hook: in a session, ask the agent to do the forbidden thing. Does the tool block it?
   Ask it a second time, phrased differently. Does the hook still block it?
□ Skill: run it on a new case. Does the agent follow the steps in order and stop where told?
□ Reviewer: give it an artifact with a planted error. Does it find it? Give it a clean one.
   Does it invent a problem? Does it say CANNOT-DETERMINE when it should?
□ Failure mode check: rules obeyed only when asked politely; hooks with a loophole (a different tool path to the
   same effect, such as the shell instead of the editor); reviewers that agree with the writer.
```

**AI Use Disclosure** (two sentences).

---

## Done when

- You have an instruction file with rules you wrote and tested, a skill, a hook with a test, and a reviewer.
- You found at least one way your own safeguards fail and recorded the fix or the remaining gap.
- You can say, in a minute, why a hook is stronger than a rule and when a rule is enough.

## A note on hook loopholes

A hook that watches the Edit tool does not see the same change made through the shell (`sed -i`, `echo >`). The guard in this repo has this exact gap. Finding it is part of the exercise; closing it (by restricting shell permissions, or watching the shell tool too) is a real design decision with trade-offs, and it belongs to you.
