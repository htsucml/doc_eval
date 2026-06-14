# Reproducibility Checklist

This checklist is written for a fresh machine or fresh RunPod. It separates the
CPU-safe smoke path from GPU model reproduction.

## 1. Clone

```bash
git clone <repo-url> doc_eval
cd doc_eval
```

If using an archive instead of Git, unpack it and `cd` into the repository root.

## 2. Create Environment

CPU-only smoke:

```bash
make env
```

Alternatively, use the lightweight cloud bootstrap:

```bash
bash scripts/bootstrap_cloud_repro.sh
```

The bootstrap script runs tests and CPU smoke only. It does not run full
reproduction, real-model inference, or training.

GPU reproduction on RunPod or a CUDA host:

```bash
. .venv/bin/activate
pip install -r requirements-gpu.txt
```

Do not replace an already working torch/CUDA stack unless intentionally
rebuilding the image.

## 3. Configure Hugging Face Cache

Recommended RunPod cache location:

```bash
export HF_HOME=/workspace/hf_home
export HF_HUB_CACHE=/workspace/hf_home/hub
export HUGGINGFACE_HUB_CACHE=/workspace/hf_home/hub
export HF_DATASETS_CACHE=/workspace/hf_home/datasets
mkdir -p "$HF_HUB_CACHE" "$HF_DATASETS_CACHE"
```

Check storage:

```bash
df -h / /root /workspace
du -sh /workspace/hf_home 2>/dev/null || true
readlink -f /root/.cache/huggingface 2>/dev/null || true
```

The final packaged runs used `/workspace/hf_home`. Keep model caches off
small `/root` disks.

## 4. Run Tests

If the clone does not include external data/image artifacts, install them first:

```bash
make setup-data
make env
make verify-data
make check-full
```

The default setup target uses these direct-download artifact URLs:

```bash
export DOC_EVAL_DATA_URL='https://www.dropbox.com/scl/fi/tu1a5eo7itq55nrrslahv/doc_eval_external_artifacts_20260614_data_v1.tgz?rlkey=mmjplcdgxe40yo25r0uke9xfg&st=1gf9foi1&dl=1'
export DOC_EVAL_DATA_SHA256_URL='https://www.dropbox.com/scl/fi/gqhgo4sotzjk1u5muec5s/doc_eval_external_artifacts_20260614_data_v1.sha256?rlkey=ypmqr51094aqhphz3vyqrt4z8&st=4tgplkyu&dl=1'
make setup-data
```

You may instead set `DOC_EVAL_DATA_SHA256=<hex>` to verify against a literal
hash. The archive is expected to extract repo-root-relative paths such as
`data/...`, `outputs/...`, and `reports/...`; it must not contain `.venv`,
model weights, Hugging Face cache files, or local backups.

`make setup-data` and `make verify-data` can run before `.venv` exists. They use
`BOOTSTRAP_PYTHON ?= python3` because the data audit script uses only the
standard library.

```bash
make test
```

Expected result:

```text
31 passed
```

## 5. Run CPU Smoke

```bash
make smoke
```

Expected outputs:

- `outputs/smoke/dummy_preds_<timestamp>.jsonl`
- `reports/smoke/dummy_results_<timestamp>.csv`
- `reports/smoke/dummy_results_<timestamp>.md`

This path uses only the deterministic dummy adapter and should not download
large models.

## 6. Optional GPU Mini Reproduction

```bash
make reproduce-mini
```

Expected outputs:

- `outputs/reproduce_mini/smolvlm2_500m_video_controlled5_<timestamp>_preds.jsonl`
- `reports/reproduce_mini/smolvlm2_500m_video_controlled5_<timestamp>_results.csv`
- `reports/reproduce_mini/smolvlm2_500m_video_controlled5_<timestamp>_results.md`

Expected runtime:

- Warm cache: a few minutes.
- Cold cache: longer, depending on Hugging Face download speed.
- Default timeout: 20 minutes.

Hardware notes:

- Requires CUDA.
- SmolVLM2 500M is the default mini model.
- The default run is bounded to 5 controlled NOT_FOUND rows.
- This target does not train and does not run SmolVLM2 2.2B, Qwen2.5-VL 3B,
  or any other large reference model by default.
- Use `MINI_MODEL=smolvlm_500m make reproduce-mini` to switch to the older
  SmolVLM 500M model.

## 7. Aggregate Existing Full Outputs

```bash
make aggregate
```

Expected output directory:

- `reports/aggregate_rebuild_<timestamp>/`

This target does not rerun inference. It recomputes selected aggregate reports
from existing prediction JSONL files.

## 8. Optional Full Experimental Reproduction

This path is optional and is not required for quick validation. It can take
1-3 hours with a warm cache and longer with a cold cache.

Preflight only:

```bash
make check-full
```

Run the default full reproduction, which includes under-1B target models and
the SmolVLM2 500M LoRA PoC but excludes large reference models:

```bash
FULL_REF_MODELS=0 make full
make print-results
```

Optional reference-model reproduction:

```bash
FULL_REF_MODELS=1 make full
make print-results
```

Expected output roots:

- `outputs/full_repro/<timestamp>/`
- `reports/full_repro/<timestamp>/`
- `outputs/full_repro/latest`
- `reports/full_repro/latest`

Defaults:

- `FULL_TRAIN_STEPS=100`
- `FULL_REF_MODELS=0`
- `FULL_LIMIT=` empty means full benchmark/set evaluation
- `FULL_DEVICE=cuda`

Cache behavior:

- Respects `DOC_EVAL_CACHE_ROOT` if set.
- Else prefers `/workspace/hf_home` only when `/workspace` exists and is
  writable.
- Else uses `HF_HOME` or `$HOME/.cache/doc_eval_hf`.
- Exports `HF_HOME`, `HF_HUB_CACHE`, `HUGGINGFACE_HUB_CACHE`, and
  `HF_DATASETS_CACHE`.

The preflight reports the resolved cache path and free disk space. It does not
fail merely because the cache is under `/root`; it fails only if the selected
cache/output filesystem lacks enough free space for the requested mode.

`make check-full` can run after the lightweight `make env` step. If torch is not
installed yet, it uses `nvidia-smi` as a CUDA-host check and warns that
`make full` will install `requirements-gpu.txt` into this clone's `.venv`.

## 9. Build Paper

```bash
make paper
```

Expected sources and generated artifacts:

- `paper/main.tex`
- `paper/tables/headline_results.tex`
- `paper/tables/lora_poc.tex`
- `paper/figures/manual_transfer.tex`
- `paper/main.pdf` if `latexmk` or `pdflatex`/`bibtex` is installed.

For official ACL formatting, place the official `acl.sty` in `paper/` or in a
TeX search path. Without it, the source uses a minimal article fallback.

## 10. Historical Full Reproduction Notes

Full reproduction of all current real-model cells requires running the
commands recorded in the latest handoffs:

- `reports/codex_marathon_handoff.md`
- `reports/codex_addon_handoff.md`
- `reports/codex_abstention_margin_handoff.md`
- `reports/codex_2b_reference_completion_handoff.md`

Do not overwrite existing prediction outputs. Use explicit new filenames or
timestamped directories for any fresh run.

## 11. Validation Before Report Handoff

```bash
make test
git diff --check
make smoke
make paper
```

Record:

- command outputs,
- generated paths,
- hardware and GPU details,
- Hugging Face cache location,
- any failed or skipped model cells.
