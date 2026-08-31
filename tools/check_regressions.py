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
    up to 30px today. Every class in an inline SVG style must be prefixed."""
    bad = []
    for m in re.finditer(r'<svg\b[^>]*>(.*?)</svg>', html, re.S):
        block = m.group(1)
        st = re.search(r'<style>(.*?)</style>', block, re.S)
        if not st:
            continue
        for cls in set(re.findall(r'\.([A-Za-z][\w-]*)\s*[,{]', st.group(1))):
            if len(cls) <= 2 or '-' not in cls:
                bad.append(cls)
    for s in sorted(set(bad)):
        out.append(f'SVG SCOPE: unprefixed class ".{s}" in an inline <style> will leak page-wide')
    return not bad


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
