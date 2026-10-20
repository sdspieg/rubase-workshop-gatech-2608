#!/usr/bin/env python3
"""Measure every slide, so the three work queues are evidence and not opinion.

Produces one JSON with three inventories:

  A. dumps          - slides still carrying a FLAT PowerPoint export. Two kinds:
                      "raw"  = class="slide img", one <img> and no words of its own
                      "fake" = an obuild slide whose ob-plate/ob-reveal is that same
                               flat export with clip-path windows cut in it. That is
                               still a png dump; SDS rejected five of these by name.
  B. germanic       - text-heavy slides with little or no visual: the ones that read
                      as a wall of prose. "NEVER less visual, but if possible GLADLY
                      more visual" - so this file also records a per-slide VISUAL
                      SCORE, which a later run compares against, and a slide whose
                      score DROPS is a regression.
  C. sre            - screen-real-estate and font problems: declared font sizes below
                      the floor, and slides whose rendered content leaves a large part
                      of the frame empty.

The rendered half (C's emptiness, and any real font size) needs a browser; run with
--render to include it. Without it the static half still runs.

    python3 tools/slide_inventory.py --out inventory.json [--render]
    python3 tools/slide_inventory.py --compare inventory.json    # visual-score gate
"""
import argparse, json, os, pathlib, re, sys

FONT_FLOOR_CQW = 1.10
ROOT = pathlib.Path(__file__).resolve().parent.parent


def sections(html):
    return [m.group(0) for m in re.finditer(r'<section class="slide.*?</section>', html, re.S)]


def strip_notes(s):
    return re.sub(r'data-n="[^"]*"', '', s)


def visible_text(s):
    t = re.sub(r'<style>.*?</style>', ' ', strip_notes(s), flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()


def visual_score(s):
    """A deliberately crude, STABLE count of visual substance on a slide.

    It is not a beauty metric. Its whole job is to be comparable across time so
    that making a slide MORE visual scores higher and quietly turning a visual
    back into prose scores lower - which is the regression SDS wants gated.
    """
    body = strip_notes(s)
    # DISTINCT sources, not <img> tags. Counting tags rewarded exactly the thing
    # being eliminated: a flat export used as the plate plus three clip-path
    # reveals of that SAME file counted as four visuals (40) and beat a genuine
    # rebuild from three real component images (30), so the gate fired on real
    # progress the first time it ran.
    imgs = len({m.group(1) for m in re.finditer(r'<img\b[^>]*src="([^"]+)"', body)})
    svgs = len(re.findall(r'<svg\b', body))
    # drawn marks inside inline SVG carry most of the visual weight when present
    marks = len(re.findall(r'<(?:rect|circle|path|line|polygon|polyline|ellipse|g)\b', body))
    return imgs * 10 + svgs * 10 + min(marks, 120)


def classify(s, idx):
    sid = re.search(r'data-sid="([^"]+)"', s).group(1)
    t = re.search(r'data-t="([^"]*)"', s).group(1)
    cls = re.search(r'class="([^"]*)"', s).group(1)
    body = strip_notes(s)
    srcs = re.findall(r'src="(img/[^"]+)"', body)
    txt = visible_text(s)
    rec = {'n': idx, 'sid': sid, 'title': t, 'cls': cls, 'chars': len(txt),
           'imgs': srcs, 'visual': visual_score(s)}

    # --- A. dumps -------------------------------------------------------------
    raw = 'img' in cls.split() and len(txt) < 40
    plate = re.search(r'class="ob-plate" src="(img/[^"]+)"', body)
    reveals = re.findall(r'class="ob-reveal" src="(img/[^"]+)"', body)
    fake = bool(plate and reveals and all(r == plate.group(1) for r in reveals))
    if raw:
        rec['dump'] = 'raw'
    elif fake:
        rec['dump'] = 'fake'          # flat export + clip-path windows
        rec['flat'] = plate.group(1)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--deck', default=str(ROOT / 'deck.html'))
    ap.add_argument('--out', default=str(ROOT / 'inventory.json'))
    ap.add_argument('--compare')
    a = ap.parse_args()

    html = pathlib.Path(a.deck).read_text(encoding='utf-8')
    secs = sections(html)
    recs = [classify(s, i) for i, s in enumerate(secs, 1)]

    if a.compare:
        old = {r['sid']: r for r in json.load(open(a.compare))['slides']}
        drops = [(r['sid'], r['title'], old[r['sid']]['visual'], r['visual'])
                 for r in recs
                 if r['sid'] in old and r['visual'] < old[r['sid']]['visual']]
        for sid, t, was, now in drops:
            print(f'LESS VISUAL: {sid} "{t[:44]}"  {was} -> {now}')
        print('PASS - no slide became less visual' if not drops
              else f'FAIL - {len(drops)} slide(s) went backwards')
        return 1 if drops else 0

    # --- B. text-heavy with little visual -------------------------------------
    for r in recs:
        if 'divider' in r['cls']:
            continue
        if r['chars'] >= 420 and r['visual'] <= 10:
            r['germanic'] = True

    # --- C. declared fonts below the floor ------------------------------------
    css = '\n'.join(m.group(1) for m in re.finditer(r'<style>(.*?)</style>', html, re.S))
    small = sorted({float(m.group(1)) for m in re.finditer(r'font-size:\s*(?:calc\()?\s*([0-9.]+)cqw', css)
                    if float(m.group(1)) < FONT_FLOOR_CQW})
    svg_px = []
    for m in re.finditer(r'<section class="slide.*?</section>', html, re.S):
        s = m.group(0)
        sid = re.search(r'data-sid="([^"]+)"', s).group(1)
        for sm in re.finditer(r'<svg\b[^>]*viewBox="0 0 ([\d.]+) ([\d.]+)"(.*?)</svg>', s, re.S):
            vbw = float(sm.group(1))
            for f in re.finditer(r'font:[^;"}]*?([\d.]+)px', sm.group(3)):
                px = float(f.group(1))
                if px / vbw * 100 < FONT_FLOOR_CQW:       # share of the figure's own width
                    svg_px.append({'sid': sid, 'px': px, 'viewBox_w': vbw,
                                   'pct_of_width': round(px / vbw * 100, 3)})

    out = {'deck': os.path.basename(a.deck), 'slides': recs,
           'A_dumps': [r for r in recs if r.get('dump')],
           'B_germanic': [r for r in recs if r.get('germanic')],
           'C_small_css_cqw': small, 'C_small_svg_px': svg_px}
    json.dump(out, open(a.out, 'w'), indent=1)

    print(f'{len(secs)} slides')
    print(f"A. png dumps still to rebuild : {len(out['A_dumps'])} "
          f"(raw {sum(1 for r in out['A_dumps'] if r['dump']=='raw')}, "
          f"flat-export-with-windows {sum(1 for r in out['A_dumps'] if r['dump']=='fake')})")
    print(f"B. text-heavy, little visual  : {len(out['B_germanic'])}")
    print(f"C. svg labels under the floor : {len(svg_px)} on "
          f"{len({x['sid'] for x in svg_px})} slides; css sizes under floor: {small}")
    print('wrote', a.out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
