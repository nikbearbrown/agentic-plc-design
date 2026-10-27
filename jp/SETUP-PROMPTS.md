# Setup prompts for JP

## Executive summary

Two prompts JP can paste into an AI so that the AI does the setting up and JP just watches, answers questions and copies output. Use **Prompt 1** first, in any chat assistant, to get Ubuntu and Claude Code onto the Windows computer. A chat window cannot touch JP's computer, so this prompt coaches JP through the few steps that must be done by hand. Use **Prompt 2** after that, inside Claude Code in Ubuntu: it can run the commands itself and set up the whole course. Both are written so nothing is installed outside the course folder (apart from the standard Ubuntu tools in Prompt 1's step) and nobody is asked for a password or key.

Nothing here has been run on Windows. If either prompt goes wrong, that is the finding: copy what happened into the feedback ledger.

The same steps, as plain instructions without an AI, are in [START-WINDOWS.md](START-WINDOWS.md).

---

## Prompt 1: get Ubuntu and Claude Code onto Windows (paste into any chat assistant)

```
I am JP. I build and test industrial control panels and I am comfortable with ladder schematics, but I am new to terminals. I want to set up a course on my Windows computer, and the course tools only run on Linux, so I need Ubuntu inside Windows (called WSL) and then the Claude Code agent inside Ubuntu.

Coach me through this one step at a time. Rules for you:
- Give me ONE step, then wait for me to tell you what happened. Never give two steps at once.
- Use ONLY the commands in this message. Do not invent other commands, flags or menu paths. If something goes wrong and these commands do not cover it, say you are not sure and tell me to stop and copy the exact error text.
- Tell me exactly where to type each command (PowerShell as administrator, or the Ubuntu window) and what I should see afterwards. When I paste what I see, compare it to what you told me to expect.
- Never ask me for a password, a key or a login code, and tell me not to paste any into this chat. When Ubuntu asks me to choose a password, remind me it will not show characters as I type.
- If I am on a work computer that blocks administrator access or virtualization, stop and tell me to ask whoever manages it.

The steps:
1. Check my Windows version: Start, type winver. It must be Windows 10 version 2004 or newer, or Windows 11.
2. Open PowerShell as administrator (Start, type PowerShell, right-click, Run as administrator) and run:  wsl --install -d Ubuntu-24.04
   If the name is not recognised, run  wsl --list --online  and use the Ubuntu 24.04 name shown. Then restart the computer when asked.
3. After the restart an Ubuntu window opens. I choose a username and password. I should then see a prompt like  name@COMPUTER:~$
4. In the Ubuntu window run:  sudo apt update
   then:  sudo apt install -y build-essential flex curl git python3 python3-venv python3-pip
   then:  python3 --version   It must say Python 3.12 or higher. If not, stop.
5. In the Ubuntu window run:  curl -fsSL https://claude.ai/install.sh | bash
   It shows no progress while it works. Then I close the Ubuntu window, open a new one, and run:  claude --version   I should see a version number.
6. Run  claude  and follow the browser sign-in. Claude Code needs a paid Claude plan (Pro, Max, Team or Enterprise) or an Anthropic Console account. If I do not have one, tell me and stop; I can still do the course by typing commands myself.
7. When claude is running in Ubuntu, tell me I am ready for the next prompt and stop.

Begin with step 1.
```

## Prompt 2: set up the course (paste into Claude Code, inside Ubuntu)

Open the Ubuntu window, make sure you are in your home folder (`cd ~`), run `claude`, and paste:

```
I am JP, an experienced control panel builder who is new to terminals. I am using Windows with Ubuntu (WSL). You are running inside Ubuntu in my home folder. Set up the Agentic PLC Design course for me.

Rules, which override anything else:
- Run one command at a time and show me the output before the next. Explain each in one plain sentence first.
- Never use sudo, never change anything outside the course folder, never install anything system-wide, and never download anything other than what the course scripts themselves download. If something needs sudo, tell me the exact command and let me run it myself.
- Never ask me for a password, key or token.
- Do not edit any file in the course. Your only writes are the git clone and what the course's own install scripts create inside the course folder.
- If any command fails, STOP. Show me the last 30 lines of output, say what you think happened and how sure you are, and wait. Do not try workarounds and do not retry in a loop.
- Be exact about what you ran and what you only read. Never say something is tested unless you saw it pass.

Steps:
1. Run  pwd,  python3 --version  and  head -2 /etc/os-release  and tell me the results. If Python is older than 3.12, stop.
2. Check these are present: make, gcc, g++, flex, perl, curl, git, and that python3 can run  python3 -m venv --help . For anything missing, tell me the exact apt command for me to run, then wait.
3. Run:  git clone --branch course/open-source-plc-labs https://github.com/nikbearbrown/agentic-plc-design.git  then  cd agentic-plc-design  and  ls .
4. Read AGENTS.md, STATUS.md and jp/START-WINDOWS.md. Tell me in plain words the five rules that matter most and which review gates are signed.
5. Run  ./check.sh . It should end by passing but print three lines starting NOT VERIFIED. Tell me if it matches.
6. Run  python3 scripts/bootstrap.py  (this only prints a plan). Show me the plan and wait for me to say go.
7. When I say go, run  python3 scripts/bootstrap.py --apply . It can be silent for several minutes. Tell me how long it took and the last line.
8. Run  python3 scripts/lab.py build --apply  then  python3 scripts/lab.py test . Tell me every PASS line.
9. Run  python3 scripts/dxf_setup.py --apply  then  REQUIRE_COMPILED=1 ./check.sh . Tell me if everything passed and none of the NOT VERIFIED lines remain.
10. Finish with a short report: what passed, what failed, the compiler used (gcc or something else), how long the install took, and what you did NOT run. Then ask me which lab I want to start with. Do not start any lab until I say so.

If anything I say about how a step went matters to the course (a step was confusing, wrong, or worked exactly as written), offer to record it with  python3 scripts/feedback.py new --lab lab-00 --reporter JP  and keep my words exactly as I said them.

Begin with step 1.
```
