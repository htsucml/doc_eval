# AGENTS.md

## Project Goal

Prepare a reproducible document-VLM evaluation repo for a bounded take-home execution. The repo should construct or adapt a small benchmark, run one evaluation pipeline across compact VLMs, aggregate comparable metrics, export error tables, record hardware and software details, and support a technical report.

## Current Priority

The immediate priority is real zero-shot evaluation on sub-1B vision-language models, starting with SmolVLM 500M and then trying one additional compact fallback model if time and hardware allow.

## Operating Rules

- Do not fake results. If a run is dummy, fixture-only, partial, failed, or blocked, label it exactly that way.
- Do not commit outputs, caches, model weights, downloaded datasets, adapters, or local virtual environments.
- Real model loading must stay gated behind explicit commands and flags such as `--allow-real-models`.
- Prefer small deterministic subsets while validating infrastructure, then scale only after the smoke path is proven.
- Fail closed on schema errors. Do not coerce malformed benchmark or prediction rows into passing silently.
- Write exact commands, logs, hardware details, inference settings, package versions, and failure messages into `logs/` or `reports/`.
- If blocked for more than 60 minutes on one model, stop that attempt and switch to the next fallback model.
- Keep RunPod execution bounded. Do not add infinite retry loops or background jobs that hide failures.
