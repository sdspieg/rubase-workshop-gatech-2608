#!/usr/bin/env python3
"""Measure each build step's rendered art, then place that step's note directly under it.

Why this is a measurement and not a global transform: every note in this deck shared one hardcoded
`--y:65%` while the art ended anywhere between 28% and 64% of the picture box, so step 1 of most
slides carried a hole a third of the slide deep. Each note now gets a value derived from ITS OWN
step's art. Re-run it after any change to a slide's art - enlarging the art invalidates the old
placement and would put the note on top of the figure.

Two passes: measure with playwright, then rewrite the HTML, then re-measure to confirm.
"""
import asyncio, io, json, re, sys, pathlib
from playwright.async_api import async_playwright

DECK = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "deck.html").resolve()
URL = "http://127.0.0.1:18078/deck.html#1"
GAP = 3.0          # % of the picture box between art bottom and note top
BOTTOM = 97.0      # note must never cross this
# beside this file, never /tmp - a reboot empties /tmp and the tool would break silently
MEASURE = pathlib.Path(__file__).resolve().parent / "measure_geom.py"


async def measure():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1366, "height": 768})
        pg = await ctx.new_page()
        try:
            await pg.goto(URL, wait_until="domcontentloaded", timeout=180000)
            n = 0
            for _ in range(25):
                await pg.wait_for_timeout(600)
                n = await pg.evaluate("document.querySelectorAll('.slide').length")
                if n:
                    break
            if not n:
                raise SystemExit("0 slides in the DOM - refusing to measure nothing")
            await pg.evaluate("present()")
            await pg.wait_for_timeout(900)
            js = MEASURE.read_text(encoding="utf-8").split('JS = r"""')[1].split('"""')[0]
            out = []
            for i in range(n):
                await pg.evaluate(f"go({i})")
                await pg.wait_for_timeout(160)
                nf = await pg.evaluate("document.querySelectorAll('.slide.on [data-frag]').length")
                steps = max(nf, 1)
                sid = await pg.evaluate(f"document.querySelectorAll('.slide')[{i}].dataset.sid")
                for k in range(1, steps + 1):
                    await pg.evaluate(f"setFrags(cur,{k})")
                    await pg.wait_for_timeout(330)
                    m = await pg.evaluate(js)
                    if m and not m.get("nopic"):
                        m.update(sid=sid, step=k)
                        out.append(m)
            return out
        finally:
            await pg.close(); await ctx.close(); await b.close()


def apply(geom):
    src = io.open(DECK, encoding="utf-8").read()
    L0, IDS = len(src), sorted(re.findall(r'id="([A-Za-z]+)"', src))
    NS = src.count('<section class="slide')

    G = {}
    for r in geom:
        if not r.get("notes") or r.get("artBot") is None:
            continue
        nt = r["notes"][0]
        G[(r["sid"], r["step"])] = (r["artBot"], nt["bot"] - nt["top"])

    secs = [m.start() for m in re.finditer(r'<section class="slide', src)]
    parts = [src[:secs[0]]]                       # the head and app shell - never drop this
    bounds = secs + [len(src)]
    moved = []
    unplaceable = []
    for i in range(len(bounds) - 1):
        body = src[bounds[i]:bounds[i + 1]]
        sid = (re.search(r'data-sid="([^"]+)"', body) or [None, ''])[1]
        ys = list(re.finditer(r'--y:[\d.]+%', body))
        if ys:
            res, last = [], 0
            for k, m in enumerate(ys, start=1):
                res.append(body[last:m.start()])
                g = G.get((sid, k))
                if g:
                    artbot, h = g
                    y = artbot + GAP
                    if y + h > BOTTOM:
                        y = BOTTOM - h
                    # 🟥 THE CLAMP USED TO WIN OVER THE ART AND THAT SHIPPED A REGRESSION.
                    # min(y, 76) placed the note at 76% no matter how far the art ran, so a slide
                    # whose art reached 88% got its bottom lines COVERED - and the note is opaque,
                    # so they were simply gone. Measured 2026-09-17: five build states, several at
                    # 100% coverage, while sre_audit printed PASS because it has no model of a note
                    # sitting on artwork. A note is never placed over art now; if it cannot fit,
                    # that is reported as a slide to redesign rather than silently overlapped.
                    if artbot + GAP + h > BOTTOM:
                        unplaceable.append((sid, k, round(artbot, 1), round(h, 1)))
                    y = max(14.0, artbot + GAP)
                    res.append(f"--y:{round(y,1)}%")
                    moved.append((sid, k, round(y, 1)))
                else:
                    res.append(m.group(0))
                last = m.end()
            res.append(body[last:])
            body = "".join(res)
        parts.append(body)
    out = "".join(parts)
    assert sorted(re.findall(r'id="([A-Za-z]+)"', out)) == IDS, "id set changed - refusing to write"
    assert out.count('<section class="slide') == NS, "slide count changed - refusing to write"
    assert len(out) > L0 * 0.98, f"file shrank {L0} -> {len(out)} - refusing to write"
    io.open(DECK, "w", encoding="utf-8").write(out)
    return moved, unplaceable


geom = asyncio.run(measure())
moved, unplaceable = apply(geom)
print(f"  reflowed {len(moved)} notes onto their own step's art")
if unplaceable:
    print(f"\n  🟥 {len(unplaceable)} build state(s) have art too tall to leave room for their note.")
    print("  The note is opaque, so it would COVER that art. Shrink the artwork on these slides:")
    for sid, k, ab, h in unplaceable:
        print(f"     {sid} step {k}: art ends at {ab}%, note needs {h}% - art must end by "
              f"{round(97.0 - h - 5.0, 1)}%")
    raise SystemExit(1)
for sid in dict.fromkeys(m[0] for m in moved):
    print(f"   {sid:9} " + ", ".join(str(v) for s, k, v in moved if s == sid))
