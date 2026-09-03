#!/usr/bin/env python3
"""Build the three workshop prompt QR codes from their public viewer URLs."""

from pathlib import Path

import qrcode


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://sdspieg.github.io/rubase-workshop-gatech-2608/prompt.html?id="
TARGETS = {
    "taxonomy-generation": ROOT / "img" / "qr_taxonomy_generation_prompt.png",
    "taxonomy-classification": ROOT / "img" / "qr_taxonomy_classification_prompt.png",
    "report-writing": ROOT / "img" / "qr_report_writing_prompt.png",
}


def render(identifier: str, target: Path) -> None:
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=14,
        border=4,
    )
    qr.add_data(BASE + identifier)
    qr.make(fit=True)
    qr.make_image(fill_color="black", back_color="white").save(target)


if __name__ == "__main__":
    for prompt_id, output in TARGETS.items():
        render(prompt_id, output)
        print(f"{output.relative_to(ROOT)} → {BASE}{prompt_id}")
