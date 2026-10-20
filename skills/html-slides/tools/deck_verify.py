#!/usr/bin/env python3
"""Prepare and validate the receipt required before an HTML deck can ship.

The receipt is bound to four things simultaneously: the exact HTML bytes, every required check,
a fresh renderer-created PNG manifest covering state 0 through final at four viewports, and a
per-PNG eyes-on acknowledgement. Existing QA folders are never adopted.
"""
import argparse
import hashlib
import json
import os
import pathlib
import secrets
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
RECEIPT_DIR = pathlib.Path(os.environ.get(
    "DECK_VERIFY_DIR", os.path.expanduser("~/.claude/state/deck-verify")))
REQUIRED_WIDTHS = [1280, 1366, 1440, 1600]
SCHEMA = "html-slides-deck-verification/v2"
REQUIRED_CHECKS = {"regressions", "inventory", "sre_audit", "render_audit", "note_overlap",
                   "box_collisions", "svg_text_html", "structure", "fresh_state_render"}


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def receipt_path(deck: pathlib.Path) -> pathlib.Path:
    key = hashlib.sha256(str(deck.resolve()).encode()).hexdigest()[:20]
    return RECEIPT_DIR / "receipts" / f"{key}.json"


def run_check(name: str, cmd: list[str]) -> tuple[bool, str]:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    combined = ((result.stdout or "") + "\n" + (result.stderr or "")).strip()
    tail = "\n".join(combined.splitlines()[-18:])
    print(f"\n=== {name}: {'PASS' if result.returncode == 0 else 'FAIL'} ===")
    if tail:
        print(tail)
    return result.returncode == 0, tail


def validate_manifest(rec: dict, deck: pathlib.Path, require_eyes: bool) -> list[str]:
    problems = []
    digest = sha256(deck)
    if rec.get("schema") != SCHEMA:
        problems.append("legacy/missing receipt schema")
    if rec.get("deck_sha256") != digest:
        problems.append("deck bytes changed after verification")
    if not rec.get("checks_all_passed"):
        problems.append("one or more required checks did not pass")
    checks = rec.get("checks") or {}
    missing_checks = REQUIRED_CHECKS - set(checks)
    failed_checks = [name for name in REQUIRED_CHECKS if not (checks.get(name) or {}).get("passed")]
    if missing_checks or failed_checks:
        problems.append("required check evidence missing/failed: " +
                        ", ".join(sorted(missing_checks | set(failed_checks))))
    manifest_path = pathlib.Path(rec.get("render_manifest", ""))
    if not manifest_path.is_file():
        return problems + ["render manifest is missing"]
    if rec.get("render_manifest_sha256") != sha256(manifest_path):
        return problems + ["render manifest bytes changed"]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return problems + [f"render manifest is unreadable: {exc}"]
    if manifest.get("schema") != "html-slides-render-manifest/v2":
        problems.append("render manifest has a legacy/missing schema")
    if manifest.get("deck_sha256") != digest:
        problems.append("render manifest belongs to different deck bytes")
    if manifest.get("coverage") != "state-0-through-final":
        problems.append("render manifest does not certify state 0 through final")
    if manifest.get("widths") != REQUIRED_WIDTHS:
        problems.append(f"render widths are {manifest.get('widths')}, expected {REQUIRED_WIDTHS}")
    states = manifest.get("states") or []
    names = [s.get("name") for s in states]
    if not states or len(names) != len(set(names)) or None in names:
        problems.append("render state list is empty, duplicated, or unnamed")
    expected = []
    for width in REQUIRED_WIDTHS:
        for slide in manifest.get("slides") or []:
            expected.extend((width, slide.get("sid"), state)
                            for state in range(0, int(slide.get("final_state", -1)) + 1))
    got = sorted((s.get("width"), s.get("sid"), s.get("state")) for s in states)
    if sorted(expected) != got or manifest.get("n_states") != len(states):
        problems.append("render state coverage is incomplete")
    run_dir = manifest_path.parent
    for state in states:
        png = run_dir / state["name"]
        if not png.is_file():
            problems.append(f"missing PNG: {state['name']}")
            continue
        if sha256(png) != state.get("sha256"):
            problems.append(f"changed PNG: {state['name']}")
    if require_eyes:
        acknowledged = rec.get("states_acknowledged") or []
        if not rec.get("eyes_on") or sorted(acknowledged) != sorted(names):
            problems.append("not every manifested PNG has a per-state eyes-on acknowledgement")
        if rec.get("eyes_on_manifest_sha256") != rec.get("render_manifest_sha256"):
            problems.append("eyes-on acknowledgement belongs to a different PNG manifest")
    return problems


def read_receipt(deck: pathlib.Path):
    path = receipt_path(deck)
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def acknowledge(deck: pathlib.Path, eyes_file: pathlib.Path) -> int:
    rec = read_receipt(deck)
    if not rec:
        print("FAIL: no current receipt; prepare verification first")
        return 1
    problems = validate_manifest(rec, deck, require_eyes=False)
    if problems:
        print("FAIL: verification evidence is no longer valid: " + "; ".join(problems))
        return 1
    manifest = json.loads(pathlib.Path(rec["render_manifest"]).read_text(encoding="utf-8"))
    wanted = [state["name"] for state in manifest["states"]]
    lines = [line.strip() for line in eyes_file.read_text(encoding="utf-8").splitlines()
             if line.strip() and not line.lstrip().startswith("#")]
    supplied = [line.split("\t", 1)[0].strip() for line in lines]
    if len(supplied) != len(set(supplied)):
        print("FAIL: duplicate eyes-on acknowledgement lines")
        return 1
    missing = sorted(set(wanted) - set(supplied))
    extra = sorted(set(supplied) - set(wanted))
    if missing or extra:
        print(f"FAIL: eyes-on list misses {len(missing)} state(s) and adds {len(extra)} unknown state(s)")
        for name in missing[:12]:
            print("  missing:", name)
        for name in extra[:12]:
            print("  unknown:", name)
        return 1
    rec.update({
        "eyes_on": True,
        "eyes_on_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "eyes_on_manifest_sha256": rec["render_manifest_sha256"],
        "states_acknowledged": wanted,
        "states_read": len(wanted),
    })
    receipt_path(deck).write_text(json.dumps(rec, indent=2), encoding="utf-8")
    problems = validate_manifest(rec, deck, require_eyes=True)
    if problems:
        print("FAIL after acknowledgement: " + "; ".join(problems))
        return 1
    print(f"PASS: all {len(wanted)} exact, manifested PNGs acknowledged; these deck bytes may ship")
    return 0


def prepare(deck: pathlib.Path, shots_parent: pathlib.Path, baseline: str | None) -> int:
    digest = sha256(deck)
    tag = f"{receipt_path(deck).stem}-{digest[:12]}-{int(time.time())}-{secrets.token_hex(3)}"
    run_dir = shots_parent / tag
    checks = [
        ("regressions", [sys.executable, str(HERE / "check_regressions.py"), "--deck", str(deck)]),
        ("inventory", [sys.executable, str(HERE / "slide_inventory.py"), "--deck", str(deck),
                       "--out", str(run_dir.parent / f"{tag}-inventory.json")]),
        ("sre_audit", [sys.executable, str(HERE / "sre_audit.py"), "--deck", str(deck), "--present"]),
        ("render_audit", [sys.executable, str(HERE / "render_audit.py"), "--deck", str(deck)]),
        ("note_overlap", [sys.executable, str(HERE / "note_overlap_check.py"),
                          "--deck", str(deck), "--present"]),
        ("box_collisions", [sys.executable, str(HERE / "box_collisions.py"), "--deck", str(deck)]),
        ("svg_text_html", [sys.executable, str(HERE / "svg_text_html_check.py"), str(deck)]),
        ("structure", [sys.executable, str(HERE / "structure_check.py"), str(deck)]),
    ]
    if baseline:
        checks.append(("visual_baseline", [sys.executable, str(HERE / "slide_inventory.py"),
                                            "--deck", str(deck), "--compare", baseline]))
    results, all_ok = {}, True
    for name, cmd in checks:
        ok, tail = run_check(name, cmd)
        results[name] = {"passed": ok, "tail": tail}
        all_ok &= ok
    if not all_ok:
        print("\nFAIL: checks failed; no render receipt was issued")
        return 1

    ok, tail = run_check("fresh_state_render", [
        sys.executable, str(HERE / "render_steps.py"), "--deck", str(deck),
        "--out", str(run_dir), "--widths", ",".join(map(str, REQUIRED_WIDTHS))])
    results["fresh_state_render"] = {"passed": ok, "tail": tail}
    if not ok:
        print("FAIL: fresh rendering failed; no receipt was issued")
        return 1
    manifest_path = run_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    required_file = run_dir / "eyes_on_required.txt"
    required_file.write_text("\n".join(state["name"] for state in manifest["states"]) + "\n",
                             encoding="utf-8")
    rec = {
        "schema": SCHEMA,
        "deck": str(deck),
        "deck_sha256": digest,
        "verified_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "checks": results,
        "checks_all_passed": True,
        "render_manifest": str(manifest_path),
        "render_manifest_sha256": sha256(manifest_path),
        "coverage": manifest["coverage"],
        "n_states": manifest["n_states"],
        "eyes_on": False,
        "states_acknowledged": [],
    }
    rp = receipt_path(deck)
    rp.parent.mkdir(parents=True, exist_ok=True)
    rp.write_text(json.dumps(rec, indent=2), encoding="utf-8")
    print(f"\nCHECKS AND FRESH RENDER PASS: {manifest['n_states']} state PNGs")
    print("NOT SHIPPABLE: READ every PNG, then use the generated acknowledgement list:")
    print(f"  {required_file}")
    print(f"  python3 {pathlib.Path(__file__).resolve()} --deck {deck} --eyes-on-file <reviewed-copy>")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--deck", required=True)
    ap.add_argument("--shots", help="parent for a NEW private render run; existing PNGs are ignored")
    ap.add_argument("--baseline")
    ap.add_argument("--eyes-on-file")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    deck = pathlib.Path(args.deck).resolve()
    if not deck.is_file():
        print(f"FAIL: no such deck: {deck}")
        return 2
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    if args.eyes_on_file:
        return acknowledge(deck, pathlib.Path(args.eyes_on_file).resolve())
    rec = read_receipt(deck)
    if rec and not args.force:
        problems = validate_manifest(rec, deck, require_eyes=True)
        if not problems:
            print(f"PASS: current deck hash, checks, PNG hashes, coverage, and {rec['states_read']} eyes-on states")
            return 0
        pending = validate_manifest(rec, deck, require_eyes=False)
        if not pending and not rec.get("eyes_on"):
            print(f"PENDING: {rec['n_states']} fresh states exist, but none may ship until all are read")
            print(pathlib.Path(rec["render_manifest"]).parent / "eyes_on_required.txt")
            return 1
        if args.status:
            print("FAIL: " + "; ".join(problems))
            return 1
    elif args.status:
        print("FAIL: no verification receipt for these deck bytes")
        return 1
    shots_parent = pathlib.Path(args.shots).resolve() if args.shots else RECEIPT_DIR / "runs"
    shots_parent.mkdir(parents=True, exist_ok=True)
    return prepare(deck, shots_parent, args.baseline)


if __name__ == "__main__":
    sys.exit(main())
