# Feedback ledger

## Executive summary

**What this is.** The place where JP, the working panel builder who is the expert for this course, records what he finds when he does the labs, and where each finding is tied to the exact change it caused in the tutorials. Agents run the labs first and record what happened (see `agent-runs/`); JP then does the same labs by hand and says where the tutorial is wrong, unclear, missing, or right. Nothing in the course counts as expert-reviewed until an entry here says so.

**Why it exists.** The tutorials were written and run by AI agents. They can be internally consistent and wrong in ways only someone who builds panels would notice (a sequence that short-cycles a pump, a sizing rule that is too simple, a menu path that does not exist). A correction that lives in a chat or an email is lost. A correction in this ledger has a number, JP's own words, the sentence it corrects, a decision, and a link to the commit that fixed it, so any reader can follow it from complaint to change and check the change.

**What is in it today.** No JP entries. Nobody in the trade has run these labs. One agent run record (`agent-runs/AR-0001-lab-09-ezdxf.md`) is the baseline JP's run will be compared with.

## The loop

1. **Agent runs the lab** and writes a run record in `agent-runs/`: commands, outputs, hashes, versions, and what it did *not* run. Films are made from these real runs, never from imagined ones.
2. **JP does the same lab** with his own hands and, where he can, his own software (DraftSight, Studio 5000, a real tape measure).
3. **Anyone writes up what JP said** with `python3 scripts/feedback.py new ...`. JP's words go in verbatim. If an agent transcribes a call or recording, `transcribed_by` names it and the recording's location is kept.
4. **A human decides** (`decided_by`): accepted, rejected or won't fix, with a reason. An agent never decides and never fills `decided_by`.
5. **The tutorial changes** in a commit. The entry then records `tutorial_commit`, the files changed, and the check that now shows the right behaviour. Status becomes `fixed`.
6. **`python3 scripts/feedback.py check`** refuses an entry marked fixed with no real commit or missing files, any decided entry without a named human, an empty or placeholder verbatim section, and a stale index. `./check.sh` runs it.

## Rules

- **JP's words are not edited.** Do not summarise, correct spelling or "improve" the verbatim section. Voice dictation can be wrong; if so, add a clarification under Decision, never in the quote.
- **Wrong ones stay.** A rejected entry is kept with its reason. Deleting feedback to look tidy is the failure this ledger exists to prevent.
- **Facts only under "What was done."** What he ran, on what machine and software version, with exact error text.
- **Quote what he was responding to.** The sentence, command or result in the tutorial, with file and line, so the fix can be tested against it.
- **No agent signs engineering gates here or in `STATUS.md`.** Closing an entry is not signing a gate.
- **Names.** JP is recorded as "JP". Do not add surnames or other identifying details of reporters beyond first name and initial.
- **Company material.** Do not paste customer drawings, proprietary standards or company-internal text into an entry. Describe it and say where it lives.

## Files

| Path | What |
|---|---|
| [LEDGER.md](LEDGER.md) | Generated index of all entries. Do not edit by hand |
| [TEMPLATE.md](TEMPLATE.md) | Entry template; `feedback.py new` fills it |
| `entries/FB-NNNN.md` | One finding per file |
| `agent-runs/AR-NNNN-*.md` | What an agent actually ran, as a baseline for JP |

## Commands

```sh
python3 scripts/feedback.py new --lab lab-09 --section 3 --reporter JP --kind wrong --severity major
python3 scripts/feedback.py check
python3 scripts/feedback.py index
```

`kind`: wrong, unclear, missing, works, idea. `severity`: blocker, major, minor, nit. `status`: open, accepted, rejected, fixed, wont-fix. Record "works" too: confirmation that a step behaved as written is evidence.
