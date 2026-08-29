# Deck visual remediation — the "German slide" pass

**Standard applied:** SDS's own
`STEPHAN_POWERPOINT_STYLE_GUIDE_V3_COMPLETE.md` — *"a strong aversion to 'German
slides'… If a concept can be explained with a graphic instead of a sentence, the
graphic is always the preferred choice."*

## Method

Three routes, in order of preference:

1. **Recover the original.** Most of these slides began life as a picture and
   decayed into prose across deck generations. The slide genealogy index
   (`_slide_genealogy/slide_index.tsv`, 43,088 slides, near-duplicate clustered)
   locates the best surviving version of each family; the source PDF is then
   rendered at 200 DPI and downscaled to 1800 px.
2. **Generate a diagram** where the original visual was good but carried data SDS
   had already rejected, or where no original exists.
3. **Leave it** where the words genuinely *are* the content.

## What changed

| Slide | Before | After | Route |
|---|---|---|---|
| s97  | 208w | original render | genealogy |
| s100 | 193w | original render | genealogy |
| s15  | 176w | original render | genealogy |
| s16  | 164w | original render | genealogy |
| s76  | 159w | original render | genealogy |
| s103 | 147w | original render | genealogy |
| s110 | 146w | original render | genealogy |
| s20  | 162w | `img/viz/query_sophistication.svg` | generated |
| s55  | 127w | `img/viz/or_sets.svg` | generated |
| s12  | 182w | `img/viz/geomics_layers.svg` | generated |

### The generated three

- **s20 — query sophistication.** The original was a good donut but plotted
  numbers SDS had rejected. Charts the PubMed operator distribution instead: AND
  11.2%, OR 1.3%, NOT 0.2%, so OR and NOT render as slivers – which *is* the
  argument. Median 3 terms, 62.75% single-query sessions, 92.7% systematic-review
  error rate as the closing box.
- **s55 — OR.** Three set diagrams: AND narrows, NOT excludes, OR is the only
  operator that grows the set.
- **s12 — geomics.** No original exists; the genealogy's 137 "omics" hits are all
  *geo-econ**omics*** substring collisions. Drawn as two horizontal pipelines.
  The encoding comes from the slide's own argument: biology's four measured
  layers carry **solid** arrows because the central dogma is known; the
  conflict's four carry **dashed** ones because IR has no central dogma and the
  cross-layer structure is estimated. The "one honest difference" card is now a
  property of the picture rather than a paragraph about it.

## Two corrections worth keeping

- **`geomics` is not a typo.** It is SDS's coinage (geomics.org). It had been
  flagged for "fixing"; it stays.
- **The deck has 128 slides, not 74.** The audit regex matched `class="slide"`
  exactly and silently skipped every section carrying a second class, so 58% of
  the deck was audited and slides were then navigated *by those wrong numbers* –
  which is what produced spurious `0x0` and `NO IMG` measurements. Audits now
  run against the live DOM and address slides **by title lookup, never by
  ordinal**.

## Verification

Driven through the deck's own navigation and build controls, not by forcing
`.on` classes (which bypasses layout and measures every image as `0x0`). Each
slide: image `complete && naturalWidth > 0`, and its rect inside the slide rect.
All placed images `fits`. The first geomics build overflowed at 2.12:1 and was
re-laid-out to 2.81:1 – images here are inline-styled `width:100%` with **no
height clamp**, so aspect ratio is the only thing keeping them in the box.

## Boundary

**Three text-heavy slides without a visual remain**, down from 72: s75 *Why they
matter for cumulative knowledge* (117w), s56 *Proximity – AND with a distance
limit* (112w), s112 *The number we still do not have* (110w). s56 and s112 are
arguably slides where the prose is the content; s75 is a genuine candidate.

## Presentation mode

The review comment toolbar was floating over the slides at z-index 2147483000,
which is why fullscreen felt wrong. It now hides under `body.present` and
`:fullscreen`. `F` toggles both ways, `Escape` exits, and a `fullscreenchange`
listener re-syncs if fullscreen is left via the browser.

## Record

- Tana: node `oPcCeoWaM0tU` (2026-08-29, HCSS) – `#output` `#Claude` `#lesson-learned`
- HANDOFF: entry under 2026-08-29 in `HANDOFF.md`
- Repo: `rubase-workshop-gatech-2608`, pushed
