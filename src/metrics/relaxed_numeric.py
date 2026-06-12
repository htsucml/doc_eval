"""Numeric parsing and relaxed accuracy."""

from __future__ import annotations

import re


def parse_number(text: str) -> float | None:
    match = re.search(r"[-+]?\d[\d,]*\.?\d*", str(text))
    if not match:
        return None
    cleaned = match.group(0).replace(",", "")
    try:
        return float(cleaned)
    except ValueError:
        return None


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

