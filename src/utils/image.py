"""Image-path helpers for fixture-oriented evaluation."""

from __future__ import annotations

from pathlib import Path


def resolve_image_path(path: str) -> str:
    return str(Path(path))

