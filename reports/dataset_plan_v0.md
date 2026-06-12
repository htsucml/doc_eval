# Dataset Plan v0

This benchmark exists to measure whether a small document VLM can answer grounded questions without quietly hallucinating, while staying cheap enough to run in a CPU-only take-home environment.

| task slice | product motivation | academic benchmark source | metric | limitation | engineering risk |
| --- | --- | --- | --- | --- | --- |
| `ocr_exact` | Catch failures on invoice IDs, account numbers, and short exact spans where one character matters. | `OCRBench` or `TextVQA`-style exact string tasks, with `DocVQA` fallback coverage. | `exact_match` | Public OCR-heavy benchmarks can overrepresent short Latin text and underrepresent messy enterprise scans. | Real-source ingestion may require annotation remapping and download gates to avoid accidental large fetches. |
| `layout_binding` | Test whether the model binds the right value to the right nearby field instead of copying a plausible number from elsewhere. | `DocVQA`, plus selected `InfoVQA` layout-referenced prompts. | `exact_match` | Layout binding is often entangled with OCR quality, so root cause attribution is imperfect. | Source schemas differ across datasets, so field normalization can drift if adapters are too loose. |
| `table_lookup` | Validate row/column lookup for spend tables, shipment manifests, and KPI summaries. | `InfoVQA` primary, `DocVQA` candidates where tables are explicit. | `exact_match` | Tiny v0 fixtures do not exercise multi-hop table reasoning or large tables. | Table questions often need structure-aware preprocessing later, which can change benchmark semantics. |
| `chart_numeric` | Check whether the model reads chart values and simple comparisons instead of guessing from trend shape. | `ChartQA`. | `relaxed_numeric` | Relaxed numeric scoring can hide formatting mistakes that matter in finance or ops settings. | Chart assets and answer normalization can become brittle across raster vs. vector render paths. |
| `domain_terms` | Measure exact recovery of domain-specific codes and terminology that generic VQA benchmarks miss. | `OCRBench` or `TextVQA`-style sources, plus filtered `DocVQA` examples. | `exact_match` | Public sources may not cover the exact regulated vocabulary needed by production workflows. | Custom vocab slices can drift into private data needs if not kept synthetic or publicly sourced. |
| `not_found` | Reward abstention when the requested field is absent, reducing hallucinated business actions. | Custom hallucination-stress prompts. | `not_found_false_answer_rate` | Negative examples are synthetic in v0 and may not capture every real ambiguity pattern. | If this slice is underspecified, models may overfit to the literal token `NOT_FOUND` instead of true abstention behavior. |
| `robustness_optional` | Leave room for handwriting, blur, compression, or scan-noise stress tests without blocking the core benchmark. | Optional custom or handwriting-oriented sources. | `exact_match` | Optional status means v0 comparisons may ignore a real-world failure mode. | Robustness sources can balloon data size quickly if perturbations are materialized eagerly. |

## Notes

- Fixture mode is the default because it is deterministic, CPU-only, and safe for CI or take-home review.
- Real-source adapters are intentionally TODO-marked and must stay behind explicit flags before any download or heavy materialization is allowed.
- The benchmark manifest is hashed after build so evaluation metadata can pin exactly which row set a run used.
