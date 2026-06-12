"""Aggregation helpers for benchmark-level reporting."""

from __future__ import annotations

from collections import defaultdict
from statistics import mean
from typing import Any, Dict, Iterable, List

from src.metrics.anls import anls_score
from src.metrics.calibration import calibration_buckets
from src.metrics.exact_match import exact_match
from src.metrics.normalization import is_anls_applicable, is_not_found_response, is_numeric_answer_type, normalize_text
from src.metrics.relaxed_numeric import parse_number, relaxed_numeric_score


def _gold_is_not_found(row: Dict[str, Any]) -> bool:
    return any(is_not_found_response(answer) for answer in row["answers"])


def _pred_is_not_found(row: Dict[str, Any]) -> bool:
    return is_not_found_response(row["parsed_answer"])


def failure_type(row: Dict[str, Any]) -> str | None:
    if row.get("exact_match", 0.0) >= 1.0:
        return None
    if row.get("error"):
        return "parse_error"
    if _gold_is_not_found(row) and not _pred_is_not_found(row):
        return "false_answer_on_unanswerable"
    if not _gold_is_not_found(row) and (_pred_is_not_found(row) or not normalize_text(row["parsed_answer"])):
        return "missing_answer"
    if row.get("numeric_applicable"):
        if parse_number(row["parsed_answer"]) is None:
            return "parse_error"
        return "numeric_mismatch"
    return "exact_mismatch"


def failure_hint(row: Dict[str, Any]) -> str:
    hint_type = row.get("failure_type") or failure_type(row)
    if hint_type == "false_answer_on_unanswerable":
        return "The model answered instead of abstaining on an unanswerable sample."
    if hint_type == "missing_answer":
        return "The prediction abstained or returned an empty answer for an answerable sample."
    if hint_type == "numeric_mismatch":
        return "The prediction found a number, but it misses the target beyond relaxed tolerance."
    if hint_type == "parse_error":
        return "The prediction failed schema or parsing expectations for this sample."
    return "The prediction is textually different from the gold answer after normalization."


def score_joined_rows(rows: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    scored = []
    for row in rows:
        answer_type = row.get("answer_type")
        exact = exact_match(row["parsed_answer"], row["answers"], answer_type=answer_type)
        numeric_applicable = is_numeric_answer_type(answer_type) or (
            answer_type is None and any(parse_number(answer) is not None for answer in row["answers"])
        )
        anls_applicable = is_anls_applicable(answer_type)
        scored_row = {
            **row,
            "exact_match": exact,
            "anls": anls_score(row["parsed_answer"], row["answers"], answer_type=answer_type) if anls_applicable else None,
            "anls_applicable": anls_applicable,
            "relaxed_numeric": relaxed_numeric_score(row["parsed_answer"], row["answers"]) if numeric_applicable else None,
            "numeric_applicable": numeric_applicable,
            "gold_not_found": _gold_is_not_found(row),
            "pred_not_found": _pred_is_not_found(row),
            "not_found_false_answer": 1.0 if _gold_is_not_found(row) and not _pred_is_not_found(row) else None,
        }
        scored_row["failure_type"] = failure_type(scored_row)
        scored_row["failure_hint"] = failure_hint(scored_row)
        scored.append(scored_row)
    return scored


def summarize_scores(rows: List[Dict[str, Any]]) -> tuple[list[dict], list[dict]]:
    by_capability: dict[str, list[dict]] = defaultdict(list)
    by_answer_type: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_capability[row["capability"]].append(row)
        by_answer_type[row["answer_type"]].append(row)

    summary_rows = [_summarize_bucket("overall", "overall", rows)]
    for capability in sorted(by_capability):
        summary_rows.append(_summarize_bucket("capability", capability, by_capability[capability]))
    for answer_type in sorted(by_answer_type):
        summary_rows.append(_summarize_bucket("answer_type", answer_type, by_answer_type[answer_type]))

    calibration = calibration_buckets(
        [row.get("confidence") for row in rows],
        [row["exact_match"] for row in rows],
    )
    return summary_rows, calibration


def _mean_or_none(values: list[float]) -> float | None:
    return round(mean(values), 4) if values else None


def _summarize_bucket(slice_type: str, slice_name: str, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not rows:
        return {
            "slice_type": slice_type,
            "slice_name": slice_name,
            "slice": slice_name,
            "count": 0,
            "exact_match": 0.0,
            "anls": None,
            "anls_applicable_count": 0,
            "relaxed_numeric": None,
            "relaxed_numeric_applicable_count": 0,
            "not_found_false_answer_rate": None,
            "not_found_applicable_count": 0,
            "avg_latency_s": 0.0,
            "error_rate": 0.0,
        }

    anls_values = [float(row["anls"]) for row in rows if row["anls"] is not None]
    numeric_values = [float(row["relaxed_numeric"]) for row in rows if row["relaxed_numeric"] is not None]
    not_found_values = [float(row["not_found_false_answer"]) for row in rows if row["not_found_false_answer"] is not None]
    return {
        "slice_type": slice_type,
        "slice_name": slice_name,
        "slice": slice_name,
        "count": len(rows),
        "exact_match": round(mean(row["exact_match"] for row in rows), 4),
        "anls": _mean_or_none(anls_values),
        "anls_applicable_count": len(anls_values),
        "relaxed_numeric": _mean_or_none(numeric_values),
        "relaxed_numeric_applicable_count": len(numeric_values),
        "not_found_false_answer_rate": _mean_or_none(not_found_values),
        "not_found_applicable_count": len(not_found_values),
        "avg_latency_s": round(mean(float(row["latency_s"]) for row in rows), 4),
        "error_rate": round(mean(1.0 if row.get("error") else 0.0 for row in rows), 4),
    }
