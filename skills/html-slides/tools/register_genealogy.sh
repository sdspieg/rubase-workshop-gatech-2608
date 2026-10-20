#!/usr/bin/env bash
# Register a shipped deck in SDS's slide genealogy (Dropbox Presentations archive), or check that it is.
#
#   tools/register_genealogy.sh <deck.html> [--title "..."] [--date YYYY-MM-DD]   # register (idempotent)
#   tools/register_genealogy.sh --check <deck.html>                              # exit 0 iff current
#
# WHY (SDS 2026-10-08): "make sure they're added to our genealogy of all of my slidedecks!" The
# archive updater only ever accepted .ppt/.pptx, so no HTML deck had reached the genealogy: the GaTech
# workshop, the Caucasus and Central Asia trip decks and the PASP method deck were all missing, and
# nothing reported it. A deck is registered only at its CURRENT bytes (sha256 ledger), so an edited
# deck counts as unregistered until it is registered again.
#
# The archive lives on the machine that holds SDS's Dropbox. Override with PRESENTATIONS_ARCHIVE_SCRIPTS.
set -uo pipefail

find_script() {
  if [ -n "${PRESENTATIONS_ARCHIVE_SCRIPTS:-}" ] && [ -f "$PRESENTATIONS_ARCHIVE_SCRIPTS/register_html_deck.py" ]; then
    echo "$PRESENTATIONS_ARCHIVE_SCRIPTS/register_html_deck.py"; return 0
  fi
  local c
  for c in /mnt/c/Users/*/Dropbox/Presentations/_PDF_archive/scripts/register_html_deck.py \
           "$HOME"/Dropbox/Presentations/_PDF_archive/scripts/register_html_deck.py; do
    [ -f "$c" ] && { echo "$c"; return 0; }
  done
  return 1
}

SCRIPT="$(find_script)" || {
  echo "GENEALOGY UNAVAILABLE: register_html_deck.py not found (no Dropbox Presentations archive on this"
  echo "machine). Set PRESENTATIONS_ARCHIVE_SCRIPTS, or register the deck from the machine that has it."
  exit 3
}

if [ "${1:-}" = "--check" ]; then
  [ -n "${2:-}" ] || { echo "usage: $0 --check <deck.html>"; exit 2; }
  exec python3 "$SCRIPT" --check "$(readlink -f "$2")"
fi

deck="${1:-}"; [ -n "$deck" ] && [ -f "$deck" ] || { echo "usage: $0 <deck.html> [--title T] [--date D]"; exit 2; }
deck="$(readlink -f "$deck")"; shift
args=("$@")
if ! printf '%s\n' "${args[@]:-}" | grep -qx -- '--title'; then
  title="$(python3 - "$deck" <<'PY'
import html, re, sys
s = open(sys.argv[1], encoding="utf-8", errors="ignore").read(200000)
m = re.search(r"<title>(.*?)</title>", s, re.S | re.I)
t = html.unescape(m.group(1)).strip() if m else ""
print(re.sub(r"\s+", " ", t.replace("·", "-")) or "")
PY
)"
  [ -n "$title" ] && args+=(--title "$title")
fi
exec python3 "$SCRIPT" --html "$deck" "${args[@]}"
