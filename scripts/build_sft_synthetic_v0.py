"""Build train-only synthetic SFT data for the LoRA PoC.

This builder intentionally avoids evaluation rows and images. It creates a
balanced controlled synthetic mix: answerable field extraction positives and
mechanically checked NOT_FOUND negatives.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.datasets.jsonl_dataset import write_jsonl
from src.datasets.schema import validate_benchmark_row, validate_benchmark_rows
from src.utils.hashing import sha256_file
from src.utils.io import write_json, write_text


FIELD_VALUES = {
    "invoice_number": ("Invoice Number", ["INV-2317", "INV-7094", "INV-8832", "INV-4408"]),
    "invoice_date": ("Invoice Date", ["2026-06-01", "2026-06-05", "2026-06-12", "2026-05-29"]),
    "vendor": ("Vendor", ["Atlas Print Co", "Maple Office Supply", "River City Parts", "Northstar Lab"]),
    "customer": ("Customer", ["Alex Kim", "Morgan Patel", "Casey Rivera", "Jordan Lee"]),
    "total_due": ("Total Due", ["$45.87", "$128.44", "$902.10", "$1,204.10"]),
    "purchase_order": ("Purchase Order", ["PO-1190", "PO-4421", "PO-7780", "PO-6502"]),
    "payment_terms": ("Payment Terms", ["Net 15", "Net 30", "Due on receipt", "Net 45"]),
    "tracking_number": ("Tracking Number", ["1Z 338 190 22", "TRK-50991", "ZX-774200", "TRK-88201"]),
    "carrier": ("Carrier", ["Metro Courier", "Northline Freight", "Postal Express", "Summit Logistics"]),
    "ship_date": ("Ship Date", ["2026-05-12", "2026-05-18", "2026-06-02", "2026-06-08"]),
    "recipient": ("Recipient", ["Acme Parts", "Cedar Lab", "Jordan Lee", "West Clinic"]),
    "service_level": ("Service Level", ["Ground", "Two Day", "Priority", "Standard"]),
    "weight": ("Weight", ["2.4 lb", "7.9 lb", "15.0 lb", "22.5 lb"]),
    "patient_id": ("Patient ID", ["P-10491", "P-55320", "P-88012", "P-77104"]),
    "visit_date": ("Visit Date", ["2026-03-02", "2026-04-10", "2026-05-21", "2026-06-03"]),
    "clinic": ("Clinic", ["Oak Clinic", "Central Care", "Westside Health", "Valley Medical"]),
    "provider": ("Provider", ["Dr. Lane", "Dr. Moreno", "Dr. Shah", "Dr. Chen"]),
    "copay": ("Copay", ["$0.00", "$20.00", "$35.00", "$50.00"]),
    "room": ("Room", ["A12", "B07", "C18", "D03"]),
    "account_ending": ("Account Ending", ["1175", "4811", "9022", "6604"]),
    "statement_date": ("Statement Date", ["2026-04-30", "2026-05-31", "2026-06-30", "2026-07-31"]),
    "opening_balance": ("Opening Balance", ["$812.02", "$1,204.10", "$5,120.00", "$220.55"]),
    "closing_balance": ("Closing Balance", ["$799.11", "$1,451.33", "$5,044.87", "$310.42"]),
    "branch": ("Branch", ["Downtown", "North Ridge", "West Loop", "East Point"]),
}

ABSENT_VALUES = {
    "fax_number": ("Fax Number", "555-0101"),
    "vendor_tax_id": ("Vendor Tax ID", "92-8844111"),
    "approval_signature": ("Approval Signature", "Dana Cole"),
    "coupon_code": ("Coupon Code", "SAVE20"),
    "loyalty_number": ("Loyalty Number", "L-908177"),
    "delivery_window": ("Delivery Window", "9 AM to 1 PM"),
    "hazmat_code": ("Hazmat Code", "HZ-22"),
    "emergency_contact": ("Emergency Contact", "Pat Lee"),
    "routing_number": ("Routing Number", "021000021"),
    "advisor_email": ("Advisor Email", "advisor@example.com"),
}

DOCUMENT_TYPES = ["invoice", "shipping_notice", "medical_form", "bank_notice"]
QUESTION_TEMPLATES = [
    "What is the {field}?",
    "Provide the {field} shown in the document.",
    "What value is listed for {field}?",
]


def _font(size: int) -> ImageFont.ImageFont:
    for candidate in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ):
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def _draw_document(path: Path, title: str, lines: list[str]) -> None:
    image = Image.new("RGB", (900, 1200), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((40, 40, 860, 1160), outline=(30, 30, 30), width=3)
    draw.rectangle((40, 40, 860, 132), fill=(240, 244, 248), outline=(30, 30, 30), width=2)
    draw.text((70, 70), title.upper().replace("_", " "), fill=(20, 35, 55), font=_font(34))
    y = 176
    for line in lines:
        draw.text((82, y), line, fill=(30, 30, 30), font=_font(25))
        draw.line((80, y + 42, 820, y + 42), fill=(215, 220, 226), width=1)
        y += 68
    draw.text((70, 1120), "Controlled synthetic SFT train-only document", fill=(90, 95, 100), font=_font(18))
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def _normalize_field(label: str) -> str:
    return label.lower().replace(" ", "_")


def _contains_absent(rendered_text: str, absent_label: str, absent_value: str) -> bool:
    text = rendered_text.casefold()
    return absent_label.casefold() in text or absent_value.casefold() in text


def _build_row(index: int, split: str, rng: random.Random, image_dir: Path, positive: bool, seed: int) -> dict:
    doc_type = DOCUMENT_TYPES[index % len(DOCUMENT_TYPES)]
    field_keys = list(FIELD_VALUES)
    present_keys = rng.sample(field_keys, k=6)
    present_pairs = []
    for key in present_keys:
        label, values = FIELD_VALUES[key]
        present_pairs.append((key, label, rng.choice(values)))
    rendered_lines = [f"{label}: {value}" for _, label, value in present_pairs]
    rendered_text = "\n".join(rendered_lines)

    sample_id = f"sft-doc-template-{split}-{index + 1:04d}"
    image_path = image_dir / f"{sample_id}.png"
    _draw_document(image_path, doc_type, rendered_lines)
    image_sha = sha256_file(image_path)

    metadata = {
        "source_dataset": "controlled_synthetic_sft",
        "source_slice": "sft_docvqa_template_train_v0",
        "intended_use": "sft_train_only",
        "not_for_primary_eval": True,
        "document_type": doc_type,
        "present_fields": [_normalize_field(label) for _, label, _ in present_pairs],
        "rendered_text": rendered_text,
        "original_image_sha256": image_sha,
        "image_sha256": image_sha,
        "seed": seed,
        "ocr_text": rendered_text,
    }

    template = QUESTION_TEMPLATES[index % len(QUESTION_TEMPLATES)]
    if positive:
        key, label, value = present_pairs[index % len(present_pairs)]
        answer = value
        metadata.update(
            {
                "target_field": key,
                "target_value": value,
                "sft_label_type": "controlled_synthetic_positive",
            }
        )
        row = {
            "id": sample_id,
            "dataset": "sft_docvqa_template_train_v0",
            "image_path": image_path.as_posix(),
            "question": template.format(field=label.lower()),
            "answers": [answer],
            "capability": "ocr_exact",
            "answer_type": "short_text",
            "metadata": metadata,
        }
    else:
        absent_key, (absent_label, absent_value) = rng.choice(list(ABSENT_VALUES.items()))
        if absent_key in metadata["present_fields"] or _contains_absent(rendered_text, absent_label, absent_value):
            raise ValueError(f"absence check failed for {sample_id}: {absent_key}")
        metadata.update(
            {
                "absent_field": absent_key,
                "absent_value": absent_value,
                "absence_evidence_type": "controlled_render_negative",
                "absence_check_result": True,
                "sft_label_type": "controlled_synthetic_negative",
            }
        )
        row = {
            "id": sample_id,
            "dataset": "sft_docvqa_template_train_v0",
            "image_path": image_path.as_posix(),
            "question": template.format(field=absent_label.lower()),
            "answers": ["NOT_FOUND"],
            "capability": "not_found",
            "answer_type": "abstain",
            "metadata": metadata,
        }
    return validate_benchmark_row(row)


def build_rows(count: int, split: str, image_dir: Path, seed: int) -> list[dict]:
    if count < 1:
        raise ValueError("count must be positive")
    rng = random.Random(seed + (0 if split == "train" else 10_000))
    rows = []
    for index in range(count):
        positive = index % 2 == 1
        rows.append(_build_row(index, split, rng, image_dir, positive, seed))
    return validate_benchmark_rows(rows)


def _count(rows: list[dict]) -> Counter:
    counter: Counter[str] = Counter()
    for row in rows:
        label = row["metadata"].get("sft_label_type", "unknown")
        counter[label] += 1
    return counter


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-rows", type=int, default=500)
    parser.add_argument("--val-rows", type=int, default=80)
    parser.add_argument("--seed", type=int, default=20260615)
    parser.add_argument("--train-out", default="data/sft_docvqa_template_train_v0.jsonl")
    parser.add_argument("--val-out", default="data/sft_docvqa_template_val_v0.jsonl")
    parser.add_argument("--meta-out", default="data/sft_docvqa_template_train_v0.meta.json")
    parser.add_argument("--image-dir", default="data/sft_docvqa_template_train_v0_images")
    parser.add_argument("--spec-out", default="reports/sft_train_data_spec.md")
    args = parser.parse_args()

    if args.train_rows < 160:
        raise ValueError("train rows must be at least 160")
    if args.val_rows < 50 or args.val_rows > 100:
        raise ValueError("validation rows must be between 50 and 100")

    image_dir = Path(args.image_dir)
    train_rows = build_rows(args.train_rows, "train", image_dir, args.seed)
    val_rows = build_rows(args.val_rows, "val", image_dir, args.seed)

    write_jsonl(args.train_out, train_rows)
    write_jsonl(args.val_out, val_rows)

    train_counts = _count(train_rows)
    val_counts = _count(val_rows)
    meta = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "seed": args.seed,
        "train_path": args.train_out,
        "val_path": args.val_out,
        "image_dir": args.image_dir,
        "train_rows": len(train_rows),
        "val_rows": len(val_rows),
        "intended_use": "sft_methodology_poc_train_only",
        "not_for_primary_eval": True,
        "composition": {
            "controlled_synthetic_positive_train": train_counts["controlled_synthetic_positive"],
            "controlled_synthetic_negative_train": train_counts["controlled_synthetic_negative"],
            "controlled_synthetic_positive_val": val_counts["controlled_synthetic_positive"],
            "controlled_synthetic_negative_val": val_counts["controlled_synthetic_negative"],
            "native_template_swapped_noisy_train": 0,
            "native_template_swapped_omitted_reason": (
                "No non-evaluation real document images were locally available; "
                "evaluation images/rows were excluded by hard constraint."
            ),
        },
    }
    write_json(args.meta_out, meta)
    write_text(
        args.spec_out,
        "\n".join(
            [
                "# SFT Train Data Spec",
                "",
                f"Controlled synthetic train-only data generated with seed `{args.seed}`.",
                "Rows and images are distinct from the evaluation datasets.",
                "",
                f"- Train rows: {len(train_rows)}",
                f"- Validation rows: {len(val_rows)}",
                f"- Controlled synthetic answerable positives: {train_counts['controlled_synthetic_positive']} train, {val_counts['controlled_synthetic_positive']} val",
                f"- Controlled synthetic NOT_FOUND negatives: {train_counts['controlled_synthetic_negative']} train, {val_counts['controlled_synthetic_negative']} val",
                "- Native template-swapped real-document negatives: 0 rows, because no non-evaluation real document images were locally available.",
                "- Negative rows use `absence_evidence_type=controlled_render_negative` and are mechanically checked against rendered text.",
                "- All rows are marked `intended_use=sft_train_only` and `not_for_primary_eval=true`.",
                "",
                "Template-swapped negatives remain a methodology option only; none are included in this generated dataset.",
                "",
            ]
        ),
    )
    print(json.dumps(meta, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
