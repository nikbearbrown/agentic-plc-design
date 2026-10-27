# JP: start here (Windows)

## Executive summary

**What this is.** The exact steps, in order, for JP to get the course tools running on a Windows computer and do the labs while an AI agent helps. Every step says what to type, what you should see, and when to stop and tell us.

**Why it is shaped this way.** The lab tools are Linux-style programs. On Windows the simplest way to run them is WSL, which is Microsoft's built-in way to run Ubuntu Linux inside Windows. Everything below happens inside that Ubuntu window except Step 1.

**What has and has not been tested.** The commands inside Ubuntu were run on a Mac, which behaves like Linux for these tools, and passed. **Nobody has run these steps on Windows or WSL yet. You are the first.** That is the point: where a step does not work or does not match what we wrote, that is the finding we need. Write it down (Step 9).

**What it costs and needs.** The labs themselves need no account, no API key, no cloud service. Tools download once from GNU, GitHub and PyPI and then everything runs offline on your machine. **The AI agent is different:** Claude Code needs a paid Claude account (Pro, Max, Team, Enterprise) or an Anthropic Console account. You can do every lab without the agent by typing the commands yourself.

**Time.** Plan on about an hour for Steps 1 to 6 (most of it waiting for software to download and build). Each lab after that is 1 to 3 hours (designed estimates; no person has timed them).

---

**Prefer to have an AI do it?** Use [SETUP-PROMPTS.md](SETUP-PROMPTS.md): one prompt coaches you through Steps 1 to 3, and a second one lets Claude Code do Steps 4 to 7 for you, one command at a time.

## Before you start

- Windows 10 version 2004 or newer, or Windows 11. (Check: Start, type `winver`.)
- You can use "Run as administrator" on this computer. If it is a work computer with restrictions, stop and tell us now.
- About 10 GB free disk space and an internet connection.
- The computer's virtualization turned on (usually already is). If Step 1 complains, stop and tell us.

## Step 1: Install Ubuntu inside Windows (about 10 minutes plus a restart)

1. Click Start, type `PowerShell`, right-click **Windows PowerShell**, choose **Run as administrator**.
2. Paste:

```powershell
wsl --install -d Ubuntu-24.04
```

3. Restart the computer when it asks.
4. After the restart an Ubuntu window opens by itself. Wait for it to finish unpacking, then choose a username and password for Linux. (You will type this password when a command starts with `sudo`. It does not show characters as you type; that is normal.)

**You should see** a prompt that looks like `yourname@COMPUTERNAME:~$`.

**If `Ubuntu-24.04` is not recognized:** in PowerShell run `wsl --list --online`, find the Ubuntu 24.04 entry, and use the name shown. The course needs Ubuntu 24.04 (or newer) because it needs Python 3.12 or newer.

**Whenever the steps below say "Ubuntu window"** it means this window. To open it later: Start, type `Ubuntu`, press Enter.

## Step 2: Install the basic tools (about 3 minutes)

In the Ubuntu window:

```bash
sudo apt update
sudo apt install -y build-essential flex curl git python3 python3-venv python3-pip
python3 --version
```

**You should see** `Python 3.12.x` or higher. If it says 3.10 or 3.11, you have an older Ubuntu: stop and tell us.

## Step 3: Install Claude Code (about 2 minutes)

Still in the Ubuntu window:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

The installer shows no progress while it downloads; wait for it to finish. Then **close the Ubuntu window and open a new one**, and check:

```bash
claude --version
```

**You should see** a version number. If it says `command not found`, stop and tell us (the official fix is to add the install folder to your PATH).

Log in by running `claude` and following the browser prompts. Do not paste any keys or passwords into the agent's chat.

## Step 4: Get the course (about 1 minute)

Always work inside Ubuntu's own folders (the `~` home folder), **not** in `C:\` through `/mnt/c`, which is slow and breaks file permissions.

```bash
cd ~
git clone --branch course/open-source-plc-labs https://github.com/nikbearbrown/agentic-plc-design.git
cd agentic-plc-design
ls
```

**You should see** folders including `labs`, `modules`, `project`, `scripts`, `feedback`, `jp`.

## Step 5: Check the course tools work (about 1 minute)

```bash
./check.sh
```

**You should see** `ok: flawed controller fails as designed` and `PASS course index and local links`. Near the end it will print three lines starting `NOT VERIFIED` (native protocol checks, compiled labs, and the DXF lab) because you have not installed the compiler yet. That is expected, and fixing it is the next two steps.

## Step 6: Install the lab compiler (the long wait)

This downloads five small open-source programs and builds them **inside the course folder**, in a hidden folder called `.toolchain`. It does not touch the rest of the computer and needs no administrator rights.

First look at what it plans to do (this changes nothing):

```bash
python3 scripts/bootstrap.py
```

**You should see** five download lines (m4, autoconf, automake, bison, matiec) and the words `DRY RUN`.

Then do it:

```bash
python3 scripts/bootstrap.py --apply
```

It can sit silent for a few minutes while it works; that is normal. On a Mac it took about 3 and a half minutes from a clean copy; Windows is unknown. **You should see** a final line starting `READY:` and ending in `iec2c`.

Build and test the first lab program:

```bash
python3 scripts/lab.py build --apply
python3 scripts/lab.py test
```

**You should see** `Compiled:` followed by a path ending in `plc-sim` (the build takes a second or two), then lines beginning `PASS`, ending with `PASS all compiled labs`. One line says `OBSERVED original comparison: 37 rows, 2 pump-output differences`; that is a known finding, not an error.

**On Ubuntu the compiler used will be gcc** (the Mac runs used clang). We expect that to work but have not seen it. If a build error appears, copy the **last 30 lines** and stop; that is a finding.

## Step 7: Optional drawing-edit lab (about 3 minutes)

```bash
python3 scripts/dxf_setup.py --apply
```

**You should see** `READY: ezdxf 1.4.5`. (About 8 seconds on a Mac.) Now run `REQUIRE_COMPILED=1 ./check.sh` again: this time everything should pass and the `NOT VERIFIED` lines are gone.

## Step 8: Do the labs, with or without the agent

Open [labs/README.md](../labs/README.md) and work down the table from Lab 00. Each lab tells you what to predict first, then which commands to run, then what you should see.

**With the agent:** in the Ubuntu window, in the course folder, run `claude` and send this first message:

```
Read AGENTS.md and labs/README.md. I am JP, an experienced panel builder, doing these labs on Windows through WSL Ubuntu. Do not change any file. Tell me in plain words what Lab 00 asks me to do and which commands you would run. Then wait for me to say go. Run one command at a time and show me the output.
```

You decide when it runs each step. Read what it does. If it tries to edit a course file instead of working in `scratch/`, say no.

**Without the agent:** type the commands from each lab yourself.

## Step 9: Tell us what you find (this is the real job)

You are the expert; the labs were written and run by AI agents. Where you disagree, where a step fails, or where something is unclear or just right, write it in the feedback ledger:

```bash
python3 scripts/feedback.py new --lab lab-00 --section 2 --reporter JP --kind wrong --severity major
```

That creates a file in `feedback/entries/`. Open it and fill in: what you did, **what you said in your own words** (do not tidy it), and the sentence in the lab you were responding to. Or just say it out loud on the call and someone will write it up with your words kept as you said them.

Record the good things too: "this step worked exactly as written" is evidence.

## If something goes wrong

| What you see | What to do |
|---|---|
| `command not found` | Close the Ubuntu window and open a new one, then try again. If it persists, stop and tell us the exact command and message |
| A build fails | Copy the last 30 lines of output. Do not try to fix it. That is a finding |
| The agent asks to run something that deletes, installs system-wide with `sudo`, or reaches outside the course folder | Say no. Tell us what it asked |
| You are not sure | Stop and ask. A step done wrong silently is worse than a step skipped |

## Removing everything later

Delete the course folder (`rm -rf ~/agentic-plc-design` in Ubuntu) and everything the labs installed goes with it. WSL and Claude Code are separate; they are removed through Windows Settings and the Claude Code uninstall steps.
