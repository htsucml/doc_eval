# SmolVLM2 2.2B Status

Generated UTC: `2026-06-14T07:54:01.401864+00:00`

- Status: `ran successfully` on all requested reference cells.
- Model: `HuggingFaceTB/SmolVLM2-2.2B-Instruct`
- Role: same-family `>1B` reference for SmolVLM2 500M, not a sub-1B target model.
- Cache routing: HF cache resolved under `/workspace/hf_home`; no model cache written to `/root`.

## Results

| Dataset | Rows | Exact match | Answer in output | NOT_FOUND false-answer | Avg latency s | Output | Metrics |
|---|---:|---:|---:|---:|---:|---|---|
| Controlled NOT_FOUND | 50 | 0.76 | 0.76 | 0.24 | 0.3602 | `outputs/smolvlm2_2_2b_notfound_controlled_v0_preds.jsonl` | `reports/smolvlm2_2_2b_notfound_controlled_v0_results.csv` |
| DocMiniBench-v0 strict | 120 | 0.525 | 0.5417 | 0.4 | 0.3719 | `outputs/smolvlm2_2_2b_docminibench_v0_strict_preds.jsonl` | `reports/smolvlm2_2_2b_docminibench_v0_strict_results.csv` |
| Manual real-doc NOT_FOUND | 85 | 0.5647 | 0.5647 | 0.4353 | 0.5088 | `outputs/smolvlm2_2_2b_docvqa_manual_notfound_combined_expanded_v0_preds.jsonl` | `reports/smolvlm2_2_2b_docvqa_manual_notfound_combined_expanded_v0_results.csv` |
| OOD sanity NOT_FOUND | 20 | 1 | 1 | 0 | 0.5615 | `outputs/smolvlm2_2_2b_notfound_ood_sanity_v0_preds.jsonl` | `reports/smolvlm2_2_2b_notfound_ood_sanity_v0_results.csv` |

## Interpretation

Scale helps relative to base SmolVLM2 500M on manual real-doc and OOD NOT_FOUND. The 2.2B model reached exact `NOT_FOUND` on all OOD sanity rows and reduced manual false-answer rate to `0.4353`, but it remains below Qwen2.5-VL-3B on manual real-doc abstention.
