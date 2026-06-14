# Final Results Tables

Updated UTC: `2026-06-14T07:54:01.401864+00:00`

Qwen2.5-VL-3B is an external `>1B reference ceiling`; SmolVLM2 2.2B is a same-family `>1B reference`. LoRA rows are bounded methodology PoC checkpoints.

## LoRA Learning Curve Add-on

| Model/checkpoint | DocMiniBench exact | Answerable-only exact | Answerable-only answer_in_output | Old demoted NOT_FOUND false-answer | Controlled false-answer | Manual false-answer | OOD false-answer | Over-abstention on answerable | Avg latency s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Base SmolVLM2 500M | 0.4417 | 0.53 | 0.57 | 1 | 0.98 | 1 | 1 | 0 (0/100) | 0.4863 |
| LoRA 50 total steps | 0.5083 | 0.55 | 0.57 | 0.7 | 0.3 | 0.8941 | 0.75 | 0.01 (1/100) | 0.5418 |
| LoRA 100 total steps | 0.5333 | 0.55 | 0.55 | 0.55 | 0.1 | 0.6235 | 0.2 | 0.02 (2/100) | 0.5308 |

## Reference Cells

| Model | Dataset | Rows | Exact match | Answer in output | NOT_FOUND false-answer | Avg latency s | Role |
|---|---|---:|---:|---:|---:|---:|---|
| SmolVLM2 2.2B | DocMiniBench-v0 | 120 | 0.525 | 0.5417 | 0.4 | 0.3719 | same-family >1B reference |
| SmolVLM2 2.2B | controlled NOT_FOUND | 50 | 0.76 | 0.76 | 0.24 | 0.3602 | same-family >1B reference |
| SmolVLM2 2.2B | manual real-doc NOT_FOUND | 85 | 0.5647 | 0.5647 | 0.4353 | 0.5088 | same-family >1B reference |
| SmolVLM2 2.2B | OOD sanity NOT_FOUND | 20 | 1 | 1 | 0 | 0.5615 | same-family >1B reference |
| Qwen2.5-VL-3B | controlled NOT_FOUND | 50 | 1.0 | 1.0 | 0.0 | 0.4486 | external >1B ceiling |
| Qwen2.5-VL-3B | manual real-doc NOT_FOUND | 85 | 0.9647 | 0.9647 | 0.0353 | 1.248 | external >1B ceiling |
| Qwen2.5-VL-3B | OOD sanity NOT_FOUND | 20 | 1.0 | 1.0 | 0.0 | 0.3702 | external >1B ceiling |

## Bottom Line

The 100-step LoRA checkpoint substantially improves generated `NOT_FOUND` behavior on controlled, manual, and OOD NOT_FOUND tests while answerable-only DocMiniBench exact match remains approximately flat. The newly completed SmolVLM2 2.2B same-family reference shows that scale helps on manual real-doc NOT_FOUND and OOD sanity compared with base SmolVLM2 500M, but Qwen2.5-VL-3B remains the stronger external ceiling on manual real-doc abstention.

## Caveats

- Original DocMiniBench-v0 NOT_FOUND remains exploratory/demoted.
- Controlled synthetic NOT_FOUND is mechanically auditable.
- Manual real-doc NOT_FOUND is assistant-assisted/author spot-checkable.
- OOD sanity is non-document sanity only.
- SmolVLM2 2.2B is a same-family `>1B` reference only, not part of the under-1B target comparison.
- Likelihood and margin analyses are diagnostic, not causal proof.
