"""Base interfaces for dataset source adapters."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class SourceBuildOptions:
    fixture_mode: bool = True
    allow_downloads: bool = False


class DatasetSourceAdapter:
    """Small source adapter contract for benchmark row candidates."""

    name: str = "source"

    def get_candidates(self, capability: str, options: SourceBuildOptions) -> Iterable[dict]:
        if options.fixture_mode:
            return self._fixture_candidates(capability)
        if not options.allow_downloads:
            raise RuntimeError(
                f"{self.name} real-source materialization is disabled; "
                "re-run with fixture mode or explicitly enable downloads."
            )
        return self._real_candidates(capability)

    def _fixture_candidates(self, capability: str) -> Iterable[dict]:
        return []

    def _real_candidates(self, capability: str) -> Iterable[dict]:
        raise NotImplementedError(
            f"TODO: implement real dataset adapter for {self.name} ({capability})."
        )

