# Day 4 &middot; the two prompts you need today

Classification, then the write-up. Both are verbatim from the pipeline that produced the
Russian-military-regeneration example on the slides &ndash; the domain-specific wording is left in so you
can see what a real one looks like, and the parts you swap are marked.

**Today you run these on YOUR OWN material:** the taxonomy you built on Day 3, applied to the corpus
you built on Day 2 (abstracts are enough &ndash; you do not need full texts to see whether this works).

**Companion file:** the full production classification prompt, with its gatekeeping phase explained
at length, is in [`taxonomy_classification_prompt.md`](taxonomy_classification_prompt.md). Day 3's
taxonomy generator is in [`taxonomy_generation_prompt.md`](taxonomy_generation_prompt.md).

---

## 1 &middot; The classification prompt

Assigns each chunk of your corpus to elements of your taxonomy. This is the whole of what tells the
model what to do.

```text
system_prompt

You are an expert [DOMAIN] analyst specializing in [WHAT YOU ASSESS].

Your task is to classify each text chunk according to our taxonomy that lists
various important aspects of [YOUR TOPIC].

Below is the taxonomy in JSON form for your reference. You must ONLY use
Tier-3 name values present in this taxonomy.

[TAXONOMY START]
... paste your whole Day-3 scheme here, verbatim ...
[TAXONOMY END]

For each text chunk, return the Tier-3 element(s) it belongs to, and nothing else.
```

**Two things carry almost all the quality, and both are counter-intuitive:**

1. **Gatekeep before you classify.** Ask a model to "classify this against the taxonomy" and it
   will classify *everything*, because you handed it categories and no exit. Give it a way to say
   *not relevant*. Most of your quality comes from that gate, not from the classification.
2. **Paste the category list verbatim and demand it back verbatim.** No IDs, no abbreviations, no
   "closest match". If the model paraphrases a label, your join silently drops the record &ndash; and
   ***a silent drop looks exactly like an absence of evidence***.

**Cost.** Batch ~20 documents per call and cache the system prompt. Batching is a bigger lever on
cost than picking a cheaper model.

---

## 2 &middot; The analysis prompt (the write-up)

Once the chunks are labelled, this is what turns labels into an argument. Run it **per taxonomic
element**, over all the chunks that landed in that element.

```text
You are an expert in [DOMAIN] analysis. Your task is to analyze a specific topic,
focusing on its implications for [YOUR RESEARCH QUESTION]. The analysis will be
conducted using data provided as input, and it should reference the chunk IDs
associated with the specific text used to support each observation.

1. SUMMARY
   Key points for this topic, and how they relate to [your question].
   Explicitly mention strengths and weaknesses. Reference the chunk IDs.

2. THEMES
   The recurring themes and subtopics. Specific examples, with chunk IDs.

3. EVOLUTION
   How the discussion changed over time, using months as the primary unit, tied to
   specific events. Highlight turning points.

4. AUTHOR AND SOURCE DIFFERENCES
   Where sources agree, disagree, or are simply silent. Silence is a finding.
```

🟥 **Every instruction demands a chunk ID.** That is not bureaucracy: it is what makes the write-up
auditable, and it is the difference between an analysis you can defend and a summary you have to be
trusted on.

---

## 3 &middot; Rolling the elements up into a report

Run prompt 2 once per element, then ask for the synthesis across them. The worked example on the
slides is a SWOT of Russian military regeneration aptitude, built entirely from the labelled chunks:
self-perceived strengths (manpower flexibility, industrial resilience, doctrinal adaptation),
weaknesses, and what the sources never say.

```text
You have the per-element analyses below, each with its chunk IDs.

Produce a [SWOT / structured assessment] for [YOUR QUESTION], drawing only on those
analyses. For every claim, carry through the chunk IDs that support it. Where the
evidence is thin or the sources are silent, say so explicitly rather than smoothing it over.
```

**The honest boundary to keep:** what you get out describes **how your sources talk about** your
topic. That is not the same as what is true, and the write-up should say which one it is claiming.
