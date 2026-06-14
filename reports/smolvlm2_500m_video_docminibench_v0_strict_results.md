# Evaluation Summary

## Overall Metrics

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| overall | 120 | 0.4417 | 0.4750 | 0.5818 | 51 | 0.6735 | 49 | 1.0000 | 20 | 0.0000 | 0.4863 |

## By Capability

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| chart_numeric | 20 | 0.3000 | 0.3000 | 0.2500 | 4 | 0.3750 | 16 | - | 0 | 0.0000 | 0.4743 |
| domain_terms | 20 | 0.7500 | 0.4500 | 0.7071 | 11 | 0.8889 | 9 | - | 0 | 0.0000 | 0.4245 |
| layout_binding | 20 | 0.4000 | 0.5500 | 0.5786 | 19 | 1.0000 | 1 | - | 0 | 0.0000 | 0.5257 |
| not_found | 20 | 0.0000 | 0.0000 | - | 0 | - | 0 | 1.0000 | 20 | 0.0000 | 0.6437 |
| ocr_exact | 20 | 0.4500 | 0.6500 | 0.4398 | 11 | 0.6667 | 9 | - | 0 | 0.0000 | 0.4634 |
| table_lookup | 20 | 0.7500 | 0.9000 | 0.8435 | 6 | 0.8571 | 14 | - | 0 | 0.0000 | 0.3865 |

## By Answer Type

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| abstain | 20 | 0.0000 | 0.0000 | - | 0 | - | 0 | 1.0000 | 20 | 0.0000 | 0.6437 |
| code | 11 | 0.6364 | 0.0909 | 0.7071 | 11 | - | 0 | - | 0 | 0.0000 | 0.4077 |
| currency | 3 | 1.0000 | 1.0000 | - | 0 | 1.0000 | 3 | - | 0 | 0.0000 | 0.4609 |
| float | 7 | 0.5714 | 0.5714 | - | 0 | 0.5714 | 7 | - | 0 | 0.0000 | 0.4279 |
| integer | 23 | 0.8696 | 0.8696 | - | 0 | 0.8696 | 23 | - | 0 | 0.0000 | 0.3791 |
| number | 16 | 0.3125 | 0.3125 | - | 0 | 0.3750 | 16 | - | 0 | 0.0000 | 0.5258 |
| short_text | 40 | 0.3500 | 0.6000 | 0.5473 | 40 | - | 0 | - | 0 | 0.0000 | 0.4873 |

## Calibration Buckets

No confidence values available.
