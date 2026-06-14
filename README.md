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
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
make test
make smoke
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

Run a small GPU mini reproduction if CUDA and model weights are available:

```bash
make reproduce-mini
```

Expected mini artifacts are timestamped:

- `outputs/reproduce_mini/smolvlm2_500m_video_controlled5_<timestamp>_preds.jsonl`
- `reports/reproduce_mini/smolvlm2_500m_video_controlled5_<timestamp>_results.csv`

Runtime depends on model cache state. On a warmed GPU cache, the mini run should
finish in a few minutes; first-time model downloads can take longer and require
several GB of workspace storage.

Regenerate selected aggregate checks from existing predictions:

```bash
make aggregate
```

This writes timestamped files under `reports/aggregate_rebuild_<timestamp>/`.

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

- CPU is sufficient for `make test` and `make smoke`.
- `make reproduce-mini` and full real-model reproduction require CUDA.
- The validated cache route is `/workspace/hf_home`; keep Hugging Face caches
  off `/root` on small RunPod root disks.
- SmolVLM2 500M fits on modest CUDA devices. SmolVLM2 2.2B and Qwen2.5-VL 3B
  require more VRAM and should be treated as reference-only runs.

## Troubleshooting

- `CUDA is required for make reproduce-mini`: run on a CUDA machine or use only
  `make smoke`.
- `Model ... is gated`: real models require `--allow-real-models`; tests and
  smoke intentionally avoid this path.
- Hugging Face downloads fill `/root`: export `HF_HOME=/workspace/hf_home` and
  related cache variables before running model commands.
- Missing LaTeX style: place the official ACL `acl.sty` in `paper/` for ACL
  formatting, or let `paper/main.tex` use its minimal article fallback.
- Existing prediction files should not be overwritten during packaging. Use
  timestamped output directories for new smoke or mini runs.

See `REPRODUCIBILITY.md` for a clean-room command checklist.
