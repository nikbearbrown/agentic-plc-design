# Workshop plan: JP's first run

## Executive summary

**What this is.** The plan for a set of short step-by-step films for JP, a working panel builder who will follow along on a Windows computer, install the course tools, do the labs, and tell us where the tutorials are wrong. It follows the `workshop` skill (orientation, one film per stretch of work, a closing conversation) and its two laws that matter most here: every film shows **real work that was actually done and recorded**, and says plainly what was not run.

**Why it is built this way.** JP is the expert; the tutorials were written and run only by AI agents. The films exist so he can follow along without guessing, and so his corrections come back as real changes. His own run is the first human evidence, so the films treat it as evidence to capture, not just a lesson to deliver.

**What it found.** Three things shape the set:
1. **JP is on Windows, and nothing has been run on Windows.** Every lab command has run only on a Mac. The Windows route is WSL (Ubuntu inside Windows). Films cannot honestly show a Windows run that nobody has done.
2. **The terminal parts are real and recordable now.** Installing the compiler and running the labs was done from a clean copy on a Mac; the commands and text are the same inside Ubuntu.
3. **The agent needs a paid account; the labs do not.** Claude Code needs a Claude paid plan or a Console account. The labs themselves need no account, key or cloud service and run offline after one-time downloads.

**What this does not do.** It builds no film yet. No film is recorded, voiced or rendered. No part of the set has been watched or followed by JP.

## Audience and what they arrive knowing

JP builds and tests control panels in a shop and reads ladder schematics well. He is new to a terminal, to WSL, to Python tooling and to AI agents. Do not assume he knows what a "repo", "PATH" or "build" means; each film names a term the first time it uses it.

## What JP will have by the end

- Ubuntu running inside his Windows computer, and the agent working in it.
- The course's lab tools installed in one folder, and a green test run.
- One compiled control program he has run and watched a deliberately broken version of fail.
- A first entry in the feedback ledger, in his own words.

## Run of show (designed to; no person has timed it)

| Move | What JP does | Film that supports it |
|---|---|---|
| Orient | Watch: what the next stretch is, what he will have, what we need from him | start |
| Get Ubuntu and the agent | Install WSL, Ubuntu, basic tools, Claude Code, log in | windows |
| Get the course and the compiler | Clone, check, build the compiler, first compiled run | install |
| Control logic | Labs that compile and run real control code, predict-then-check | control-logic |
| Break it, then fix it | Faulty programs, the plant, the two models that disagree | break-and-fix |
| Drawings | Edit a drawing file by script, safely, on a copy | drawings |
| Say what you found | The ledger; what to record | talk |

These are steps in a sequence, not choices to pick from, which is a departure from the workshop skill's "every choice, equal weight." Decision for Nik: keep a sequence (recommended for one learner) or offer tracks later when there are several learners.

## The films

All use the `claude-liam` channel (Liam in for Nik, free Kokoro voice) and the playlist name "JP's first run", spoken in the opening title card. No film is numbered anywhere a viewer can see.

| Film folder (under `youtube/`) | What it shows | Real evidence it is built from | Status |
|---|---|---|---|
| `claude-liam-workshop-jp-first-run-start` | The stretch ahead, what JP will have, what we need from him | The finished results of the other films, as real captures | Not started |
| `claude-liam-workshop-jp-first-run-windows` | WSL, Ubuntu, the basic tools, Claude Code, login | **None yet.** Must come from a real Windows run. Best source: record JP's own screen (with his OK) while he does Steps 1 to 3 of `jp/START-WINDOWS.md` | Blocked on a recording |
| `claude-liam-workshop-jp-first-run-install` | Clone, check, build the compiler, first compiled run | A clean-clone install and lab run on a Mac on 2026-10-27 (see below); replace with JP's Ubuntu run when it exists | Evidence being collected |
| `claude-liam-workshop-jp-first-run-control-logic` | Compiled labs: starter, timers, duplex contract | Real runs of the labs from the same clean clone | Not started |
| `claude-liam-workshop-jp-first-run-break-and-fix` | Mutations, the toy plant, the two models that disagree | Real runs of those labs | Not started |
| `claude-liam-workshop-jp-first-run-drawings` | Safe drawing edits with the open-source library; the AutoLISP route as the part only JP can run | Real run of the drawing lab | Not started |
| `claude-liam-workshop-jp-first-run-talk` | Now we talk: what did you do, what surprised you, what would you change | JP's feedback entries, once they exist | Waits for JP |

Every beat that shows a terminal shows text from an actual run. A recreated screen is labelled as a recreation; where a real capture can be taken, a real capture wins. A film built from a Mac run says it was a Mac run.

## What the films must say honestly

- Which films come from a Mac and not from Windows, and that Ubuntu inside Windows is expected to behave the same but has not been seen to.
- That a small AI agent, not a person, ran the labs first.
- That no one has timed any lab; the hours are designed estimates.
- That the compiler used on Ubuntu will be gcc, not the clang the Mac runs used, and that is untested.

## Fallback when a tool fails

JP stops at the first failing step and records the last 30 lines of output and what he typed. A failure is not a setback: it is the finding we need, and the film for that step gets re-made from his real run.

## How JP's feedback changes the films

His corrections go in `feedback/` (in his words, traced to a commit). A film whose step he corrected is re-laid out from the corrected tutorial and his real run; the first version is kept, marked superseded, not deleted. Mac and other systems are converted at the very end, once the Windows run has shaped the labs; a second set of install films will be needed then.

## Two things only Nik can decide

1. **Whether to record JP's screen** during his setup to make the Windows film, and whether JP agrees. This is the only honest source for that film.
2. **Whether to push the lab branch** (`course/open-source-plc-labs`) to the public repository. JP's clone step needs it; today GitHub `main` has none of the labs.

## What is not tested

Everything on Windows, WSL and gcc; the Claude Code install on Ubuntu; every film; any lab by anyone other than an AI agent; DraftSight and AutoLISP; the time each step takes.
