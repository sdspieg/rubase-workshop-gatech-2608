#!/usr/bin/env python3
"""Mechanical coverage and integration gate for the participant glossary."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "resources" / "glossary.json"
INDEX = ROOT / "index.html"
SCRIPT = ROOT / "glossary.js"
TOOLTIPS = ROOT / "glossary-tooltips.js"
SOURCE = Path("/mnt/g/My Drive/Begrippenlijst.docx")


def key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def fail(message: str) -> None:
    print(f"GLOSSARY FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


payload = json.loads(DATA.read_text(encoding="utf-8"))
meta = payload["meta"]
entries = payload["entries"]

if len(entries) != meta["entry_count"] or len(entries) != 437:
    fail(f"entry count is {len(entries)}, expected 437")

display_keys = [key(entry["term"]) for entry in entries]
if len(display_keys) != len(set(display_keys)):
    fail("reader-facing terms are not unique after normalization")

for entry in entries:
    if not entry["term"].strip() or not entry["definition"].strip():
        fail("blank term or definition")
    if len(entry["definition"].split()) > 65:
        fail(f"definition exceeds 65 words: {entry['term']}")
    if "—" in entry["definition"]:
        fail(f"house-style em dash remains: {entry['term']}")

aira = [term for entry in entries for term in entry["aira_source_terms"]]
required = [term for entry in entries for term in entry["workshop_required_terms"]]
sweep = [term for entry in entries for term in entry["sweep_terms"]]
excluded = meta["surface_sweep"]["excluded"]

for label, terms, expected in (
    ("AIRA", aira, 105),
    ("workshop-required", required, 76),
    ("full-surface sweep", sweep, 249),
):
    if len(terms) != expected or len(set(terms)) != expected:
        fail(f"{label} coverage is {len(terms)} records / {len(set(terms))} unique, expected {expected}")

if len(sweep) + len(excluded) != meta["surface_sweep"]["candidate_terms"] or meta["surface_sweep"]["candidate_terms"] != 251:
    fail("sweep inclusion and exclusion ledger does not balance to 251")

lookup = {
    key(value)
    for entry in entries
    for value in [entry["term"], *entry.get("aliases", [])]
}
for original in (
    "Corpus", "Taxonomy", "Ontology", "Classification", "Precision", "Recall",
    "Cohen's kappa", "Confusion matrix", "Bibliometrics", "RAG", "LLM",
):
    if key(original) not in lookup:
        fail(f"original workshop term is no longer findable: {original}")

for distinction_term in (
    "Chunk", "Passage", "Text span", "Evidence span", "Document", "Record",
    "Corpus", "Dataset", "Sample", "Classification", "Taxonomic annotation",
    "Inter-annotator agreement", "Cohen's kappa", "Terminal", "Command-line interface",
):
    if key(distinction_term) not in display_keys:
        fail(f"distinct participant concept lacks its own entry: {distinction_term}")

distinction = meta.get("distinction_audit", {})
if distinction.get("missing_base_concepts_added") != 43 or distinction.get("definitions_rewritten_for_contrast") != 57:
    fail("distinction-audit ledger is missing or incomplete")

index = INDEX.read_text(encoding="utf-8")
script = SCRIPT.read_text(encoding="utf-8")
for marker in ('<script src="glossary.js"></script>', "id = 'glossaryAlphabet'", "id = 'glossaryList'", "block.replaceChildren()"):
    haystack = index if marker.startswith("<script") else script
    if marker not in haystack:
        fail(f"integration marker missing: {marker}")
if "ABCDEFGHIJKLMNOPQRSTUVWXYZ" not in script:
    fail("A–Z jump control is missing")
if "innerHTML" in script:
    fail("glossary renderer must not inject HTML")

tooltip_script = TOOLTIPS.read_text(encoding="utf-8")
if "MutationObserver" not in tooltip_script or "tabIndex = 0" not in tooltip_script:
    fail("tooltip layer must cover dynamically inserted deck content and keyboard focus")
html_pages = sorted(ROOT.glob("*.html"))
missing_tooltips = [page.name for page in html_pages if 'src="glossary-tooltips.js"' not in page.read_text(encoding="utf-8")]
if missing_tooltips:
    fail("tooltip layer missing from: " + ", ".join(missing_tooltips))

for required_file in ("prompt.html", "prompt-viewer.js", "prompt-link-router.js"):
    if not (ROOT / required_file).exists():
        fail(f"tooltip-enabled prompt viewer missing: {required_file}")
prompt_html = (ROOT / "prompt.html").read_text(encoding="utf-8")
if 'class="participant-prompt"' not in prompt_html or 'src="glossary-tooltips.js"' not in prompt_html:
    fail("prompt viewer is not connected to the glossary tooltip layer")

# Regenerate each QR deterministically in memory/on a temporary sibling and
# compare bytes. This gates the exact public prompt-viewer URLs without trusting
# a filename or a nearby anchor.
qr_spec = importlib.util.spec_from_file_location("build_prompt_qr", ROOT / "tools" / "build_prompt_qr.py")
qr_module = importlib.util.module_from_spec(qr_spec)
assert qr_spec.loader is not None
qr_spec.loader.exec_module(qr_module)
for prompt_id, live_path in qr_module.TARGETS.items():
    temporary = live_path.with_suffix(".audit.png")
    try:
        qr_module.render(prompt_id, temporary)
        if temporary.read_bytes() != live_path.read_bytes():
            fail(f"prompt QR does not encode the gated viewer URL: {live_path.name}")
    finally:
        temporary.unlink(missing_ok=True)

if SOURCE.exists():
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if digest != meta["aira_source"]["sha256"]:
        fail("authoritative AIRA glossary changed; regenerate and re-audit")
    try:
        from docx import Document
    except ImportError as exc:
        fail(f"python-docx is required while the source is mounted: {exc}")
    paragraphs = [" ".join(p.text.split()) for p in Document(SOURCE).paragraphs]
    source_terms = {
        text for index, text in enumerate(paragraphs)
        if text and 1 < len(text) <= 90 and index + 1 < len(paragraphs)
        and len(paragraphs[index + 1]) >= 180
        and text not in {"HCSS RuBase Training", "Begrippenlijst"}
    }
    if source_terms != set(aira):
        fail(f"AIRA source mismatch: source={len(source_terms)}, covered={len(set(aira))}")

print(
    "GLOSSARY PASS: "
    f"{len(entries)} entries; AIRA {len(set(aira))}/105; "
    f"workshop-required {len(set(required))}/76; "
    f"surface sweep {len(set(sweep))} included + {len(excluded)} excluded = 251; "
    f"{meta['surface_sweep']['participant_characters_reviewed']:,} participant-facing characters reviewed; "
    f"tooltips loaded on {len(html_pages)}/{len(html_pages)} HTML pages"
)
