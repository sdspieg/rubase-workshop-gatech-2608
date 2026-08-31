# Getting the GaTech workshop to Monday — scoped from the 76 review comments

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
