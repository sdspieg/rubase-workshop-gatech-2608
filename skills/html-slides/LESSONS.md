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
