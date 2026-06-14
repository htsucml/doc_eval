#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHON_BIN="${PYTHON_BIN:-python}"
if [[ ! -x .venv/bin/python ]]; then
  "$PYTHON_BIN" -m venv .venv
fi

.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt

make test
make smoke

cat <<'MSG'
Lightweight bootstrap complete.

This script intentionally does not download real models, train LoRA adapters,
or run `make full`. For optional GPU reproduction, configure cache/GPU first:

  export DOC_EVAL_CACHE_ROOT=/workspace/hf_home
  make check-full
  FULL_REF_MODELS=0 make full
MSG
