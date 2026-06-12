"""Fixture benchmark rows plus TODO markers for real slices."""

from __future__ import annotations

from typing import List


def build_fixture_benchmark() -> List[dict]:
    """Return the committed fixture benchmark rows."""

    invoice_ocr = (
        "Invoice No: INV-001\n"
        "PO Number: PO-77\n"
        "CPT Code: 99213\n"
        "Total Due: $42.00"
    )
    table_ocr = (
        "Item Qty\n"
        "Printer Paper 8\n"
        "Staples 3\n"
        "Pens 12"
    )
    chart_ocr = (
        "Jan 14\n"
        "Feb 19\n"
        "Mar 27"
    )

    return [
        {
            "id": "ocr-1",
            "dataset": "docmini_v0",
            "image_path": "data/fixtures/images/invoice_note.svg",
            "question": "What is the invoice number?",
            "answers": ["INV-001"],
            "capability": "ocr_exact",
            "answer_type": "short_text",
            "metadata": {
                "source_slice": "ocr_exact_v0",
                "doc_type": "invoice",
                "source_adapter": "docvqa",
                "source_dataset": "DocVQA",
                "ocr_text": invoice_ocr,
            },
        },
        {
            "id": "layout-1",
            "dataset": "docmini_v0",
            "image_path": "data/fixtures/images/invoice_note.svg",
            "question": "What is the total due on the invoice?",
            "answers": ["$42.00", "42.00"],
            "capability": "layout_binding",
            "answer_type": "currency",
            "metadata": {
                "source_slice": "layout_binding_v0",
                "doc_type": "invoice",
                "source_adapter": "docvqa",
                "source_dataset": "DocVQA",
                "ocr_text": invoice_ocr,
            },
        },
        {
            "id": "table-1",
            "dataset": "docmini_v0",
            "image_path": "data/fixtures/images/mini_table.svg",
            "question": "How many units of Printer Paper are listed?",
            "answers": ["8"],
            "capability": "table_lookup",
            "answer_type": "integer",
            "metadata": {
                "source_slice": "table_lookup_v0",
                "doc_type": "table",
                "source_adapter": "infovqa",
                "source_dataset": "InfoVQA",
                "ocr_text": table_ocr,
            },
        },
        {
            "id": "chart-1",
            "dataset": "docmini_v0",
            "image_path": "data/fixtures/images/mini_chart.svg",
            "question": "Which month has the highest number of tickets closed?",
            "answers": ["Mar", "March"],
            "capability": "chart_numeric",
            "answer_type": "short_text",
            "metadata": {
                "source_slice": "chart_numeric_v0",
                "doc_type": "chart",
                "source_adapter": "chartqa",
                "source_dataset": "ChartQA",
                "ocr_text": chart_ocr,
            },
        },
        {
            "id": "domain-1",
            "dataset": "docmini_v0",
            "image_path": "data/fixtures/images/invoice_note.svg",
            "question": "What CPT code appears on the document?",
            "answers": ["99213"],
            "capability": "domain_terms",
            "answer_type": "code",
            "metadata": {
                "source_slice": "domain_terms_v0",
                "doc_type": "invoice",
                "source_adapter": "ocrbench",
                "source_dataset": "OCRBench_or_TextVQA_style",
                "ocr_text": invoice_ocr,
            },
        },
        {
            "id": "notfound-1",
            "dataset": "docmini_v0",
            "image_path": "data/fixtures/images/invoice_note.svg",
            "question": "What is the fax number?",
            "answers": ["NOT_FOUND"],
            "capability": "not_found",
            "answer_type": "abstain",
            "metadata": {
                "source_slice": "not_found_v0",
                "doc_type": "invoice",
                "source_adapter": "custom_not_found",
                "source_dataset": "custom_hallucination_stress",
                "ocr_text": invoice_ocr,
            },
        },
        {
            "id": "robust-1",
            "dataset": "docmini_v0",
            "image_path": "data/fixtures/images/invoice_note.svg",
            "question": "What is the PO Number?",
            "answers": ["PO-77"],
            "capability": "robustness_optional",
            "answer_type": "short_text",
            "metadata": {
                "source_slice": "robustness_optional_v0",
                "doc_type": "invoice",
                "source_adapter": "robustness",
                "source_dataset": "custom_or_handwriting",
                "ocr_text": invoice_ocr,
            },
        },
    ]


def filter_fixture_rows(capabilities: set[str]) -> List[dict]:
    return [row for row in build_fixture_benchmark() if row["capability"] in capabilities]


def describe_real_dataset_todos() -> list[str]:
    return [
        "Add VLMEvalKit-compatible readers for DocVQA, InfoVQA, ChartQA, and OCRBench/TextVQA-style slices.",
        "Keep downloads behind explicit CLI flags and cache paths outside the repo.",
        "Preserve capability labels during benchmark materialization for slice-aware reporting.",
    ]
