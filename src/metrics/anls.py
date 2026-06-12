"""ANLS-style string similarity."""

from __future__ import annotations

from src.metrics.normalization import normalize_answer


def _levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, char_a in enumerate(a, start=1):
        current = [i]
        for j, char_b in enumerate(b, start=1):
            insert_cost = current[j - 1] + 1
            delete_cost = prev[j] + 1
            replace_cost = prev[j - 1] + (char_a != char_b)
            current.append(min(insert_cost, delete_cost, replace_cost))
        prev = current
    return prev[-1]


def anls_score(
    prediction: str,
    answers: list[str],
    threshold: float = 0.5,
    answer_type: str | None = None,
) -> float:
    pred = normalize_answer(prediction, answer_type=answer_type)
    best = 0.0
    for answer in answers:
        truth = normalize_answer(answer, answer_type=answer_type)
        if not truth and not pred:
            return 1.0
        denom = max(len(pred), len(truth), 1)
        score = 1.0 - (_levenshtein(pred, truth) / denom)
        best = max(best, score)
    return best if best >= threshold else 0.0
