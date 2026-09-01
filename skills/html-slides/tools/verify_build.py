#!/usr/bin/env python3
"""Step a built slide and MEASURE it, instead of looking at it and hoping.

Why this exists: every defect in the 2026-08-31 rebuild pass was a geometry
defect - an explanation box landing on art that was already revealed, or falling
off the bottom of the slide - and none of them were visible from the source.
DOM probes do not catch them either; only the rendered rectangles do.

For each build step it reports:
  * every element that escapes the slide box (overflow), and
  * the overlap between the CURRENT explanation box and the bounding box of every
    component revealed SO FAR (a later component may be covered - it is not on
    screen yet).

It also writes one PNG per step so the pictures can be eyeballed afterwards, per
the standing rule that visual work is verified on the picture, never the DOM.

    python3 tools/verify_build.py --sid 04c7c6
    python3 tools/verify_build.py --sid 10f148 --widths 1280,1366,1600 --shots /tmp/pr
"""
import argparse, asyncio, json, os, sys

async def run(deck, sid, widths, shots, manifest, allow):
    from playwright.async_api import async_playwright
    man = json.load(open(manifest)) if manifest and os.path.exists(manifest) else {}
    bad = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for W in widths:
            pg = await b.new_page(viewport={'width': W, 'height': 900})
            errs = []
            pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            # the stage only has a size once a slide hash is live, so land on one first
            await pg.goto(f'file://{deck}#13'); await pg.wait_for_timeout(1500)
            i = await pg.evaluate(f"[...document.querySelectorAll('.slide')].findIndex(s=>s.dataset.sid==='{sid}')")
            if i < 0: sys.exit(f'no slide with data-sid={sid}')
            await pg.evaluate(f"go({i})"); await pg.wait_for_timeout(900)
            title = await pg.evaluate("document.querySelector('.slide.on').dataset.t")
            n = await pg.evaluate("document.querySelectorAll('.slide.on [data-frag]').length")
            box = await pg.evaluate("(()=>{const r=document.querySelector('.slide.on')"
                                    ".getBoundingClientRect();return{x:r.x,y:r.y,width:r.width,height:r.height};})()")
            print(f'--- {W}px | slide {i} "{title}" | {n} build steps')
            for k in range(1, n + 1):
                await pg.evaluate(f"setFrags(cur,{k})"); await pg.wait_for_timeout(320)
                if shots and W == widths[0]:
                    os.makedirs(shots, exist_ok=True)
                    await pg.screenshot(path=os.path.join(shots, f'{sid}_{k:02d}.png'), clip=box)
                r = await pg.evaluate("""(()=>{const s=document.querySelector('.slide.on');
                  const sr=s.getBoundingClientRect();
                  const pic=s.querySelector('.ob-pic'); const pr=pic?pic.getBoundingClientRect():sr;
                  const steps=[...s.querySelectorAll('.ob-step')];
                  const cur=steps.filter(e=>e.classList.contains('shown')).pop();
                  const note=cur&&cur.querySelector('.ob-note');
                  const scrim=!!(cur&&cur.querySelector('.ob-scrim'));
                  const esc=[...s.querySelectorAll('.ob-note,.ob-pic,img,svg')].filter(e=>{
                    // A clip-path'd <image> reports its UNCLIPPED source rect, which is far
                    // larger than what is on screen and routinely hangs off the slide while the
                    // visible crop sits comfortably inside. Counting it as an escape is a false
                    // alarm - and a gate that cries wolf gets ignored. Judge it by its clip.
                    if (e.getAttribute && e.getAttribute('clip-path')) return false;
                    const r=e.getBoundingClientRect();
                    return r.right>sr.right+1||r.bottom>sr.bottom+1||r.left<sr.left-1||r.top<sr.top-1;}).length;
                  const imgs=[...s.querySelectorAll('img')];
                  return {esc, scrim, broken:imgs.filter(i=>!i.complete||i.naturalWidth===0).length,
                    note: note?{x:(note.getBoundingClientRect().x-pr.x)/pr.width,
                                y:(note.getBoundingClientRect().y-pr.y)/pr.height,
                                w:note.getBoundingClientRect().width/pr.width,
                                h:note.getBoundingClientRect().height/pr.height}:null};})()""")
                if r['esc']:    bad.append(f'{W}px step {k}: {r["esc"]} element(s) escape the slide')
                if r['broken']: bad.append(f'{W}px step {k}: {r["broken"]} image(s) failed to load')
                hits = []
                if r['note'] and man and not r['scrim']:
                    CW, CH = 1770, 750
                    nb = [r['note']['x']*CW, r['note']['y']*CH,
                          (r['note']['x']+r['note']['w'])*CW, (r['note']['y']+r['note']['h'])*CH]
                    for name in list(man)[:k]:
                        cb = man[name]['box']
                        ox = max(0, min(nb[2], cb[2]) - max(nb[0], cb[0]))
                        oy = max(0, min(nb[3], cb[3]) - max(nb[1], cb[1]))
                        if ox*oy > 0:
                            pct = round(ox*oy / ((cb[2]-cb[0])*(cb[3]-cb[1])) * 100)
                            hits.append(f'{name} {pct}%')
                            if pct > 20 and f'{k}:{name}' not in allow:
                                bad.append(f'{W}px step {k}: box covers {pct}% of "{name}"')
                tag = ' [scrim card - collisions deliberate]' if r['scrim'] else ''
                print(f'   step {k:2d}  escapes={r["esc"]} broken={r["broken"]}'
                      + (f'  covers: {", ".join(hits)}' if hits else '  covers: nothing') + tag)
            if errs: bad.append(f'{W}px: console errors {errs[:2]}')
            await pg.close()
        await b.close()
    print('\nFAIL' if bad else '\nPASS')
    for x in bad: print('  ' + x)
    return 1 if bad else 0

if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('--deck', default=os.path.abspath('deck.html'))
    a.add_argument('--sid', required=True, help='data-sid of the slide to step')
    a.add_argument('--widths', default='1280,1366,1600')
    a.add_argument('--shots', default='', help='directory to write one PNG per step')
    a.add_argument('--manifest', default='', help='component manifest.json for collision checks')
    a.add_argument('--allow', default='', help='comma-separated STEP:COMPONENT collisions that are '
                   'a deliberate design choice, e.g. "8:protein,8:dna". Declare them; do not silence the check.')
    g = a.parse_args()
    sys.exit(asyncio.run(run(g.deck, g.sid, [int(w) for w in g.widths.split(',')], g.shots, g.manifest,
                             {x.strip() for x in g.allow.split(',') if x.strip()})))
