#!/usr/bin/env bash
# Regression for 2026-10-08: no HTML deck had ever reached SDS's slide genealogy, because the archive
# updater accepted only .ppt/.pptx and nothing in the shipping workflow asked. Proves that:
#   1. an unregistered deck fails --check;
#   2. registration makes --check pass;
#   3. EDITING the deck makes --check fail again (registration is bound to the bytes);
#   4. preflight.sh calls the genealogy step only after verification passes, re-checks it, and fails on it;
#   5. against the real archive (when this machine has it): a registered deck passes, an edited copy fails.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; TOOLS="$HERE/../tools"
pass=0; fail=0
ok(){ pass=$((pass+1)); echo "  ok    $1"; }
bad(){ fail=$((fail+1)); echo "  FAIL  $1"; }

T="$(mktemp -d)" || exit 1
case "$T" in /tmp/*|/var/tmp/*) : ;; *) echo "unsafe temp path"; exit 1 ;; esac
trap 'rm -rf "$T"' EXIT
mkdir -p "$T/scripts"
# A stand-in archive: same CLI contract as register_html_deck.py (--check / --html), sha256 ledger.
cat > "$T/scripts/register_html_deck.py" <<'PY'
import hashlib, sys, pathlib
led = pathlib.Path(__file__).with_name("ledger.tsv")
def h(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
rows = dict(l.split("\t") for l in led.read_text().splitlines()) if led.exists() else {}
a = sys.argv[1:]
if a[0] == "--check":
    p = str(pathlib.Path(a[1]).resolve())
    sys.exit(0 if rows.get(p) == h(p) else 1)
if a[0] == "--html":
    p = str(pathlib.Path(a[1]).resolve()); rows[p] = h(p)
    led.write_text("\n".join(f"{k}\t{v}" for k, v in rows.items())); print("registered", p)
PY
export PRESENTATIONS_ARCHIVE_SCRIPTS="$T/scripts"
printf '<html><title>Test &middot; deck</title>A</html>\n' > "$T/deck.html"

bash "$TOOLS/register_genealogy.sh" --check "$T/deck.html" >/dev/null 2>&1 && bad "unregistered deck passed --check" || ok "unregistered deck fails --check"
bash "$TOOLS/register_genealogy.sh" "$T/deck.html" >/dev/null 2>&1
bash "$TOOLS/register_genealogy.sh" --check "$T/deck.html" >/dev/null 2>&1 && ok "registered deck passes --check" || bad "registered deck failed --check"
printf 'edit\n' >> "$T/deck.html"
bash "$TOOLS/register_genealogy.sh" --check "$T/deck.html" >/dev/null 2>&1 && bad "edited deck still passed --check" || ok "edited deck fails --check (bound to bytes)"

PF="$TOOLS/preflight.sh"
python3 - "$PF" <<'PY' && ok "preflight: genealogy runs only inside the verification-passed branch and re-checks" || bad "preflight wiring"
import re, sys
s = open(sys.argv[1]).read()
i_if = s.find('if "${cmd[@]}"; then'); i_reg = s.find('register_genealogy.sh" "$deck"')
i_chk = s.rfind('register_genealogy.sh" --check "$deck" ||'); i_else = s.find("  else\n    fail=1", i_chk)
assert -1 not in (i_if, i_reg, i_chk, i_else) and i_if < i_reg < i_chk < i_else, (i_if, i_reg, i_chk, i_else)
assert "GENEALOGY FAILED" in s and "fail=1" in s[i_chk:i_chk + 200]
PY

unset PRESENTATIONS_ARCHIVE_SCRIPTS
REAL=$(ls /mnt/c/Users/*/Dropbox/Presentations/_PDF_archive/_html_decks.tsv 2>/dev/null | head -1)
if [ -n "$REAL" ]; then
  deck=$(awk -F'\t' 'NR>1 && $1 ~ /yerevan_futures/ {print $1; exit}' "$REAL")
  if [ -n "$deck" ] && [ -f "$deck" ]; then
    bash "$TOOLS/register_genealogy.sh" --check "$deck" >/dev/null 2>&1 && ok "real archive: registered deck passes" || bad "real archive: registered deck failed"
    cp "$deck" "$T/copy.html"
    bash "$TOOLS/register_genealogy.sh" --check "$T/copy.html" >/dev/null 2>&1 && bad "real archive: unregistered copy passed" || ok "real archive: unregistered path fails"
  else
    echo "  skip  real archive has no yerevan_futures row"
  fi
else
  echo "  skip  no Dropbox Presentations archive on this machine"
fi
echo "genealogy gate: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
