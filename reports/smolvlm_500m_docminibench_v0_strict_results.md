# Evaluation Summary

## Overall Metrics

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| overall | 120 | 0.4250 | 0.5000 | 0.5334 | 51 | 0.7347 | 49 | 1.0000 | 20 | 0.0000 | 0.4794 |

## By Capability

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| chart_numeric | 20 | 0.3500 | 0.4000 | 0.1667 | 4 | 0.4375 | 16 | - | 0 | 0.0000 | 0.6465 |
| domain_terms | 20 | 0.8000 | 0.5000 | 0.7112 | 11 | 1.0000 | 9 | - | 0 | 0.0000 | 0.4488 |
| layout_binding | 20 | 0.2000 | 0.5500 | 0.4748 | 19 | 1.0000 | 1 | - | 0 | 0.0000 | 0.5085 |
| not_found | 20 | 0.0000 | 0.0000 | - | 0 | - | 0 | 1.0000 | 20 | 0.0000 | 0.4197 |
| ocr_exact | 20 | 0.4000 | 0.7000 | 0.4309 | 11 | 0.7778 | 9 | - | 0 | 0.0000 | 0.4334 |
| table_lookup | 20 | 0.8000 | 0.8500 | 0.8254 | 6 | 0.8571 | 14 | - | 0 | 0.0000 | 0.4191 |

## By Answer Type

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| abstain | 20 | 0.0000 | 0.0000 | - | 0 | - | 0 | 1.0000 | 20 | 0.0000 | 0.4197 |
| code | 11 | 0.6364 | 0.0909 | 0.7112 | 11 | - | 0 | - | 0 | 0.0000 | 0.4831 |
| currency | 3 | 0.6667 | 0.6667 | - | 0 | 0.6667 | 3 | - | 0 | 0.0000 | 0.6103 |
| float | 7 | 0.7143 | 0.7143 | - | 0 | 0.7143 | 7 | - | 0 | 0.0000 | 0.4657 |
| integer | 23 | 0.9565 | 0.9565 | - | 0 | 0.9565 | 23 | - | 0 | 0.0000 | 0.3708 |
| number | 16 | 0.4375 | 0.4375 | - | 0 | 0.4375 | 16 | - | 0 | 0.0000 | 0.7342 |
| short_text | 40 | 0.2000 | 0.5750 | 0.4845 | 40 | - | 0 | - | 0 | 0.0000 | 0.4612 |

## Calibration Buckets

No confidence values available.
