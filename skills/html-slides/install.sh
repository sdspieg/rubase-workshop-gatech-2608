#!/usr/bin/env bash
# Deploy this skill to every CLI on THIS machine, and to the Drive master when reachable.
#
# Claude Code, Codex and Gemini each read skills from their own directory, so a skill that
# lives in only one of them is a skill two of the three CLIs will never see. Drive is the
# cross-machine master: sync-llm-instructions.sh redeploys from there on every login, which
# is what carries this to the desktop and to any future machine.
set -eu
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME="$(basename "$HERE")"

for d in "$HOME/.claude/skills" "$HOME/.codex/skills" "$HOME/.gemini/skills"; do
  [ -d "$d" ] || { echo "skip (no such dir): $d"; continue; }
  mkdir -p "$d/$NAME"
  cp -r "$HERE"/. "$d/$NAME"/
  echo "deployed -> $d/$NAME"
done

MASTER="/mnt/g/My Drive/claude-skills/$NAME"
if [ -d "/mnt/g/My Drive/claude-skills" ]; then
  mkdir -p "$MASTER"
  cp -r "$HERE"/. "$MASTER"/
  echo "master   -> $MASTER   (sync-llm-instructions.sh will carry it to every machine)"
else
  echo
  echo "Google Drive is NOT mounted here, so the cross-machine master was NOT updated."
  echo "On a machine where /mnt/g/My Drive exists, run this script again, then:"
  echo "    sync-llm-instructions.sh"
fi
