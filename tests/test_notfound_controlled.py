from __future__ import annotations

import json
from pathlib import Path

from scripts.build_notfound_controlled_v0 import build_all
from src.datasets.jsonl_dataset import load_jsonl
from src.datasets.schema import validate_benchmark_row
from src.utils.hashing import sha256_file


def test_build_notfound_controlled_writes_valid_rows_and_absence_evidence(tmp_path: Path) -> None:
    controlled_out = tmp_path / "data" / "notfound_controlled_v0.jsonl"
    controlled_meta = tmp_path / "data" / "notfound_controlled_v0.meta.json"
    controlled_image_dir = tmp_path / "data" / "notfound_controlled_v0_images"
    spec_out = tmp_path / "reports" / "notfound_controlled_v0_spec.md"
    ood_out = tmp_path / "data" / "notfound_ood_sanity_v0.jsonl"
    ood_meta = tmp_path / "data" / "notfound_ood_sanity_v0.meta.json"
    ood_image_dir = tmp_path / "data" / "notfound_ood_sanity_v0_images"

    build_all(
        controlled_out=controlled_out,
        controlled_meta=controlled_meta,
        controlled_image_dir=controlled_image_dir,
        spec_out=spec_out,
        ood_out=ood_out,
        ood_meta=ood_meta,
        ood_image_dir=ood_image_dir,
        controlled_rows=40,
        ood_rows=20,
    )

    rows = load_jsonl(controlled_out, validator=validate_benchmark_row)
    metadata = json.loads(controlled_meta.read_text(encoding="utf-8"))

    assert len(rows) == 40
    assert metadata["row_count"] == 40
    assert metadata["benchmark_sha256"] == sha256_file(controlled_out)
    assert spec_out.exists()

    for row in rows:
        row_meta = row["metadata"]
        image_path = Path(row["image_path"])
        rendered_text = row_meta["rendered_text"].casefold()
        absent_field = row_meta["absent_field"]
        absent_value = row_meta["absent_value"]

        assert row_meta["source_dataset"] == "controlled_synthetic"
        assert row_meta["source_slice"] == "notfound_controlled_v0"
        assert row_meta["document_type"]
        assert row_meta["present_fields"]
        assert row_meta["absent_question_template_id"]
        assert row_meta["absence_evidence_type"] == "controlled_render_negative"
        assert row_meta["absence_check_result"] is True
        assert image_path.exists()
        assert sha256_file(image_path) == row_meta["original_image_sha256"]
        assert absent_field not in row_meta["present_fields"]
        assert absent_field.casefold() not in rendered_text
        assert absent_value.casefold() not in rendered_text


def test_build_notfound_ood_sanity_is_labeled_non_document(tmp_path: Path) -> None:
    build_all(
        controlled_out=tmp_path / "controlled.jsonl",
        controlled_meta=tmp_path / "controlled.meta.json",
        controlled_image_dir=tmp_path / "controlled_images",
        spec_out=tmp_path / "spec.md",
        ood_out=tmp_path / "ood.jsonl",
        ood_meta=tmp_path / "ood.meta.json",
        ood_image_dir=tmp_path / "ood_images",
        controlled_rows=40,
        ood_rows=20,
    )

    rows = load_jsonl(tmp_path / "ood.jsonl", validator=validate_benchmark_row)

    assert len(rows) == 20
    for row in rows:
        assert row["metadata"]["source_slice"] == "notfound_ood_sanity_v0"
        assert row["metadata"]["document_type"] == "non_document_ood"
        assert row["metadata"]["absence_evidence_type"] == "non_document_ood_sanity"
        assert Path(row["image_path"]).exists()
