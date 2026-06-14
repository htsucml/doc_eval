# Step 4 SFT Training Status

- Timestamp UTC: `2026-06-13T16:28:18.944783+00:00`
- Status: `passed`
- Existing `scripts/finetune_lora.py` support before this step: dry-run validation only; no real model loading/training/save/reload/eval path.
- Implemented support in this step: image+text examples, processor/model loading, PEFT LoRA attachment, answer-token loss masking, adapter save, adapter reload verification.
- Adapted-model evaluation support is handled in Step 5 if reload works.
- Target model: `smolvlm2_500m_video`
- HF model id: `HuggingFaceTB/SmolVLM2-500M-Video-Instruct`
- Completed steps: `50`
- Checkpoint path: `outputs/lora_sft_poc_real/smolvlm2_500m_video_20260613T162714Z`
- Reload verified: `True`
- Trainable parameters: `819200`
- Total parameters: `508301504`
- Loss first: `1.155880331993103`
- Loss last: `0.17790615558624268`
- Vision tower was frozen; LoRA targeted text-model self-attention `q_proj`/`v_proj` modules only.
- Processor emitted non-fatal warnings about processor kwargs; training completed despite them.

## Exact Training Command
```bash
HF_HOME=/workspace/hf_home HF_HUB_CACHE=/workspace/hf_home/hub HUGGINGFACE_HUB_CACHE=/workspace/hf_home/hub HF_DATASETS_CACHE=/workspace/hf_home/datasets .venv/bin/python scripts/finetune_lora.py --model smolvlm2_500m_video --train data/sft_docvqa_template_train_v0.jsonl --val data/sft_docvqa_template_val_v0.jsonl --max_steps 50 --output-dir outputs/lora_sft_poc_real --device cuda --verify-reload
```
