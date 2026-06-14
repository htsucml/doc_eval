#!/usr/bin/env bash
set -euo pipefail

DEFAULT_DATA_URL="https://www.dropbox.com/scl/fi/tu1a5eo7itq55nrrslahv/doc_eval_external_artifacts_20260614_data_v1.tgz?rlkey=mmjplcdgxe40yo25r0uke9xfg&st=1gf9foi1&dl=1"
DEFAULT_SHA_URL="https://www.dropbox.com/scl/fi/gqhgo4sotzjk1u5muec5s/doc_eval_external_artifacts_20260614_data_v1.sha256?rlkey=ypmqr51094aqhphz3vyqrt4z8&st=4tgplkyu&dl=1"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BOOTSTRAP_PYTHON="${BOOTSTRAP_PYTHON:-python3}"
EXTRACT_ROOT="${DOC_EVAL_EXTRACT_ROOT:-$ROOT}"
DATA_URL="${DOC_EVAL_DATA_URL:-$DEFAULT_DATA_URL}"
SHA_VALUE="${DOC_EVAL_DATA_SHA256:-}"
SHA_URL="${DOC_EVAL_DATA_SHA256_URL:-$DEFAULT_SHA_URL}"
WORK_DIR="${DOC_EVAL_DATA_WORK_DIR:-$(mktemp -d)}"
KEEP_WORK="${DOC_EVAL_DATA_KEEP_WORK:-0}"

cleanup() {
  if [[ "$KEEP_WORK" != "1" ]]; then
    rm -rf "$WORK_DIR"
  fi
}
trap cleanup EXIT

mkdir -p "$WORK_DIR" "$EXTRACT_ROOT"
ARCHIVE="$WORK_DIR/doc_eval_external_artifacts.tgz"
SHA_FILE="$WORK_DIR/doc_eval_external_artifacts.sha256"

echo "download_url=$DATA_URL"
echo "extract_root=$EXTRACT_ROOT"
echo "work_dir=$WORK_DIR"

curl -L "$DATA_URL" -o "$ARCHIVE"

if [[ -n "$SHA_VALUE" ]]; then
  echo "$SHA_VALUE  $ARCHIVE" > "$SHA_FILE"
else
  curl -L "$SHA_URL" -o "$SHA_FILE.raw"
  first_field="$(awk 'NF {print $1; exit}' "$SHA_FILE.raw")"
  if [[ "$first_field" =~ ^[0-9a-fA-F]{64}$ ]]; then
    echo "$first_field  $ARCHIVE" > "$SHA_FILE"
  else
    echo "Could not parse SHA256 from $SHA_URL" >&2
    cat "$SHA_FILE.raw" >&2
    exit 1
  fi
fi

sha256sum -c "$SHA_FILE"

echo "archive_size=$(du -h "$ARCHIVE" | awk '{print $1}')"
tar -tzf "$ARCHIVE" > "$WORK_DIR/archive_manifest.txt"
if awk 'BEGIN {bad=0} /^\// || /(^|\/)\.\.($|\/)/ {print; bad=1} END {exit bad}' "$WORK_DIR/archive_manifest.txt"; then
  :
else
  echo "Archive contains unsafe absolute or parent-relative paths." >&2
  exit 1
fi
tar -xzf "$ARCHIVE" -C "$EXTRACT_ROOT"

if [[ "$EXTRACT_ROOT" == "$ROOT" ]]; then
  make verify-data BOOTSTRAP_PYTHON="$BOOTSTRAP_PYTHON"
else
  "$BOOTSTRAP_PYTHON" "$ROOT/scripts/audit_data_dependencies.py" \
    --root "$EXTRACT_ROOT" \
    --report reports/data_setup_status.md \
    --json-report reports/data_setup_status.json
fi

echo "data_artifact_setup_complete=$EXTRACT_ROOT"
