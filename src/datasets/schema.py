"""Strict benchmark and prediction schemas."""

from __future__ import annotations

from typing import Any, Dict


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
    if not isinstance(row["answers"], list) or not row["answers"] or not all(
        isinstance(item, str) for item in row["answers"]
    ):
        raise ValueError("benchmark.answers must be a non-empty list[str]")
    if row["capability"] not in CAPABILITIES:
        raise ValueError(f"unsupported capability: {row['capability']}")
    if not isinstance(row["metadata"], dict):
        raise ValueError("benchmark.metadata must be a dict")
    if "ocr_text" in row["metadata"] and not isinstance(row["metadata"]["ocr_text"], str):
        raise ValueError("benchmark.metadata.ocr_text must be str when present")
    return row


def validate_prediction_row(row: Dict[str, Any]) -> Dict[str, Any]:
    _ensure_keys(row, PREDICTION_REQUIRED_KEYS, "prediction")
    if row["confidence"] is not None and not isinstance(row["confidence"], (int, float)):
        raise ValueError("prediction.confidence must be numeric or null")
    if not isinstance(row["latency_s"], (int, float)):
        raise ValueError("prediction.latency_s must be numeric")
    if row["error"] is not None and not isinstance(row["error"], str):
        raise ValueError("prediction.error must be str or null")
    if not isinstance(row["inference_config"], dict):
        raise ValueError("prediction.inference_config must be a dict")
    return row
