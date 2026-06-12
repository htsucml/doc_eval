# Overnight Handoff

## Snapshot

- git_commit: TO_BE_UPDATED_AFTER_COMMIT
- benchmark: `data/docminibench_v0.jsonl`
- benchmark_sha256: `a03022faa968e32072abbe9eceaa01ed7a2ec1cc91cb22cdfb4b3162274aa596`
- sample_count: 120
- device: NVIDIA GeForce RTX 4090, driver 565.57.01, 24564 MiB
- python: 3.11.10
- torch: 2.12.0+cu126
- cuda_available: true
- transformers: 5.12.0

## Models

| model | status | notes |
| --- | --- | --- |
| `smolvlm_500m` | succeeded | 120-row CUDA eval completed with `--allow-real-models`. |
| `smolvlm2_500m_video` | succeeded | First attempt failed on missing `num2words`; installed with pip, added to `requirements-gpu.txt`, retry succeeded. |
| `llava_ov_qwen2_0_5b` | not attempted | Not needed because SmolVLM2 succeeded. Adapter remains placeholder. |
| `internvl2_5_1b` | not attempted | Not needed because SmolVLM2 succeeded. Adapter remains placeholder. |

## Commands

```bash
BENCHMARK=data/docminibench_v0.jsonl timeout 45m bash scripts/run_docminibench_v0.sh smolvlm_500m
BENCHMARK=data/docminibench_v0.jsonl timeout 45m bash scripts/run_docminibench_v0.sh smolvlm2_500m_video
timeout 15m python scripts/eval_model.py --model smolvlm_500m --benchmark data/docminibench_v0.jsonl --config configs/eval_not_found_strict.yaml --capability not_found --device cuda --allow-real-models --out outputs/smolvlm_500m_not_found_strict_poc_preds.jsonl
pytest -q
git diff --check
```

## Artifacts

Reports:

- `reports/model_comparison_v0.md`
- `reports/analysis_v0.md`
- `reports/improvement_poc_status.md`
- `reports/overnight_handoff.md`
- `reports/smolvlm_500m_docminibench_v0_results.csv`
- `reports/smolvlm_500m_docminibench_v0_results.md`
- `reports/smolvlm_500m_docminibench_v0_errors.md`
- `reports/smolvlm2_500m_video_docminibench_v0_results.csv`
- `reports/smolvlm2_500m_video_docminibench_v0_results.md`
- `reports/smolvlm2_500m_video_docminibench_v0_errors.md`
- `reports/smolvlm_500m_not_found_strict_poc_results.csv`
- `reports/smolvlm_500m_not_found_strict_poc_results.md`
- `reports/smolvlm_500m_not_found_strict_poc_errors.md`

Outputs:

- `outputs/smolvlm_500m_docminibench_v0_preds.jsonl`
- `outputs/smolvlm_500m_docminibench_v0_preds.meta.json`
- `outputs/smolvlm2_500m_video_docminibench_v0_preds.jsonl`
- `outputs/smolvlm2_500m_video_docminibench_v0_preds.meta.json`
- `outputs/smolvlm_500m_not_found_strict_poc_preds.jsonl`
- `outputs/smolvlm_500m_not_found_strict_poc_preds.meta.json`

Logs:

- `logs/run_docminibench_v0_smolvlm_500m_20260612T164950Z.log`
- `logs/run_docminibench_v0_smolvlm2_500m_video_20260612T165251Z.log`
- `logs/run_docminibench_v0_smolvlm2_500m_video_20260612T165430Z.log`

## Blockers

No active blocker. SmolVLM2 needed `num2words`; fixed in the venv and added to GPU requirements. OCR-assisted prompting is blocked on absent `metadata.ocr_text` in the real benchmark rows.

## Next Actions

1. Populate OCR text for real benchmark rows and rerun a small `image_plus_ocr` ablation.
2. Add an answerability gate or negative-example LoRA for NOT_FOUND behavior.
3. Decide whether strict exact_match or containment should drive model selection for each product-facing slice.
