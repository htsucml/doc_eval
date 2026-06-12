#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p logs
LOG="logs/setup_runpod_env_$(date -u +%Y%m%dT%H%M%SZ).log"

{
  echo "timestamp_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "cwd=$PWD"
  echo "git_commit=$(git rev-parse HEAD 2>/dev/null || true)"

  if [[ ! -d .venv ]]; then
    python -m venv .venv
  fi

  # shellcheck disable=SC1091
  source .venv/bin/activate
  python -m pip install --upgrade pip
  python -m pip install -r requirements-gpu.txt

  if command -v nvidia-smi >/dev/null 2>&1; then
    nvidia-smi
  else
    echo "nvidia-smi=not-found"
  fi

  python scripts/check_env.py
  pytest -q
} 2>&1 | tee "$LOG"

echo "wrote_log=$LOG"
