# Evaluation Summary

## Overall Metrics

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| overall | 120 | 0.8083 | 0.8167 | 0.7649 | 51 | 0.8776 | 49 | 0.0000 | 20 | 0.0000 | 1.2059 |

## By Capability

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| chart_numeric | 20 | 0.5000 | 0.6000 | 0.2500 | 4 | 0.6250 | 16 | - | 0 | 0.0000 | 0.5459 |
| domain_terms | 20 | 0.9000 | 0.6500 | 0.9034 | 11 | 1.0000 | 9 | - | 0 | 0.0000 | 1.2375 |
| layout_binding | 20 | 0.5000 | 0.7000 | 0.6355 | 19 | 1.0000 | 1 | - | 0 | 0.0000 | 1.6999 |
| not_found | 20 | 1.0000 | 1.0000 | - | 0 | - | 0 | 0.0000 | 20 | 0.0000 | 1.3084 |
| ocr_exact | 20 | 0.9500 | 0.9500 | 0.9091 | 11 | 1.0000 | 9 | - | 0 | 0.0000 | 1.2738 |
| table_lookup | 20 | 1.0000 | 1.0000 | 1.0000 | 6 | 1.0000 | 14 | - | 0 | 0.0000 | 1.1700 |

## By Answer Type

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| abstain | 20 | 1.0000 | 1.0000 | - | 0 | - | 0 | 0.0000 | 20 | 0.0000 | 1.3084 |
| code | 11 | 0.8182 | 0.3636 | 0.9034 | 11 | - | 0 | - | 0 | 0.0000 | 1.3829 |
| currency | 3 | 1.0000 | 1.0000 | - | 0 | 1.0000 | 3 | - | 0 | 0.0000 | 1.0882 |
| float | 7 | 1.0000 | 1.0000 | - | 0 | 1.0000 | 7 | - | 0 | 0.0000 | 1.2460 |
| integer | 23 | 1.0000 | 1.0000 | - | 0 | 1.0000 | 23 | - | 0 | 0.0000 | 1.1956 |
| number | 16 | 0.5625 | 0.5625 | - | 0 | 0.6250 | 16 | - | 0 | 0.0000 | 0.6134 |
| short_text | 40 | 0.6500 | 0.8000 | 0.7268 | 40 | - | 0 | - | 0 | 0.0000 | 1.3508 |

## Calibration Buckets

No confidence values available.
