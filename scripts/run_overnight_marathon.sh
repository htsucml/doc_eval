#!/usr/bin/env bash
set -u -o pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p logs outputs reports
MASTER_LOG="logs/overnight_marathon_$(date -u +%Y%m%dT%H%M%SZ).log"
BENCHMARK="${BENCHMARK:-data/fixtures/docminibench_sample.jsonl}"
PRIMARY_MODEL="${PRIMARY_MODEL:-smolvlm_500m}"
FALLBACK_MODELS=(${FALLBACK_MODELS:-smolvlm2_500m_video llava_ov_qwen2_0_5b internvl2_5_1b})
SUCCESSFUL_MODELS=()
FAILED_MODELS=()

log() {
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*"
}

run_stage() {
  local name="$1"
  shift
  log "START $name"
  "$@"
  local status=$?
  if [[ $status -eq 0 ]]; then
    log "PASS $name"
  else
    log "FAIL $name status=$status"
  fi
  return "$status"
}

run_model_full() {
  local model="$1"
  local preds="outputs/${model}_docminibench_v0_preds.jsonl"
  local results="reports/${model}_docminibench_v0_results.csv"
  local markdown="reports/${model}_docminibench_v0_results.md"
  local errors="reports/${model}_docminibench_v0_errors.md"
  local analysis="reports/${model}_docminibench_v0_next_steps.md"

  python scripts/eval_model.py \
    --model "$model" \
    --benchmark "$BENCHMARK" \
    --device cuda \
    --allow-real-models \
    --out "$preds" || return $?

  python scripts/aggregate_results.py \
    --preds "$preds" \
    --benchmark "$BENCHMARK" \
    --out "$results" \
    --markdown "$markdown" || return $?

  python scripts/export_errors.py \
    --preds "$preds" \
    --benchmark "$BENCHMARK" \
    --out "$errors" || return $?

  python scripts/analyze_next_steps.py \
    --results "$results" \
    --errors "$errors" \
    --out "$analysis" || return $?
}

write_handoff() {
  local handoff="reports/overnight_handoff.md"
  {
    echo "# Overnight Handoff"
    echo
    echo "- timestamp_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "- git_commit: $(git rev-parse HEAD 2>/dev/null || true)"
    echo "- benchmark: $BENCHMARK"
    echo "- successful_models: ${SUCCESSFUL_MODELS[*]:-none}"
    echo "- failed_models: ${FAILED_MODELS[*]:-none}"
    echo "- master_log: $MASTER_LOG"
    echo
    echo "## Commands"
    echo
    echo "- bash scripts/run_overnight_marathon.sh"
    echo
    echo "## Notes"
    echo
    echo "- Real model loading was gated by explicit --allow-real-models calls inside this script."
    echo "- Fallback model aliases from the assignment map to repo keys: smolvlm2_500m_video, llava_ov_qwen2_0_5b, internvl2_5_1b."
    echo "- Inspect logs for exact failure messages before reporting final metrics."
  } > "$handoff"
  log "wrote_handoff=$handoff"
}

main() {
  {
    log "START overnight_marathon"
    log "cwd=$PWD"
    log "git_commit=$(git rev-parse HEAD 2>/dev/null || true)"
    log "benchmark=$BENCHMARK"

    if command -v nvidia-smi >/dev/null 2>&1; then
      nvidia-smi
    else
      log "nvidia-smi=not-found"
      log "CUDA unavailable; real model stages are expected to fail closed."
    fi

    run_stage "stage0_env_check" python scripts/check_env.py
    run_stage "stage0_pytest" pytest -q

    run_stage "stage1_${PRIMARY_MODEL}_smoke" bash scripts/run_cuda_smoke.sh

    run_stage "stage2_build_docminibench_v0" python scripts/build_benchmark_v0.py --out "$BENCHMARK"

    if run_stage "stage3_${PRIMARY_MODEL}_full_v0" run_model_full "$PRIMARY_MODEL"; then
      SUCCESSFUL_MODELS+=("$PRIMARY_MODEL")
    else
      FAILED_MODELS+=("$PRIMARY_MODEL")
    fi

    local fallback_ran=0
    for model in "${FALLBACK_MODELS[@]}"; do
      if [[ $fallback_ran -eq 1 ]]; then
        break
      fi
      if run_stage "stage4_${model}_full_v0" run_model_full "$model"; then
        SUCCESSFUL_MODELS+=("$model")
        fallback_ran=1
      else
        FAILED_MODELS+=("$model")
        log "continuing_to_next_fallback_model"
      fi
    done

    for model in "${SUCCESSFUL_MODELS[@]}"; do
      run_stage "stage5_${model}_aggregate_refresh" python scripts/aggregate_results.py \
        --preds "outputs/${model}_docminibench_v0_preds.jsonl" \
        --benchmark "$BENCHMARK" \
        --out "reports/${model}_docminibench_v0_results.csv" \
        --markdown "reports/${model}_docminibench_v0_results.md"
      run_stage "stage5_${model}_errors_refresh" python scripts/export_errors.py \
        --preds "outputs/${model}_docminibench_v0_preds.jsonl" \
        --benchmark "$BENCHMARK" \
        --out "reports/${model}_docminibench_v0_errors.md"
    done

    if [[ ${#SUCCESSFUL_MODELS[@]} -gt 0 ]]; then
      local ablation_benchmark="data/fixtures/docminibench_not_found_ablation.jsonl"
      local ablation_model="${SUCCESSFUL_MODELS[0]}"
      run_stage "stage6_build_ocr_assisted_ablation" python scripts/build_not_found_ablation.py \
        --in "$BENCHMARK" \
        --out "$ablation_benchmark"
      run_stage "stage6_${ablation_model}_ocr_assisted_limit" python scripts/eval_model.py \
        --model "$ablation_model" \
        --benchmark "$ablation_benchmark" \
        --config configs/eval.yaml \
        --limit 3 \
        --device cuda \
        --allow-real-models \
        --out "outputs/${ablation_model}_ocr_ablation_smoke_preds.jsonl"
    else
      log "stage6_skipped=no_zero_shot_outputs"
    fi

    write_handoff
    log "DONE overnight_marathon successful_models=${SUCCESSFUL_MODELS[*]:-none} failed_models=${FAILED_MODELS[*]:-none}"
  } 2>&1 | tee "$MASTER_LOG"
}

main "$@"
