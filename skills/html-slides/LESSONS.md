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
