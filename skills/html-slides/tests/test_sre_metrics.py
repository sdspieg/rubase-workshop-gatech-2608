#!/usr/bin/env python3
"""Regression test for sre_audit's overflow and hole metrics.

WHY THIS EXISTS. On 2026-09-17 both metrics were wrong in BOTH directions inside one session:

  - `hole` reported 0.392 on a slide whose render had nothing in that band at all, because
    getBoundingClientRect() returns a layout box even when an ancestor's overflow:hidden clips the
    element away. A pixel sample of the band found zero non-background pixels.
  - `overflow` under-reported at first (its `inside` test never checked the text's RIGHT edge), then
    a rewrite OVER-reported: it let any box that merely started left of a text be its host, so a row
    of sibling cards qualified for each other's labels and a visibly clean slide scored nine.

Three successive "fixes" each traded one defect for another because nothing pinned the correct
answer. The fixtures do. The clean cases matter more than the bad ones: a gate that flags nothing is
worse than one that cries wolf, because it reports a pass.

Run:  python3 test_sre_metrics.py
"""
import asyncio, http.server, json, os, pathlib, subprocess, sys, tempfile, threading

HERE = pathlib.Path(__file__).resolve().parent
FIXTURE = HERE / "fixtures" / "overflow_hole_cases.html"
AUDIT = HERE.parent / "tools" / "sre_audit.py"

# sid -> {metric: expectation}. None means "do not assert" - an expectation you cannot justify is
# worse than none, because it gets "fixed" by loosening the metric.
# 🟥 The first version of this table expected BAD-superimposed to raise OVERFLOW. It does not, and
# should not: superimposed text escapes no container. That wrong expectation is what exposed the gap
# and produced the `collide` metric, so it is recorded here rather than quietly corrected.
EXPECT = {
    "BAD-overflow-clipped": {"overflow": True,  "collide": None,  "hole": False},
    "BAD-superimposed":     {"overflow": False, "collide": True,  "hole": None},
    "CLEAN-sibling-cards":  {"overflow": False, "collide": False, "hole": False},
    "CLEAN-clipped-below":  {"overflow": False, "collide": False, "hole": False},
    # a big number under its own label, and two tight adjacent lines - readable, not collided
    "CLEAN-stacked-number": {"overflow": False, "collide": False, "hole": None},
    # a label painted over by its own bar - SVG paint order, invisible to a text-vs-text check
    "BAD-occluded":         {"occluded": True,  "collide": False, "hole": None},
    # 2026-10-10: art from a later step drawn across an earlier step's art. A DECLARED overlay
    # (data-crossstep-ok with a real reason) is exempt; an empty marker exempts nothing.
    "BAD-crossstep":            {"crossstep": True,  "hole": None},
    "CLEAN-crossstep-declared": {"crossstep": False, "hole": None},
    "BAD-crossstep-bare":       {"crossstep": True,  "hole": None},
}


def serve(directory, port):
    """Threading server: the single-threaded one deadlocks on Chrome's keep-alive connections."""
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=directory, **k)
        def log_message(self, *a):
            pass
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def main():
    if not FIXTURE.exists():
        print(f"FAIL: fixture missing: {FIXTURE}"); return 1
    if not AUDIT.exists():
        print(f"FAIL: audit missing: {AUDIT}"); return 1

    port = 18711
    srv = serve(str(FIXTURE.parent), port)
    try:
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "m.json")
            # The fixture is a plain page, not the deck app, so drive the audit's --deck path at it.
            r = subprocess.run([sys.executable, str(AUDIT), "--deck", str(FIXTURE),
                                "--out", out, "--max-hole", "0.17"],
                               capture_output=True, text=True, timeout=600)
            if not os.path.exists(out):
                print("FAIL: audit produced no measurements")
                print(r.stdout[-2500:]); print(r.stderr[-1500:]); return 1
            rows = json.load(open(out))
    finally:
        srv.shutdown()

    by_sid = {}
    for row in rows:
        by_sid.setdefault(row.get("sid"), []).append(row)

    failures = []
    print(f"  {len(rows)} measurement rows over {len(by_sid)} fixture slides\n")
    for sid, want in EXPECT.items():
        got = by_sid.get(sid)
        if not got:
            failures.append(f"{sid}: never measured"); continue
        vals = {"overflow": max(r.get("overflow", 0) for r in got),
                "collide":  max(r.get("collide", 0) for r in got),
                "occluded": max(r.get("occluded", 0) for r in got),
                "crossstep": max(r.get("crossstep", 0) for r in got),
                "hole":     max(r.get("hole", 0) for r in got)}
        bits, ok_all = [], True
        for metric, expected in want.items():
            v = vals[metric]
            hit = (v > 0.17) if metric == "hole" else (v > 0)
            shown = f"{v:.3f}" if metric == "hole" else str(v)
            if expected is None:
                bits.append(f"{metric}={shown}(-)"); continue
            ok = hit == expected
            ok_all &= ok
            bits.append(f"{metric}={shown}({'want+' if expected else 'want0'}{'' if ok else ' MISS'})")
            if not ok:
                failures.append(f"{sid}: {metric}={shown}, wanted {'nonzero' if expected else 'zero'}")
        print(f"  {'ok  ' if ok_all else 'FAIL'} {sid:24} " + "  ".join(bits))

    print()
    if failures:
        for f in failures:
            print("  FAIL:", f)
        return 1
    print(f"  PASS - {len(EXPECT)}/{len(EXPECT)} fixture cases")
    return 0


sys.exit(main())
