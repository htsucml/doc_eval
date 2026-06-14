"""Teacher-forced abstention likelihood diagnostics for VLM outputs.

This script scores candidate answer strings under a loaded VLM using the same
image+question prompt. The result is diagnostic only: higher likelihood for a
candidate does not prove the model's causal generation behavior.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.eval_model import prepare_sample, resolve_eval_config
from src.datasets.jsonl_dataset import load_jsonl
from src.datasets.schema import validate_benchmark_row
from src.utils.image import load_image_for_vlm
from src.utils.parsing import load_config_like_json


DEFAULT_CANDIDATES = [
    "NOT_FOUND",
    "not answerable from the document",
    "The requested information is not visible in the document.",
]


@dataclass
class ModelSpec:
    name: str
    peft_adapter_path: str | None = None


def parse_model_spec(raw: str) -> ModelSpec:
    if ":" not in raw:
        return ModelSpec(name=raw)
    name, adapter_path = raw.split(":", 1)
    return ModelSpec(name=name, peft_adapter_path=adapter_path)


def load_predictions(path: str | None) -> dict[str, str]:
    if not path or not Path(path).exists():
        return {}
    predictions = {}
    with Path(path).open("r", encoding="utf-8") as handle:
        for raw in handle:
            if not raw.strip():
                continue
            row = json.loads(raw)
            predictions[row["sample_id"]] = row.get("parsed_answer") or row.get("raw_output") or ""
    return predictions


def auto_model_cls(adapter: str):
    if adapter == "qwen25vl":
        from transformers import Qwen2_5_VLForConditionalGeneration

        return Qwen2_5_VLForConditionalGeneration
    try:
        from transformers import AutoModelForVision2Seq

        return AutoModelForVision2Seq
    except ImportError:
        from transformers import AutoModelForImageTextToText

        return AutoModelForImageTextToText


def load_model_and_processor(model_name: str, peft_adapter_path: str | None, device: str):
    import torch
    from transformers import AutoProcessor

    models = load_config_like_json("configs/models.yaml")["models"]
    cfg = models[model_name]
    dtype = torch.float32 if device == "cpu" else torch.float16
    processor = AutoProcessor.from_pretrained(cfg["hf_model_id"], trust_remote_code=True)
    model = auto_model_cls(cfg["adapter"]).from_pretrained(
        cfg["hf_model_id"],
        torch_dtype=dtype,
        trust_remote_code=True,
    )
    if peft_adapter_path:
        from peft import PeftModel

        model = PeftModel.from_pretrained(model, peft_adapter_path)
    model.to(device)
    model.eval()
    return cfg, processor, model


def build_prompt(processor, adapter: str, prompt_text: str, answer: str | None, image):
    if adapter == "qwen25vl":
        content = [{"type": "image", "image": image}, {"type": "text", "text": prompt_text}]
    else:
        content = [{"type": "image"}, {"type": "text", "text": prompt_text}]
    messages = [{"role": "user", "content": content}]
    if answer is not None:
        messages.append({"role": "assistant", "content": [{"type": "text", "text": answer}]})
    return processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=answer is None,
    )


def encode(processor, prompt: str, image, device: str):
    inputs = processor(text=prompt, images=[image], return_tensors="pt")
    return {key: value.to(device) if hasattr(value, "to") else value for key, value in inputs.items()}


def avg_answer_logprob(model, processor, adapter: str, sample: dict, candidate: str, device: str) -> tuple[float, int]:
    import torch

    image = load_image_for_vlm(sample["image_path"])
    prompt = build_prompt(processor, adapter, sample["prompt_text"], answer=None, image=image)
    full_prompt = build_prompt(processor, adapter, sample["prompt_text"], answer=candidate, image=image)
    prompt_inputs = encode(processor, prompt, image, device)
    full_inputs = encode(processor, full_prompt, image, device)
    prompt_len = int(prompt_inputs["input_ids"].shape[1])
    input_ids = full_inputs["input_ids"]
    with torch.no_grad():
        logits = model(**full_inputs).logits
    log_probs = torch.log_softmax(logits[:, :-1, :], dim=-1)
    labels = input_ids[:, 1:]
    start = max(prompt_len - 1, 0)
    token_log_probs = log_probs[:, start:, :].gather(-1, labels[:, start:].unsqueeze(-1)).squeeze(-1)
    token_count = int(token_log_probs.numel())
    if token_count == 0:
        return float("nan"), 0
    return float(token_log_probs.mean().detach().cpu()), token_count


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "model",
        "peft_adapter_path",
        "sample_id",
        "candidate_type",
        "candidate",
        "avg_logprob",
        "token_count",
        "rank_within_sample",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict], blockers: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    by_model: dict[str, list[dict]] = {}
    for row in rows:
        by_model.setdefault(row["model"], []).append(row)
    lines = [
        "# Abstention Likelihood Analysis",
        "",
        "Teacher-forced average log-likelihood was computed on the first controlled NOT_FOUND rows. This is diagnostic, not causal proof of generation behavior.",
        "",
        "| Model | Rows scored | NOT_FOUND top-1 count | Mean NOT_FOUND avg logprob | Mean greedy-prediction avg logprob |",
        "|---|---:|---:|---:|---:|",
    ]
    for model, model_rows in by_model.items():
        sample_ids = sorted({row["sample_id"] for row in model_rows})
        nf_rows = [row for row in model_rows if row["candidate_type"] == "canonical_not_found"]
        greedy_rows = [row for row in model_rows if row["candidate_type"] == "greedy_prediction"]
        nf_top = sum(1 for row in nf_rows if int(row["rank_within_sample"]) == 1)
        nf_mean = sum(float(row["avg_logprob"]) for row in nf_rows) / len(nf_rows) if nf_rows else float("nan")
        greedy_mean = (
            sum(float(row["avg_logprob"]) for row in greedy_rows) / len(greedy_rows) if greedy_rows else float("nan")
        )
        lines.append(f"| {model} | {len(sample_ids)} | {nf_top} | {nf_mean:.4f} | {greedy_mean:.4f} |")
    if blockers:
        lines.extend(["", "## Blockers"])
        lines.extend(f"- {item}" for item in blockers)
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "A model can assign reasonable likelihood to `NOT_FOUND` and still generate a false answer under greedy decoding. These scores should be used as calibration evidence, not as a replacement for generation metrics.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", default="data/notfound_controlled_v0.jsonl")
    parser.add_argument("--config", default="configs/eval_not_found_strict.yaml")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--device", choices=["cpu", "cuda", "mps"], default="cuda")
    parser.add_argument("--model", action="append", required=True, help="model name or model:peft_adapter_path")
    parser.add_argument("--predictions", action="append", default=[], help="model=path mapping for greedy candidate")
    parser.add_argument("--out-csv", default="reports/abstention_likelihood_analysis.csv")
    parser.add_argument("--out-md", default="reports/abstention_likelihood_analysis.md")
    args = parser.parse_args()

    pred_paths = dict(item.split("=", 1) for item in args.predictions)
    eval_cfg = resolve_eval_config(args.config)
    rows = load_jsonl(args.benchmark, validate_benchmark_row)[: args.limit]
    prepared = [
        prepare_sample(row, eval_cfg["prompt_mode"], answer_instruction=eval_cfg["answer_instruction"])
        for row in rows
    ]
    output_rows: list[dict] = []
    blockers: list[str] = []
    for spec in [parse_model_spec(item) for item in args.model]:
        predictions = load_predictions(pred_paths.get(spec.name))
        try:
            cfg, processor, model = load_model_and_processor(spec.name, spec.peft_adapter_path, args.device)
            candidates_by_sample = {}
            for sample in prepared:
                candidates = [
                    ("canonical_not_found", DEFAULT_CANDIDATES[0]),
                    ("short_abstention_phrase", DEFAULT_CANDIDATES[1]),
                    ("long_abstention_phrase", DEFAULT_CANDIDATES[2]),
                ]
                greedy = predictions.get(sample["id"], "").strip()
                if greedy:
                    candidates.append(("greedy_prediction", greedy))
                candidates_by_sample[sample["id"]] = candidates
                scored = []
                for candidate_type, candidate in candidates:
                    avg_logprob, token_count = avg_answer_logprob(
                        model, processor, cfg["adapter"], sample, candidate, args.device
                    )
                    scored.append((candidate_type, candidate, avg_logprob, token_count))
                ranked = sorted(scored, key=lambda item: item[2], reverse=True)
                ranks = {(item[0], item[1]): rank for rank, item in enumerate(ranked, start=1)}
                for candidate_type, candidate, avg_logprob, token_count in scored:
                    output_rows.append(
                        {
                            "model": spec.name if not spec.peft_adapter_path else f"{spec.name}+lora",
                            "peft_adapter_path": spec.peft_adapter_path or "",
                            "sample_id": sample["id"],
                            "candidate_type": candidate_type,
                            "candidate": candidate,
                            "avg_logprob": avg_logprob,
                            "token_count": token_count,
                            "rank_within_sample": ranks[(candidate_type, candidate)],
                        }
                    )
        except Exception as exc:
            blockers.append(f"{spec.name}: {type(exc).__name__}: {exc}")
        finally:
            try:
                del model
            except Exception:
                pass
            if args.device == "cuda":
                try:
                    import torch

                    torch.cuda.empty_cache()
                except Exception:
                    pass

    write_csv(Path(args.out_csv), output_rows)
    write_markdown(Path(args.out_md), output_rows, blockers)
    print(f"wrote_csv={args.out_csv}")
    print(f"wrote_markdown={args.out_md}")
    if blockers:
        print("blockers=" + json.dumps(blockers))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
