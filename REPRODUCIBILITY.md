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
python -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

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

## 8. Build Paper

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

## 9. Full Reproduction Notes

Full reproduction of all current real-model cells requires running the
commands recorded in the latest handoffs:

- `reports/codex_marathon_handoff.md`
- `reports/codex_addon_handoff.md`
- `reports/codex_abstention_margin_handoff.md`
- `reports/codex_2b_reference_completion_handoff.md`

Do not overwrite existing prediction outputs. Use explicit new filenames or
timestamped directories for any fresh run.

## 10. Validation Before Report Handoff

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
