# Final Results Tables

Generated UTC: `2026-06-13T16:47:32.023108+00:00`

Qwen2.5-VL-3B is included only as an external `>1B reference ceiling`; SmolVLM2 2.2B is a same-family `>1B reference`.
LoRA/SFT is a bounded 50-step methodology PoC, not optimized full training.

## DocMiniBench-v0 strict

| Model | Rows | Exact match | Answer in output | NOT_FOUND false-answer | Avg latency | Error rate |
|---|---:|---:|---:|---:|---:|---:|
| SmolVLM 500M | 120 | 0.425 | 0.5 | 1.0 | 0.4794 | 0.0 |
| SmolVLM2 500M Video | 120 | 0.4417 | 0.475 | 1.0 | 0.4863 | 0.0 |
| SmolVLM2 2.2B same-family >1B reference | 120 | 0.525 | 0.5417 | 0.4 | 0.3719 | 0.0 |
| Qwen2.5-VL-3B external >1B ceiling | 120 | 0.8083 | 0.8167 | 0.0 | 1.2059 | 0.0 |
| SmolVLM2 500M + 50-step LoRA | 120 | 0.5083 | 0.525 | 0.7 | 0.5418 | 0.0 |

### Answerable-only DocMiniBench-v0

| Model | Answerable rows | Exact match | Answer in output | Avg latency |
|---|---:|---:|---:|---:|
| SmolVLM 500M | 100 | 0.5100 | 0.6000 | 0.4913 |
| SmolVLM2 500M Video | 100 | 0.5300 | 0.5700 | 0.4549 |
| SmolVLM2 2.2B same-family >1B reference | 100 | 0.5100 | 0.5300 | 0.3710 |
| Qwen2.5-VL-3B external >1B ceiling | 100 | 0.7700 | 0.7800 | 1.1854 |
| SmolVLM2 500M + 50-step LoRA | 100 | 0.5500 | 0.5700 | 0.5369 |

## controlled NOT_FOUND

| Model | Rows | Exact match | Answer in output | NOT_FOUND false-answer | Avg latency | Error rate |
|---|---:|---:|---:|---:|---:|---:|
| SmolVLM 500M | 50 | 0.0 | 0.0 | 1.0 | 0.4142 | 0.0 |
| SmolVLM2 500M Video | 50 | 0.02 | 0.02 | 0.98 | 0.7372 | 0.0 |
| SmolVLM2 2.2B same-family >1B reference | 50 | 0.76 | 0.76 | 0.24 | 0.3602 | 0.0 |
| Qwen2.5-VL-3B external >1B ceiling | 50 | 1.0 | 1.0 | 0.0 | 0.4486 | 0.0 |
| SmolVLM2 500M + 50-step LoRA | 50 | 0.7 | 0.7 | 0.3 | 0.4599 | 0.0 |

## manual real-doc NOT_FOUND

| Model | Rows | Exact match | Answer in output | NOT_FOUND false-answer | Avg latency | Error rate |
|---|---:|---:|---:|---:|---:|---:|
| SmolVLM 500M | 85 | 0.0471 | 0.0471 | 0.9529 | 0.5221 | 0.0 |
| SmolVLM2 500M Video | 85 | 0.0 | 0.0 | 1.0 | 0.6752 | 0.0 |
| Qwen2.5-VL-3B external >1B ceiling | 85 | 0.9647 | 0.9647 | 0.0353 | 1.248 | 0.0 |
| SmolVLM2 500M + 50-step LoRA | 85 | 0.1059 | 0.1059 | 0.8941 | 0.7463 | 0.0 |

## OOD sanity NOT_FOUND

| Model | Rows | Exact match | Answer in output | NOT_FOUND false-answer | Avg latency | Error rate |
|---|---:|---:|---:|---:|---:|---:|
| SmolVLM 500M | 20 | 0.0 | 0.0 | 1.0 | 0.613 | 0.0 |
| SmolVLM2 500M Video | 20 | 0.0 | 0.0 | 1.0 | 0.893 | 0.0 |
| Qwen2.5-VL-3B external >1B ceiling | 20 | 1.0 | 1.0 | 0.0 | 0.3702 | 0.0 |
| SmolVLM2 500M + 50-step LoRA | 20 | 0.25 | 0.25 | 0.75 | 0.8813 | 0.0 |

## Caveats

- Original DocMiniBench-v0 NOT_FOUND is exploratory/demoted; it was not mechanically proven absent.
- Controlled synthetic NOT_FOUND is mechanically auditable.
- Manual real-doc NOT_FOUND is assistant-assisted and author spot-checkable.
- OOD sanity is non-document sanity only, not a document understanding benchmark.
- The first adapted controlled output without `_fixed` is an error-only failed run and should not be used for scoring.
