"""Build a deterministic v0 benchmark manifest without model inference."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.datasets.jsonl_dataset import write_jsonl
from src.datasets.registry import DATASET_SOURCE_ADAPTERS
from src.datasets.schema import validate_benchmark_row, validate_benchmark_rows
from src.datasets.source_adapters.base import SourceBuildOptions
from src.datasets.vlmevalkit_placeholders import describe_real_dataset_todos
from src.utils.hashing import sha256_file
from src.utils.io import write_json
from src.utils.parsing import load_config_like_json


def _stable_rank(slice_name: str, row: dict) -> str:
    return hashlib.sha256(f"{slice_name}:{row['id']}".encode("utf-8")).hexdigest()


def _select_rows_for_slice(slice_cfg: dict, options: SourceBuildOptions) -> list[dict]:
    capability = slice_cfg["capability"]
    candidates: list[dict] = []
    for source in slice_cfg["sources"]:
        if not source.get("enabled_by_default", True):
            continue
        adapter_name = source["adapter"]
        adapter = DATASET_SOURCE_ADAPTERS[adapter_name]
        for row in adapter.get_candidates(capability, options):
            if row["capability"] != capability:
                continue
            merged = validate_benchmark_row(
                {
                    **row,
                    "metadata": {
                        **row["metadata"],
                        "source_adapter": adapter_name,
                        "source_dataset": source["dataset"],
                        "source_slice": slice_cfg["name"],
                    },
                }
            )
            candidates.append(merged)
    ranked = sorted(candidates, key=lambda row: (_stable_rank(slice_cfg["name"], row), row["id"]))
    limit = int(slice_cfg.get("sample_size", len(ranked)))
    selected = ranked[:limit]
    if len(selected) != limit:
        raise ValueError(
            f"slice {slice_cfg['name']} requested {limit} rows but only found {len(selected)}"
        )
    return selected


def _load_slice_config(config_path: str | Path) -> dict:
    payload = load_config_like_json(config_path)
    if not isinstance(payload, dict) or "benchmark_slices" not in payload:
        raise ValueError("benchmark slice config must contain benchmark_slices")
    return payload


def build_benchmark(
    out_path: str,
    *,
    config_path: str = "configs/benchmark_slices.yaml",
    fixture_mode: bool = True,
    allow_downloads: bool = False,
) -> tuple[str, str]:
    config = _load_slice_config(config_path)
    options = SourceBuildOptions(
        fixture_mode=fixture_mode,
        allow_downloads=allow_downloads,
    )
    rows: list[dict] = []
    for slice_cfg in config["benchmark_slices"]:
        rows.extend(_select_rows_for_slice(slice_cfg, options))
    rows = validate_benchmark_rows(rows)
    write_jsonl(out_path, rows)
    meta_path = str(Path(out_path).with_suffix(".meta.json"))
    write_json(
        meta_path,
        {
            "benchmark_name": config.get("benchmark_name", "docminibench_v0"),
            "benchmark_path": str(out_path),
            "benchmark_sha256": sha256_file(out_path),
            "row_count": len(rows),
            "fixture_mode": fixture_mode,
            "allow_downloads": allow_downloads,
            "slice_config_path": str(config_path),
            "slice_names": [slice_cfg["name"] for slice_cfg in config["benchmark_slices"]],
            "todos": describe_real_dataset_todos(),
        },
    )
    return out_path, meta_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data/fixtures/docminibench_sample.jsonl")
    parser.add_argument("--config", default="configs/benchmark_slices.yaml")
    parser.add_argument(
        "--mode",
        choices=("fixture", "real"),
        default="fixture",
        help="Fixture mode is the safe default; real mode still requires explicit source enablement.",
    )
    parser.add_argument(
        "--allow-downloads",
        action="store_true",
        help="Required before any real adapter is allowed to fetch or materialize data.",
    )
    args = parser.parse_args()
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    out_path, meta_path = build_benchmark(
        args.out,
        config_path=args.config,
        fixture_mode=args.mode == "fixture",
        allow_downloads=args.allow_downloads,
    )
    print(f"wrote_benchmark={args.out}")
    print(f"wrote_metadata={meta_path}")


if __name__ == "__main__":
    main()
