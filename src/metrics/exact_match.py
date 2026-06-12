"""Exact-match helpers."""

from __future__ import annotations

from src.metrics.normalization import normalize_answer


def normalize_text(text: str, answer_type: str | None = None) -> str:
    return normalize_answer(text, answer_type=answer_type)


def exact_match(prediction: str, answers: list[str], answer_type: str | None = None) -> float:
    normalized_prediction = normalize_text(prediction, answer_type=answer_type)
    normalized_answers = {normalize_text(answer, answer_type=answer_type) for answer in answers}
    return 1.0 if normalized_prediction in normalized_answers else 0.0
