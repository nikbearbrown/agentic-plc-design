## Executive summary

Build the open-source MatIEC compiler locally and execute a real Structured Text program compiled to native machine code. This lab establishes what software actually ran. The C scan harness is course code, not OpenPLC, Beremiz's runtime, a production PLC runtime or a Python mock. No hardware or network service participates. Allow 20–40 minutes for first setup and inspection; later builds take seconds.

## Before you start

Read the repository's `AGENTS.md` and [synthetic contract](SPEC.md). Ask the agent to run the commands while you inspect results; the blocks also make the workflow reproducible by a second learner. All blocks assume the repository root:

```sh
cd /Users/bear/Documents/CoWork/bear-textbooks/books/agentic-plc-design
python3 project/tools/apd.py --help
./check.sh
```

On another computer substitute the clone's absolute path once. The original design tests require Python 3.11+. The source installer requires **Python 3.12+** for safe archive extraction, plus a working C/C++ compiler, SDK/system headers, Make, Flex, Perl, curl and tar support. On the tested Mac these prerequisites already existed. This course does not install Command Line Tools, accept an Xcode license, use sudo, install Homebrew or change the network. If a prerequisite is missing, record the exact missing tool and stop setup for local owner action; the original Python lessons remain available.

Not sure your computer is ready? Run `python3 scripts/preflight.py`: it checks everything below read-only and prints the exact fix for your system. Full setup for Windows, Mac and Linux is in [SETUP.md](../SETUP.md).

Check the environment:

```sh
python3 --version
cc --version
c++ --version
make --version
flex --version
perl -v
curl --version
```

**Prediction:** Does a C compiler by itself understand Structured Text? No. MatIEC translates ST to C first. Reading or linting an ST file is not compiling it.

## 1. Review the isolated installation plan

```sh
python3 scripts/bootstrap.py
```

Expected: five official HTTPS source URLs, pinned versions, and `DRY RUN`. The installer reads [toolchain.lock.json](toolchain.lock.json). It builds M4 1.4.20, Autoconf 2.72, Automake 1.18.1, Bison 3.8.2 and MatIEC at the pinned commit inside `.toolchain/`. It does not put executables in system directories. A source checksum mismatch stops execution.

The hashes record the exact archives obtained from official sources over HTTPS; they are reproducibility checks, not a claim of independently verified author signatures. The MatIEC checkout is pinned by commit because its configured version string is only `0.1`. Do not replace the lock with `latest` to make a failing build disappear.

## 2. Build

```sh
python3 scripts/bootstrap.py --apply
```

Expected final line: `READY: .../.toolchain/prefix/bin/iec2c`. During a first build, configure may print nothing to the terminal for several minutes while checking C library functions. Logs are under `.toolchain/logs/`; inspect the relevant log if the command fails. After the downloads exist, the reproducible no-network route is:

```sh
python3 scripts/bootstrap.py --apply --offline
```

Successfully installed packages have a hash stamp and are reused. This is a source pin, not a promise of byte-identical binaries on different macOS SDKs. See [toolchain provenance](../reference/open-source-toolchain.md) for licenses and platform limits.

## 3. Review, then compile copies

```sh
python3 scripts/lab.py build
python3 scripts/lab.py build --apply
```

Expected: `Compiled: .../build/reference/plc-sim`. The first command prints its plan. The second creates a combined ST copy and a harness copy under `build/reference/`, runs MatIEC, and compiles the resulting C. Original source programs remain unchanged. Read `build/reference/compile.log` and `build/reference/build.json`: the latter records commands, source hashes, compiler version, platform and executable hash.

The build selects existing Homebrew LLVM if present, otherwise the existing `cc`. To make a chosen compiler explicit:

```sh
CC=/opt/homebrew/opt/llvm/bin/clang python3 scripts/lab.py build --apply
```

Use that path only if it exists on your Mac. The tested native-code compiler was LLVM; Apple SDK/system libraries are still host prerequisites. macOS itself is not open-source. No claim that the entire host is open-source is made.

## 4. Run the first real scan tests

```sh
python3 scripts/lab.py foundations
```

Expected: `PASS foundations: 8 truth rows, latch/stop precedence, R_TRIG, CTU, TON boundary/reset`.

A pass means the **compiled ST** produced the asserted outputs through the C harness. Python only drove inputs and checked outputs. It does not mean OpenPLC ran, a GUI was installed, or a real panel was validated.

## Troubleshooting without guessing

| Symptom | Inspect / action |
|---|---|
| `Could not resolve host` | Network policy or connectivity; use approved access to the exact official source, or offline cached archives. Do not use a random mirror. |
| `Wrong bison version ... 2.3` | The isolated prefix is missing from the installer environment. Do not modify Apple's `/usr/bin/bison`. |
| M4 cannot produce accurate traces | Build the pinned M4 first. Apple's older M4 was insufficient during the author probe. |
| Compiler missing | Setup has not completed; inspect the last package log. |
| `CHECKSUM MISMATCH` | Preserve the bad download for investigation; do not change the expected hash just to continue. |
| ST syntax/type error | Read `compile.log`; keep the original and repair a learner copy only. |
| AssertionError | The program ran and disagreed with a test. Preserve the failing input and expected/actual values. |

## Evidence and stopping point

Keep the environment versions, build receipt and command outcome in your learner notes. Explain which process translated ST and which executed the generated native code. Stop for human review before the next learner module. No engineering gate is signed by setup.
