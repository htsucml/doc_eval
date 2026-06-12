"""Small parsing helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_config_like_json(path: str | Path) -> Any:
    """Parse `.yaml` config files written as JSON, avoiding external YAML deps in v0."""

    return json.loads(Path(path).read_text(encoding="utf-8"))

