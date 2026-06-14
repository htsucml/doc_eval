# Evaluation Summary

## Overall Metrics

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| overall | 120 | 0.5083 | 0.5250 | 0.5698 | 51 | 0.6735 | 49 | 0.7000 | 20 | 0.0000 | 0.5418 |

## By Capability

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| chart_numeric | 20 | 0.3000 | 0.3000 | 0.0000 | 4 | 0.4375 | 16 | - | 0 | 0.0000 | 0.5709 |
| domain_terms | 20 | 0.7500 | 0.4500 | 0.6864 | 11 | 0.8889 | 9 | - | 0 | 0.0000 | 0.5309 |
| layout_binding | 20 | 0.4500 | 0.6000 | 0.6025 | 19 | 1.0000 | 1 | - | 0 | 0.0000 | 0.6007 |
| not_found | 20 | 0.3000 | 0.3000 | - | 0 | - | 0 | 0.7000 | 20 | 0.0000 | 0.5665 |
| ocr_exact | 20 | 0.6000 | 0.7000 | 0.4545 | 11 | 0.7778 | 9 | - | 0 | 0.0000 | 0.5410 |
| table_lookup | 20 | 0.6500 | 0.8000 | 0.8435 | 6 | 0.7143 | 14 | - | 0 | 0.0000 | 0.4410 |

## By Answer Type

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| abstain | 20 | 0.3000 | 0.3000 | - | 0 | - | 0 | 0.7000 | 20 | 0.0000 | 0.5665 |
| code | 11 | 0.6364 | 0.0909 | 0.6864 | 11 | - | 0 | - | 0 | 0.0000 | 0.5146 |
| currency | 3 | 0.6667 | 0.6667 | - | 0 | 0.6667 | 3 | - | 0 | 0.0000 | 0.5114 |
| float | 7 | 0.7143 | 0.7143 | - | 0 | 0.7143 | 7 | - | 0 | 0.0000 | 0.5157 |
| integer | 23 | 0.8261 | 0.8261 | - | 0 | 0.8261 | 23 | - | 0 | 0.0000 | 0.4384 |
| number | 16 | 0.3750 | 0.3750 | - | 0 | 0.4375 | 16 | - | 0 | 0.0000 | 0.6358 |
| short_text | 40 | 0.4000 | 0.6000 | 0.5377 | 40 | - | 0 | - | 0 | 0.0000 | 0.5657 |

## Calibration Buckets

No confidence values available.
