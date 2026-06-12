# Improvement PoC Status

## Attempted PoC

Attempt: stricter NOT_FOUND prompt ablation on the 20-row `not_found` capability slice using SmolVLM 500M.

Command:

```bash
timeout 15m python scripts/eval_model.py \
  --model smolvlm_500m \
  --benchmark data/docminibench_v0.jsonl \
  --config configs/eval_not_found_strict.yaml \
  --capability not_found \
  --device cuda \
  --allow-real-models \
  --out outputs/smolvlm_500m_not_found_strict_poc_preds.jsonl
```

## Result

The PoC did not improve abstention.

| model/config | rows | strict_exact_match | answer_in_output | not_found_false_answer_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: |
| SmolVLM 500M, default final-value prompt, not_found slice | 20 | 0.0000 | 0.0000 | 1.0000 | 0.4230 |
| SmolVLM 500M, strict NOT_FOUND prompt, not_found slice | 20 | 0.0000 | 0.0000 | 1.0000 | 0.6372 |

The strict prompt still produced concrete values such as `1980.`, `0.28`, `0.22`, `1001777777`, `1950`, and `USPS.`.

OCR-assisted prompting was not run because `data/docminibench_v0.jsonl` currently contains no `metadata.ocr_text` fields. Running `image_plus_ocr` would therefore be equivalent to image-only prompting for this benchmark.

## Next Step

Use a bounded OCR extraction pass to populate `metadata.ocr_text`, then rerun a small NOT_FOUND and OCR-heavy slice with `prompt_mode=image_plus_ocr`. If abstention still fails, add a lightweight answerability gate before generation or train a tiny negative-example LoRA with strict no-guess examples.
