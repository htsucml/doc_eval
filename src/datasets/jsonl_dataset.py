"""JSONL dataset loading and writing utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List


def load_jsonl(path: str | Path, validator: Callable[[Dict[str, Any]], Dict[str, Any]] | None = None) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            row = json.loads(line)
            if validator:
                try:
                    row = validator(row)
                except Exception as exc:  # pragma: no cover - exercised through tests
                    raise ValueError(f"{path}:{line_number}: {exc}") from exc
            rows.append(row)
    return rows


def write_jsonl(path: str | Path, rows: Iterable[Dict[str, Any]]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True) + "\n")

