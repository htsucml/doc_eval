"""Build cross-run error analysis reports from existing predictions."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.aggregate_results import join_rows
from src.datasets.jsonl_dataset import load_jsonl
from src.datasets.schema import validate_benchmark_row, validate_prediction_row
from src.metrics.aggregation import failure_hint, score_joined_rows
from src.utils.io import write_text


DEFAULT_RUNS = [
    {
        "model_label": "SmolVLM 500M Instruct",
        "slice_label": "old_docminibench_v0",
        "benchmark": "data/docminibench_v0.jsonl",
        "preds": "outputs/smolvlm_500m_docminibench_v0_preds.jsonl",
    },
    {
        "model_label": "SmolVLM2 500M Video Instruct",
        "slice_label": "old_docminibench_v0",
        "benchmark": "data/docminibench_v0.jsonl",
        "preds": "outputs/smolvlm2_500m_video_docminibench_v0_preds.jsonl",
    },
    {
        "model_label": "SmolVLM 500M Instruct",
        "slice_label": "controlled_notfound_v0",
        "benchmark": "data/notfound_controlled_v0.jsonl",
        "preds": "outputs/smolvlm_500m_notfound_controlled_v0_preds.jsonl",
    },
    {
        "model_label": "SmolVLM2 500M Video Instruct",
        "slice_label": "controlled_notfound_v0",
        "benchmark": "data/notfound_controlled_v0.jsonl",
        "preds": "outputs/smolvlm2_500m_video_notfound_controlled_v0_preds.jsonl",
    },
    {
        "model_label": "Qwen2.5-VL 3B Instruct",
        "slice_label": "controlled_notfound_v0",
        "benchmark": "data/notfound_controlled_v0.jsonl",
        "preds": "outputs/qwen2_5_vl_3b_instruct_notfound_controlled_v0_preds.jsonl",
        "optional": True,
    },
    {
        "model_label": "Qwen2.5-VL 3B Instruct",
        "slice_label": "old_docminibench_v0",
        "benchmark": "data/docminibench_v0.jsonl",
        "preds": "outputs/qwen2_5_vl_3b_instruct_docminibench_v0_preds.jsonl",
        "optional": True,
    },
]

CSV_FIELDS = [
    "model",
    "slice",
    "capability",
    "sample_id",
    "question",
    "ground_truth",
    "parsed_answer",
    "strict_exact_match",
    "answer_in_output",
    "latency_s",
    "failure_type",
    "failure_hint",
    "formatting_only_failure",
    "representative_both_failed",
]


def _load_run(run: dict) -> list[dict]:
    preds_path = Path(run["preds"])
    if not preds_path.exists():
        if run.get("optional"):
            return []
        raise FileNotFoundError(preds_path)
    predictions = load_jsonl(preds_path, validator=validate_prediction_row)
    benchmark = load_jsonl(run["benchmark"], validator=validate_benchmark_row)
    scored = score_joined_rows(join_rows(predictions, benchmark))
    for row in scored:
        row["model_label"] = run["model_label"]
        row["slice_label"] = run["slice_label"]
    return scored


def _mean(values: list[float]) -> float:
    return round(sum(values) / len(values), 4) if values else 0.0


def _summary(rows: list[dict]) -> list[dict]:
    buckets: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for row in rows:
        buckets[(row["model_label"], row["slice_label"], row["capability"])].append(row)
    output = []
    for (model, slice_label, capability), bucket in sorted(buckets.items()):
        output.append(
            {
                "model": model,
                "slice": slice_label,
                "capability": capability,
                "count": len(bucket),
                "strict_exact_match": _mean([float(row["exact_match"]) for row in bucket]),
                "answer_in_output": _mean([float(row["answer_in_output"]) for row in bucket]),
                "avg_latency_s": _mean([float(row["latency_s"]) for row in bucket]),
                "formatting_only_failures": sum(
                    1 for row in bucket if row["exact_match"] < 1.0 and row["answer_in_output"] >= 1.0
                ),
                "both_failed": sum(1 for row in bucket if row["exact_match"] < 1.0 and row["answer_in_output"] < 1.0),
            }
        )
    return output


def _csv_rows(rows: list[dict]) -> list[dict]:
    representatives: set[tuple[str, str, str]] = set()
    output = []
    for row in rows:
        formatting_only = row["exact_match"] < 1.0 and row["answer_in_output"] >= 1.0
        both_failed = row["exact_match"] < 1.0 and row["answer_in_output"] < 1.0
        rep_key = (row["model_label"], row["slice_label"], row["capability"])
        representative = False
        if both_failed and rep_key not in representatives:
            representatives.add(rep_key)
            representative = True
        output.append(
            {
                "model": row["model_label"],
                "slice": row["slice_label"],
                "capability": row["capability"],
                "sample_id": row["id"],
                "question": row["question"],
                "ground_truth": "; ".join(row["answers"]),
                "parsed_answer": row["parsed_answer"],
                "strict_exact_match": row["exact_match"],
                "answer_in_output": row["answer_in_output"],
                "latency_s": row["latency_s"],
                "failure_type": row["failure_type"] or "",
                "failure_hint": failure_hint(row),
                "formatting_only_failure": formatting_only,
                "representative_both_failed": representative,
            }
        )
    return output


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _markdown(rows: list[dict], summary_rows: list[dict]) -> str:
    lines = [
        "# Error Analysis v0",
        "",
        "This report uses existing v0 prediction outputs and the additive controlled NOT_FOUND outputs. No existing v0 model outputs or datasets were regenerated.",
        "",
        "## Provenance Caveat",
        "",
        "The old `docminibench_v0` NOT_FOUND slice should be treated as exploratory. The provenance audit found fixed-template questions, one DocVQA validation image, no source-provided unanswerable QA, and no OCR/field-inventory/annotation proof of absence.",
        "",
        "The controlled NOT_FOUND slice is stronger for abstention testing because each image is rendered from a known field inventory and the queried field/value is excluded from `present_fields` and `rendered_text`.",
        "",
        "## Per-Model Capability Summary",
        "",
        "| model | slice | capability | count | strict_exact_match | answer_in_output | avg_latency_s | formatting_only_failures | both_failed |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary_rows:
        lines.append(
            "| {model} | {slice} | {capability} | {count} | {strict_exact_match:.4f} | {answer_in_output:.4f} | {avg_latency_s:.4f} | {formatting_only_failures} | {both_failed} |".format(
                **row
            )
        )

    lines.extend(["", "## Old vs Controlled NOT_FOUND", ""])
    not_found_rows = [row for row in summary_rows if row["capability"] == "not_found"]
    lines.extend(
        [
            "| model | slice | rows | strict_exact_match | answer_in_output | both_failed |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in not_found_rows:
        lines.append(
            "| {model} | {slice} | {count} | {strict_exact_match:.4f} | {answer_in_output:.4f} | {both_failed} |".format(
                **row
            )
        )

    formatting = [row for row in rows if row["exact_match"] < 1.0 and row["answer_in_output"] >= 1.0]
    both_failed = [row for row in rows if row["exact_match"] < 1.0 and row["answer_in_output"] < 1.0]
    lines.extend(["", "## Formatting-Only Failures", ""])
    if not formatting:
        lines.append("No formatting-only failures found.")
    else:
        lines.extend(
            [
                "| model | slice | capability | id | gold | parsed_answer |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in formatting[:12]:
            lines.append(
                "| {model_label} | {slice_label} | {capability} | {id} | {gold} | {pred} |".format(
                    model_label=row["model_label"],
                    slice_label=row["slice_label"],
                    capability=row["capability"],
                    id=row["id"],
                    gold="; ".join(row["answers"]).replace("|", "/"),
                    pred=str(row["parsed_answer"]).replace("|", "/"),
                )
            )

    lines.extend(["", "## Representative Both-Failed Cases", ""])
    lines.extend(
        [
            "| model | slice | capability | id | gold | parsed_answer | failure_type |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    seen: set[tuple[str, str, str]] = set()
    for row in both_failed:
        key = (row["model_label"], row["slice_label"], row["capability"])
        if key in seen:
            continue
        seen.add(key)
        lines.append(
            "| {model_label} | {slice_label} | {capability} | {id} | {gold} | {pred} | {failure_type} |".format(
                model_label=row["model_label"],
                slice_label=row["slice_label"],
                capability=row["capability"],
                id=row["id"],
                gold="; ".join(row["answers"]).replace("|", "/"),
                pred=str(row["parsed_answer"]).replace("|", "/"),
                failure_type=row["failure_type"] or "",
            )
        )
    return "\n".join(lines) + "\n"


def build_error_analysis(csv_out: str, markdown_out: str) -> tuple[Path, Path]:
    rows = []
    for run in DEFAULT_RUNS:
        rows.extend(_load_run(run))
    summary_rows = _summary(rows)
    _write_csv(Path(csv_out), _csv_rows(rows))
    write_text(markdown_out, _markdown(rows, summary_rows))
    return Path(csv_out), Path(markdown_out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv-out", default="reports/error_analysis_v0.csv")
    parser.add_argument("--markdown-out", default="reports/error_analysis_v0.md")
    args = parser.parse_args()
    csv_out, markdown_out = build_error_analysis(args.csv_out, args.markdown_out)
    print(f"wrote_csv={csv_out}")
    print(f"wrote_markdown={markdown_out}")


if __name__ == "__main__":
    main()
