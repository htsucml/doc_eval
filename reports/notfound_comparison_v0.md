# NOT_FOUND Comparison v0

Generated UTC: `2026-06-14T07:54:01.401864+00:00`

## Dataset Status

| Slice | Status | Primary use | Evidence |
|---|---|---|---|
| Original DocMiniBench-v0 NOT_FOUND | exploratory/demoted | not primary | fixed-template questions attached to one old DocVQA image; absence not mechanically proven |
| Controlled synthetic NOT_FOUND | mechanically auditable | primary controlled eval | rendered field inventory plus absent field/value check |
| Manual real-doc NOT_FOUND | assistant-assisted/author spot-checkable | auxiliary real-doc eval | 85 rows, 23 images, visual audit metadata |
| OOD sanity | non-document sanity only | auxiliary robustness sanity | synthetic non-document PIL images |
| Template-swapped NOT_FOUND | noisy train-only | SFT methodology only | not used as benchmark in this run |

## False-answer Rates

| Model/checkpoint | Controlled | Manual real-doc | OOD sanity | DocMiniBench old NOT_FOUND | Role |
|---|---:|---:|---:|---:|---|
| SmolVLM 500M | 1.0 | 0.9529 | 1.0 | 1.0 | sub-1B target |
| SmolVLM2 500M Video | 0.98 | 1.0 | 1.0 | 1.0 | sub-1B target |
| SmolVLM2 500M + 50-step LoRA | 0.3 | 0.8941 | 0.75 | 0.7 | bounded sub-1B PoC |
| SmolVLM2 500M + 100-step LoRA | 0.1 | 0.6235 | 0.2 | 0.55 | bounded sub-1B PoC |
| SmolVLM2 2.2B | 0.24 | 0.4353 | 0 | 0.4 | same-family >1B reference |
| Qwen2.5-VL-3B | 0.0 | 0.0353 | 0.0 | 0.0 | external >1B ceiling |

## Interpretation

SmolVLM2 2.2B improves substantially over base SmolVLM2 500M on manual real-doc and OOD NOT_FOUND transfer: manual false-answer falls from `1.0` to `0.4353`, and OOD false-answer falls from `1.0` to `0`. It is still a same-family `>1B` reference, not an under-1B target model.

The 100-step LoRA adapter remains the best sub-1B SmolVLM2 result in this matrix for controlled NOT_FOUND, but 2.2B scale is stronger on manual real-doc transfer. Qwen2.5-VL-3B remains the external ceiling, especially on manual real-doc NOT_FOUND.

Strict exact `NOT_FOUND` is reported separately from false-answer rate: on these NOT_FOUND-only slices, false-answer rate is `1 - exact_NOT_FOUND_rate` for valid predictions.
