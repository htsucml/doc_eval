# Survey Matrix v0

This matrix is intentionally scoped to planning and reporting. Citations below are placeholders unless a URL is already available in local notes.

## Application / Product Side

| Area | Why it matters in products | Typical evaluation slice | Reporting / metric focus | Citation / note |
| --- | --- | --- | --- | --- |
| OCR / text extraction | Downstream field extraction and QA fail early if text fidelity is weak. | Small fonts, IDs, totals, noisy scans | Exact match, ANLS, token-F1 later | Placeholder: add OCRBench or DocVQA note |
| Structured field extraction | Invoices, forms, and receipts depend on correct field-to-value binding. | Key-value documents, forms, invoices | By-capability exact match, field-level grounding later | Placeholder: add form extraction reference |
| Table / list parsing | Operational workflows often need row and column retrieval, not generic captions. | Line items, schedules, inventories | Table lookup slice accuracy, numeric agreement | Placeholder: add table benchmark reference |
| Not-found / calibration | Safe abstention matters when a requested field is absent. | Explicit unanswerable questions with distractors | Not-found false-answer rate, calibration buckets | Placeholder: add abstention/calibration reference |
| Hallucination avoidance | Over-answering creates high-cost errors in business settings. | Negative examples with nearby distractor text | Failure-type counts, abstention precision/recall later | Placeholder: add hallucination mitigation note |
| Efficiency / edge deployment | Compact models only help if latency and memory stay bounded on CPU or edge hardware. | Fixed-resolution document runs | Latency, memory, throughput, image-size sensitivity | Placeholder: add edge deployment note |

## Research Side

| Area | Why it matters in research | Typical evaluation slice | Reporting / metric focus | Citation / note |
| --- | --- | --- | --- | --- |
| OCR fidelity | Character-level errors often dominate document QA before reasoning. | OCR-heavy spans, codes, dates | Exact match, ANLS, normalized string analysis | Placeholder: add OCR fidelity paper |
| Layout perception | Models must bind values to the right visual regions and labels. | Forms, multi-column pages, dense layouts | Capability slices for layout binding and field extraction | Placeholder: add layout benchmark |
| Complex parsing | Documents mix prose, headers, lists, tables, and semi-structured regions. | Multi-region extraction tasks | Error export by capability and answer type | Placeholder: add parsing benchmark |
| Table / chart / numeric reasoning | Numeric mistakes are especially costly and easy to hide behind string overlap. | Charts, tables, totals, comparisons | Relaxed numeric score, exact match, failure-type breakdown | Placeholder: add ChartQA / numeric reasoning note |
| Domain terminology | Specialized abbreviations stress OCR, vocabulary, and prior knowledge together. | Medical, legal, finance terminology | Domain slice exact match, ANLS for near-misses | Placeholder: add domain-doc benchmark |
| Unanswerable QA | Abstention quality is part of correctness, not just a UX preference. | Missing fields, ambiguous prompts | Not-found false-answer rate, calibration buckets | Placeholder: add unanswerable QA reference |
| Robustness | Formatting variation and noisy scans expose brittle prompt or parser assumptions. | Rotation, blur, low contrast, alternate templates | Slice-aware regressions, normalization stress tests | Placeholder: add robustness benchmark |
