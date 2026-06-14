# LoRA SFT PoC Results

Updated UTC: `2026-06-14T07:20:55.364679+00:00`

This remains a bounded methodology PoC, not optimized full training. No evaluation rows or images were used for training. Generation metrics are the primary deployed-behavior evaluation; likelihood/margin diagnostics are secondary calibration evidence.

## Learning Curve Check

| Model/checkpoint | DocMiniBench exact | Answerable-only exact | Answerable-only answer_in_output | Old demoted NOT_FOUND false-answer | Controlled false-answer | Manual false-answer | OOD false-answer | Over-abstention on answerable | Avg latency s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Base SmolVLM2 500M | 0.4417 | 0.53 | 0.57 | 1 | 0.98 | 1 | 1 | 0 (0/100) | 0.4863 |
| LoRA 50 total steps | 0.5083 | 0.55 | 0.57 | 0.7 | 0.3 | 0.8941 | 0.75 | 0.01 (1/100) | 0.5418 |
| LoRA 100 total steps | 0.5333 | 0.55 | 0.55 | 0.55 | 0.1 | 0.6235 | 0.2 | 0.02 (2/100) | 0.5308 |

## Prompt Consistency

- Base DocMiniBench reused: `outputs/smolvlm2_500m_video_docminibench_v0_strict_preds.jsonl` with `configs/eval_not_found_strict.yaml`.
- 50-step DocMiniBench reused: `outputs/smolvlm2_500m_video_lora_real_docminibench_v0_preds.jsonl` with `configs/eval_not_found_strict.yaml` and adapter `outputs/lora_sft_poc_real/smolvlm2_500m_video_20260613T162714Z`.
- 100-step DocMiniBench reused: `outputs/smolvlm2_500m_video_lora_real_100step_docminibench_v0_preds.jsonl` with `configs/eval_not_found_strict.yaml` and adapter `outputs/lora_sft_poc_real_continued/smolvlm2_500m_video_continued_20260614T063401Z`.

## Interpretation

- Controlled synthetic NOT_FOUND improved monotonically: base `0.98` false-answer rate, 50-step `0.30`, 100-step `0.10`.
- Manual real-doc NOT_FOUND improved but remains unsolved: base `1.00`, 50-step `0.8941`, 100-step `0.6235`.
- OOD sanity improved: base `1.00`, 50-step `0.75`, 100-step `0.20`. This is non-document sanity only.
- Answerable-only DocMiniBench exact match was roughly preserved: base `0.53`, 50-step `0.55`, 100-step `0.55`. This is not enough evidence to claim broad QA improvement.
- Over-abstention on answerable DocMiniBench rows stayed low but nonzero: base `0/100`, 50-step `1/100`, 100-step `2/100`.
- 100 steps improved NOT_FOUND transfer over 50 steps on controlled, manual, and OOD sets.

## Abstention Diagnostics

See `reports/abstention_likelihood_analysis.md` and `reports/abstention_margin_analysis.md`. Likelihood/margin results are diagnostic calibration evidence, not causal proof and not a replacement for generation metrics.
