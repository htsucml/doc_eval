# Evaluation Summary

## Overall Metrics

| slice | count | exact_match | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| overall | 120 | 0.1667 | 0.0000 | 51 | 0.0000 | 49 | - | 0 | 0.0000 | 0.0100 |

## By Capability

| slice | count | exact_match | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| chart_numeric | 20 | 0.0000 | 0.0000 | 4 | 0.0000 | 16 | - | 0 | 0.0000 | 0.0100 |
| domain_terms | 20 | 0.0000 | 0.0000 | 11 | 0.0000 | 9 | - | 0 | 0.0000 | 0.0100 |
| layout_binding | 20 | 0.0000 | 0.0000 | 19 | 0.0000 | 1 | - | 0 | 0.0000 | 0.0100 |
| not_found | 20 | 1.0000 | - | 0 | - | 0 | - | 0 | 0.0000 | 0.0100 |
| ocr_exact | 20 | 0.0000 | 0.0000 | 11 | 0.0000 | 9 | - | 0 | 0.0000 | 0.0100 |
| table_lookup | 20 | 0.0000 | 0.0000 | 6 | 0.0000 | 14 | - | 0 | 0.0000 | 0.0100 |

## By Answer Type

| slice | count | exact_match | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| abstain | 20 | 1.0000 | - | 0 | - | 0 | - | 0 | 0.0000 | 0.0100 |
| code | 11 | 0.0000 | 0.0000 | 11 | - | 0 | - | 0 | 0.0000 | 0.0100 |
| currency | 3 | 0.0000 | - | 0 | 0.0000 | 3 | - | 0 | 0.0000 | 0.0100 |
| float | 7 | 0.0000 | - | 0 | 0.0000 | 7 | - | 0 | 0.0000 | 0.0100 |
| integer | 23 | 0.0000 | - | 0 | 0.0000 | 23 | - | 0 | 0.0000 | 0.0100 |
| number | 16 | 0.0000 | - | 0 | 0.0000 | 16 | - | 0 | 0.0000 | 0.0100 |
| short_text | 40 | 0.0000 | 0.0000 | 40 | - | 0 | - | 0 | 0.0000 | 0.0100 |

## Calibration Buckets

| bucket | count | avg_confidence | avg_accuracy | gap | bucket_ece |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0.4-0.6 | 120 | 0.5000 | 0.1667 | 0.3333 | 0.3333 |
