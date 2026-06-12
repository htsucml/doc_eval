"""Lazy SmolVLM adapter for explicit real-model smoke runs."""

from __future__ import annotations

import time
from typing import Any, Dict

from src.adapters.base import VLMAdapter
from src.utils.image import load_image_for_vlm


class SmolVLMAdapter(VLMAdapter):
    """Lazy-load SmolVLM only when real model runs are explicitly enabled."""

    def __init__(self, config: Dict[str, Any] | None = None) -> None:
        super().__init__(config)
        self._processor = None
        self._model = None
        self._device = "cpu"
        self._generation_kwargs: Dict[str, Any] = {}

    @property
    def model_id(self) -> str:
        return str(self.config.get("hf_model_id", "smolvlm"))

    def load(self) -> None:
        try:
            import torch
            from transformers import AutoProcessor
        except Exception as exc:
            raise RuntimeError(
                "Real model loading requires a compatible torch/transformers/Pillow stack. "
                "Install requirements-gpu.txt in a fresh environment and retry with --allow-real-models. "
                f"Original import error: {exc}"
            ) from exc
        try:
            from transformers import AutoModelForVision2Seq as auto_model_cls
        except ImportError:
            try:
                from transformers import AutoModelForImageTextToText as auto_model_cls
            except ImportError as exc:
                raise RuntimeError(
                    "Your transformers build does not expose a compatible image-text auto model class "
                    "for SmolVLM. Upgrade transformers from requirements-gpu.txt."
                ) from exc

        requested_device = str(self.runtime.get("device", self.config.get("device", "cpu"))).lower()
        if requested_device not in {"cpu", "cuda", "mps"}:
            raise RuntimeError(f"Unsupported device '{requested_device}'. Expected one of: cpu, cuda, mps.")
        if requested_device == "cuda" and not torch.cuda.is_available():
            raise RuntimeError("CUDA was requested but is not available on this machine.")
        mps_backend = getattr(torch.backends, "mps", None)
        if requested_device == "mps" and (mps_backend is None or not mps_backend.is_available()):
            raise RuntimeError("MPS was requested but is not available on this machine.")

        dtype = torch.float32 if requested_device == "cpu" else torch.float16
        self._processor = AutoProcessor.from_pretrained(self.model_id)
        self._model = auto_model_cls.from_pretrained(
            self.model_id,
            torch_dtype=dtype,
        )
        self._model.to(requested_device)
        self._model.eval()
        self._device = requested_device
        self._generation_kwargs = dict(self.config.get("generation_kwargs", {}))

    def generate(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        if self._processor is None or self._model is None:
            raise RuntimeError("Call load() before generate() on real adapters.")

        import torch

        prompt_text = sample.get("prompt_text") or sample["question"]
        image = load_image_for_vlm(sample["image_path"])
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image"},
                    {
                        "type": "text",
                        "text": prompt_text,
                    },
                ],
            }
        ]
        prompt = self._build_prompt(messages, prompt_text)

        started = time.perf_counter()
        inputs = self._processor(
            text=prompt,
            images=[image],
            return_tensors="pt",
        )
        inputs = {key: value.to(self._device) if hasattr(value, "to") else value for key, value in inputs.items()}
        with torch.no_grad():
            generated = self._model.generate(
                **inputs,
                **self._generation_kwargs,
            )
        decoded = self._decode_generated_text(generated, inputs)
        latency_s = round(time.perf_counter() - started, 4)
        return {
            "raw_output": decoded,
            "parsed_answer": decoded,
            "confidence": None,
            "latency_s": latency_s,
            "error": None,
            "inference_config": {
                "device": self._device,
                **self._generation_kwargs,
            },
        }

    def _build_prompt(self, messages: list[dict], fallback_question: str) -> str:
        if hasattr(self._processor, "apply_chat_template"):
            return self._processor.apply_chat_template(
                messages,
                add_generation_prompt=True,
            )
        return fallback_question

    def _decode_generated_text(self, generated: Any, inputs: Dict[str, Any]) -> str:
        generated_ids = generated
        input_ids = inputs.get("input_ids")
        if input_ids is not None and hasattr(generated, "shape") and generated.shape[1] >= input_ids.shape[1]:
            generated_ids = generated[:, input_ids.shape[1] :]
        text = self._processor.batch_decode(
            generated_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True,
        )[0]
        return text.strip()
