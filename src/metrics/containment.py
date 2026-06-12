"""Containment-style scoring for generative answers."""

from __future__ import annotations

from decimal import Decimal
import re

from src.metrics.normalization import (
    is_not_found_response,
    is_numeric_answer_type,
    normalize_answer,
    normalize_text,
    parse_decimal,
)


_NUMERIC_PATTERN = re.compile(r"[-+]?\$?\d[\d,]*(?:\.\d+)?%?")


def _contains_text_answer(prediction: str, answer: str, answer_type: str | None) -> bool:
    normalized_answer = normalize_answer(answer, answer_type=answer_type)
    normalized_prediction = normalize_text(prediction)
    if not normalized_answer:
        return False
    return normalized_answer in normalized_prediction


def _numeric_values(text: str) -> list[Decimal]:
    values = []
    for match in _NUMERIC_PATTERN.finditer(str(text or "")):
        value = parse_decimal(match.group(0))
        if value is not None:
            values.append(value)
    return values


def _contains_numeric_answer(prediction: str, answer: str) -> bool:
    gold = parse_decimal(answer)
    if gold is None:
        return False
    return any(value == gold for value in _numeric_values(prediction))


def answer_in_output(prediction: str, answers: list[str], answer_type: str | None = None) -> float:
    """Return 1.0 when any normalized gold answer appears in the generated output.

    This is intentionally separate from strict exact match. It gives credit when a
    generative VLM wraps the final value in a sentence, while exact match remains
    the conservative primary metric.
    """

    if any(is_not_found_response(answer) for answer in answers):
        return 1.0 if is_not_found_response(prediction) else 0.0

    for answer in answers:
        if is_numeric_answer_type(answer_type):
            if _contains_numeric_answer(prediction, answer):
                return 1.0
            continue
        if _contains_text_answer(prediction, answer, answer_type) or _contains_numeric_answer(prediction, answer):
            return 1.0
    return 0.0
