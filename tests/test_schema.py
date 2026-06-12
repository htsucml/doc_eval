from __future__ import annotations

import pytest

from src.datasets.schema import (
    validate_benchmark_row,
    validate_benchmark_rows,
    validate_prediction_row,
)


def test_validate_benchmark_row_accepts_valid_row() -> None:
    row = {
        "id": "x",
        "dataset": "fixture",
        "image_path": "img.svg",
        "question": "q",
        "answers": ["a"],
        "capability": "ocr_exact",
        "answer_type": "short_text",
        "metadata": {"ocr_text": "hello"},
    }
    assert validate_benchmark_row(row)["id"] == "x"


def test_validate_benchmark_row_rejects_extra_keys() -> None:
    row = {
        "id": "x",
        "dataset": "fixture",
        "image_path": "img.svg",
        "question": "q",
        "answers": ["a"],
        "capability": "ocr_exact",
        "answer_type": "short_text",
        "metadata": {},
        "extra": 1,
    }
    with pytest.raises(ValueError):
        validate_benchmark_row(row)


def test_validate_prediction_row_rejects_bad_confidence() -> None:
    row = {
        "run_id": "r",
        "model_id": "m",
        "sample_id": "s",
        "raw_output": "x",
        "parsed_answer": "x",
        "confidence": "high",
        "latency_s": 0.1,
        "error": None,
        "inference_config": {},
    }
    with pytest.raises(ValueError):
        validate_prediction_row(row)


def test_validate_benchmark_row_rejects_non_string_ocr_text() -> None:
    row = {
        "id": "x",
        "dataset": "fixture",
        "image_path": "img.svg",
        "question": "q",
        "answers": ["a"],
        "capability": "ocr_exact",
        "answer_type": "short_text",
        "metadata": {"ocr_text": 7},
    }
    with pytest.raises(ValueError):
        validate_benchmark_row(row)


def test_validate_benchmark_rows_rejects_duplicate_ids() -> None:
    row = {
        "id": "x",
        "dataset": "fixture",
        "image_path": "img.svg",
        "question": "q",
        "answers": ["a"],
        "capability": "ocr_exact",
        "answer_type": "short_text",
        "metadata": {},
    }
    with pytest.raises(ValueError):
        validate_benchmark_rows([row, row.copy()])
