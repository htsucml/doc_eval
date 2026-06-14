# Step 1 HF Cache Status

- Status: `passed`
- Timestamp UTC: `2026-06-13T16:09:22.287160+00:00`
- `/root/.cache/huggingface` resolves to: `/workspace/hf_home`
- Cache movement performed only after corrected process check found no active `eval_model.py` or `finetune_lora.py` process.
- Required env for future HF commands:
  - `HF_HOME=/workspace/hf_home`
  - `HF_HUB_CACHE=/workspace/hf_home/hub`
  - `HUGGINGFACE_HUB_CACHE=/workspace/hf_home/hub`
  - `HF_DATASETS_CACHE=/workspace/hf_home/datasets`

## Commands And Output

```text
$ readlink -f /root/.cache/huggingface
/workspace/hf_home
$ ls -ld /root/.cache/huggingface /workspace/hf_home /workspace/hf_home/hub /workspace/hf_home/datasets
lrwxrwxrwx  1 root root      18 Jun 13 16:09 /root/.cache/huggingface -> /workspace/hf_home
drwxrwxrwx+ 5 root root 3001360 Jun 12 16:14 /workspace/hf_home
drwxrwxrwx+ 2 root root       1 Jun 12 16:22 /workspace/hf_home/datasets
drwxrwxrwx+ 9 root root 3001360 Jun 13 15:58 /workspace/hf_home/hub
$ df -h / /root /workspace
Filesystem                    Size  Used Avail Use% Mounted on
overlay                        20G  4.5G   16G  23% /
overlay                        20G  4.5G   16G  23% /
mfs#eur-is-1.runpod.net:9421  1.4P  827T  606T  58% /workspace
$ du -sh /root/.cache/huggingface 2>/dev/null || true
0	/root/.cache/huggingface
$ du -sh /workspace/hf_home 2>/dev/null || true
14G	/workspace/hf_home

```
