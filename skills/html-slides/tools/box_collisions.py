#!/usr/bin/env python3
"""Which explanation boxes are sitting on art the room has already been shown?

`verify_build.py` has a collision check, but it needs a `--manifest` naming each
component's rectangle, and without one it silently measures NOTHING and prints
PASS. Every slide in the 34-agent campaign passed it that way, and Day 2 shipped
boxes printed straight over the logos, the baskets and the bar chart they were
supposed to sit beside.

This needs no manifest. At each build step it asks the browser for the rectangles
of everything currently VISIBLE and already revealed - images, lit SVG groups,
chips, cards - and measures how much of that the current box covers.

An `.ob-scrim` step is exempt: a closing card over a deliberately dimmed picture is
the documented pattern, not a defect.

    python3 tools/box_collisions.py --deck deck.html --from 44 --to 72
"""
import argparse, asyncio, json, pathlib, sys

MEASURE = """(() => {
  const s = document.querySelector('.slide.on');
  const steps = [...s.querySelectorAll('.ob-step')];
  const cur = steps.filter(e => e.classList.contains('shown')).pop();
  if (!cur) return null;
  const note = cur.querySelector('.ob-note');
  if (!note) return null;
  const scrim = !!cur.querySelector('.ob-scrim');
  const nb = note.getBoundingClientRect();
  if (!nb.width) return null;
  const hit = [];
  // everything that is ART and currently visible: images, lit svg groups, and any
  // chip/label that is not part of the note itself
  const arts = [...s.querySelectorAll('img, svg g, svg text, svg rect, .ob-chip, .ob-lab')];
  for (const el of arts) {
    if (note.contains(el) || el.contains(note)) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || parseFloat(cs.opacity) < 0.25) continue;
    // an element inside a not-yet-shown step is not on screen
    const step = el.closest('.ob-step');
    if (step && !step.classList.contains('shown')) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 8 || r.height < 8) continue;
    const ox = Math.min(nb.right, r.right) - Math.max(nb.left, r.left);
    const oy = Math.min(nb.bottom, r.bottom) - Math.max(nb.top, r.top);
    if (ox > 0 && oy > 0) {
      const frac = (ox * oy) / (r.width * r.height);
      if (frac > 0.30) hit.push({tag: el.tagName.toLowerCase(),
                                 cls: (el.getAttribute('class') || '').slice(0, 24),
                                 covered: +frac.toFixed(2),
                                 area: Math.round(r.width * r.height)});
    }
  }
  hit.sort((a, b) => b.area - a.area);
  return {scrim, hits: hit.slice(0, 6), worst: hit.length ? hit[0].covered : 0, n: hit.length};
})()"""


async def run(deck, lo, hi, width):
    from playwright.async_api import async_playwright
    bad = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': width, 'height': 768})
        await pg.goto(f'file://{deck}#13')
        await pg.wait_for_timeout(1600)
        n = await pg.evaluate("document.querySelectorAll('.slide').length")
        for i in range(n):
            if not (lo <= i + 1 <= hi):
                continue
            meta = await pg.evaluate(
                f"(()=>{{const s=document.querySelectorAll('.slide')[{i}];"
                f"return {{sid:s.dataset.sid,t:s.dataset.t||''}};}})()")
            await pg.evaluate(f"go({i})")
            await pg.wait_for_timeout(220)
            nf = await pg.evaluate("document.querySelectorAll('.slide.on [data-frag]').length")
            for k in range(1, nf + 1):
                await pg.evaluate(f"setFrags(cur,{k})")
                await pg.wait_for_timeout(110)
                r = await pg.evaluate(MEASURE)
                if r and r['n'] and not r['scrim']:
                    bad.append({'slide': i + 1, 'sid': meta['sid'], 'title': meta['t'],
                                'step': k, **r})
        await b.close()
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--deck', default='deck.html')
    ap.add_argument('--from', dest='lo', type=int, default=1)
    ap.add_argument('--to', dest='hi', type=int, default=9999)
    ap.add_argument('--width', type=int, default=1366)
    ap.add_argument('--out')
    a = ap.parse_args()
    bad = asyncio.run(run(str(pathlib.Path(a.deck).resolve()), a.lo, a.hi, a.width))
    per = {}
    for r in bad:
        per.setdefault(r['sid'], []).append(r)
    print(f'{len(per)} slide(s) with a box on already-revealed art '
          f'({len(bad)} step(s)), slides {a.lo}-{a.hi}\n')
    for sid, rs in sorted(per.items(), key=lambda kv: -max(r['worst'] for r in kv[1])):
        w = max(r['worst'] for r in rs)
        r0 = max(rs, key=lambda r: r['worst'])
        print(f"  {sid:<8} s{r0['slide']:<4} worst {w:.0%} covered  steps "
              f"{','.join(str(r['step']) for r in rs):<12} {r0['title'][:34]}")
        for h in r0['hits'][:3]:
            print(f"           <{h['tag']} class=\"{h['cls']}\"> {h['covered']:.0%} covered")
    if a.out:
        json.dump(bad, open(a.out, 'w'), indent=1)
    return 1 if per else 0


if __name__ == '__main__':
    sys.exit(main())
