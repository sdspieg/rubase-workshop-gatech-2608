# Getting the GaTech workshop to Monday — scoped from the 76 review comments

> ## ⏰ UPDATE 2026-08-31 10:05 EDT — the build-up cluster, and how it is done now
>
> **The pattern is settled and tooled.** SDS's rule, stated three times before it landed: *parse the
> individual components out of the ORIGINAL picture and build THOSE, each paired with its own
> explanation box, one box on screen at a time, placed where the revealed art is not.* My two earlier
> attempts had redrawn the diagram as labelled rectangles — which builds correctly and throws away the
> picture he teaches from. Procedure, prohibitions and the measurement harness:
> [`SLIDE_BUILD_PATTERN.md`](SLIDE_BUILD_PATTERN.md).
>
> **Four slides done, all pushed and live:**
>
> | `data-sid` | Slide | How the components were obtained | Steps |
> |---|---|---|---|
> | `04c7c6` | The 'omics | cut from `img/orig/gt2025_omics-13.png` by `tools/decompose_figure.py` | 9 |
> | `lung01` | **Same organ, different disease** (NEW) | drawn — precision oncology vs war | 7 |
> | `d2l001` | **From epistemic darkness to light** (NEW) | the geomics figure's own 18 build layers | 7 |
> | `10f148` | Precision and recall | drawn, plus cover tiles cropped from the 2025 render | 8 |
>
> `10f148` closes both of its review comments: built up like the original PPT, and **the Russian
> examples restored** — Integrum 31,000 publications against CNA 700→144, monographs often >200,
> Jonsson 449, all reproduced from SDS's own 2025 slide.
>
> **Verification is mechanical, not visual-only:** `python3 tools/verify_build.py --sid <sid>` steps the
> slide at 1280/1366/1600 and reports overflow, failed images, and box-over-revealed-art collisions.
> `lung01`, `d2l001`, `10f148` PASS; `04c7c6` passes with three *declared* collisions at step 8.
>
> ### Still on the build-up list
> AlphaFold (`314842` — its image is an **832×93 sliver**, a real defect), strategic analysis 3.0,
> pub-centric → knowledge-centric, real-vs-our IR, RuBase name, and the two paradigm-shift tables.
>
> ### Deferred on purpose
> The GPT-5.6 Sol **Geomics session addendum** (ontological lock-in · theory-protective escalation ·
> phenotype-vs-mechanism). Substance agreed; its brief targets the Geomics Drive corpus, needs the
> Washington and Rush medical claims sourced first, and is half a day. Washington and Rush stay off
> today's deck.
>
> ### Record
> HANDOFF 2026-08-31 · Tana `FSrdiXCG91CL` (`#output` `#Claude` `#RuBase` `#method`)


> ## ⏰ STATUS AT 2026-08-31 03:40 EDT — DAY 1 IS TODAY, 11:00
>
> Measured against the live deck, the live site and the live comment store this morning.
>
> **The deck runs.** 133 slides, 349 build steps. Day 1 = s1–s42; Day 2 opens at s43. All five day
> blocks plus materials, glossary and programme are present. The rebuilt slides were stepped
> through on screen, not assumed.
>
> **Comment state: 36 addressed (28 of them verifier-backed), 44 open, 11 blocked on SDS.**
> Split by urgency, only **~24 open items touch today** — 11 on the Day 1 deck, 13 on home/#day1.
> The other 19 are Days 2–5 and have the week to land.
>
> ### The five worth fixing before 11:00, in order
> 1. **s8 — the "200 million" figure.** Hero-sized AND unsourced: Microsoft Academic shut down in
>    2021. A wrong number, displayed large, in a talk about rigor. Largest exposure in the deck.
> 2. **s18 — "Where are the two answers??!"** A slide that visibly promises what it does not deliver.
> 3. **s6 —** duplicates the previous slide's point.
> 4. **s9 —** needs its punchline.
> 5. **The QR code —** untested against the live URL; if it is on screen and dead, the room sees it.
>
> Everything else on Day 1 is an improvement, not a blocker, and several need SDS's input.
>
> ### 🟥 Still blocked on SDS and due TODAY
> **The Google Doc needs Share → Anyone with the link → EDITOR.** My tooling can only grant Reader.
> If participants cannot write in it, that is felt in the room this morning.
>
> ### Reversibility
> Both repos are pushed (`rubase-workshop-gatech-2608` 0f7fe47, `gt-workshop-review` 6c705fa), each
> decision a separate commit. The dead `GITHUB_PAT` no longer blocks pushes — `gh` holds its own
> working OAuth token — but it is still worth rotating for anything that reads the variable directly.


Measured 2026-08-29 against the live DOM and the comment store, not from memory.

## The finding that reshapes the plan

**All 28 deck comments sit on Day 1 slides (s5–s41). Zero on Days 2–5.** SDS reviewed Monday in
detail and has not reached the rest. Day boundaries in `deck.html`: Day 1 = s5–s41 (37 slides),
Day 2 opens s42, Day 3 s71, Day 4 s95, Day 5 s116–s129.

| Surface | Comments | Needed by |
|---|---|---|
| Day 1 deck + `#day1` + `#home` + `#program` | **51** | **Monday 31 Aug** |
| `#day2` … `#day5` pages | 25 | Tue–Fri, as the week runs |

Days 2–5 slides carry no comments at all, so they are not Monday work.

## Monday-critical, in order

### 1 · Correctness bugs participants will hit (~1h)
- **#11** Day 1 tells them to *"open the seed corpus"* — *"There IS no seed corpus yet!!! That's only Day 2!!"*
- **#64** s18 promises two answers — *"Where are the two answers??!"* — and never gives them
- **#13** the AlphaFold slide's bottom bullet is cut off and never visible
- **#51** the aphorism duplicates the previous slide's
- **#7** US English across every surface, every piece of text (mechanical sweep)

### 2 · Build-ups on Day 1 slides (~3–4h) — the largest cluster
14 requests, all Day 1: humors (viz then 4 bullets), 'omics, AlphaFold (viz then 4 bullets, all
visible), paradigm shifts **row by row AND cell by cell**, precision/recall built sequentially **with
the Russian examples restored**, strategic-analysis 3.0, pub-centric→knowledge-centric, real-vs-our
IR, RuBase name. Now protected by gate #158 against being re-flattened.

### 3 · Typography (~30m)
#49 the *"ATROCIOUS"* Foundations font · #54 the oversized *200 million* · #42 home strapline on two lines.

### 4 · Evidence refresh (~1h)
#21 and #4 want recent, **academic-search-based** data on query sophistication; #25 a current
peer-review-crisis figure; #22 re-run the LLM-uptake research with the same scripts/prompts.
Sources to be shown, not asserted.

## Blocked on SDS

1. 🟥 **Google Doc → General access → Anyone with the link → Editor.** Participants cannot write
   their RQ until this is set. This terminal cannot do it: `drive_share_file` grants
   anyone-with-link **reader** only, and the Drive OAuth returned `invalid_grant`.
2. **The human-vs-AI slides** (#65) — "we have been using these in recent presentations". Name the
   deck and they can be pulled from the genealogy.
3. **The policy-myopia paper** (#27) for the animal-deterrence / criminology / public-health angle.
4. **Four judgment calls**, not chores: is deterrence the best worked case (#26); is 35 min right
   for two worked taxonomies (#28) and for the neighbor swap (#30); and #41 — refocusing
   Foundations on IR's pathologies and *"where's the vaccine for war and conflict?"*, which is a
   real reshape of Monday's argument, not an edit.

## Deliberately not Monday work

Days 2–5 slides · resource wiring (#15, #17, #29, #36, #38) · the §6 three-corpus numbers · s76,
the last remaining visual candidate.

## Standing rule for this work

**Read the slide's comments before touching the slide, and keep every build-up.** A visual goes in
alongside the reveal, never instead of it. Enforced by gates #158 and #159 rather than intention.

---

Tana: node `F7wuxGh_0jKD` (2026-08-29, HCSS). HANDOFF entry under 2026-08-29.
