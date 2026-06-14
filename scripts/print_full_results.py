"""Print compact Markdown tables for the latest full reproduction run."""

from __future__ import annotations

import argparse
import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def is_complete_run(report_dir: Path) -> bool:
    status_path = report_dir / "run_status.json"
    if not status_path.exists():
        return False
    try:
        status = json.loads(status_path.read_text(encoding="utf-8"))
    except Exception:
        return False
    return status.get("status") == "complete" and any(report_dir.glob("*_results.csv"))


def resolve_run(run: str | None) -> tuple[str, Path, Path] | None:
    report_base = ROOT / "reports" / "full_repro"
    output_base = ROOT / "outputs" / "full_repro"
    if run:
        run_id = run
        report_dir = report_base / run_id
        if not is_complete_run(report_dir):
            return None
    else:
        latest = report_base / "latest"
        candidates: list[str] = []
        if latest.is_symlink():
            candidates.append(os.readlink(latest))
        elif latest.exists():
            candidates.append(latest.resolve().name)
        if report_base.exists():
            candidates.extend(reversed(sorted(p.name for p in report_base.iterdir() if p.is_dir())))
        seen = set()
        run_id = ""
        for candidate in candidates:
            if candidate in seen:
                continue
            seen.add(candidate)
            if is_complete_run(report_base / candidate):
                run_id = candidate
                break
        if not run_id:
            return None
    return run_id, output_base / run_id, report_base / run_id


def overall(path: Path) -> dict[str, str] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["slice_type"] == "overall":
                return row
    return None


def capability(path: Path, name: str) -> dict[str, str] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["slice_type"] == "capability" and row["slice_name"] == name:
                return row
    return None


def f(row: dict[str, str] | None, key: str) -> str:
    if row is None or row.get(key) in (None, ""):
        return "--"
    return f"{float(row[key]):.4f}".rstrip("0").rstrip(".")


def answerable_exact(path: Path) -> str:
    caps = ["chart_numeric", "domain_terms", "layout_binding", "ocr_exact", "table_lookup"]
    total = 0
    weighted = 0.0
    for cap in caps:
        row = capability(path, cap)
        if row is None:
            return "--"
        count = int(row["count"])
        total += count
        weighted += count * float(row["exact_match"])
    return f"{weighted / total:.4f}".rstrip("0").rstrip(".") if total else "--"


def line(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def build_markdown(run_id: str, _out_dir: Path, report_dir: Path) -> str:
    rows = [
        ("SmolVLM 500M", "smolvlm_500m"),
        ("SmolVLM2 500M", "smolvlm2_500m_video"),
        ("SmolVLM2 500M + LoRA", "smolvlm2_500m_video_lora"),
        ("SmolVLM2 2.2B ref", "smolvlm2_2_2b"),
        ("Qwen2.5-VL 3B ref", "qwen2_5_vl_3b_instruct"),
    ]
    lines = [f"# Full Reproduction Results: `{run_id}`", ""]
    lines += [
        "## DocMiniBench",
        "",
        line(["Model", "Overall exact", "Answer in output", "Answerable-only exact", "Old NF false-answer"]),
        line(["---", "---:", "---:", "---:", "---:"]),
    ]
    for label, prefix in rows:
        path = report_dir / f"{prefix}_docminibench_v0_results.csv"
        if not path.exists():
            continue
        row = overall(path)
        nf = capability(path, "not_found")
        lines.append(line([label, f(row, "exact_match"), f(row, "answer_in_output"), answerable_exact(path), f(nf, "not_found_false_answer_rate")]))

    lines += [
        "",
        "## NOT_FOUND Transfer",
        "",
        line(["Model", "Controlled false", "Manual false", "OOD false"]),
        line(["---", "---:", "---:", "---:"]),
    ]
    for label, prefix in rows:
        controlled = overall(report_dir / f"{prefix}_notfound_controlled_v0_results.csv")
        manual = overall(report_dir / f"{prefix}_docvqa_manual_notfound_combined_expanded_v0_results.csv")
        ood = overall(report_dir / f"{prefix}_notfound_ood_sanity_v0_results.csv")
        if not any([controlled, manual, ood]):
            continue
        lines.append(line([label, f(controlled, "not_found_false_answer_rate"), f(manual, "not_found_false_answer_rate"), f(ood, "not_found_false_answer_rate")]))

    margin = report_dir / "abstention_margin_analysis.md"
    lines += ["", "## Abstention Diagnostics", ""]
    if margin.exists():
        lines.append(f"- Margin diagnostics: `{margin}`")
    else:
        lines.append("- Margin diagnostics were not produced for this run.")
    skipped = report_dir / "skipped_reference_models.log"
    if skipped.exists():
        lines += ["", "## Skips", "", "```text", skipped.read_text(encoding="utf-8").strip(), "```"]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", default=None)
    parser.add_argument("--write-handoff", action="store_true")
    args = parser.parse_args()
    resolved = resolve_run(args.run)
    if resolved is None:
        target = f"`{args.run}`" if args.run else "latest full reproduction"
        print(
            f"No complete full reproduction results found for {target}.\n\n"
            "A valid run must contain `reports/full_repro/<timestamp>/run_status.json` "
            "with `status: complete` and at least one `*_results.csv` file. "
            "Run `make check-full` first, then `make full` on a CUDA-enabled environment."
        )
        return 0
    run_id, out_dir, report_dir = resolved
    markdown = build_markdown(run_id, out_dir, report_dir)
    print(markdown)
    summary_path = report_dir / "compact_results.md"
    summary_path.write_text(markdown, encoding="utf-8")
    if args.write_handoff:
        handoff = {
            "run_id": run_id,
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "output_dir": str(out_dir),
            "report_dir": str(report_dir),
            "compact_results": str(summary_path),
            "commands_log": str(report_dir / "full_repro_commands.log"),
        }
        (report_dir / "full_repro_handoff.json").write_text(json.dumps(handoff, indent=2) + "\n", encoding="utf-8")
        (report_dir / "full_repro_handoff.md").write_text(markdown, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
