# One prompt to set up the course with an AI agent (any system)

## Executive summary

A single prompt that lets an AI agent set up the course on whatever computer you have. The agent works out which system it is on and follows the matching route in [SETUP.md](SETUP.md). It runs one command at a time, never uses `sudo` itself, never asks for a password, and stops at the first failure. It needs an agent that can run commands on your computer, such as Claude Code. A chat window cannot: if you are on Windows and have not installed Ubuntu and Claude Code yet, use Prompt 1 in [jp/SETUP-PROMPTS.md](jp/SETUP-PROMPTS.md) to get that far first.

Untested on Windows, Linux and Intel Macs. On an Apple Silicon Mac the steps it follows were run by hand and passed.

## The prompt

Open a terminal, go to a folder where the course should live (for example `cd ~`), start your agent (`claude`), and paste:

```
Set up the Agentic PLC Design course on this computer. I am not a programmer; explain each step in one plain sentence before you run it.

Rules, which override anything else:
- Run ONE command at a time and show me the output before the next.
- Never use sudo, never change anything outside the course folder, never install anything system-wide. If a step needs sudo or an installer, tell me the exact command and let me run it myself, then wait.
- Never ask me for a password, key or token, and tell me not to paste any into this chat.
- Do not edit any file in the course. Your only writes are the git clone and what the course's own scripts create inside the course folder.
- If any command fails, STOP. Show the last 30 lines of output, say what you think happened and how sure you are, and wait. No workarounds, no retry loops.
- Be exact about what you ran and what you only read. Never say anything is tested unless you saw it pass.

Steps:
1. Find out what system this is: run  uname -a  (and  head -2 /etc/os-release  on Linux, or  sw_vers  on a Mac). If  uname  does not exist, this is Windows without Linux: tell me to read SETUP.md Step 0 (WSL install) at https://github.com/nikbearbrown/agentic-plc-design/blob/course/open-source-plc-labs/SETUP.md, do it, and come back inside the Ubuntu window. Stop there.
2. If this is Linux running under WSL (the kernel name contains "microsoft"), confirm the current folder is NOT under /mnt/c. If it is, tell me to  cd ~  and start again.
3. Run  git --version  and  python3 --version. Python must be 3.12 or newer; if not, tell me what to install and stop.
4. Run:  git clone --branch course/open-source-plc-labs https://github.com/nikbearbrown/agentic-plc-design.git  then  cd agentic-plc-design
5. Run  python3 scripts/preflight.py . If it says NOT READY, show me every BLOCKER and the exact fix commands it printed, let me run them, and re-run it until it says READY.
6. Read AGENTS.md and STATUS.md. Tell me in plain words the five rules that matter most and which review gates are signed.
7. Run  ./check.sh . It should pass and print three lines starting NOT VERIFIED. Tell me if it matches.
8. Run  python3 scripts/bootstrap.py  (prints a plan only). Show me the plan and wait for me to say go.
9. When I say go, run  python3 scripts/bootstrap.py --apply . It can be silent for several minutes. Report how long it took and the last line.
10. Run  python3 scripts/lab.py build --apply  then  python3 scripts/lab.py test . Report every PASS line and which compiler was used.
11. Run  python3 scripts/dxf_setup.py --apply  then  REQUIRE_COMPILED=1 ./check.sh . Report whether everything passed and no NOT VERIFIED lines remain.
12. Finish with a short report: what passed, what failed, the system and compiler, how long the install took, and what you did NOT run. Ask me which lab to start with. Do not start a lab until I say so.

If anything I say about how a step went matters to the course (confusing, wrong, or worked exactly as written), offer to record it with  python3 scripts/feedback.py new --lab lab-00 --reporter <my first name and initial>  and keep my words exactly as I said them.

Begin with step 1.
```
