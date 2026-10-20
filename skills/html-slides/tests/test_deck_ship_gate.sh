#!/usr/bin/env bash
# Exact regression for 2026-09-23: arbitrary relative scp escaped the old hard-coded gate, while a
# copied qa/ directory made a new deck look visually checked. Clean v2 receipts must still pass.
set -uo pipefail
GATE="${1:-$HOME/.claude/hooks/deck-ship-gate.sh}"
[ -x "$GATE" ] || { echo "FAIL: not executable: $GATE"; exit 1; }

TESTROOT="$(mktemp -d)" || exit 1
case "$TESTROOT" in /tmp/*|/var/tmp/*) : ;; *) echo "unsafe temp path"; exit 1 ;; esac
trap 'rm -rf "$TESTROOT"' EXIT
mkdir -p "$TESTROOT/project/slides/qa" "$TESTROOT/receipts/receipts"
printf '<html>deck A</html>\n' > "$TESTROOT/project/slides/deck.html"
printf '<html>presentation B</html>\n' > "$TESTROOT/project/slides/presentation.html"
printf 'old screenshot from another deck\n' > "$TESTROOT/project/slides/qa/old-success.png"
export DECK_VERIFY_DIR="$TESTROOT/receipts"
pass=0; fail=0

payload() { # payload <command|cmd> <command string>
  FIELD="$1" COMMAND_TEXT="$2" WORKDIR="$TESTROOT/project" python3 - <<'PY'
import json, os
print(json.dumps({"tool_input": {os.environ["FIELD"]: os.environ["COMMAND_TEXT"],
                                 "workdir": os.environ["WORKDIR"]}}))
PY
}

run() { # run BLOCK|ALLOW description field command
  local want="$1" desc="$2" field="$3" command="$4" rc got
  payload "$field" "$command" | "$GATE" >/dev/null 2>&1
  rc=$?; [ "$rc" = 2 ] && got=BLOCK || got=ALLOW
  if [ "$got" = "$want" ]; then
    pass=$((pass+1)); printf '  ok    %-5s %s\n' "$want" "$desc"
  else
    fail=$((fail+1)); printf '  FAIL  want=%s got=%s  %s\n' "$want" "$got" "$desc"
  fi
}

make_receipt() { # make_receipt <deck path>
  DECK_PATH="$1" RECEIPT_ROOT="$DECK_VERIFY_DIR" python3 - <<'PY'
import hashlib, json, os, pathlib
deck = pathlib.Path(os.environ["DECK_PATH"]).resolve()
root = pathlib.Path(os.environ["RECEIPT_ROOT"])
digest = hashlib.sha256(deck.read_bytes()).hexdigest()
run = root / "runs" / (deck.stem + "-" + digest[:10] + "-fresh")
run.mkdir(parents=True, exist_ok=True)
states = []
for width in [1280, 1366, 1440, 1600]:
    name = f"w{width}_s01_only_state00of00.png"
    png = run / name
    png.write_bytes(f"fresh-{digest}-{width}".encode())
    states.append({"name": name, "sha256": hashlib.sha256(png.read_bytes()).hexdigest(),
                   "bytes": png.stat().st_size, "width": width, "height": round(width*9/16),
                   "slide_index": 1, "sid": "only", "state": 0, "final_state": 0})
manifest = {"schema": "html-slides-render-manifest/v2", "deck_sha256": digest,
            "widths": [1280,1366,1440,1600], "slides": [{"slide_index":1,"sid":"only","final_state":0}],
            "coverage": "state-0-through-final", "n_states": len(states), "states": states}
mp = run / "manifest.json"
mp.write_text(json.dumps(manifest))
mhash = hashlib.sha256(mp.read_bytes()).hexdigest()
receipt = {"schema":"html-slides-deck-verification/v2", "deck_sha256":digest,
           "checks_all_passed":True, "render_manifest":str(mp), "render_manifest_sha256":mhash,
           "eyes_on":True, "eyes_on_manifest_sha256":mhash,
           "states_acknowledged":[s["name"] for s in states]}
receipt["checks"] = {name:{"passed":True} for name in
    ["regressions","inventory","sre_audit","render_audit","note_overlap","box_collisions",
     "svg_text_html","structure","fresh_state_render"]}
(root / "receipts").mkdir(parents=True, exist_ok=True)
(root / "receipts" / (digest[:20] + ".json")).write_text(json.dumps(receipt))
PY
}

# The exact escaped path: scp + relative arbitrary project + presentation.html.
run BLOCK "relative scp presentation via command" command \
  "scp slides/presentation.html root@example:/var/www/"
run BLOCK "relative scp deck via cross-CLI cmd" cmd \
  "timeout 30 scp slides/deck.html root@example:/var/www/"
run BLOCK "copied stale qa directory proves nothing" command \
  "scp -r slides root@example:/var/www/"
run BLOCK "local cp mirror is also shipment" command \
  "cp slides/deck.html /tmp/deck.html"
run ALLOW "unrelated scp remains unrelated" command \
  "scp README.md root@example:/var/www/"
run ALLOW "mentioning a deck in another segment does not arm" command \
  "cp README.md /tmp/x; python3 inspect.py slides/deck.html"

make_receipt "$TESTROOT/project/slides/presentation.html"
run ALLOW "clean exact presentation receipt permits scp" command \
  "scp slides/presentation.html root@example:/var/www/"
run BLOCK "directory ship still blocks unverified deck sibling" command \
  "scp -r slides root@example:/var/www/"

make_receipt "$TESTROOT/project/slides/deck.html"
run ALLOW "both clean exact receipts permit directory scp" command \
  "scp -r slides root@example:/var/www/"
run ALLOW "quoted arbitrary absolute path permits scp" cmd \
  "scp '$TESTROOT/project/slides/presentation.html' root@example:/var/www/"

# PNG hashes remain live evidence, not historical claims.
presentation_digest="$(sha256sum "$TESTROOT/project/slides/presentation.html" | cut -d' ' -f1)"
printf 'tampered after acknowledgement\n' >> "$TESTROOT/receipts/runs/presentation-${presentation_digest:0:10}-fresh/w1280_s01_only_state00of00.png"
run BLOCK "tampered manifested PNG invalidates shipment" command \
  "scp slides/presentation.html root@example:/var/www/"

# Editing the deck invalidates the byte-bound receipt even when qa/ still looks populated.
printf '<!-- edited -->\n' >> "$TESTROOT/project/slides/deck.html"
run BLOCK "HTML edit invalidates receipt despite stale qa" command \
  "scp slides/deck.html root@example:/var/www/"

# Git shipment is bound to INDEX/HEAD bytes, not a convenient working-copy substitute.
mkdir -p "$TESTROOT/project/repo"
printf '<html>git head</html>\n' > "$TESTROOT/project/repo/deck.html"
git -C "$TESTROOT/project/repo" init -q
git -C "$TESTROOT/project/repo" config user.name test
git -C "$TESTROOT/project/repo" config user.email test@example.invalid
git -C "$TESTROOT/project/repo" add deck.html
git -C "$TESTROOT/project/repo" commit -qm initial
run BLOCK "unverified exact HEAD blocks git push" command \
  "cd repo && git push origin main"
make_receipt "$TESTROOT/project/repo/deck.html"
run ALLOW "verified exact HEAD permits git push" command \
  "cd repo && git push origin main"
printf '<html>new staged bytes</html>\n' > "$TESTROOT/project/repo/deck.html"
git -C "$TESTROOT/project/repo" add deck.html
run BLOCK "new staged INDEX bytes block git commit" command \
  "cd repo && git commit -m changed"

echo
echo "  $pass passed, $fail failed"
[ "$fail" = 0 ]
