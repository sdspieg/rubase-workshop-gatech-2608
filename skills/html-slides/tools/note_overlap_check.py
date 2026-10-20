#!/usr/bin/env python3
"""Refuse an .ob-note box that lands ON TOP of the slide's own artwork.

WHY THIS EXISTS. On 2026-09-17 a deck was shipped with heavy note-over-art overlap while
sre_audit.py printed "PASS - all 66 build states". That audit models space use, text spilling a
rect, SVG-text-on-SVG-text collision and a rect painted over text. It has NO model of the HTML
.ob-note box colliding with the SVG art beneath it - and the note is precisely what reflow_notes.py
moves on every edit. So the thing most disturbed by editing was the one thing nothing measured, and
the report said PASS with full confidence.

The note is opaque (background rgba(10,24,47,.94)), so whatever it covers is GONE from the slide.
That makes this a hard defect, not a cosmetic one, on every build step.

Run:  python3 note_overlap_check.py --deck <deck.html> [--present] [--max-cover 0.02]
Exit 1 if any build state has a note covering art.
"""
import argparse, asyncio, json, sys
from playwright.async_api import async_playwright

MEASURE = r"""(() => {
  const s = document.querySelector('.slide.on');
  if (!s) return null;
  const pic = s.querySelector('.ob-pic');
  if (!pic) return {n: 0, worst: 0, hits: []};
  const selfVis = el => {
    const c = getComputedStyle(el);
    if (c.display==='none' || c.visibility==='hidden' || parseFloat(c.opacity)===0) return false;
    if (el.tagName==='rect' && el.getAttribute('fill')==='none' && !el.getAttribute('stroke')) return false;
    return true;
  };
  const vis = el => {
    if (!selfVis(el)) return false;
    for (let a = el.parentElement; a && a !== s; a = a.parentElement) {
      const c = getComputedStyle(a);
      if (c.display==='none' || c.visibility==='hidden' || parseFloat(c.opacity)===0) return false;
    }
    return true;
  };
  // clip to the picture box, which is overflow:hidden on most slides
  const pb = pic.getBoundingClientRect();
  const clip = r => ({left: Math.max(r.left, pb.left), right: Math.min(r.right, pb.right),
                      top: Math.max(r.top, pb.top), bottom: Math.min(r.bottom, pb.bottom)});
  const notes = [...pic.querySelectorAll('.ob-note')].filter(vis).map(n => ({el: n, b: n.getBoundingClientRect()}));
  if (!notes.length) return {n: 0, worst: 0, hits: []};

  const hits = [];
  let worst = 0;
  for (const el of pic.querySelectorAll('svg text, svg rect, svg path, svg line, svg circle, svg polygon, img')) {
    if (!vis(el)) continue;
    const r = clip(el.getBoundingClientRect());
    const w = r.right - r.left, h = r.bottom - r.top;
    if (w < 2 || h < 2) continue;
    for (const nt of notes) {
      const ow = Math.min(r.right, nt.b.right) - Math.max(r.left, nt.b.left);
      const oh = Math.min(r.bottom, nt.b.bottom) - Math.max(r.top, nt.b.top);
      if (ow <= 1 || oh <= 1) continue;
      const frac = (ow * oh) / (w * h);          // how much of the ART element the note eats
      if (frac > 0.10) {
        worst = Math.max(worst, frac);
        hits.push({tag: el.tagName.toLowerCase(),
                   txt: (el.textContent || '').trim().slice(0, 42),
                   covered: +frac.toFixed(2)});
      }
      break;
    }
  }
  hits.sort((a, b) => b.covered - a.covered);
  return {n: hits.length, worst: +worst.toFixed(2), hits: hits.slice(0, 5)};
})()"""


async def run(deck, present, max_cover):
    rows = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1366, "height": 768})
        pg = await ctx.new_page()
        try:
            await pg.goto(f"file://{deck}", timeout=180000)
            n = 0
            for _ in range(25):
                await pg.wait_for_timeout(600)
                n = await pg.evaluate("document.querySelectorAll('.slide').length")
                if n:
                    break
            if not n:
                print("0 slides in the DOM - refusing to report a pass on nothing")
                return 1
            if present:
                await pg.evaluate("present()")
                await pg.wait_for_timeout(900)
            for i in range(n):
                await pg.evaluate(f"go({i})")
                await pg.wait_for_timeout(160)
                nf = await pg.evaluate("document.querySelectorAll('.slide.on [data-frag]').length")
                steps = max(nf, 1)
                sid = await pg.evaluate(f"document.querySelectorAll('.slide')[{i}].dataset.sid")
                t = await pg.evaluate(f"document.querySelectorAll('.slide')[{i}].dataset.t")
                for k in range(1, steps + 1):
                    await pg.evaluate(f"setFrags(cur,{k})")
                    await pg.wait_for_timeout(430)
                    m = await pg.evaluate(MEASURE)
                    if m:
                        m.update(sid=sid, title=t or "", idx=i + 1, step=k, steps=steps)
                        rows.append(m)
        finally:
            await pg.close(); await ctx.close(); await b.close()

    bad = [r for r in rows if r["worst"] > max_cover]
    print(f"  {len(rows)} build states measured; note-over-art threshold {max_cover}\n")
    for r in bad:
        print(f"  {r['sid']:8} {r['step']}/{r['steps']}  {r['n']:>3} element(s) covered, worst {r['worst']:.0%}"
              f"   {r['title'][:24]}")
        for h in r["hits"][:3]:
            print(f"        {h['covered']:.0%} of <{h['tag']}> {h['txt']!r}")
    if bad:
        print(f"\nFAIL - the note box sits on top of the artwork in {len(bad)} of {len(rows)} build states.")
        print("The note is opaque, so whatever it covers is gone from the slide.")
        return 1
    print(f"PASS - no note covers artwork in any of {len(rows)} build states.")
    return 0


ap = argparse.ArgumentParser()
ap.add_argument("--deck", required=True)
ap.add_argument("--present", action="store_true")
ap.add_argument("--max-cover", type=float, default=0.02)
a = ap.parse_args()
import pathlib
sys.exit(asyncio.run(run(pathlib.Path(a.deck).resolve(), a.present, a.max_cover)))
