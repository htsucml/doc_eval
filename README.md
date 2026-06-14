# Document VLM Evaluation Handoff

This repository packages a reproducible document-VLM evaluation for compact
vision-language models, with special attention to NOT_FOUND / abstention
behavior. It includes a CPU-safe smoke path, GPU mini-reproduction commands,
aggregation utilities, final result artifacts, and an ACL-style technical report
source under `paper/`.

## What Is Evaluated

Primary target models:

- `smolvlm_500m`
- `smolvlm2_500m_video`
- `smolvlm2_500m_video` with bounded LoRA/SFT proof-of-concept adapters

Reference-only models:

- `smolvlm2_2_2b`: same-family `>1B` reference
- `qwen2_5_vl_3b_instruct`: external `>1B` reference ceiling

Benchmarks and auxiliary sets:

- `data/docminibench_v0.jsonl`: 120-row document QA benchmark.
- `data/notfound_controlled_v0.jsonl`: mechanically auditable controlled
  synthetic NOT_FOUND benchmark.
- `data/docvqa_manual_notfound_combined_expanded_v0_eval.jsonl`: manual
  real-document NOT_FOUND transfer set.
- `data/notfound_ood_sanity_v0_eval_strict.jsonl`: non-document OOD sanity
  set, not a document benchmark.

The original DocMiniBench-v0 NOT_FOUND slice is retained only as
exploratory/demoted because absence was not mechanically proven.

## Setup

CPU-only smoke and tests:

```bash
make env
make test
make smoke
```

On a fresh cloud VM, the lightweight bootstrap wrapper performs the same
CPU-safe setup/test/smoke path and does not download real models:

```bash
bash scripts/bootstrap_cloud_repro.sh
```

GPU evaluation environment, using the already validated torch/CUDA stack:

```bash
. .venv/bin/activate
pip install -r requirements-gpu.txt
export HF_HOME=/workspace/hf_home
export HF_HUB_CACHE=/workspace/hf_home/hub
export HUGGINGFACE_HUB_CACHE=/workspace/hf_home/hub
export HF_DATASETS_CACHE=/workspace/hf_home/datasets
```

Do not install or replace torch/CUDA on an already configured RunPod unless you
are intentionally rebuilding the environment.

## Quickstart

Set up external data artifacts, if starting from a clean clone without bundled
data/images. This is the CPU/data reproducibility path and does not require
CUDA or real model downloads:

```bash
make setup-data
make env
make verify-data
make smoke
```

`make setup-data` downloads the documented artifact with `curl -L`, verifies
SHA256, extracts repo-root-relative paths, and then runs `make verify-data`.
It can run before `.venv` exists because verification uses
`BOOTSTRAP_PYTHON ?= python3` and only the Python standard library.
The default artifact URLs are:

```bash
export DOC_EVAL_DATA_URL='https://www.dropbox.com/scl/fi/tu1a5eo7itq55nrrslahv/doc_eval_external_artifacts_20260614_data_v1.tgz?rlkey=mmjplcdgxe40yo25r0uke9xfg&st=1gf9foi1&dl=1'
export DOC_EVAL_DATA_SHA256_URL='https://www.dropbox.com/scl/fi/gqhgo4sotzjk1u5muec5s/doc_eval_external_artifacts_20260614_data_v1.sha256?rlkey=ypmqr51094aqhphz3vyqrt4z8&st=4tgplkyu&dl=1'
```

Override `DOC_EVAL_DATA_SHA256` with a literal hash if you do not want to fetch
the `.sha256` URL.

Run all unit tests:

```bash
make test
```

Run a CPU-only deterministic smoke pipeline:

```bash
make smoke
```

Expected smoke artifacts are timestamped:

- `outputs/smoke/dummy_preds_<timestamp>.jsonl`
- `reports/smoke/dummy_results_<timestamp>.csv`
- `reports/smoke/dummy_results_<timestamp>.md`

Optionally run a small bounded GPU mini reproduction if CUDA and model weights
are available:

```bash
make reproduce-mini
```

Expected mini artifacts are timestamped:

- `outputs/reproduce_mini/smolvlm2_500m_video_controlled5_<timestamp>_preds.jsonl`
- `reports/reproduce_mini/smolvlm2_500m_video_controlled5_<timestamp>_results.csv`

Runtime depends on model cache state. On a warmed GPU cache, the mini run should
finish in a few minutes; first-time model downloads can take longer and require
several GB of workspace storage.

By default, `make reproduce-mini` evaluates only 5 controlled NOT_FOUND rows
with `smolvlm2_500m_video`, applies a 20-minute timeout, does not train, and
does not run `>1B` reference models. Override only when intentionally running a
different bounded subset, for example `MINI_MODEL=smolvlm_500m MINI_LIMIT=5
make reproduce-mini`.

Regenerate selected aggregate checks from existing predictions:

```bash
make aggregate
```

This writes timestamped files under `reports/aggregate_rebuild_<timestamp>/`.

## Optional Full Reproduction

The full reproduction path is opt-in and is not part of quick smoke validation.
It reruns headline experiments into fresh timestamped directories:

- `outputs/full_repro/<timestamp>/`
- `reports/full_repro/<timestamp>/`

It also updates convenience symlinks:

- `outputs/full_repro/latest`
- `reports/full_repro/latest`

Recommended clean-clone usage on a CUDA machine with a CUDA-enabled torch/model
environment active in this clone:

```bash
export DOC_EVAL_CACHE_ROOT=/workspace/hf_home  # recommended on cloud runners when available
make env
make check-full
FULL_REF_MODELS=0 make full
make print-results
```

Reference-only reproduction is disabled by default. To include SmolVLM2 2.2B
and Qwen2.5-VL 3B:

```bash
FULL_REF_MODELS=1 make full
```

Defaults:

- `FULL_TRAIN_STEPS=100`
- `FULL_REF_MODELS=0`
- `FULL_LIMIT=` means full benchmark/set evaluation
- `FULL_DEVICE=cuda`

`make full` runs tests, CPU smoke, zero-shot under-1B target evaluations, a
SmolVLM2 500M LoRA PoC, adapted-model evaluation, bounded abstention-margin
diagnostics, and compact result printing. It does not overwrite frozen
historical `outputs/*.jsonl` or `reports/*.md`; all new files go under the
timestamped full-reproduction directories.

`make check-full` validates the active `.venv` for the requested full
reproduction mode. With the default `FULL_DEVICE=cuda`, it fails unless that
environment can import torch and `torch.cuda.is_available()` is true. `make full`
depends on `gpu-env`, but platform-specific CUDA torch wheels may still need to
be installed or selected explicitly for a clean machine before full reproduction.
`make print-results` only reports completed full-reproduction runs and skips
failed or incomplete timestamp directories.

Expected runtime is roughly 1-3 hours with warm model cache and longer with a
cold cache. Disk needs depend on whether reference models are enabled. Sharing a
Hugging Face cache is encouraged, but not required. If `DOC_EVAL_CACHE_ROOT` is
unset, the scripts prefer `/workspace/hf_home` when `/workspace` exists and is
writable; otherwise they use `HF_HOME` or a normal user-cache path.

Build the paper tables and PDF if LaTeX is installed:

```bash
make paper
```

If no LaTeX toolchain is available, the command still regenerates paper table
inputs and prints the build instructions.

## Final Result Artifacts

Main report tables:

- `reports/final_results_tables.md`
- `reports/notfound_comparison_v0.md`
- `reports/lora_sft_poc_results.md`
- `reports/smolvlm2_2b_status.md`
- `reports/abstention_margin_analysis.md`

Latest handoffs:

- `reports/codex_abstention_margin_handoff.md`
- `reports/codex_2b_reference_completion_handoff.md`

Paper source:

- `paper/main.tex`
- `paper/sections/*.tex`
- `paper/tables/*.tex`
- `paper/figures/*.tex`
- `paper/references.bib`

## Hardware Notes

- CPU is sufficient for `make setup-data`, `make verify-data`, `make test`, and
  `make smoke`.
- `make reproduce-mini` is optional and requires CUDA. Full real-model
  reproduction requires a CUDA-enabled torch/model environment, more GPU time,
  and more storage.
- `/workspace/hf_home` is the recommended cloud cache default when available;
  local machines can use a normal user cache. Full preflight fails only when the
  selected cache filesystem lacks enough free space.
- SmolVLM2 500M fits on modest CUDA devices. SmolVLM2 2.2B and Qwen2.5-VL 3B
  require more VRAM and should be treated as reference-only runs.

## Troubleshooting

- `CUDA is required for make reproduce-mini`: run on a CUDA machine or use only
  `make smoke`.
- `make check-full` reports `torch.cuda.is_available() is false`: the active
  `.venv` is not a CUDA-capable full-reproduction environment. Install the
  CUDA torch wheel appropriate for the host or activate the validated GPU env,
  then rerun `make check-full`.
- `Model ... is gated`: real models require `--allow-real-models`; tests and
  smoke intentionally avoid this path.
- Hugging Face downloads fill `/root`: export `HF_HOME=/workspace/hf_home` and
  related cache variables before running model commands.
- Missing LaTeX style: place the official ACL `acl.sty` in `paper/` for ACL
  formatting, or let `paper/main.tex` use its minimal article fallback.
- Existing prediction files should not be overwritten during packaging. Use
  timestamped output directories for new smoke or mini runs.

See `REPRODUCIBILITY.md` for a clean-room command checklist.
