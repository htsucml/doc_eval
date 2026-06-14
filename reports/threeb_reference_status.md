# 3B Reference Status

Status: completed bounded reference runs.

Model: `Qwen/Qwen2.5-VL-3B-Instruct`  
Repo key: `qwen2_5_vl_3b_instruct`  
Purpose: `>1B reference ceiling`, not part of the sub-1B primary comparison.

## Environment

- GPU: NVIDIA GeForce RTX 4090, 24564 MiB
- Driver/CUDA from `nvidia-smi`: driver 565.57.01, CUDA 12.7
- Python: 3.11.10
- torch: 2.12.0+cu126
- transformers: 5.12.0
- accelerate: 1.14.0
- pillow: 12.2.0

## Commands

```bash
timeout 45m .venv/bin/python scripts/eval_model.py --model qwen2_5_vl_3b_instruct --benchmark data/notfound_controlled_v0.jsonl --out outputs/qwen2_5_vl_3b_instruct_notfound_controlled_v0_preds.jsonl --config configs/eval_not_found_strict.yaml --device cuda --allow-real-models
timeout 45m .venv/bin/python scripts/eval_model.py --model qwen2_5_vl_3b_instruct --benchmark data/docminibench_v0.jsonl --out outputs/qwen2_5_vl_3b_instruct_docminibench_v0_preds.jsonl --config configs/eval_not_found_strict.yaml --device cuda --allow-real-models
```

Logs:

- `logs/run_notfound_controlled_v0_qwen2_5_vl_3b_instruct_20260613T075850Z.log`
- `logs/run_docminibench_v0_qwen2_5_vl_3b_instruct_20260613T080134Z.log`

## Results

| dataset | rows | strict_exact_match | answer_in_output | not_found_false_answer_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: |
| `data/notfound_controlled_v0.jsonl` | 50 | 1.0000 | 1.0000 | 0.0000 | 0.4486 |
| `data/docminibench_v0.jsonl` | 120 | 0.8083 | 0.8167 | 0.0000 | 1.2059 |

Artifacts:

- `outputs/qwen2_5_vl_3b_instruct_notfound_controlled_v0_preds.jsonl`
- `outputs/qwen2_5_vl_3b_instruct_docminibench_v0_preds.jsonl`
- `reports/qwen2_5_vl_3b_instruct_notfound_controlled_v0_results.csv`
- `reports/qwen2_5_vl_3b_instruct_docminibench_v0_results.csv`
- `reports/qwen2_5_vl_3b_instruct_notfound_controlled_v0_errors.md`
- `reports/qwen2_5_vl_3b_instruct_docminibench_v0_errors.md`

No torch/CUDA packages were installed or replaced for this run.
