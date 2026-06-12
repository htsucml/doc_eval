# Improvement Plan v0

## System-side improvements

### OCR-assisted prompting

- Add optional `metadata.ocr_text` per benchmark row so we can run a clean ablation between `image_only` and `image_plus_ocr`.
- Record `prompt_mode` inside each prediction's `inference_config` so offline analysis can compare OCR-heavy slices, abstention slices, and document types directly.
- Expected outcome: lift exact-match and ANLS on OCR-heavy questions with minimal regression on layout-sensitive questions.

### High-resolution crops and tiling

- Add a second inference path that extracts focused crops for dense regions like tables, receipt totals, and small-print headers.
- Keep the benchmark row stable while storing crop/tiling policy in inference metadata for later slice-aware analysis.
- Expected outcome: improve small-text retrieval and table lookup where full-page downsampling loses detail.

### Not-found calibration

- Build extra plausible-but-missing questions against the fixture docs so abstention can be tuned separately from answer extraction.
- Analyze false positives on `NOT_FOUND` prompts with confidence and prompt-mode metadata.
- Expected outcome: lower hallucinated field extraction rate while holding recall on present fields.

## Model-side improvements

### LoRA or QLoRA targeted adaptation

- Start with lightweight LoRA adapters on the smallest viable document-capable model, then evaluate QLoRA if memory is still a bottleneck.
- Fine-tune on benchmark-shaped JSONL so question formatting, abstention behavior, and OCR-augmented prompting stay aligned with evaluation.
- Expected outcome: better domain-term recall, improved calibration on present-vs-missing fields, and less brittle formatting on short answer outputs.

### Distillation from a stronger document model

- Use a stronger teacher model to generate rationalized answers, abstention examples, and OCR-aware prompt completions for the same fixture/task format.
- Distill into the smaller student with a focus on missing-field behavior, layout binding, and table/chart extraction.
- Expected outcome: recover part of the teacher's document understanding without serving a heavier model in the final stack.

## Metrics and success criteria

- Primary metrics: exact match, ANLS, relaxed numeric accuracy, and not-found precision/recall.
- Slice metrics: OCR-heavy fields, layout binding, table lookup, chart reading, and not-found ablations.
- Success target for the PoC: demonstrate measurable gains from `image_plus_ocr` on OCR-centric rows, reduce hallucinated answers on missing-field rows, and leave a CPU-safe training scaffold ready for GPU follow-up in Kaggle or Colab.
