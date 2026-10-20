---
name: html-slides
description: Build, verify, or repair SDS's HTML slide decks. Use whenever work touches deck.html, presentation.html, slide build-up, review comments, visual QA, or shipping an HTML presentation in this house style. The skill requires fresh hash-bound state renders and eyes-on approval before deployment.
---

# HTML slides, the way SDS wants them

Every rule here has an incident attached, because a rule without its incident gets rationalised away.
All of them come from 2026-08-31, when a full day of "rebuilt" slides turned out to be the thing he
had rejected, and a fix that had been made once came back because nothing was watching it.

**Run the gates. Do not rely on remembering this file.**

```bash
python3 tools/slide_inventory.py --deck deck.html --out /tmp/before.json  # BEFORE editing
bash tools/preflight.sh /tmp/before.json deck.html presentation.html
```

🟥 **`preflight.sh` is the shipping workflow, not merely a static lint.** It runs the full
hash-bound verifier for every named or discovered `deck.html` and `presentation.html`. A first clean
run deliberately stops after creating a **new** render directory and a PNG manifest covering state
0 through the final state at 1280/1366/1440/1600. Read every named PNG, acknowledge the exact list
with `deck_verify.py --eyes-on-file`, then rerun preflight. Only that second run can say
`PREFLIGHT OK`.

🟥 **Existing `qa/` images are never evidence.** A copied project can carry beautiful screenshots
of a different deck. The renderer refuses an existing output directory; the receipt binds the HTML
hash, manifest hash, every PNG hash, complete state coverage, all checks, and every per-state
acknowledgement. Any later HTML or PNG edit voids shipment.

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

Floor: **1.10% of slide width**.

🟥 **AND IT IS NOW A GATE: `tools/sre_audit.py`.** *"It's still VERY poor use of the screen real
estate!!! ... THIS HAS TO BE A GATE!!!"* (2026-09-16). Measures coverage, vertical span, the tallest
dead horizontal strip, and text spilling past its own container. Run it with **`--present`** &ndash;
the windowed view hides the waste behind the sidebar. It refuses to pass on an empty measurement.

🟥 **The gate does NOT replace reading the images, and cannot.** It measures the fully built state, so
a box pinned at a fixed y &ndash; leaving a third of the slide empty on step 1 and closing the gap only
on the last step &ndash; passes it. That exact defect shipped. **58 step PNGs were read by 21 agents
and found 98 defects, 34 high, on a deck that had passed every mechanical gate.** Render every step,
read every one. *"Too small font. Let's define a mandatory lower threshold."*

"Optimize SRE" usually means the defect is **inside the figure**. He said it three times on one slide;
the cause was a viewBox whose aspect did not match its container, so `object-fit` letterboxed ~60px
per side on top of the chart's own dead space. **Measure the figure as a fraction of SLIDE width
before and after, and quote both numbers.**

## 4 · The build grammar

**The complete specification of every visual element is [`VISUAL_SPEC.md`](VISUAL_SPEC.md) in this
folder** - the slide shell, `.ob-pic`/`.ob-step`/`.ob-note`/`.ob-scrim`/`.ob-plate` and their
contracts, the three component routes, the clip-path crop technique and why a cropped image's own
rect lies, inline-SVG rules (class prefixes, the type floor against viewBox, numeric entities),
the stacked full-size overlays and what they do to selectability, the motion rule, the two
specificity traps, and the gates. Read it before authoring or repairing any slide.

In short:

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

## 4b · Whose voice is the slide in, and did you read its notes?

🟥 **The slides are for the STUDENTS, not the instructor.** SDS, 2026-09-01: *"This is for
instructors. Reframe ALL of these instances throughout the deck!"* and, on the next one, *"Also
here: wrong framing. These slides are for the students - NOT for the instructor!!!"*

A line like *"Ask the room to guess…"* or *"This is where the room realizes…"* is **stage
direction**. It belongs in `data-n`, where the speaker reads it. What is ON the slide is what the
student reads. **Move it, never delete it** — appending to `data-n` keeps the delivery cue.

🟥 **Read the slide's own `data-n` BEFORE changing what it argues.** *"This is misframed. Make
sure you always read the notes of the original slides!"* Every rebuild that quietly changed a
slide's point did so because nobody read them first.

A related consequence for build order: if a slide asks the room a question, **the answer must not
be on screen when the question is** — he asked for the priming figure to arrive on a later step,
not to sit at the bottom of the slide giving the game away.

## 4c · Every example must say what it is an example OF

🟥 SDS, three times in one pass on 2026-09-02: *"But so what is the topic here? Hard to understand
the 3d without knowing what it's about!"* &middot; *"ALWAYS mention the actual topic whenever you give
examples, so students understand"* &middot; *"mention that this is from Red Lines! Double-check ALL slides
to make sure it is clear what topic the slides/examples are about."*

**A worked example with no named subject is a diagram of nothing.** Every figure, screenshot, table
and worked case names its topic ON THE SLIDE - not only in `data-n`, where the student cannot see it.
Find the real subject in the slide's own notes, in its neighbours, or in the source document; if it
genuinely has none, say so rather than inventing one.

The same instinct covers a related defect: a slide that deliberately withholds an answer must SAY it
is withholding. Six empty bars read as a bug, not as an invitation, until the slide asks the question
out loud.

## 4d · Build-up is the default, and fidelity to the original is VERIFIED, not assumed

Extracted 2026-09-02 from a cross-deck pattern analysis of 135 review comments across three decks
(the GaTech workshop deck, `generic_deck`, and a CNS/OSINT deck) — these are not one-off complaints,
they are the two most-repeated corrections SDS has given across every deck he has reviewed.

🟥 **Every `.ob-pic` slide builds up, unless it is genuinely a single static figure.** *"Build up!!!!"*
&middot; *"Needs to be built up - like I mentioned in the previous slide with explanatory boxes on the
current box appearing and the disappearing"* &middot; *"You TOTALLY messed up the build up. Make sure
ALL slides are 'built up'!!!!!"* &middot; *"NEEDS to be built up. ALWAYS. In ALL slides that have
pipelines like this one."* A slide that shows its whole figure on the first click, with only the note
text changing, has not been built up — every distinct component (a pyramid band, a pipeline stage, a
diagram box) is its own `.ob-step` reveal per the house grammar in §4, with the explanatory box
appearing and disappearing in step with it (already the `.ob-note` default — see §4/VISUAL_SPEC §2).
Default to build-up for ANY diagram with more than one identifiable component; a single indivisible
photo/chart with one caption is the only real exception.

🟥 **"Rebuilt to look like the original" is a VERIFIED claim, not a rendered guess.** *"DOUBLE CHECK
AGAINST THE ORIGINAL!!! ALWAYS!!!"* &middot; *"Whenever I ask you to replicate a ppt slide EXACTLY, you
SHOULD verify that's the case!!! ALWAYS."* &middot; *"THIS needs the three bullets on the right from the
original!!!"* &middot; *"Where are the two answers??!"* &middot; *"You cropped this very badly."* A
rebuild that captures the gist but drops a bullet list, an annotation, a red line, a second half of a
comparison, or the two-tone coloring of the source image has failed even though it "looks like a
rebuild." **The check is mechanical, not impressionistic:** open the actual source image/slide text
side by side with the new fragment and enumerate every distinct visual element in the original (every
bullet, every label, every colored line, every callout) before writing a single line of the rebuild;
after writing it, re-open the source and tick off that every element you listed is present in the
fragment. State in your own summary which elements you verified present, not just "rebuilt to match."
Missing this step, twice in one afternoon, produced a DIKW pyramid missing its "top-2-only" red line
and a wordmark slide missing three original bullet points — both had to be redone.

🟥 **Font sizes come from the shared CSS classes, never ad hoc per-slide values.** *"Is this
css-compliant? Make it the standard."* &middot; *"font-sizes on this slide seem different from the
other slides."* A slide-scoped override that happens to look fine in isolation still breaks the
deck's visual consistency; reuse `h2`, `.sub`/`.deck-sub`, `.kicker`, `.ob-note .k`/`.d` sizing rather
than inventing a new `font-size` for text that plays the same role as text elsewhere in the deck.

🟥 **No text overflow, ever.** *"NO OVERFLOW!"* Verified by `render_audit.py`, not by eye — a box
whose text visually looks fine at one viewport can clip at another; run the tool.

🟢 **Hyperlink and QR-code anything the audience needs to act on.** *"I'd hyperlink all of these"*
&middot; *"This slide needs a QR code for the Google Doc!"* A programme item, a resource list, a
dashboard reference, or a form the audience is meant to open: make it a real link on the slide (and a
QR code if the audience is in the room, not at a keyboard), not a URL typed in prose.

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

The deploy/commit gate resolves the **actual local source bytes** in `cp`, `scp`, `rsync`, `install`,
`mv`, `rclone`, and deck-repository `git commit/push` commands. It reads either `command` or `cmd`
plus `workdir`, handles arbitrary relative paths, and checks both canonical filenames. It never
substitutes one hard-coded project deck for the file being shipped.

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

## 8b · Every shipped deck enters the genealogy of ALL of SDS's decks

🟥 **Mandatory, and part of `preflight.sh`.** SDS, 2026-10-08: *"make sure they're added to our
genealogy of all of my slidedecks! Also check whether this is already part of the skill - if not add
it and make it mandatory."* It was not. The genealogy (Dropbox `Presentations/_PDF_archive/`, 1,162
decks / 43,088 slides / 4,558 reused-slide families as of 2 June 2026) was built only from
PowerPoint, so **not one HTML deck had ever reached it** – the GaTech workshop, the Caucasus and Central
Asia trip decks and the PASP method deck were all missing, and nothing said so. A deck nobody can find
the ancestors of gets rebuilt from scratch next time.

- `tools/register_genealogy.sh <deck.html>` renders every slide fully built, writes the PDF, PNGs and
  per-slide summary into the archive, rebuilds the genealogy over the WHOLE archive and refuses to
  publish it if any previously indexed deck vanished. Idempotent: an unchanged deck is a no-op.
- Registration is bound to the deck's **SHA-256**: after any edit the deck counts as unregistered.
- `preflight.sh` registers a deck automatically once its verification passes, re-checks with
  `register_genealogy.sh --check`, and **cannot print `PREFLIGHT OK` for an unregistered deck**.
- The archive exists only on the machine that holds SDS's Dropbox. Elsewhere the step fails closed;
  `HTML_SLIDES_GENEALOGY_SKIP="<reason>"` lets preflight pass and logs the skip to
  `~/.claude/state/html-slides-genealogy-skips.log` – register from the Dropbox machine afterwards.
- The renderer also refuses blank slides. Its first run found **four blank final slides in the live
  ADA morning deck** – see `LESSONS.md`, 2026-10-08.

Test: `tests/test_genealogy_gate.sh`.

## 9 · How this skill improves, and why it cannot quietly un-improve

**The rule: a lesson is not learned until it is a check that runs, or an entry with its incident.**

When you learn something new here:

1. If it can be mechanically detected → **add it to `check_regressions.py` or `slide_inventory.py`**,
   with a test that proves it catches the real defect. Prose in a doc is the weak layer: today's flash
   rule was written down and violated by three separate authors including its own author.
2. If it cannot be → add it above **with the incident that produced it**, in one or two lines.
3. Append the date, the symptom and the fix to `LESSONS.md` in this folder.
4. Re-run the skill tests and `bash tools/preflight.sh`; commit the skill with the code change.

🟥 **And step 4 is not optional, because the master is the source and your copy is a cache.**
`sync-llm-instructions.sh` copies `$GDRIVE_ROOT/claude-skills/<skill>/` over every CLI skill
directory on each WSL login &ndash; its own comment reads *"EDIT THE GDRIVE COPY, never the local one
(local is a cache and gets overwritten)."* On 2026-09-16 a fail-closed assertion added to
`render_audit.py` in `~/.claude/skills/` was collected by that sync and the tool went back to passing
on a deck it never loaded. **Run `install.sh`** &ndash; it writes all three CLIs and the master
together and cannot forget a file the way a hand-picked `cp` list can, which is exactly how that file
was missed. Enforced by gate #169.

**Nothing is ever removed from this file to make a task easier.** A rule that turns out to be wrong is
*corrected in place with its evidence* — as the visual metric was, when it proved to reward the very
thing it existed to block. Deleting a rule because it is inconvenient is the failure mode this section
exists to prevent.
