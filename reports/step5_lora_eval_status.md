# Step 5 LoRA Evaluation Status

- Timestamp UTC: `2026-06-13T16:45:40.899931+00:00`
- Status: `completed`
- Adapter path: `outputs/lora_sft_poc_real/smolvlm2_500m_video_20260613T162714Z`
- Reload verified before evaluation: `True`
- Note: first controlled adapted eval wrote an error-only prediction file due to `peft_adapter_path` leaking into generation kwargs; it was preserved and fixed output was written to `_fixed_preds.jsonl`.

## Metrics

| Dataset | Rows | Exact match | Answer in output | NOT_FOUND false-answer | Error rate | Output |
|---|---:|---:|---:|---:|---:|---|
| Controlled NOT_FOUND, base SmolVLM2 500M | 50 | 0.02 | 0.02 | 0.98 | 0.0 | `outputs/smolvlm2_500m_video_notfound_controlled_v0_preds.jsonl` |
| Controlled NOT_FOUND, LoRA fixed | 50 | 0.7 | 0.7 | 0.3 | 0.0 | `outputs/smolvlm2_500m_video_lora_real_notfound_controlled_v0_fixed_preds.jsonl` |
| DocMiniBench-v0, base strict | 120 | 0.4417 | 0.475 | 1.0 | 0.0 | `outputs/smolvlm2_500m_video_docminibench_v0_strict_preds.jsonl` |
| DocMiniBench-v0, LoRA | 120 | 0.5083 | 0.525 | 0.7 | 0.0 | `outputs/smolvlm2_500m_video_lora_real_docminibench_v0_preds.jsonl` |
| Manual real-doc NOT_FOUND, LoRA | 85 | 0.1059 | 0.1059 | 0.8941 | 0.0 | `outputs/smolvlm2_500m_video_lora_real_docvqa_manual_notfound_combined_expanded_v0_preds.jsonl` |
| OOD sanity NOT_FOUND, LoRA | 20 | 0.25 | 0.25 | 0.75 | 0.0 | `outputs/smolvlm2_500m_video_lora_real_notfound_ood_sanity_v0_preds.jsonl` |

## Interpretation

- The 50-step synthetic LoRA PoC improved controlled synthetic NOT_FOUND for SmolVLM2 500M from mostly false-answering to `0.30` false-answer rate.
- The same adapter did not transfer well to manual real-doc NOT_FOUND (`0.8941` false-answer rate) or OOD sanity (`0.75`).
- DocMiniBench-v0 overall stayed close to base, but the old demoted NOT_FOUND slice worsened; this slice remains exploratory/demoted because its absence provenance is weak.
- This is a bounded methodology PoC, not optimized training.
