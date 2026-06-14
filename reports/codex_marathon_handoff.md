# Codex Marathon Handoff

- Start UTC: `2026-06-13T15:10:10Z`
- End UTC: `2026-06-13T15:33:11.853494+00:00`

## Git Status
```
?? data/docvqa_manual_notfound_combined_expanded_v0.jsonl
?? data/docvqa_manual_notfound_combined_expanded_v0_eval.jsonl
?? data/notfound_controlled_v0.jsonl
?? data/notfound_controlled_v0.meta.json
?? data/notfound_controlled_v0_images/
?? data/notfound_controlled_v0_smoke5.jsonl
?? data/notfound_ood_sanity_v0.jsonl
?? data/notfound_ood_sanity_v0.meta.json
?? data/notfound_ood_sanity_v0_eval.jsonl
?? data/notfound_ood_sanity_v0_eval_strict.jsonl
?? data/notfound_ood_sanity_v0_images/
?? data/sft_docvqa_template_train_v0.jsonl
?? data/sft_docvqa_template_train_v0.meta.json
?? data/sft_docvqa_template_train_v0_images/
?? data/sft_docvqa_template_val_v0.jsonl
?? doc_eval_git_20260613T073259Z.bundle
?? doc_eval_git_20260613T141341Z.bundle
?? tmp_audit_pack/
```

## Data Artifacts Created/Updated
- `data/docvqa_manual_notfound_combined_expanded_v0_eval.jsonl`
- `data/notfound_ood_sanity_v0_eval_strict.jsonl`
- `data/sft_docvqa_template_train_v0.jsonl`
- `data/sft_docvqa_template_val_v0.jsonl`
- `data/sft_docvqa_template_train_v0.meta.json`
- `data/sft_docvqa_template_train_v0_images/`

## Outputs Created/Used
- `outputs/smolvlm_500m_docminibench_v0_strict_preds.jsonl`
- `outputs/smolvlm2_500m_video_docminibench_v0_strict_preds.jsonl`
- `outputs/qwen2_5_vl_3b_instruct_docminibench_v0_preds.jsonl`
- `outputs/smolvlm_500m_notfound_controlled_v0_preds.jsonl`
- `outputs/smolvlm2_500m_video_notfound_controlled_v0_preds.jsonl`
- `outputs/qwen2_5_vl_3b_instruct_notfound_controlled_v0_preds.jsonl`
- `outputs/smolvlm_500m_docvqa_manual_notfound_combined_expanded_v0_preds.jsonl`
- `outputs/smolvlm2_500m_video_docvqa_manual_notfound_combined_expanded_v0_preds.jsonl`
- `outputs/qwen2_5_vl_3b_instruct_docvqa_manual_notfound_combined_expanded_v0_preds.jsonl`
- `outputs/smolvlm_500m_notfound_ood_sanity_v0_preds.jsonl`
- `outputs/smolvlm2_500m_video_notfound_ood_sanity_v0_preds.jsonl`
- `outputs/qwen2_5_vl_3b_instruct_notfound_ood_sanity_v0_preds.jsonl`

## Reports Created/Updated
- `reports/final_results_tables.md`
- `reports/experiment_matrix_status.md`
- `reports/notfound_comparison_v0.md`
- `reports/lora_sft_poc_results.md`
- `reports/lora_poc_status.md`
- `reports/tomorrow_action_items.md`
- `reports/sft_train_data_spec.md`

## Datasets Evaluated
- `data/docminibench_v0.jsonl`
- `data/docvqa_manual_notfound_combined_expanded_v0_eval.jsonl`
- `data/notfound_controlled_v0.jsonl`
- `data/notfound_ood_sanity_v0_eval_strict.jsonl`

## Models Evaluated
- `qwen2_5_vl_3b_instruct`
- `smolvlm2_500m_video`
- `smolvlm_500m`

## Key Scores
| model_dataset | rows | exact_match | answer_in_output | not_found_false_answer_rate | avg_latency_s |
| --- | --- | --- | --- | --- | --- |
| smolvlm_500m|data/docminibench_v0.jsonl | 120 | 0.4250 | 0.5000 | 1.0000 | 0.4794 |
| smolvlm2_500m_video|data/docminibench_v0.jsonl | 120 | 0.4417 | 0.4750 | 1.0000 | 0.4863 |
| qwen2_5_vl_3b_instruct|data/docminibench_v0.jsonl | 120 | 0.8083 | 0.8167 | 0.0000 | 1.2059 |
| smolvlm_500m|data/notfound_controlled_v0.jsonl | 50 | 0.0000 | 0.0000 | 1.0000 | 0.4142 |
| smolvlm2_500m_video|data/notfound_controlled_v0.jsonl | 50 | 0.0200 | 0.0200 | 0.9800 | 0.7372 |
| qwen2_5_vl_3b_instruct|data/notfound_controlled_v0.jsonl | 50 | 1.0000 | 1.0000 | 0.0000 | 0.4486 |
| smolvlm_500m|data/docvqa_manual_notfound_combined_expanded_v0_eval.jsonl | 85 | 0.0471 | 0.0471 | 0.9529 | 0.5221 |
| smolvlm2_500m_video|data/docvqa_manual_notfound_combined_expanded_v0_eval.jsonl | 85 | 0.0000 | 0.0000 | 1.0000 | 0.6752 |
| qwen2_5_vl_3b_instruct|data/docvqa_manual_notfound_combined_expanded_v0_eval.jsonl | 85 | 0.9647 | 0.9647 | 0.0353 | 1.2480 |
| smolvlm_500m|data/notfound_ood_sanity_v0_eval_strict.jsonl | 20 | 0.0000 | 0.0000 | 1.0000 | 0.6130 |
| smolvlm2_500m_video|data/notfound_ood_sanity_v0_eval_strict.jsonl | 20 | 0.0000 | 0.0000 | 1.0000 | 0.8930 |
| qwen2_5_vl_3b_instruct|data/notfound_ood_sanity_v0_eval_strict.jsonl | 20 | 1.0000 | 1.0000 | 0.0000 | 0.3702 |

## Prompt/Config Caveats
- New marathon runs use `configs/eval_not_found_strict.yaml` and store `answer_instruction` metadata.
- Older default-prompt outputs remain available but are not headline prompt-consistent rows.

## SFT PoC
- Target: `smolvlm2_500m_video`
- Requested steps: 50
- Actual steps: 0 dry-run only
- Checkpoint path: none
- Train data: `data/sft_docvqa_template_train_v0.jsonl`
- Validation data: `data/sft_docvqa_template_val_v0.jsonl`

## Blockers
- Real LoRA training/reload/eval not implemented in scripts/finetune_lora.py scaffold.
- Native template-swapped real-doc SFT negatives omitted because no non-evaluation real document images were locally available.
- Optional SmolVLM2 2.2B reference not attempted.

## Exact Commands
See `logs/codex_marathon_commands.log`.

## Next Recommended Action Items
- Package final report/PDF.
- Implement real LoRA adapter training path if needed.
- Optional SmolVLM2 2.2B reference.
