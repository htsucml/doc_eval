"""Dataset registry placeholders for benchmark materialization."""

from __future__ import annotations

from typing import Callable, Dict, List

from src.datasets.source_adapters import SOURCE_ADAPTERS
from src.datasets.vlmevalkit_placeholders import build_fixture_benchmark


DATASET_BUILDERS: Dict[str, Callable[[], List[dict]]] = {
    "fixture_docmini_v0": build_fixture_benchmark,
}

DATASET_SOURCE_ADAPTERS = SOURCE_ADAPTERS
