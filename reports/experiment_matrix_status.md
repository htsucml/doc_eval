# Experiment Matrix Status

Generated UTC: `2026-06-14T07:54:01.401864+00:00`

| Model | Dataset | Run exists | Output path | Metric path | Prompt/config status | Notes |
|---|---|---|---|---|---|---|
| SmolVLM 500M | DocMiniBench-v0 strict | yes | `outputs/smolvlm_500m_docminibench_v0_strict_preds.jsonl` | `reports/smolvlm_500m_docminibench_v0_strict_results.csv` | strict prompt metadata | sub-1B target |
| SmolVLM2 500M Video | DocMiniBench-v0 strict | yes | `outputs/smolvlm2_500m_video_docminibench_v0_strict_preds.jsonl` | `reports/smolvlm2_500m_video_docminibench_v0_strict_results.csv` | strict prompt metadata | sub-1B target |
| SmolVLM2 2.2B | DocMiniBench-v0 strict | yes | `outputs/smolvlm2_2_2b_docminibench_v0_strict_preds.jsonl` | `reports/smolvlm2_2_2b_docminibench_v0_strict_results.csv` | strict prompt metadata | same-family >1B reference |
| Qwen2.5-VL-3B | DocMiniBench-v0 strict | yes | `outputs/qwen2_5_vl_3b_instruct_docminibench_v0_preds.jsonl` | `reports/qwen2_5_vl_3b_instruct_docminibench_v0_results.csv` | strict prompt metadata | external >1B ceiling |
| SmolVLM2 500M + 50-step LoRA | DocMiniBench-v0 strict | yes | `outputs/smolvlm2_500m_video_lora_real_docminibench_v0_preds.jsonl` | `reports/smolvlm2_500m_video_lora_real_docminibench_v0_results.csv` | strict prompt + PEFT adapter | bounded PoC |
| SmolVLM2 500M + 100-step LoRA | DocMiniBench-v0 strict | yes | `outputs/smolvlm2_500m_video_lora_real_100step_docminibench_v0_preds.jsonl` | `reports/smolvlm2_500m_video_lora_real_100step_docminibench_v0_results.csv` | strict prompt + PEFT adapter | bounded PoC |
| SmolVLM2 2.2B | controlled NOT_FOUND | yes | `outputs/smolvlm2_2_2b_notfound_controlled_v0_preds.jsonl` | `reports/smolvlm2_2_2b_notfound_controlled_v0_results.csv` | strict prompt metadata | same-family >1B reference |
| SmolVLM2 2.2B | manual real-doc NOT_FOUND | yes | `outputs/smolvlm2_2_2b_docvqa_manual_notfound_combined_expanded_v0_preds.jsonl` | `reports/smolvlm2_2_2b_docvqa_manual_notfound_combined_expanded_v0_results.csv` | strict prompt metadata, normalized eval copy | same-family >1B reference; completed in reference add-on |
| SmolVLM2 2.2B | OOD sanity NOT_FOUND | yes | `outputs/smolvlm2_2_2b_notfound_ood_sanity_v0_preds.jsonl` | `reports/smolvlm2_2_2b_notfound_ood_sanity_v0_results.csv` | strict prompt metadata, eval strict copy | same-family >1B reference; completed in reference add-on |
| Qwen2.5-VL-3B | controlled/manual/OOD NOT_FOUND | yes | see `outputs/qwen2_5_vl_3b_instruct_*_preds.jsonl` | see matching `reports/qwen2_5_vl_3b_instruct_*_results.csv` | strict prompt metadata | external >1B ceiling |
| SmolVLM/SmoLVLM2 500M target NOT_FOUND cells | yes | see matching `outputs/*notfound*_preds.jsonl` | see matching `reports/*notfound*_results.csv` | strict prompt metadata | target sub-1B comparisons |

The legacy/default-prompt Smol DocMiniBench outputs remain present but are not the preferred strict-prompt cells.
