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


def load_error_rows(path: str | None) -> list[dict]:
    if not path:
        return []
    target = Path(path)
    if not target.exists():
        return []
    lines = target.read_text(encoding="utf-8").splitlines()
    table_lines = [line for line in lines if line.startswith("|")]
    if len(table_lines) < 3:
        return []
    headers = [part.strip() for part in table_lines[0].strip("|").split("|")]
    rows: list[dict] = []
    for line in table_lines[2:]:
        values = [part.strip() for part in line.strip("|").split("|")]
        if len(values) != len(headers):
            continue
        rows.append(dict(zip(headers, values)))
    return rows


def infer_error_path(results_path: str) -> str | None:
    path = Path(results_path)
    candidates = [
        path.with_name(path.name.replace("results", "errors")).with_suffix(".md"),
        path.with_name("dummy_errors.md"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return None


def _to_float(row: dict, key: str) -> float:
    value = row.get(key, "")
    return float(value) if value not in ("", None) else 0.0


def analyze(results_path: str, out_path: str, errors_path: str | None = None) -> str:
    rows = load_results(results_path)
    errors = load_error_rows(errors_path or infer_error_path(results_path))
    slice_rows = [row for row in rows if row.get("slice_type") in {"capability", "answer_type"}]
    failing_slices = [row for row in slice_rows if _to_float(row, "exact_match") < 1.0]
    weakest_pool = failing_slices or slice_rows
    weakest = sorted(weakest_pool, key=lambda row: (_to_float(row, "exact_match"), row["slice_name"]))[:5]
    weakest_names = ", ".join(f"{row['slice_type']}:{row['slice_name']}" for row in weakest) if weakest else "none"

    capability_errors: dict[str, int] = {}
    failure_type_counts: dict[str, int] = {}
    for row in errors:
        capability_errors[row["capability"]] = capability_errors.get(row["capability"], 0) + 1
        failure_type_counts[row["failure_type"]] = failure_type_counts.get(row["failure_type"], 0) + 1

    top_capability_errors = sorted(capability_errors.items(), key=lambda item: (-item[1], item[0]))[:3]
    top_failure_types = sorted(failure_type_counts.items(), key=lambda item: (-item[1], item[0]))[:4]
    capability_error_summary = ", ".join(f"{name} ({count})" for name, count in top_capability_errors) or "none"
    failure_type_summary = ", ".join(f"{name} ({count})" for name, count in top_failure_types) or "none"

    content = f"""# Next Steps v0

## Weakest observed slices

Current weakest slices by exact match: {weakest_names}.

Top error-heavy capabilities from the exported failure table: {capability_error_summary}.

Most common failure modes: {failure_type_summary}.

## Dataset engineering next steps

- Expand the benchmark with slice-balanced examples for OCR extraction, structured fields, tables, charts, domain terminology, and explicit unanswerable questions.
- Preserve capability and answer-type metadata in every benchmark row so we can keep reporting by capability, answer type, and abstention behavior.
- Add harder negatives where visually adjacent distractors exist, plus formatting variants for dates, currencies, and IDs to stress normalization quality.

## Metrics to add beyond generic VQA

- Keep exact match as the gate metric, but pair it with ANLS for OCR-like strings and relaxed numeric scoring for amounts, counts, and chart values.
- Add answerable-vs-unanswerable calibration reporting so abstention quality is visible alongside generic accuracy.
- Introduce richer document metrics later: field grounding, table cell retrieval, token-F1 for longer spans, and efficiency slices for latency and memory.

## Model and adapter risks

- Weak OCR and layout binding will likely dominate before higher-order reasoning becomes the bottleneck on compact VLMs.
- Numeric and abstention failures can look better than they are unless normalization and slice-aware reporting stay consistent across models.
- Real model APIs differ in chat templates, image preprocessing, and confidence availability, so prediction schema compatibility and normalization should remain centralized.

## Candidate improvement strategies

- Use OCR-assisted prompting or retrieved text spans for field extraction and dense small-font documents.
- Add crop-and-rerank or region-focused prompting for table lookup and layout binding errors.
- Tune abstention prompts and confidence thresholds against the unanswerable slice before optimizing aggregate accuracy.
- Target any future LoRA/QLoRA work at the weakest capability slices rather than the whole benchmark uniformly.
- If numeric and OCR failures remain dominant, consider a hybrid VLM-plus-OCR pipeline before scaling model size.
"""
    write_text(out_path, content)
    return content


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True)
    parser.add_argument("--errors")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    analyze(args.results, args.out, errors_path=args.errors)
    print(f"wrote_analysis={args.out}")


if __name__ == "__main__":
    main()
