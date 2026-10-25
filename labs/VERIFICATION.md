## Executive summary

Author execution on 2026-10-25 has built the pinned open-source toolchain and run actual MatIEC-compiled ST in a deterministic native C scan harness on macOS arm64. All current compiled lab tests and three fault mutations have run successfully. The independent learner pass is pending at this checkpoint. No production PLC runtime, vendor IDE or hardware was used; all human gates remain unsigned.

## Checkpoint evidence

| Command | Actual outcome |
|---|---|
| `./check.sh` before expansion | 31 original tests passed; flawed Python controller rejected; generated LISP lint passed |
| `python3 scripts/bootstrap.py` | Dry-run plan only |
| `python3 scripts/bootstrap.py --apply --offline` | All five pinned source packages built under `.toolchain/`, then a second invocation reused them; exit 0 |
| `python3 scripts/lab.py build --apply` | MatIEC translated the ST copies and LLVM 22.1.7 produced a native arm64 executable; exit 0 |
| `python3 scripts/lab.py test` | Starter, standard FBs, station histories, 1024 input images, replay, repeatable plant and expected legacy discrepancies passed |
| `python3 scripts/lab.py mutations --apply` | Three faulty ST copies compiled; all three rejected by station assertions |
| `python3 scripts/view_trace.py build/reference/plant.csv --output build/reference/plant.html` | Offline HTML generated; browser interaction review pending |

Actual environment: macOS 26.5.1 build 25F80, arm64; Python 3.14.6; native-code compiler Homebrew Clang 22.1.7; host source-build compiler Apple Clang 21.0.0; MatIEC commit `3a41303bcb4e50403417bc39c63f88981d7d961e`; M4 1.4.20, Autoconf 2.72, Automake 1.18.1, Bison 3.8.2; host Flex 2.6.4. Full build commands, hashes and diagnostics are in `build/reference/build.json` and `build/reference/compile.log`.

## Observed findings

- Legacy comparison: 37 rows; two pump-command differences (T02 and T07, t=5 s). The Python model credits time on the first TRUE sample; the compiled TON starts elapsed time there. Original program/model files remain unchanged. Alarm interfaces are not fully equivalent.
- Normal toy plant: 1800 scans, maximum volume 72500 mL, zero spill, p1 on 648 scans, p2 on 563 scans.
- Both-trip plant: 84400 mL simulated spill, 355 high-alarm scans and 315 no-pump-alarm scans. This is a deliberately failing plant scenario that the test correctly reports.
- Initial integration repairs: required MatIEC accessor header added after compile errors; C function-block storage zero-initialized after a real CTU assertion failure. Tests were not weakened to hide either defect.
- Compiler warnings remain in the upstream generic headers/generated C; see [toolchain limits](../reference/open-source-toolchain.md). Original Python tests emit ResourceWarnings for existing unclosed fixture reads.

## NOT VERIFIED

OpenPLC runtime/editor, Beremiz IDE/runtime, DraftSight, Studio 5000, TwinCAT, Siemens TIA Portal, real electrical panels, live PLC/RTU/VFD/SCADA I/O, actual pump hydraulics, fieldbus behavior, hard-real-time scheduling, safety certification, complete IEC conformance, Intel macOS/Linux/Windows. Electrical tables remain unverified. No gate was signed. Nothing from this task was pushed or deployed.
