#!/usr/bin/env python3
"""Measure every slide as RENDERED: smallest readable text, and how much frame it uses.

Why this exists: the static gates were blind in two ways the completeness critic
proved on 2026-08-31.

  * `slide_inventory.py` checks `cqw` declarations and SVG `px`. Text sized in
    `rem`/`em` walks straight through - 18 fragments rendered below the floor and
    every static check passed them.
  * `verify_build.py` returns PASS on everything without a `--manifest`, because its
    coverage check then measures nothing at all. It scored PASS on a slide whose two
    text runs were overprinted into illegibility.

Only the browser knows the real size, so ask the browser.

    python3 tools/render_audit.py --deck deck.html --out /tmp/audit.json
    python3 tools/render_audit.py --deck deck.html --sids 2363ed,e2c812
"""
import argparse, asyncio, json, pathlib, sys

FLOOR_PCT = 1.10          # smallest readable text, as a share of slide width
OCCUPANCY_FLOOR = 0.42    # below this the slide is mostly empty frame

MEASURE = """(() => {
  const s = document.querySelector('.slide.on');
  if (!s) return null;
  const sr = s.getBoundingClientRect();
  let smallest = 1e9, smallText = '', minX = 1e9, minY = 1e9, maxX = -1e9, maxY = -1e9;
  const overlaps = [];
  const texts = [];
  for (const el of s.querySelectorAll('*')) {
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.opacity === '0') continue;
    minX = Math.min(minX, r.left); minY = Math.min(minY, r.top);
    maxX = Math.max(maxX, r.right); maxY = Math.max(maxY, r.bottom);
    // a leaf that carries its own words is the only thing whose font size matters
    const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (own) {
      const fs = parseFloat(cs.fontSize);
      if (fs && fs < smallest) { smallest = fs; smallText = el.textContent.trim().slice(0, 48); }
      texts.push({el, x: r.left, y: r.top, w: r.width, h: r.height,
                  t: el.textContent.trim().slice(0, 30)});
    }
  }
  // overprinted text: two text boxes sharing more than half of the smaller one's area
  for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
    const a = texts[i], b = texts[j];
    // a <b> inside a sentence overlaps its own parent completely - that is nesting,
    // not collision. Only unrelated elements sharing space are a defect. The first
    // version of this check reported 84 "overprints", nearly all of them a span
    // inside its own paragraph, which would have buried the handful of real ones.
    if (a.el.contains(b.el) || b.el.contains(a.el)) continue;
    const ox = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x);
    const oy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
    if (ox > 0 && oy > 0) {
      const inter = ox * oy, small = Math.min(a.w * a.h, b.w * b.h);
      if (small && inter / small > 0.5) overlaps.push([a.t, b.t]);
    }
  }
  const used = (maxX > minX && maxY > minY) ? ((maxX - minX) * (maxY - minY)) : 0;
  return {sid: s.dataset.sid, title: s.dataset.t || '',
          smallest_px: smallest === 1e9 ? null : +smallest.toFixed(2),
          smallest_text: smallText,
          slide_w: +sr.width.toFixed(1),
          smallest_pct: smallest === 1e9 ? null : +(smallest / sr.width * 100).toFixed(3),
          occupancy: +(used / (sr.width * sr.height)).toFixed(3),
          overprinted: overlaps.slice(0, 3)};
})()"""


async def run(deck, width, sids):
    from playwright.async_api import async_playwright
    out = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': width, 'height': 768})
        await pg.goto(f'file://{deck}#13')
        await pg.wait_for_timeout(1600)
        n = await pg.evaluate("document.querySelectorAll('.slide').length")
        for i in range(n):
            sid = await pg.evaluate(f"document.querySelectorAll('.slide')[{i}].dataset.sid")
            if sids and sid not in sids:
                continue
            await pg.evaluate(f"go({i})")
            await pg.wait_for_timeout(70)
            # measure fully built - the state the room spends most time looking at
            await pg.evaluate("setFrags(cur, document.querySelectorAll('.slide.on [data-frag]').length)")
            await pg.wait_for_timeout(60)
            r = await pg.evaluate(MEASURE)
            if r:
                out.append(r)
        await b.close()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--deck', default='deck.html')
    ap.add_argument('--width', type=int, default=1366)
    ap.add_argument('--sids', default='')
    ap.add_argument('--out')
    a = ap.parse_args()
    sids = {s for s in a.sids.split(',') if s}
    rows = asyncio.run(run(str(pathlib.Path(a.deck).resolve()), a.width, sids))

    tiny = [r for r in rows if r['smallest_pct'] is not None and r['smallest_pct'] < FLOOR_PCT]
    empty = [r for r in rows if r['occupancy'] < OCCUPANCY_FLOOR]
    over = [r for r in rows if r['overprinted']]

    print(f'{len(rows)} slides measured at {a.width}px\n')
    print(f'--- text below the {FLOOR_PCT}% floor: {len(tiny)}')
    for r in sorted(tiny, key=lambda r: r['smallest_pct'])[:25]:
        print(f"  {r['sid']:<8} {r['smallest_pct']:>6.3f}%  {r['smallest_px']:>5}px  "
              f"{r['title'][:30]:<31} \"{r['smallest_text'][:32]}\"")
    print(f"\n--- frame occupancy below {OCCUPANCY_FLOOR}: {len(empty)}")
    for r in sorted(empty, key=lambda r: r['occupancy'])[:15]:
        print(f"  {r['sid']:<8} {r['occupancy']:>5.2f}  {r['title'][:44]}")
    print(f'\n--- overprinted text runs: {len(over)}')
    for r in over[:10]:
        print(f"  {r['sid']:<8} {r['title'][:34]:<35} {r['overprinted'][0]}")
    if a.out:
        json.dump({'width': a.width, 'slides': rows}, open(a.out, 'w'), indent=1)
        print('\nwrote', a.out)
    return 1 if (tiny or over) else 0


if __name__ == '__main__':
    sys.exit(main())
