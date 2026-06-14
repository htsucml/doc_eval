# Step 0 Preflight Status

- Status: completed
- Timestamp UTC: `2026-06-13T16:07:33.153909+00:00`

## Commands And Output

```text
# Codex addon stepwise command log
start_utc=2026-06-13T16:07:23Z
cwd=/workspace/doc_eval
$ .venv/bin/python -m pytest -q
...............................                                          [100%]
31 passed in 6.50s
$ git diff --check
$ git status --short
 M configs/models.yaml
?? data/docvqa_manual_notfound_combined_expanded_v0.jsonl
?? data/docvqa_manual_notfound_combined_expanded_v0_eval.jsonl
?? data/notfound_controlled_v0.jsonl
?? data/notfound_controlled_v0.meta.json
?? data/notfound_controlled_v0_images/
?? data/notfound_controlled_v0_smoke5.jsonl
?? data/notfound_ood_sanity_v0.jsonl
?? data/notfound_ood_sanity_v0.meta.json
?? data/notfound_ood_sanity_v0_eval.jsonl
?? data/notfound_ood_sanity_v0_eval_strict.jsonl
?? data/notfound_ood_sanity_v0_images/
?? data/sft_docvqa_template_train_v0.jsonl
?? data/sft_docvqa_template_train_v0.meta.json
?? data/sft_docvqa_template_train_v0_images/
?? data/sft_docvqa_template_val_v0.jsonl
?? doc_eval_git_20260613T073259Z.bundle
?? doc_eval_git_20260613T141341Z.bundle
?? reports/codex_marathon_handoff.json
?? tmp_audit_pack/
$ df -h / /root /workspace
Filesystem                    Size  Used Avail Use% Mounted on
overlay                        20G   19G  2.0G  91% /
overlay                        20G   19G  2.0G  91% /
mfs#eur-is-1.runpod.net:9421  1.4P  827T  606T  58% /workspace
$ du -sh /root/.cache/huggingface 2>/dev/null || true
14G	/root/.cache/huggingface
$ du -sh /workspace/hf_home 2>/dev/null || true

```
