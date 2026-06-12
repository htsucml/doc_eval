"""Gated adapter skeleton for LLaVA-OneVision."""

from __future__ import annotations

from typing import Any, Dict

from src.adapters.base import VLMAdapter


class LlavaOVAdapter(VLMAdapter):
    @property
    def model_id(self) -> str:
        return str(self.config.get("hf_model_id", "llava_ov"))

    def load(self) -> None:
        try:
            __import__("transformers")
        except ImportError as exc:
            raise RuntimeError(
                "LLaVA-OneVision loading is unavailable in the CPU-safe milestone. "
                "Install requirements-gpu.txt and rerun with --allow-real-models."
            ) from exc
        raise RuntimeError(
            "LLaVA-OneVision adapter is a placeholder in v0. Add model-specific loading later."
        )

    def generate(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        raise RuntimeError("Call load() before generate() on real adapters.")

