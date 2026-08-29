# What of the 'omics ↔ IR brief is actually in the deck

Coverage audit of [`OMICS_IR_ARGUMENT_BRIEF_2026-08-29.md`](https://drive.google.com/drive/folders/1Ut6e-mMDTb2j_MyLSNGIDyahhkcz2BPj)
(claude.ai web session, 2026-08-29) against the deck at commit `a43d45e`.

**Method:** 37 probes, each a distinctive string from the brief, matched against the rendered
text and the `data-n` speaker notes of all five HTML files. Measured, not recalled.

## In — and almost all of it is speaker notes

| Point | Section | Lands as |
|---|---|---|
| Black bile does not exist; survives in *melancholia* | staged | s10 note + visible |
| Tetrad imported from Empedocles/Alcmaeon, not derived | staged | s10 note |
| *On the Nature of Man* not the internal consensus; won via Galen | staged | s10 note |
| `contraria contrariis curantur`, the six non-naturals | staged | s10 note |
| Ended by Pierre Louis counting bled vs unbled pneumonia patients | staged | s10 note |
| 'omics dating: 2003 / 2007 / 2005 / 2013 / 2020 | staged | s11 note |
| "Younger than most of the people in this room" | staged | s11 note |
| The Sanger-1977 guard against overclaiming | staged | s11 note |
| `warm` → `hot and moist` (restores the hot/cold × wet/dry grid) | staged | **visible** |
| `leaderly` → `commanding` | staged | **visible** |
| Punchline split into its own sixth fragment | staged | **visible** |

Everything here comes from `DECK_SLIDES_7-8_CLAUDE_WEB_2026-08-29.md`, i.e. the *staged edits*
file – not from the argument brief.

## Out — the entire argument brief, §1 to §7

All 26 remaining probes miss in every file.

| Section | What is absent |
|---|---|
| §1 | phenotype-vs-mechanism reframe, EGFR / tumour-agnostic, "Correlates of War codes by organ", and the N-objection answer (unit = utterance / dyad-week, not the state) |
| §2 | culture-dish problem, 99% of gut flora, GDELT/ICEWS news-boundness, no HGNC/GO equivalent, prestige gradient, no pharmacovigilance |
| §3 | category C, MERLN's death, ISN Digital Library, why C is the worst kind |
| §4 | UN General Debate Corpus, CMFA PressCon (33,199 Q/A), FBIS / BBC Monitoring, paired bilateral readouts |
| §5 | counterfactual layer, second-order beliefs, microbiome analogue |
| §6 | 852 / 820 / 660, the 74 shared countries, 1,416 distinct at 4–8% overlap, the naming failure, PolData-as-registry |
| §7 | LLMs making the 113th redundant corpus cheaper than finding the first 112 |

## What this means, ranked

1. **§6 is the gap worth closing.** It is the only *verified* section – both manifests machine-read,
   script and outputs exist – and the brief's own §8 says the numbers "are the natural replacement
   for the abstract version of the fragmentation argument." Figure source is in
   `SESSION_INDEX_2026-08-29.md` §3, but it uses `c-purple` / `c-coral` / `var(--b)` theme classes
   that exist in the chat widget host and **not** in this deck – it needs re-drawing in deck hex.
2. **§1–§5 and §7 are argued, not surveyed** (brief §9). They are not slide-ready as fact; putting
   them on a slide would assert as established what the brief itself flags as analysis.
3. The gap between "documented" and "in the deck" is the whole finding here. All five files existed
   and were complete; none of their substance had reached a slide.

## Also applied this session, outside the deck

`index.html` Day 1: labels summed to 155 minutes in a 150-minute window – fixed by taking 5 from
*The approach* so the hands-on block keeps its full 25 and starts 13:00, following the session
index's own recommendation to protect the block where participants touch their own work. And the
pre-arrival page no longer promises "nothing to install beforehand" against a block that installs
a CLI participants need working by Tuesday.

## Still blocked

The "What are you working on?" Google Doc still has no link-sharing. This terminal cannot set it
either, for a different reason than the web session gave: the available `drive_share_file` grants
**anyone-with-link → reader**, and participants need **Editor**. The Drive OAuth also returned
`invalid_grant`. Manual: Share → General access → Anyone with the link → Editor.

## Update — one gap closed, s17 added

A new slide, **s17 "What transfers, and what does not"**, now sits immediately before
*"So why not us?"* (`a6cf0db`). Two columns, eight small diagrams, **23 visible words**.

**Why it was needed, precisely.** The gap was not that the material sat in `data-n`. It was that
the arc has an open rhetorical flank: six slides say *other fields did it* (humors, 'omics,
geomics, AlphaFold, vaccine, two paradigm-shift slides), and then s18 asks *"So why not us?"* with
no answer on screen when someone in an IR department supplies the obvious one – **because states
are not cells**. The slide closes that at the point the deck is most exposed, so the question lands
as earned rather than rhetorical.

**What it moves out of the brief and onto a slide:**

| Brief | Now on s17 |
|---|---|
| §1 | reclassification by mechanism – *the load-bearing move*, previously in no slide |
| §1 | the N-objection answer: the state and the war ARE the phenotype |
| §2 | no HGNC/GO equivalent, so nothing pools |
| §2 | no adverse-event registry |
| §1 | no central dogma (also on s12, as dashed arrows) |

**One row is not from the brief.** *"The specimen reads the paper"* – a tumour does not change its
behaviour because you published its profile, an adversary does – is this terminal's addition, not
the web session's. It is arguably the deepest of the four differences, because unlike the others it
never goes away however much data is collected. Flagged because it is the one claim on the slide
that has not been through anyone else's hands.

**Still not on any slide:** §6's verified three-corpus numbers, §3 category C and MERLN's death,
§4's corpora (UNGDC, CMFA PressCon, FBIS), §5's counterfactual layer and second-order beliefs, and
§7's closing beat about the 113th redundant corpus.

**Cost, stated honestly:** this adds a slide to Day 1, already 53% diagnosis, whose cut list names
the 'omics slide as first cut. It earns its place by replacing live improvisation at the weakest
moment – but if Monday runs long it is a better cut than the hands-on block.

**A process defect worth keeping.** The first render passed the automated fit check and was still
wrong in three places: the right column's last line clipped mid-word, and two left rows overran
their cards, because the text was sized by eye. Only reading the PNG caught it. *A container that
fits does not mean the text inside it fits.* The generator now asserts every string against the
measured card budget before it will emit.

## Record

- Tana: node `czszAKKlgy9Q` (2026-08-29, HCSS) – `#output` `#Claude` `#lesson-learned`
- HANDOFF: the web session's own entry, appended under 2026-08-29 and extended with what was applied
- Repo: `rubase-workshop-gatech-2608`, pushed – audit at `f97f158`, new slide at `a6cf0db`
