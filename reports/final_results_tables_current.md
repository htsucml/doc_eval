# Final Results Tables

All headline rows use strict NOT_FOUND prompt metadata. Qwen2.5-VL-3B is shown only as a `>1B reference ceiling`. OOD sanity is non-document sanity only.

## DocMiniBench-v0 Overall
| model | rows | strict_exact | answer_in_output | not_found_false_answer_rate | avg_latency_s | output |
| --- | --- | --- | --- | --- | --- | --- |
| smolvlm_500m | 120 | 0.4250 | 0.5000 | 1.0000 | 0.4794 | outputs/smolvlm_500m_docminibench_v0_strict_preds.jsonl |
| smolvlm2_500m_video | 120 | 0.4417 | 0.4750 | 1.0000 | 0.4863 | outputs/smolvlm2_500m_video_docminibench_v0_strict_preds.jsonl |
| qwen2_5_vl_3b_instruct | 120 | 0.8083 | 0.8167 | 0.0000 | 1.2059 | outputs/qwen2_5_vl_3b_instruct_docminibench_v0_preds.jsonl |

## DocMiniBench-v0 Answerable Only
| model | answerable_rows | answerable_strict_exact | answerable_answer_in_output | over_abstention_rate | avg_latency_s |
| --- | --- | --- | --- | --- | --- |
| smolvlm_500m | 100 | 0.5100 | 0.6000 | 0.0000 | 0.4913 |
| smolvlm2_500m_video | 100 | 0.5300 | 0.5700 | 0.0000 | 0.4549 |
| qwen2_5_vl_3b_instruct | 100 | 0.7700 | 0.7800 | 0.0400 | 1.1854 |

## Controlled Synthetic NOT_FOUND
| model | rows | strict_exact | answer_in_output | not_found_false_answer_rate | avg_latency_s | output |
| --- | --- | --- | --- | --- | --- | --- |
| smolvlm_500m | 50 | 0.0000 | 0.0000 | 1.0000 | 0.4142 | outputs/smolvlm_500m_notfound_controlled_v0_preds.jsonl |
| smolvlm2_500m_video | 50 | 0.0200 | 0.0200 | 0.9800 | 0.7372 | outputs/smolvlm2_500m_video_notfound_controlled_v0_preds.jsonl |
| qwen2_5_vl_3b_instruct | 50 | 1.0000 | 1.0000 | 0.0000 | 0.4486 | outputs/qwen2_5_vl_3b_instruct_notfound_controlled_v0_preds.jsonl |

## Manual Real-Doc NOT_FOUND
| model | rows | strict_exact | answer_in_output | not_found_false_answer_rate | avg_latency_s | output |
| --- | --- | --- | --- | --- | --- | --- |
| smolvlm_500m | 85 | 0.0471 | 0.0471 | 0.9529 | 0.5221 | outputs/smolvlm_500m_docvqa_manual_notfound_combined_expanded_v0_preds.jsonl |
| smolvlm2_500m_video | 85 | 0.0000 | 0.0000 | 1.0000 | 0.6752 | outputs/smolvlm2_500m_video_docvqa_manual_notfound_combined_expanded_v0_preds.jsonl |
| qwen2_5_vl_3b_instruct | 85 | 0.9647 | 0.9647 | 0.0353 | 1.2480 | outputs/qwen2_5_vl_3b_instruct_docvqa_manual_notfound_combined_expanded_v0_preds.jsonl |

## OOD Sanity NOT_FOUND
| model | rows | strict_exact | answer_in_output | not_found_false_answer_rate | avg_latency_s | output |
| --- | --- | --- | --- | --- | --- | --- |
| smolvlm_500m | 20 | 0.0000 | 0.0000 | 1.0000 | 0.6130 | outputs/smolvlm_500m_notfound_ood_sanity_v0_preds.jsonl |
| smolvlm2_500m_video | 20 | 0.0000 | 0.0000 | 1.0000 | 0.8930 | outputs/smolvlm2_500m_video_notfound_ood_sanity_v0_preds.jsonl |
| qwen2_5_vl_3b_instruct | 20 | 1.0000 | 1.0000 | 0.0000 | 0.3702 | outputs/qwen2_5_vl_3b_instruct_notfound_ood_sanity_v0_preds.jsonl |

## Per-Capability DocMiniBench-v0

### `smolvlm_500m`
| capability | count | exact | answer_in_output | not_found_false_answer_rate | over_abstention_rate | latency |
| --- | --- | --- | --- | --- | --- | --- |
| chart_numeric | 20 | 0.3500 | 0.4000 | - | 0.0000 | 0.6465 |
| domain_terms | 20 | 0.8000 | 0.5000 | - | 0.0000 | 0.4488 |
| layout_binding | 20 | 0.2000 | 0.5500 | - | 0.0000 | 0.5085 |
| not_found | 20 | 0.0000 | 0.0000 | 1.0000 | - | 0.4197 |
| ocr_exact | 20 | 0.4000 | 0.7000 | - | 0.0000 | 0.4334 |
| table_lookup | 20 | 0.8000 | 0.8500 | - | 0.0000 | 0.4191 |

### `smolvlm2_500m_video`
| capability | count | exact | answer_in_output | not_found_false_answer_rate | over_abstention_rate | latency |
| --- | --- | --- | --- | --- | --- | --- |
| chart_numeric | 20 | 0.3000 | 0.3000 | - | 0.0000 | 0.4743 |
| domain_terms | 20 | 0.7500 | 0.4500 | - | 0.0000 | 0.4245 |
| layout_binding | 20 | 0.4000 | 0.5500 | - | 0.0000 | 0.5257 |
| not_found | 20 | 0.0000 | 0.0000 | 1.0000 | - | 0.6437 |
| ocr_exact | 20 | 0.4500 | 0.6500 | - | 0.0000 | 0.4634 |
| table_lookup | 20 | 0.7500 | 0.9000 | - | 0.0000 | 0.3865 |

### `qwen2_5_vl_3b_instruct`
| capability | count | exact | answer_in_output | not_found_false_answer_rate | over_abstention_rate | latency |
| --- | --- | --- | --- | --- | --- | --- |
| chart_numeric | 20 | 0.5000 | 0.6000 | - | 0.2000 | 0.5459 |
| domain_terms | 20 | 0.9000 | 0.6500 | - | 0.0000 | 1.2375 |
| layout_binding | 20 | 0.5000 | 0.7000 | - | 0.0000 | 1.6999 |
| not_found | 20 | 1.0000 | 1.0000 | 0.0000 | - | 1.3084 |
| ocr_exact | 20 | 0.9500 | 0.9500 | - | 0.0000 | 1.2738 |
| table_lookup | 20 | 1.0000 | 1.0000 | - | 0.0000 | 1.1700 |
