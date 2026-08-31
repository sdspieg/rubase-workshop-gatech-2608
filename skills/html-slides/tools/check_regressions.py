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
    for m in re.finditer(r'<svg\b[^>]*>(.*?)</svg>', html, re.S):
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--deck', default=str(pathlib.Path(__file__).resolve().parent.parent / 'deck.html'))
    a = ap.parse_args()
    html = pathlib.Path(a.deck).read_text(encoding='utf-8')
    css = '\n'.join(m.group(1) for m in re.finditer(r'<style>(.*?)</style>', html, re.S))

    out, ok = [], True
    for fn, arg in ((check_hidden_state_fades, css), (check_font_floor, css),
                    (check_svg_class_scoping, html)):
        ok &= fn(arg, out)

    for line in out:
        print(line)
    print(('PASS' if ok else f'FAIL - {len(out)} regression(s)') + f'  [{a.deck}]')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
