"""Abstention-margin diagnostics for NOT_FOUND calibration.

This script computes teacher-forced average token log-likelihood margins between
abstention candidates and an answer candidate. It is diagnostic calibration
evidence, not a replacement for free-generation metrics.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.eval_model import prepare_sample, resolve_eval_config
from src.datasets.jsonl_dataset import load_jsonl
from src.datasets.schema import validate_benchmark_row
from src.utils.image import load_image_for_vlm
from src.utils.parsing import load_config_like_json


STRICT_CONFIG = "configs/eval_not_found_strict.yaml"
ABSTENTIONS = [
    "NOT_FOUND",
    "not answerable from the document",
    "The requested information is not visible in the document.",
]


@dataclass
class ModelRun:
    label: str
    model_name: str
    adapter_path: str | None
    predictions: dict[str, str]


def read_predictions(path: str) -> dict[str, str]:
    predictions = {}
    if not Path(path).exists():
        return predictions
    with Path(path).open("r", encoding="utf-8") as handle:
        for raw in handle:
            if raw.strip():
                row = json.loads(raw)
                predictions[row["sample_id"]] = (row.get("parsed_answer") or row.get("raw_output") or "").strip()
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


def load_model(model_name: str, adapter_path: str | None, device: str):
    import torch
    from transformers import AutoProcessor

    cfg = load_config_like_json("configs/models.yaml")["models"][model_name]
    dtype = torch.float32 if device == "cpu" else torch.float16
    processor = AutoProcessor.from_pretrained(cfg["hf_model_id"], trust_remote_code=True, local_files_only=True)
    model = auto_model_cls(cfg["adapter"]).from_pretrained(
        cfg["hf_model_id"],
        torch_dtype=dtype,
        trust_remote_code=True,
        local_files_only=True,
    )
    if adapter_path:
        from peft import PeftModel

        model = PeftModel.from_pretrained(model, adapter_path, local_files_only=True)
    model.to(device)
    model.eval()
    return cfg, processor, model


def build_prompt(processor, adapter: str, prompt_text: str, answer: str | None, image):
    content = [{"type": "image", "image": image}, {"type": "text", "text": prompt_text}] if adapter == "qwen25vl" else [
        {"type": "image"},
        {"type": "text", "text": prompt_text},
    ]
    messages = [{"role": "user", "content": content}]
    if answer is not None:
        messages.append({"role": "assistant", "content": [{"type": "text", "text": answer}]})
    return processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=answer is None)


def encode(processor, text: str, image, device: str) -> dict:
    batch = processor(text=text, images=[image], return_tensors="pt")
    return {key: value.to(device) if hasattr(value, "to") else value for key, value in batch.items()}


def avg_logprob(model, processor, adapter: str, sample: dict, answer: str, device: str) -> tuple[float, int]:
    import torch

    image = load_image_for_vlm(sample["image_path"])
    prompt = build_prompt(processor, adapter, sample["prompt_text"], None, image)
    full_prompt = build_prompt(processor, adapter, sample["prompt_text"], answer, image)
    prompt_inputs = encode(processor, prompt, image, device)
    full_inputs = encode(processor, full_prompt, image, device)
    prompt_len = int(prompt_inputs["input_ids"].shape[1])
    labels = full_inputs["input_ids"]
    with torch.no_grad():
        logits = model(**full_inputs).logits
    log_probs = torch.log_softmax(logits[:, :-1, :], dim=-1)
    next_labels = labels[:, 1:]
    start = max(prompt_len - 1, 0)
    token_log_probs = log_probs[:, start:, :].gather(-1, next_labels[:, start:].unsqueeze(-1)).squeeze(-1)
    if token_log_probs.numel() == 0:
        return float("nan"), 0
    return float(token_log_probs.mean().detach().cpu()), int(token_log_probs.numel())


def load_prepared_rows(config_path: str, controlled_limit: int, manual_limit: int, answerable_limit: int, ood_limit: int) -> list[dict]:
    cfg = resolve_eval_config(config_path)
    datasets = [
        ("controlled_not_found", "data/notfound_controlled_v0.jsonl", controlled_limit),
        ("manual_real_doc_not_found", "data/docvqa_manual_notfound_combined_expanded_v0_eval.jsonl", manual_limit),
        ("ood_sanity_not_found", "data/notfound_ood_sanity_v0.jsonl", ood_limit),
    ]
    rows: list[dict] = []
    for dataset_name, path, limit in datasets:
        loaded = load_jsonl(path, validate_benchmark_row)
        if limit:
            loaded = loaded[:limit]
        for row in loaded:
            p = prepare_sample(row, cfg["prompt_mode"], cfg["answer_instruction"])
            p["margin_dataset"] = dataset_name
            rows.append(p)
    answerable = [r for r in load_jsonl("data/docminibench_v0.jsonl", validate_benchmark_row) if r["capability"] != "not_found"]
    for row in answerable[:answerable_limit]:
        p = prepare_sample(row, cfg["prompt_mode"], cfg["answer_instruction"])
        p["margin_dataset"] = "docminibench_answerable"
        rows.append(p)
    return rows


def answer_candidates(sample: dict, predictions: dict[str, str]) -> list[str]:
    if sample["margin_dataset"] == "docminibench_answerable":
        return [a for a in sample.get("answers", []) if a]
    greedy = predictions.get(sample["id"], "")
    return [greedy] if greedy else [""]


def score_model(run: ModelRun, samples: list[dict], device: str) -> list[dict]:
    cfg, processor, model = load_model(run.model_name, run.adapter_path, device)
    rows = []
    for sample in samples:
        nf_logp, nf_tokens = avg_logprob(model, processor, cfg["adapter"], sample, "NOT_FOUND", device)
        alt_scores = [avg_logprob(model, processor, cfg["adapter"], sample, alt, device) for alt in ABSTENTIONS[1:]]
        best_alt_logp, best_alt_tokens = max(alt_scores, key=lambda item: item[0])
        candidates = answer_candidates(sample, run.predictions)
        answer_scores = [avg_logprob(model, processor, cfg["adapter"], sample, c, device) for c in candidates]
        answer_logp, answer_tokens = max(answer_scores, key=lambda item: item[0])
        answer_candidate = candidates[answer_scores.index((answer_logp, answer_tokens))]
        ranked = sorted([("NOT_FOUND", nf_logp), ("alt_abstain", best_alt_logp), ("answer", answer_logp)], key=lambda x: x[1], reverse=True)
        generation = run.predictions.get(sample["id"], "")
        exact_nf = generation == "NOT_FOUND"
        is_not_found = sample["margin_dataset"] != "docminibench_answerable"
        rows.append(
            {
                "model": run.label,
                "model_name": run.model_name,
                "checkpoint": run.adapter_path or "base",
                "dataset": sample["margin_dataset"],
                "sample_id": sample["id"],
                "capability": sample["capability"],
                "logp_not_found_avg": nf_logp,
                "logp_alt_abstain_best_avg": best_alt_logp,
                "logp_answer_candidate_avg": answer_logp,
                "abstention_margin": nf_logp - answer_logp,
                "best_abstention_margin": max(nf_logp, best_alt_logp) - answer_logp,
                "not_found_candidate_rank": next(i for i, item in enumerate(ranked, start=1) if item[0] == "NOT_FOUND"),
                "not_found_token_count": nf_tokens,
                "alt_abstain_token_count": best_alt_tokens,
                "answer_candidate_token_count": answer_tokens,
                "answer_candidate": answer_candidate,
                "generation": generation,
                "generation_exact_not_found": exact_nf,
                "generation_false_answer": bool(is_not_found and not exact_nf),
                "gold_answers": "|".join(sample.get("answers", [])),
            }
        )
    return rows


def auroc(labels: list[int], scores: list[float]) -> float:
    pairs = sorted(zip(scores, labels), key=lambda x: x[0])
    pos = sum(labels)
    neg = len(labels) - pos
    if pos == 0 or neg == 0:
        return float("nan")
    rank_sum = 0.0
    i = 0
    while i < len(pairs):
        j = i
        while j + 1 < len(pairs) and pairs[j + 1][0] == pairs[i][0]:
            j += 1
        avg_rank = (i + 1 + j + 1) / 2
        for k in range(i, j + 1):
            if pairs[k][1] == 1:
                rank_sum += avg_rank
        i = j + 1
    return (rank_sum - pos * (pos + 1) / 2) / (pos * neg)


def aggregate(rows: list[dict]) -> tuple[list[str], dict]:
    lines = [
        "# Abstention Margin Analysis",
        "",
        "Teacher-forced likelihood margins are diagnostic calibration evidence. Free-generation metrics remain primary.",
        "",
        "## Likelihood Separation",
        "",
        "| Model | Dataset | Rows | Mean logp NOT_FOUND | Mean logp answer | Mean margin | Median margin | NOT_FOUND top-1 | Generation NOT_FOUND rate | Generation false-answer rate |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    summary = {}
    for model in sorted({r["model"] for r in rows}):
        summary[model] = {}
        for dataset in sorted({r["dataset"] for r in rows if r["model"] == model}):
            subset = [r for r in rows if r["model"] == model and r["dataset"] == dataset]
            margins = [float(r["abstention_margin"]) for r in subset]
            gen_nf = sum(1 for r in subset if r["generation_exact_not_found"]) / len(subset)
            false_rate = sum(1 for r in subset if r["generation_false_answer"]) / len(subset)
            top1 = sum(1 for r in subset if int(r["not_found_candidate_rank"]) == 1)
            rec = {
                "rows": len(subset),
                "mean_logp_not_found": statistics.mean(float(r["logp_not_found_avg"]) for r in subset),
                "mean_logp_answer": statistics.mean(float(r["logp_answer_candidate_avg"]) for r in subset),
                "mean_margin": statistics.mean(margins),
                "median_margin": statistics.median(margins),
                "not_found_top1": top1,
                "generation_not_found_rate": gen_nf,
                "generation_false_answer_rate": false_rate,
            }
            summary[model][dataset] = rec
            lines.append(
                f"| {model} | {dataset} | {rec['rows']} | {rec['mean_logp_not_found']:.4f} | {rec['mean_logp_answer']:.4f} | {rec['mean_margin']:.4f} | {rec['median_margin']:.4f} | {top1} | {gen_nf:.4f} | {false_rate:.4f} |"
            )
    lines += [
        "",
        "## Separability And Gate Simulation",
        "",
        "This gate simulation is computed only on the bounded rows scored in this run. It is not a replacement for full generation metrics.",
        "",
        "| Model | AUROC margin | AUROC best margin | Threshold | Threshold accuracy | Answerable FPR | NOT_FOUND FNR | Gate answerable-subset exact | Gate answerable-subset over-abstention | Gate controlled false-answer | Gate manual false-answer | Gate OOD false-answer |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for model in sorted(summary):
        subset = [r for r in rows if r["model"] == model and r["dataset"] in {"controlled_not_found", "manual_real_doc_not_found", "ood_sanity_not_found", "docminibench_answerable"}]
        labels = [0 if r["dataset"] == "docminibench_answerable" else 1 for r in subset]
        margin_scores = [float(r["abstention_margin"]) for r in subset]
        best_scores = [float(r["best_abstention_margin"]) for r in subset]
        preds = [s > 0 for s in margin_scores]
        acc = sum(int(p) == y for p, y in zip(preds, labels)) / len(labels)
        answerable = [p for p, y in zip(preds, labels) if y == 0]
        notfound = [p for p, y in zip(preds, labels) if y == 1]
        fpr = sum(answerable) / len(answerable)
        fnr = sum(not p for p in notfound) / len(notfound)
        def gate_false(dataset: str) -> float:
            s = [r for r in rows if r["model"] == model and r["dataset"] == dataset]
            return sum(1 for r in s if not (float(r["abstention_margin"]) > 0 or r["generation_exact_not_found"])) / len(s)
        doc = [r for r in rows if r["model"] == model and r["dataset"] == "docminibench_answerable"]
        gate_answer_exact = sum(
            1
            for r in doc
            if not (float(r["abstention_margin"]) > 0 or r["generation_exact_not_found"])
            and r["generation"] in r["gold_answers"].split("|")
        ) / len(doc)
        gate_answer_over_abstain = sum(
            1 for r in doc if float(r["abstention_margin"]) > 0 or r["generation_exact_not_found"]
        ) / len(doc)
        lines.append(
            f"| {model} | {auroc(labels, margin_scores):.4f} | {auroc(labels, best_scores):.4f} | 0 | {acc:.4f} | {fpr:.4f} | {fnr:.4f} | {gate_answer_exact:.4f} | {gate_answer_over_abstain:.4f} | {gate_false('controlled_not_found'):.4f} | {gate_false('manual_real_doc_not_found'):.4f} | {gate_false('ood_sanity_not_found'):.4f} |"
        )
    lines += ["", "## Failure Taxonomy", ""]
    examples = []
    for r in rows:
        margin = float(r["abstention_margin"])
        if r["generation_false_answer"] and margin > 0:
            label = "false generated answer but high NOT_FOUND margin: reranking/gating opportunity"
        elif r["generation_false_answer"] and margin <= 0:
            label = "false generated answer and low NOT_FOUND margin: needs training/data"
        elif r["dataset"] == "docminibench_answerable" and margin < 0:
            label = "answerable row with high answer margin: good behavior"
        elif r["dataset"] == "docminibench_answerable" and margin > 0:
            label = "answerable row with high NOT_FOUND margin: over-abstention risk"
        else:
            continue
        examples.append((label, r))
    seen = set()
    for label, r in examples:
        if (label, r["model"]) in seen:
            continue
        seen.add((label, r["model"]))
        lines.append(f"- {label}; model=`{r['model']}`, dataset=`{r['dataset']}`, sample=`{r['sample_id']}`, generation=`{r['generation']}`, margin=`{float(r['abstention_margin']):.4f}`")
        if len(seen) >= 12:
            break
    return lines, summary


def write_csv(path: str, rows: list[dict]) -> None:
    fieldnames = list(rows[0])
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", choices=["cpu", "cuda", "mps"], default="cuda")
    parser.add_argument("--controlled-limit", type=int, default=50)
    parser.add_argument("--manual-limit", type=int, default=40)
    parser.add_argument("--answerable-limit", type=int, default=60)
    parser.add_argument("--ood-limit", type=int, default=20)
    parser.add_argument("--include-2b", action="store_true")
    parser.add_argument("--out-csv", default="reports/abstention_margin_analysis.csv")
    parser.add_argument("--out-md", default="reports/abstention_margin_analysis.md")
    parser.add_argument("--base-doc-preds", default="outputs/smolvlm2_500m_video_docminibench_v0_strict_preds.jsonl")
    parser.add_argument("--base-controlled-preds", default="outputs/smolvlm2_500m_video_notfound_controlled_v0_preds.jsonl")
    parser.add_argument("--base-manual-preds", default="outputs/smolvlm2_500m_video_docvqa_manual_notfound_combined_expanded_v0_preds.jsonl")
    parser.add_argument("--base-ood-preds", default="outputs/smolvlm2_500m_video_notfound_ood_sanity_v0_preds.jsonl")
    parser.add_argument("--lora-adapter-path", default="outputs/lora_sft_poc_real/smolvlm2_500m_video_20260613T162714Z")
    parser.add_argument("--lora-doc-preds", default="outputs/smolvlm2_500m_video_lora_real_docminibench_v0_preds.jsonl")
    parser.add_argument("--lora-controlled-preds", default="outputs/smolvlm2_500m_video_lora_real_notfound_controlled_v0_fixed_preds.jsonl")
    parser.add_argument("--lora-manual-preds", default="outputs/smolvlm2_500m_video_lora_real_docvqa_manual_notfound_combined_expanded_v0_preds.jsonl")
    parser.add_argument("--lora-ood-preds", default="outputs/smolvlm2_500m_video_lora_real_notfound_ood_sanity_v0_preds.jsonl")
    parser.add_argument("--no-historical-100step", action="store_true")
    args = parser.parse_args()

    samples = load_prepared_rows(STRICT_CONFIG, args.controlled_limit, args.manual_limit, args.answerable_limit, args.ood_limit)
    runs = [
        ModelRun(
            "base_smolvlm2_500m",
            "smolvlm2_500m_video",
            None,
            read_predictions(args.base_doc_preds)
            | read_predictions(args.base_controlled_preds)
            | read_predictions(args.base_manual_preds)
            | read_predictions(args.base_ood_preds),
        ),
        ModelRun(
            "lora",
            "smolvlm2_500m_video",
            args.lora_adapter_path,
            read_predictions(args.lora_doc_preds)
            | read_predictions(args.lora_controlled_preds)
            | read_predictions(args.lora_manual_preds)
            | read_predictions(args.lora_ood_preds),
        ),
    ]
    if not args.no_historical_100step:
        runs.append(
            ModelRun(
                "lora_100step",
                "smolvlm2_500m_video",
                "outputs/lora_sft_poc_real_continued/smolvlm2_500m_video_continued_20260614T063401Z",
                read_predictions("outputs/smolvlm2_500m_video_lora_real_100step_docminibench_v0_preds.jsonl")
                | read_predictions("outputs/smolvlm2_500m_video_lora_real_100step_notfound_controlled_v0_preds.jsonl")
                | read_predictions("outputs/smolvlm2_500m_video_lora_real_100step_docvqa_manual_notfound_combined_expanded_v0_preds.jsonl")
                | read_predictions("outputs/smolvlm2_500m_video_lora_real_100step_notfound_ood_sanity_v0_preds.jsonl"),
            )
        )
    if args.include_2b:
        runs.append(ModelRun("smolvlm2_2_2b", "smolvlm2_2_2b", None, read_predictions("outputs/smolvlm2_2_2b_docminibench_v0_strict_preds.jsonl") | read_predictions("outputs/smolvlm2_2_2b_notfound_controlled_v0_preds.jsonl")))
    all_rows = []
    blockers = []
    for run in runs:
        try:
            all_rows.extend(score_model(run, samples, args.device))
        except Exception as exc:
            blockers.append(f"{run.label}: {type(exc).__name__}: {exc}")
        finally:
            if args.device == "cuda":
                try:
                    import torch
                    torch.cuda.empty_cache()
                except Exception:
                    pass
    if not all_rows:
        raise RuntimeError("no margin rows produced")
    write_csv(args.out_csv, all_rows)
    lines, _summary = aggregate(all_rows)
    if blockers:
        lines += ["", "## Skipped/Blocked Models", ""]
        lines += [f"- {b}" for b in blockers]
    Path(args.out_md).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote_csv={args.out_csv}")
    print(f"wrote_markdown={args.out_md}")
    if blockers:
        print("blockers=" + json.dumps(blockers))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
