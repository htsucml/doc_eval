"""CPU-safe LoRA/QLoRA training scaffold with dry-run validation."""

from __future__ import annotations

import argparse
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.datasets.jsonl_dataset import load_jsonl
from src.datasets.schema import validate_benchmark_row
from src.utils.parsing import load_config_like_json


REAL_TRAINING_COMMAND = (
    "python scripts/finetune_lora.py --model smolvlm_500m "
    "--train /kaggle/working/train.jsonl --val /kaggle/working/val.jsonl "
    "--max_steps 200"
)


@dataclass
class FinetunePlan:
    dry_run: bool
    model_name: str
    hf_model_id: str
    train_rows: int
    val_rows: int
    max_steps: int
    adapter: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--train", required=True)
    parser.add_argument("--val", required=True)
    parser.add_argument("--max_steps", type=int, default=100)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def load_model_config(model_name: str) -> dict:
    models = load_config_like_json("configs/models.yaml")["models"]
    if model_name not in models:
        available = ", ".join(sorted(models))
        raise ValueError(f"Unknown model '{model_name}'. Available models: {available}")
    model_cfg = models[model_name]
    if "hf_model_id" not in model_cfg:
        raise ValueError(f"Model '{model_name}' does not have a Hugging Face model id for LoRA fine-tuning.")
    return model_cfg


def load_split(path: str) -> list[dict]:
    return load_jsonl(path, validator=validate_benchmark_row)


def build_plan(args: argparse.Namespace) -> FinetunePlan:
    if args.max_steps <= 0:
        raise ValueError("--max_steps must be positive")
    model_cfg = load_model_config(args.model)
    train_rows = load_split(args.train)
    val_rows = load_split(args.val)
    return FinetunePlan(
        dry_run=args.dry_run,
        model_name=args.model,
        hf_model_id=model_cfg["hf_model_id"],
        train_rows=len(train_rows),
        val_rows=len(val_rows),
        max_steps=args.max_steps,
        adapter=model_cfg["adapter"],
    )


def import_training_stack() -> None:
    __import__("transformers")
    __import__("peft")


def run(plan: FinetunePlan) -> None:
    print("finetune_plan=" + str(asdict(plan)))
    print("expected_kaggle_or_colab_command=" + REAL_TRAINING_COMMAND)
    if plan.dry_run:
        print("dry_run=true")
        print("status=validated_inputs_only")
        return

    import_training_stack()
    print("status=dependency_stack_validated")
    print("note=Training loop intentionally stops before model loading to avoid accidental downloads in this repo.")


def main() -> None:
    try:
        plan = build_plan(parse_args())
        run(plan)
    except Exception as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
