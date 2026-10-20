#!/usr/bin/env python3
"""Refuse HTML markup inside an SVG <text> element.

WHY. On 2026-09-17 five <text> elements in the PASP deck carried <em> for their English glosses.
<em> is HTML: inside an SVG <text> the browser renders NOTHING for it and drops the rest of the line.
So «Пресс-секретарь президента РФ <em>(of the president of the RF)</em> Дмитрий Песков отметил…»
displayed as «Пресс-секретарь президента РФ» and stopped, and the note beneath it referred to a
pronoun the audience could not see.

Nothing caught it. There was no overflow (nothing escaped a box), no collision (the text was simply
absent) and the slide scored a healthy coverage number, because what is missing cannot be measured.
That is the whole point of a static check: it reads the SOURCE, so absence is visible.

Every one of the five was an English gloss - exactly the thing the house rule says must always
accompany a Russian sentence. The failure mode is therefore not cosmetic, it deletes the translation.

Use <tspan> instead, styled inline:
    <tspan font-style="italic" fill="#9db8d6">(gloss)</tspan>

Run:  python3 svg_text_html_check.py <deck.html> [...]
"""
import io, re, sys

# These <text> nodes never span a newline, and an unbounded DOTALL pattern matches straight across
# a source comment - which is how the first version of this check reported a false positive on its
# own documentation.
TEXT = re.compile(r'<text\b[^>\n]*>[^\n]*?</text>')
HTML_IN_SVG = re.compile(r'</?(em|strong|b|i|u|span|br|p|div)\b')


def check(path):
    s = io.open(path, encoding="utf-8").read()
    secs = [m.start() for m in re.finditer(r'<section class="slide', s)] + [len(s)]
    bad = []
    for i in range(len(secs) - 1):
        body = s[secs[i]:secs[i + 1]]
        sid = (re.search(r'data-sid="([^"]+)"', body) or [None, '?'])[1]
        for m in TEXT.finditer(body):
            hit = HTML_IN_SVG.search(m.group(0))
            if hit:
                plain = re.sub(r'<[^>]+>', '', m.group(0))
                bad.append((sid, hit.group(0), plain.strip()[:58]))
    return bad


def main(argv):
    if len(argv) < 2:
        print("usage: svg_text_html_check.py <deck.html> [...]"); return 2
    total = 0
    for path in argv[1:]:
        bad = check(path)
        total += len(bad)
        if bad:
            print(f"FAIL {path}: {len(bad)} SVG <text> element(s) carry HTML that will not render "
                  f"and will truncate the line")
            for sid, tag, txt in bad:
                print(f"   {sid}  {tag}  {txt!r}")
        else:
            print(f"ok   {path}: no HTML markup inside any SVG <text>")
    if total:
        print("\nUse <tspan font-style=\"italic\" fill=\"#9db8d6\">…</tspan> instead of <em>.")
        return 1
    return 0


sys.exit(main(sys.argv))
