"""Strict benchmark and prediction schemas."""

from __future__ import annotations

from typing import Any, Dict
from typing import Any, Dict, Iterable


CAPABILITIES = {
    "ocr_exact",
    "layout_binding",
    "table_lookup",
    "chart_numeric",
    "domain_terms",
    "not_found",
    "robustness_optional",
}

BENCHMARK_REQUIRED_KEYS = {
    "id",
    "dataset",
    "image_path",
    "question",
    "answers",
    "capability",
    "answer_type",
    "metadata",
}

PREDICTION_REQUIRED_KEYS = {
    "run_id",
    "model_id",
    "sample_id",
    "raw_output",
    "parsed_answer",
    "confidence",
    "latency_s",
    "error",
    "inference_config",
}


def _ensure_keys(row: Dict[str, Any], required: set[str], label: str) -> None:
    missing = sorted(required - set(row))
    extra = sorted(set(row) - required)
    if missing or extra:
        raise ValueError(f"{label} schema mismatch: missing={missing}, extra={extra}")


def validate_benchmark_row(row: Dict[str, Any]) -> Dict[str, Any]:
    _ensure_keys(row, BENCHMARK_REQUIRED_KEYS, "benchmark")
    for key in ("id", "dataset", "image_path", "question", "answer_type"):
        if not isinstance(row[key], str) or not row[key].strip():
            raise ValueError(f"benchmark.{key} must be a non-empty string")
    if not isinstance(row["answers"], list) or not row["answers"] or not all(
        isinstance(item, str) for item in row["answers"]
    ):
        raise ValueError("benchmark.answers must be a non-empty list[str]")
    if row["capability"] not in CAPABILITIES:
        raise ValueError(f"unsupported capability: {row['capability']}")
    if not isinstance(row["metadata"], dict):
        raise ValueError("benchmark.metadata must be a dict")
    return row


def validate_benchmark_rows(rows: Iterable[Dict[str, Any]]) -> list[Dict[str, Any]]:
    validated = [validate_benchmark_row(row) for row in rows]
    ids = [row["id"] for row in validated]
    if len(ids) != len(set(ids)):
        raise ValueError("benchmark ids must be unique")
    return validated


def validate_prediction_row(row: Dict[str, Any]) -> Dict[str, Any]:
    _ensure_keys(row, PREDICTION_REQUIRED_KEYS, "prediction")
    for key in ("run_id", "model_id", "sample_id", "raw_output", "parsed_answer"):
        if not isinstance(row[key], str):
            raise ValueError(f"prediction.{key} must be a string")
    if row["confidence"] is not None and not isinstance(row["confidence"], (int, float)):
        raise ValueError("prediction.confidence must be numeric or null")
    if not isinstance(row["latency_s"], (int, float)):
        raise ValueError("prediction.latency_s must be numeric")
    if row["error"] is not None and not isinstance(row["error"], str):
        raise ValueError("prediction.error must be str or null")
    if not isinstance(row["inference_config"], dict):
        raise ValueError("prediction.inference_config must be a dict")
    return row
