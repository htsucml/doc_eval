# Codex Add-on Handoff

- Start UTC: `2026-06-13T16:00:00Z`
- End UTC: `2026-06-13T16:49:04.954049+00:00`
- Command log: `logs/codex_addon_stepwise_commands.log`

## Step Status

- `step0_preflight`: passed: pytest 31 passed, diff check clean, status recorded
- `step1_cache`: passed: /root/.cache/huggingface resolves to /workspace/hf_home; root filesystem freed
- `step2_smolvlm2_2_2b`: passed: controlled NOT_FOUND and DocMiniBench strict ran successfully
- `step3_sft_data`: passed: regenerated 500 train / 80 val controlled synthetic rows, no eval row/image overlap
- `step4_sft_training`: passed: real SmolVLM2 500M LoRA training completed 50 steps and reload verified
- `step5_lora_eval`: passed: adapted evals completed for controlled, DocMiniBench, manual real-doc, and OOD; first controlled attempt preserved as failed error-only output
- `step6_reports`: passed: consolidated reports updated
- `step7_validation`: passed: pytest 31 passed; git diff --check clean

## Key Scores

| Cell | Rows | Exact match | Answer in output | NOT_FOUND false-answer | Avg latency | Error rate |
|---|---:|---:|---:|---:|---:|---:|
| smolvlm2_2_2b_controlled_notfound | 50 | 0.76 | 0.76 | 0.24 | 0.3602 | 0.0 |
| smolvlm2_2_2b_docminibench | 120 | 0.525 | 0.5417 | 0.4 | 0.3719 | 0.0 |
| lora_controlled_notfound_fixed | 50 | 0.7 | 0.7 | 0.3 | 0.4599 | 0.0 |
| lora_docminibench | 120 | 0.5083 | 0.525 | 0.7 | 0.5418 | 0.0 |
| lora_manual_real_doc_notfound | 85 | 0.1059 | 0.1059 | 0.8941 | 0.7463 | 0.0 |
| lora_ood_sanity_notfound | 20 | 0.25 | 0.25 | 0.75 | 0.8813 | 0.0 |
| base_smolvlm2_controlled_notfound | 50 | 0.02 | 0.02 | 0.98 | 0.7372 | 0.0 |

## SFT

- Target model: `smolvlm2_500m_video`
- Steps completed: `50`
- Checkpoint path: `outputs/lora_sft_poc_real/smolvlm2_500m_video_20260613T162714Z`
- Reload verified: `True`
- Train data: 500 rows, 250 positives, 250 controlled NOT_FOUND negatives; 0 native template-swapped negatives.

## Outputs Created

- `outputs/smolvlm2_2_2b_notfound_controlled_v0_preds.jsonl`
- `outputs/smolvlm2_2_2b_docminibench_v0_strict_preds.jsonl`
- `outputs/lora_sft_poc_real/smolvlm2_500m_video_20260613T162714Z/`
- `outputs/lora_sft_poc_real_smoke/smolvlm2_500m_video_20260613T162517Z/`
- `outputs/smolvlm2_500m_video_lora_real_notfound_controlled_v0_preds.jsonl (failed error-only preserved)`
- `outputs/smolvlm2_500m_video_lora_real_notfound_controlled_v0_fixed_preds.jsonl`
- `outputs/smolvlm2_500m_video_lora_real_docminibench_v0_preds.jsonl`
- `outputs/smolvlm2_500m_video_lora_real_docvqa_manual_notfound_combined_expanded_v0_preds.jsonl`
- `outputs/smolvlm2_500m_video_lora_real_notfound_ood_sanity_v0_preds.jsonl`

## Reports Created/Updated

- `reports/step0_preflight_status.md`
- `reports/step1_cache_status.md`
- `reports/step2_smolvlm2_2b_status.md`
- `reports/step3_sft_data_status.md`
- `reports/step4_sft_training_status.md`
- `reports/step5_lora_eval_status.md`
- `reports/final_results_tables.md`
- `reports/experiment_matrix_status.md`
- `reports/notfound_comparison_v0.md`
- `reports/smolvlm2_2b_status.md`
- `reports/lora_sft_poc_results.md`
- `reports/lora_poc_status.md`
- `reports/sft_train_data_spec.md`
- `reports/sft_rescue_handoff.md`
- `reports/sft_rescue_handoff.json`
- `reports/tomorrow_action_items.md`
- `reports/codex_addon_handoff.md`
- `reports/codex_addon_handoff.json`

## Files Changed

- `configs/models.yaml`
- `scripts/build_sft_synthetic_v0.py`
- `scripts/eval_model.py`
- `scripts/finetune_lora.py`
- `src/adapters/smolvlm.py`
- `data/sft_docvqa_template_train_v0.jsonl`
- `data/sft_docvqa_template_val_v0.jsonl`
- `data/sft_docvqa_template_train_v0.meta.json`
- `data/docvqa_manual_notfound_combined_expanded_v0_eval.jsonl`

## Blockers/Caveats

- Manual real-doc uploaded file uses alternate answer/answer_mode schema; created additive normalized eval copy for evaluation.
- First adapted controlled eval was error-only because peft_adapter_path leaked into generation kwargs; preserved original failed output and reran to _fixed_preds.jsonl after patch.
- Native real-doc train negatives were omitted: no non-evaluation real document images were locally available without download/eval leakage.
- LoRA transfer remains weak on manual real-doc and OOD NOT_FOUND despite controlled synthetic improvement.

## Validation

- `.venv/bin/python -m pytest -q`: 31 passed
- `git diff --check`: clean

## Next Actions

- Use reports/final_results_tables.md and reports/notfound_comparison_v0.md for report writing.
- Do not score the failed non-fixed LoRA controlled predictions.
- For further SFT, add real non-eval document train data and run longer controlled sweeps.
