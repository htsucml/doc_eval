"""Export wrong predictions with structured failure hints."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.datasets.jsonl_dataset import load_jsonl
from src.datasets.schema import validate_benchmark_row, validate_prediction_row
from src.metrics.aggregation import failure_hint, score_joined_rows
from src.utils.io import write_text


def export_errors(preds_path: str, benchmark_path: str, out_path: str) -> str:
    predictions = load_jsonl(preds_path, validator=validate_prediction_row)
    benchmark_rows = load_jsonl(benchmark_path, validator=validate_benchmark_row)
    benchmark_by_id = {row["id"]: row for row in benchmark_rows}
    joined = [{**benchmark_by_id[prediction["sample_id"]], **prediction} for prediction in predictions]
    scored_rows = score_joined_rows(joined)
    error_rows = [row for row in scored_rows if row["exact_match"] < 1.0]
    error_rows.sort(key=lambda row: (row["capability"], row["failure_type"] or "", row["id"]))

    lines = [
        "# Error Report",
        "",
        "| capability | id | answer_type | question | ground_truth | parsed_answer | strict_exact_match | answer_in_output | failure_type | failure_hint | confidence | error |",
        "| --- | --- | --- | --- | --- | --- | ---: | ---: | --- | --- | ---: | --- |",
    ]
    for row in error_rows:
        lines.append(
            "| {capability} | {id} | {answer_type} | {question} | {ground_truth} | {parsed_answer} | {exact_match:.1f} | {answer_in_output:.1f} | {failure_type} | {hint} | {confidence} | {error} |".format(
                capability=row["capability"],
                id=row["id"],
                answer_type=row["answer_type"],
                question=row["question"].replace("|", "/"),
                ground_truth=", ".join(row["answers"]).replace("|", "/"),
                parsed_answer=str(row["parsed_answer"]).replace("|", "/"),
                exact_match=row["exact_match"],
                answer_in_output=row["answer_in_output"],
                failure_type=(row["failure_type"] or "").replace("|", "/"),
                hint=failure_hint(row).replace("|", "/"),
                confidence="" if row.get("confidence") is None else f"{float(row['confidence']):.2f}",
                error=str(row.get("error") or "").replace("|", "/"),
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
