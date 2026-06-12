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

