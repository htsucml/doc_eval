# RunPod Runbook

This runbook is for a bounded overnight execution on a RunPod PyTorch template. RunPod Pods are already containerized; the Dockerfiles in `docker/` are for reproducibility or building a custom template later, not mandatory for the first run.

## 1. Clone

```bash
git clone <GITHUB_REPO_URL> doc_eval
cd doc_eval
git status --short
```

## 2. Create Environment

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-gpu.txt
```

Or run the setup wrapper:

```bash
bash scripts/setup_runpod_env.sh
```

## 3. Hardware And Environment Checks

```bash
nvidia-smi
python scripts/check_env.py
pytest -q
```

Record the command output in `logs/`. If CUDA is unavailable or GPU dependencies are not installed, do not run real model inference.

## 4. SmolVLM Fixture Smoke

This is the first real-model gate. It loads SmolVLM only because the command explicitly passes `--allow-real-models`.

```bash
bash scripts/run_cuda_smoke.sh
```

Expected outputs:

- `outputs/smolvlm_500m_smoke_preds.jsonl`
- `reports/smolvlm_500m_smoke_results.csv`
- `reports/smolvlm_500m_smoke_results.md`

## 5. Build `docminibench_v0`

```bash
python scripts/build_benchmark_v0.py --out data/fixtures/docminibench_sample.jsonl
```

This default build is fixture mode and should not download datasets.

## 6. Zero-Shot Evaluation

Run one selected model on the benchmark:

```bash
bash scripts/run_docminibench_v0.sh smolvlm_500m
```

The wrapper builds the fixture benchmark if missing, runs CUDA inference with `--allow-real-models`, aggregates metrics, and exports errors.

For the bounded overnight plan:

```bash
bash scripts/run_overnight_marathon.sh
```

The marathon stages are:

1. env/test
2. SmolVLM 500M smoke
3. build dataset v0
4. SmolVLM 500M full v0
5. try one fallback from SmolVLM2 500M, LLaVA-OneVision Qwen2 0.5B, InternVL2.5 1B
6. aggregate comparison and errors
7. OCR-assisted ablation or LoRA smoke only if zero-shot outputs exist
8. write `reports/overnight_handoff.md`

## 7. Aggregate, Export, Analyze

Manual command pattern:

```bash
python scripts/aggregate_results.py \
  --preds outputs/smolvlm_500m_docminibench_v0_preds.jsonl \
  --benchmark data/fixtures/docminibench_sample.jsonl \
  --out reports/smolvlm_500m_docminibench_v0_results.csv \
  --markdown reports/smolvlm_500m_docminibench_v0_results.md

python scripts/export_errors.py \
  --preds outputs/smolvlm_500m_docminibench_v0_preds.jsonl \
  --benchmark data/fixtures/docminibench_sample.jsonl \
  --out reports/smolvlm_500m_docminibench_v0_errors.md

python scripts/analyze_next_steps.py \
  --results reports/smolvlm_500m_docminibench_v0_results.csv \
  --errors reports/smolvlm_500m_docminibench_v0_errors.md \
  --out reports/smolvlm_500m_docminibench_v0_next_steps.md
```

## 8. Download Artifacts

Download only source-controlled files plus the run artifacts you need for the report:

```bash
tar -czf runpod_artifacts.tgz logs reports outputs
```

Copy `runpod_artifacts.tgz` off the pod through the RunPod file browser, `scp`, or your preferred remote sync. Do not commit `logs/`, `outputs/`, caches, model weights, or downloaded datasets.

## 9. Stop Pod

After artifacts are copied:

```bash
git status --short
```

Then stop or terminate the RunPod pod from the RunPod console to avoid continued billing.
