"""InfoVQA source adapter skeleton."""

from __future__ import annotations

from typing import Iterable

from src.datasets.source_adapters.base import DatasetSourceAdapter
from src.datasets.vlmevalkit_placeholders import filter_fixture_rows


class InfoVQASourceAdapter(DatasetSourceAdapter):
    name = "infovqa"

    def _fixture_candidates(self, capability: str) -> Iterable[dict]:
        return filter_fixture_rows({"layout_binding", "table_lookup"})

    def _real_candidates(self, capability: str) -> Iterable[dict]:
        raise NotImplementedError(
            "TODO: convert InfoVQA infographic QA examples into slice-tagged benchmark rows."
        )

