# Working on this deck — read before touching deck.html

Claude Code loads this file automatically when a session starts in this directory. Codex reads
`AGENTS.md` and Gemini reads `GEMINI.md`; both point here. **Whatever you remember about this deck
from another machine is not the authority — this file and the gates in `tools/` are.**

Everything below was learned the hard way on 2026-08-31, mostly by getting it wrong first. Each rule
names the incident, because a rule without its incident gets rationalised away.

---

## 1 · "Rebuilt" means composed from the pptx media. Nothing else counts.

`img/src2025/` holds **194 individual images unzipped from SDS's PowerPoint `/media` folder**. A slide
is rebuilt when it is **composed in HTML from those individual assets**, with **every word set in the
deck's own type**.

🟥 **Taking the flat PowerPoint export, dimming it, and cutting `clip-path` windows in it is NOT a
rebuild.** It is still a png dump carrying the old slide's title, captions, layout and JPEG artefacts
baked into a raster. In his words: *"Not rebuilt. Just a png dump."* · *"Terrible. Has not been
rebuilt but SHOULD be rebuilt in html WITH the original vizzes!!!"* · *"you HAVE the individual source
images that you can just use!!!"*

**26 slides reached the deck that way and were reported done before anyone measured it.** That is why
`tools/splice_frag.py` now REFUSES a fragment whose `ob-plate` and every `ob-reveal` are the same
file. If the component genuinely is not in `src2025`, say so and draw it as inline SVG — do not fall
back to the composite.

**Find the pieces by OPENING them and looking.** Filenames say nothing. `image10.jpeg` is a ballerina.

---

## 2 · Never less visual. Gladly more.

His words: *"You can ALWAYS use better visuals if you can find or generate them (please do!), BUT you
can not re-germanize my previous manual attempts to make them more visual. NEVER less visual, but if
possible GLADLY more visual should be the rule (and the gate!!!)."*

`python3 tools/slide_inventory.py --compare <earlier.json>` fails if any slide's visual score dropped.
Take a baseline BEFORE you edit and compare after.

⚠️ The metric counts **distinct image sources**, not `<img>` tags — because counting tags made a flat
export used four times score higher than a genuine three-component rebuild, and the gate fired on real
progress the first time it ran.

---

## 3 · Type has a floor, and screen real estate is not free

*"Too small font. Let's define a mandatory lower threshold."* Floor: **1.10% of slide width**.
`tools/check_regressions.py` enforces it for CSS; `slide_inventory.py` reports sub-floor labels inside
inline SVGs, measured against that figure's own viewBox.

"Optimize SRE" usually means the problem is **inside the figure**, not around it. On the query
slide he said it three times; the cause was a viewBox whose aspect did not match its container, so
`object-fit` letterboxed ~60px per side on top of the chart's own dead space. Stretching the
container could never have fixed it. **Measure the rendered bar/figure as a fraction of SLIDE width,
before and after, and quote both numbers.**

---

## 4 · The build grammar

One click reveals **one component of the picture plus the box explaining it**; the previous box
disappears. Boxes carry 2–3 sentences of real prose, never a label. The box goes where the
**already-revealed** art is not — a later component may be sat on, it is not on screen yet.
Full procedure and the decomposition routes: [`SLIDE_BUILD_PATTERN.md`](SLIDE_BUILD_PATTERN.md).

---

## 5 · Four traps that have each shipped a defect

- 🟥 **A hidden state must carry `transition:none`.** `autofit()` lights every fragment via
  `body.measuring` to measure a full slide; a hidden state that *transitions* then animates back to
  hidden, so the slide visibly paints fully built and fades — *"flashes again before starting the
  animation"*. Fixed once, then reintroduced by every new build class, because the original fix was
  one rule nobody could see. **33 rules carried it.** Now gated.
- 🟥 **An inline SVG `<style>` is NOT scoped to its subtree.** Bare class names leak page-wide and
  restyle other inlined SVGs. Six real collisions already exist (`.ft .hd .mc .mono .ph .tag`).
  Prefix every class.
- 🟥 **`.obuild .ob-pic img` outranks a plain two-class selector**, so positioned component images get
  force-stretched to fill the picture box and photographs come out distorted. Use
  `.slideclass .ob-pic img.component` plus explicit `right:auto; bottom:auto`.
- 🟥 **A box clipped by the picture's own `overflow:hidden` does NOT register as an escape** in
  `verify_build.py`. It shipped three times in one day. **Read the render.**

---

## 6 · Verification is measured, not asserted

```bash
python3 tools/preflight.sh                      # all three gates at once
python3 tools/verify_build.py --sid <sid> --shots /tmp/<sid>   # then READ the PNGs
```

DOM inspection is **not** verification in this project. Neither is "the tool passed" — the tool has
blind spots listed above. Take the screenshot, `Read` it, and say what you actually see.

---

## 7 · The review comments are the spec

The store lives at `../comments.json` (parent of this repo), served by `../review_server.py` on
**127.0.0.1:8777**. Before editing a slide, read its comments.

🟥 **Match a comment to its slide by `elText`, never by the slide number in the route.** Slide numbers
shift when a slide is added or removed; matching by number sent a whole afternoon's work to the wrong
slide. And **never truncate comment text when reading** — a 400-character cut hid the second half of a
comment and lost a requirement.

🟥 **`review.js` replaces localStorage with whatever the server returns on page load.** Starting the
server with an empty store and opening a page destroyed 25 of his comments. They were recovered out of
Chrome's LevelDB with `tools/` scripts, but do not repeat it: check `../comments.json` is populated
**before** starting the server or opening the review UI.

---

## 8 · One browser tab, not a new one every time

🟥 **Do not launch a new browser window to show something.** SDS, 2026-09-01: *"do NOT spawn a
million browser tabs! Just keep using the same one!!!!!"* Six were opened in one session - two QR
pages, the Doc, the deck twice, a specific slide - each one landing on top of whatever he was doing.

Reuse the window he already has:
- **If Chrome is already running with its debugging port enabled**, navigate the EXISTING tab:
  `open_and_front.py --front <match>` brings an already-open tab forward, and CDP can navigate it.
  That is precisely what that script exists for.
- **If it is not**, ask him to reload or navigate, or ask once before relaunching. Do not paper
  over a missing port by opening another window. Note that hand-launching a browser with that
  port is itself forbidden here (gate #97) - the canonical launchers own it.
- Bringing an existing window to the front is fine and encouraged; opening another is not.

## 9 · Editing concurrently

Many agents cannot edit `deck.html` at once. Each writes `frag_<sid>.html` (+ `.css`) to a scratchpad;
`tools/splice_frag.py` splices them in by `data-sid`, preserves the deck's own `data-n` speaker notes,
refuses png dumps, and skips-and-reports rather than aborting the batch.

House style: US English. HTML entities `&middot; &ndash; &rsquo;`. No em-dashes in prose — NBSP + en-dash.
