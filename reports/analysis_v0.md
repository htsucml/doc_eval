# Analysis v0

## Benchmark Composition

`DocMiniBench-v0` contains 120 real Hugging Face-derived rows: 20 each for chart numeric QA, domain terms, layout binding, unanswerable/NOT_FOUND, OCR exact, and table lookup. Answer types are short_text, integer, abstain, number, code, float, and currency.

## Strongest Model

SmolVLM 500M is the strongest v0 model overall: strict exact_match 0.3917 and answer_in_output 0.4917. SmolVLM2 500M Video is close but lower overall at strict exact_match 0.3667 and answer_in_output 0.4750.

## Weakest Slices

The weakest slice is `not_found`: both models answer all 20 unanswerable prompts with concrete values, producing 0.0000 strict exact_match and 1.0000 false-answer rate.

`layout_binding` is also weak under strict exact_match. SmolVLM gets 0.1500 strict but 0.6000 containment, and SmolVLM2 gets 0.0500 strict but 0.5500 containment. Many outputs contain the right span plus punctuation, casing, or extra context, so strict exact_match is intentionally conservative for these generative VLMs.

`chart_numeric` remains weak for both models, especially SmolVLM2. Errors include reading a chart value instead of computing a requested difference or comparison.

## Representative Failures

SmolVLM on `chartqa-chart_numeric-002`: gold `0.57`, output `103.7.`. The model copied one visible value rather than computing the difference.

SmolVLM on `docvqa-layout_binding-001`: gold includes `university of california, san diego`, output `University of California, San Diego.`. Strict exact_match fails, containment passes.

SmolVLM2 on `docvqa-not_found-001`: gold `NOT_FOUND`, output `1234567890.`. This is a false answer on an unanswerable document question.

SmolVLM2 on `docvqa-table_lookup-003`: gold includes `lee a. waller`, output `Lee A. Waller, TRRF Vice President.`. Strict exact_match fails, containment passes.

## Knowledge Gap

The main gap is abstention discipline. The models appear optimized to produce a plausible document value even when the requested field is absent. A second gap is metric sensitivity: strict exact_match undercounts useful generative answers, while containment can expose cases where the answer is present but not formatted as the final value.

## Improvement Plan

Keep strict exact_match as the headline metric, but report answer_in_output beside it for generative VLMs.

Prioritize an abstention-specific intervention next: negative examples, confidence calibration, or a small classifier/reranker over retrieved OCR spans before accepting a generated answer.

Add OCR text to the real benchmark rows if OCR-assisted prompting is evaluated. The current real benchmark metadata has no `ocr_text`, so an OCR-assisted prompt would not actually add evidence yet.

Use targeted chart/table decomposition only after abstention is under control, because hallucinated false answers are the highest-risk product failure in this v0 run.
