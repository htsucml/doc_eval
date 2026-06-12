from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.build_benchmark_v0 import build_benchmark
from src.datasets.jsonl_dataset import load_jsonl
from src.datasets.schema import validate_benchmark_row


def test_build_benchmark_is_deterministic_and_writes_metadata(tmp_path: Path) -> None:
    benchmark = tmp_path / "bench.jsonl"
    out_path, meta_path = build_benchmark(str(benchmark))

    rows = load_jsonl(out_path, validator=validate_benchmark_row)
    metadata = json.loads(Path(meta_path).read_text(encoding="utf-8"))

    assert len(rows) == 7
    assert metadata["row_count"] == 7
    assert metadata["fixture_mode"] is True
    assert metadata["benchmark_sha256"]
    assert rows[0]["id"] == "ocr-1"

    out_path_2, _ = build_benchmark(str(tmp_path / "bench2.jsonl"))
    assert Path(out_path).read_text(encoding="utf-8") == Path(out_path_2).read_text(encoding="utf-8")


def test_build_benchmark_fails_closed_on_invalid_slice_row(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from src.datasets.source_adapters import SOURCE_ADAPTERS
    from src.datasets.source_adapters.custom_not_found import CustomNotFoundSourceAdapter

    class BadAdapter(CustomNotFoundSourceAdapter):
        def _fixture_candidates(self, capability: str):  # type: ignore[override]
            return [
                {
                    "id": "bad-row",
                    "dataset": "fixture",
                    "image_path": "img.svg",
                    "question": "q",
                    "answers": ["NOT_FOUND"],
                    "capability": capability,
                    "answer_type": "abstain",
                    "metadata": {},
                    "extra": 1,
                }
            ]

    monkeypatch.setitem(SOURCE_ADAPTERS, "custom_not_found", BadAdapter())
    with pytest.raises(ValueError):
        build_benchmark(str(tmp_path / "bad.jsonl"))
