# SFT Train Data Spec

Controlled synthetic train-only data generated with seed `20260615`.
Rows and images are distinct from the evaluation datasets.

- Train rows: 500
- Validation rows: 80
- Controlled synthetic answerable positives: 250 train, 40 val
- Controlled synthetic NOT_FOUND negatives: 250 train, 40 val
- Native template-swapped real-document negatives: 0 rows, because no non-evaluation real document images were locally available.
- Negative rows use `absence_evidence_type=controlled_render_negative` and are mechanically checked against rendered text.
- All rows are marked `intended_use=sft_train_only` and `not_for_primary_eval=true`.

Template-swapped negatives remain a methodology option only; none are included in this generated dataset.
