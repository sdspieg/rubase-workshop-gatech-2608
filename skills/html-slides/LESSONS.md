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
