from __future__ import annotations

from src.metrics.anls import anls_score
from src.metrics.calibration import calibration_buckets
from src.metrics.exact_match import exact_match
from src.metrics.relaxed_numeric import relaxed_numeric_score


def test_exact_match_is_case_insensitive() -> None:
    assert exact_match("march", ["March"]) == 1.0


def test_anls_gives_partial_credit() -> None:
    assert anls_score("inv001", ["inv-001"]) > 0.5


def test_relaxed_numeric_accepts_small_relative_error() -> None:
    assert relaxed_numeric_score("10.4", ["10"]) == 1.0


def test_calibration_buckets_return_counts() -> None:
    buckets = calibration_buckets([0.9, 0.8, None], [1.0, 0.0, 1.0], bins=2)
    assert sum(bucket["count"] for bucket in buckets) == 2

