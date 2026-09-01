# The visual specification — every element, and what it must obey

Frozen 2026-09-01 at SDS's instruction: *"ALL visual elements have to be specified and BAKED into
the skill."* Nothing here is style advice. Every clause is a defect that shipped, was measured, and
now has a rule or a gate.

---

## 1 · The slide

```html
<section class="slide obuild <slideclass>" data-t="<sidebar title>" data-sid="<6 hex>" data-n="<speaker notes>">
  <h2>Title</h2>
  <p class="sub">One line under it.</p>
  <div class="ob-pic"> … the picture and its build steps … </div>
</section>
```

- `data-sid` is the identity. **Never change it** — the review comments, every tool and every splice
  address slides by it. `data-t` is the sidebar label; `data-n` is the speaker notes and is copied
  **verbatim** by anyone rebuilding the slide.
- `h2` size is **constant** (`var(--title-size)`, 4.5cqw). It is not autofit-scaled: SDS asked for one
  standard title size and got an explanation instead, twice.
- Body content is autofit-scaled by `--sc`, which the deck binary-searches per slide. **`--sc` can
  exceed 1**, so anything multiplied by the raw `--sc` grows without limit — that is how a source
  footnote came to render as large as the sentence it supported. Cap it: `min(var(--sc), N)`.

## 2 · The picture and its build steps

```html
<div class="ob-pic">
  <img class="ob-plate" src="…" alt="">                 <!-- optional dimmed backdrop -->
  <div class="ob-step" data-frag="1">                    <!-- ONE click -->
     …one component of the picture…
     <div class="ob-note" style="--x:52%;--y:14%;--w:40%">
       <div class="k">Heading</div><div class="d">Two or three sentences of real prose.</div>
     </div>
  </div>
  <div class="ob-step" data-frag="1"><div class="ob-scrim"></div>
     <div class="ob-note wide" style="…">…closing card…</div></div>
</div>
```

| element | contract |
|---|---|
| `.ob-step` | **one per click.** `setFrags()` walks `[data-frag]` in document order; the *value* is ignored. Each step is `position:absolute; inset:0` — a **full-size transparent layer**. |
| `.ob-note` | the explanation box. Positioned by `--x` (left), `--y` (top), `--w` (width), all % of `.ob-pic`. Only the CURRENT one is visible, by CSS alone: `.ob-step:has(~ .ob-step.shown) .ob-note{opacity:0;visibility:hidden}` |
| `.ob-scrim` | dims the finished picture for a closing card. It buys **legibility, not coverage** — the box still hides whatever is under it. |
| `.ob-plate` | the flat source shown dimmed. **Its presence plus reveals of the same file is the png-dump signature the splicer refuses.** |
| `.k` / `.d` | box heading / box prose. Never a bare label: 2–3 sentences. |

**Reveals accumulate; boxes do not.** Every component revealed so far stays lit. Exactly one box is
on screen.

🟥 **The box goes where the ALREADY-REVEALED art is not.** A later component may be sat on — it is
not on screen yet. Measured with `box_collisions.py`; a box covering >30% of any revealed element
fails. Four Day-2 slides shipped with boxes covering 91–100% of labels, logos and diagrams.

🟥 **If the last step has no free space, give it an `.ob-scrim`** and close over the dimmed picture.
That is the documented exception, not a licence to print on live art.

## 3 · Components: the three routes

| route | when | how |
|---|---|---|
| **1 · original build layers** | the figure came from a generator that emits stages | transparent PNGs, one per stage |
| **2 · the pptx media** | the figure exists as separate assets | `img/src2025/` — **194 files unzipped from the PowerPoint `/media` folder.** Compose in HTML from them. |
| **3 · draw it** | no original, or the original is a wall of text | inline SVG, classes prefixed |

🟥 **Route 0 does not exist.** Dimming the flat PowerPoint export and cutting `clip-path` windows in
it is **not** a rebuild — it is a png dump with the old slide's title, captions and layout baked into
a raster. 26 slides shipped that way and were reported done. `splice_frag.py` refuses a fragment whose
plate and every reveal are the same file.

**Identify assets by OPENING them and looking.** `image10.jpeg` is a ballerina.

## 4 · Cropping one component out of a source image

The working technique, used across this deck:

```html
<svg class="<pfx>-svg" viewBox="0 0 1000 400" preserveAspectRatio="xMidYMid meet">
  <defs><clipPath id="<pfx>-figclip"><rect x="20" y="108" width="270" height="183" rx="6"/></clipPath></defs>
  <rect class="<pfx>-figbg" x="20" y="108" width="270" height="183" rx="6"/>   <!-- white panel behind -->
  <image href="img/src2025/imageNN.jpeg" x="-735" y="-90" width="1071" height="446"
         clip-path="url(#<pfx>-figclip)" preserveAspectRatio="none"><title>what it shows</title></image>
  <rect class="<pfx>-figfr" x="20" y="108" width="270" height="183" rx="6"/>   <!-- frame on top -->
</svg>
```

- The `<image>` is scaled and offset so the wanted region lands inside the clip window.
- 🟥 **Its `getBoundingClientRect()` is the UNCLIPPED source rect** — far larger than what is visible,
  and often mostly off-slide. Any tool reasoning about "where is this picture" must use the clip
  rectangle, not the element's own box. This is why a picture-preferring rule is needed before a
  cropped image can ever be selected.
- Always give the `<image>` a `<title>`: it is the only accessible description, and it is what a
  reviewer sees when they select it.

## 5 · Inline SVG

- **Prefix every class per slide.** An inline SVG `<style>` is **not** scoped to its subtree; bare
  names leak page-wide and restyle other figures. Six classes (`.ft .hd .mc .mono .ph .tag`) were each
  defined 2–4 different ways and silently restyling each other.
- Font sizes are in **user units against the viewBox**. The floor is **1.10% of slide width** — for a
  1000-wide viewBox that is ~11px, and 8–9px labels are below it. `render_audit.py` measures what is
  actually rendered, because text sized in `rem`/`em` walks past every static check.
- Entities: use **numeric** refs (`&#8211;`), never HTML names (`&ndash;`). An SVG loaded through
  `<img src>` is parsed as standalone XML and a named entity makes it fail to render at all — one
  chart was silently a broken image for hours.
- A viewBox whose aspect does not match its container makes `object-fit` letterbox on top of the
  figure's own dead space. **Match the aspect, then measure the figure as a fraction of SLIDE width
  before and after.**

## 6 · Stacked overlays, and why anything is clickable at all

🟥 **Every `.ob-step` is a full-size layer, and an SVG-built slide therefore carries one full-size
`<svg>` per step — four on the Boolean NOT slide.** The topmost overlay is empty where the pointer is
and swallows everything beneath it, so `document.elementFromPoint` returns the `<svg>` **root** and
never the part inside. Measured: at the exact centre of a png insert, and at 560 probe points across
that slide, not one returned a child element.

Consequences, both mandatory:

- **Authoring:** do not add a full-size overlay that carries nothing. If a step only needs a box, it
  needs no `<svg>` at all.
- **Tooling:** anything that must select a part (the review overlay, any future picker) resolves it
  **geometrically** — smallest descendant whose screen box contains the pointer, walking down the
  `elementsFromPoint` stack when the topmost overlay is empty there, and preferring an `<image>` over
  the panel drawn behind it. Implemented in `review.js`; see `LESSONS.md`.

## 7 · Motion

🟥 **A hidden state carries `transition:none`. The fade lives on the shown state.**

```css
.<slideclass> .ob-reveal        {opacity:0; transition:none}
.<slideclass> .ob-step.shown .ob-reveal {opacity:1; transition:opacity .3s ease}
```

`autofit()` lights every fragment via `body.measuring` so it can measure a full slide. A hidden state
that *transitions* then animates back to hidden — the slide paints fully built and fades away, which
the room sees as a flash before the build starts. **33 rules carried this defect**, because the
original fix was a single line invisible from the next build class. Gated by `check_regressions.py`,
which also reads `frag_*.css` via `--css`.

## 8 · CSS specificity traps

- `.obuild .ob-pic img{position:absolute;inset:0;width:100%;height:100%}` **outranks a plain
  two-class selector**, so positioned component images get force-stretched and photographs distort.
  Use `.<slideclass> .ob-pic img.<component>` plus explicit `right:auto; bottom:auto`.
- `.ob-pic` has `overflow:hidden`. **A box clipped by it does NOT register as an escape** in
  `verify_build.py` — that defect shipped three times in one day. Read the render.

## 9 · Never less visual

*"NEVER less visual, but if possible GLADLY more visual should be the rule (and the gate!!!)."*

`slide_inventory.py --compare <baseline>` fails on any drop. The score counts **distinct image
sources**, not `<img>` tags — counting tags let a flat export used four times outscore a genuine
three-component rebuild, and the gate fired on real progress the first time it ran.

Four slides in one campaign deleted SDS's picture and replaced it with 2,400–3,750 characters of
prose. That is the failure this gate exists for.

## 10 · The gates, in one command

```bash
bash tools/preflight.sh [baseline.json]
python3 tools/box_collisions.py --deck deck.html      # box on already-revealed art
python3 tools/render_audit.py   --deck deck.html      # rendered type, occupancy, overprint
python3 tools/triage_fragments.py <scratchpad> --apply
```

And then **read the render**. Every tool here has a documented blind spot; `verify_build.py` prints
PASS while measuring nothing when it has no `--manifest`. The picture is the acceptance test.

---

## 11 · The review overlay is part of the visual contract

A slide nobody can select is a slide nobody can comment on, so `review.js` ships **inside this
skill** and its behaviour is specified here, not left to chance.

- **Comment mode persists** (`localStorage: gtreview:mode`) and **defaults ON**. It used to reset to
  false on every load, so a full-screen round trip or opening a comment from the history panel
  silently switched it off - hovering then does nothing at all and there is no symptom to see.
- **Selection resolves geometrically inside inline SVG**: smallest descendant whose screen box holds
  the pointer, walking down the `elementsFromPoint` stack when the topmost step-overlay is empty
  there, and **preferring an `<image>` over the panel behind it** because a cropped image's own rect
  is the unclipped source and would otherwise never win. Without this, an SVG-built slide is one
  undifferentiated click target - measured at 560 probe points.
- **The compose box always fits the viewport.** It is a flex column with
  `max-height:calc(100vh - 20px)`, the thread scrolls inside `.gtr-scroll`, the action row is
  `position:sticky` at the bottom, and after insertion the box is repositioned from its MEASURED
  height. The old code assumed every box was 200px tall, so a box with a thread hung off the bottom
  and SDS had to shrink the whole window to reach **Done**. Verified at 768px and 620px viewport
  heights, clicking at the very bottom of the slide: box fully on screen, Done visible, both times.
