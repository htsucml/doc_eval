# Error Analysis v0

This report uses existing v0 prediction outputs and the additive controlled NOT_FOUND outputs. No existing v0 model outputs or datasets were regenerated.

## Provenance Caveat

The old `docminibench_v0` NOT_FOUND slice should be treated as exploratory. The provenance audit found fixed-template questions, one DocVQA validation image, no source-provided unanswerable QA, and no OCR/field-inventory/annotation proof of absence.

The controlled NOT_FOUND slice is stronger for abstention testing because each image is rendered from a known field inventory and the queried field/value is excluded from `present_fields` and `rendered_text`.

## Per-Model Capability Summary

| model | slice | capability | count | strict_exact_match | answer_in_output | avg_latency_s | formatting_only_failures | both_failed |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-VL 3B Instruct | controlled_notfound_v0 | not_found | 50 | 1.0000 | 1.0000 | 0.4486 | 0 | 0 |
| Qwen2.5-VL 3B Instruct | old_docminibench_v0 | chart_numeric | 20 | 0.5000 | 0.6000 | 0.5459 | 2 | 8 |
| Qwen2.5-VL 3B Instruct | old_docminibench_v0 | domain_terms | 20 | 0.9000 | 0.6500 | 1.2375 | 1 | 1 |
| Qwen2.5-VL 3B Instruct | old_docminibench_v0 | layout_binding | 20 | 0.5000 | 0.7000 | 1.6999 | 4 | 6 |
| Qwen2.5-VL 3B Instruct | old_docminibench_v0 | not_found | 20 | 1.0000 | 1.0000 | 1.3084 | 0 | 0 |
| Qwen2.5-VL 3B Instruct | old_docminibench_v0 | ocr_exact | 20 | 0.9500 | 0.9500 | 1.2738 | 0 | 1 |
| Qwen2.5-VL 3B Instruct | old_docminibench_v0 | table_lookup | 20 | 1.0000 | 1.0000 | 1.1700 | 0 | 0 |
| SmolVLM 500M Instruct | controlled_notfound_v0 | not_found | 50 | 0.0000 | 0.0000 | 0.4142 | 0 | 50 |
| SmolVLM 500M Instruct | old_docminibench_v0 | chart_numeric | 20 | 0.4000 | 0.4000 | 0.6243 | 0 | 12 |
| SmolVLM 500M Instruct | old_docminibench_v0 | domain_terms | 20 | 0.8000 | 0.5000 | 0.4366 | 0 | 4 |
| SmolVLM 500M Instruct | old_docminibench_v0 | layout_binding | 20 | 0.1500 | 0.6000 | 0.5269 | 9 | 8 |
| SmolVLM 500M Instruct | old_docminibench_v0 | not_found | 20 | 0.0000 | 0.0000 | 0.4230 | 0 | 20 |
| SmolVLM 500M Instruct | old_docminibench_v0 | ocr_exact | 20 | 0.3500 | 0.6500 | 0.4233 | 6 | 7 |
| SmolVLM 500M Instruct | old_docminibench_v0 | table_lookup | 20 | 0.6500 | 0.8000 | 0.4275 | 3 | 4 |
| SmolVLM2 500M Video Instruct | controlled_notfound_v0 | not_found | 50 | 0.0200 | 0.0200 | 0.7372 | 0 | 49 |
| SmolVLM2 500M Video Instruct | old_docminibench_v0 | chart_numeric | 20 | 0.3000 | 0.3000 | 0.4491 | 0 | 14 |
| SmolVLM2 500M Video Instruct | old_docminibench_v0 | domain_terms | 20 | 0.7500 | 0.4500 | 0.4440 | 0 | 5 |
| SmolVLM2 500M Video Instruct | old_docminibench_v0 | layout_binding | 20 | 0.0500 | 0.5500 | 0.4943 | 10 | 9 |
| SmolVLM2 500M Video Instruct | old_docminibench_v0 | not_found | 20 | 0.0000 | 0.0000 | 0.4977 | 0 | 20 |
| SmolVLM2 500M Video Instruct | old_docminibench_v0 | ocr_exact | 20 | 0.3500 | 0.6500 | 0.3887 | 6 | 7 |
| SmolVLM2 500M Video Instruct | old_docminibench_v0 | table_lookup | 20 | 0.7500 | 0.9000 | 0.4049 | 3 | 2 |

## Old vs Controlled NOT_FOUND

| model | slice | rows | strict_exact_match | answer_in_output | both_failed |
| --- | --- | ---: | ---: | ---: | ---: |
| Qwen2.5-VL 3B Instruct | controlled_notfound_v0 | 50 | 1.0000 | 1.0000 | 0 |
| Qwen2.5-VL 3B Instruct | old_docminibench_v0 | 20 | 1.0000 | 1.0000 | 0 |
| SmolVLM 500M Instruct | controlled_notfound_v0 | 50 | 0.0000 | 0.0000 | 50 |
| SmolVLM 500M Instruct | old_docminibench_v0 | 20 | 0.0000 | 0.0000 | 20 |
| SmolVLM2 500M Video Instruct | controlled_notfound_v0 | 50 | 0.0200 | 0.0200 | 49 |
| SmolVLM2 500M Video Instruct | old_docminibench_v0 | 20 | 0.0000 | 0.0000 | 20 |

## Formatting-Only Failures

| model | slice | capability | id | gold | parsed_answer |
| --- | --- | --- | --- | --- | --- |
| SmolVLM 500M Instruct | old_docminibench_v0 | layout_binding | docvqa-layout_binding-001 | university of california; university of california, san diego | University of California, San Diego. |
| SmolVLM 500M Instruct | old_docminibench_v0 | layout_binding | docvqa-layout_binding-007 | cigfil limited | CIGFIL LIMITED, CHENNAI. |
| SmolVLM 500M Instruct | old_docminibench_v0 | layout_binding | docvqa-layout_binding-008 | ITC Limited | ITC Limited. |
| SmolVLM 500M Instruct | old_docminibench_v0 | layout_binding | docvqa-layout_binding-009 | ITC LIMITED | ITC Limited. |
| SmolVLM 500M Instruct | old_docminibench_v0 | layout_binding | docvqa-layout_binding-014 | meharry medical college | Meharry Medical College. |
| SmolVLM 500M Instruct | old_docminibench_v0 | layout_binding | docvqa-layout_binding-015 | February 24; February 24 .1966; February 24 1966 | February 24, 1966. |
| SmolVLM 500M Instruct | old_docminibench_v0 | layout_binding | docvqa-layout_binding-017 | ITC Limited | ITC Limited. |
| SmolVLM 500M Instruct | old_docminibench_v0 | layout_binding | docvqa-layout_binding-018 | itc | ITC Limited. |
| SmolVLM 500M Instruct | old_docminibench_v0 | layout_binding | docvqa-layout_binding-019 | scientists; scientists themselves | The persons most capable of evaluating a scientific field are scientists. |
| SmolVLM 500M Instruct | old_docminibench_v0 | ocr_exact | docvqa-ocr_exact-002 | san diego | CALIFORNIA, SAN DIEGO. |
| SmolVLM 500M Instruct | old_docminibench_v0 | ocr_exact | docvqa-ocr_exact-007 | As competitor's joined the price war | As competitor's joined the price war. |
| SmolVLM 500M Instruct | old_docminibench_v0 | ocr_exact | docvqa-ocr_exact-012 | bengaluru; in Bengaluru | Bengaluru. |

## Representative Both-Failed Cases

| model | slice | capability | id | gold | parsed_answer | failure_type |
| --- | --- | --- | --- | --- | --- | --- |
| SmolVLM 500M Instruct | old_docminibench_v0 | chart_numeric | chartqa-chart_numeric-001 | 14 | 10. | numeric_mismatch |
| SmolVLM 500M Instruct | old_docminibench_v0 | domain_terms | docvqa-domain_terms-002 | 51092 5213 | EITZS 26015 | exact_mismatch |
| SmolVLM 500M Instruct | old_docminibench_v0 | layout_binding | docvqa-layout_binding-003 | 1128 SIXTEENTH ST., N. W., WASHINGTON, D. C. 20036 | 112B 16TH ST. N.V., WASHINGTON, D.C. 20036. | exact_mismatch |
| SmolVLM 500M Instruct | old_docminibench_v0 | not_found | docvqa-not_found-001 | not found; not answerable from the document; NOT_FOUND | 1980. | false_answer_on_unanswerable |
| SmolVLM 500M Instruct | old_docminibench_v0 | ocr_exact | docvqa-ocr_exact-001 | 0.28 | 0.2. | numeric_mismatch |
| SmolVLM 500M Instruct | old_docminibench_v0 | table_lookup | docvqa-table_lookup-010 | 3 | 2. | numeric_mismatch |
| SmolVLM2 500M Video Instruct | old_docminibench_v0 | chart_numeric | chartqa-chart_numeric-001 | 14 | 10. | numeric_mismatch |
| SmolVLM2 500M Video Instruct | old_docminibench_v0 | domain_terms | docvqa-domain_terms-001 | 62272 | 2565-16. | numeric_mismatch |
| SmolVLM2 500M Video Instruct | old_docminibench_v0 | layout_binding | docvqa-layout_binding-003 | 1128 SIXTEENTH ST., N. W., WASHINGTON, D. C. 20036 | 1286TH ST., N.V., WASHINGTON, D.C. 20036 | exact_mismatch |
| SmolVLM2 500M Video Instruct | old_docminibench_v0 | not_found | docvqa-not_found-001 | not found; not answerable from the document; NOT_FOUND | 1234567890. | false_answer_on_unanswerable |
| SmolVLM2 500M Video Instruct | old_docminibench_v0 | ocr_exact | docvqa-ocr_exact-001 | 0.28 | 0.22. | numeric_mismatch |
| SmolVLM2 500M Video Instruct | old_docminibench_v0 | table_lookup | docvqa-table_lookup-016 | 10,000 | 3,58,000 | numeric_mismatch |
| SmolVLM 500M Instruct | controlled_notfound_v0 | not_found | notfound-controlled-v0-001 | NOT_FOUND | 8821. | false_answer_on_unanswerable |
| SmolVLM2 500M Video Instruct | controlled_notfound_v0 | not_found | notfound-controlled-v0-001 | NOT_FOUND | 8821. | false_answer_on_unanswerable |
| Qwen2.5-VL 3B Instruct | old_docminibench_v0 | chart_numeric | chartqa-chart_numeric-001 | 14 | 13 | numeric_mismatch |
| Qwen2.5-VL 3B Instruct | old_docminibench_v0 | domain_terms | docvqa-domain_terms-003 | gurrj@war.wyeth.com | (gurrf@war.wyeth.com) | exact_mismatch |
| Qwen2.5-VL 3B Instruct | old_docminibench_v0 | layout_binding | docvqa-layout_binding-002 | itc limited | !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! | exact_mismatch |
| Qwen2.5-VL 3B Instruct | old_docminibench_v0 | ocr_exact | docvqa-ocr_exact-004 | aashirvaad | !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! | exact_mismatch |
