#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHON="${PYTHON:-.venv/bin/python}"
FULL_DEVICE="${FULL_DEVICE:-cuda}"
FULL_TRAIN_STEPS="${FULL_TRAIN_STEPS:-100}"
FULL_REF_MODELS="${FULL_REF_MODELS:-0}"
FULL_LIMIT="${FULL_LIMIT:-}"
FULL_TIMEOUT_TARGET="${FULL_TIMEOUT_TARGET:-45m}"
FULL_TIMEOUT_REF="${FULL_TIMEOUT_REF:-45m}"
FULL_TIMEOUT_TRAIN="${FULL_TIMEOUT_TRAIN:-3h}"
STAMP="${FULL_STAMP:-$(date -u +%Y%m%dT%H%M%SZ)}"

if [[ -n "${DOC_EVAL_CACHE_ROOT:-}" ]]; then
  CACHE_ROOT="$DOC_EVAL_CACHE_ROOT"
elif [[ -d /workspace && -w /workspace ]]; then
  CACHE_ROOT="/workspace/hf_home"
elif [[ -n "${HF_HOME:-}" ]]; then
  CACHE_ROOT="$HF_HOME"
else
  CACHE_ROOT="$HOME/.cache/doc_eval_hf"
fi
export HF_HOME="$CACHE_ROOT"
export HF_HUB_CACHE="$CACHE_ROOT/hub"
export HUGGINGFACE_HUB_CACHE="$CACHE_ROOT/hub"
export HF_DATASETS_CACHE="$CACHE_ROOT/datasets"
mkdir -p "$HF_HUB_CACHE" "$HF_DATASETS_CACHE"

echo "Running full reproduction preflight before creating a timestamped run directory."
FULL_DEVICE="$FULL_DEVICE" FULL_REF_MODELS="$FULL_REF_MODELS" "$PYTHON" scripts/check_full_repro.py --device "$FULL_DEVICE" --ref-models "$FULL_REF_MODELS"

OUT_DIR="outputs/full_repro/$STAMP"
REPORT_DIR="reports/full_repro/$STAMP"
mkdir -p "$OUT_DIR" "$REPORT_DIR"
ln -sfn "$STAMP" outputs/full_repro/latest
ln -sfn "$STAMP" reports/full_repro/latest

LOG="$REPORT_DIR/full_repro_commands.log"
exec > >(tee -a "$LOG") 2>&1

write_status() {
  local status="$1"
  local message="${2:-}"
  "$PYTHON" - "$REPORT_DIR/run_status.json" "$status" "$message" <<'PY'
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

path = Path(sys.argv[1])
payload = {
    "status": sys.argv[2],
    "message": sys.argv[3],
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
}
path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
PY
}

on_error() {
  local rc=$?
  write_status "failed" "run_full_repro.sh exited with status $rc"
  exit "$rc"
}
trap on_error ERR
write_status "running" "full reproduction started"

run_cmd() {
  echo
  echo "+ $*"
  "$@"
}

eval_model() {
  local model="$1" dataset_name="$2" benchmark="$3" timeout_value="$4" extra_label="${5:-}"
  local label="${model}_${dataset_name}${extra_label}"
  local out="$OUT_DIR/${label}_preds.jsonl"
  local args=(timeout "$timeout_value" "$PYTHON" scripts/eval_model.py --model "$model" --benchmark "$benchmark" --out "$out" --config configs/eval_not_found_strict.yaml --device "$FULL_DEVICE" --allow-real-models)
  if [[ -n "$FULL_LIMIT" ]]; then
    args+=(--limit "$FULL_LIMIT")
  fi
  run_cmd "${args[@]}"
  run_cmd "$PYTHON" scripts/aggregate_results.py --preds "$out" --benchmark "$benchmark" --out "$REPORT_DIR/${label}_results.csv" --markdown "$REPORT_DIR/${label}_results.md"
}

eval_lora() {
  local adapter="$1" dataset_name="$2" benchmark="$3"
  local label="smolvlm2_500m_video_lora_${dataset_name}"
  local out="$OUT_DIR/${label}_preds.jsonl"
  local args=(timeout "$FULL_TIMEOUT_TARGET" "$PYTHON" scripts/eval_model.py --model smolvlm2_500m_video --benchmark "$benchmark" --out "$out" --config configs/eval_not_found_strict.yaml --device "$FULL_DEVICE" --allow-real-models --peft-adapter-path "$adapter")
  if [[ -n "$FULL_LIMIT" ]]; then
    args+=(--limit "$FULL_LIMIT")
  fi
  run_cmd "${args[@]}"
  run_cmd "$PYTHON" scripts/aggregate_results.py --preds "$out" --benchmark "$benchmark" --out "$REPORT_DIR/${label}_results.csv" --markdown "$REPORT_DIR/${label}_results.md"
}

echo "full_repro_stamp=$STAMP"
echo "cache_root=$CACHE_ROOT"
echo "out_dir=$OUT_DIR"
echo "report_dir=$REPORT_DIR"
echo "FULL_REF_MODELS=$FULL_REF_MODELS"
echo "FULL_TRAIN_STEPS=$FULL_TRAIN_STEPS"
echo "FULL_LIMIT=${FULL_LIMIT:-<full>}"

run_cmd make test
run_cmd make smoke

for model in smolvlm_500m smolvlm2_500m_video; do
  eval_model "$model" docminibench_v0 data/docminibench_v0.jsonl "$FULL_TIMEOUT_TARGET"
  eval_model "$model" notfound_controlled_v0 data/notfound_controlled_v0.jsonl "$FULL_TIMEOUT_TARGET"
  eval_model "$model" docvqa_manual_notfound_combined_expanded_v0 data/docvqa_manual_notfound_combined_expanded_v0_eval.jsonl "$FULL_TIMEOUT_TARGET"
  eval_model "$model" notfound_ood_sanity_v0 data/notfound_ood_sanity_v0_eval_strict.jsonl "$FULL_TIMEOUT_TARGET"
done

if [[ "$FULL_REF_MODELS" == "1" ]]; then
  for model in smolvlm2_2_2b qwen2_5_vl_3b_instruct; do
    for item in \
      "docminibench_v0 data/docminibench_v0.jsonl" \
      "notfound_controlled_v0 data/notfound_controlled_v0.jsonl" \
      "docvqa_manual_notfound_combined_expanded_v0 data/docvqa_manual_notfound_combined_expanded_v0_eval.jsonl" \
      "notfound_ood_sanity_v0 data/notfound_ood_sanity_v0_eval_strict.jsonl"; do
      set +e
      eval_model "$model" ${item} "$FULL_TIMEOUT_REF"
      rc=$?
      set -e
      if [[ $rc -ne 0 ]]; then
        echo "reference_skip model=$model item=$item rc=$rc" | tee -a "$REPORT_DIR/skipped_reference_models.log"
      fi
    done
  done
else
  echo "Reference models skipped by default. Set FULL_REF_MODELS=1 to include SmolVLM2 2.2B and Qwen2.5-VL 3B." | tee "$REPORT_DIR/skipped_reference_models.log"
fi

LORA_ROOT="$OUT_DIR/lora_sft"
run_cmd timeout "$FULL_TIMEOUT_TRAIN" "$PYTHON" scripts/finetune_lora.py \
  --model smolvlm2_500m_video \
  --train data/sft_docvqa_template_train_v0.jsonl \
  --val data/sft_docvqa_template_val_v0.jsonl \
  --max_steps "$FULL_TRAIN_STEPS" \
  --output-dir "$LORA_ROOT" \
  --device "$FULL_DEVICE" \
  --verify-reload

ADAPTER_PATH="$(find "$LORA_ROOT" -mindepth 1 -maxdepth 1 -type d -name 'smolvlm2_500m_video_*' | sort | tail -n 1)"
if [[ -z "$ADAPTER_PATH" ]]; then
  echo "LoRA training did not produce an adapter path under $LORA_ROOT" >&2
  exit 1
fi
echo "$ADAPTER_PATH" > "$REPORT_DIR/lora_adapter_path.txt"

eval_lora "$ADAPTER_PATH" docminibench_v0 data/docminibench_v0.jsonl
eval_lora "$ADAPTER_PATH" notfound_controlled_v0 data/notfound_controlled_v0.jsonl
eval_lora "$ADAPTER_PATH" docvqa_manual_notfound_combined_expanded_v0 data/docvqa_manual_notfound_combined_expanded_v0_eval.jsonl
eval_lora "$ADAPTER_PATH" notfound_ood_sanity_v0 data/notfound_ood_sanity_v0_eval_strict.jsonl

set +e
run_cmd "$PYTHON" scripts/analyze_abstention_margin.py \
  --device "$FULL_DEVICE" \
  --controlled-limit "${FULL_MARGIN_CONTROLLED_LIMIT:-10}" \
  --manual-limit "${FULL_MARGIN_MANUAL_LIMIT:-10}" \
  --answerable-limit "${FULL_MARGIN_ANSWERABLE_LIMIT:-20}" \
  --ood-limit "${FULL_MARGIN_OOD_LIMIT:-10}" \
  --base-doc-preds "$OUT_DIR/smolvlm2_500m_video_docminibench_v0_preds.jsonl" \
  --base-controlled-preds "$OUT_DIR/smolvlm2_500m_video_notfound_controlled_v0_preds.jsonl" \
  --base-manual-preds "$OUT_DIR/smolvlm2_500m_video_docvqa_manual_notfound_combined_expanded_v0_preds.jsonl" \
  --base-ood-preds "$OUT_DIR/smolvlm2_500m_video_notfound_ood_sanity_v0_preds.jsonl" \
  --lora-adapter-path "$ADAPTER_PATH" \
  --lora-doc-preds "$OUT_DIR/smolvlm2_500m_video_lora_docminibench_v0_preds.jsonl" \
  --lora-controlled-preds "$OUT_DIR/smolvlm2_500m_video_lora_notfound_controlled_v0_preds.jsonl" \
  --lora-manual-preds "$OUT_DIR/smolvlm2_500m_video_lora_docvqa_manual_notfound_combined_expanded_v0_preds.jsonl" \
  --lora-ood-preds "$OUT_DIR/smolvlm2_500m_video_lora_notfound_ood_sanity_v0_preds.jsonl" \
  --no-historical-100step \
  --out-csv "$REPORT_DIR/abstention_margin_analysis.csv" \
  --out-md "$REPORT_DIR/abstention_margin_analysis.md"
margin_rc=$?
set -e
if [[ $margin_rc -ne 0 ]]; then
  echo "abstention_margin_status=failed rc=$margin_rc" | tee "$REPORT_DIR/abstention_margin_status.txt"
fi

write_status "complete" "full reproduction completed"
run_cmd "$PYTHON" scripts/print_full_results.py --run "$STAMP" --write-handoff
write_status "complete" "full reproduction completed and handoff written"
echo "full_repro_complete=$STAMP"
