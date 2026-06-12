from __future__ import annotations

import subprocess
import sys


def test_finetune_lora_dry_run_cli() -> None:
    command = [
        sys.executable,
        "scripts/finetune_lora.py",
        "--model",
        "smolvlm_500m",
        "--train",
        "data/fixtures/docminibench_sample.jsonl",
        "--val",
        "data/fixtures/docminibench_sample.jsonl",
        "--max_steps",
        "1",
        "--dry-run",
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    assert "dry_run=true" in completed.stdout
    assert "expected_kaggle_or_colab_command=" in completed.stdout
