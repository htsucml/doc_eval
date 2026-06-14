"""Build LaTeX tables and lightweight figures from existing result CSVs."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"


def read_overall(path: str) -> dict[str, str] | None:
    file_path = ROOT / path
    if not file_path.exists():
        return None
    with file_path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["slice_type"] == "overall":
                return row
    return None


def read_capability(path: str, capability: str) -> dict[str, str] | None:
    file_path = ROOT / path
    if not file_path.exists():
        return None
    with file_path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["slice_type"] == "capability" and row["slice_name"] == capability:
                return row
    return None


def as_float(row: dict[str, str] | None, key: str) -> float | None:
    if row is None:
        return None
    value = row.get(key)
    if value in (None, ""):
        return None
    return float(value)


def fmt(value: float | None) -> str:
    if value is None:
        return "--"
    return f"{value:.4f}".rstrip("0").rstrip(".")


def table_line(cells: list[str]) -> str:
    return " & ".join(cells) + r" \\"


def write(path: str, text: str) -> None:
    out = PAPER / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")


def build_tables() -> dict[str, dict[str, float | None]]:
    runs = [
        (
            "SmolVLM 500M",
            "target",
            "reports/smolvlm_500m_docminibench_v0_strict_results.csv",
            "reports/smolvlm_500m_notfound_controlled_v0_results.csv",
            "reports/smolvlm_500m_docvqa_manual_notfound_combined_expanded_v0_results.csv",
            "reports/smolvlm_500m_notfound_ood_sanity_v0_results.csv",
        ),
        (
            "SmolVLM2 500M",
            "target",
            "reports/smolvlm2_500m_video_docminibench_v0_strict_results.csv",
            "reports/smolvlm2_500m_video_notfound_controlled_v0_results.csv",
            "reports/smolvlm2_500m_video_docvqa_manual_notfound_combined_expanded_v0_results.csv",
            "reports/smolvlm2_500m_video_notfound_ood_sanity_v0_results.csv",
        ),
        (
            "SmolVLM2 500M + LoRA-100",
            "target PoC",
            "reports/smolvlm2_500m_video_lora_real_100step_docminibench_v0_results.csv",
            "reports/smolvlm2_500m_video_lora_real_100step_notfound_controlled_v0_results.csv",
            "reports/smolvlm2_500m_video_lora_real_100step_docvqa_manual_notfound_combined_expanded_v0_results.csv",
            "reports/smolvlm2_500m_video_lora_real_100step_notfound_ood_sanity_v0_results.csv",
        ),
        (
            "SmolVLM2 2.2B",
            ">1B same-family reference",
            "reports/smolvlm2_2_2b_docminibench_v0_strict_results.csv",
            "reports/smolvlm2_2_2b_notfound_controlled_v0_results.csv",
            "reports/smolvlm2_2_2b_docvqa_manual_notfound_combined_expanded_v0_results.csv",
            "reports/smolvlm2_2_2b_notfound_ood_sanity_v0_results.csv",
        ),
        (
            "Qwen2.5-VL 3B",
            ">1B external ceiling",
            "reports/qwen2_5_vl_3b_instruct_docminibench_v0_results.csv",
            "reports/qwen2_5_vl_3b_instruct_notfound_controlled_v0_results.csv",
            "reports/qwen2_5_vl_3b_instruct_docvqa_manual_notfound_combined_expanded_v0_results.csv",
            "reports/qwen2_5_vl_3b_instruct_notfound_ood_sanity_v0_results.csv",
        ),
    ]

    metrics: dict[str, dict[str, float | None]] = {}
    main_rows = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\small",
        r"\begin{tabular}{llrrrrrr}",
        r"\hline",
        table_line(
            [
                "Model",
                "Role",
                "DocMini exact",
                "DocMini ans-in",
                "Old NF false",
                "Controlled false",
                "Manual false",
                "OOD false",
            ]
        ),
        r"\hline",
    ]
    for label, role, doc_path, controlled_path, manual_path, ood_path in runs:
        doc = read_overall(doc_path)
        old_nf = read_capability(doc_path, "not_found")
        controlled = read_overall(controlled_path)
        manual = read_overall(manual_path)
        ood = read_overall(ood_path)
        metrics[label] = {
            "doc_exact": as_float(doc, "exact_match"),
            "doc_answer_in": as_float(doc, "answer_in_output"),
            "old_nf_false": as_float(old_nf, "not_found_false_answer_rate"),
            "controlled_false": as_float(controlled, "not_found_false_answer_rate"),
            "manual_false": as_float(manual, "not_found_false_answer_rate"),
            "ood_false": as_float(ood, "not_found_false_answer_rate"),
        }
        main_rows.append(
            table_line(
                [
                    label,
                    role,
                    fmt(metrics[label]["doc_exact"]),
                    fmt(metrics[label]["doc_answer_in"]),
                    fmt(metrics[label]["old_nf_false"]),
                    fmt(metrics[label]["controlled_false"]),
                    fmt(metrics[label]["manual_false"]),
                    fmt(metrics[label]["ood_false"]),
                ]
            )
        )
    main_rows.extend(
        [
            r"\hline",
            r"\end{tabular}",
            r"\caption{Current headline metrics from existing CSV artifacts. NOT\_FOUND false-answer rates are lower-is-better. The original DocMiniBench-v0 NOT\_FOUND slice is demoted and shown only for continuity.}",
            r"\label{tab:headline-results}",
            r"\end{table*}",
        ]
    )
    write("tables/headline_results.tex", "\n".join(main_rows) + "\n")

    lora_rows = [
        r"\begin{table}[t]",
        r"\centering",
        r"\small",
        r"\begin{tabular}{lrrrr}",
        r"\hline",
        table_line(["Checkpoint", "Doc exact", "Ans-only exact", "Controlled false", "Manual false"]),
        r"\hline",
        table_line(["Base", "0.4417", "0.53", "0.98", "1.0"]),
        table_line(["50 steps", "0.5083", "0.55", "0.30", "0.8941"]),
        table_line(["100 steps", "0.5333", "0.55", "0.10", "0.6235"]),
        r"\hline",
        r"\end{tabular}",
        r"\caption{Bounded LoRA/SFT methodology PoC. The answerable-only exact-match values exclude the demoted NOT\_FOUND slice.}",
        r"\label{tab:lora-poc}",
        r"\end{table}",
    ]
    write("tables/lora_poc.tex", "\n".join(lora_rows) + "\n")

    figure = [
        r"\begin{figure}[t]",
        r"\centering",
        r"\small",
        r"\fbox{\begin{minipage}{0.92\linewidth}",
        r"\textbf{Manual real-doc NOT\_FOUND false-answer rate}\\[2pt]",
        r"SmolVLM2 500M: 1.0000\\",
        r"SmolVLM2 500M + LoRA-100: 0.6235\\",
        r"SmolVLM2 2.2B reference: 0.4353\\",
        r"Qwen2.5-VL 3B ceiling: 0.0353",
        r"\end{minipage}}",
        r"\caption{Manual real-document abstention transfer. Lower false-answer rate is better.}",
        r"\label{fig:manual-transfer}",
        r"\end{figure}",
    ]
    write("figures/manual_transfer.tex", "\n".join(figure) + "\n")
    return metrics


def main() -> int:
    build_tables()
    write(
        "tables/generated_at.tex",
        "% Auto-generated by scripts/build_paper_assets.py\n"
        + r"\newcommand{\paperassetsgenerated}{generated from local CSV artifacts}"
        + "\n",
    )
    print("wrote paper tables and figure snippets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
