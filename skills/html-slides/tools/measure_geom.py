#!/usr/bin/env python3
"""Per-slide, per-step rendered geometry, as percentages of the .ob-pic box.

The viewBox tells you nothing usable on its own: the SVG is letterboxed inside .ob-pic by
preserveAspectRatio, so viewBox y and container y are different coordinate systems. Measure the
RENDERED rects. This is the input for setting each note's --y from its OWN slide's art, instead of
the single hardcoded --y:65% every note in this deck currently shares.
"""
import asyncio, json, pathlib, sys
from playwright.async_api import async_playwright

URL = "http://127.0.0.1:18078/deck.html#1"

JS = r"""(() => {
  const s = document.querySelector('.slide.on');
  if (!s) return null;
  const pic = s.querySelector('.ob-pic');
  if (!pic) return {nopic: true};
  const pb = pic.getBoundingClientRect();
  const H = Math.max(1, pb.height), W = Math.max(1, pb.width);
  const pct = v => +(((v - pb.top) / H) * 100).toFixed(1);

  const vis = el => {
    const c = getComputedStyle(el);
    return !(c.display === 'none' || c.visibility === 'hidden' || parseFloat(c.opacity) === 0);
  };
  // drawn SVG content that is actually visible right now
  let aTop = Infinity, aBot = -Infinity;
  for (const el of pic.querySelectorAll('svg rect, svg text, svg line, svg path, svg circle, svg polygon, img')) {
    if (!vis(el)) continue;
    if (el.tagName === 'rect' && el.getAttribute('fill') === 'none' && !el.getAttribute('stroke')) continue;
    let anc = el, hidden = false;
    while (anc && anc !== pic) { if (!vis(anc)) { hidden = true; break; } anc = anc.parentElement; }
    if (hidden) continue;
    const r = el.getBoundingClientRect();
    if (r.height < 1 || r.width < 1) continue;
    aTop = Math.min(aTop, r.top); aBot = Math.max(aBot, r.bottom);
  }
  const notes = [];
  for (const nEl of pic.querySelectorAll('.ob-note')) {
    if (!vis(nEl)) continue;
    let anc = nEl, hidden = false;
    while (anc && anc !== pic) { if (!vis(anc)) { hidden = true; break; } anc = anc.parentElement; }
    if (hidden) continue;
    const r = nEl.getBoundingClientRect();
    notes.push({top: pct(r.top), bot: pct(r.bottom), h: +((r.height / H) * 100).toFixed(1),
                w: +((r.width / W) * 100).toFixed(1)});
  }
  return {picH: Math.round(H), picW: Math.round(W),
          artTop: aBot > -Infinity ? pct(aTop) : null,
          artBot: aBot > -Infinity ? pct(aBot) : null,
          notes};
})()"""


async def main():
    out = []
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
                print("0 slides - refusing"); return 1
            await pg.evaluate("present()"); await pg.wait_for_timeout(900)
            for i in range(n):
                await pg.evaluate(f"go({i})"); await pg.wait_for_timeout(160)
                nf = await pg.evaluate("document.querySelectorAll('.slide.on [data-frag]').length")
                steps = max(nf, 1)
                sid = await pg.evaluate(f"document.querySelectorAll('.slide')[{i}].dataset.sid")
                t = await pg.evaluate(f"document.querySelectorAll('.slide')[{i}].dataset.t")
                for k in range(1, steps + 1):
                    await pg.evaluate(f"setFrags(cur,{k})"); await pg.wait_for_timeout(520)
                    m = await pg.evaluate(JS)
                    if m:
                        m.update(idx=i + 1, sid=sid, title=t or "", step=k, steps=steps)
                        out.append(m)
            pathlib.Path("/tmp/geom.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
            print(f"measured {len(out)} build states -> /tmp/geom.json")
            return 0
        finally:
            await pg.close(); await ctx.close(); await b.close()


sys.exit(asyncio.run(main()))
