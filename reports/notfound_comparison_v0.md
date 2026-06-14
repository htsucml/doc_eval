# NOT_FOUND Comparison v0

Generated UTC: `2026-06-13T16:47:32.134612+00:00`

## Dataset Status

| Slice | Status | Primary use | Evidence |
|---|---|---|---|
| Original DocMiniBench-v0 NOT_FOUND | exploratory/demoted | not primary | fixed-template questions attached to one old DocVQA image; absence not mechanically proven |
| Controlled synthetic NOT_FOUND | mechanically auditable | primary controlled eval | rendered field inventory plus absent field/value check |
| Manual real-doc NOT_FOUND | assistant-assisted/author spot-checkable | auxiliary real-doc eval | 85 rows, 23 images, visual audit metadata |
| OOD sanity | non-document sanity only | auxiliary robustness sanity | synthetic non-document PIL images |
| Template-swapped NOT_FOUND | noisy train-only | SFT methodology only | not used as benchmark in this run |

## False-answer Rates

| Model | Controlled | Manual real-doc | OOD sanity | DocMiniBench old NOT_FOUND |
|---|---:|---:|---:|---:|
| SmolVLM 500M | 1.0 | 0.9529 | 1.0 | 1.0 |
| SmolVLM2 500M Video | 0.98 | 1.0 | 1.0 | 1.0 |
| SmolVLM2 2.2B same-family >1B reference | 0.24 | not run | not run | 0.4 |
| Qwen2.5-VL-3B external >1B ceiling | 0.0 | 0.0353 | 0.0 | 0.0 |
| SmolVLM2 500M + 50-step LoRA | 0.3 | 0.8941 | 0.75 | 0.7 |

The LoRA adapter substantially improves controlled synthetic NOT_FOUND but does not solve real-doc or OOD NOT_FOUND transfer.
