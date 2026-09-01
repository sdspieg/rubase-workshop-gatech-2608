#!/usr/bin/env python3
"""Splice a rebuilt <section> back into deck.html by data-sid.

Agents write frag_<sid>.html into a scratchpad; this puts them in, one at a time,
so four concurrent authors never write the same file. Refuses on anything it
cannot match exactly, and refuses a fragment whose data-n is not the one the
deck already carries (the speaker notes are not the agents' to rewrite).
"""
import re, sys, pathlib, html

# The deck this writes into. Resolved from THIS FILE's real location, which means a copy of the
# repo that symlinks tools/ still writes the ORIGINAL deck - an agent hit exactly that today and
# had to reverse-apply the diff. Pass --deck <path> to target a private copy.
DECK = pathlib.Path(__file__).resolve().parent.parent / 'deck.html'

def sections(text):
    for m in re.finditer(r'<section class="slide.*?</section>', text, re.S):
        yield m

def _is_flat_export(frag):
    """One raster used as the plate AND as every reveal = a dimmed png dump."""
    plate = re.search(r'class="ob-plate" src="(img/[^"]+)"', frag)
    reveals = re.findall(r'class="ob-reveal" src="(img/[^"]+)"', frag)
    return bool(plate and reveals and all(r == plate.group(1) for r in reveals))


def main(paths):
    text = DECK.read_text(encoding='utf-8')
    refused = []
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
        # THE GATE (SDS, 2026-08-31): a "rebuilt" slide that is still the flat
        # PowerPoint export with clip-path windows cut in it is NOT rebuilt. 26 of
        # them reached the deck and were reported done before anyone measured it.
        # Refuse them here, where they would otherwise become a green report.
        if _is_flat_export(frag) and '--allow-dump' not in sys.argv:
            refused.append(f'{sid}: still a flat export with clip-path windows, not a '
                           f'rebuild. Compose it from img/src2025/ assets, or pass '
                           f'--allow-dump with a reason.')
            continue
        oldn = re.search(r'data-n="([^"]*)"', old)
        newn = re.search(r'data-n="([^"]*)"', frag)
        # The notes are the deck's, not the fragment's - EXCEPT when the fragment
        # APPENDS to them. Moving instructor stage direction off the slide and into
        # data-n is required work ("these slides are for the students"), and a blanket
        # restore silently threw that away. An append keeps the whole old value as a
        # prefix; anything else is a rewrite and is refused.
        appended = bool(oldn and newn and newn.group(1).startswith(oldn.group(1))
                        and len(newn.group(1)) > len(oldn.group(1)))
        if appended:
            print(f'  {sid}: data-n APPENDED (+{len(newn.group(1)) - len(oldn.group(1))} chars) - kept')
        elif oldn and (not newn or newn.group(1) != oldn.group(1)):
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
    for r in refused:
        print('REFUSED ' + r)
    if refused:
        sys.exit(f'{len(refused)} fragment(s) refused; the rest were spliced')

if __name__ == '__main__':
    args = sys.argv[1:]
    # --allow-dump is read off sys.argv by the gate above; it must NOT survive into the
    # file list or it is opened as a path and the run dies BEFORE deck.html is written -
    # so the flag could never actually be used.
    while '--allow-dump' in args:
        args.remove('--allow-dump')
    if '--deck' in args:
        i = args.index('--deck')
        DECK = pathlib.Path(args[i + 1]).resolve()
        del args[i:i + 2]
    main(args)
