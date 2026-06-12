"""Generate a lightweight next-steps memo from aggregated results."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.utils.io import write_text


def load_results(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def analyze(results_path: str, out_path: str) -> str:
    rows = load_results(results_path)
    slice_rows = [row for row in rows if row["slice"] != "overall"]
    weakest = sorted(slice_rows, key=lambda row: float(row["exact_match"]))[:3]
    weakest_names = ", ".join(row["slice"] for row in weakest) if weakest else "none"

    content = f"""# Next Steps v0

## Weakest observed slices

Current weakest slices by exact match: {weakest_names}.

## Dataset engineering next steps

- Replace the local fixture with explicit slice builders for DocVQA, InfoVQA, ChartQA, OCRBench-style OCR, and a custom not-found stress set.
- Preserve slice metadata so we can compare OCR exactness, layout binding, table lookup, chart reasoning, and abstention behavior separately.
- Add richer negative examples where the answer is absent but visually nearby distractors exist.

## Metrics to add beyond generic VQA

- Field-level span overlap or token-F1 for long OCR answers.
- Table-specific cell grounding and row/column retrieval metrics.
- Abstention-aware calibration metrics such as AUROC for answerable vs unanswerable detection.
- Efficiency reporting across latency, memory, image resolution, and prompt length.

## Model and adapter risks

- Small VLMs may fail from OCR fidelity limits before reasoning becomes the bottleneck.
- High-resolution document pages may exceed the default vision encoder granularity for sub-1B models.
- Real model APIs differ in chat templates, image preprocessing, and confidence availability, so adapter normalization will matter.

## Candidate improvement strategies

- OCR-assisted prompting with extracted spans or candidate fields.
- High-resolution tiling or crop-and-rerank for dense documents.
- Not-found calibration prompts and explicit abstention instruction tuning.
- LoRA or QLoRA adaptation targeted at weak capability slices.
- Distillation from a stronger document model into a compact VLM or VLM-plus-OCR hybrid.
"""
    write_text(out_path, content)
    return content


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    analyze(args.results, args.out)
    print(f"wrote_analysis={args.out}")


if __name__ == "__main__":
    main()
