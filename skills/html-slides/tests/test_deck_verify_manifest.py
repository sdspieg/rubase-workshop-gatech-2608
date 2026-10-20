#!/usr/bin/env python3
"""Unit checks for the v2 receipt's stale-QA and complete-state invariants."""
import importlib.util
import hashlib
import json
import pathlib
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("deck_verify", HERE.parent / "tools" / "deck_verify.py")
dv = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dv)


def make(root: pathlib.Path):
    deck = root / "presentation.html"
    deck.write_text("<html>current</html>")
    digest = dv.sha256(deck)
    run = root / "fresh-run"
    run.mkdir()
    states = []
    for width in dv.REQUIRED_WIDTHS:
        for state in (0, 1):
            name = f"w{width}_s01_a_state{state:02d}of01.png"
            png = run / name
            png.write_bytes(f"{width}-{state}".encode())
            states.append({"name":name,"sha256":dv.sha256(png),"width":width,"sid":"a",
                           "state":state,"final_state":1})
    manifest = {"schema":"html-slides-render-manifest/v2","deck_sha256":digest,
                "coverage":"state-0-through-final","widths":dv.REQUIRED_WIDTHS,
                "slides":[{"sid":"a","final_state":1}],"n_states":len(states),"states":states}
    mp = run / "manifest.json"
    mp.write_text(json.dumps(manifest))
    mhash = dv.sha256(mp)
    receipt = {"schema":dv.SCHEMA,"deck_sha256":digest,"checks_all_passed":True,
               "render_manifest":str(mp),"render_manifest_sha256":mhash,"eyes_on":True,
               "eyes_on_manifest_sha256":mhash,"states_acknowledged":[s["name"] for s in states]}
    receipt["checks"] = {name:{"passed":True} for name in dv.REQUIRED_CHECKS}
    return deck, run, receipt


with tempfile.TemporaryDirectory() as td:
    root = pathlib.Path(td)
    deck, run, receipt = make(root)
    assert dv.validate_manifest(receipt, deck, True) == [], "clean v2 evidence must pass"
    legacy = dict(receipt); legacy.pop("schema")
    assert any("legacy" in p for p in dv.validate_manifest(legacy, deck, True))
    incomplete = dict(receipt); incomplete["checks"] = dict(receipt["checks"])
    incomplete["checks"].pop("note_overlap")
    assert any("required check" in p for p in dv.validate_manifest(incomplete, deck, True))
    missing_zero = json.loads((run / "manifest.json").read_text())
    missing_zero["states"] = [s for s in missing_zero["states"] if s["state"] != 0]
    missing_zero["n_states"] = len(missing_zero["states"])
    (run / "manifest.json").write_text(json.dumps(missing_zero))
    receipt["render_manifest_sha256"] = dv.sha256(run / "manifest.json")
    receipt["eyes_on_manifest_sha256"] = receipt["render_manifest_sha256"]
    receipt["states_acknowledged"] = [s["name"] for s in missing_zero["states"]]
    assert any("coverage" in p for p in dv.validate_manifest(receipt, deck, True))

print("PASS: clean v2 plus legacy, missing-check, and missing-state-0 rejection")
