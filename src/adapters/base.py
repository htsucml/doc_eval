"""Backend-neutral VLM adapter interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class VLMAdapter(ABC):
    """Abstract interface for small VLM backends."""

    supports_confidence: bool = False

    def __init__(self, config: Dict[str, Any] | None = None) -> None:
        self.config = config or {}
        self.runtime: Dict[str, Any] = {}

    @property
    @abstractmethod
    def model_id(self) -> str:
        """Stable identifier for the loaded model."""

    @abstractmethod
    def load(self) -> None:
        """Initialize model resources lazily."""

    @abstractmethod
    def generate(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Run generation for one benchmark sample."""
