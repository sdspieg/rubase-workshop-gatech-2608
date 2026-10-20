#!/usr/bin/env python3
"""SCREEN REAL ESTATE gate - fails a slide that wastes the screen.

🟥 THE INCIDENT (2026-09-16). SDS, on a slide whose content sat in a thin band with a third of the
slide empty below it: *"It's still VERY poor use of the screen real estate!!! Look for yourself!!!
Why are you so bad at this now when the last slidedecks were MUCH better?!?!? ... THIS HAS TO BE A
GATE!!!"*

The cause was a rule I invented to fix a different defect: boxes were covering art, so I forced all
art into the TOP band (y <= 214 of a 406 viewBox) and pinned every explanation box to the bottom
band. That removed the overlap and left the middle and bottom of every slide empty. ***A fix that
trades one defect for a worse one is not a fix, and nothing was measuring the second one.***

SKILL.md section 3 already said "optimize SRE" and "measure the figure as a fraction of SLIDE width
before and after". It was prose. Prose is the weak layer - this is the check that runs.

WHAT IT MEASURES, per slide, in its FULLY BUILT state (the state the room looks at longest):

  coverage   - union area of visible content (text, rects, images, notes) / area of the slide's
               content box. Low coverage means the slide is mostly background.
  vspan      - vertical extent of content / available height. Catches the exact failure above:
               content packed into a band with dead space beneath it.
  hspan      - horizontal extent / available width.
  deadband   - the tallest empty horizontal strip inside the content box, as a fraction of height.
               A slide can have decent vspan and still have a hole in the middle.
  overflow   - text whose rendered box escapes its own container rect (the card-edge spill).

DEFAULTS are deliberately loose - this is a floor against waste, not a demand for density.
"""
import argparse, asyncio, json, pathlib, sys

MEASURE = r"""(() => {
  const s = document.querySelector('.slide.on');
  if (!s) return null;
  const sb = s.getBoundingClientRect();
  // the usable content box: the slide minus its own padding
  const cs = getComputedStyle(s);
  const pad = {t: parseFloat(cs.paddingTop)||0, b: parseFloat(cs.paddingBottom)||0,
               l: parseFloat(cs.paddingLeft)||0, r: parseFloat(cs.paddingRight)||0};
  const box = {l: sb.left+pad.l, r: sb.right-pad.r, t: sb.top+pad.t, b: sb.bottom-pad.b};
  const W = Math.max(1, box.r-box.l), H = Math.max(1, box.b-box.t);

  // 🟥 This used to test ONLY the element's own style, so it counted text inside build steps that
  // are not on screen yet - which made the overflow tally disagree with the render and with a
  // getBBox() check that reported zero. A hidden .ob-step sets opacity on the STEP, not on its
  // text, so visibility has to be resolved by walking up to the slide.
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
  // only elements that actually paint something
  // 🟥 getBoundingClientRect() RETURNS A LAYOUT BOX EVEN WHEN AN ANCESTOR CLIPS IT AWAY.
  // .ob-pic is overflow:hidden, so an element positioned past its edge reports real geometry and
  // paints NOTHING. Measured 2026-09-17: this metric reported a 0.392 hole on p0a009 step 1 because
  // a path.pn-a and a text.pk-ru sat at 95-98% of the slide - below .ob-pic's own 88.3% bottom edge -
  // while a pixel sample of that band found ZERO pixels differing from the background. Same trap as
  // SKILL.md section 5, now in the gate that exists to catch it. Intersect every candidate against
  // each clipping ancestor and drop what survives to nothing.
  const clipOf = el => {
    let r = el.getBoundingClientRect();
    let l = r.left, rr = r.right, t = r.top, b = r.bottom;
    for (let a = el.parentElement; a && a !== s; a = a.parentElement) {
      const c = getComputedStyle(a);
      if (/hidden|clip|auto|scroll/.test(c.overflow + c.overflowX + c.overflowY)) {
        const ar = a.getBoundingClientRect();
        l = Math.max(l, ar.left); rr = Math.min(rr, ar.right);
        t = Math.max(t, ar.top);  b = Math.min(b, ar.bottom);
      }
    }
    return {left:l, right:rr, top:t, bottom:b, width:rr-l, height:b-t};
  };
  const sel = 'h2, p, text, rect, image, img, path, .ob-note, .ob-note .k, .ob-note .d';
  const rects = [];
  for (const el of s.querySelectorAll(sel)) {
    if (!vis(el)) continue;
    const r = clipOf(el);
    if (r.width < 2 || r.height < 2) continue;      // clipped to nothing = paints nothing
    // skip a full-bleed transparent backdrop - it would score 100% coverage on its own
    if (r.width >= W*0.98 && r.height >= H*0.98 && el.tagName==='rect') continue;
    rects.push({l:Math.max(r.left,box.l), r:Math.min(r.right,box.r),
                t:Math.max(r.top,box.t), b:Math.min(r.bottom,box.b)});
  }
  if (!rects.length) return {coverage:0, vspan:0, hspan:0, deadband:1, hole:0, overflow:0, n:0};

  // union area by scanline over a coarse grid - exact enough at 1px rows
  const GRID = 240;
  const cw = W/GRID, ch = H/GRID;
  const filled = new Uint8Array(GRID*GRID);
  for (const q of rects) {
    const x0=Math.max(0,Math.floor((q.l-box.l)/cw)), x1=Math.min(GRID-1,Math.ceil((q.r-box.l)/cw)-1);
    const y0=Math.max(0,Math.floor((q.t-box.t)/ch)), y1=Math.min(GRID-1,Math.ceil((q.b-box.t)/ch)-1);
    for (let y=y0;y<=y1;y++) for (let x=x0;x<=x1;x++) filled[y*GRID+x]=1;
  }
  let on=0; for (let i=0;i<filled.length;i++) on+=filled[i];
  const coverage = on/(GRID*GRID);

  // rows that carry any content
  const rowHas = new Uint8Array(GRID), colHas = new Uint8Array(GRID);
  for (let y=0;y<GRID;y++) for (let x=0;x<GRID;x++) if (filled[y*GRID+x]) { rowHas[y]=1; colHas[x]=1; }
  let first=-1,last=-1; for (let y=0;y<GRID;y++) if (rowHas[y]) { if(first<0)first=y; last=y; }
  const vspan = first<0 ? 0 : (last-first+1)/GRID;
  let fc=-1,lc=-1; for (let x=0;x<GRID;x++) if (colHas[x]) { if(fc<0)fc=x; lc=x; }
  const hspan = fc<0 ? 0 : (lc-fc+1)/GRID;

  // tallest empty horizontal strip ANYWHERE inside the box (including below the content)
  let dead=0, run=0;
  for (let y=0;y<GRID;y++) { if(!rowHas[y]) { run++; if(run>dead) dead=run; } else run=0; }
  const deadband = dead/GRID;

  // HOLE = tallest empty strip with content BOTH ABOVE AND BELOW it. This is the metric that
  // survives a half-built slide. A trailing gap at the bottom of step 1 of 4 is just an unfilled
  // slide and says nothing; a gap with art above it and a box below it is a HOLE, and it is wrong
  // on every step. The fixed-y explanation box that shipped - one thin row of art, ~30% empty
  // beneath it, closing only on the last step - scores a large hole on step 1 and none when built,
  // which is exactly why the built-state-only audit passed it.
  let hole=0, hrun=0;
  for (let y=first; y<=last; y++) { if(!rowHas[y]) { hrun++; if(hrun>hole) hole=hrun; } else hrun=0; }
  const holeFrac = first<0 ? 0 : hole/GRID;

  // Text escaping the card that HOLDS it (the card-edge spill).
  // 🟥 Two defects fixed 2026-09-17, after this count disagreed with both the renders and a
  // getBBox() check that found zero. (1) `inside` tested left, top and bottom but NOT the right
  // edge, so a string that started in a box and ran out of it counted as contained. (2) every text
  // was compared against EVERY rect in the same <svg>, so a label sitting beside a bar was judged
  // against that bar. A box only CONTAINS a text if the text's vertical mid-line falls inside it;
  // anything else is a neighbour, not a container. Rects are clip-corrected like everything else.
  let overflow = 0;
  for (const g of s.querySelectorAll('svg')) {
    const boxes = [...g.querySelectorAll('rect')].filter(vis)
      .map(r=>({el:r, b:clipOf(r)}))
      .filter(o=>o.b.width>40 && o.b.height>18);
    for (const t of g.querySelectorAll('text')) {
      if (!vis(t)) continue;
      const tb = clipOf(t);
      if (tb.width<2 || tb.height<2) continue;
      const mid = (tb.top + tb.bottom) / 2;
      // the smallest box whose vertical band holds this text's mid-line and that starts left of it
      let host = null;
      for (const o of boxes) {
        if (mid < o.b.top || mid > o.b.bottom) continue;      // a neighbour, not a container
        // 🟥 The host must CONTAIN the text's left edge, not merely start to the left of it.
        // Requiring only `tb.left >= o.b.left` let a row of sibling cards all qualify for each
        // other's labels, and picking the narrowest then judged card 5's text against card 1:
        // 9 false overflows on p0a011, a slide whose render is visibly clean.
        if (tb.left < o.b.left - 2 || tb.left > o.b.right + 2) continue;
        if (!host || (o.b.right - o.b.left) < (host.b.right - host.b.left)) host = o;
      }
      if (host && tb.right > host.b.right + 2) overflow++;
    }
  }
  // 🟥 COLLIDE: two VISIBLE <text> elements printing on top of each other.
  // Added 2026-09-17 because the worst defect of that session was caught by no metric at all.
  // p0a004 shipped two lines at y=173 and y=174 that rendered as "bftfc79Mdny na2ts4l5%ce by arm";
  // p0a009 shipped a header at y=169 over its own Russian line at y=172. Both passed every gate and
  // were found only by reading the render. Superimposition is not an overflow - nothing escapes a
  // container - so the spill check is structurally blind to it. Overlap is measured on the
  // intersection area, so ordinary tight leading (which does not intersect) stays quiet.
  let collide = 0;
  for (const g of s.querySelectorAll('svg')) {
    const ts = [...g.querySelectorAll('text')].filter(vis)
      .map(t => ({t, b: clipOf(t)}))
      .filter(o => o.b.width > 2 && o.b.height > 2);
    for (let i = 0; i < ts.length; i++) {
      for (let j = i + 1; j < ts.length; j++) {
        const a = ts[i].b, b2 = ts[j].b;
        const ow = Math.min(a.right, b2.right) - Math.max(a.left, b2.left);
        const oh = Math.min(a.bottom, b2.bottom) - Math.max(a.top, b2.top);
        if (ow <= 1 || oh <= 1) continue;
        // 🟥 Area ratio conflates two different things. An SVG <text> box carries the font's full
        // ascent and descent, so a 30px number stacked under its own 17px label overlaps that label
        // by ~50% of the SMALLER box's area while rendering perfectly - measured on p0a005's
        // HLTP/8, L2/37, L3/101 and TAXON/939 pairs, and on p0a0t4's tight-but-readable Cyrillic
        // line above its sources line. What distinguishes a true superimposition is that the two
        // BASELINES nearly coincide, so the vertical overlap consumes most of a line's height.
        const vFrac = oh / Math.min(a.height, b2.height);
        const hFrac = ow / Math.min(a.width, b2.width);
        const sameLine = vFrac > 0.9;   // same baseline: any real overlap is a collision
        if (vFrac > 0.6 && hFrac > (sameLine ? 0.10 : 0.35)) { collide++; break; }
      }
    }
  }

  // 🟥 CROSSSTEP: artwork from one build step drawn on top of artwork from another.
  // Art accumulates here - a revealed step stays on screen - so a step added later can land on a
  // step already shown. Measured 2026-09-17: a Sankey was inserted into a slide whose next step
  // draws a text block over the same region, and every check passed because each looks only WITHIN
  // one step. Compare the drawn bounding boxes of each revealed group against every other.
  // A group's bounding box is far too coarse: two wide, short rows stacked one above the other have
  // overlapping boxes while nothing actually touches. Compare DRAWN ELEMENTS across steps, and only
  // count a pair that genuinely covers each other - which is what puts one thing on top of another.
  let crossstep = 0;
  {
    const perStep = [...s.querySelectorAll('.ob-step')].filter(vis).map(st =>
      [...st.querySelectorAll('svg text, svg rect, svg path, svg circle, svg polygon')]
        .filter(vis)
        .map(el => ({el, q: clipOf(el)}))
        .filter(o => o.q.width > 3 && o.q.height > 3 &&
                     !(o.el.tagName === 'rect' && o.el.getAttribute('fill') === 'none'))
        // A DECLARED deliberate overlay (2026-10-10): the September 'machinery of knowing' slide draws
        // dashed 'mislead' paths ACROSS the library on purpose - the crossing is the metaphor - and
        // their bounding boxes overlap the shelves. The author must say why, in at least 12 characters
        // (data-crossstep-ok="<reason>"); a bare or empty marker exempts nothing.
        .filter(o => { const d = o.el.closest('[data-crossstep-ok]');
                       return !(d && (d.getAttribute('data-crossstep-ok') || '').trim().length >= 12); })
    ).filter(g => g.length);
    outer:
    for (let i = 0; i < perStep.length; i++) {
      for (let j = i + 1; j < perStep.length; j++) {
        for (const A of perStep[i]) for (const B of perStep[j]) {
          const ow = Math.min(A.q.right, B.q.right) - Math.max(A.q.left, B.q.left);
          const oh = Math.min(A.q.bottom, B.q.bottom) - Math.max(A.q.top, B.q.top);
          if (ow <= 2 || oh <= 2) continue;
          const inter = ow * oh;
          const small = Math.min(A.q.width * A.q.height, B.q.width * B.q.height);
          if (small <= 0) continue;
          // A deliberate HIGHLIGHT redraws the same row on top of itself - near-identical boxes.
          // That is intentional and must not be flagged; a pile-up is a PARTIAL overlap of two
          // different things. Measured on p0a0t4, where step 2 re-draws the T3 row to highlight it
          // and scored 11 false hits.
          const uni = (A.q.width * A.q.height) + (B.q.width * B.q.height) - inter;
          if (uni > 0 && inter / uni > 0.80) continue;          // a redraw of the same thing
          // A pile-up is two COMPARABLE things covering each other. A small label sitting inside
          // a large card from another step is ordinary containment - it scores inter/small ~ 1 and
          // must not count, or every highlighted row flags.
          const large = Math.max(A.q.width * A.q.height, B.q.width * B.q.height);
          if (large > 0 && inter / large < 0.25) continue;
          if (inter / small > 0.55) { crossstep++; if (crossstep > 40) break outer; }
        }
      }
    }
  }

  // 🟥 OCCLUDED: a filled <rect> painted OVER a label. SVG has no z-index - later elements win -
  // so a text written before its own bar is half-erased by it. Shipped on p0a016, where
  // "officialdom by NAMED VOICE" sat inside its bar's band and rendered sliced in half. `collide`
  // cannot see this: it compares text to text, and the thing on top here is a rectangle.
  let occluded = 0;
  for (const g of s.querySelectorAll('svg')) {
    const kids = [...g.querySelectorAll('text, rect')];
    for (let i = 0; i < kids.length; i++) {
      const t = kids[i];
      if (t.tagName !== 'text' || !vis(t)) continue;
      const tb = clipOf(t);
      if (tb.width < 2 || tb.height < 2) continue;
      for (let j = i + 1; j < kids.length; j++) {          // only what paints AFTER it
        const r = kids[j];
        if (r.tagName !== 'rect' || !vis(r)) continue;
        const f = r.getAttribute('fill');
        if (f === 'none') continue;                         // an outline does not hide text
        const rb = clipOf(r);
        const ow = Math.min(tb.right, rb.right) - Math.max(tb.left, rb.left);
        const oh = Math.min(tb.bottom, rb.bottom) - Math.max(tb.top, rb.top);
        if (ow <= 1 || oh <= 1) continue;
        if ((ow * oh) / (tb.width * tb.height) > 0.25) { occluded++; break; }
      }
    }
  }

  return {coverage:+coverage.toFixed(3), vspan:+vspan.toFixed(3), hspan:+hspan.toFixed(3),
          deadband:+deadband.toFixed(3), hole:+holeFrac.toFixed(3), overflow, collide, occluded,
          crossstep, n:rects.length};
})()"""


async def run(deck, width, height, thresholds):
    from playwright.async_api import async_playwright
    rows = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': width, 'height': height})
        await pg.goto(f'file://{deck}#1', timeout=180000)
        await pg.wait_for_timeout(1600)
        if thresholds.present:
            await pg.evaluate('present()')
            await pg.wait_for_timeout(700)
        n = await pg.evaluate("document.querySelectorAll('.slide').length")
        if n == 0:
            await b.close()
            raise SystemExit(f"sre_audit: 0 slides in the DOM for {deck} - refusing to pass on an "
                             f"empty measurement")
        for i in range(n):
            await pg.evaluate(f"go({i})")
            await pg.wait_for_timeout(80)
            nf = await pg.evaluate("document.querySelectorAll('.slide.on [data-frag]').length")
            steps = max(nf, 1)
            sid = await pg.evaluate(f"document.querySelectorAll('.slide')[{i}].dataset.sid")
            t = await pg.evaluate(f"document.querySelectorAll('.slide')[{i}].dataset.t")
            # A deliberate exception is declared ON the slide and PRINTED, never hidden by loosening
            # a threshold for every deck. data-sre-ok="<reason>" waives only the SPACE metrics
            # (coverage / vspan / deadband) for that one slide; a spill, a collision or an occluded
            # label is a defect on any slide and can never be waived this way.
            waive = await pg.evaluate(
                f"document.querySelectorAll('.slide')[{i}].dataset.sreOk || ''")
            # EVERY step, not only the built one. The built state is the one step where a fixed-y
            # box's gap closes, so a built-state-only audit is blind to precisely the defect that
            # made SDS say "you CLEARLY also didn't visually double-check all animation buildup
            # snapshots". --built-only restores the old behaviour; it is not the default.
            ks = [steps] if thresholds.built_only else range(1, steps + 1)
            for k in ks:
                await pg.evaluate(f"setFrags(cur,{k})")
                await pg.wait_for_timeout(260)
                m = await pg.evaluate(MEASURE)
                if m:
                    m.update(sid=sid, title=t or '', idx=i + 1, step=k, steps=steps,
                             sre_ok=waive)
                    rows.append(m)
        await b.close()
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--deck', default='deck.html')
    ap.add_argument('--width', type=int, default=1600)
    ap.add_argument('--height', type=int, default=900)
    ap.add_argument('--min-coverage', type=float, default=0.24)
    ap.add_argument('--min-vspan', type=float, default=0.72)
    ap.add_argument('--max-deadband', type=float, default=0.26)
    ap.add_argument('--max-hole', type=float, default=0.17,
                    help='tallest empty strip WITH CONTENT ABOVE AND BELOW IT, as a fraction of\n'
                         'height. Unlike deadband this is meaningful mid-build, so it is the one\n'
                         'waste metric enforced on every step.')
    ap.add_argument('--built-only', action='store_true',
                    help='measure only the fully built state (the pre-2026-09-16 behaviour, which\n'
                         'was blind to fixed-y boxes that only close their gap on the last step)')
    ap.add_argument('--present', action='store_true',
                    help='measure in PRESENT mode - the state the room actually sees, and the\n'
                         'one the windowed view flatters: the sidebar is gone and the slide\n'
                         'fills the screen, so dead space is proportionally larger')
    ap.add_argument('--out')
    a = ap.parse_args()

    rows = asyncio.run(run(str(pathlib.Path(a.deck).resolve()), a.width, a.height, a))
    if a.out:
        pathlib.Path(a.out).write_text(json.dumps(rows, indent=1), encoding='utf-8')

    bad = []
    print(f"{'#':>3} {'sid':9} {'step':>5} {'cover':>6} {'vspan':>6} {'hspan':>6} "
          f"{'dead':>6} {'hole':>6} {'ovf':>4} {'coll':>5}  title")
    for r in rows:
        built = r.get('step', 1) == r.get('steps', 1)
        flags = []
        # Coverage and vspan judge how well a FINISHED slide fills the screen; a half-built slide
        # is legitimately sparse, so enforcing them mid-build would flag every build-up in the deck.
        waived = bool(r.get('sre_ok'))
        if built and not waived and r['coverage'] < a.min_coverage: flags.append('COVERAGE')
        if built and not waived and r['vspan'] < a.min_vspan:       flags.append('VSPAN')
        if built and not waived and r['deadband'] > a.max_deadband: flags.append('DEADBAND')
        # A hole and a text spill are wrong on EVERY step.
        if r.get('hole', 0) > a.max_hole:             flags.append('HOLE')
        if r['overflow']:                             flags.append(f"OVERFLOW x{r['overflow']}")
        # text printing THROUGH other text - wrong on every step, and no other metric sees it
        if r.get('collide'):                          flags.append(f"COLLIDE x{r['collide']}")
        # a label painted over by a later filled rect - SVG has no z-index
        if r.get('occluded'):                         flags.append(f"OCCLUDED x{r['occluded']}")
        # one build step's artwork drawn on top of another's - art accumulates here
        if r.get('crossstep'):                        flags.append(f"CROSSSTEP x{r['crossstep']}")
        mark = '  <-- ' + ', '.join(flags) if flags else (
            f"  [space waived: {r['sre_ok'][:54]}]" if r.get('sre_ok') else '')
        if flags:
            bad.append((r, flags))
        print(f"{r['idx']:>3} {r['sid']:9} {r.get('step',1):>2}/{r.get('steps',1):<2} "
              f"{r['coverage']:>6.2f} {r['vspan']:>6.2f} "
              f"{r['hspan']:>6.2f} {r['deadband']:>6.2f} {r.get('hole',0):>6.2f} "
              f"{r['overflow']:>4} {r.get('collide',0):>5}  {r['title'][:22]}{mark}")

    print(f"\nthresholds (built state): coverage>={a.min_coverage} vspan>={a.min_vspan} "
          f"deadband<={a.max_deadband}")
    print(f"thresholds (EVERY step):  hole<={a.max_hole} overflow==0 collide==0 occluded==0 "
          f"crossstep==0")
    if bad:
        nsl = len({r['sid'] for r, _ in bad})
        print(f"FAIL - {len(bad)} build state(s) across {nsl} slide(s) waste the screen or "
              f"spill text  [{a.deck}]")
        return 1
    print(f"PASS - all {len(rows)} build states across "
          f"{len({r['sid'] for r in rows})} slides use the screen  [{a.deck}]")
    return 0


if __name__ == '__main__':
    sys.exit(main())
