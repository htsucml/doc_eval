# Survey Matrix v0

This is a concise starting matrix for the take-home task.

| Need / Challenge | Why it matters | Candidate datasets | Candidate metrics |
| --- | --- | --- | --- |
| OCR/text extraction | Short identifiers and exact spans often dominate downstream failure | DocVQA, OCRBench-style slices, TextVQA-style OCR | Exact match, ANLS, token-F1 |
| Structured field parsing | Forms and invoices require binding values to the right fields | DocVQA, custom form slices | Exact match by field, field grounding |
| Table/list lookup | Business docs often require row/column retrieval rather than free-form QA | InfoVQA, table-focused custom slices | Exact match, table retrieval accuracy |
| Chart/numeric reasoning | Numeric mistakes are high-cost in document workflows | ChartQA | Relaxed numeric score, exact match |
| Domain terminology | Medical/legal/finance terms stress OCR and vocabulary robustness | OCRBench-style domain slices, custom terminology slices | Exact match, ANLS |
| Not-found / calibration | Safe abstention matters when answers are absent or ambiguous | Custom unanswerable stress slice | False-answer rate, ECE-style buckets |
| Hallucination avoidance | Small VLMs may over-answer sparse prompts | Custom negative slices | Abstention precision/recall |
| Efficiency | Under-1B models are attractive only if latency/memory remain low | Any benchmark with fixed image sizes | Latency, throughput, memory |

