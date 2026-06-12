"""Aggregation helpers for benchmark-level reporting."""

from __future__ import annotations

from collections import defaultdict
from statistics import mean
from typing import Any, Dict, Iterable, List

from src.metrics.anls import anls_score
from src.metrics.calibration import calibration_buckets
from src.metrics.exact_match import exact_match, normalize_text
from src.metrics.relaxed_numeric import relaxed_numeric_score


def _not_found_false_answer(row: Dict[str, Any]) -> float:
    gold_is_not_found = any(normalize_text(answer) == "not_found" for answer in row["answers"])
    pred_is_not_found = normalize_text(row["parsed_answer"]) == "not_found"
    return 1.0 if gold_is_not_found and not pred_is_not_found else 0.0


def score_joined_rows(rows: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    scored = []
    for row in rows:
        exact = exact_match(row["parsed_answer"], row["answers"])
        scored.append(
            {
                **row,
                "exact_match": exact,
                "anls": anls_score(row["parsed_answer"], row["answers"]),
                "relaxed_numeric": relaxed_numeric_score(row["parsed_answer"], row["answers"]),
                "not_found_far": _not_found_false_answer(row),
            }
        )
    return scored


def summarize_scores(rows: List[Dict[str, Any]]) -> tuple[list[dict], list[dict]]:
    by_capability: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_capability[row["capability"]].append(row)

    summary_rows = [_summarize_bucket("overall", rows)]
    for capability in sorted(by_capability):
        summary_rows.append(_summarize_bucket(capability, by_capability[capability]))

    calibration = calibration_buckets(
        [row.get("confidence") for row in rows],
        [row["exact_match"] for row in rows],
    )
    return summary_rows, calibration


def _summarize_bucket(label: str, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not rows:
        return {
            "slice": label,
            "count": 0,
            "exact_match": 0.0,
            "anls": 0.0,
            "relaxed_numeric": 0.0,
            "not_found_false_answer_rate": 0.0,
            "avg_latency_s": 0.0,
        }
    return {
        "slice": label,
        "count": len(rows),
        "exact_match": round(mean(row["exact_match"] for row in rows), 4),
        "anls": round(mean(row["anls"] for row in rows), 4),
        "relaxed_numeric": round(mean(row["relaxed_numeric"] for row in rows), 4),
        "not_found_false_answer_rate": round(mean(row["not_found_far"] for row in rows), 4),
        "avg_latency_s": round(mean(float(row["latency_s"]) for row in rows), 4),
    }

