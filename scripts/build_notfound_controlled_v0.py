"""Build controlled synthetic NOT_FOUND benchmark slices.

The controlled slice renders documents from known fields, then asks for one
field that is deliberately absent from both the field inventory and rendered
text. This gives a provenance-backed negative benchmark without relying on OCR
or source-dataset annotations.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.datasets.jsonl_dataset import write_jsonl
from src.datasets.schema import validate_benchmark_row, validate_benchmark_rows
from src.utils.hashing import sha256_file
from src.utils.io import write_json, write_text


FIELD_POOLS = {
    "invoice": [
        ("Invoice Number", "INV-1047"),
        ("Invoice Date", "2026-01-18"),
        ("Vendor", "Northstar Office Supply"),
        ("Subtotal", "$418.20"),
        ("Total Due", "$452.76"),
        ("Purchase Order", "PO-7718"),
        ("Bill To", "Cedar Lab"),
        ("Terms", "Net 15"),
    ],
    "receipt": [
        ("Store", "Harbor Market"),
        ("Receipt Number", "R-88341"),
        ("Date", "2026-02-03"),
        ("Cashier", "M. Rivera"),
        ("Item Count", "6"),
        ("Total", "$37.42"),
        ("Payment", "Visa"),
        ("Terminal", "T04"),
    ],
    "shipping_notice": [
        ("Tracking Number", "1Z 491 771 20"),
        ("Carrier", "Metro Freight"),
        ("Ship Date", "2026-03-09"),
        ("Recipient", "Acme Bio Lab"),
        ("Weight", "4.8 lb"),
        ("Service", "Ground"),
        ("Origin", "Reno NV"),
        ("Destination", "Austin TX"),
    ],
    "medical_form": [
        ("Patient ID", "P-44029"),
        ("Visit Date", "2026-04-21"),
        ("Clinic", "Westside Health"),
        ("Provider", "Dr. K. Shah"),
        ("Reason", "Annual exam"),
        ("Copay", "$25.00"),
        ("Room", "B12"),
        ("Status", "Complete"),
    ],
    "bank_notice": [
        ("Account Ending", "8821"),
        ("Statement Date", "2026-05-31"),
        ("Customer", "Jordan Lee"),
        ("Opening Balance", "$1,284.11"),
        ("Closing Balance", "$1,402.58"),
        ("Branch", "Downtown"),
        ("Reference", "BNK-5017"),
        ("Notice Type", "Monthly Summary"),
    ],
}

ABSENT_FIELDS = {
    "invoice": [
        ("Fax Number", "555-0198", "missing_contact_fax"),
        ("Vendor Tax ID", "92-0004412", "missing_tax_id"),
        ("Approval Signature", "Dana Cole", "missing_signature"),
    ],
    "receipt": [
        ("Coupon Code", "SAVE20", "missing_coupon"),
        ("Loyalty Number", "L-908177", "missing_loyalty"),
        ("Refund Deadline", "2026-03-05", "missing_refund_deadline"),
    ],
    "shipping_notice": [
        ("Delivery Window", "9 AM to 1 PM", "missing_delivery_window"),
        ("Hazmat Code", "HZ-22", "missing_hazmat"),
        ("Driver Name", "A. Santos", "missing_driver"),
    ],
    "medical_form": [
        ("Insurance Group", "GRP-771", "missing_insurance_group"),
        ("Prescription Number", "RX-45019", "missing_prescription"),
        ("Emergency Contact", "Pat Lee", "missing_emergency_contact"),
    ],
    "bank_notice": [
        ("Routing Number", "021000021", "missing_routing"),
        ("Overdraft Fee", "$35.00", "missing_overdraft_fee"),
        ("Advisor Email", "advisor@example.com", "missing_advisor_email"),
    ],
}

QUESTION_TEMPLATES = [
    ("what_is_field", "What is the {field}?"),
    ("provide_field", "Provide the {field} shown in the document."),
    ("field_value", "What value is listed for {field}?"),
]

OOD_SCENES = [
    ("colored_blocks", "What is the invoice number?"),
    ("sunset_shapes", "What is the vendor tax ID?"),
    ("abstract_lines", "What is the routing number?"),
    ("simple_landscape", "What is the tracking number?"),
]


def _font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def _draw_document(path: Path, title: str, lines: list[str]) -> None:
    image = Image.new("RGB", (900, 1200), "white")
    draw = ImageDraw.Draw(image)
    title_font = _font(34)
    body_font = _font(25)
    small_font = _font(18)
    draw.rectangle((40, 40, 860, 1160), outline=(25, 25, 25), width=3)
    draw.rectangle((40, 40, 860, 130), fill=(238, 242, 247), outline=(25, 25, 25), width=2)
    draw.text((70, 68), title.upper().replace("_", " "), fill=(20, 35, 55), font=title_font)
    y = 175
    for line in lines:
        draw.text((82, y), line, fill=(30, 30, 30), font=body_font)
        draw.line((80, y + 42, 820, y + 42), fill=(215, 220, 226), width=1)
        y += 68
    draw.text((70, 1120), "Controlled synthetic document", fill=(90, 95, 100), font=small_font)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def _draw_ood(path: Path, scene: str, index: int) -> None:
    image = Image.new("RGB", (900, 700), (235, 238, 241))
    draw = ImageDraw.Draw(image)
    rng = random.Random(index)
    if scene == "colored_blocks":
        for _ in range(20):
            x0 = rng.randint(20, 760)
            y0 = rng.randint(20, 560)
            color = tuple(rng.randint(40, 220) for _ in range(3))
            draw.rectangle((x0, y0, x0 + rng.randint(45, 120), y0 + rng.randint(45, 110)), fill=color)
    elif scene == "sunset_shapes":
        draw.rectangle((0, 0, 900, 700), fill=(246, 194, 123))
        draw.ellipse((610, 80, 760, 230), fill=(255, 241, 138))
        for y in range(380, 700, 50):
            draw.rectangle((0, y, 900, y + 25), fill=(130, 91, 112))
    elif scene == "abstract_lines":
        for _ in range(45):
            color = tuple(rng.randint(20, 230) for _ in range(3))
            draw.line(
                (rng.randint(0, 900), rng.randint(0, 700), rng.randint(0, 900), rng.randint(0, 700)),
                fill=color,
                width=rng.randint(2, 8),
            )
    else:
        draw.rectangle((0, 0, 900, 390), fill=(135, 195, 228))
        draw.rectangle((0, 390, 900, 700), fill=(87, 154, 91))
        draw.polygon((160, 390, 330, 190, 500, 390), fill=(95, 105, 110))
        draw.polygon((430, 390, 610, 220, 790, 390), fill=(110, 112, 116))
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def _contains_absent_text(rendered_text: str, absent_field: str, absent_value: str) -> bool:
    normalized = rendered_text.casefold()
    return absent_field.casefold() in normalized or absent_value.casefold() in normalized


def build_controlled_rows(row_count: int, image_dir: Path) -> list[dict]:
    if row_count < 40 or row_count > 60:
        raise ValueError("controlled row_count must be between 40 and 60")

    rng = random.Random(20260613)
    rows = []
    doc_types = sorted(FIELD_POOLS)
    for index in range(row_count):
        document_type = doc_types[index % len(doc_types)]
        fields = FIELD_POOLS[document_type]
        absent_field, absent_value, absent_id = ABSENT_FIELDS[document_type][index % len(ABSENT_FIELDS[document_type])]
        template_id, template = QUESTION_TEMPLATES[index % len(QUESTION_TEMPLATES)]
        present = rng.sample(fields, k=5)
        present_fields = [field for field, _ in present]
        rendered_lines = [f"{field}: {value}" for field, value in present]
        rendered_text = "\n".join(rendered_lines)
        if absent_field in present_fields or _contains_absent_text(rendered_text, absent_field, absent_value):
            raise ValueError(f"absence check failed for {document_type} {absent_field}")

        sample_id = f"notfound-controlled-v0-{index + 1:03d}"
        image_path = image_dir / f"{sample_id}.png"
        _draw_document(image_path, document_type, rendered_lines)
        rel_image_path = image_path.as_posix()
        metadata = {
            "source_dataset": "controlled_synthetic",
            "source_slice": "notfound_controlled_v0",
            "document_type": document_type,
            "present_fields": present_fields,
            "absent_field": absent_field,
            "absent_value": absent_value,
            "absent_question_template_id": template_id,
            "rendered_text": rendered_text,
            "original_image_sha256": sha256_file(image_path),
            "absence_evidence_type": "controlled_render_negative",
            "absence_check_result": True,
            "controlled_absent_id": absent_id,
            "ocr_text": rendered_text,
        }
        row = {
            "id": sample_id,
            "dataset": "notfound_controlled_v0",
            "image_path": rel_image_path,
            "question": template.format(field=absent_field.lower()),
            "answers": ["NOT_FOUND"],
            "capability": "not_found",
            "answer_type": "abstain",
            "metadata": metadata,
        }
        rows.append(validate_benchmark_row(row))
    return validate_benchmark_rows(rows)


def build_ood_rows(row_count: int, image_dir: Path) -> list[dict]:
    rows = []
    for index in range(row_count):
        scene, question = OOD_SCENES[index % len(OOD_SCENES)]
        sample_id = f"notfound-ood-sanity-v0-{index + 1:03d}"
        image_path = image_dir / f"{sample_id}.png"
        _draw_ood(image_path, scene, index + 1)
        metadata = {
            "source_dataset": "controlled_synthetic",
            "source_slice": "notfound_ood_sanity_v0",
            "document_type": "non_document_ood",
            "present_fields": [],
            "absent_field": question.split(" the ", 1)[-1].rstrip("?"),
            "absent_value": "",
            "absent_question_template_id": "ood_document_field_probe",
            "rendered_text": "",
            "original_image_sha256": sha256_file(image_path),
            "absence_evidence_type": "non_document_ood_sanity",
            "absence_check_result": True,
            "ood_scene": scene,
            "ocr_text": "",
        }
        row = {
            "id": sample_id,
            "dataset": "notfound_ood_sanity_v0",
            "image_path": image_path.as_posix(),
            "question": question,
            "answers": ["NOT_FOUND"],
            "capability": "not_found",
            "answer_type": "abstain",
            "metadata": metadata,
        }
        rows.append(validate_benchmark_row(row))
    return validate_benchmark_rows(rows)


def _write_spec(path: Path, controlled_rows: list[dict], ood_rows: list[dict]) -> None:
    doc_types = sorted({row["metadata"]["document_type"] for row in controlled_rows})
    lines = [
        "# NOT_FOUND Controlled v0 Specification",
        "",
        "This benchmark is controlled synthetic data. Every controlled document image is rendered from a known field inventory, then queried for one field intentionally excluded from the inventory and rendered text.",
        "",
        "## Controlled Slice",
        "",
        f"- Rows: {len(controlled_rows)}",
        f"- Document types: {', '.join(doc_types)}",
        "- Ground truth answer: `NOT_FOUND` for every row",
        "- Absence evidence: `controlled_render_negative`",
        "- Validation rule: `absent_field` is not in `present_fields`, and neither `absent_field` nor `absent_value` appears in `rendered_text`.",
        "",
        "## OOD Sanity Slice",
        "",
        f"- Rows: {len(ood_rows)}",
        "- Source: simple PIL-rendered non-document images",
        "- Intended use: OOD abstention sanity only, not document understanding.",
        "",
        "## Caveat",
        "",
        "These examples prove absence only inside the synthetic render specification. They should be reported separately from source-dataset document QA.",
        "",
    ]
    write_text(path, "\n".join(lines))


def _metadata_payload(rows: list[dict], dataset_path: Path, image_dir: Path, kind: str) -> dict:
    return {
        "dataset": kind,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "row_count": len(rows),
        "benchmark_path": dataset_path.as_posix(),
        "benchmark_sha256": sha256_file(dataset_path),
        "image_dir": image_dir.as_posix(),
        "image_count": len(list(image_dir.glob("*.png"))),
        "source_dataset": "controlled_synthetic",
        "generator": "scripts/build_notfound_controlled_v0.py",
        "rows": [
            {
                "id": row["id"],
                "image_path": row["image_path"],
                "original_image_sha256": row["metadata"]["original_image_sha256"],
                "absence_check_result": row["metadata"]["absence_check_result"],
            }
            for row in rows
        ],
    }


def build_all(
    controlled_out: Path,
    controlled_meta: Path,
    controlled_image_dir: Path,
    spec_out: Path,
    ood_out: Path,
    ood_meta: Path,
    ood_image_dir: Path,
    controlled_rows: int = 50,
    ood_rows: int = 20,
) -> tuple[Path, Path, Path, Path, Path, Path]:
    controlled = build_controlled_rows(controlled_rows, controlled_image_dir)
    write_jsonl(controlled_out, controlled)
    write_json(controlled_meta, _metadata_payload(controlled, controlled_out, controlled_image_dir, "notfound_controlled_v0"))

    ood = build_ood_rows(ood_rows, ood_image_dir)
    write_jsonl(ood_out, ood)
    write_json(ood_meta, _metadata_payload(ood, ood_out, ood_image_dir, "notfound_ood_sanity_v0"))
    _write_spec(spec_out, controlled, ood)
    return controlled_out, controlled_meta, spec_out, ood_out, ood_meta, ood_image_dir


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controlled-out", default="data/notfound_controlled_v0.jsonl")
    parser.add_argument("--controlled-meta", default="data/notfound_controlled_v0.meta.json")
    parser.add_argument("--controlled-image-dir", default="data/notfound_controlled_v0_images")
    parser.add_argument("--spec-out", default="reports/notfound_controlled_v0_spec.md")
    parser.add_argument("--ood-out", default="data/notfound_ood_sanity_v0.jsonl")
    parser.add_argument("--ood-meta", default="data/notfound_ood_sanity_v0.meta.json")
    parser.add_argument("--ood-image-dir", default="data/notfound_ood_sanity_v0_images")
    parser.add_argument("--controlled-rows", type=int, default=50)
    parser.add_argument("--ood-rows", type=int, default=20)
    args = parser.parse_args()

    outputs = build_all(
        controlled_out=Path(args.controlled_out),
        controlled_meta=Path(args.controlled_meta),
        controlled_image_dir=Path(args.controlled_image_dir),
        spec_out=Path(args.spec_out),
        ood_out=Path(args.ood_out),
        ood_meta=Path(args.ood_meta),
        ood_image_dir=Path(args.ood_image_dir),
        controlled_rows=args.controlled_rows,
        ood_rows=args.ood_rows,
    )
    for output in outputs:
        print(f"wrote={output}")


if __name__ == "__main__":
    main()
