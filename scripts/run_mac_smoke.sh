#!/usr/bin/env bash
set -euo pipefail

python scripts/eval_model.py \
  --model smolvlm_500m \
  --benchmark data/fixtures/docminibench_sample.jsonl \
  --limit 3 \
  --device mps \
  --allow-real-models \
  --out outputs/smolvlm_smoke_preds.jsonl

python scripts/aggregate_results.py \
  --preds outputs/smolvlm_smoke_preds.jsonl \
  --benchmark data/fixtures/docminibench_sample.jsonl \
  --out reports/smolvlm_smoke_results.csv \
  --markdown reports/smolvlm_smoke_results.md
