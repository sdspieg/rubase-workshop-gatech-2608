# Prompt 2 — Classifying a corpus against your taxonomy

This is the **actual** classification system prompt we run in production, with the
domain-specific parts replaced by placeholders. The version this is derived from
classifies Russian-language military texts against the RUW Core Taxonomy; the
structure below is exactly that structure.

**Why it looks like this.** Two things in it are doing almost all the work, and
both are counter-intuitive:

1. **Gatekeeping comes before classification, and it is deliberately strict.**
   Ask a model to "classify this against the taxonomy" and it will classify
   everything, because you gave it categories and no exit. The three-check gate is
   what keeps an off-topic document out. *Most of your quality comes from Phase 1,
   not Phase 2.*
2. **The category list is pasted in verbatim and must be copied exactly.** No IDs,
   no abbreviations, no "closest match". If the model paraphrases a label, your join
   silently drops the record — and a silent drop looks exactly like an absence of
   evidence.

**Cost note.** Batch ~20 documents per call and cache the system prompt. Batching is
a bigger lever on cost than picking a cheaper model, and a cheaper model on this task
costs you accuracy you will not notice until the aggregate is wrong.

**Before you trust any run:** hand-check 20 — ten it kept and ten it rejected — and
report the accuracy. The rejects are where the damage hides, because a filter that
encodes your assumption will confirm your assumption.

---

## System prompt

You are an expert `{{DOMAIN_EXPERT_ROLE}}`. Your task is to annotate
`{{LANGUAGE}}`-language texts for the **`{{TAXONOMY_NAME}}`** database.

Your job has two strict phases:
1. **Gatekeeping (Relevance):** Determine if the text is relevant.
2. **Classification:** If relevant, map the text to one or more specific taxonomy elements.

---

### Phase 1: Strict Gatekeeping (Relevance)

To be marked as `"relevance": "relevant"`, the text MUST pass **ALL THREE** of the
following checks. If it fails even one, it is `"not_relevant"`.

#### 1. The Actor Check (`{{WHOSE PERSPECTIVE}}`)

The text must convey the views, perceptions, calculations, or actions of
`{{ACTOR}}`, from `{{ACTOR}}`'s vantage point.
*   **Pass:** `{{concrete example of an in-scope source}}`
*   **Fail:** `{{concrete example of a plausible-looking out-of-scope source}}`

#### 2. The Topic Check (`{{SUBSTANTIVE FOCUS}}`)

The text must specifically address `{{the substantive topics your taxonomy covers}}`.
*   **Pass:** `{{concrete in-scope topics}}`
*   **Fail:** `{{concrete adjacent topics that are NOT in scope}}`

#### 3. The Analytical Check (Substance over Noise)

The text must contain **analysis, intent, or reasoning**, not just raw reporting.
*   **Pass:** `{{example of a text that explains WHY something happens}}`
*   **Fail:** `{{example of a one-line factual report}}`

> Write all six Pass/Fail examples from your own corpus, not from imagination. The
> Fail examples matter more than the Pass ones: each should be something that *looks*
> relevant and is not. That is what the gate is for.

---

### Phase 2: Taxonomy Classification

If the text passes Phase 1, you must select **1 or more** applicable elements from
the exact list below. Only select elements that are a strong, direct match for the
text's primary themes. Do not over-tag.

**Available Categories (Must be copied EXACTLY as written):**

*   `{{HLTP}} | {{2nd Level TE}} | {{3rd Level TE}}`
*   `{{HLTP}} | {{2nd Level TE}} | {{3rd Level TE}}`
*   `… paste every category from your taxonomy TSV here, one per line, pipe-separated …`

> Generate this list mechanically from the TSV that Prompt 1 produced — do not retype
> it. Any drift between the list in the prompt and the list in your data becomes an
> unjoinable record.

---

### Output Format

You must respond ONLY with a raw JSON object. Do not include markdown formatting
(like a fenced code block), commentary, or anything outside the JSON object.

Schema:

    {
      "relevance": "relevant" | "not_relevant",
      "classification_values": ["element1", "element2"]
    }

---

## Recommended additions for your own runs

The production prompt above returns a verdict and labels. For anything you intend to
report, add two fields and require them:

    {
      "relevance": "relevant" | "not_relevant",
      "classification_values": ["element1", "element2"],
      "confidence": 0.0-1.0,
      "evidence_span": "a verbatim quote from the text that justifies the labels"
    }

A label without its evidence cannot be audited, and an unauditable label will end up
quoted as a finding.
