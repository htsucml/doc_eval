# Evaluation Summary

## Overall Metrics

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| overall | 120 | 0.5250 | 0.5417 | 0.4581 | 51 | 0.7347 | 49 | 0.4000 | 20 | 0.0000 | 0.3719 |

## By Capability

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| chart_numeric | 20 | 0.5000 | 0.5000 | 0.0000 | 4 | 0.6250 | 16 | - | 0 | 0.0000 | 0.4104 |
| domain_terms | 20 | 0.5500 | 0.4500 | 0.6528 | 11 | 0.7778 | 9 | - | 0 | 0.0000 | 0.3713 |
| layout_binding | 20 | 0.4500 | 0.5000 | 0.4507 | 19 | 1.0000 | 1 | - | 0 | 0.0000 | 0.3815 |
| not_found | 20 | 0.6000 | 0.6000 | - | 0 | - | 0 | 0.4000 | 20 | 0.0000 | 0.3763 |
| ocr_exact | 20 | 0.3500 | 0.4500 | 0.4545 | 11 | 0.5556 | 9 | - | 0 | 0.0000 | 0.3477 |
| table_lookup | 20 | 0.7000 | 0.7500 | 0.4362 | 6 | 0.9286 | 14 | - | 0 | 0.0000 | 0.3440 |

## By Answer Type

| slice | count | strict_exact_match | answer_in_output | anls | anls_n | relaxed_numeric | numeric_n | not_found_false_answer_rate | not_found_n | error_rate | avg_latency_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| abstain | 20 | 0.6000 | 0.6000 | - | 0 | - | 0 | 0.4000 | 20 | 0.0000 | 0.3763 |
| code | 11 | 0.3636 | 0.1818 | 0.6528 | 11 | - | 0 | - | 0 | 0.0000 | 0.3836 |
| currency | 3 | 0.6667 | 0.6667 | - | 0 | 0.6667 | 3 | - | 0 | 0.0000 | 0.3583 |
| float | 7 | 0.2857 | 0.2857 | - | 0 | 0.7143 | 7 | - | 0 | 0.0000 | 0.3928 |
| integer | 23 | 0.8261 | 0.8261 | - | 0 | 0.8261 | 23 | - | 0 | 0.0000 | 0.3226 |
| number | 16 | 0.6250 | 0.6250 | - | 0 | 0.6250 | 16 | - | 0 | 0.0000 | 0.4433 |
| short_text | 40 | 0.3500 | 0.4500 | 0.4045 | 40 | - | 0 | - | 0 | 0.0000 | 0.3635 |

## Calibration Buckets

No confidence values available.
