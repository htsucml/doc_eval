#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

MODEL="${1:-${MODEL:-smolvlm_500m}}"
BENCHMARK="${BENCHMARK:-data/fixtures/docminibench_sample.jsonl}"
LIMIT_ARGS=()
if [[ -n "${LIMIT:-}" ]]; then
  LIMIT_ARGS=(--limit "$LIMIT")
fi

mkdir -p logs outputs reports
LOG="logs/run_docminibench_v0_${MODEL}_$(date -u +%Y%m%dT%H%M%SZ).log"
PREDS="outputs/${MODEL}_docminibench_v0_preds.jsonl"
RESULTS="reports/${MODEL}_docminibench_v0_results.csv"
MARKDOWN="reports/${MODEL}_docminibench_v0_results.md"
ERRORS="reports/${MODEL}_docminibench_v0_errors.md"
ANALYSIS="reports/${MODEL}_docminibench_v0_next_steps.md"

{
  echo "timestamp_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "model=$MODEL"
  echo "benchmark=$BENCHMARK"
  echo "limit=${LIMIT:-none}"

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
    --device cuda \
    --allow-real-models \
    "${LIMIT_ARGS[@]}" \
    --out "$PREDS"

  python scripts/aggregate_results.py \
    --preds "$PREDS" \
    --benchmark "$BENCHMARK" \
    --out "$RESULTS" \
    --markdown "$MARKDOWN"

  python scripts/export_errors.py \
    --preds "$PREDS" \
    --benchmark "$BENCHMARK" \
    --out "$ERRORS"

  python scripts/analyze_next_steps.py \
    --results "$RESULTS" \
    --errors "$ERRORS" \
    --out "$ANALYSIS"
} 2>&1 | tee "$LOG"

echo "wrote_log=$LOG"
