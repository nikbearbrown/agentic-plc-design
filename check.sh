#!/bin/sh
# Runs original tests plus executable-course checks. Writes temporary lint output and simulation traces only.
set -e
cd "$(dirname "$0")/project"
echo "== unit tests (correct controller) =="
python3 -m unittest discover -s tests
echo "== the flawed controller must FAIL its tests (that is the point) =="
if APD_TEST_FLAWED=1 python3 -m unittest discover -s tests -p test_sim.py >/dev/null 2>&1; then
  echo "ERROR: flawed controller passed; the tests are too weak" ; exit 1
else
  echo "ok: flawed controller fails as designed"
fi
echo "== generated LISP passes the safety lint =="
TMP="$(mktemp)"
python3 tools/lisp_gen.py variants/a-baseline.toml --swap "7.5 HP=10 HP" > "$TMP"
python3 tools/lisp_lint.py lisp/apd-lib.lsp "$TMP"
rm -f "$TMP"

cd ..
echo "== course links, manifest and native protocol =="
python3 scripts/check_course.py
if [ -x build/reference/plc-sim ]; then
  echo "== actual compiled ST and deterministic plant =="
  python3 scripts/lab.py test
else
  echo "NOT VERIFIED: compiled labs; run python3 scripts/lab.py build --apply after setup"
  if [ "${REQUIRE_COMPILED:-0}" = "1" ]; then exit 1; fi
fi
