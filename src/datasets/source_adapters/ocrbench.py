"""OCRBench/TextVQA-style source adapter skeleton."""

from __future__ import annotations

from typing import Iterable

from src.datasets.source_adapters.base import DatasetSourceAdapter
from src.datasets.vlmevalkit_placeholders import filter_fixture_rows


class OCRBenchSourceAdapter(DatasetSourceAdapter):
    name = "ocrbench"

    def _fixture_candidates(self, capability: str) -> Iterable[dict]:
        return filter_fixture_rows({"ocr_exact", "domain_terms"})

    def _real_candidates(self, capability: str) -> Iterable[dict]:
        raise NotImplementedError(
            "TODO: add OCRBench/TextVQA-style exactness row extraction behind an explicit flag."
        )

