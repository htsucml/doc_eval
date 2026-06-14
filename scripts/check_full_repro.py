"""Preflight checks for optional full experimental reproduction."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


BENCHMARKS = [
    "data/docminibench_v0.jsonl",
    "data/notfound_controlled_v0.jsonl",
    "data/docvqa_manual_notfound_combined_expanded_v0_eval.jsonl",
    "data/notfound_ood_sanity_v0_eval_strict.jsonl",
]
SCRIPTS = [
    "scripts/eval_model.py",
    "scripts/aggregate_results.py",
    "scripts/finetune_lora.py",
    "scripts/analyze_abstention_margin.py",
    "scripts/run_full_repro.sh",
    "scripts/print_full_results.py",
]
TARGET_MODELS = ["smolvlm_500m", "smolvlm2_500m_video"]
REFERENCE_MODELS = ["smolvlm2_2_2b", "qwen2_5_vl_3b_instruct"]


def resolve_cache_root() -> Path:
    if os.environ.get("DOC_EVAL_CACHE_ROOT"):
        return Path(os.environ["DOC_EVAL_CACHE_ROOT"]).expanduser()
    workspace = Path("/workspace")
    if workspace.exists() and os.access(workspace, os.W_OK):
        return workspace / "hf_home"
    if os.environ.get("HF_HOME"):
        return Path(os.environ["HF_HOME"]).expanduser()
    return Path.home() / ".cache" / "doc_eval_hf"


def disk_free_gb(path: Path) -> float:
    path.mkdir(parents=True, exist_ok=True)
    usage = shutil.disk_usage(path)
    return usage.free / (1024**3)


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for raw in handle:
            if raw.strip():
                rows.append(json.loads(raw))
    return rows


def check_images(path: Path) -> list[str]:
    missing = []
    for row in load_jsonl(path):
        image_path = ROOT / row["image_path"]
        if not image_path.exists():
            missing.append(row["image_path"])
    return missing


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default=os.environ.get("FULL_DEVICE", "cuda"))
    parser.add_argument("--ref-models", default=os.environ.get("FULL_REF_MODELS", "0"))
    parser.add_argument("--min-cache-gb", type=float, default=float(os.environ.get("FULL_MIN_CACHE_GB", "25")))
    parser.add_argument("--min-output-gb", type=float, default=float(os.environ.get("FULL_MIN_OUTPUT_GB", "10")))
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    cache_root = resolve_cache_root()
    output_root = ROOT / "outputs" / "full_repro"
    report_root = ROOT / "reports" / "full_repro"
    cache_free = disk_free_gb(cache_root)
    output_free = disk_free_gb(output_root)
    report_free = disk_free_gb(report_root)

    if args.device == "cuda":
        try:
            import torch

            if not torch.cuda.is_available():
                errors.append("CUDA requested for full reproduction, but torch.cuda.is_available() is false.")
        except Exception as exc:
            if shutil.which("nvidia-smi") is None:
                errors.append(
                    f"CUDA requested, torch is not importable ({exc}), and nvidia-smi is not available. "
                    "Run on a CUDA host or set FULL_DEVICE=cpu for non-GPU checks."
                )
            else:
                probe = subprocess.run(["nvidia-smi", "-L"], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                if probe.returncode != 0:
                    errors.append(f"CUDA requested, torch is not importable ({exc}), and nvidia-smi failed: {probe.stdout.strip()}")
                else:
                    warnings.append(
                        "torch is not installed in the current environment, but nvidia-smi detected a GPU. "
                        "`make full` will install requirements-gpu.txt into this clone's .venv."
                    )

    required_cache_gb = args.min_cache_gb + (30 if args.ref_models == "1" else 0)
    if cache_free < required_cache_gb:
        errors.append(
            f"Cache filesystem has {cache_free:.1f} GiB free at {cache_root}, "
            f"below required {required_cache_gb:.1f} GiB for FULL_REF_MODELS={args.ref_models}."
        )
    if min(output_free, report_free) < args.min_output_gb:
        errors.append(
            f"Output/report filesystem has insufficient free space: outputs {output_free:.1f} GiB, "
            f"reports {report_free:.1f} GiB, required {args.min_output_gb:.1f} GiB."
        )

    for rel in BENCHMARKS + SCRIPTS + ["configs/models.yaml", "configs/eval_not_found_strict.yaml"]:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required path: {rel}")

    if (ROOT / "configs/models.yaml").exists():
        from src.utils.parsing import load_config_like_json

        models = load_config_like_json(str(ROOT / "configs/models.yaml"))["models"]
        for key in TARGET_MODELS + (REFERENCE_MODELS if args.ref_models == "1" else []):
            if key not in models:
                errors.append(f"Missing model key in configs/models.yaml: {key}")

    for rel in BENCHMARKS:
        path = ROOT / rel
        if path.exists():
            missing = check_images(path)
            if missing:
                errors.append(f"{rel} has {len(missing)} missing image paths; first: {missing[:3]}")

    if cache_root == Path.home() / ".cache" / "doc_eval_hf":
        warnings.append("Using user-cache default. Set DOC_EVAL_CACHE_ROOT=/workspace/hf_home on cloud runners when available.")

    print("# Full Reproduction Preflight")
    print(f"repo={ROOT}")
    print(f"device={args.device}")
    print(f"FULL_REF_MODELS={args.ref_models}")
    print(f"cache_root={cache_root}")
    print(f"cache_free_gib={cache_free:.1f}")
    print(f"output_root={output_root}")
    print(f"output_free_gib={output_free:.1f}")
    print(f"report_root={report_root}")
    print(f"report_free_gib={report_free:.1f}")
    print("")
    print("Estimated stages/runtime:")
    print("- tests + CPU smoke: minutes")
    print("- target zero-shot 500M evaluations: ~30-90 minutes with warm cache")
    print("- LoRA PoC default 100 steps + adapted eval: ~1-2 hours with warm cache")
    if args.ref_models == "1":
        print("- reference models enabled: add substantial download/runtime; skip if storage/time is unsafe")
    else:
        print("- reference models disabled by default; set FULL_REF_MODELS=1 to include them")
    for warning in warnings:
        print(f"warning: {warning}")
    if errors:
        print("")
        print("Preflight failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("")
    print("Preflight passed. Full reproduction can be started with `make full`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
