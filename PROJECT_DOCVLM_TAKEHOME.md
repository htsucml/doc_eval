# Adapting Small Vision-Language Models under 1B parameters for Document Understanding

## Scope

This repo is the first milestone of a reproducible evaluation and analysis pipeline for small document-focused VLMs. It is intentionally CPU-safe and download-free by default, but it mirrors the interfaces we will need for:

- VLMEvalKit-style benchmark ingestion
- Hugging Face model loading
- capability-sliced reporting
- future LoRA/QLoRA fine-tuning experiments

## Design principles

1. Reproducibility first: deterministic seeds, benchmark hashing, explicit run metadata, fail-closed schema validation.
2. CPU-first milestone: dummy benchmark + dummy model should pass the whole pipeline on a laptop with no GPU.
3. Progressive realism: real adapters and dataset connectors are stubbed or gated behind explicit flags.
4. Document-specific evaluation: OCR fidelity, layout binding, table lookup, chart reasoning, terminology robustness, not-found behavior, calibration, and efficiency are treated as first-class outputs.

## Initial candidate models

- `HuggingFaceTB/SmolVLM-500M-Instruct`
- `HuggingFaceTB/SmolVLM2-500M-Video-Instruct`
- `OpenGVLab/InternVL2_5-1B`
- `llava-hf/llava-onevision-qwen2-0.5b-ov-hf`

`InternVL2_5-1B` sits at the upper edge of the requested size band, so the later comparison write-up should clearly note parameter-count assumptions and any tokenizer / vision tower accounting caveats.

## Metrics in v0

- Exact match overall and by capability
- ANLS-style soft string score
- Relaxed numeric accuracy
- Not-found false-answer rate
- Confidence bucket summaries when available
- Latency summaries

## Next extension points

- Replace fixture builder with real dataset slice builders under `src/datasets/`
- Add OCR-assisted parsing and answer normalization hooks
- Plug in gated real-model inference backends
- Add LoRA/QLoRA data formatting and training stubs in `scripts/finetune_lora.py`

