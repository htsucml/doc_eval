"""Aggregate predictions into CSV and Markdown reports."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.datasets.jsonl_dataset import load_jsonl
from src.datasets.schema import validate_benchmark_row, validate_prediction_row
from src.metrics.aggregation import score_joined_rows, summarize_scores
from src.utils.io import write_csv, write_text


def join_rows(predictions: list[dict], benchmark_rows: list[dict]) -> list[dict]:
    benchmark_by_id = {row["id"]: row for row in benchmark_rows}
    joined = []
    for prediction in predictions:
        sample = benchmark_by_id[prediction["sample_id"]]
        joined.append({**sample, **prediction})
    return joined


def markdown_table(summary_rows: list[dict], calibration_rows: list[dict]) -> str:
    lines = [
        "# Evaluation Summary",
        "",
        "| slice | count | exact_match | anls | relaxed_numeric | not_found_false_answer_rate | avg_latency_s |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary_rows:
        lines.append(
            "| {slice} | {count} | {exact_match:.4f} | {anls:.4f} | {relaxed_numeric:.4f} | {not_found_false_answer_rate:.4f} | {avg_latency_s:.4f} |".format(
                **row
            )
        )
    lines.extend(["", "## Calibration Buckets", ""])
    if not calibration_rows:
        lines.append("No confidence values available.")
    else:
        lines.extend(
            [
                "| bucket | count | avg_confidence | avg_accuracy | gap |",
                "| --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in calibration_rows:
            lines.append(
                "| {bucket} | {count} | {avg_confidence:.4f} | {avg_accuracy:.4f} | {gap:.4f} |".format(
                    **row
                )
            )
    return "\n".join(lines) + "\n"


def aggregate(preds_path: str, benchmark_path: str, csv_out: str, markdown_out: str) -> tuple[list[dict], list[dict]]:
    predictions = load_jsonl(preds_path, validator=validate_prediction_row)
    benchmark_rows = load_jsonl(benchmark_path, validator=validate_benchmark_row)
    summary_rows, calibration_rows = summarize_scores(score_joined_rows(join_rows(predictions, benchmark_rows)))
    write_csv(
        csv_out,
        summary_rows,
        [
            "slice",
            "count",
            "exact_match",
            "anls",
            "relaxed_numeric",
            "not_found_false_answer_rate",
            "avg_latency_s",
        ],
    )
    write_text(markdown_out, markdown_table(summary_rows, calibration_rows))
    return summary_rows, calibration_rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preds", required=True)
    parser.add_argument("--benchmark", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--markdown", required=True)
    args = parser.parse_args()

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown).parent.mkdir(parents=True, exist_ok=True)
    aggregate(args.preds, args.benchmark, args.out, args.markdown)
    print(f"wrote_csv={args.out}")
    print(f"wrote_markdown={args.markdown}")


if __name__ == "__main__":
    main()
