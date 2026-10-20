#!/usr/bin/env python3
"""Render fresh, hash-manifested PNGs for every deck build state.

The output directory MUST NOT exist. On 2026-09-23 a copied deck project retained successful QA
images from the older deck; those files were mistaken for evidence about a new eleven-slide deck.
This renderer owns a new directory, captures state 0 through the final state for every slide at every
required viewport, hashes every PNG, and writes manifest.json bound to the exact deck bytes.
"""
import argparse
import asyncio
import hashlib
import json
import pathlib
import sys
import time

from playwright.async_api import async_playwright


IMG_WAIT_JS = """() => new Promise(done => {
  const sl = document.querySelector('.slide.on') || document;
  const urls = new Set();
  sl.querySelectorAll('img').forEach(i => { if (i.currentSrc || i.src) urls.add(i.currentSrc || i.src); });
  sl.querySelectorAll('image').forEach(i => {
    const h = i.getAttribute('href') || i.getAttribute('xlink:href'); if (h) urls.add(new URL(h, document.baseURI).href); });
  const ps = [...sl.querySelectorAll('img')].map(i => (i.complete && i.naturalWidth) ? null : i.decode().catch(() => null));
  [...urls].forEach(u => { const im = new Image(); im.src = u; ps.push(im.decode().catch(() => null)); });
  const t = setTimeout(done, 10000);
  Promise.all(ps).then(() => requestAnimationFrame(() => requestAnimationFrame(() => { clearTimeout(t); done(); })));
})"""


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


async def render(deck: pathlib.Path, out: pathlib.Path, widths: list[int]) -> dict:
    if out.exists():
        raise SystemExit(f"REFUSE: render output already exists (stale evidence risk): {out}")
    out.mkdir(parents=True)
    started = time.time()
    deck_digest = sha256(deck)
    states = []
    slides_model = None

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        try:
            for width in widths:
                height = round(width * 9 / 16)
                ctx = await browser.new_context(viewport={"width": width, "height": height})
                page = await ctx.new_page()
                messages = []
                page.on("console", lambda m: messages.append(f"{m.type}: {m.text[:180]}"))
                page.on("pageerror", lambda e: messages.append(f"PAGEERROR: {str(e)[:220]}"))
                try:
                    await page.goto(deck.as_uri() + "#1", wait_until="domcontentloaded", timeout=180000)
                    nslides = 0
                    for _ in range(25):
                        await page.wait_for_timeout(400)
                        nslides = await page.evaluate("document.querySelectorAll('.slide').length")
                        if nslides:
                            break
                    if not nslides:
                        raise RuntimeError(f"0 slides in the DOM at {width}px: {messages[:8]}")
                    await page.evaluate("present()")
                    await page.wait_for_timeout(500)

                    model = []
                    for i in range(nslides):
                        await page.evaluate(f"go({i})")
                        await page.wait_for_timeout(100)
                        sid = await page.evaluate(
                            f"document.querySelectorAll('.slide')[{i}].dataset.sid || 'slide{i+1:02d}'")
                        nfrags = await page.evaluate(
                            "document.querySelectorAll('.slide.on [data-frag]').length")
                        model.append({"slide_index": i + 1, "sid": sid, "final_state": nfrags})
                        for state in range(0, nfrags + 1):
                            await page.evaluate(f"setFrags(cur,{state})")
                            await page.wait_for_timeout(220)
                            # 2026-10-10: a fixed 220 ms is not enough when the deck is read from a slow
                            # mount (Google Drive): 30+ AIRA states were captured with EMPTY photo slots
                            # at some widths and not others. Wait until every image on the current slide
                            # (HTML <img> and SVG <image>) has decoded, capped at 10 s.
                            await page.evaluate(IMG_WAIT_JS)
                            name = (f"w{width}_s{i+1:02d}_{sid}_"
                                    f"state{state:02d}of{nfrags:02d}.png")
                            target = out / name
                            await page.screenshot(path=str(target))
                            states.append({
                                "name": name,
                                "sha256": sha256(target),
                                "bytes": target.stat().st_size,
                                "width": width,
                                "height": height,
                                "slide_index": i + 1,
                                "sid": sid,
                                "state": state,
                                "final_state": nfrags,
                            })
                    if slides_model is None:
                        slides_model = model
                    elif model != slides_model:
                        raise RuntimeError(f"slide/state model changed across viewports: {width}px")
                finally:
                    await page.close()
                    await ctx.close()
        finally:
            await browser.close()

    expected = len(widths) * sum(s["final_state"] + 1 for s in slides_model or [])
    if len(states) != expected:
        raise RuntimeError(f"coverage mismatch: rendered {len(states)}, expected {expected}")
    for width in widths:
        for slide in slides_model or []:
            got = sorted(s["state"] for s in states
                         if s["width"] == width and s["sid"] == slide["sid"])
            want = list(range(0, slide["final_state"] + 1))
            if got != want:
                raise RuntimeError(f"missing state coverage at {width}px/{slide['sid']}: {got} != {want}")

    manifest = {
        "schema": "html-slides-render-manifest/v2",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "render_started_epoch": started,
        "deck": str(deck),
        "deck_sha256": deck_digest,
        "widths": widths,
        "slides": slides_model or [],
        "coverage": "state-0-through-final",
        "n_states": len(states),
        "states": states,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--deck", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--widths", default="1280,1366,1440,1600")
    args = ap.parse_args()
    deck = pathlib.Path(args.deck).resolve()
    out = pathlib.Path(args.out).resolve()
    widths = [int(v) for v in args.widths.split(",") if v.strip()]
    if not deck.is_file():
        print(f"FAIL: no such deck: {deck}")
        return 2
    if widths != sorted(set(widths)) or not widths:
        print("FAIL: widths must be a non-empty ascending unique list")
        return 2
    try:
        manifest = asyncio.run(render(deck, out, widths))
    except Exception as exc:
        print(f"FAIL: {exc}")
        return 1
    print(f"PASS: {len(manifest['slides'])} slides, {manifest['n_states']} fresh state PNGs")
    print(f"manifest: {out / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
