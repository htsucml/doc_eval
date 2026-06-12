from __future__ import annotations

import csv
from pathlib import Path

from scripts.aggregate_results import aggregate
from scripts.analyze_next_steps import analyze
from scripts.build_benchmark_v0 import build_benchmark
from scripts.eval_model import run_eval
from scripts.export_errors import export_errors


def test_aggregate_outputs_summary(tmp_path: Path) -> None:
    benchmark = tmp_path / "bench.jsonl"
    preds = tmp_path / "preds.jsonl"
    csv_out = tmp_path / "results.csv"
    markdown_out = tmp_path / "results.md"
    errors_out = tmp_path / "errors.md"
    next_steps_out = tmp_path / "next_steps.md"
    build_benchmark(str(benchmark))
    run_eval("dummy", str(benchmark), str(preds))
    summary_rows, calibration_rows = aggregate(
        str(preds),
        str(benchmark),
        str(csv_out),
        str(markdown_out),
    )
    export_errors(str(preds), str(benchmark), str(errors_out))
    analyze(str(csv_out), str(next_steps_out), errors_path=str(errors_out))

    assert summary_rows[0]["slice_type"] == "overall"
    assert any(row["slice_type"] == "capability" and row["slice_name"] == "not_found" for row in summary_rows)
    assert any(row["slice_type"] == "answer_type" and row["slice_name"] == "currency" for row in summary_rows)
    assert "answer_in_output" in summary_rows[0]
    assert csv_out.exists()
    assert markdown_out.exists()
    assert errors_out.exists()
    assert next_steps_out.exists()
    assert calibration_rows

    csv_rows = list(csv.DictReader(csv_out.open("r", encoding="utf-8", newline="")))
    assert any(row["slice_type"] == "answer_type" for row in csv_rows)
    assert "false_answer_on_unanswerable" in errors_out.read_text(encoding="utf-8")
    assert "Most common failure modes" in next_steps_out.read_text(encoding="utf-8")
