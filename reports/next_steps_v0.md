# Next Steps v0

## Weakest observed slices

Current weakest slices by exact match: answer_type:abstain, answer_type:integer, capability:not_found, capability:table_lookup.

Top error-heavy capabilities from the exported failure table: not_found (1), table_lookup (1).

Most common failure modes: false_answer_on_unanswerable (1), numeric_mismatch (1).

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
