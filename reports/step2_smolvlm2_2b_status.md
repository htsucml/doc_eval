# Step 2 SmolVLM2 2.2B Status

- Status: controlled NOT_FOUND and DocMiniBench-v0 strict runs succeeded
- Timestamp UTC: `2026-06-13T16:15:08.351147+00:00`
- Model: `smolvlm2_2_2b`
- HF model id: `HuggingFaceTB/SmolVLM2-2.2B-Instruct`
- Cache routing: `HF_HOME=/workspace/hf_home`

## Controlled NOT_FOUND

- Output: `outputs/smolvlm2_2_2b_notfound_controlled_v0_preds.jsonl`
- Results: `reports/smolvlm2_2_2b_notfound_controlled_v0_results.csv`
- Rows: `50`
- Strict exact_match: `0.76`
- Answer in output: `0.76`
- NOT_FOUND false-answer rate: `0.24`
- Avg latency: `0.3602`

## DocMiniBench-v0 Strict

- Output: `outputs/smolvlm2_2_2b_docminibench_v0_strict_preds.jsonl`
- Results: `reports/smolvlm2_2_2b_docminibench_v0_strict_results.csv`
- Rows: `120`
- Strict exact_match: `0.525`
- Answer in output: `0.5417`
- NOT_FOUND false-answer rate: `0.4`
- Avg latency: `0.3719`

Manual real-doc NOT_FOUND was not attempted in this step because the requested second run target was DocMiniBench-v0 after controlled success; remaining time was reserved for SFT rescue.
