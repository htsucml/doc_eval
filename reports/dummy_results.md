# Evaluation Summary

## Overall Metrics

| slice | count | exact_match | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| overall | 7 | 0.7143 | 1.0000 | 4 | 0.5000 | 2 | 1.0000 | 1 | 0.0000 | 0.0100 |

## By Capability

| slice | count | exact_match | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| chart_numeric | 1 | 1.0000 | 1.0000 | 1 | - | 0 | - | 0 | 0.0000 | 0.0100 |
| domain_terms | 1 | 1.0000 | 1.0000 | 1 | - | 0 | - | 0 | 0.0000 | 0.0100 |
| layout_binding | 1 | 1.0000 | - | 0 | 1.0000 | 1 | - | 0 | 0.0000 | 0.0100 |
| not_found | 1 | 0.0000 | - | 0 | - | 0 | 1.0000 | 1 | 0.0000 | 0.0100 |
| ocr_exact | 1 | 1.0000 | 1.0000 | 1 | - | 0 | - | 0 | 0.0000 | 0.0100 |
| robustness_optional | 1 | 1.0000 | 1.0000 | 1 | - | 0 | - | 0 | 0.0000 | 0.0100 |
| table_lookup | 1 | 0.0000 | - | 0 | 0.0000 | 1 | - | 0 | 0.0000 | 0.0100 |

## By Answer Type

| slice | count | exact_match | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| abstain | 1 | 0.0000 | - | 0 | - | 0 | 1.0000 | 1 | 0.0000 | 0.0100 |
| code | 1 | 1.0000 | 1.0000 | 1 | - | 0 | - | 0 | 0.0000 | 0.0100 |
| currency | 1 | 1.0000 | - | 0 | 1.0000 | 1 | - | 0 | 0.0000 | 0.0100 |
| integer | 1 | 0.0000 | - | 0 | 0.0000 | 1 | - | 0 | 0.0000 | 0.0100 |
| short_text | 3 | 1.0000 | 1.0000 | 3 | - | 0 | - | 0 | 0.0000 | 0.0100 |

## Calibration Buckets

| bucket | count | avg_confidence | avg_accuracy | gap | bucket_ece |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0.6-0.8 | 1 | 0.7600 | 1.0000 | 0.2400 | 0.0343 |
| 0.8-1.0 | 6 | 0.9217 | 0.6667 | 0.2550 | 0.2186 |
