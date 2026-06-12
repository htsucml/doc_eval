"""Source adapter registry for benchmark materialization."""

from __future__ import annotations

from src.datasets.source_adapters.base import DatasetSourceAdapter
from src.datasets.source_adapters.chartqa import ChartQASourceAdapter
from src.datasets.source_adapters.custom_not_found import CustomNotFoundSourceAdapter
from src.datasets.source_adapters.docvqa import DocVQASourceAdapter
from src.datasets.source_adapters.infovqa import InfoVQASourceAdapter
from src.datasets.source_adapters.ocrbench import OCRBenchSourceAdapter
from src.datasets.source_adapters.robustness import RobustnessSourceAdapter


SOURCE_ADAPTERS: dict[str, DatasetSourceAdapter] = {
    "docvqa": DocVQASourceAdapter(),
    "infovqa": InfoVQASourceAdapter(),
    "chartqa": ChartQASourceAdapter(),
    "ocrbench": OCRBenchSourceAdapter(),
    "custom_not_found": CustomNotFoundSourceAdapter(),
    "robustness": RobustnessSourceAdapter(),
}

