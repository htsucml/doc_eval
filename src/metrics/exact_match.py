"""Exact-match helpers."""

from __future__ import annotations

import re


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", str(text).strip()).casefold()


def exact_match(prediction: str, answers: list[str]) -> float:
    normalized_prediction = normalize_text(prediction)
    normalized_answers = {normalize_text(answer) for answer in answers}
    return 1.0 if normalized_prediction in normalized_answers else 0.0

