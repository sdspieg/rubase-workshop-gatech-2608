# GATech workshop seed corpus – deterrence and red lines

A starter corpus for the RuBase / StratBase methods workshop, Georgia Tech, 31 August to
4 September 2026. It exists so that every hands-on block is attendable by someone who walked in
that morning with nothing.

Harvested from OpenAlex. Every query was logged verbatim **before** the request that used it, and
abstracts are reconstructed from OpenAlex's inverted index rather than stringified, which is the
difference between an abstract and a dictionary of word positions in your corpus.

---

## The six-line methods block, filled in

This corpus ships with the Day 4 handout already completed for it. That is deliberate: the first
thing you do with a corpus is describe it, and this is what that looks like.

**1. Question.** What does the scholarly record since 2010 say about deterrence, strategic
stability and red lines, and how is that literature structured?

**2. Query.** Ten quoted bands on OpenAlex, surface `filter=title_and_abstract.search:` (aboutness:
title and abstract only, **not** full text), each bounded
`from_publication_date:2010-01-01,to_publication_date:2026-12-31`, run **2026-08-27**:

| band | query, verbatim | records |
|---|---|--:|
| `nuclear_deterrence` | `"nuclear deterrence"` | 2,563 |
| `deterrence_theory` | `"deterrence theory"` | 1,574 |
| `strategic_stability` | `"strategic stability"` | 1,355 |
| `nuclear_signalling` | `"nuclear signaling" OR "nuclear signalling"` | 1,262 |
| `extended_deterrence` | `"extended deterrence"` | 476 |
| `escalation_control` | `"escalation management" OR "escalation control"` | 314 |
| `denial_punishment` | `"deterrence by denial" OR "deterrence by punishment"` | 287 |
| `conventional_deterrence` | `"conventional deterrence"` | 169 |
| `cross_domain_deterrence` | `"cross-domain deterrence"` | 31 |
| `red_lines` | `"red line" OR "red lines"` | 7,937 |

**3. Corpus.** **15,968 unique works** deduplicated by OpenAlex work id across the ten bands.
**86.4%** carry a reconstructed abstract. Filtered to on-domain primary subfield
(*Political Science and International Relations* or *Sociology and Political Science*) **and** a
non-empty abstract: **4,534 records**, 3,724 of them with a DOI, 2010 to 2026, median abstract
1,202 characters.

**4. Scheme.** None applied yet. Building one is Day 3; applying it is Day 4.

**5. Reliability.** Not applicable yet, and it will not be until two people code the same slice.
Do not report a number here until then.

**6. Blind spot.** The surface is title-and-abstract, so a work that discusses deterrence
substantively in its body but never in its abstract is **invisible to this corpus by construction**.
The date floor of 2010 excludes the entire Cold War theoretical literature. Both are choices, not
oversights, and both belong in any sentence that starts "the literature shows".

---

## What makes this corpus worth teaching with: it is deliberately noisy

The harvest was **recall-first**, on purpose. No discipline filter was applied at query time, so the
raw 15,968 carry the noise a real first harvest carries. Measured share whose **primary** OpenAlex
subfield is Political Science and International Relations:

| band | on-domain | what the noise actually is |
|---|--:|---|
| `nuclear_deterrence` | **73.6%** | a precise phrase; little competition for it |
| `conventional_deterrence` | 61.5% | |
| `cross_domain_deterrence` | 61.3% | tiny band, 31 records |
| `extended_deterrence` | 59.7% | |
| `strategic_stability` | 46.4% | economics and econometrics; also control theory |
| `denial_punishment` | 39.0% | criminology, which is a *cousin* rather than noise |
| `escalation_control` | 26.1% | clinical escalation, project management |
| `deterrence_theory` | 19.6% | criminology dominates: deterrence theory is theirs too |
| `red_lines` | **6.9%** | ecology, ALS genetics, cell stress, astronomy |
| `nuclear_signalling` | **2.0%** | **molecular biology.** The nucleus of a *cell* |

**The two lessons are in that table.**

*"Nuclear signalling"* returns 1,262 works of which **25** are international relations. 26.9% are
molecular biology: *Nuclear Signaling of Plant MAPKs*, *Mitochondrial Biogenesis through Activation
of Nuclear Signaling Proteins*. The phrase is not ambiguous in English, it is ambiguous **across
fields**, and no amount of care in phrasing fixes it. A domain filter does.

*"Red lines"* returns 7,937 works of which 550 are IR: *China's ambitious ecological red lines*,
*The Enigmatic Red Line in ALS*, *The Thin Red Line Between Adaptation and Failure*. Here the noise
speaks a **foreign vocabulary**, so a NOT term can clean it cheaply. That is the difference the
Day 2 block is about: when the noise is domain-foreign, Boolean works; when it shares your
vocabulary, only a semantic pass will separate it.

**And the filter is not free of error either.** *New Technologies & Strategic Stability* and
*The Gulf And The Search For Strategic Stability* are plainly on-topic and were still excluded,
because OpenAlex gave them a non-IR primary subfield. The clean file is therefore a **high-precision
subset, not a complete one** – which is exactly the trade this workshop is about.

---

## Files

| file | what it is | size |
|---|---|--:|
| `seed_corpus.csv` / `.csv.gz` | the clean 4,534: on-domain, with abstracts | 10.0 / 3.2 MB |
| `seed_corpus.jsonl` / `.jsonl.gz` | the same records, one JSON object per line | 11.0 / 3.3 MB |
| `seed_corpus_quickstart.csv` | 442 records, stratified across all ten bands, for the room | 0.8 MB |
| `ledger.json` | the exact submitted query and record count per band | small |

Columns: `id · year · title · authors · venue · cited_by · subfield · band · doi · keywords ·
topics · abstract`. `keywords` and `topics` are carried through deliberately: they are the **K** in
title-abstract-keywords, and they are the cheapest classification signal you have.

## Reproducing it

The ledger holds every submitted query string, so the harvest can be re-run exactly as it was.
Counts will drift upward as OpenAlex grows, which is precisely why line 2 of the methods block
carries the date it was run.
