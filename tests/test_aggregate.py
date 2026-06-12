from __future__ import annotations

from pathlib import Path

from scripts.aggregate_results import aggregate
from scripts.build_benchmark_v0 import build_benchmark
from scripts.eval_model import run_eval


def test_aggregate_outputs_summary(tmp_path: Path) -> None:
    benchmark = tmp_path / "bench.jsonl"
    preds = tmp_path / "preds.jsonl"
    csv_out = tmp_path / "results.csv"
    markdown_out = tmp_path / "results.md"
    build_benchmark(str(benchmark))
    run_eval("dummy", str(benchmark), str(preds))
    summary_rows, calibration_rows = aggregate(
        str(preds),
        str(benchmark),
        str(csv_out),
        str(markdown_out),
    )
    assert summary_rows[0]["slice"] == "overall"
    assert csv_out.exists()
    assert markdown_out.exists()
    assert calibration_rows
