"""ChartQA source adapter skeleton."""

from __future__ import annotations

from typing import Iterable

from src.datasets.source_adapters.base import DatasetSourceAdapter
from src.datasets.vlmevalkit_placeholders import filter_fixture_rows


class ChartQASourceAdapter(DatasetSourceAdapter):
    name = "chartqa"

    def _fixture_candidates(self, capability: str) -> Iterable[dict]:
        return filter_fixture_rows({"chart_numeric"})

    def _real_candidates(self, capability: str) -> Iterable[dict]:
        raise NotImplementedError(
            "TODO: support ChartQA subset extraction with numeric-answer normalization."
        )

