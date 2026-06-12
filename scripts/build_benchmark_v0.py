"""Build the tiny v0 fixture benchmark without external downloads."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.datasets.jsonl_dataset import write_jsonl
from src.datasets.schema import validate_benchmark_row
from src.datasets.vlmevalkit_placeholders import build_fixture_benchmark


def build_benchmark(out_path: str) -> None:
    rows = [validate_benchmark_row(row) for row in build_fixture_benchmark()]
    write_jsonl(out_path, rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data/fixtures/docminibench_sample.jsonl")
    args = parser.parse_args()
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    build_benchmark(args.out)
    print(f"wrote_benchmark={args.out}")


if __name__ == "__main__":
    main()
