# NOT_FOUND Generation Spec

## Scope

This report documents the provenance of the 20 `not_found` rows currently present in `data/docminibench_v0.jsonl`. It is based on inspection of `scripts/build_hf_docminibench_v0.py`, `scripts/build_benchmark_v0.py`, `data/docminibench_v0.jsonl`, `data/docminibench_v0.meta.json`, and existing reports that mention `NOT_FOUND`, `not_found`, absent, or unanswerable behavior. No model inference was run for this report.

## Short Answer

The current `NOT_FOUND` rows are synthetic absent-field prompts generated from a fixed template list and attached to a DocVQA image. They are not existing unanswerable QA examples from DocVQA, and they are not produced from source annotations, OCR text, a field inventory, or document-type-specific metadata. The source image content is reused, but the image is saved/re-encoded into `data/docminibench_v0_images/`; no crop or visual edit is performed by the builder.

## Source Dataset And Splits

- Benchmark mode in metadata: `real_hf`.
- Metadata source datasets: `lmms-lab/DocVQA, lmms-lab/ChartQA`.
- Metadata split names: `{"lmms-lab/ChartQA": ["default:test"], "lmms-lab/DocVQA": ["DocVQA:validation"]}`.
- For the `not_found` rows specifically, each row has `metadata.source_dataset = generated_from_lmms-lab/DocVQA`, `metadata.source_config = DocVQA`, `metadata.source_split = validation`, and `metadata.source_index = 0`.
- All 20 current `not_found` rows point at the same saved image path: `data/docminibench_v0_images/docvqa_144428ff617fe939.png`.

## Construction Category

For every current `not_found` row, the category is: **d. generated question from a fixed template**.

The rows are not:

- existing unanswerable QA from source data: no source unanswerable question or source negative label is stored or used;
- modified/re-written answerable QA: the generated question text does not derive from the source question text;
- generated from document metadata/field inventory: no field inventory, OCR text, or document type is consulted by `_add_not_found_rows`.

## Generation Mechanism In Code

In `scripts/build_hf_docminibench_v0.py`, `NOT_FOUND_QUESTIONS` is a six-item fixed list:

```text
What is the fax number?
What is the vendor tax ID?
What is the payment due date?
What is the discount code?
Who approved this document?
What is the shipping method?
```

The answer list is fixed as:

```text
not found
not answerable from the document
NOT_FOUND
```

`_add_not_found_rows()` appends rows while the target `not_found` count is unmet. It chooses:

- image/source metadata by `docvqa_image_paths[index % len(docvqa_image_paths)]`;
- question text by `NOT_FOUND_QUESTIONS[index % len(NOT_FOUND_QUESTIONS)]`;
- row id by `docvqa-not_found-{index + 1:03d}`;
- metadata by copying the source image metadata and overriding `source_dataset`, plus adding `source_slice = not_found_generated` and `generation_rule = plausible_missing_field_question`.

Because `_add_not_found_rows()` is called immediately after the first accepted DocVQA row is appended, it filled all 20 `not_found` targets from the first available DocVQA image in this build. That is why all 20 rows share `source_index = 0` and the same saved image path.

## What Is Modified Or Generated

- **Question text:** generated from the fixed six-question template list, repeated cyclically to reach 20 rows.
- **Target field:** implied by the generated question text only; no explicit `absent_target` field is stored.
- **Gold answer:** generated fixed answer list: `not found`, `not answerable from the document`, `NOT_FOUND`.
- **Metadata:** copied from the source DocVQA image metadata available in the builder (`source_config`, `source_split`, `source_index`, `source_row_keys`) and then marked as generated with `source_dataset = generated_from_lmms-lab/DocVQA`, `source_slice = not_found_generated`, and `generation_rule = plausible_missing_field_question`.
- **Image:** saved from the source DocVQA image. The code converts PIL images to RGB and saves PNG files. It does not crop, mask, redact, or otherwise intentionally modify visual content, but the original image hash/source id is not stored.

## How The Absent Field Is Chosen

Absent fields are chosen by fixed template order, not by inspecting the document. The six targets are fax number, vendor tax ID, payment due date, discount code, approver, and shipping method. The sequence repeats as needed; counts in this benchmark are:

- `What is the discount code?`: 3
- `What is the fax number?`: 4
- `What is the payment due date?`: 3
- `What is the shipping method?`: 3
- `What is the vendor tax ID?`: 4
- `Who approved this document?`: 3

## Evidence Of Absence

There is **not enough stored evidence to prove absence mechanically**.

Evidence currently available:

- The row is labeled by construction as `capability = not_found` and `answer_type = abstain`.
- Metadata records `generation_rule = plausible_missing_field_question`.
- Metadata records source dataset/config/split/index and source row keys.

Evidence not stored:

- no source annotation saying the question is unanswerable;
- no OCR text for the source page;
- no field inventory or list of present fields;
- no document type;
- no original source id values such as `docId`, `questionId`, `ucsf_document_id`, or `ucsf_document_page_no`, despite those keys being present in the source row;
- no original image hash or source image URI/path;
- no explicit generated absent target field.

Therefore absence is a manual/plausibility assumption made by the benchmark generator, not a mechanically verified property of the source document.

## Does JSONL Store Enough Metadata To Reconstruct The Absent-Field Reason?

No. The JSONL stores enough to reconstruct that a fixed-template generated `not_found` row was attached to DocVQA validation source index 0, but it does not store enough to prove why the requested field is absent. It also does not store enough source identifiers to reload the exact source record without relying on dataset ordering and split stability.

Minimum metadata fields to add:

- `source_record_ids`: values copied from DocVQA such as `docId`, `questionId`, `ucsf_document_id`, and `ucsf_document_page_no` where available;
- `original_image_sha256` and/or source image URI/path;
- `generated_absent_target`, for example `fax_number`;
- `absent_question_template_id`;
- `absence_evidence_type`, one of `source_unanswerable_annotation`, `ocr_negative_match`, `field_inventory_negative`, `manual_audit`, or similar;
- `ocr_text` or a pointer/hash for the OCR text used during absence checking;
- `available_fields` extracted from source annotations/OCR/field inventory;
- `absence_check_result`, including matcher version and timestamp if automated;
- `manual_audit_status`, `manual_auditor`, and `manual_audit_notes` if absence is manually confirmed.

## Relation To `scripts/build_benchmark_v0.py` Fixture Path

`scripts/build_benchmark_v0.py` uses configured source adapters and, for `not_found_v0`, delegates to `src/datasets/source_adapters/custom_not_found.py`. That adapter only returns fixture rows in fixture mode; its real mode raises `NotImplementedError`. The current `data/docminibench_v0.jsonl` was built by `scripts/build_hf_docminibench_v0.py`, not by that fixture adapter path.

## Existing Reports

Existing reports describe the slice as `unanswerable`, absent-field, or `NOT_FOUND`, and model error reports show every model answer as a false answer on those rows. Those reports do not add provenance evidence for absence; they evaluate model behavior against the generated gold answer.

## Row Inventory

| row id | source dataset | source id/image path | question | gold answer | generated absent target | source available fields | absence evidence | mechanically verifiable? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| docvqa-not_found-001 | generated_from_lmms-lab/DocVQA | config=DocVQA; split=validation; source_index=0; source_id=not stored; image=data/docminibench_v0_images/docvqa_144428ff617fe939.png | What is the fax number? | not found; not answerable from the document; NOT_FOUND | fax number | not stored | manual assumption only; no source unanswerable annotation, OCR text, field inventory, document type, or source available-field list stored | no - needs manual audit |
| docvqa-not_found-002 | generated_from_lmms-lab/DocVQA | config=DocVQA; split=validation; source_index=0; source_id=not stored; image=data/docminibench_v0_images/docvqa_144428ff617fe939.png | What is the vendor tax ID? | not found; not answerable from the document; NOT_FOUND | vendor tax ID | not stored | manual assumption only; no source unanswerable annotation, OCR text, field inventory, document type, or source available-field list stored | no - needs manual audit |
| docvqa-not_found-003 | generated_from_lmms-lab/DocVQA | config=DocVQA; split=validation; source_index=0; source_id=not stored; image=data/docminibench_v0_images/docvqa_144428ff617fe939.png | What is the payment due date? | not found; not answerable from the document; NOT_FOUND | payment due date | not stored | manual assumption only; no source unanswerable annotation, OCR text, field inventory, document type, or source available-field list stored | no - needs manual audit |
| docvqa-not_found-004 | generated_from_lmms-lab/DocVQA | config=DocVQA; split=validation; source_index=0; source_id=not stored; image=data/docminibench_v0_images/docvqa_144428ff617fe939.png | What is the discount code? | not found; not answerable from the document; NOT_FOUND | discount code | not stored | manual assumption only; no source unanswerable annotation, OCR text, field inventory, document type, or source available-field list stored | no - needs manual audit |
| docvqa-not_found-005 | generated_from_lmms-lab/DocVQA | config=DocVQA; split=validation; source_index=0; source_id=not stored; image=data/docminibench_v0_images/docvqa_144428ff617fe939.png | Who approved this document? | not found; not answerable from the document; NOT_FOUND | approval person / approver | not stored | manual assumption only; no source unanswerable annotation, OCR text, field inventory, document type, or source available-field list stored | no - needs manual audit |
| docvqa-not_found-006 | generated_from_lmms-lab/DocVQA | config=DocVQA; split=validation; source_index=0; source_id=not stored; image=data/docminibench_v0_images/docvqa_144428ff617fe939.png | What is the shipping method? | not found; not answerable from the document; NOT_FOUND | shipping method | not stored | manual assumption only; no source unanswerable annotation, OCR text, field inventory, document type, or source available-field list stored | no - needs manual audit |
| docvqa-not_found-007 | generated_from_lmms-lab/DocVQA | config=DocVQA; split=validation; source_index=0; source_id=not stored; image=data/docminibench_v0_images/docvqa_144428ff617fe939.png | What is the fax number? | not found; not answerable from the document; NOT_FOUND | fax number | not stored | manual assumption only; no source unanswerable annotation, OCR text, field inventory, document type, or source available-field list stored | no - needs manual audit |
| docvqa-not_found-008 | generated_from_lmms-lab/DocVQA | config=DocVQA; split=validation; source_index=0; source_id=not stored; image=data/docminibench_v0_images/docvqa_144428ff617fe939.png | What is the vendor tax ID? | not found; not answerable from the document; NOT_FOUND | vendor tax ID | not stored | manual assumption only; no source unanswerable annotation, OCR text, field inventory, document type, or source available-field list stored | no - needs manual audit |
| docvqa-not_found-009 | generated_from_lmms-lab/DocVQA | config=DocVQA; split=validation; source_index=0; source_id=not stored; image=data/docminibench_v0_images/docvqa_144428ff617fe939.png | What is the payment due date? | not found; not answerable from the document; NOT_FOUND | payment due date | not stored | manual assumption only; no source unanswerable annotation, OCR text, field inventory, document type, or source available-field list stored | no - needs manual audit |
| docvqa-not_found-010 | generated_from_lmms-lab/DocVQA | config=DocVQA; split=validation; source_index=0; source_id=not stored; image=data/docminibench_v0_images/docvqa_144428ff617fe939.png | What is the discount code? | not found; not answerable from the document; NOT_FOUND | discount code | not stored | manual assumption only; no source unanswerable annotation, OCR text, field inventory, document type, or source available-field list stored | no - needs manual audit |
| docvqa-not_found-011 | generated_from_lmms-lab/DocVQA | config=DocVQA; split=validation; source_index=0; source_id=not stored; image=data/docminibench_v0_images/docvqa_144428ff617fe939.png | Who approved this document? | not found; not answerable from the document; NOT_FOUND | approval person / approver | not stored | manual assumption only; no source unanswerable annotation, OCR text, field inventory, document type, or source available-field list stored | no - needs manual audit |
| docvqa-not_found-012 | generated_from_lmms-lab/DocVQA | config=DocVQA; split=validation; source_index=0; source_id=not stored; image=data/docminibench_v0_images/docvqa_144428ff617fe939.png | What is the shipping method? | not found; not answerable from the document; NOT_FOUND | shipping method | not stored | manual assumption only; no source unanswerable annotation, OCR text, field inventory, document type, or source available-field list stored | no - needs manual audit |
| docvqa-not_found-013 | generated_from_lmms-lab/DocVQA | config=DocVQA; split=validation; source_index=0; source_id=not stored; image=data/docminibench_v0_images/docvqa_144428ff617fe939.png | What is the fax number? | not found; not answerable from the document; NOT_FOUND | fax number | not stored | manual assumption only; no source unanswerable annotation, OCR text, field inventory, document type, or source available-field list stored | no - needs manual audit |
| docvqa-not_found-014 | generated_from_lmms-lab/DocVQA | config=DocVQA; split=validation; source_index=0; source_id=not stored; image=data/docminibench_v0_images/docvqa_144428ff617fe939.png | What is the vendor tax ID? | not found; not answerable from the document; NOT_FOUND | vendor tax ID | not stored | manual assumption only; no source unanswerable annotation, OCR text, field inventory, document type, or source available-field list stored | no - needs manual audit |
| docvqa-not_found-015 | generated_from_lmms-lab/DocVQA | config=DocVQA; split=validation; source_index=0; source_id=not stored; image=data/docminibench_v0_images/docvqa_144428ff617fe939.png | What is the payment due date? | not found; not answerable from the document; NOT_FOUND | payment due date | not stored | manual assumption only; no source unanswerable annotation, OCR text, field inventory, document type, or source available-field list stored | no - needs manual audit |
| docvqa-not_found-016 | generated_from_lmms-lab/DocVQA | config=DocVQA; split=validation; source_index=0; source_id=not stored; image=data/docminibench_v0_images/docvqa_144428ff617fe939.png | What is the discount code? | not found; not answerable from the document; NOT_FOUND | discount code | not stored | manual assumption only; no source unanswerable annotation, OCR text, field inventory, document type, or source available-field list stored | no - needs manual audit |
| docvqa-not_found-017 | generated_from_lmms-lab/DocVQA | config=DocVQA; split=validation; source_index=0; source_id=not stored; image=data/docminibench_v0_images/docvqa_144428ff617fe939.png | Who approved this document? | not found; not answerable from the document; NOT_FOUND | approval person / approver | not stored | manual assumption only; no source unanswerable annotation, OCR text, field inventory, document type, or source available-field list stored | no - needs manual audit |
| docvqa-not_found-018 | generated_from_lmms-lab/DocVQA | config=DocVQA; split=validation; source_index=0; source_id=not stored; image=data/docminibench_v0_images/docvqa_144428ff617fe939.png | What is the shipping method? | not found; not answerable from the document; NOT_FOUND | shipping method | not stored | manual assumption only; no source unanswerable annotation, OCR text, field inventory, document type, or source available-field list stored | no - needs manual audit |
| docvqa-not_found-019 | generated_from_lmms-lab/DocVQA | config=DocVQA; split=validation; source_index=0; source_id=not stored; image=data/docminibench_v0_images/docvqa_144428ff617fe939.png | What is the fax number? | not found; not answerable from the document; NOT_FOUND | fax number | not stored | manual assumption only; no source unanswerable annotation, OCR text, field inventory, document type, or source available-field list stored | no - needs manual audit |
| docvqa-not_found-020 | generated_from_lmms-lab/DocVQA | config=DocVQA; split=validation; source_index=0; source_id=not stored; image=data/docminibench_v0_images/docvqa_144428ff617fe939.png | What is the vendor tax ID? | not found; not answerable from the document; NOT_FOUND | vendor tax ID | not stored | manual assumption only; no source unanswerable annotation, OCR text, field inventory, document type, or source available-field list stored | no - needs manual audit |
