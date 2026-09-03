#!/usr/bin/env python3
"""Apply a reviewed, structured distinction audit to the workshop glossary."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GLOSSARY = ROOT / "resources" / "glossary.json"
AUDIT_RECORD = ROOT / "resources" / "glossary_distinction_audit.json"


def norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


parser = argparse.ArgumentParser()
parser.add_argument("audit", type=Path)
args = parser.parse_args()

data = json.loads(GLOSSARY.read_text(encoding="utf-8"))
audit = json.loads(args.audit.read_text(encoding="utf-8"))
assert len(audit["additions"]) == 43
assert len(audit["revisions"]) == 57

entries = data["entries"]
by_term = {norm(entry["term"]): entry for entry in entries}
assert len(by_term) == len(entries)

# These strings were aliases, but the audit established that participants need
# them as separately defined concepts. Keeping both would make lookup ambiguous.
alias_splits = {
    "Abstract": "summary",
    "Cohen's kappa": "inter-annotator agreement",
    "Command-line interface": "terminal",
    "Evidence span": "text span",
    "Relevance screening": "gatekeeping",
    "Taxonomic annotation": "classification",
}
for display, alias in alias_splits.items():
    entry = by_term[norm(display)]
    entry["aliases"] = [value for value in entry.get("aliases", []) if norm(value) != norm(alias)]

for revision in audit["revisions"]:
    entry = by_term[norm(revision["term"])]
    entry["definition"] = revision["definition"]
    entry["contrasts_with"] = revision["contrast_group"]

for addition in audit["additions"]:
    assert norm(addition["term"]) not in by_term, addition["term"]
    entry = {
        "term": addition["term"],
        "aliases": addition["aliases"],
        "definition": addition["definition"],
        "aira_source_terms": [],
        "workshop_required_terms": [],
        "sweep_terms": [],
        "distinction_audit_terms": [addition["term"]],
        "contrast_evidence": addition["evidence"],
    }
    entries.append(entry)
    by_term[norm(entry["term"])] = entry

for entry in entries:
    entry["definition"] = entry["definition"].replace(" — ", " – ").replace("—", " –")

entries.sort(key=lambda entry: norm(entry["term"]))
data["meta"]["entry_count"] = len(entries)
data["meta"]["distinction_audit"] = {
    "date": "2026-09-04",
    "missing_base_concepts_added": len(audit["additions"]),
    "definitions_rewritten_for_contrast": len(audit["revisions"]),
    "misleading_aliases_split": len(alias_splits),
    "method": "Full glossary plus every participant prompt and guide audited for missing base objects and confusable neighboring concepts.",
}

assert len(entries) == 437
assert len({norm(entry["term"]) for entry in entries}) == 437
assert all(entry["definition"].strip() and len(entry["definition"].split()) <= 70 for entry in entries)
assert all("—" not in entry["definition"] for entry in entries)

GLOSSARY.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
AUDIT_RECORD.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Applied 43 additions and 57 contrast rewrites; glossary now has {len(entries)} entries")
