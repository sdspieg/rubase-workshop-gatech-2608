#!/usr/bin/env python3
"""Refuse a deck whose slides have unbalanced <div>s, or whose .ob-step is not inside .ob-pic.

WHY. On 2026-09-17 a step was lifted out of one slide and into a new one, and the extraction took
one </div> too few. The result: p0a17b was missing a closing div, the NEXT slide inherited a stray
one, and on that slide every .ob-step became a DIRECT CHILD OF THE SECTION. Because .ob-step is
position:absolute;inset:0, each one then covered the whole slide and permanently escaped its padding
box - so the deck's own autofit() could never find a scale, bottomed out at --sc 0.5, and rendered
the artwork on top of the title.

Nothing else caught it. The audit measured the slide happily, the note-overlap check passed, and the
HTML "looked" fine in a diff, because a browser silently repairs unbalanced markup into a DIFFERENT
tree than the one written. The defect is in the SOURCE, so the check belongs in the source.

Run:  python3 structure_check.py <deck.html> [...]
"""
import io, re, sys


def check(path):
    s = io.open(path, encoding="utf-8").read()
    secs = [m.start() for m in re.finditer(r'<section class="slide', s)] + [len(s)]
    bad = []
    for i in range(len(secs) - 1):
        body = s[secs[i]:secs[i + 1]]
        sid = (re.search(r'data-sid="([^"]+)"', body) or [None, "?"])[1]
        opens = len(re.findall(r"<div\b", body))
        closes = len(re.findall(r"</div>", body))
        if opens != closes:
            bad.append((sid, f"unbalanced <div>: {opens} open, {closes} close ({opens - closes:+d})"))
            continue
        # every .ob-step must sit inside the .ob-pic that precedes it
        pic = body.find('<div class="ob-pic"')
        for m in re.finditer(r'<div class="ob-step"', body):
            if pic < 0 or m.start() < pic:
                bad.append((sid, "an .ob-step appears outside/before .ob-pic"))
                break
            between = body[pic:m.start()]
            depth = len(re.findall(r"<div\b", between)) - len(re.findall(r"</div>", between))
            if depth < 1:
                bad.append((sid, "an .ob-step is NOT nested inside .ob-pic - it will cover the whole slide"))
                break
    return bad


def main(argv):
    if len(argv) < 2:
        print("usage: structure_check.py <deck.html> [...]"); return 2
    total = 0
    for path in argv[1:]:
        bad = check(path)
        total += len(bad)
        if bad:
            print(f"FAIL {path}: {len(bad)} structural problem(s)")
            for sid, why in bad:
                print(f"   {sid}  {why}")
        else:
            print(f"ok   {path}: every slide balances and every .ob-step is inside its .ob-pic")
    return 1 if total else 0


sys.exit(main(sys.argv))
