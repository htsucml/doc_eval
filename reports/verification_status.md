# Verification Status

Verification-only pass. No model inference, training, dependency installation, or prediction overwrites were performed.

## Preflight
### `git status --short`
Return code: `0`
```
?? data/docvqa_manual_notfound_combined_expanded_v0.jsonl
?? data/notfound_controlled_v0.jsonl
?? data/notfound_controlled_v0.meta.json
?? data/notfound_controlled_v0_images/
?? data/notfound_ood_sanity_v0.jsonl
?? data/notfound_ood_sanity_v0.meta.json
?? data/notfound_ood_sanity_v0_eval.jsonl
?? data/notfound_ood_sanity_v0_images/
?? doc_eval_git_20260613T073259Z.bundle
?? doc_eval_git_20260613T141341Z.bundle
?? tmp_audit_pack/
```

### `git log --oneline -12`
Return code: `0`
```
ccb48ad Add controlled not-found evaluation support
5ca7f7d Fix handoff commit hash
3e72551 Record v0 handoff commit hash
d52d034 Add v0 model comparison analysis
4de48d5 Add HF DocMiniBench v0 builder and manifest
7588d47 Pin RunPod CUDA 12 PyTorch setup
308184f Add RunPod reproducibility infrastructure
e73d27a Ignore local worktree and pycache artifacts
555c207 Merge branch 'feat/gpu-smoke-smol'
643d1eb Merge branch 'feat/improvement-poc'
40adb11 Merge branch 'feat/metrics-analysis'
0fb492a Merge branch 'feat/dataset-v0'
```

### `pytest -q`
Return code: `127`
```
/bin/sh: 1: pytest: not found
```

### `.venv/bin/python -m pytest -q`
Return code: `0`
```
...............................                                          [100%]
31 passed in 4.67s
```

### `git diff --check`
Return code: `0`
```

```

## Relevant File Inventory
Total files under `data/`, `outputs/`, `reports/`, `configs/`: `257`

## Dataset Validation
### `data/docminibench_v0.jsonl`
- Rows: `120`
- Capability counts: `{'chart_numeric': 20, 'domain_terms': 20, 'layout_binding': 20, 'not_found': 20, 'ocr_exact': 20, 'table_lookup': 20}`
- Answer/answer_mode schema: `{'answers,answer_type': 120}`
- Answer mode/type counts: `{'number': 16, 'short_text': 40, 'integer': 23, 'code': 11, 'abstain': 20, 'float': 7, 'currency': 3}`
- Unique images: `100`
- Missing images: `0`
- Image hash checks: `0/0` matched; mismatches `0`
- Absence evidence types: `{}`
- Absence check results: `{}`
- Absence classification: weak/demoted for original NOT_FOUND rows; answerable rows remain primary
- Suitability: primary answerable eval; old NOT_FOUND exploratory only

### `data/notfound_controlled_v0.jsonl`
- Rows: `50`
- Capability counts: `{'not_found': 50}`
- Answer/answer_mode schema: `{'answers,answer_type': 50}`
- Answer mode/type counts: `{'abstain': 50}`
- Unique images: `50`
- Missing images: `0`
- Image hash checks: `50/50` matched; mismatches `0`
- Absence evidence types: `{'controlled_render_negative': 50}`
- Absence check results: `{'True': 50}`
- Absence classification: mechanically verified controlled render negative
- Suitability: primary auxiliary NOT_FOUND eval

### `data/notfound_ood_sanity_v0.jsonl`
- Rows: `20`
- Capability counts: `{'not_found': 20}`
- Answer/answer_mode schema: `{'answers,answer_type': 20}`
- Answer mode/type counts: `{'abstain': 20}`
- Unique images: `20`
- Missing images: `0`
- Image hash checks: `20/20` matched; mismatches `0`
- Absence evidence types: `{'non_document_ood_sanity': 20}`
- Absence check results: `{'True': 20}`
- Absence classification: OOD/non-document sanity
- Suitability: auxiliary OOD sanity only

### `data/docvqa_manual_notfound_combined_expanded_v0.jsonl`
- Rows: `85`
- Capability counts: `{'not_found': 85}`
- Answer/answer_mode schema: `{'answer,answer_mode': 85}`
- Answer mode/type counts: `{'abstain': 85}`
- Unique images: `23`
- Missing images: `0`
- Image hash checks: `85/85` matched; mismatches `0`
- Absence evidence types: `{'assistant_assisted_author_visual_audit': 85}`
- Absence check results: `{'True': 85}`
- Absence classification: assistant-assisted author visual audit; not OCR/mechanical
- Suitability: auxiliary real-doc eval after inference

### `data/notfound_ood_sanity_v0_eval.jsonl`
- Rows: `20`
- Capability counts: `{'not_found': 20}`
- Answer/answer_mode schema: `{'answer,answers,answer_mode,answer_type': 20}`
- Answer mode/type counts: `{'abstain': 20}`
- Unique images: `20`
- Missing images: `0`
- Image hash checks: `20/20` matched; mismatches `0`
- Absence evidence types: `{'non_document_ood_sanity': 20}`
- Absence check results: `{'True': 20}`
- Absence classification: OOD/non-document sanity eval copy
- Suitability: auxiliary OOD sanity only

### `data/fixtures/docminibench_sample.jsonl`
- Rows: `7`
- Capability counts: `{'ocr_exact': 1, 'layout_binding': 1, 'table_lookup': 1, 'chart_numeric': 1, 'domain_terms': 1, 'not_found': 1, 'robustness_optional': 1}`
- Answer/answer_mode schema: `{'answers,answer_type': 7}`
- Answer mode/type counts: `{'short_text': 3, 'currency': 1, 'integer': 1, 'code': 1, 'abstain': 1}`
- Unique images: `3`
- Missing images: `0`
- Image hash checks: `0/0` matched; mismatches `0`
- Absence evidence types: `{}`
- Absence check results: `{}`
- Absence classification: fixture
- Suitability: test fixture only

## Output Validation And Prompt Provenance
| output | model | benchmark | run_id | config | meta_instruction | row_prompt | prompt_status | log_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| outputs/dummy_docminibench_v0.jsonl | dummy | data/docminibench_v0.jsonl | dummy-3b4b92d7 | configs/eval.yaml | False | False | prompt_config_unverified | strict_config_proven_in_log |
| outputs/dummy_preds.jsonl | dummy | data/fixtures/docminibench_sample.jsonl | dummy-079f3656 | configs/eval.yaml | False | False | prompt_config_unverified | strict_config_proven_in_log |
| outputs/qwen2_5_vl_3b_instruct_docminibench_v0_preds.jsonl | qwen2_5_vl_3b_instruct | data/docminibench_v0.jsonl | qwen2_5_vl_3b_instruct-b29b3fce | configs/eval_not_found_strict.yaml | True | False | prompt_verified | log_links_output_but_not_full_config_command |
| outputs/qwen2_5_vl_3b_instruct_notfound_controlled_v0_preds.jsonl | qwen2_5_vl_3b_instruct | data/notfound_controlled_v0.jsonl | qwen2_5_vl_3b_instruct-7cf4930e | configs/eval_not_found_strict.yaml | True | False | prompt_verified | log_links_output_but_not_full_config_command |
| outputs/smolvlm2_500m_video_docminibench_v0_preds.jsonl | smolvlm2_500m_video | data/docminibench_v0.jsonl | smolvlm2_500m_video-8a3b7a01 | configs/eval.yaml | False | False | prompt_config_unverified | strict_config_proven_in_log |
| outputs/smolvlm2_500m_video_notfound_controlled_v0_preds.jsonl | smolvlm2_500m_video | data/notfound_controlled_v0.jsonl | smolvlm2_500m_video-f88fcc12 | configs/eval_not_found_strict.yaml | True | False | prompt_verified | log_links_output_but_not_full_config_command |
| outputs/smolvlm_500m_docminibench_v0_preds.jsonl | smolvlm_500m | data/docminibench_v0.jsonl | smolvlm_500m-108fa3a2 | configs/eval.yaml | False | False | prompt_config_unverified | strict_config_proven_in_log |
| outputs/smolvlm_500m_not_found_strict_poc_preds.jsonl | smolvlm_500m | data/docminibench_v0.jsonl | smolvlm_500m-9db4c341 | configs/eval_not_found_strict.yaml | True | False | prompt_verified | strict_config_proven_in_log |
| outputs/smolvlm_500m_notfound_controlled_v0_preds.jsonl | smolvlm_500m | data/notfound_controlled_v0.jsonl | smolvlm_500m-772115f1 | configs/eval_not_found_strict.yaml | True | False | prompt_verified | log_links_output_but_not_full_config_command |
| outputs/smolvlm_500m_smoke_preds.jsonl | smolvlm_500m | data/fixtures/docminibench_sample.jsonl | smolvlm_500m-7076ae4f | configs/eval.yaml | False | False | prompt_config_unverified | strict_config_proven_in_log |

## Known Caveats
- System `pytest -q` is unavailable on PATH; `.venv/bin/python -m pytest -q` passes.
- Older SmolVLM DocMiniBench-v0 outputs use `configs/eval.yaml`; they are prompt-config unverified for strict abstention claims.
- Prediction rows store `prompt_mode` but not full prompt text. Newer metadata stores `answer_instruction`; row-level prompt text is absent.
- Logs generally record stdout and prediction paths, not full original commands; strict prompt proof mostly comes from metadata.
- Manual real-doc NOT_FOUND and OOD sanity have no prediction outputs yet.

## Recomputed Metrics For Existing Outputs

| output | model | benchmark | rows | strict_exact | answer_in_output | nf_false_answer_rate | avg_latency_s | prompt_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| outputs/dummy_docminibench_v0.jsonl | dummy | data/docminibench_v0.jsonl | 120 | 0.1667 | 0.1833 | 0.0000 | 0.0100 | prompt_config_unverified |
| outputs/dummy_preds.jsonl | dummy | data/fixtures/docminibench_sample.jsonl | 7 | 0.7143 | 0.7143 | 1.0000 | 0.0100 | prompt_config_unverified |
| outputs/qwen2_5_vl_3b_instruct_docminibench_v0_preds.jsonl | qwen2_5_vl_3b_instruct | data/docminibench_v0.jsonl | 120 | 0.8083 | 0.8167 | 0.0000 | 1.2059 | prompt_verified |
| outputs/qwen2_5_vl_3b_instruct_notfound_controlled_v0_preds.jsonl | qwen2_5_vl_3b_instruct | data/notfound_controlled_v0.jsonl | 50 | 1.0000 | 1.0000 | 0.0000 | 0.4486 | prompt_verified |
| outputs/smolvlm2_500m_video_docminibench_v0_preds.jsonl | smolvlm2_500m_video | data/docminibench_v0.jsonl | 120 | 0.3667 | 0.4750 | 1.0000 | 0.4464 | prompt_config_unverified |
| outputs/smolvlm2_500m_video_notfound_controlled_v0_preds.jsonl | smolvlm2_500m_video | data/notfound_controlled_v0.jsonl | 50 | 0.0200 | 0.0200 | 0.9800 | 0.7372 | prompt_verified |
| outputs/smolvlm_500m_docminibench_v0_preds.jsonl | smolvlm_500m | data/docminibench_v0.jsonl | 120 | 0.3917 | 0.4917 | 1.0000 | 0.4769 | prompt_config_unverified |
| outputs/smolvlm_500m_not_found_strict_poc_preds.jsonl | smolvlm_500m | data/docminibench_v0.jsonl | 20 | 0.0000 | 0.0000 | 1.0000 | 0.6372 | prompt_verified |
| outputs/smolvlm_500m_notfound_controlled_v0_preds.jsonl | smolvlm_500m | data/notfound_controlled_v0.jsonl | 50 | 0.0000 | 0.0000 | 1.0000 | 0.4142 | prompt_verified |
| outputs/smolvlm_500m_smoke_preds.jsonl | smolvlm_500m | data/fixtures/docminibench_sample.jsonl | 3 | 0.6667 | 1.0000 | - | 2.0063 | prompt_config_unverified |
