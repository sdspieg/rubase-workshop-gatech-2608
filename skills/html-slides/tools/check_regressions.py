#!/usr/bin/env python3
"""Fail on the defects that have already been fixed once and came back.

SDS, 2026-08-31: "why do you not learn or self-improve, but UNlearn and
self-deteriorate?!?" - about the build-up flash, which was fixed, and returned.

The reason it returned is worth stating plainly: the original fix lived in ONE
CSS rule (`.slide [data-frag]{...transition:none}`) and was invisible to anyone
writing the NEXT build class. Every obuild class added afterwards re-declared its
own hidden state with a fade, and nothing anywhere objected. A fix that depends on
the next author remembering it is not a fix, it is a hope.

So each defect below is a check that fails loudly, and every new slide has to pass
it. Run it before any commit that touches deck.html:

    python3 tools/check_regressions.py            # or --deck <path>

Exit status 1 if any check fails.
"""
import argparse, pathlib, re, sys

FLOOR_CQW = 1.10          # nothing readable should render below this share of slide width


def check_hidden_state_fades(css, out):
    """A hidden state that TRANSITIONS animates back to hidden after autofit's
    body.measuring pass lights everything - the room sees the slide flash fully
    built and fade away. Hidden states must be instantaneous."""
    bad = []
    for m in re.finditer(r'([^{}]+)\{([^{}]*opacity:\s*0[^{}]*)\}', css):
        sel, body = m.group(1).strip(), m.group(2)
        if 'transition' not in body:
            continue
        if re.search(r'transition:\s*none', body):
            continue
        bad.append(sel.replace('\n', ' ')[:90])
    for s in bad:
        out.append(f'FLASH: hidden state fades, so it will animate back to hidden -- {s}')
    return not bad


def check_font_floor(css, out):
    """SDS, 16:07: 'Too small font. Let's define a mandatory lower threshold.'
    Anything sized in cqw below the floor is unreadable from the back of a room."""
    bad = []
    for m in re.finditer(r'font-size:\s*(?:calc\()?\s*([0-9.]+)cqw', css):
        v = float(m.group(1))
        if v < FLOOR_CQW:
            ctx = css[max(0, m.start() - 70):m.start()].replace('\n', ' ')[-60:]
            bad.append(f'{v}cqw  ...{ctx}')
    for s in bad:
        out.append(f'FONT FLOOR ({FLOOR_CQW}cqw): {s}')
    return not bad


def check_svg_class_scoping(html, out):
    """An inline SVG <style> is NOT scoped to its subtree: bare class names leak
    and restyle every other inlined SVG on the page. This blew one slide's labels
    up to 30px today.

    Only a class defined DIFFERENTLY in more than one inline SVG is actually doing
    harm, so that is what FAILS. A merely-unprefixed but unique class is a warning:
    it is a collision waiting to happen the next time someone adds a figure, but it
    is not currently breaking anything, and a gate that cries about 31 harmless
    names is a gate people learn to ignore.
    """
    defs = {}
    # Only SVGs INSIDE a slide count. Scanning the whole document made the check
    # match the literal text "<svg>" sitting in a CSS COMMENT in a fragment's
    # stylesheet, then swallow the rest of the stylesheet as that "SVG's" content -
    # which reported 50 phantom collisions on deck-level classes like .ob-pic and
    # turned preflight red for no reason. A gate that invents failures gets ignored
    # just as fast as one that misses them.
    # PER SECTION, never a concatenation: an unbalanced "<svg" mentioned in one
    # slide's prose or speaker notes lets the regex run on into the NEXT slide and
    # pair with its </svg>, inventing collisions out of two unrelated figures. Same
    # family of bug as scanning the whole document; both invented ~50 failures.
    for sec in re.finditer(r'<section class="slide.*?</section>', html, re.S):
        for m in re.finditer(r'<svg\b[^>]*>(.*?)</svg>', sec.group(0), re.S):
            st = re.search(r'<style>(.*?)</style>', m.group(1), re.S)
            if not st:
                continue
            for rm in re.finditer(r'\.([A-Za-z][\w-]*)\s*\{([^}]*)\}', st.group(1)):
                defs.setdefault(rm.group(1), set()).add(re.sub(r'\s+', '', rm.group(2)))
    collisions = sorted(k for k, v in defs.items() if len(v) > 1)
    unprefixed = sorted(k for k in defs if '-' not in k and k not in collisions)
    for c in collisions:
        out.append(f'SVG COLLISION: ".{c}" is defined {len(defs[c])} different ways in '
                   f'separate inline SVGs - they are restyling each other')
    if unprefixed:
        out.append(f'  (warning, not failing: {len(unprefixed)} unprefixed but unique SVG '
                   f'classes - {", ".join("." + u for u in unprefixed[:8])}'
                   f'{" ..." if len(unprefixed) > 8 else ""})')
    return not collisions


def check_review_layer_captured(html, out):
    """A deck cut from a SERVED page carries the review host's injected layer with it.

    Incident, 2026-10-20 (CENTREPEACE/Helsinki): both decks for Adam were built from
    the review host, so the presentation shipped with a `gtr-favicon` speech-bubble
    icon and an inline `document.title = "\uD83D\uDCAC " + t` script baked into the
    FILE. It passed every "is review.js present?" check - because review.js genuinely
    was not there - while the tab the Finnish hosts would open showed a comment-bubble
    favicon and a title reading as a review copy. The glyph was written as an escaped
    surrogate pair, so grepping for the literal character found nothing.

    LESSONS.md already warned that the review server injects user, favicon and title
    prefix; that warning could not catch this, because it was about COMPARING hashes,
    not about what a rebuild swallows. Hence a check.

    What does NOT fail: `body.present #gtr-bar{display:none}` and its siblings. Those
    are the deck's own rules for hiding the review bar when it IS injected, and they
    belong in the source.
    """
    bad = []
    if re.search(r'id=["\']gtr-favicon["\']', html):
        bad.append('a captured <link id="gtr-favicon"> - the review host\'s speech-bubble icon')
    if '__GTR_USER__' in html:
        bad.append('a captured __GTR_USER__ placeholder from the review host')
    if re.search(r'<script[^>]+src=[^>]*review[^>]*>', html):
        bad.append('a <script src=...review...> injected by the review host')
    for m in re.finditer(r'document\.title\s*=\s*["\'][^"\']{0,20}["\']\s*\+', html):
        frag = m.group(0)
        if 'uD83D' in frag or chr(0x1F4AC) in frag:
            bad.append('an inline script prefixing document.title with the comment bubble')
    for b in bad:
        out.append(f'REVIEW LAYER CAPTURED: {b} - this deck was cut from a SERVED page, '
                   f'not from its source; strip it before shipping')
    return not bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--deck', default=str(pathlib.Path(__file__).resolve().parent.parent / 'deck.html'))
    # 🟥 The flash gate was BLIND where the work actually happens. It read CSS only from
    # inline <style> blocks, but agents write their CSS to frag_<sid>.css files, which are
    # never checked until after they are spliced into the deck - i.e. after the defect has
    # already landed. Three fragments arrived carrying the fade, one of them REVERTING an
    # applied fix, and the gate passed the deck while they sat there. Point it at the
    # fragments too: --css accepts files or globs.
    ap.add_argument('--css', nargs='*', default=[], help='extra .css files/globs to check')
    a = ap.parse_args()
    html = pathlib.Path(a.deck).read_text(encoding='utf-8') if pathlib.Path(a.deck).exists() else ''
    css = '\n'.join(m.group(1) for m in re.finditer(r'<style>(.*?)</style>', html, re.S))
    import glob as _g
    for pat in a.css:
        for f in sorted(_g.glob(pat)):
            css += '\n/* ==== ' + f + ' ==== */\n' + pathlib.Path(f).read_text(encoding='utf-8')

    out, ok = [], True
    for fn, arg in ((check_hidden_state_fades, css), (check_font_floor, css),
                    (check_svg_class_scoping, html), (check_review_layer_captured, html)):
        ok &= fn(arg, out)

    for line in out:
        print(line)
    print(('PASS' if ok else f'FAIL - {len(out)} regression(s)') + f'  [{a.deck}]')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
