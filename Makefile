PYTHON ?= .venv/bin/python
DEVICE ?= cuda
MINI_MODEL ?= smolvlm2_500m_video
STAMP ?= $(shell date -u +%Y%m%dT%H%M%SZ)
SMOKE_BENCH ?= outputs/smoke/docminibench_sample_$(STAMP).jsonl
SMOKE_PREDS ?= outputs/smoke/dummy_preds_$(STAMP).jsonl
SMOKE_CSV ?= reports/smoke/dummy_results_$(STAMP).csv
SMOKE_MD ?= reports/smoke/dummy_results_$(STAMP).md
MINI_PREDS ?= outputs/reproduce_mini/$(MINI_MODEL)_controlled5_$(STAMP)_preds.jsonl
MINI_CSV ?= reports/reproduce_mini/$(MINI_MODEL)_controlled5_$(STAMP)_results.csv
MINI_MD ?= reports/reproduce_mini/$(MINI_MODEL)_controlled5_$(STAMP)_results.md
AGG_DIR ?= reports/aggregate_rebuild_$(STAMP)

.PHONY: test smoke reproduce-mini aggregate paper clean-paper

test:
	$(PYTHON) -m pytest -q

smoke:
	mkdir -p outputs/smoke reports/smoke
	$(PYTHON) scripts/build_benchmark_v0.py --out $(SMOKE_BENCH)
	$(PYTHON) scripts/eval_model.py --model dummy --benchmark $(SMOKE_BENCH) --out $(SMOKE_PREDS) --limit 3 --device cpu
	$(PYTHON) scripts/aggregate_results.py --preds $(SMOKE_PREDS) --benchmark $(SMOKE_BENCH) --out $(SMOKE_CSV) --markdown $(SMOKE_MD)
	@echo "smoke_preds=$(SMOKE_PREDS)"
	@echo "smoke_results=$(SMOKE_CSV)"

reproduce-mini:
	$(PYTHON) -c "import torch; raise SystemExit(0 if torch.cuda.is_available() else 'CUDA is required for make reproduce-mini')"
	mkdir -p outputs/reproduce_mini reports/reproduce_mini
	HF_HOME=/workspace/hf_home HF_HUB_CACHE=/workspace/hf_home/hub HUGGINGFACE_HUB_CACHE=/workspace/hf_home/hub HF_DATASETS_CACHE=/workspace/hf_home/datasets \
	$(PYTHON) scripts/eval_model.py --model $(MINI_MODEL) --benchmark data/notfound_controlled_v0.jsonl --limit 5 --out $(MINI_PREDS) --config configs/eval_not_found_strict.yaml --device $(DEVICE) --allow-real-models
	$(PYTHON) scripts/aggregate_results.py --preds $(MINI_PREDS) --benchmark data/notfound_controlled_v0.jsonl --out $(MINI_CSV) --markdown $(MINI_MD)
	@echo "mini_preds=$(MINI_PREDS)"
	@echo "mini_results=$(MINI_CSV)"

aggregate:
	mkdir -p $(AGG_DIR)
	$(PYTHON) scripts/aggregate_results.py --preds outputs/smolvlm2_500m_video_docminibench_v0_strict_preds.jsonl --benchmark data/docminibench_v0.jsonl --out $(AGG_DIR)/smolvlm2_500m_video_docminibench_v0_strict_results.csv --markdown $(AGG_DIR)/smolvlm2_500m_video_docminibench_v0_strict_results.md
	$(PYTHON) scripts/aggregate_results.py --preds outputs/smolvlm2_2_2b_docvqa_manual_notfound_combined_expanded_v0_preds.jsonl --benchmark data/docvqa_manual_notfound_combined_expanded_v0_eval.jsonl --out $(AGG_DIR)/smolvlm2_2_2b_docvqa_manual_notfound_combined_expanded_v0_results.csv --markdown $(AGG_DIR)/smolvlm2_2_2b_docvqa_manual_notfound_combined_expanded_v0_results.md
	@echo "aggregate_dir=$(AGG_DIR)"

paper:
	$(PYTHON) scripts/build_paper_assets.py
	@if command -v latexmk >/dev/null 2>&1; then \
		cd paper && latexmk -pdf -interaction=nonstopmode main.tex; \
	elif command -v pdflatex >/dev/null 2>&1 && command -v bibtex >/dev/null 2>&1; then \
		cd paper && pdflatex -interaction=nonstopmode main.tex && bibtex main && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex; \
	else \
		echo "No LaTeX toolchain found. Install latexmk or pdflatex+bibtex, then run: make paper"; \
		echo "Paper sources are in paper/main.tex; generated tables are in paper/tables/."; \
	fi

clean-paper:
	rm -f paper/*.aux paper/*.bbl paper/*.blg paper/*.fdb_latexmk paper/*.fls paper/*.log paper/*.out paper/*.pdf
