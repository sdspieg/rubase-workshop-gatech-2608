#!/usr/bin/env python3
"""Decide which rebuilt-slide fragments may be spliced, and say why for the rest.

A 34-agent campaign produced 118 fragments and reported "104 done, 0 blocked".
The completeness critic then measured them and found the report false: two were
still flat exports, FOUR had deleted SDS's picture and replaced it with typed prose
(the one direction he explicitly forbade), twelve were byte-identical to the deck,
and three carried the flash defect - one of them reverting a fix already applied.

A batch that size cannot be judged by reading agent reports. This judges the
artifacts:

  SPLICE      passes every test
  QUARANTINE  fails one, with the reason named

    python3 tools/triage_fragments.py <scratchpad> [--apply]
"""
import argparse, glob, os, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import slide_inventory as SI


def deck_sections(html):
    return {re.search(r'data-sid="([^"]+)"', s).group(1): s
            for s in SI.sections(html)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('scratchpad')
    ap.add_argument('--deck', default=str(ROOT / 'deck.html'))
    ap.add_argument('--apply', action='store_true', help='move quarantined fragments aside')
    a = ap.parse_args()

    cur = deck_sections(pathlib.Path(a.deck).read_text(encoding='utf-8'))
    rows = []
    for f in sorted(glob.glob(os.path.join(a.scratchpad, 'frag_*.html'))):
        frag = pathlib.Path(f).read_text(encoding='utf-8').strip()
        if not frag.startswith('<section'):
            continue
        m = re.search(r'data-sid="([^"]+)"', frag)
        if not m:
            rows.append((os.path.basename(f), '?', 'QUARANTINE', 'no data-sid')); continue
        sid = m.group(1)
        new = SI.classify(frag, 0)
        old = SI.classify(cur[sid], 0) if sid in cur else None

        verdict, why = 'SPLICE', ''
        if sid not in cur:
            verdict, why = 'QUARANTINE', 'no slide with this data-sid in the deck'
        elif new.get('dump') == 'fake':
            verdict, why = 'QUARANTINE', 'still a flat export with clip-path windows'
        elif old and new['visual'] < old['visual']:
            verdict, why = ('QUARANTINE',
                            f"LESS VISUAL {old['visual']} -> {new['visual']}"
                            + (' (his picture deleted, replaced by prose)'
                               if new['visual'] == 0 and old['visual'] > 0 else ''))
        elif frag == cur[sid].strip():
            verdict, why = 'QUARANTINE', 'byte-identical to the deck - no work was done'
        rows.append((os.path.basename(f), sid, verdict, why))

    ok = [r for r in rows if r[2] == 'SPLICE']
    bad = [r for r in rows if r[2] != 'SPLICE']
    for n, sid, v, why in bad:
        print(f'QUARANTINE {sid:<8} {why}')
    print(f'\n{len(ok)} splice-able, {len(bad)} quarantined, {len(rows)} fragments seen')

    if a.apply and bad:
        q = os.path.join(a.scratchpad, 'quarantine')
        os.makedirs(q, exist_ok=True)
        for n, sid, v, why in bad:
            for ext in ('.html', '.css'):
                src = os.path.join(a.scratchpad, f'frag_{sid}{ext}')
                if os.path.exists(src):
                    os.replace(src, os.path.join(q, f'frag_{sid}{ext}'))
        print(f'moved {len(bad)} fragment(s) to {q}')
    print('\n'.join(f'  splice: {r[1]}' for r in ok[:80]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
