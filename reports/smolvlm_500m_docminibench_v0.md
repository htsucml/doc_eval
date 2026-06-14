# Evaluation Summary

## Overall Metrics

| slice | count | exact_match | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| overall | 120 | 0.3917 | 0.3927 | 51 | 0.6531 | 49 | 1.0000 | 20 | 0.0000 | 0.6035 |

## By Capability

| slice | count | exact_match | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| chart_numeric | 20 | 0.3500 | 0.0000 | 4 | 0.4375 | 16 | - | 0 | 0.0000 | 0.9867 |
| domain_terms | 20 | 0.8000 | 0.7112 | 11 | 1.0000 | 9 | - | 0 | 0.0000 | 0.4666 |
| layout_binding | 20 | 0.1500 | 0.2763 | 19 | 1.0000 | 1 | - | 0 | 0.0000 | 0.6142 |
| not_found | 20 | 0.0000 | - | 0 | - | 0 | 1.0000 | 20 | 0.0000 | 0.4357 |
| ocr_exact | 20 | 0.5000 | 0.2727 | 11 | 0.7778 | 9 | - | 0 | 0.0000 | 0.5601 |
| table_lookup | 20 | 0.5500 | 0.6587 | 6 | 0.5714 | 14 | - | 0 | 0.0000 | 0.5576 |

## By Answer Type

| slice | count | exact_match | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| abstain | 20 | 0.0000 | - | 0 | - | 0 | 1.0000 | 20 | 0.0000 | 0.4357 |
| code | 11 | 0.6364 | 0.7112 | 11 | - | 0 | - | 0 | 0.0000 | 0.4053 |
| currency | 3 | 1.0000 | - | 0 | 1.0000 | 3 | - | 0 | 0.0000 | 0.3784 |
| float | 7 | 0.7143 | - | 0 | 0.7143 | 7 | - | 0 | 0.0000 | 0.4958 |
| integer | 23 | 0.7391 | - | 0 | 0.7391 | 23 | - | 0 | 0.0000 | 0.5691 |
| number | 16 | 0.4375 | - | 0 | 0.4375 | 16 | - | 0 | 0.0000 | 1.0198 |
| short_text | 40 | 0.2000 | 0.3051 | 40 | - | 0 | - | 0 | 0.0000 | 0.6308 |

## Calibration Buckets

No confidence values available.
