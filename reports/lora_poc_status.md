# LoRA SFT PoC Results

Updated UTC: `2026-06-14T06:52:02.249867+00:00`

This remains a bounded methodology PoC, not optimized full training. No evaluation rows or images were used for training.

## Learning Curve Check

| Checkpoint | Controlled false-answer | DocMiniBench exact | DocMiniBench NOT_FOUND false-answer | Manual real-doc false-answer | OOD false-answer | Over-abstention on DocMiniBench answerable |
|---|---:|---:|---:|---:|---:|---:|
| Base SmolVLM2 500M | 0.98 | 0.4417 | 1.0 | not run | not run | n/a |
| LoRA 50 total steps | 0.3 | 0.5083 | 0.7 | 0.8941 | 0.75 | 0.0100 (1/100) |
| LoRA 100 total steps | 0.1 | 0.5333 | 0.55 | 0.6235 | 0.2 | 0.0200 (2/100) |

## Checkpoints

- 50-step adapter: `outputs/lora_sft_poc_real/smolvlm2_500m_video_20260613T162714Z`
- 100-total-step adapter: `outputs/lora_sft_poc_real_continued/smolvlm2_500m_video_continued_20260614T063401Z`
- The 100-step adapter was continued from the 50-step adapter using the same controlled synthetic train/val data.

## Interpretation

- Controlled synthetic NOT_FOUND improved monotonically from base `0.98` false-answer rate to `0.30` at 50 steps and `0.10` at 100 steps.
- Manual real-doc NOT_FOUND improved from `0.8941` at 50 steps to `0.6235` at 100 steps, but remains far from solved.
- OOD sanity improved to `0.20` false-answer rate at 100 steps.
- DocMiniBench overall exact match at 100 steps (`0.5333`) is slightly above base strict SmolVLM2 500M, but old DocMiniBench NOT_FOUND remains demoted/exploratory.
- Over-abstention on answerable DocMiniBench rows was 0/100 for both LoRA checkpoints in this run.

## Abstention Likelihood Diagnostic

See `reports/abstention_likelihood_analysis.md`. On the first 20 controlled NOT_FOUND rows, `NOT_FOUND` was top-ranked for 2/20 base SmolVLM2 rows, 18/20 LoRA rows, 19/20 SmolVLM2 2.2B rows, and 20/20 Qwen2.5-VL-3B rows.
