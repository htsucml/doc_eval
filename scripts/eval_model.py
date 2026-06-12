"""Run one adapter over a benchmark and emit predictions + metadata."""

from __future__ import annotations

import argparse
import os
import platform
import random
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.adapters.dummy import DummyAdapter
from src.adapters.internvl import InternVLAdapter
from src.adapters.llava_ov import LlavaOVAdapter
from src.adapters.smolvlm import SmolVLMAdapter
from src.datasets.jsonl_dataset import load_jsonl, write_jsonl
from src.datasets.schema import validate_benchmark_row, validate_prediction_row
from src.utils.hashing import sha256_file
from src.utils.io import write_json
from src.utils.parsing import load_config_like_json


ADAPTERS = {
    "dummy": DummyAdapter,
    "smolvlm": SmolVLMAdapter,
    "internvl": InternVLAdapter,
    "llava_ov": LlavaOVAdapter,
}


def get_git_commit() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return None
    return result.stdout.strip()


def optional_version(module_name: str) -> str | None:
    try:
        module = __import__(module_name)
    except Exception:
        return None
    return getattr(module, "__version__", None)


def load_adapter(model_name: str, allow_real_models: bool, runtime: dict | None = None):
    model_cfg = load_config_like_json("configs/models.yaml")["models"][model_name]
    adapter_name = model_cfg["adapter"]
    if model_cfg.get("allow_real_models_required") and not allow_real_models:
        raise RuntimeError(
            f"Model '{model_name}' is gated. Re-run with --allow-real-models to enable lazy loading."
        )
    adapter_cls = ADAPTERS[adapter_name]
    adapter = adapter_cls(model_cfg)
    adapter.runtime = runtime or {}
    adapter.load()
    return adapter, model_cfg


def run_eval(
    model_name: str,
    benchmark_path: str,
    out_path: str,
    allow_real_models: bool = False,
    device: str = "cpu",
    limit: int | None = None,
) -> tuple[str, str]:
    random.seed(7)
    benchmark_rows = load_jsonl(benchmark_path, validator=validate_benchmark_row)
    if limit is not None:
        benchmark_rows = benchmark_rows[:limit]
    adapter, model_cfg = load_adapter(
        model_name,
        allow_real_models,
        runtime={"device": device, "seed": 7},
    )

    run_id = f"{model_name}-{uuid.uuid4().hex[:8]}"
    predictions = []
    for sample in benchmark_rows:
        try:
            result = adapter.generate(sample)
            payload = {
                "run_id": run_id,
                "model_id": adapter.model_id,
                "sample_id": sample["id"],
                **result,
            }
        except Exception as exc:
            payload = {
                "run_id": run_id,
                "model_id": adapter.model_id,
                "sample_id": sample["id"],
                "raw_output": "",
                "parsed_answer": "",
                "confidence": None,
                "latency_s": 0.0,
                "error": str(exc),
                "inference_config": {},
            }
        predictions.append(validate_prediction_row(payload))

    write_jsonl(out_path, predictions)
    meta_path = str(Path(out_path).with_suffix(".meta.json"))
    metadata = {
        "run_id": run_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": get_git_commit(),
        "model_name": model_name,
        "model_config": model_cfg,
        "benchmark_path": benchmark_path,
        "benchmark_sha256": sha256_file(benchmark_path),
        "python_version": platform.python_version(),
        "torch_version": optional_version("torch"),
        "device": device,
        "seed": 7,
        "limit": limit,
        "cwd": os.getcwd(),
    }
    write_json(meta_path, metadata)
    return out_path, meta_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--benchmark", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--device", choices=["cpu", "cuda", "mps"], default="cpu")
    parser.add_argument("--allow-real-models", action="store_true")
    args = parser.parse_args()

    out_path, meta_path = run_eval(
        model_name=args.model,
        benchmark_path=args.benchmark,
        out_path=args.out,
        allow_real_models=args.allow_real_models,
        device=args.device,
        limit=args.limit,
    )
    print(f"wrote_predictions={out_path}")
    print(f"wrote_metadata={meta_path}")


if __name__ == "__main__":
    main()
