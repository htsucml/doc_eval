# Tomorrow Action Items

1. Package the report around the verified matrix; use controlled NOT_FOUND as the primary absence benchmark and manual real-doc as auxiliary transfer evidence.
2. In the report, treat the old DocMiniBench-v0 NOT_FOUND slice as exploratory/demoted.
3. Decide whether to run a longer SmolVLM2 500M LoRA sweep with real non-eval document train data; the 50-step synthetic-only PoC improved controlled NOT_FOUND but did not transfer well.
4. If manual real-doc eval needs to be rerun, use the normalized additive copy `data/docvqa_manual_notfound_combined_expanded_v0_eval.jsonl` or update the evaluator to accept `answer/answer_mode` schema directly.
5. Exclude the failed adapted controlled prediction file without `_fixed` from final scoring.
