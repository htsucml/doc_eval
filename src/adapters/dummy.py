"""Deterministic adapter for CPU-only fixture validation."""

from __future__ import annotations

from typing import Any, Dict

from src.adapters.base import VLMAdapter


class DummyAdapter(VLMAdapter):
    """Return predictable outputs for fixture samples."""

    supports_confidence = True

    _OUTPUTS = {
        "ocr-1": ("INV-001", 0.99),
        "layout-1": ("$42.00", 0.96),
        "table-1": ("6", 0.88),
        "chart-1": ("March", 0.82),
        "domain-1": ("99213", 0.97),
        "notfound-1": ("555-0199", 0.91),
        "robust-1": ("PO-77", 0.76),
    }

    @property
    def model_id(self) -> str:
        return "dummy"

    def load(self) -> None:
        return None

    def generate(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        answer, confidence = self._OUTPUTS.get(sample["id"], ("NOT_FOUND", 0.5))
        return {
            "raw_output": answer,
            "parsed_answer": answer,
            "confidence": confidence,
            "latency_s": 0.01,
            "error": None,
            "inference_config": {
                "temperature": 0.0,
                "seed": 7,
                "adapter_mode": "fixture",
            },
        }

