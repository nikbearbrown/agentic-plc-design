# Set up the course on your computer

## Executive summary

**What this is.** One setup guide for any computer: Windows, Mac or Linux. The lab tools are Linux-style command-line programs, so every route ends in the same place, a Unix-style terminal with the course folder in it, and from there the steps are identical. What differs is only how you get that terminal.

**What it needs.** No account, no API key, no cloud service, no server. The tools download once (from GNU, GitHub and the Python package index), build inside the course folder, and then everything runs offline. The one optional exception is an AI agent to help you: Claude Code needs a paid Claude plan (Pro, Max, Team or Enterprise) or an Anthropic Console account; the free Claude plan does not include it. You can do every lab without an agent by typing the commands yourself.

**What has been tested.** Only the Mac. On an Apple Silicon Mac, from an empty folder, the install took about 3.5 minutes and every lab and check passed, with both Homebrew's clang and Apple's own compiler. **Windows (through WSL), Linux and Intel Macs have not been run.** Where a step does not work as written on your system, that is a finding: write it in `feedback/` (see the end).

**Fastest route.** Run `python3 scripts/preflight.py` once you have the course folder: it checks your system, says what is missing, and prints the exact command to fix each thing for your system. Or paste the prompt in [SETUP-PROMPT.md](SETUP-PROMPT.md) into an AI agent and let it do the steps one at a time.

---

## Pick your route

| Your computer | Route | Status |
|---|---|---|
| **Windows 10 (2004+) or 11** | Install WSL, which runs Ubuntu inside Windows, and work in the Ubuntu window | **Not tested.** See [jp/START-WINDOWS.md](jp/START-WINDOWS.md) for the detailed version |
| **Mac, Apple Silicon** | Work in Terminal directly | **Tested** (clean install, 2026-10-27) |
| **Mac, Intel** | Work in Terminal directly | Not tested; expected to work |
| **Linux (Ubuntu 24.04 or newer, or similar)** | Work in your terminal directly | Not tested; expected to work |

## Step 0: get a terminal

**Windows.** Open PowerShell as administrator (Start, type `PowerShell`, right-click, Run as administrator), run `wsl --install -d Ubuntu-24.04`, and restart. An Ubuntu window opens after the restart; choose a username and password (the password does not show as you type). **Do everything below inside the Ubuntu window**, and keep the course inside Ubuntu's home folder (`cd ~`), not on `C:\`. If a company policy blocks WSL or administrator rights, stop and ask your IT team.

**Mac.** Open Terminal (Command-Space, type `Terminal`). If it offers to install "command line developer tools", accept; that gives you `make`, a compiler, `git` and the rest.

**Linux.** Open a terminal.

You also need **git** and **Python 3.12 or newer**. Check:

```bash
git --version
python3 --version
```

The stock Python on a Mac is older than 3.12 and does not work for the install: install a newer one from https://www.python.org/downloads/ (or `brew install python`), then open a new Terminal window. On Ubuntu 24.04 the default is already 3.12.

## Step 1: get the course

```bash
cd ~
git clone --branch course/open-source-plc-labs https://github.com/nikbearbrown/agentic-plc-design.git
cd agentic-plc-design
```

(The labs live on that branch for now. Once they are merged into the main branch, the `--branch` option is not needed.)

Keep the folder path free of spaces. The compiler's build scripts break on them.

## Step 2: check your computer

```bash
python3 scripts/preflight.py
```

It changes nothing. It checks your system, Python, the build tools (`make`, a C and C++ compiler, `flex`, `perl`, `curl`, `git`), the folder you are in, and free disk space. If something is missing it prints the exact command for your system, for example on Ubuntu:

```bash
sudo apt update && sudo apt install -y build-essential flex curl git perl python3 python3-venv python3-pip
```

Run those, then run the check again until it says `READY`.

## Step 3: check the course itself

```bash
./check.sh
```

Expected: it ends passing, and prints three lines starting `NOT VERIFIED` (native protocol checks, compiled labs, the drawing lab). Those are the parts you install next.

## Step 4: install the lab compiler (the long step)

```bash
python3 scripts/bootstrap.py            # prints the plan; changes nothing
python3 scripts/bootstrap.py --apply    # does it
```

This downloads five small open-source programs, checks each against a pinned fingerprint, and builds them inside the course folder in a hidden `.toolchain/` folder. It needs no administrator rights and does not touch the rest of the computer. It can sit silent for a few minutes; on an Apple Silicon Mac it took about 3.5 minutes. Expected final line: `READY: .../iec2c`.

## Step 5: build and run the first lab programs

```bash
python3 scripts/lab.py build --apply
python3 scripts/lab.py test
```

Expected: `Compiled: ...plc-sim`, then lines starting `PASS`, ending `PASS all compiled labs`. One line says `OBSERVED original comparison: 37 rows, 2 pump-output differences`; that is a known finding, not an error.

On Linux and WSL the compiler will be gcc, not the clang used in the tested runs. If the build fails, copy the last 30 lines and stop.

## Step 6: install the drawing lab (optional)

```bash
python3 scripts/dxf_setup.py --apply
REQUIRE_COMPILED=1 ./check.sh
```

Expected: `READY: ezdxf 1.4.5`, and then a check that passes with none of the `NOT VERIFIED` lines left.

## Step 7: start the labs

Open [labs/README.md](labs/README.md) and work down the table, predicting before you run. If you have an AI agent, start it in the course folder (`claude`) and see [SETUP-PROMPT.md](SETUP-PROMPT.md) for a safe first message.

To install Claude Code, run the one command for your system from https://code.claude.com/docs/en/setup (on Mac, Linux and WSL: `curl -fsSL https://claude.ai/install.sh | bash`), open a new terminal, and run `claude`. Install it inside Ubuntu on Windows. Never paste a key or password into an agent's chat.

## Tell us what happened

Whatever you find is useful: a step that failed, a message that was confusing, a step that worked exactly as written. Record it with:

```bash
python3 scripts/feedback.py new --lab lab-00 --section 4 --reporter JP --kind wrong --severity major
```

(Change `--reporter` to your first name and initial.) Keep your own words exactly as you said them. See [feedback/README.md](feedback/README.md).

## Removing everything

Delete the course folder. Everything the labs installed lives inside it. WSL, Claude Code and Python are separate and are removed the way you removed any program on your system.
