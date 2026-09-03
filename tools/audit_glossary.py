#!/usr/bin/env python3
"""Mechanical coverage and integration gate for the participant glossary."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "resources" / "glossary.json"
INDEX = ROOT / "index.html"
SCRIPT = ROOT / "glossary.js"
SOURCE = Path("/mnt/g/My Drive/Begrippenlijst.docx")


def key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def fail(message: str) -> None:
    print(f"GLOSSARY FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


payload = json.loads(DATA.read_text(encoding="utf-8"))
meta = payload["meta"]
entries = payload["entries"]

if len(entries) != meta["entry_count"] or len(entries) != 394:
    fail(f"entry count is {len(entries)}, expected 394")

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
    f"{meta['surface_sweep']['participant_characters_reviewed']:,} participant-facing characters reviewed"
)
