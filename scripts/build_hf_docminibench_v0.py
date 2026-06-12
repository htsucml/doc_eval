"""Build DocMiniBench-v0 from HF sources with a deterministic fallback.

Primary sources:
- lmms-lab/DocVQA
- lmms-lab/ChartQA

The builder is intentionally conservative: rows are schema-validated before writing,
images are materialized under data/docminibench_v0_images, and any HF loading
blocker falls back to local deterministic fixtures so overnight evaluation can run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
import re
import shutil
import signal
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path
from typing import Any, Iterable

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.datasets.jsonl_dataset import load_jsonl, write_jsonl
from src.datasets.schema import validate_benchmark_row, validate_benchmark_rows
from src.utils.hashing import sha256_file
from src.utils.io import write_json, write_text

CAPABILITIES = [
    "ocr_exact",
    "layout_binding",
    "table_lookup",
    "chart_numeric",
    "domain_terms",
    "not_found",
]
DOCVQA_CAPABILITIES = ["ocr_exact", "layout_binding", "table_lookup", "domain_terms"]
NOT_FOUND_QUESTIONS = [
    "What is the fax number?",
    "What is the vendor tax ID?",
    "What is the payment due date?",
    "What is the discount code?",
    "Who approved this document?",
    "What is the shipping method?",
]
NOT_FOUND_ANSWERS = ["not found", "not answerable from the document", "NOT_FOUND"]
DATASET_NAME = "docminibench_v0"


class BuildTimeout(RuntimeError):
    pass


@dataclass
class BuildStats:
    mode: str = "real_hf"
    source_datasets: list[str] = field(default_factory=list)
    split_names: dict[str, list[str]] = field(default_factory=lambda: defaultdict(list))
    sample_counts: Counter = field(default_factory=Counter)
    attempted_source_examples: Counter = field(default_factory=Counter)
    limitations: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def _timeout_handler(signum: int, frame: Any) -> None:  # pragma: no cover - integration guard
    raise BuildTimeout("HF dataset loading exceeded the configured timebox")


def _stable_key(*parts: Any) -> str:
    payload = ":".join(str(part) for part in parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _normalize_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _flatten_strings(value: Any, limit: int = 40) -> list[str]:
    out: list[str] = []
    if value is None or len(out) >= limit:
        return out
    if isinstance(value, str):
        text = _normalize_text(value)
        return [text] if text else []
    if isinstance(value, (int, float, bool)):
        return [str(value)]
    if isinstance(value, (list, tuple)):
        for item in value:
            out.extend(_flatten_strings(item, limit=limit))
            if len(out) >= limit:
                break
        return out[:limit]
    if isinstance(value, dict):
        for item in value.values():
            out.extend(_flatten_strings(item, limit=limit))
            if len(out) >= limit:
                break
    return out[:limit]


def _first_field(row: dict[str, Any], names: Iterable[str]) -> Any:
    lowered = {key.lower(): key for key in row}
    for name in names:
        key = lowered.get(name.lower())
        if key is not None:
            return row[key]
    return None


def _extract_question(row: dict[str, Any]) -> str | None:
    value = _first_field(row, ["question", "query", "prompt", "Question"])
    text = _normalize_text(value)
    return text or None


def _extract_answers(row: dict[str, Any]) -> list[str]:
    value = _first_field(row, ["answers", "answer", "ground_truth", "label", "response", "final_answer"])
    answers = [item for item in _flatten_strings(value) if item]
    deduped = []
    seen = set()
    for answer in answers:
        key = answer.casefold()
        if key not in seen:
            seen.add(key)
            deduped.append(answer)
    return deduped


def _question_context(row: dict[str, Any], question: str, answers: list[str]) -> str:
    useful_keys = [
        "question_types",
        "question_type",
        "answer_type",
        "data_source",
        "ocr_tokens",
        "ocr_text",
        "document_type",
        "doc_type",
    ]
    parts = [question, " ".join(answers)]
    for key in useful_keys:
        value = _first_field(row, [key])
        if value is not None:
            parts.extend(_flatten_strings(value, limit=10))
    return " ".join(parts).casefold()


def _infer_docvqa_capability(row: dict[str, Any], question: str, answers: list[str]) -> str:
    context = _question_context(row, question, answers)
    if re.search(r"\b(table|row|column|cell|header|line item|quantity|qty|units?)\b", context):
        return "table_lookup"
    if re.search(r"\b(cpt|icd|sku|invoice|po\s*number|policy|claim|account|routing|swift|iban|tax id|code|serial|id)\b", context):
        return "domain_terms"
    if re.search(r"\b(total|subtotal|amount|due|date|address|name|field|top|bottom|left|right|near|under|above|beside|section)\b", context):
        return "layout_binding"
    return "ocr_exact"


def _infer_answer_type(answers: list[str], capability: str) -> str:
    if capability == "not_found":
        return "abstain"
    joined = " ".join(answers)
    if capability == "chart_numeric":
        return "number" if re.search(r"[-+]?\d", joined) else "short_text"
    if re.search(r"[$€£¥]|\b(?:usd|eur|gbp|cad|aud)\b", joined, re.IGNORECASE):
        return "currency"
    if re.fullmatch(r"[-+]?\d+", answers[0].replace(",", "")) if answers else False:
        return "integer"
    if re.search(r"[-+]?\d+\.\d+", joined):
        return "float"
    if capability == "domain_terms":
        return "code"
    return "short_text"


def _find_image_value(row: dict[str, Any]) -> Any:
    preferred = ["image", "image_path", "img", "page_image", "chart", "document", "file", "path"]
    value = _first_field(row, preferred)
    if value is not None:
        return value
    for value in row.values():
        if _looks_like_image(value):
            return value
    return None


def _looks_like_image(value: Any) -> bool:
    if hasattr(value, "save") and hasattr(value, "convert"):
        return True
    if isinstance(value, (bytes, bytearray)):
        return True
    if isinstance(value, dict) and ("bytes" in value or "path" in value):
        return True
    if isinstance(value, str) and Path(value).suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}:
        return True
    return False


def _save_image(value: Any, image_dir: Path, stem: str) -> str | None:
    from PIL import Image

    image_dir.mkdir(parents=True, exist_ok=True)
    if isinstance(value, dict):
        if value.get("bytes") is not None:
            value = value["bytes"]
        elif value.get("path") is not None:
            value = value["path"]

    if hasattr(value, "save") and hasattr(value, "convert"):
        path = image_dir / f"{stem}.png"
        value.convert("RGB").save(path)
        return str(path)

    if isinstance(value, (bytes, bytearray)):
        path = image_dir / f"{stem}.png"
        Image.open(BytesIO(value)).convert("RGB").save(path)
        return str(path)

    if isinstance(value, str):
        source = Path(value)
        if source.exists():
            suffix = source.suffix.lower() or ".png"
            path = image_dir / f"{stem}{suffix}"
            shutil.copy2(source, path)
            return str(path)

    return None


def _dataset_call(fn: Any, *args: Any, **kwargs: Any) -> Any:
    return fn(*args, **kwargs)


def _list_configs(datasets_module: Any, dataset_name: str) -> list[str | None]:
    try:
        configs = _dataset_call(datasets_module.get_dataset_config_names, dataset_name)
        return list(configs) or [None]
    except Exception:
        return [None]


def _list_splits(datasets_module: Any, dataset_name: str, config: str | None) -> list[str]:
    try:
        if config is None:
            splits = _dataset_call(datasets_module.get_dataset_split_names, dataset_name)
        else:
            splits = _dataset_call(datasets_module.get_dataset_split_names, dataset_name, config)
        return list(splits) or ["train"]
    except Exception:
        return ["train", "validation", "test"]


def _load_split(datasets_module: Any, dataset_name: str, config: str | None, split: str) -> Any:
    kwargs = {"split": split, "streaming": True}
    if config is None:
        return _dataset_call(datasets_module.load_dataset, dataset_name, **kwargs)
    return _dataset_call(datasets_module.load_dataset, dataset_name, config, **kwargs)


def _make_row(
    *,
    row_id: str,
    dataset: str,
    image_path: str,
    question: str,
    answers: list[str],
    capability: str,
    answer_type: str,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    return validate_benchmark_row(
        {
            "id": row_id,
            "dataset": dataset,
            "image_path": image_path,
            "question": question,
            "answers": answers,
            "capability": capability,
            "answer_type": answer_type,
            "metadata": metadata,
        }
    )


def _target_counts(target_count: int) -> dict[str, int]:
    base = target_count // len(CAPABILITIES)
    counts = {capability: base for capability in CAPABILITIES}
    for capability in CAPABILITIES[: target_count - base * len(CAPABILITIES)]:
        counts[capability] += 1
    return counts


def _capability_counts(rows: list[dict[str, Any]]) -> Counter:
    return Counter(row["capability"] for row in rows)


def _need_more(rows: list[dict[str, Any]], targets: dict[str, int], capability: str) -> bool:
    return _capability_counts(rows)[capability] < targets[capability]


def _build_real_hf(args: argparse.Namespace, stats: BuildStats) -> list[dict[str, Any]]:
    import datasets

    targets = _target_counts(args.target_count)
    rows: list[dict[str, Any]] = []
    docvqa_image_paths: list[tuple[str, dict[str, Any]]] = []
    image_dir = Path(args.image_dir)

    stats.source_datasets.extend(["lmms-lab/DocVQA", "lmms-lab/ChartQA"])

    # DocVQA supplies OCR/layout/table/domain examples and source images for unanswerable rows.
    for config in _list_configs(datasets, "lmms-lab/DocVQA")[: args.max_configs_per_source]:
        splits = _list_splits(datasets, "lmms-lab/DocVQA", config)
        for split in _ordered_splits(splits):
            if _docvqa_done(rows, targets) and _need_more(rows, targets, "not_found") is False:
                break
            stats.split_names["lmms-lab/DocVQA"].append(_format_split(config, split))
            try:
                dataset = _load_split(datasets, "lmms-lab/DocVQA", config, split)
            except Exception as exc:
                stats.errors.append(f"DocVQA load failed config={config} split={split}: {exc}")
                continue
            for index, source_row in enumerate(dataset):
                if index >= args.max_source_examples:
                    break
                stats.attempted_source_examples["lmms-lab/DocVQA"] += 1
                question = _extract_question(source_row)
                answers = _extract_answers(source_row)
                if not question or not answers:
                    continue
                capability = _infer_docvqa_capability(source_row, question, answers)
                if capability not in DOCVQA_CAPABILITIES or not _need_more(rows, targets, capability):
                    continue
                image_path = _save_image(
                    _find_image_value(source_row),
                    image_dir,
                    f"docvqa_{_stable_key(config, split, index)[:16]}",
                )
                if image_path is None:
                    continue
                row_id = f"docvqa-{capability}-{_capability_counts(rows)[capability] + 1:03d}"
                metadata = {
                    "source_dataset": "lmms-lab/DocVQA",
                    "source_config": config or "default",
                    "source_split": split,
                    "source_index": index,
                    "source_row_keys": sorted(str(key) for key in source_row.keys()),
                }
                row = _make_row(
                    row_id=row_id,
                    dataset=DATASET_NAME,
                    image_path=image_path,
                    question=question,
                    answers=answers,
                    capability=capability,
                    answer_type=_infer_answer_type(answers, capability),
                    metadata=metadata,
                )
                rows.append(row)
                docvqa_image_paths.append((image_path, metadata))
                _add_not_found_rows(rows, targets, docvqa_image_paths, stats)
                if _docvqa_done(rows, targets) and not _need_more(rows, targets, "not_found"):
                    break

    # ChartQA supplies chart_numeric examples.
    for config in _list_configs(datasets, "lmms-lab/ChartQA")[: args.max_configs_per_source]:
        splits = _list_splits(datasets, "lmms-lab/ChartQA", config)
        for split in _ordered_splits(splits):
            if not _need_more(rows, targets, "chart_numeric"):
                break
            stats.split_names["lmms-lab/ChartQA"].append(_format_split(config, split))
            try:
                dataset = _load_split(datasets, "lmms-lab/ChartQA", config, split)
            except Exception as exc:
                stats.errors.append(f"ChartQA load failed config={config} split={split}: {exc}")
                continue
            for index, source_row in enumerate(dataset):
                if index >= args.max_source_examples:
                    break
                stats.attempted_source_examples["lmms-lab/ChartQA"] += 1
                if not _need_more(rows, targets, "chart_numeric"):
                    break
                question = _extract_question(source_row)
                answers = _extract_answers(source_row)
                if not question or not answers:
                    continue
                image_path = _save_image(
                    _find_image_value(source_row),
                    image_dir,
                    f"chartqa_{_stable_key(config, split, index)[:16]}",
                )
                if image_path is None:
                    continue
                row_id = f"chartqa-chart_numeric-{_capability_counts(rows)['chart_numeric'] + 1:03d}"
                row = _make_row(
                    row_id=row_id,
                    dataset=DATASET_NAME,
                    image_path=image_path,
                    question=question,
                    answers=answers,
                    capability="chart_numeric",
                    answer_type=_infer_answer_type(answers, "chart_numeric"),
                    metadata={
                        "source_dataset": "lmms-lab/ChartQA",
                        "source_config": config or "default",
                        "source_split": split,
                        "source_index": index,
                        "source_row_keys": sorted(str(key) for key in source_row.keys()),
                    },
                )
                rows.append(row)

    rows = _stable_trim(rows, args.target_count)
    rows = validate_benchmark_rows(rows)
    stats.sample_counts.update(_capability_counts(rows))
    if len(rows) < args.min_count:
        raise RuntimeError(
            f"HF build produced {len(rows)} rows, below minimum {args.min_count}. "
            f"counts={dict(_capability_counts(rows))}; errors={stats.errors[:3]}"
        )
    return rows


def _ordered_splits(splits: list[str]) -> list[str]:
    preferred = ["train", "validation", "val", "test", "dev"]
    return sorted(set(splits), key=lambda split: (preferred.index(split) if split in preferred else len(preferred), split))


def _format_split(config: str | None, split: str) -> str:
    return f"{config or 'default'}:{split}"


def _docvqa_done(rows: list[dict[str, Any]], targets: dict[str, int]) -> bool:
    counts = _capability_counts(rows)
    return all(counts[capability] >= targets[capability] for capability in DOCVQA_CAPABILITIES)


def _add_not_found_rows(
    rows: list[dict[str, Any]],
    targets: dict[str, int],
    docvqa_image_paths: list[tuple[str, dict[str, Any]]],
    stats: BuildStats,
) -> None:
    while _need_more(rows, targets, "not_found") and docvqa_image_paths:
        index = _capability_counts(rows)["not_found"]
        image_path, source_meta = docvqa_image_paths[index % len(docvqa_image_paths)]
        question = NOT_FOUND_QUESTIONS[index % len(NOT_FOUND_QUESTIONS)]
        row_id = f"docvqa-not_found-{index + 1:03d}"
        rows.append(
            _make_row(
                row_id=row_id,
                dataset=DATASET_NAME,
                image_path=image_path,
                question=question,
                answers=NOT_FOUND_ANSWERS,
                capability="not_found",
                answer_type="abstain",
                metadata={
                    **source_meta,
                    "source_dataset": "generated_from_lmms-lab/DocVQA",
                    "source_slice": "not_found_generated",
                    "generation_rule": "plausible_missing_field_question",
                },
            )
        )


def _stable_trim(rows: list[dict[str, Any]], target_count: int) -> list[dict[str, Any]]:
    counts = _target_counts(target_count)
    selected: list[dict[str, Any]] = []
    current = Counter()
    for row in sorted(rows, key=lambda item: (_stable_key(item["capability"], item["id"]), item["id"])):
        capability = row["capability"]
        if current[capability] < counts[capability]:
            selected.append(row)
            current[capability] += 1
    return sorted(selected, key=lambda item: item["id"])


def _build_fallback(args: argparse.Namespace, stats: BuildStats, reason: str) -> list[dict[str, Any]]:
    stats.mode = "fixture_expanded_fallback"
    stats.limitations.append(reason)
    fixture_rows = load_jsonl("data/fixtures/docminibench_sample.jsonl", validator=validate_benchmark_row)
    image_dir = Path(args.image_dir)
    image_dir.mkdir(parents=True, exist_ok=True)

    copied: dict[str, str] = {}
    for fixture in fixture_rows:
        src = Path(fixture["image_path"])
        dst = image_dir / src.name
        if src.exists() and str(src) not in copied:
            shutil.copy2(src, dst)
            copied[str(src)] = str(dst)

    templates = {
        "ocr_exact": [
            ("What is the invoice number?", ["INV-001"], "short_text", "data/fixtures/images/invoice_note.svg"),
            ("Read the invoice identifier.", ["INV-001"], "short_text", "data/fixtures/images/invoice_note.svg"),
            ("What PO Number is shown?", ["PO-77"], "short_text", "data/fixtures/images/invoice_note.svg"),
            ("What is the exact PO number?", ["PO-77"], "short_text", "data/fixtures/images/invoice_note.svg"),
            ("What total due text appears?", ["$42.00", "42.00"], "currency", "data/fixtures/images/invoice_note.svg"),
        ],
        "layout_binding": [
            ("What is the total due on the invoice?", ["$42.00", "42.00"], "currency", "data/fixtures/images/invoice_note.svg"),
            ("Which value is next to Total Due?", ["$42.00", "42.00"], "currency", "data/fixtures/images/invoice_note.svg"),
            ("What value is shown for PO Number?", ["PO-77"], "short_text", "data/fixtures/images/invoice_note.svg"),
            ("What identifier follows Invoice No?", ["INV-001"], "short_text", "data/fixtures/images/invoice_note.svg"),
            ("What amount is listed at the bottom of the invoice note?", ["$42.00", "42.00"], "currency", "data/fixtures/images/invoice_note.svg"),
        ],
        "table_lookup": [
            ("How many units of Printer Paper are listed?", ["8"], "integer", "data/fixtures/images/mini_table.svg"),
            ("What quantity is listed for Staples?", ["3"], "integer", "data/fixtures/images/mini_table.svg"),
            ("How many Pens are listed?", ["12"], "integer", "data/fixtures/images/mini_table.svg"),
            ("Which item has quantity 8?", ["Printer Paper"], "short_text", "data/fixtures/images/mini_table.svg"),
            ("Which item has quantity 3?", ["Staples"], "short_text", "data/fixtures/images/mini_table.svg"),
        ],
        "chart_numeric": [
            ("Which month has the highest number of tickets closed?", ["Mar", "March"], "short_text", "data/fixtures/images/mini_chart.svg"),
            ("How many tickets were closed in March?", ["27"], "integer", "data/fixtures/images/mini_chart.svg"),
            ("How many tickets were closed in February?", ["19"], "integer", "data/fixtures/images/mini_chart.svg"),
            ("How many tickets were closed in January?", ["14"], "integer", "data/fixtures/images/mini_chart.svg"),
            ("What is the difference between March and January tickets?", ["13"], "integer", "data/fixtures/images/mini_chart.svg"),
        ],
        "domain_terms": [
            ("What CPT code appears on the document?", ["99213"], "code", "data/fixtures/images/invoice_note.svg"),
            ("Read the CPT code.", ["99213"], "code", "data/fixtures/images/invoice_note.svg"),
            ("What code follows CPT Code?", ["99213"], "code", "data/fixtures/images/invoice_note.svg"),
            ("What purchase order code appears?", ["PO-77"], "code", "data/fixtures/images/invoice_note.svg"),
            ("What invoice code appears?", ["INV-001"], "code", "data/fixtures/images/invoice_note.svg"),
        ],
        "not_found": [
            (question, NOT_FOUND_ANSWERS, "abstain", "data/fixtures/images/invoice_note.svg")
            for question in NOT_FOUND_QUESTIONS
        ],
    }

    rows: list[dict[str, Any]] = []
    per_capability = max(1, min(args.fallback_count, 80) // len(CAPABILITIES))
    for capability in CAPABILITIES:
        items = templates[capability]
        for index in range(per_capability):
            question, answers, answer_type, image_path = items[index % len(items)]
            copied_path = copied.get(image_path, str(image_dir / Path(image_path).name))
            rows.append(
                _make_row(
                    row_id=f"fallback-{capability}-{index + 1:03d}",
                    dataset=DATASET_NAME,
                    image_path=copied_path,
                    question=f"{question} [{index + 1}]" if index >= len(items) else question,
                    answers=answers,
                    capability=capability,
                    answer_type=answer_type,
                    metadata={
                        "source_dataset": "local_fixture_expansion",
                        "source_slice": f"{capability}_fallback",
                        "fallback_reason": reason,
                        "doc_type": "chart" if capability == "chart_numeric" else "invoice_or_table",
                    },
                )
            )
    rows = validate_benchmark_rows(rows)
    stats.sample_counts.update(_capability_counts(rows))
    return rows


def _write_limitations(path: str, stats: BuildStats) -> None:
    lines = [
        "# Dataset Limitations v0",
        "",
        f"- mode: {stats.mode}",
        f"- source_datasets: {', '.join(stats.source_datasets) or 'local fixtures'}",
        f"- sample_counts: {dict(stats.sample_counts)}",
        "",
        "## Limitations",
        "",
    ]
    limitations = stats.limitations or ["No additional limitations recorded."]
    for item in limitations:
        lines.append(f"- {item}")
    if stats.errors:
        lines.extend(["", "## Source Errors", ""])
        for item in stats.errors[:20]:
            lines.append(f"- {item}")
    write_text(path, "\n".join(lines) + "\n")


def build(args: argparse.Namespace) -> tuple[list[dict[str, Any]], BuildStats]:
    stats = BuildStats()
    started = time.monotonic()
    previous_handler = signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(max(1, int(args.hf_timebox_seconds)))
    try:
        rows = _build_real_hf(args, stats)
    except Exception as exc:
        reason = f"HF build fallback triggered: {type(exc).__name__}: {exc}"
        stats.errors.append(reason)
        rows = _build_fallback(args, stats, reason)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous_handler)
    stats.limitations.append(f"builder_elapsed_seconds={time.monotonic() - started:.1f}")
    return rows, stats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data/docminibench_v0.jsonl")
    parser.add_argument("--target-count", type=int, default=120)
    parser.add_argument("--min-count", type=int, default=80)
    parser.add_argument("--fallback-count", type=int, default=60)
    parser.add_argument("--image-dir", default="data/docminibench_v0_images")
    parser.add_argument("--limitations-out", default="reports/dataset_limitations_v0.md")
    parser.add_argument("--hf-timebox-seconds", type=int, default=2700)
    parser.add_argument("--max-source-examples", type=int, default=3000)
    parser.add_argument("--max-configs-per-source", type=int, default=4)
    args = parser.parse_args()

    if args.target_count < 1:
        raise ValueError("--target-count must be positive")
    if args.min_count < 1:
        raise ValueError("--min-count must be positive")

    rows, stats = build(args)
    rows = validate_benchmark_rows(rows)
    write_jsonl(args.out, rows)
    benchmark_sha = sha256_file(args.out)
    meta_path = str(Path(args.out).with_suffix(".meta.json"))
    write_json(
        meta_path,
        {
            "benchmark_name": DATASET_NAME,
            "benchmark_path": args.out,
            "benchmark_sha256": benchmark_sha,
            "row_count": len(rows),
            "target_count": args.target_count,
            "minimum_acceptable_count": args.min_count,
            "mode": stats.mode,
            "source_datasets": stats.source_datasets or ["local_fixture_expansion"],
            "split_names": {key: sorted(set(value)) for key, value in stats.split_names.items()},
            "sample_counts": dict(stats.sample_counts),
            "attempted_source_examples": dict(stats.attempted_source_examples),
            "image_dir": args.image_dir,
            "limitations": stats.limitations,
            "errors": stats.errors,
        },
    )
    _write_limitations(args.limitations_out, stats)
    print(f"wrote_benchmark={args.out}")
    print(f"wrote_metadata={meta_path}")
    print(f"wrote_limitations={args.limitations_out}")
    print(f"mode={stats.mode}")
    print(f"row_count={len(rows)}")
    print(f"sample_counts={json.dumps(dict(stats.sample_counts), sort_keys=True)}")


if __name__ == "__main__":
    main()
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)
