"""Optional handwriting/robustness adapter skeleton."""

from __future__ import annotations

from typing import Iterable

from src.datasets.source_adapters.base import DatasetSourceAdapter
from src.datasets.vlmevalkit_placeholders import filter_fixture_rows


class RobustnessSourceAdapter(DatasetSourceAdapter):
    name = "robustness"

    def _fixture_candidates(self, capability: str) -> Iterable[dict]:
        return filter_fixture_rows({"robustness_optional"})

    def _real_candidates(self, capability: str) -> Iterable[dict]:
        raise NotImplementedError(
            "TODO: plug in handwriting or perturbation robustness slices as optional sources."
        )
