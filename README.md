# Document VLM Take-Home Repo

This repository provides a CPU-first, reproducible evaluation scaffold for small vision-language models on document-understanding tasks. The first milestone uses a strict JSONL schema, tiny synthetic fixtures, a deterministic dummy adapter, and lightweight metrics so the full pipeline can run without GPU, large downloads, or model weights.

## Goals

- Evaluate small VLMs under 1B parameters.
- Focus on document-specific capabilities beyond generic VQA accuracy.
- Keep runs reproducible with benchmark hashing, run metadata, deterministic seeds, and explicit configs.
- Leave clean extension points for real VLMEvalKit-style datasets, Hugging Face adapters, and future LoRA/QLoRA experiments.

## Quickstart

```bash
python scripts/check_env.py
pytest -q
python scripts/build_benchmark_v0.py --out data/fixtures/docminibench_sample.jsonl
python scripts/eval_model.py --model dummy --benchmark data/fixtures/docminibench_sample.jsonl --out outputs/dummy_preds.jsonl
python scripts/aggregate_results.py --preds outputs/dummy_preds.jsonl --benchmark data/fixtures/docminibench_sample.jsonl --out reports/dummy_results.csv --markdown reports/dummy_results.md
python scripts/export_errors.py --preds outputs/dummy_preds.jsonl --benchmark data/fixtures/docminibench_sample.jsonl --out reports/dummy_errors.md
python scripts/analyze_next_steps.py --results reports/dummy_results.csv --out reports/next_steps_v0.md
```

## Real-model smoke runs

GPU smoke:

```bash
bash scripts/run_gpu_smoke.sh
```

Apple Silicon smoke:

```bash
bash scripts/run_mac_smoke.sh
```

Direct CLI form:

```bash
python scripts/eval_model.py \
  --model smolvlm_500m \
  --benchmark data/fixtures/docminibench_sample.jsonl \
  --limit 3 \
  --device cuda \
  --allow-real-models \
  --out outputs/smolvlm_smoke_preds.jsonl

python scripts/aggregate_results.py \
  --preds outputs/smolvlm_smoke_preds.jsonl \
  --benchmark data/fixtures/docminibench_sample.jsonl \
  --out reports/smolvlm_smoke_results.csv \
  --markdown reports/smolvlm_smoke_results.md
```

Common failure modes:

- `CUDA was requested but is not available on this machine.` The adapter fails closed and does not fall back to CPU. Use a CUDA runner such as Kaggle or Colab, or choose `--device cpu` for code-path debugging only.
- `MPS was requested but is not available on this machine.` Run the MPS smoke command on Apple Silicon with a recent PyTorch build that supports MPS.
- `Install requirements-gpu.txt and rerun with --allow-real-models.` The real adapter keeps heavy imports lazy and only loads them when the gate is enabled.
- If imports fail with errors similar to `numpy.typing ... NDArray`, your local `numpy`/`Pillow`/`transformers` stack is inconsistent. Create a fresh environment and reinstall `requirements-gpu.txt`.
- If fixture SVG loading is the blocker, the adapter renders the committed SVG fixtures through Pillow at runtime so the smoke path can reuse the existing benchmark.

## Repository layout

- [PROJECT_DOCVLM_TAKEHOME.md](/Users/htsu/Projects/doc_eval/PROJECT_DOCVLM_TAKEHOME.md)
- [configs/models.yaml](/Users/htsu/Projects/doc_eval/configs/models.yaml)
- [configs/benchmark_slices.yaml](/Users/htsu/Projects/doc_eval/configs/benchmark_slices.yaml)
- [src/adapters/base.py](/Users/htsu/Projects/doc_eval/src/adapters/base.py)
- [src/datasets/schema.py](/Users/htsu/Projects/doc_eval/src/datasets/schema.py)
- [scripts/eval_model.py](/Users/htsu/Projects/doc_eval/scripts/eval_model.py)

## Notes

- Real model adapters are lazy and gated so tests never try to import or load large dependencies.
- Fixture images are tiny SVG documents committed to the repo.
- `reports/next_steps_v0.md` ships as a template and is overwritten by `analyze_next_steps.py`.
- Suggested remote smoke targets if this machine lacks the right accelerator: Kaggle Notebook with a T4, Colab with a T4/L4, or Apple Silicon locally with `--device mps`.
