#!/bin/sh
# Runs every check in the repo. Exit 0 = all pass. Safe: reads files, writes nothing.
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
