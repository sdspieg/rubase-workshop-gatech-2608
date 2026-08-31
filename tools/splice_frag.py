#!/usr/bin/env python3
"""Splice a rebuilt <section> back into deck.html by data-sid.

Agents write frag_<sid>.html into a scratchpad; this puts them in, one at a time,
so four concurrent authors never write the same file. Refuses on anything it
cannot match exactly, and refuses a fragment whose data-n is not the one the
deck already carries (the speaker notes are not the agents' to rewrite).
"""
import re, sys, pathlib, html

DECK = pathlib.Path(__file__).resolve().parent.parent / 'deck.html'

def sections(text):
    for m in re.finditer(r'<section class="slide.*?</section>', text, re.S):
        yield m

def main(paths):
    text = DECK.read_text(encoding='utf-8')
    for p in paths:
        frag = pathlib.Path(p).read_text(encoding='utf-8').strip()
        sid = re.search(r'data-sid="([^"]+)"', frag)
        if not sid:
            sys.exit(f'{p}: no data-sid')
        sid = sid.group(1)
        hits = [m for m in sections(text) if f'data-sid="{sid}"' in m.group(0)]
        if len(hits) != 1:
            sys.exit(f'{p}: {len(hits)} sections match data-sid={sid}')
        old = hits[0].group(0)
        oldn = re.search(r'data-n="([^"]*)"', old)
        newn = re.search(r'data-n="([^"]*)"', frag)
        if oldn and (not newn or newn.group(1) != oldn.group(1)):
            # keep the deck's notes; agents were told to copy them verbatim
            if newn:
                frag = frag.replace(newn.group(0), oldn.group(0), 1)
            else:
                frag = frag.replace('<section class="slide',
                                    '<section ' + oldn.group(0) + ' class="slide', 1)
            print(f'  {sid}: restored deck data-n')
        text = text[:hits[0].start()] + frag + text[hits[0].end():]
        print(f'spliced {sid}  ({len(old)} -> {len(frag)} bytes)')
    DECK.write_text(text, encoding='utf-8')

if __name__ == '__main__':
    main(sys.argv[1:])
