"""Augment fixture benchmarks with plausible missing-field questions."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.datasets.jsonl_dataset import load_jsonl, write_jsonl
from src.datasets.schema import validate_benchmark_row


DEFAULT_QUESTIONS = {
    "invoice": [
        "What is the fax number?",
        "What is the vendor tax ID?",
        "What is the payment due date?",
    ],
    "table": [
        "What is the shipping method?",
        "What is the discount code?",
    ],
    "chart": [
        "What is the quarterly target line value?",
        "Who prepared the dashboard?",
    ],
}


def build_not_found_rows(rows: list[dict]) -> list[dict]:
    existing_questions = {(row["image_path"], row["question"]) for row in rows}
    augmented = list(rows)
    counters: dict[str, int] = {}

    for row in rows:
        metadata = row.get("metadata", {})
        doc_type = metadata.get("doc_type")
        questions = DEFAULT_QUESTIONS.get(doc_type, [])
        for question in questions:
            dedupe_key = (row["image_path"], question)
            if dedupe_key in existing_questions:
                continue
            counters[doc_type] = counters.get(doc_type, 0) + 1
            new_row = {
                "id": f"notfound-{doc_type}-{counters[doc_type]}",
                "dataset": row["dataset"],
                "image_path": row["image_path"],
                "question": question,
                "answers": ["NOT_FOUND"],
                "capability": "not_found",
                "answer_type": "abstain",
                "metadata": {
                    **metadata,
                    "source_slice": "not_found_ablation",
                    "derived_from": row["id"],
                },
            }
            validated = validate_benchmark_row(new_row)
            augmented.append(validated)
            existing_questions.add(dedupe_key)

    return augmented


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="input_path", default="data/fixtures/docminibench_sample.jsonl")
    parser.add_argument(
        "--out",
        dest="output_path",
        default="data/fixtures/docminibench_not_found_ablation.jsonl",
    )
    args = parser.parse_args()

    rows = load_jsonl(args.input_path, validator=validate_benchmark_row)
    augmented = build_not_found_rows(rows)
    write_jsonl(args.output_path, augmented)
    print(f"wrote_rows={len(augmented)}")
    print(f"wrote_benchmark={args.output_path}")


if __name__ == "__main__":
    main()
