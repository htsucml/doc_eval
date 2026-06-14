"""LoRA/QLoRA training scaffold with dry-run and bounded real-training modes."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.datasets.jsonl_dataset import load_jsonl
from src.datasets.schema import validate_benchmark_row
from src.utils.image import load_image_for_vlm
from src.utils.io import write_json, write_text
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
    output_dir: str
    device: str
    learning_rate: float
    batch_size: int
    grad_accum_steps: int
    max_train_rows: int | None
    verify_reload: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--train", required=True)
    parser.add_argument("--val", required=True)
    parser.add_argument("--max_steps", type=int, default=100)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output-dir", default="outputs/lora_sft_poc_real")
    parser.add_argument("--device", choices=["cpu", "cuda", "mps"], default="cuda")
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--grad-accum-steps", type=int, default=1)
    parser.add_argument("--max-train-rows", type=int, default=None)
    parser.add_argument("--verify-reload", action="store_true")
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
    if args.batch_size != 1:
        raise ValueError("This bounded PoC currently supports --batch-size 1 only.")
    if args.grad_accum_steps <= 0:
        raise ValueError("--grad-accum-steps must be positive")
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
        output_dir=args.output_dir,
        device=args.device,
        learning_rate=args.learning_rate,
        batch_size=args.batch_size,
        grad_accum_steps=args.grad_accum_steps,
        max_train_rows=args.max_train_rows,
        verify_reload=args.verify_reload,
    )


def import_training_stack() -> None:
    __import__("transformers")
    __import__("peft")


def _auto_model_cls():
    try:
        from transformers import AutoModelForVision2Seq

        return AutoModelForVision2Seq
    except ImportError:
        from transformers import AutoModelForImageTextToText

        return AutoModelForImageTextToText


def _chat_prompt(processor, question: str, answer: str | None = None) -> str:
    instruction = (
        "Answer only with the final value. "
        "If the document does not contain enough evidence, answer exactly NOT_FOUND."
    )
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": f"{question}\n\n{instruction}"},
            ],
        }
    ]
    if answer is not None:
        messages.append({"role": "assistant", "content": [{"type": "text", "text": answer}]})
    kwargs = {"tokenize": False}
    if answer is None:
        kwargs["add_generation_prompt"] = True
    else:
        kwargs["add_generation_prompt"] = False
    try:
        return processor.apply_chat_template(messages, **kwargs)
    except TypeError:
        return processor.apply_chat_template(messages, add_generation_prompt=answer is None)


def _tensor_to_device(batch: dict, device: str) -> dict:
    return {key: value.to(device) if hasattr(value, "to") else value for key, value in batch.items()}


def _encode_training_example(processor, row: dict, device: str) -> dict:
    import torch

    answer = row["answers"][0]
    image = load_image_for_vlm(row["image_path"])
    prompt = _chat_prompt(processor, row["question"], answer=None)
    full_prompt = _chat_prompt(processor, row["question"], answer=answer)
    prompt_inputs = processor(text=prompt, images=[image], return_tensors="pt")
    full_inputs = processor(text=full_prompt, images=[image], return_tensors="pt")
    prompt_len = int(prompt_inputs["input_ids"].shape[1])
    labels = full_inputs["input_ids"].clone()
    labels[:, :prompt_len] = -100
    attention_mask = full_inputs.get("attention_mask")
    if attention_mask is not None:
        labels = labels.masked_fill(attention_mask == 0, -100)
    full_inputs["labels"] = labels
    return _tensor_to_device(full_inputs, device)


def _target_text_lora_modules(model) -> str:
    matches = []
    for name, _module in model.named_modules():
        if ".text_model." in name and (name.endswith(".q_proj") or name.endswith(".v_proj")):
            matches.append(name)
    if not matches:
        raise RuntimeError("Could not find text_model q_proj/v_proj modules for LoRA attachment.")
    return r"model\.text_model\.layers\.\d+\.self_attn\.(q_proj|v_proj)$"


def run_real_training(plan: FinetunePlan, train_path: str, val_path: str) -> dict:
    import torch
    from peft import LoraConfig, PeftModel, get_peft_model
    from transformers import AutoProcessor

    if plan.adapter != "smolvlm":
        raise RuntimeError(f"Real LoRA PoC only supports the smolvlm adapter, got {plan.adapter!r}.")
    if plan.device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested for real training but torch.cuda.is_available() is false.")

    model_cfg = load_model_config(plan.model_name)
    rows = load_split(train_path)
    if plan.max_train_rows is not None:
        rows = rows[: plan.max_train_rows]
    if not rows:
        raise RuntimeError("No training rows available.")

    dtype = torch.float32 if plan.device == "cpu" else torch.float16
    processor = AutoProcessor.from_pretrained(plan.hf_model_id)
    model = _auto_model_cls().from_pretrained(plan.hf_model_id, torch_dtype=dtype)
    model.config.use_cache = False
    for parameter in model.parameters():
        parameter.requires_grad_(False)

    target_modules = _target_text_lora_modules(model)
    lora_cfg = LoraConfig(
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        bias="none",
        target_modules=target_modules,
        exclude_modules=r"model\.vision_model\..*",
    )
    model = get_peft_model(model, lora_cfg)
    trainable_parameters = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_parameters = sum(p.numel() for p in model.parameters())
    model.to(plan.device)
    model.train()

    optimizer = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad), lr=plan.learning_rate)
    started = datetime.now(timezone.utc)
    losses: list[float] = []
    completed_steps = 0
    optimizer.zero_grad(set_to_none=True)
    row_index = 0
    while completed_steps < plan.max_steps:
        row = rows[row_index % len(rows)]
        row_index += 1
        batch = _encode_training_example(processor, row, plan.device)
        outputs = model(**batch)
        loss = outputs.loss / plan.grad_accum_steps
        loss.backward()
        losses.append(float(loss.detach().cpu()) * plan.grad_accum_steps)
        if row_index % plan.grad_accum_steps == 0:
            optimizer.step()
            optimizer.zero_grad(set_to_none=True)
            completed_steps += 1
            print(json.dumps({"step": completed_steps, "loss": round(losses[-1], 6)}), flush=True)

    output_root = Path(plan.output_dir)
    run_dir = output_root / f"{plan.model_name}_{started.strftime('%Y%m%dT%H%M%SZ')}"
    run_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(run_dir)
    processor.save_pretrained(run_dir / "processor")
    summary = {
        "status": "trained",
        "model_name": plan.model_name,
        "hf_model_id": plan.hf_model_id,
        "train_path": train_path,
        "val_path": val_path,
        "max_steps": plan.max_steps,
        "completed_steps": completed_steps,
        "learning_rate": plan.learning_rate,
        "batch_size": plan.batch_size,
        "grad_accum_steps": plan.grad_accum_steps,
        "device": plan.device,
        "dtype": str(dtype),
        "target_modules": target_modules,
        "trainable_parameters": trainable_parameters,
        "total_parameters": total_parameters,
        "loss_first": losses[0] if losses else None,
        "loss_last": losses[-1] if losses else None,
        "adapter_path": str(run_dir),
        "started_utc": started.isoformat(),
        "ended_utc": datetime.now(timezone.utc).isoformat(),
        "reload_verified": False,
    }
    write_json(run_dir / "training_summary.json", summary)

    if plan.verify_reload:
        del model
        if plan.device == "cuda":
            torch.cuda.empty_cache()
        base = _auto_model_cls().from_pretrained(plan.hf_model_id, torch_dtype=dtype)
        loaded = PeftModel.from_pretrained(base, run_dir)
        loaded.to(plan.device)
        loaded.eval()
        summary["reload_verified"] = True
        write_json(run_dir / "training_summary.json", summary)
        del loaded
        if plan.device == "cuda":
            torch.cuda.empty_cache()

    write_text(
        run_dir / "README.md",
        "\n".join(
            [
                "# LoRA SFT PoC Adapter",
                "",
                f"- Base model: `{plan.hf_model_id}`",
                f"- Completed steps: `{completed_steps}`",
                f"- Train data: `{train_path}`",
                f"- Validation data: `{val_path}`",
                f"- Reload verified: `{summary['reload_verified']}`",
                "",
            ]
        ),
    )
    return summary


def run(plan: FinetunePlan) -> None:
    print("finetune_plan=" + str(asdict(plan)))
    print("expected_kaggle_or_colab_command=" + REAL_TRAINING_COMMAND)
    if plan.dry_run:
        print("dry_run=true")
        print("status=validated_inputs_only")
        return

    import_training_stack()
    summary = run_real_training(plan, train_path=ARGS.train, val_path=ARGS.val)
    print("status=real_training_complete")
    print("training_summary=" + json.dumps(summary, sort_keys=True))


def main() -> None:
    try:
        global ARGS
        ARGS = parse_args()
        plan = build_plan(ARGS)
        run(plan)
    except Exception as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
