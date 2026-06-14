"""Audit JSONL benchmark/data files for local image dependencies."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def iter_jsonl_files(data_dir: Path) -> list[Path]:
    return sorted(data_dir.glob("*.jsonl"))


def audit(root: Path, data_dir: Path) -> tuple[list[str], list[dict]]:
    machine_rows: list[dict] = []
    missing_all: list[str] = []
    for path in iter_jsonl_files(data_dir):
        rows = 0
        image_paths: list[str] = []
        missing: list[str] = []
        capabilities: Counter[str] = Counter()
        with path.open("r", encoding="utf-8") as handle:
            for raw in handle:
                if not raw.strip():
                    continue
                rows += 1
                row = json.loads(raw)
                if "capability" in row:
                    capabilities[str(row["capability"])] += 1
                image_path = row.get("image_path")
                if image_path:
                    image_paths.append(str(image_path))
                    resolved = Path(image_path)
                    if not resolved.is_absolute():
                        resolved = root / resolved
                    if not resolved.exists():
                        missing.append(str(image_path))
        unique_count = len(set(image_paths))
        missing_unique = sorted(set(missing))
        missing_all.extend(missing_unique)
        machine_rows.append(
            {
                "jsonl": str(path.relative_to(root) if path.is_relative_to(root) else path),
                "rows": rows,
                "unique_images": unique_count,
                "missing_images": len(missing_unique),
                "capabilities": dict(sorted(capabilities.items())),
            }
        )
    return missing_all, machine_rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--report", default=None)
    parser.add_argument("--json-report", default=None)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    data_dir = (root / args.data_dir).resolve()
    if not data_dir.exists():
        raise SystemExit(f"data directory does not exist: {data_dir}")
    missing, machine = audit(root, data_dir)
    text_lines = [
        "# Data Dependency Audit",
        "",
        f"- root: `{root}`",
        f"- data_dir: `{data_dir}`",
        f"- jsonl_files: `{len(machine)}`",
        "",
        "## Files",
        "",
    ]
    for row in machine:
        text_lines.append(
            f"- `{row['jsonl']}`: rows={row['rows']}, "
            f"unique_images={row['unique_images']}, missing_images={row['missing_images']}"
        )
        if row["capabilities"]:
            text_lines.append(f"  - capabilities={row['capabilities']}")
    if missing:
        text_lines += ["", "## Missing Images", ""]
        text_lines.extend(f"- `{path}`" for path in sorted(set(missing)))
    else:
        text_lines += ["", "No missing image dependencies found."]

    output = "\n".join(text_lines) + "\n"
    print(output)
    if args.report:
        report_path = root / args.report
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(output, encoding="utf-8")
    if args.json_report:
        json_path = root / args.json_report
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(machine, indent=2) + "\n", encoding="utf-8")
    if missing:
        raise SystemExit(f"missing image dependencies: {len(set(missing))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
