from __future__ import annotations

from pathlib import Path

from scripts.build_benchmark_v0 import build_benchmark
from scripts.eval_model import run_eval
from src.datasets.jsonl_dataset import load_jsonl
from src.datasets.schema import validate_prediction_row


def test_dummy_eval_produces_predictions(tmp_path: Path) -> None:
    benchmark = tmp_path / "bench.jsonl"
    preds = tmp_path / "preds.jsonl"
    build_benchmark(str(benchmark))
    out_path, meta_path = run_eval("dummy", str(benchmark), str(preds))
    rows = load_jsonl(out_path, validator=validate_prediction_row)
    assert len(rows) == 7
    assert any(row["sample_id"] == "notfound-1" for row in rows)
    assert Path(meta_path).exists()


def test_dummy_eval_limit_and_device_metadata(tmp_path: Path) -> None:
    benchmark = tmp_path / "bench.jsonl"
    preds = tmp_path / "preds.jsonl"
    build_benchmark(str(benchmark))
    out_path, meta_path = run_eval("dummy", str(benchmark), str(preds), device="cpu", limit=3)
    rows = load_jsonl(out_path, validator=validate_prediction_row)
    assert len(rows) == 3
    assert '"device": "cpu"' in Path(meta_path).read_text(encoding="utf-8")
