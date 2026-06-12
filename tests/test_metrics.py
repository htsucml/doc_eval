from __future__ import annotations

from src.metrics.anls import anls_score
from src.metrics.calibration import calibration_buckets
from src.metrics.containment import answer_in_output
from src.metrics.exact_match import exact_match
from src.metrics.normalization import normalize_answer
from src.metrics.relaxed_numeric import relaxed_numeric_score


def test_exact_match_is_case_insensitive() -> None:
    assert exact_match("march", ["March"]) == 1.0


def test_exact_match_normalizes_ids() -> None:
    assert exact_match("inv 001", ["INV-001"], answer_type="code") == 1.0


def test_exact_match_normalizes_dates() -> None:
    assert exact_match("March 5, 2024", ["2024-03-05"], answer_type="date") == 1.0


def test_exact_match_normalizes_not_found_variants() -> None:
    assert exact_match("N/A", ["NOT_FOUND"], answer_type="abstain") == 1.0


def test_anls_gives_partial_credit() -> None:
    assert anls_score("inv001", ["inv-001"], answer_type="code") > 0.5


def test_relaxed_numeric_accepts_small_relative_error() -> None:
    assert relaxed_numeric_score("10.4", ["10"]) == 1.0


def test_relaxed_numeric_parses_currency() -> None:
    assert relaxed_numeric_score("$42.00", ["42"]) == 1.0


def test_calibration_buckets_return_counts() -> None:
    buckets = calibration_buckets([0.9, 0.8, None], [1.0, 0.0, 1.0], bins=2)
    assert sum(bucket["count"] for bucket in buckets) == 2


def test_normalize_answer_normalizes_currency() -> None:
    assert normalize_answer("$1,250.00", answer_type="currency") == "1250"


def test_answer_in_output_accepts_sentence_wrapped_answer() -> None:
    assert answer_in_output("The final answer is March.", ["March"], answer_type="short_text") == 1.0


def test_answer_in_output_finds_numeric_answer_later_in_output() -> None:
    assert answer_in_output("103.7 - 103.13\nAnswer: 0.57.", ["0.57"], answer_type="number") == 1.0


def test_answer_in_output_does_not_substring_match_numeric_answers() -> None:
    assert answer_in_output("28.", ["2"], answer_type="integer") == 0.0


def test_answer_in_output_keeps_not_found_strict() -> None:
    assert answer_in_output("I cannot find it.", ["NOT_FOUND"], answer_type="abstain") == 0.0
