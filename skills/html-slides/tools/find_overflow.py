#!/usr/bin/env python3
"""Name the exact <text> elements whose rendered box escapes their own container rect.

The audit reports a COUNT; a count does not tell you which string to shorten. It also does not walk
ancestors, so it counts text inside build steps that are not on screen yet - true as a defect (the
text is too wide whenever it does appear) but confusing when read against one screenshot.
"""
import asyncio, sys
from playwright.async_api import async_playwright

URL = "http://127.0.0.1:18078/deck.html#1"

JS = r"""(() => {
  const out = [];
  for (const s of document.querySelectorAll('.slide')) {
    const sid = s.dataset.sid;
    for (const g of s.querySelectorAll('svg')) {
      const boxes = [...g.querySelectorAll('rect')]
        .filter(r => !(r.getAttribute('fill') === 'none' && !r.getAttribute('stroke')))
        .map(r => ({el: r, b: r.getBBox()}))
        .filter(o => o.b.width > 40 && o.b.height > 18);
      for (const t of g.querySelectorAll('text')) {
        let tb; try { tb = t.getBBox(); } catch (e) { continue; }
        if (tb.width < 2) continue;
        for (const o of boxes) {
          const startsInside = tb.x >= o.b.x - 2 && tb.x < o.b.x + o.b.width;
          const spills = tb.x + tb.width > o.b.x + o.b.width - 6;
          if (startsInside && spills) {
            out.push({sid, text: t.textContent.slice(0, 46),
                      textW: Math.round(tb.width), boxW: Math.round(o.b.width),
                      over: Math.round(tb.x + tb.width - (o.b.x + o.b.width))});
            break;
          }
        }
      }
    }
  }
  return out;
})()"""


async def main():
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
            rows = await pg.evaluate(JS)
            print(f"  {len(rows)} text element(s) escaping their own box\n")
            for r in rows:
                print(f"   {r['sid']:8} over by {r['over']:>4}px  (text {r['textW']} in box {r['boxW']})  {r['text']!r}")
            return 0
        finally:
            await pg.close(); await ctx.close(); await b.close()


sys.exit(asyncio.run(main()))
