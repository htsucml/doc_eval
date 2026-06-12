"""Export wrong predictions with lightweight failure hints."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.datasets.jsonl_dataset import load_jsonl
from src.datasets.schema import validate_benchmark_row, validate_prediction_row
from src.metrics.exact_match import exact_match, normalize_text
from src.metrics.relaxed_numeric import parse_number
from src.utils.io import write_text


def failure_hint(row: dict) -> str:
    if row["capability"] == "not_found" and normalize_text(row["parsed_answer"]) != "not_found":
        return "Hallucinated answer when abstention was expected."
    if row["capability"] == "table_lookup":
        return "Likely row/column lookup error."
    if row["capability"] == "chart_numeric":
        return "Likely chart reading or comparison error."
    if parse_number(row["parsed_answer"]) is not None:
        return "Numeric mismatch beyond relaxed tolerance."
    return "String mismatch; inspect OCR/layout grounding."


def export_errors(preds_path: str, benchmark_path: str, out_path: str) -> str:
    predictions = load_jsonl(preds_path, validator=validate_prediction_row)
    benchmark_rows = load_jsonl(benchmark_path, validator=validate_benchmark_row)
    benchmark_by_id = {row["id"]: row for row in benchmark_rows}

    lines = [
        "# Error Report",
        "",
        "| id | capability | question | ground_truth | parsed_answer | raw_output | failure_hint |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for prediction in predictions:
        sample = benchmark_by_id[prediction["sample_id"]]
        if exact_match(prediction["parsed_answer"], sample["answers"]) >= 1.0:
            continue
        row = {**sample, **prediction}
        lines.append(
            "| {id} | {capability} | {question} | {ground_truth} | {parsed_answer} | {raw_output} | {hint} |".format(
                id=sample["id"],
                capability=sample["capability"],
                question=sample["question"].replace("|", "/"),
                ground_truth=", ".join(sample["answers"]).replace("|", "/"),
                parsed_answer=str(prediction["parsed_answer"]).replace("|", "/"),
                raw_output=str(prediction["raw_output"]).replace("|", "/"),
                hint=failure_hint(row).replace("|", "/"),
            )
        )
    markdown = "\n".join(lines) + "\n"
    write_text(out_path, markdown)
    return markdown


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preds", required=True)
    parser.add_argument("--benchmark", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    export_errors(args.preds, args.benchmark, args.out)
    print(f"wrote_errors={args.out}")


if __name__ == "__main__":
    main()
