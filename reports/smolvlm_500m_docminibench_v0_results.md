# Evaluation Summary

## Overall Metrics

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| overall | 120 | 0.3917 | 0.4917 | 0.5290 | 51 | 0.7143 | 49 | 1.0000 | 20 | 0.0000 | 0.4769 |

## By Capability

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| chart_numeric | 20 | 0.4000 | 0.4000 | 0.0000 | 4 | 0.5000 | 16 | - | 0 | 0.0000 | 0.6243 |
| domain_terms | 20 | 0.8000 | 0.5000 | 0.7112 | 11 | 1.0000 | 9 | - | 0 | 0.0000 | 0.4366 |
| layout_binding | 20 | 0.1500 | 0.6000 | 0.4680 | 19 | 1.0000 | 1 | - | 0 | 0.0000 | 0.5269 |
| not_found | 20 | 0.0000 | 0.0000 | - | 0 | - | 0 | 1.0000 | 20 | 0.0000 | 0.4230 |
| ocr_exact | 20 | 0.3500 | 0.6500 | 0.5198 | 11 | 0.6667 | 9 | - | 0 | 0.0000 | 0.4233 |
| table_lookup | 20 | 0.6500 | 0.8000 | 0.7579 | 6 | 0.7857 | 14 | - | 0 | 0.0000 | 0.4275 |

## By Answer Type

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| abstain | 20 | 0.0000 | 0.0000 | - | 0 | - | 0 | 1.0000 | 20 | 0.0000 | 0.4230 |
| code | 11 | 0.6364 | 0.0909 | 0.7112 | 11 | - | 0 | - | 0 | 0.0000 | 0.4445 |
| currency | 3 | 1.0000 | 1.0000 | - | 0 | 1.0000 | 3 | - | 0 | 0.0000 | 0.4463 |
| float | 7 | 0.5714 | 0.5714 | - | 0 | 0.5714 | 7 | - | 0 | 0.0000 | 0.4940 |
| integer | 23 | 0.8696 | 0.8696 | - | 0 | 0.8696 | 23 | - | 0 | 0.0000 | 0.3942 |
| number | 16 | 0.5000 | 0.5000 | - | 0 | 0.5000 | 16 | - | 0 | 0.0000 | 0.7051 |
| short_text | 40 | 0.1250 | 0.5750 | 0.4789 | 40 | - | 0 | - | 0 | 0.0000 | 0.4685 |

## Calibration Buckets

No confidence values available.
