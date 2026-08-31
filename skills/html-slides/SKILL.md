---
name: html-slides
description: Build or repair SDS's HTML slide decks (GaTech workshop deck and its siblings) - rebuilding PowerPoint png-dump slides from the unzipped pptx /media assets, building slides up one component at a time with appearing/disappearing explanation boxes, making text-wall slides visual, and fixing small type and wasted screen. Use WHENEVER the task touches deck.html, a slide build-up, a "rebuild this slide", a review comment on a slide, or any HTML presentation in this house style. Carries four gates that refuse the defects that have already shipped once.
---

# HTML slides, the way SDS wants them

Every rule here has an incident attached, because a rule without its incident gets rationalised away.
All of them come from 2026-08-31, when a full day of "rebuilt" slides turned out to be the thing he
had rejected, and a fix that had been made once came back because nothing was watching it.

**Run the gates. Do not rely on remembering this file.**

```bash
bash tools/preflight.sh [baseline.json]     # all gates
python3 tools/slide_inventory.py --out /tmp/before.json    # baseline BEFORE you edit
```

---

## 1 · "Rebuilt" means composed from the pptx media

The pptx `/media` folder, unzipped (in the GaTech deck: `img/src2025/`, 194 files), holds the
**individual** images: each photograph, each diagram panel. A slide is rebuilt when it is **composed
in HTML from those assets**, with **every word set in the deck's own type**.

🟥 **Dimming the flat PowerPoint export and cutting `clip-path` windows in it is NOT a rebuild.** It
is a png dump with the old slide's title, captions and layout baked into a raster. His words:
*"Not rebuilt. Just a png dump."* · *"you HAVE the individual source images that you can just use!!!"*
**26 slides shipped that way and were reported done.**

`splice_frag.py` refuses a fragment whose plate and every reveal are the same file. If a component is
genuinely absent from the media folder, say so and draw it as inline SVG — never fall back to the
composite. **Identify assets by OPENING and LOOKING**; filenames tell you nothing.

## 2 · Never less visual. Gladly more.

*"You can ALWAYS use better visuals if you can find or generate them (please do!), BUT you can not
re-germanize my previous manual attempts to make them more visual. NEVER less visual, but if possible
GLADLY more visual should be the rule (and the gate!!!)."*

`slide_inventory.py --compare <baseline>` fails on any drop. The score counts **distinct image
sources**, not `<img>` tags — counting tags made a flat export used four times outscore a real
three-component rebuild, and the gate fired on progress the first time it ran.

## 3 · Type floor and screen real estate

Floor: **1.10% of slide width**. *"Too small font. Let's define a mandatory lower threshold."*

"Optimize SRE" usually means the defect is **inside the figure**. He said it three times on one slide;
the cause was a viewBox whose aspect did not match its container, so `object-fit` letterboxed ~60px
per side on top of the chart's own dead space. **Measure the figure as a fraction of SLIDE width
before and after, and quote both numbers.**

## 4 · The build grammar

One click = **one component of the picture + the box explaining it**; the previous box disappears. The
box goes where the *already-revealed* art is not. Boxes carry 2–3 sentences of real prose, never a
label. Markup:

```html
<section class="slide obuild myslide" data-t="…" data-sid="…" data-n="…">
  <div class="ob-pic">
    <img class="ob-comp c1" src="img/src2025/imageNN.png" alt="…">   <!-- a REAL component -->
    <div class="ob-step" data-frag="1">
      <div class="ob-note" style="--x:52%;--y:14%;--w:40%"><div class="k">…</div><div class="d">…</div></div>
    </div>
  </div>
</section>
```

`setFrags()` walks `[data-frag]` in document order — one `.ob-step` = one click; the value is ignored.
Only the current box shows, by CSS alone:
`.ob-step:has(~ .ob-step.shown) .ob-note{opacity:0;visibility:hidden}`

## 5 · Four traps, each of which has shipped a defect

- 🟥 **Hidden states carry `transition:none`.** `autofit()` lights everything via `body.measuring` to
  measure a full slide; a hidden state that *transitions* animates back to hidden, so the slide paints
  fully built and fades — *"flashes again before starting the animation"*. **33 rules carried it**,
  because the original fix was one rule nobody could see from the next build class.
- 🟥 **An inline SVG `<style>` is not scoped to its subtree.** Bare class names leak page-wide.
  Prefix every class per slide.
- 🟥 **`.obuild .ob-pic img` outranks a two-class selector** → positioned components get stretched and
  photographs distort. Use `.myslide .ob-pic img.component` + explicit `right:auto; bottom:auto`.
- 🟥 **A box clipped by the picture's own `overflow:hidden` is NOT an escape** to `verify_build.py`.
  It shipped three times in one day. **Read the render.**

## 6 · Verification

`verify_build.py --sid <sid> --shots /tmp/x` steps the slide at 1280/1366/1600 and reports overflow,
failed images and box-over-revealed-art. Then **read the PNGs**. DOM inspection is not verification
here, and neither is "the tool passed" — the tool's blind spots are listed above.

## 7 · Review comments are the spec

🟥 **Match a comment to its slide by `elText`, never by the slide number in its route** — numbers shift
when a slide is added or removed, and matching by number sent an afternoon's work to the wrong slide.
🟥 **Never truncate comment text when reading it** — a 400-character cut hid the second half of a
comment and lost a requirement.
🟥 **`review.js` replaces localStorage with whatever the server returns on page load.** Starting the
review server with an empty store and opening a page destroyed 25 comments. Check the store is
populated *before* starting the server. (Recovery, if it happens: `ldb_recover2.py` reads Chrome's
LevelDB directly — SSTable + write-ahead log + snappy, all implemented locally.)

## 8 · Concurrent editing

Agents never edit `deck.html`. Each writes `frag_<sid>.html` (+ `.css`) to a scratchpad;
`splice_frag.py` splices by `data-sid`, preserves the deck's own `data-n`, refuses png dumps, and
skips-and-reports rather than aborting the batch (it used to `sys.exit` on the first refusal and
silently drop every good fragment behind it).

House style: US English · entities `&middot; &ndash; &rsquo;` · no em-dashes in prose (NBSP + en-dash).

---

## 9 · How this skill improves, and why it cannot quietly un-improve

**The rule: a lesson is not learned until it is a check that runs, or an entry with its incident.**

When you learn something new here:

1. If it can be mechanically detected → **add it to `check_regressions.py` or `slide_inventory.py`**,
   with a test that proves it catches the real defect. Prose in a doc is the weak layer: today's flash
   rule was written down and violated by three separate authors including its own author.
2. If it cannot be → add it above **with the incident that produced it**, in one or two lines.
3. Append the date, the symptom and the fix to `LESSONS.md` in this folder.
4. Re-run `bash tools/preflight.sh` and commit the skill together with the code change.

**Nothing is ever removed from this file to make a task easier.** A rule that turns out to be wrong is
*corrected in place with its evidence* — as the visual metric was, when it proved to reward the very
thing it existed to block. Deleting a rule because it is inconvenient is the failure mode this section
exists to prevent.
