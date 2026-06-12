# Model Comparison v0

Benchmark: `data/docminibench_v0.jsonl`  
Rows: 120 real_hf rows, 20 each for chart_numeric, domain_terms, layout_binding, not_found, ocr_exact, and table_lookup.  
Device: NVIDIA GeForce RTX 4090, CUDA, torch 2.12.0+cu126.  
Prompt: image-only, final-value instruction, `NOT_FOUND` requested when evidence is absent.  

Strict `exact_match` remains the conservative primary metric. `answer_in_output` is a normalized containment metric for generative VLMs that often return the right value with punctuation or in a sentence. It should be read as supporting evidence, not a replacement for exact match.

## Overall

| model | rows | strict_exact_match | answer_in_output | relaxed_numeric | not_found_false_answer_rate | avg_latency_s | error_rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| SmolVLM 500M Instruct | 120 | 0.3917 | 0.4917 | 0.7143 | 1.0000 | 0.4769 | 0.0000 |
| SmolVLM2 500M Video Instruct | 120 | 0.3667 | 0.4750 | 0.7143 | 1.0000 | 0.4464 | 0.0000 |

## By Capability

| capability | SmolVLM strict | SmolVLM contain | SmolVLM2 strict | SmolVLM2 contain |
| --- | ---: | ---: | ---: | ---: |
| chart_numeric | 0.4000 | 0.4000 | 0.3000 | 0.3000 |
| domain_terms | 0.8000 | 0.5000 | 0.7500 | 0.4500 |
| layout_binding | 0.1500 | 0.6000 | 0.0500 | 0.5500 |
| not_found | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| ocr_exact | 0.3500 | 0.6500 | 0.3500 | 0.6500 |
| table_lookup | 0.6500 | 0.8000 | 0.7500 | 0.9000 |

## Reading

SmolVLM 500M is the strongest overall by strict exact match and containment. SmolVLM2 is slightly faster and stronger on table lookup, but weaker on chart numeric, domain terms, and layout binding strict scoring.

Both models fail closedness: `not_found_false_answer_rate` is 1.0 for both, meaning every unanswerable prompt received a concrete answer instead of `NOT_FOUND`.
