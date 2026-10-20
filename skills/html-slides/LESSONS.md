# Lessons ledger — append only, never prune

One line per lesson: the date, what went wrong, and where the fix now lives. A lesson with no
enforcing check is a lesson that will be unlearned; the "enforced by" column is the point.

| date | what went wrong | enforced by |
|---|---|---|
| 2026-08-31 | "Rebuilt" 26 slides by dimming the flat pptx export and cutting clip-path windows. Reported done. It is a png dump. | `splice_frag.py` refuses plate==reveals |
| 2026-08-31 | Build-up flash, fixed once, reintroduced by every new build class: a hidden state that transitions animates back to hidden after `body.measuring`. 33 rules. | `check_regressions.py` FLASH |
| 2026-08-31 | Inline SVG `<style>` is not scoped; `.hd` etc. defined 4 different ways across SVGs, restyling each other. | `check_regressions.py` SVG COLLISION |
| 2026-08-31 | Sub-floor type; SDS asked for "a mandatory lower threshold". | `check_regressions.py` FONT FLOOR, 1.10cqw |
| 2026-08-31 | Visual gate counted `<img>` tags, so a flat export used 4× outscored a real 3-component rebuild and it failed on progress. | metric counts DISTINCT sources |
| 2026-08-31 | Matched a review comment by slide NUMBER instead of its `elText`; fixed the wrong slide. | rule §7 — no mechanical check yet |
| 2026-08-31 | Truncated comment text at 400 chars when reading the store; lost the second half of a requirement. | rule §7 — no mechanical check yet |
| 2026-08-31 | Started the review server with an empty store; `review.js` load() replaced localStorage and destroyed 25 comments. Recovered from Chrome LevelDB. | rule §7 + `ldb_recover2.py` |
| 2026-08-31 | `splice_frag.py` called `sys.exit` on the first refused fragment, silently dropping every good fragment behind it. | skips and reports at the end |
| 2026-08-31 | `verify_build.py` reports 0 escapes for a box clipped by the picture's own `overflow:hidden`. Shipped 3×. | rule §5 — read the render; no check yet |
| 2026-08-31 | `.obuild .ob-pic img` outranks a two-class selector; positioned components get stretched and photos distort. | rule §5 — no check yet |
| 2026-09-01 | Opened six new browser windows in one session instead of reusing the one already on his desktop. | rule CLAUDE.md section 8 - no check yet |
| 2026-09-01 | Four Day-2 slides printed an explanation box over 91-100% of labels, logos and diagrams the room had already been shown. | `box_collisions.py` (no manifest needed) |
| 2026-09-01 | `verify_build.py` prints PASS while measuring NOTHING when it has no --manifest; every slide in a 34-agent campaign passed that way. | `box_collisions.py` + read the render |
| 2026-09-01 | 26 slides rendered text below the floor; the static checks read cqw and SVG px only, so rem/em walked past. | `render_audit.py` measures the RENDERED size |
| 2026-09-01 | The query line rendered as "( OR ) AND (...)" - both quoted phrases computed to position:absolute and landed at the same point. | rule VISUAL_SPEC section 8 |
| 2026-09-01 | An SVG chart used HTML named entities and silently rendered as a broken image. | rule VISUAL_SPEC section 5 - numeric refs only |
| 2026-09-01 | Comment mode reset to OFF on every page load, so hovering did nothing and there was no symptom to see. | review.js remembers it, defaults ON |
| 2026-09-01 | Every build step carries a FULL-SIZE svg overlay, so hit-testing returned the svg root at all 560 probe points and no part of an SVG slide could be selected. | review.js resolves geometrically; rule VISUAL_SPEC section 6 |
| 2026-09-01 | check_regressions invented 53 SVG collisions by matching "<svg>" inside a CSS COMMENT and swallowing the stylesheet. | scoped per section |
| 2026-09-01 | The compose box was placed with a hardcoded 200px height guess, so Done hung off screen and he had to shrink the window. | measured-height repositioning + sticky action row |
| 2026-09-01 | 636 of 798 elements on 99 slides were unreachable by the pointer: full-size .ob-step layers plus inset:0 component images. Fixed per slide three times before measuring. | deck CSS + universal resolver + `reach_audit.py` |
| 2026-09-01 | The comment toggle looked the same in both states and its type was too small to read. | red OFF / green ON, 15px bold, state written in words |
| 2026-09-01 | Slides written in instructor voice ("Ask the room to guess...") - stage direction printed where the student reads. | rule SKILL.md 4b - move it into data-n |
| 2026-09-01 | A slide was re-argued without reading its own data-n and lost the point it existed to make. | rule SKILL.md 4b - read the notes first |
| 2026-09-01 | A slide asked the room a question with the answer already printed at the bottom. | rule SKILL.md 4b - the answer arrives on a later step |
| 2026-09-02 | Worked examples across the deck never named their topic - a 3-D taxonomy figure, two blind generations, a Red Lines case. | rule SKILL.md 4c - no check yet |
| 2026-09-02 | A deliberately empty chart ("guess first") read as a bug: "Why are these empty?" | rule SKILL.md 4c - say that you are withholding |
| 2026-09-02 | Two Day-3 comments would have gone to the WRONG slide by number - a slide had been inserted since. Matched by elText instead. | rule SKILL.md 7 |
| 2026-09-02 | A DIKW pyramid rebuild dropped the original's "top-2-only" red line; a wordmark rebuild dropped three original bullets. Both "looked rebuilt" but were never checked against the source. | rule SKILL.md 4d - no check yet |
| 2026-09-02 | A rebuilt pipeline/pyramid appeared all at once instead of building step by step, on a slide that clearly needed it - across three separate decks, this is the single most-repeated correction (15+ instances). | rule SKILL.md 4d - no check yet |
| 2026-09-02 | review_server.py's write_store() used one literal ".tmp" filename; two concurrent autosave POSTs (comment text + author name) raced on it, one lost FileNotFoundError, surfaced as "server write failed". | tmp filename now unique per-thread (pid+thread id) |
| 2026-09-02 | review.js's "prefer an image under the pointer" rule unconditionally beat an .ob-note that geometrically overlapped a full-inset picture - 31 of 69 visible note/image targets unreachable on one deck. | resolveTarget() now returns an .ob-note over any image match |
| 2026-09-02 | A closing `.ob-scrim` step on a MULTI-COMPONENT build (pyramid, pipeline, spiral) triggers `.slide:has(.ob-step:last-child.shown .ob-scrim) .ob-step:not(:last-child){visibility:hidden}` and wipes out the ENTIRE accumulated diagram, not just dims a picture. Correct for a single-image chart slide; wrong for anything built up over multiple steps. Shipped on 6 slides, survived box_collisions.py/verify_build.py/per-step screenshots, only caught by SDS clicking through the TRUE final state live. | no mechanical check yet - box_collisions.py/verify_build.py need a mode that reveals ALL frags at once (not per-step) and flags any `.ob-step` losing >0 rendered content when the scrim step is added |

## 2026-09-02 – the review store is SHARED across decks and falls back to local-only

**Symptom.** Asked to open a deck in feedback mode, I checked the comment store first and found
`generic_deck/comments.json` holding a comment keyed `page: "index.html#2"` – a comment about a deck
SDS had already rejected, sitting where a different deck would load it. `review.js` pushes the server's
store into localStorage on page load, so opening the new deck would have adopted the wrong deck's
comments.

**Cause, from reading `review_server.py::_pick_store()` rather than inferring it.** The store path is
resolved to a **hardcoded GaTech location**, `RuBase/Workshops/2026/GATech/OFFLINE-REVIEW/comments.json`,
so **every deck that runs this server writes into the same file**. When that path is absent – which is
the case for any other deck – it falls back to `ROOT / "comments.json"`, **local, beside the deck, not on
Drive**, under a comment reading *"never fails to run"*.

***That fallback is the defect, not a safety net: it is the branch that silently produces an unsynced,
deck-local store.***

**SDS's rule, 2026-09-02:** *"make sure every slidedeck has a separate (AND persistent  –  meaning copied
to gdrive!) folder!!!"*

**The fix (specified, not yet implemented – awaiting his go):**

1. **One store per deck, on Drive:** `<deck>/review/comments.json`, resolved from the deck's OWN
   directory, with the deck name embedded so a mismatched store is **detectable rather than silently
   loaded**.
2. **Refuse rather than fall back.** If the resolved store is not under Drive, stop and say so. *A
   review server that always starts is worse than one that refuses, because the failure is invisible
   until the comments are gone.*
3. **Migrate** the existing 530-byte comment to the GaTech store it belongs to.

**Related:** the skill already warns that starting the server with an empty store destroyed 25 comments.
This is the same wound from the other side – starting it with the WRONG store.

- 2026-09-15: FutureBase economy slide repair copied the app’s mean-line SVG faithfully but selected the wrong app view. The user wanted category distributions with years down the vertical axis, one parameter per slide. Match the named view, axis orientation and visual encoding before proving numeric fidelity. The new year-row QA asserts seven parameter slides, ordered vertical years, all shares/counts/missing states and exact rendered category colors. A primitive-count decline from scatter marks to requested distribution bars is documented, not disguised with decorative marks.

## 2026-09-16 · A deck that measured fine and looked broken

**Symptom.** SDS, twice: *"It's still VERY poor use of the screen real estate!!! Look for yourself!!!
Why are you so bad at this now when the last slidedecks were MUCH better?!?!?"* and then *"you
CLEARLY also didn't visually double-check all animation buildup snapshots because there are LOADS of
issues still."* Both were right. A 21-slide deck passed `check_regressions`, `slide_inventory`,
`box_collisions` and a hand-written geometry sweep, and was still cramped and empty at once.

**What the images showed when they were finally read.** 21 agents read all 58 build-step PNGs:
**15 slides BROKEN, 6 MINOR, 0 clean &ndash; 98 defects, 34 of them high severity.**
Wasted space on **every one of the 21 slides**; overlaps on 14 of them, after overlaps had already
been "fixed" twice.

**Root cause of the layout half.** To stop boxes covering art I invented a rule &ndash; all art into
the TOP band, every box pinned to the bottom band. It removed the overlap and left the middle and
bottom of every slide empty. ***A fix that trades one defect for a worse one is not a fix, and
nothing was measuring the second one.*** Two further blunt global y-scalings made some slides better
and others worse: `p0a003` and `p0a019` went from deadband 0.23 to 0.27. **Three global transforms in
one session, each fixing one defect and seeding another &ndash; the signal that a slide needs hand
layout, not another scale factor.**

**Root cause of the process half, which matters more.** SKILL.md &sect;6 says *"Then read the PNGs.
DOM inspection is not verification here, and neither is 'the tool passed'"*, and the house rule says
*"NEVER VERIFY VISUAL WORK VIA THE DOM. ALWAYS EYEBALL A MEDIUM-RES PNG."* I read about six images
all session and measured geometry for everything else. **Every defect SDS caught was sitting in a PNG
I never opened.** The rule existed, the file was loaded, and I substituted a cheaper check for the
required one.

**Fix: `tools/sre_audit.py`** &ndash; coverage, vertical span, horizontal span, the tallest dead
horizontal strip, and text escaping its own container rect. It refuses to pass on an empty
measurement, and carries `--present` because the windowed view flatters the layout (the sidebar hides
the waste).

🟥 **And the gate has a demonstrated blind spot, recorded here rather than discovered later.** It
measures the FULLY BUILT state only. On "The problem" the explanation box is pinned at a fixed y, so
step 1 is one thin row with ~30% of the slide empty beneath it &ndash; and the built state is the one
step where that gap closes. **The new gate would have passed it.** Reading the images caught it. A
per-step sweep is the next extension; until it exists, the images remain mandatory.

## 2026-09-16 · render_audit passed on a deck it never loaded &ndash; and the fix was then overwritten

**Symptom.** `render_audit.py` printed `0 slides measured at 1366px ... 0 below the floor ...
0 overprinted` on a new 5-slide deck and exited clean. Every count was zero because nothing was ever
in the DOM, and the summary is indistinguishable from a real pass.

**Cause.** It navigated to a hardcoded `file://{deck}#13`. The deck routes `#N` to `showDeck(N-1)`,
so on any deck with fewer than 13 slides the route fell out of range and no slide was cloned out of
`<template id="deck">`.

**Fix.** Navigate to `#1` and **assert the slide count**, exiting non-zero rather than reporting a
pass on an empty measurement. *A gate that can silently measure zero is worse than no gate.*

🟥 **This fix was silently lost once already, and the cause is the opposite of what it looked
like.** It was first read as one session's whole-file mirror to the Drive master clobbering another's
edit. **The ledger does not support that**: across 03:33&ndash;10:14 UTC on 2026-09-16 no tool call
wrote `render_audit.py` in either location. What actually happened is simpler and worse. The fix was
applied to `~/.claude/skills/html-slides/` &ndash; **the CACHE** &ndash; and never mirrored to the
Drive master. At 07:54 UTC `sync-llm-instructions.sh` ran from `~/.profile` and copied the master,
still carrying `#13`, file-by-file over every CLI skill directory. Its own source comment says so in
plain words: ***"EDIT THE GDRIVE COPY, never the local one (local is a cache and gets overwritten)."***

**So the rule is the reverse of "append, never mirror".** A skill fix that exists only in
`~/.claude/skills/` is not a fix; it is a change with a scheduled expiry, and the login sync is what
collects it &ndash; silently, with no failure, no log line and no diff. **Mirror any skill edit to
`$GDRIVE_ROOT/claude-skills/<skill>/` in the same breath as making it**, ideally by running the
skill's own `install.sh`, which deploys to all three CLIs and the master together and cannot forget a
file the way a hand-picked `cp` list can &ndash; that hand-picked list is exactly how this one was
missed, since the mirror that afternoon carried `SKILL.md`, `LESSONS.md` and `sre_audit.py` and not
this file. When two sessions really are in the same file at once, apply the same targeted edit to
both copies rather than copying one over the other.

🟥 **And two verification traps that each reported the opposite of the truth**, hit twice in ten
minutes while checking this very fix: `grep -c 'deck}#1'` **matches `deck}#13` as a substring** and
reports the defect as fixed; and `grep -c 'refusing to report a pass'` returns **0** against source
where the formatter split that string across two lines. **Grep for an anchored or unsplittable
fragment and print the actual line**, never trust a count. 🟥 **A third instance landed the same
afternoon** &ndash; a grep reporting this very lesson as ABSENT from `LESSONS.md`, because it searched
for its author's own wording rather than the text that was actually there. Three confident wrong
answers in one day from the same move: ***the habit is the defect, not the pattern. Read the lines;
do not count them.***

**Two more from the same deck.**
`.ob-pic` carries `overflow:hidden`, so a box running past the bottom of the picture is **clipped
without overflowing the slide**: a DOM overflow check on the slide box returned `[]` while the render
plainly showed the last box cut in half. Measure against the `.ob-pic` rect, not the slide rect.
Root cause was VISUAL_SPEC &#167;5 &ndash; a viewBox aspect of 2.13 in a container of 2.47.

And `page.goto()` to a URL differing **only by its hash is a no-op**, so a verification ran against a
cached earlier build while reporting on the new one. Cache-bust with a query parameter and assert the
DOM slide count matches the file before trusting any result.

## 2026-09-16 (later) &middot; Fixing the deck: what the per-step audit found, and four traps in the tooling

**The defect, finally measured.** Every `.ob-note` in a 21-slide deck carried **one hardcoded
`--y:65%`**, while the art ended anywhere between **28% and 64%** of the picture box. On step 1 of
most slides the gap between the art and its explanation was **32&ndash;50% of the slide**. On the
FINAL step it closed to 0.5&ndash;15% &ndash; which is exactly why a built-state-only audit passed the
deck. Fix: measure each step's rendered art and give that step's note its own `--y`. That is a
per-slide measurement, not a global transform; `tools/` now carries the two-pass script.

🟥 **`preserveAspectRatio` means the viewBox tells you nothing on its own.** Art at viewBox
`y=24..113` of `0 0 1000 406` is not "at 28% of the slide" &ndash; the SVG is letterboxed inside
`.ob-pic` and the two are different coordinate systems. **Measure the rendered rects.**

🟥 **Enlarging art invalidates every note position on that slide.** Growing three boxes from 89 to
226 units moved the art bottom from 28% to 62%, and the notes computed against the old extent then
sat ON the figure. Re-run the reflow after ANY art change &ndash; and the clamp that stops a note
sliding too low is the thing that will bite: at `min(y,70)` an amplified chart ran straight under its
own note.

🟥 **A slide-splitting script must keep the preamble.** Splitting on `<section class="slide"` and
rebuilding from the pieces DROPPED everything before the first section &ndash; the head, the CSS and
the whole app shell. Every `id=` went with it, `showDeck()` threw on a null `#home`, and the deck
rendered zero slides. **Assert the id set, the slide count and the file size before writing**, and
keep a backup. That is now in the script.

🟥 **Two of my own metrics disagreed and I could not tell which was right.** `getBBox()` (SVG user
units) reported **0** text overflows where the audit's `getBoundingClientRect()` reported **20**. The
audit's `vis()` also does not walk ancestors, so it counts text inside build steps that are not on
screen. Until that is reconciled the overflow COUNT is not trustworthy &ndash; the image is. A count
never tells you which string to shorten anyway.

🟥 **Waiting on a log file that survives the previous run reads the previous run.** Twice I concluded
a rebuild had finished by grepping `PASS -|FAIL -` in a log the new run had not written yet, and once
read a screenshot the next run had already deleted. Wait on an artifact **newer than the input**
(`[ out -nt deck.html ]`), and never let two render chains run at once &ndash; they delete each
other's PNGs mid-write.

🟥 **`python3 -m http.server` is single-threaded**, so Chrome's keep-alive connections queue behind
one another, the deck's scripts never load and `goto` hangs forever. Two runs died this way before a
one-line server log (one request, no subresources) gave it away. Use `ThreadingHTTPServer`.

**Result of this pass, measured:** states with a hole >0.17 **9 &rarr; 3**; mean hole **0.112 &rarr;
0.071**; mean coverage **0.496 &rarr; 0.554**. Honest boundary: mean deadband went **0.136 &rarr;
0.166**, because moving a note up off a mid-slide hole leaves a trailing gap below it. That is a
better defect than a hole, not the absence of one, and the slides whose art is genuinely too small
still need their figures redesigned rather than repositioned.

## 2026-09-17 &middot; The audit was wrong in both directions, and a whole defect class had no check at all

**A gate that reports a pass is not evidence.** Three metrics in `sre_audit.py` were repaired this
day, each after it had confidently reported something the render contradicted. All three repairs are
now pinned by `tests/test_sre_metrics.py` against `tests/fixtures/overflow_hole_cases.html`, which
carries the REAL failing shapes. Two earlier "fixes" each traded one defect for a worse one precisely
because nothing pinned the right answer.

🟥 **`getBoundingClientRect()` returns a layout box even when an ancestor clips the element away.**
`.ob-pic` is `overflow:hidden`, so an element positioned past its edge reports real geometry and
paints nothing. `hole` therefore reported **0.392** on a slide where a pixel sample of that exact band
found **zero** non-background pixels. Every candidate is now intersected against each clipping
ancestor (`clipOf`) and dropped if it survives to nothing. This is the SKILL.md &sect;5 trap, found
inside the gate that exists to catch it.

🟥 **"Starts to the left of" is not "contains".** The overflow check first UNDER-reported, because its
`inside` test checked left, top and bottom but never the text's RIGHT edge. The rewrite then
OVER-reported: it let any box that merely began left of a text be that text's host and picked the
narrowest, so a row of five sibling cards qualified for each other's labels and **p0a011 scored nine
overflows while rendering perfectly**. A host must contain the text's left edge AND hold its vertical
mid-line; anything else is a neighbour.

🟥 **The worst defect of the session was caught by NO metric.** Two `<text>` elements printing through
each other rendered as `bftfc79Mdny na2ts4l5%ce by arm`, and superimposition is not an overflow &ndash;
nothing escapes a container &ndash; so the spill check is structurally blind to it. A new **`collide`**
metric closes that, and on its first run against the deck it found **seven more** that had survived
every previous read, including a callout on `p0a005` I had looked at repeatedly. ***The wrong
expectation in the first draft of the test is what exposed the gap, so it is recorded in the test
rather than quietly corrected.***

🟥 **Area ratio is the wrong statistic for overlap.** An SVG `<text>` box carries the font's full
ascent and descent, so a 40px number stacked under its own 19px label overlaps that label by half its
area while rendering perfectly. Keying on **baseline coincidence** (`vertical overlap / min line
height > 0.6`) separates a true superimposition from ordinary tight leading; the clean shapes are
fixtures now.

**The clean fixtures matter more than the broken ones.** A gate that flags nothing reports a pass, and
a pass is what everyone acts on.

## 2026-09-17 (later) &middot; A deck shipped broken while the audit said PASS. What that cost, and the gate that now prevents it

SDS: *"MASSIVE regression!!!! HUGE amount of overlap. Explain to me how you possibly could NOT
visually inspect everything before giving it to me. We must have MULTIPLE VERY FIRM gates on that!!!"*
and *"make it 100% IMPOSSIBLE"*.

**The mechanism, stated plainly: a PASS from a PARTIAL instrument was allowed to stand in for
looking.** `sre_audit.py` models space use, text spilling a rect, text-on-text collision and a rect
over text. It had **no model of the opaque `.ob-note` box covering the SVG art** &ndash; and the note
is exactly what `reflow_notes.py` moves on every edit. So the thing most disturbed by editing was the
one thing nothing measured, and the report said PASS with total confidence. Compounding it: one state
was read per edited slide rather than all 66, and the deck was mirrored BEFORE looking.

🟥 **The tool's own clamp was the root cause.** `reflow_notes.py` placed the note at
`min(artBot + gap, 76%)`, so on a slide whose art reached 88% the note landed **on** it. It now
REFUSES and names the slides whose art must shrink, instead of silently overlapping.

**Four defect classes had no check at all. Each is now one that runs:**

| check | what it catches | why nothing else could |
|---|---|---|
| `note_overlap_check.py` | the note covering the artwork | the audit has no model of the HTML note vs the SVG art |
| `crossstep` in `sre_audit` | one build step's art drawn on another's | every other metric looks WITHIN a single step |
| `svg_text_html_check.py` | `<em>` inside an SVG `<text>` | the text is simply ABSENT, and what is missing cannot be measured |
| `structure_check.py` | an `.ob-step` outside its `.ob-pic` | a browser silently repairs bad markup into a different tree than the one written |

🟥 **`<em>` inside an SVG `<text>` renders nothing AND swallows the rest of the line.** Five of them,
and **every one was an English gloss** &ndash; so the bug deleted precisely the translations the house
rule requires. Use `<tspan font-style="italic">`.

🟥 **One missing `</div>` turned every build step into a full-slide overlay.** A step extraction took
one closing tag too few; `.ob-step` is `position:absolute; inset:0`, so each became a direct child of
the section, permanently escaped its padding box, `autofit()` could never find a scale, bottomed out
at `--sc 0.5`, and painted the artwork over the title. Three separate probes said the geometry was
fine because they measured the repaired DOM.

🟥 **A detector that fires is not always wrong.** `crossstep` was assumed to be over-reporting and
was nearly loosened; the render showed it was right &ndash; three slides really were three layouts
stacked on each other. **Look before tuning a metric that disagrees with you.**

**The gate: `deck-ship-gate.sh` (10/10 tests).** `cp`, `rsync`, `git commit` and `git push` of a deck
are DENIED unless a receipt exists that is bound to the deck's exact sha256, records that EVERY check
passed, and records that EVERY rendered build state was acknowledged **by name**. Any edit voids it.
Verification attaches to the **bytes**, not the path, so mirroring verified content is allowed.

***It cannot force anyone to look. It makes not looking a deliberate false statement instead of a
quiet omission &ndash; which is the most a hook can honestly do.***

Two bugs in the gate itself, both of which DISARMED it rather than making it noisy - the dangerous
direction: whole-string matching fired on an unrelated segment, and `printf '%s' | while read` never
executed its body because there was no trailing newline. Both are fixtures now.

**Outcome, so the numbers are here and not only in a handoff:** the deck went out at **27 slides / 66 build
states**, every check PASS, all 66 rendered PNGs read and acknowledged by name, and md5-identical
(`89268af24907d88b1329bcb3838e5459`, 459,273 bytes) across Drive, `/mnt/c/Apps/` and the repo. 🟥 **The
receipt records a claim, not a fact about anyone's attention** — that is the honest limit of this design, and
the reason the acknowledgement is per state and by name rather than a single yes.

## 2026-09-23 · A new deck shipped under an old deck's screenshots

An eleven-slide replacement was deployed by `scp` after only the static preflight. Its copied
project directory still held the old, good deck's `qa/` PNGs. The verifier accepted arbitrary PNG
filenames from that directory; `preflight.sh` never invoked it; and the ship gate missed the actual
command because it recognised `cp/rsync/install` but not `scp`, read only `tool_input.command`, and
checked only `~/src/pasp-method-deck/deck.html`. Every layer pointed at the wrong evidence.

The repair is one chain. `render_steps.py` refuses an existing output directory and renders state 0
through final at four widths into a new run, with a SHA-256 for every PNG. `deck_verify.py` binds the
exact `deck.html` or `presentation.html` bytes to all required checks, the manifest, complete state
coverage, current PNG hashes, and one acknowledgement per state. `preflight.sh` invokes that workflow.
The ship hook resolves the actual sources from `command` **or** `cmd` plus `workdir`, including
relative paths and directories, and now catches `scp`; Git commit/push checks INDEX/HEAD bytes rather
than a convenient working-copy substitute. Regression evidence: 15/15 ship cases and 4/4 manifest
invariants, including the exact stale-qa and arbitrary-relative-scp failure.

## 2026-10-08 · No HTML deck had ever reached the genealogy

SDS asked for the new Monday AIRA decks to be *"added to our genealogy of all of my slidedecks"* and
whether the skill required it. It did not, and could not have: the archive updater
(`update_presentations_archive.py`) refused anything but `.ppt/.pptx`, so the genealogy stopped at the
PowerPoint era. Every HTML deck since August – GaTech, Yerevan, Baku, Almaty, PASP – was absent, and
the absence produced no error anywhere.

Fix: `register_html_deck.py` in the archive's `scripts/` (render fully built at 1600x900, image PDF,
PNGs, per-slide summary from the slide's own text, genealogy rebuilt over the whole archive with a
no-deck-lost check, SHA-256 ledger `_html_decks.tsv`), wrapped here as `tools/register_genealogy.sh`
and made a step of `preflight.sh`.

Two things the work itself turned up:
- 🟥 **The PowerPoint updater's single-deck path rebuilds the genealogy from `/tmp` and publishes it with
  `rsync --delete`.** On a machine whose `/tmp` does not already hold the full archive, that replaces
  the 43,088-slide genealogy with one covering only the decks in `/tmp`. The HTML path stages the full
  summary set first and refuses to publish unless every previously indexed deck is still present and
  the slide count equals the sum of pages over the worklist. Positive control before any write: the
  rebuild reproduced 43,088 slides / 4,558 families exactly.
- 🟥 **A renderer that refuses blank slides found four in a live deck** (ADA morning, the four slides
  after `gt24`). See the registration report for the diagnosis.


## 2026-10-09 · SVG text boxes are still German slides

The PASP NATO briefing passed the inventory's text-heavy check while almost every figure was a stack of prose cards drawn as SVG. SDS rejected it as “German slides in disguise” and asked for the documentation. The canonical [PowerPoint generation guide](https://drive.google.com/file/d/1Xlrbz1sNPwwaJ749Tzr6bRLUb51CXxWc/view) applies to HTML too: read it in full, alongside this skill. A shape count is not visual communication. Before accepting a slide, name the relationship encoded by its geometry (branch, contrast, dependency, quantity, sequence or evidence boundary); if removing the prose leaves no argument, redesign it. Retain a short current-step explanation and move detailed reasoning into speaker notes. The correction rebuilt the briefing with branching mechanisms, timeline contrasts, source-to-unit flow, parallel method paths and a parsed quotation. Full-state PNG inspection remains required; no primitive-count gate can certify this semantic judgment.

## 2026-10-10 · A deliberate overlay could not be declared, so the gate blocked a slide SDS had accepted

`sre_audit`'s CROSSSTEP check (art from a later step drawn across an earlier step's art) flagged the September
"The machinery of knowing has changed" slide (`ada-open`, reused in the AIRA Monday deck) 13 times: its dashed
"mislead" paths cross the library shelves on purpose – the crossing IS the metaphor – and their bounding boxes overlap
the shelves. There was no way to say "this overlay is deliberate" except loosening the metric. Fix: an element (or any
ancestor) may carry `data-crossstep-ok="<reason>"`; the reason must be at least 12 characters, and a bare or empty marker
exempts nothing. Fixtures `BAD-crossstep`, `CLEAN-crossstep-declared`, `BAD-crossstep-bare` in
`tests/fixtures/overflow_hole_cases.html`; `test_sre_metrics.py` 9/9. Use it only for an overlay that is the point of
the picture, never to silence a pile-up.

## 2026-10-10 · Renders taken before the photos decoded: empty picture slots read as defects

The eyes-on review of the AIRA Monday decks found photo slots EMPTY on ha-flashback, ha-back, ha-wonks, ha-eras and
lf-week – at some widths and not others (1440 clean, 1280/1366/1600 blank), with the same image present elsewhere. The
decks sit on the Google Drive mount, which serves files slowly, and `render_steps.py` screenshotted a fixed 220 ms after
each `setFrags`. A render that missed the image is not evidence of anything, in either direction. Fix: after each state,
`render_steps.py` waits until every `<img>` and SVG `<image>` on the current slide has decoded (cap 10 s), then two
animation frames. Verified by re-rendering the affected slides.

## 2026-10-11 · Page loads from the Drive mount exceed 30 s, and a timeout reads as a failed gate

On the AIRA decks (stored on the Google Drive mount) `deck_verify --force` reported sre_audit, render_audit,
note_overlap and box_collisions all FAIL – every one a `Page.goto: Timeout 30000ms exceeded`, not a measured defect.
Reading the analysis deck's 5 MB of images took 36–59 s at that moment; a minute later the whole page loaded in 8 s.
Fix: every tool's navigation timeout is now 180 s. A gate that times out has measured nothing – read the traceback
before treating a FAIL as a slide defect.

## 2026-10-11 · "Open it for SDS" means: signed in, on the review site, in front of him – then verified

A new AIRA deck was "opened" as a local `file://` copy: no review layer (the 💬 comment bar is injected by the review
server), and not the site SDS reviews on. When it was deployed, his Chrome was left twice at the basic-auth sign-in
dialog. SDS: *"what part of authenticated don't you understand! Look at my screen!!!!!"* His standing rule (system
instructions, 2026-10-04): sign him in, in the actual user-visible browser, and verify the protected page before handing
it over.

**THE method – use the tool, do not improvise:** `tools/open_authed.py URL [PORT=9224]` (in this skill since
2026-10-11; first used 2026-10-08). It connects to the BROWSER-level CDP websocket of the debug Chrome on **9224**
(the browser SDS has used with Claude all week), creates the tab with `Target.createTarget`, attaches, answers the
basic-auth challenge with `Fetch.continueWithAuth` (credentials from `CRED_FILE`, a dotenv file – never printed,
never in a URL, never typed), verifies title + review layer, and activates the tab. Then raise THAT window by its
title: `winfront 'AIRA week overview'` (the page title, not the URL). Then confirm from a screen capture before
saying it is open.

🟥 **What failed on 2026-10-11, in order, so nobody repeats it:** (1) a local `file://` copy; (2) `Start-Process`
on the URL – opens SDS's DEFAULT browser, not the debug browser, and lands on a sign-in dialog; (3) SendKeys into that
dialog – keys went nowhere (locked screen / wrong foreground); (4) a WSLg Playwright window – blocked by the window
gate, rightly; (5) Playwright `connect_over_cdp` to the 30-tab browser – hung 9+ minutes; (6) `PUT /json/new` +
`cdp_focus.py` – SDS: *"no you did not use the cdp debug browser that you've used before"*. The proven helper
existed in the session scratchpad the whole time; it was not looked up. **Before improvising a browser route, grep
this skill and the session for the route that already worked.** When `CRED_FILE` on the Drive mount is unreadable,
write a two-line dotenv Windows-side from `G:\My Drive\SYSTEM_CREDENTIALS.env` into `%TEMP%` and delete it after.

## 2026-10-12 · The genealogy registrar wedged itself, and three reviewed decks never shipped

- **What happened:** three AIRA Monday decks passed review and failed preflight on GENEALOGY only. `register_html_deck.py` deletes a
  re-registered deck's superseded render BEFORE rebuilding the index; when that rebuild refused (or was skipped with
  `--no-genealogy`), the published index still listed the deleted file, and every later registration refused with "previously
  indexed decks vanished". Each retry deleted one more render, so the refusal cascaded (1 → 2 → 4 decks).
- **Fix:** removals are journaled in `_PDF_archive/_retired_decks.tsv` before deletion; the rebuild treats journaled removals as
  expected and still refuses silent loss (scripts repo commit `5841312`).
- **Diagnosis rule:** preflight's genealogy step filters the registrar's output to a few prefixes; when it reports MISSING/STALE
  after "rendered_ok", run `register_genealogy.sh <deck>` unfiltered – the REFUSE line names the real cause.
- **Do not call `register_html_deck.py` directly:** the wrapper supplies `--title` from `<title>`; the direct call registered
  "hun-analyse deck" as the title. Re-register with `--force` to correct it.
- **Enforced by:** the journal in the registrar. No check yet that preflight surfaces the registrar's REFUSE line.

## 2026-10-12 · A live deck never hashes equal to its local build

- **What happened:** comparing live vs local md5 said every AIRA deck differed, including one the driver had just verified live.
  The review server injects a comment layer (`__GTR_USER__`, favicon, title prefix) into every served page.
- **Rule:** compare live and local with the injected lines excluded (or compare the file on the server by SSH, as the
  driver does). A raw HTTPS hash mismatch proves nothing.
- **Enforced by:** rule only – no check yet.

## 2026-10-20 — a deck cut from a SERVED page swallows the review layer

- **What happened:** both CENTREPEACE decks for Adam's Helsinki workshop were built from the review
  host. The presentation shipped with a `<link id="gtr-favicon">` speech-bubble icon and an inline
  `document.title = "💬 " + t` script **baked into the file**. Every check for the review
  layer passed, because `review.js` genuinely was not there and no review UI rendered - but the tab
  the Finnish hosts would open showed a comment-bubble favicon and a title reading as a review copy.
- **Why nothing caught it:** the glyph is written as an escaped surrogate pair, so grepping for the
  literal 💬 returns zero. The existing LESSONS entry about this injection was about *comparing
  hashes*, which cannot see what a rebuild swallowed.
- **Rule:** never cut a deck from a served URL; cut from the source file. The injected trio is
  `__GTR_USER__`, the favicon and the title prefix.
- **Enforced by:** `check_regressions.py::check_review_layer_captured`, with the real pre-fix artefact
  kept at `tests/fixtures/deck_review_layer_captured.html`. `body.present #gtr-bar{display:none}` and
  its siblings deliberately do NOT fail - those are the deck's own rules for hiding the bar when it
  IS injected.
- **Also found, not fixed:** the presentation inherits four inline-SVG class collisions from its
  source deck (`.zz-ax`, `.zz-big`, `.zz-cnt`, `.zz-lg`), left alone because Adam was presenting from
  the live URL at the time.
