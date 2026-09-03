#!/usr/bin/env bash
# Every gate this deck has, in one command. Run before any commit that touches deck.html.
#
# These exist because each of them catches a defect that ALREADY shipped once, was
# fixed, and came back - the rule was written down and violated anyway. A check that
# runs is worth more than a rule that is remembered.
set -u
cd "$(dirname "$0")/.." || exit 1
fail=0

echo "== 1. regressions: flash / type floor / SVG class scoping =="
python3 tools/check_regressions.py || fail=1

echo
echo "== 1b. glossary: authoritative coverage / full-surface ledger / A–Z integration =="
python3 tools/audit_glossary.py || fail=1

echo
echo "== 2. inventory: png dumps, text walls, sub-floor labels =="
python3 tools/slide_inventory.py --out /tmp/inventory_now.json || fail=1

if [ -f "${1:-}" ]; then
  echo
  echo "== 3. visual gate: no slide may become less visual =="
  python3 tools/slide_inventory.py --compare "$1" || fail=1
else
  echo
  echo "== 3. visual gate: SKIPPED - pass an earlier inventory.json as \$1 to compare =="
  echo "   take a baseline BEFORE editing:  python3 tools/slide_inventory.py --out /tmp/before.json"
fi

echo
[ "$fail" -eq 0 ] && echo "PREFLIGHT OK" || echo "PREFLIGHT FAILED"
exit "$fail"
