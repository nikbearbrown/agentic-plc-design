# AR-0002: clean-clone install and lab run on a Mac

## Executive summary

An AI agent (Claude) cloned the course branch into an empty folder on a Mac on 2026-10-27, installed the lab tools from nothing, and ran the checks, so there is a record of what the install really does and how long it takes before JP tries it on Windows. It worked: the compiler built in about 3.5 minutes, every compiled lab passed, and the drawing lab installed in 8 seconds. It also showed three honest `NOT VERIFIED` lines before the tools were installed. This is Mac evidence only. Nothing was run on Windows, WSL, Ubuntu or gcc. Status: awaiting JP.

## Environment

macOS arm64, Python 3.14.6, host compilers Apple clang and Homebrew clang 22.1.7 (the build picks Homebrew clang). Fresh `git clone --branch course/open-source-plc-labs` of the local repository at commit `b0dfe99`, into an empty folder; no `.toolchain/` existed beforehand.

## What was run and what happened

| Step | Command | Result |
|---|---|---|
| Plan | `python3 scripts/bootstrap.py` | Five pinned downloads listed; DRY RUN; nothing written |
| Install | `python3 scripts/bootstrap.py --apply` | `READY: .../.toolchain/prefix/bin/iec2c`, exit 0, **202.6 s** wall time |
| Check before compile | `./check.sh` | Pass, with three `NOT VERIFIED` lines: native protocol checks, compiled labs, DXF lab |
| Build | `python3 scripts/lab.py build --apply` | `Compiled: .../build/reference/plc-sim`, 1.2 s |
| Run | `python3 scripts/lab.py test` | `PASS foundations`, `PASS station` (1024 input images), two replays, `OBSERVED original comparison: 37 rows, 2 pump-output differences`, `PASS all compiled labs` |
| Drawing lab | `python3 scripts/dxf_setup.py --apply` | `ezdxf 1.4.5` installed, 8.1 s |
| Everything | `REQUIRE_COMPILED=1 ./check.sh` | 51 unit tests OK (11 skip under system Python), compiled labs PASS, ledger check 0 problems, 11 DXF tests OK, exit 0 |

## Not run

Windows, WSL, Ubuntu; gcc (the Mac build used clang); Claude Code or any other agent installed by the agent; offline reuse after install; Intel Macs; any step by a person.

## Questions for JP

1. Did the compiler build finish on your machine, and how long did it take?
2. Did `lab.py build --apply` work with gcc? Copy the last 30 lines if not.
3. Did you see the same three `NOT VERIFIED` lines before installing and none after?
4. Was any step confusing, or in the wrong order?
