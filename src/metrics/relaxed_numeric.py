"""Numeric parsing and relaxed accuracy."""

from __future__ import annotations

from src.metrics.normalization import parse_decimal


def parse_number(text: str) -> float | None:
    value = parse_decimal(text)
    if value is None:
        return None
    return float(value)


def relaxed_numeric_score(prediction: str, answers: list[str], rel_tol: float = 0.05, abs_tol: float = 1e-6) -> float:
    pred = parse_number(prediction)
    if pred is None:
        return 0.0
    for answer in answers:
        truth = parse_number(answer)
        if truth is None:
            continue
        tolerance = max(abs(truth) * rel_tol, abs_tol)
        if abs(pred - truth) <= tolerance:
            return 1.0
    return 0.0
