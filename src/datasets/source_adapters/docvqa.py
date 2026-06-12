"""DocVQA source adapter skeleton."""

from __future__ import annotations

from typing import Iterable

from src.datasets.source_adapters.base import DatasetSourceAdapter
from src.datasets.vlmevalkit_placeholders import filter_fixture_rows


class DocVQASourceAdapter(DatasetSourceAdapter):
    name = "docvqa"

    def _fixture_candidates(self, capability: str) -> Iterable[dict]:
        return filter_fixture_rows({"ocr_exact", "layout_binding", "domain_terms"})

    def _real_candidates(self, capability: str) -> Iterable[dict]:
        raise NotImplementedError(
            "TODO: map DocVQA task annotations into benchmark rows without eager downloads."
        )

