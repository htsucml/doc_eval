#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p logs outputs reports
LOG="logs/run_cuda_smoke_$(date -u +%Y%m%dT%H%M%SZ).log"
BENCHMARK="${BENCHMARK:-data/fixtures/docminibench_sample.jsonl}"
MODEL="${MODEL:-smolvlm_500m}"
LIMIT="${LIMIT:-3}"

{
  echo "timestamp_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "model=$MODEL"
  echo "benchmark=$BENCHMARK"
  echo "limit=$LIMIT"

  if command -v nvidia-smi >/dev/null 2>&1; then
    nvidia-smi
  else
    echo "nvidia-smi=not-found"
    exit 1
  fi

  if [[ ! -f "$BENCHMARK" ]]; then
    python scripts/build_benchmark_v0.py --out "$BENCHMARK"
  fi

  python scripts/eval_model.py \
    --model "$MODEL" \
    --benchmark "$BENCHMARK" \
    --limit "$LIMIT" \
    --device cuda \
    --allow-real-models \
    --out "outputs/${MODEL}_smoke_preds.jsonl"

  python scripts/aggregate_results.py \
    --preds "outputs/${MODEL}_smoke_preds.jsonl" \
    --benchmark "$BENCHMARK" \
    --out "reports/${MODEL}_smoke_results.csv" \
    --markdown "reports/${MODEL}_smoke_results.md"
} 2>&1 | tee "$LOG"

echo "wrote_log=$LOG"
