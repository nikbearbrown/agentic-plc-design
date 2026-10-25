## Executive summary

The runnable course uses MatIEC for IEC Structured Text compilation, an existing LLVM C compiler for native code, Python's standard library for tests and a toy plant, and a self-contained HTML viewer for recorded evidence. It was built on Apple Silicon macOS, without Docker, a vendor PLC IDE, an account or a paid service. MatIEC is a compiler; the course supplies the scan harness. No production PLC runtime was installed or claimed.

## Sources checked 2026-10-25

| Component | Pin / license | Official source and purpose |
|---|---|---|
| MatIEC | Git commit `3a41303bcb4e50403417bc39c63f88981d7d961e`; compiler GPL-3.0-or-later | [Beremiz repository](https://github.com/beremiz/matiec), [build instructions at pin](https://github.com/beremiz/matiec/blob/3a41303bcb4e50403417bc39c63f88981d7d961e/README.build), [COPYING](https://github.com/beremiz/matiec/blob/3a41303bcb4e50403417bc39c63f88981d7d961e/COPYING) |
| MatIEC IEC library | Same commit; `iec_std_lib.h` carries LGPL version 2 or later notice | [Header](https://github.com/beremiz/matiec/blob/3a41303bcb4e50403417bc39c63f88981d7d961e/lib/C/iec_std_lib.h); other files retain their own notices. We do not redistribute the dependency tree or binaries. |
| GNU M4 | 1.4.20; GPL-3.0-or-later | [GNU M4](https://www.gnu.org/software/m4/), official archive URL and SHA-256 in lock |
| GNU Autoconf | 2.72; GPL-3.0-or-later, generated configure exception | [GNU Autoconf](https://www.gnu.org/software/autoconf/) |
| GNU Automake | 1.18.1; GPL-2.0-or-later, generated Makefile exception | [GNU Automake](https://www.gnu.org/software/automake/) |
| GNU Bison | 3.8.2; GPL-3.0-or-later with parser exception | [GNU Bison](https://www.gnu.org/software/bison/) |
| LLVM/Clang | Existing Homebrew LLVM 22.1.7; Apache-2.0 with LLVM exceptions | [Clang](https://clang.llvm.org/), [LLVM license](https://llvm.org/docs/DeveloperPolicy.html#license); used for generated C. Not newly installed. |
| Python | Existing 3.14.6; PSF license | [Python documentation](https://docs.python.org/3.14/), [license](https://docs.python.org/3/license.html); no third-party Python package needed |
| Host tools | Existing Make 3.81, Flex 2.6.4 (Apple build), Perl, curl and C/C++ compiler/SDK | Exact host output is in the execution ledger. Apple developer tools and macOS are host prerequisites, not presented as wholly open-source. |

The [lock file](../labs/toolchain.lock.json) pins every newly downloaded archive by URL and SHA-256. The compiler's printed version `0.1` is not a sufficient identity; use its commit. Bootstrapping uses the existing host C/C++ compiler to build GNU tools and MatIEC. The ST native harness uses the compiler selected in its build receipt.

## What upstream says, and what we measured

MatIEC's [readme](https://github.com/beremiz/matiec/blob/3a41303bcb4e50403417bc39c63f88981d7d961e/readme) describes textual ST/IL/SFC translation to C and a separate native compilation step. This course exercises **ST only**, including R_TRIG, CTU and TON. It does not test Ladder/FBD editing, every IEC type, or conformance to later IEC editions. The source describes an older IEC draft baseline; do not call this a full current-standard conformance suite.

[Beremiz](https://beremiz.org/) provides a broader IDE/runtime ecosystem. We use its MatIEC compiler component directly to keep the macOS teaching path small and inspectable. The compiler built natively on this host. That measured fact does not establish official support for all macOS versions or for Beremiz's GUI on this Mac.

OpenPLC and vendor IDE paths remain **NOT VERIFIED**. We did not install them just to turn an optional GUI into a prerequisite. The local compiled harness gives stronger evidence than the former uncompiled ST file while explicitly stopping short of a production runtime claim.

## Isolation and reproducibility

Downloads, source builds, installed tools and logs stay in `.toolchain/`; generated programs and traces stay in `build/`. Both are ignored by Git. Scripts never write physical I/O or open industrial connections. No server is needed; the trace viewer opens as an offline file. No privileged package or network changes were made.

The tested platform is macOS 26.5.1 build 25F80, arm64. Linux and Intel macOS builds are **NOT VERIFIED**. Windows native setup is **NOT VERIFIED**; do not assume the POSIX scripts or `select`-based pipe timeout will work there. Source archives are reproducible inputs, but compiler/SDK differences can produce different binaries. No container or binary reproducibility claim is made.

## Known diagnostics and limits

Clang emits warnings from MatIEC's generic standard-function headers, including variadic argument promotion and pointer-sign warnings, plus generated-code parenthesis diagnostics. Full warnings are retained in `build/reference/compile.log`. The course exercises Boolean operations, time and small integer counts; it does not exercise the generic variadic arithmetic/string functions implicated by those warnings. This is a limitation, not a claim that the upstream warnings are fixed or harmless in arbitrary programs.

The course's own initial harness probe omitted `accessor.h` and failed compilation. After adding that required header, a counter test exposed uninitialized C storage flags. Zero-initializing function block storage before MatIEC initialization repaired the harness. These were course integration errors, not evidence that TON or CTU should have their expected results weakened.

## License boundary

These open-source tool licenses do not relicense the course repository, whose existing all-rights-reserved notice is preserved. The course-authored source files are not advertised as independently open-source. Before redistributing built binaries or library headers, review their individual notices and applicable source-distribution obligations; this work only commits course source, lock files and selected textual execution evidence. No third-party vendor skill code is copied into the teaching stack.
