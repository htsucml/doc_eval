"""Gated Hugging Face adapter skeleton for SmolVLM variants."""

from __future__ import annotations

from typing import Any, Dict

from src.adapters.base import VLMAdapter


class SmolVLMAdapter(VLMAdapter):
    """Lazy-import SmolVLM only when real model runs are explicitly allowed."""

    @property
    def model_id(self) -> str:
        return str(self.config.get("hf_model_id", "smolvlm"))

    def load(self) -> None:
        try:
            __import__("transformers")
        except ImportError as exc:
            raise RuntimeError(
                "Real model loading requires transformers and related GPU/runtime deps. "
                "Install requirements-gpu.txt and rerun with --allow-real-models."
            ) from exc

        raise RuntimeError(
            "SmolVLM real inference is intentionally gated in v0. "
            "Use --allow-real-models only after wiring the processor/model-specific path."
        )

    def generate(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        raise RuntimeError("Call load() before generate() on real adapters.")

