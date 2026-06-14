# Experiment Matrix Status

Generated UTC: `2026-06-13T16:47:32.096083+00:00`

| Model | Dataset | Run exists | Output path | Metric path | Prompt/config status | Notes |
|---|---|---|---|---|---|---|
| SmolVLM 500M | DocMiniBench-v0 strict | yes | `outputs/smolvlm_500m_docminibench_v0_strict_preds.jsonl` | `reports/smolvlm_500m_docminibench_v0_strict_results.csv` | strict prompt metadata | ok |
| SmolVLM2 500M Video | DocMiniBench-v0 strict | yes | `outputs/smolvlm2_500m_video_docminibench_v0_strict_preds.jsonl` | `reports/smolvlm2_500m_video_docminibench_v0_strict_results.csv` | strict prompt metadata | ok |
| SmolVLM2 2.2B same-family >1B reference | DocMiniBench-v0 strict | yes | `outputs/smolvlm2_2_2b_docminibench_v0_strict_preds.jsonl` | `reports/smolvlm2_2_2b_docminibench_v0_strict_results.csv` | strict prompt metadata | ok |
| Qwen2.5-VL-3B external >1B ceiling | DocMiniBench-v0 strict | yes | `outputs/qwen2_5_vl_3b_instruct_docminibench_v0_preds.jsonl` | `reports/qwen2_5_vl_3b_instruct_docminibench_v0_results.csv` | strict prompt metadata | ok |
| SmolVLM2 500M + 50-step LoRA | DocMiniBench-v0 strict | yes | `outputs/smolvlm2_500m_video_lora_real_docminibench_v0_preds.jsonl` | `reports/smolvlm2_500m_video_lora_real_docminibench_v0_results.csv` | strict prompt + PEFT adapter | ok |
| SmolVLM 500M | controlled NOT_FOUND | yes | `outputs/smolvlm_500m_notfound_controlled_v0_preds.jsonl` | `reports/smolvlm_500m_notfound_controlled_v0_results.csv` | strict prompt metadata | ok |
| SmolVLM2 500M Video | controlled NOT_FOUND | yes | `outputs/smolvlm2_500m_video_notfound_controlled_v0_preds.jsonl` | `reports/smolvlm2_500m_video_notfound_controlled_v0_results.csv` | strict prompt metadata | ok |
| SmolVLM2 2.2B same-family >1B reference | controlled NOT_FOUND | yes | `outputs/smolvlm2_2_2b_notfound_controlled_v0_preds.jsonl` | `reports/smolvlm2_2_2b_notfound_controlled_v0_results.csv` | strict prompt metadata | ok |
| Qwen2.5-VL-3B external >1B ceiling | controlled NOT_FOUND | yes | `outputs/qwen2_5_vl_3b_instruct_notfound_controlled_v0_preds.jsonl` | `reports/qwen2_5_vl_3b_instruct_notfound_controlled_v0_results.csv` | strict prompt metadata | ok |
| SmolVLM2 500M + 50-step LoRA | controlled NOT_FOUND | yes | `outputs/smolvlm2_500m_video_lora_real_notfound_controlled_v0_fixed_preds.jsonl` | `reports/smolvlm2_500m_video_lora_real_notfound_controlled_v0_fixed_results.csv` | strict prompt + PEFT adapter | ok |
| SmolVLM 500M | manual real-doc NOT_FOUND | yes | `outputs/smolvlm_500m_docvqa_manual_notfound_combined_expanded_v0_preds.jsonl` | `reports/smolvlm_500m_docvqa_manual_notfound_combined_expanded_v0_results.csv` | strict prompt metadata | ok |
| SmolVLM2 500M Video | manual real-doc NOT_FOUND | yes | `outputs/smolvlm2_500m_video_docvqa_manual_notfound_combined_expanded_v0_preds.jsonl` | `reports/smolvlm2_500m_video_docvqa_manual_notfound_combined_expanded_v0_results.csv` | strict prompt metadata | ok |
| Qwen2.5-VL-3B external >1B ceiling | manual real-doc NOT_FOUND | yes | `outputs/qwen2_5_vl_3b_instruct_docvqa_manual_notfound_combined_expanded_v0_preds.jsonl` | `reports/qwen2_5_vl_3b_instruct_docvqa_manual_notfound_combined_expanded_v0_results.csv` | strict prompt metadata | ok |
| SmolVLM2 500M + 50-step LoRA | manual real-doc NOT_FOUND | yes | `outputs/smolvlm2_500m_video_lora_real_docvqa_manual_notfound_combined_expanded_v0_preds.jsonl` | `reports/smolvlm2_500m_video_lora_real_docvqa_manual_notfound_combined_expanded_v0_results.csv` | strict prompt + PEFT adapter, normalized eval copy | ok |
| SmolVLM 500M | OOD sanity NOT_FOUND | yes | `outputs/smolvlm_500m_notfound_ood_sanity_v0_preds.jsonl` | `reports/smolvlm_500m_notfound_ood_sanity_v0_results.csv` | strict prompt metadata | ok |
| SmolVLM2 500M Video | OOD sanity NOT_FOUND | yes | `outputs/smolvlm2_500m_video_notfound_ood_sanity_v0_preds.jsonl` | `reports/smolvlm2_500m_video_notfound_ood_sanity_v0_results.csv` | strict prompt metadata | ok |
| Qwen2.5-VL-3B external >1B ceiling | OOD sanity NOT_FOUND | yes | `outputs/qwen2_5_vl_3b_instruct_notfound_ood_sanity_v0_preds.jsonl` | `reports/qwen2_5_vl_3b_instruct_notfound_ood_sanity_v0_results.csv` | strict prompt metadata | ok |
| SmolVLM2 500M + 50-step LoRA | OOD sanity NOT_FOUND | yes | `outputs/smolvlm2_500m_video_lora_real_notfound_ood_sanity_v0_preds.jsonl` | `reports/smolvlm2_500m_video_lora_real_notfound_ood_sanity_v0_results.csv` | strict prompt + PEFT adapter | ok |

The legacy/default-prompt Smol DocMiniBench outputs remain present but are not the preferred strict-prompt cells.
