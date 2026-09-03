# Day 4 &middot; the prompts you need today

**What you are doing today:** running **the taxonomy you built on Day 3** over **the corpus you built
on Day 2**. Abstracts are enough &ndash; you do not need full texts to find out whether this works. Then
measuring, briefly and cheaply, whether it worked.

Two prompts, in this order.

---

## 1 &middot; Classify &rarr; [`taxonomy_classification_prompt.md`](taxonomy_classification_prompt.md)

Assigns every chunk of your corpus to elements of your taxonomy.

**Two things carry almost all the quality, and both are counter-intuitive:**

- **Gatekeeping comes first, and is deliberately strict.** Ask a model to "classify this against the
  taxonomy" and it classifies *everything*, because you gave it categories and no exit. The gate is
  what keeps an off-topic document out. Most of your quality comes from Phase 1, not Phase 2.
- **The category list is pasted verbatim and must come back verbatim.** No IDs, no abbreviations, no
  "closest match". If the model paraphrases a label your join silently drops the record &ndash; and
  ***a silent drop looks exactly like an absence of evidence***.

**Cost:** batch ~20 documents per call and cache the system prompt. Batching is a bigger lever than
picking a cheaper model.

---

## 2 &middot; Write it up &rarr; [`report_writing_prompt.md`](report_writing_prompt.md)

Turns labels into an argument. Run it **once per taxonomy element**, over the chunks that landed in
that element.

Four required moves: **summary &middot; themes &middot; evolution over time &middot; author and source
differences** &ndash; and *silence is a finding*.

🟥 **Every substantive claim must point to one or more chunk IDs.** If the supplied chunks do not
support a claim, the model must say so. ***A fluent paragraph without traceable evidence is not a
finding*** &ndash; it is the difference between an analysis you can defend and a summary someone has to
take on trust.

---

## Also on this site

- [`taxonomy_generation_prompt.md`](taxonomy_generation_prompt.md) &ndash; Day 3's generator, if you want
  to revise your scheme before you run it.
- [`MDTDF_PROMPT.md`](MDTDF_PROMPT.md) &ndash; the fuller multidimensional-taxonomy framework.
- [`cli_setup_guide.md`](cli_setup_guide.md) &ndash; if your CLI still is not working.

## The honest boundary, worth saying out loud in your write-up

What you get out describes **how your sources talk about** your topic. That is not the same as what is
true. A write-up that says which of the two it is claiming is a better piece of work than one that
quietly blurs them.
