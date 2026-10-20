#!/usr/bin/env bash
# The single shipping preflight. It preserves the caller's project directory and runs the
# hash-bound verifier over every deck.html/presentation.html source named or found there.
set -uo pipefail
TOOLS="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$PWD"
baseline=""
if [ "${1:-}" != "" ] && [ -f "$1" ] && [[ "$1" == *.json ]]; then
  baseline="$(readlink -f "$1")"
  shift
fi

decks=("$@")
if [ "${#decks[@]}" -eq 0 ]; then
  [ -f "$PROJECT_DIR/deck.html" ] && decks+=("$PROJECT_DIR/deck.html")
  [ -f "$PROJECT_DIR/presentation.html" ] && decks+=("$PROJECT_DIR/presentation.html")
fi
if [ "${#decks[@]}" -eq 0 ]; then
  echo "PREFLIGHT FAILED: no deck.html or presentation.html in $PROJECT_DIR"
  exit 2
fi

fail=0
for deck in "${decks[@]}"; do
  deck="$(readlink -f "$deck")"
  echo "== hash-bound visual verification: $deck =="
  cmd=(python3 "$TOOLS/deck_verify.py" --deck "$deck")
  [ -n "$baseline" ] && cmd+=(--baseline "$baseline")
  if "${cmd[@]}"; then
    # GENEALOGY (mandatory, SDS 2026-10-08): a deck that passes verification is entered in the
    # slide genealogy of all of SDS's decks at its current bytes. Registration is idempotent (an
    # unchanged deck is a no-op) and the result is re-checked, so a deck can never be called
    # shippable while missing from, or stale in, the genealogy.
    if [ -n "${HTML_SLIDES_GENEALOGY_SKIP:-}" ]; then
      echo "GENEALOGY SKIPPED by HTML_SLIDES_GENEALOGY_SKIP: ${HTML_SLIDES_GENEALOGY_SKIP}"
      mkdir -p "$HOME/.claude/state"
      printf '%s\t%s\t%s\n' "$(date -Is)" "$deck" "$HTML_SLIDES_GENEALOGY_SKIP" >> "$HOME/.claude/state/html-slides-genealogy-skips.log"
    else
      if ! bash "$TOOLS/register_genealogy.sh" --check "$deck" >/dev/null 2>&1; then
        echo "== registering in the slide genealogy: $deck =="
        bash "$TOOLS/register_genealogy.sh" "$deck" 2>&1 | grep -E "^(registered|already|REFUSE|GENEALOGY|genealogy_ok|rendered_ok)"
      fi
      bash "$TOOLS/register_genealogy.sh" --check "$deck" || { echo "GENEALOGY FAILED: $deck is not registered at its current hash"; fail=1; }
    fi
  else
    fail=1
  fi
  echo
done

[ "$fail" -eq 0 ] && echo "PREFLIGHT OK — every exact deck is shippable" \
                    || echo "PREFLIGHT FAILED OR PENDING EYES-ON REVIEW"
exit "$fail"
