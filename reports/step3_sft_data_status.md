# Step 3 SFT Data Status

- Timestamp UTC: `2026-06-13T16:20:12.314362+00:00`
- Status: `passed`
- Train path: `data/sft_docvqa_template_train_v0.jsonl`
- Validation path: `data/sft_docvqa_template_val_v0.jsonl`
- Train rows: `500`
- Validation rows: `80`
- Train controlled synthetic answerable positives: `250`
- Train controlled synthetic NOT_FOUND negatives: `250`
- Train native template-swapped noisy negatives: `0`
- Validation controlled synthetic answerable positives: `40`
- Validation controlled synthetic NOT_FOUND negatives: `40`
- Missing images: `0`
- Train/val row ID overlap: `0`
- Train/val image overlap: `0`
- Eval row ID overlap: `0`
- Eval image path overlap: `0`
- Metadata/target validation errors: `0`
- Seed: `20260615`

## Eval Datasets Checked
- `data/docminibench_v0.jsonl`: strict benchmark schema
- `data/notfound_controlled_v0.jsonl`: strict benchmark schema
- `data/docvqa_manual_notfound_combined_expanded_v0.jsonl`: alternate schema parsed for leakage checks: ValueError
- `data/notfound_ood_sanity_v0.jsonl`: strict benchmark schema

## Decision
The SFT dataset is train-only controlled synthetic data and passes the requested separation checks.
Native template-swapped real-document negatives remain omitted because no non-evaluation real document images were locally available without download or eval leakage.
