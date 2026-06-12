# Evaluation Summary

## Overall Metrics

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| overall | 120 | 0.3667 | 0.4750 | 0.5874 | 51 | 0.7143 | 49 | 1.0000 | 20 | 0.0000 | 0.4464 |

## By Capability

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| chart_numeric | 20 | 0.3000 | 0.3000 | 0.0000 | 4 | 0.4375 | 16 | - | 0 | 0.0000 | 0.4491 |
| domain_terms | 20 | 0.7500 | 0.4500 | 0.6932 | 11 | 0.8889 | 9 | - | 0 | 0.0000 | 0.4440 |
| layout_binding | 20 | 0.0500 | 0.5500 | 0.5616 | 19 | 1.0000 | 1 | - | 0 | 0.0000 | 0.4943 |
| not_found | 20 | 0.0000 | 0.0000 | - | 0 | - | 0 | 1.0000 | 20 | 0.0000 | 0.4977 |
| ocr_exact | 20 | 0.3500 | 0.6500 | 0.6016 | 11 | 0.7778 | 9 | - | 0 | 0.0000 | 0.3887 |
| table_lookup | 20 | 0.7500 | 0.9000 | 0.8408 | 6 | 0.8571 | 14 | - | 0 | 0.0000 | 0.4049 |

## By Answer Type

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| abstain | 20 | 0.0000 | 0.0000 | - | 0 | - | 0 | 1.0000 | 20 | 0.0000 | 0.4977 |
| code | 11 | 0.6364 | 0.0909 | 0.6932 | 11 | - | 0 | - | 0 | 0.0000 | 0.4376 |
| currency | 3 | 1.0000 | 1.0000 | - | 0 | 1.0000 | 3 | - | 0 | 0.0000 | 0.4556 |
| float | 7 | 0.5714 | 0.5714 | - | 0 | 0.7143 | 7 | - | 0 | 0.0000 | 0.4463 |
| integer | 23 | 0.8696 | 0.8696 | - | 0 | 0.8696 | 23 | - | 0 | 0.0000 | 0.3975 |
| number | 16 | 0.3750 | 0.3750 | - | 0 | 0.4375 | 16 | - | 0 | 0.0000 | 0.4902 |
| short_text | 40 | 0.1000 | 0.5750 | 0.5583 | 40 | - | 0 | - | 0 | 0.0000 | 0.4333 |

## Calibration Buckets

No confidence values available.
