# NOT_FOUND Controlled v0 Specification

This benchmark is controlled synthetic data. Every controlled document image is rendered from a known field inventory, then queried for one field intentionally excluded from the inventory and rendered text.

## Controlled Slice

- Rows: 50
- Document types: bank_notice, invoice, medical_form, receipt, shipping_notice
- Ground truth answer: `NOT_FOUND` for every row
- Absence evidence: `controlled_render_negative`
- Validation rule: `absent_field` is not in `present_fields`, and neither `absent_field` nor `absent_value` appears in `rendered_text`.

## OOD Sanity Slice

- Rows: 20
- Source: simple PIL-rendered non-document images
- Intended use: OOD abstention sanity only, not document understanding.

## Caveat

These examples prove absence only inside the synthetic render specification. They should be reported separately from source-dataset document QA.
