# 08_UI_SPEC.md
# CLI & Output Interface Specification
# (No GUI — competition requires only TSV output files)

## 1. Command-Line Interface

### Primary Entrypoint
```bash
python src/run_pipeline.py [OPTIONS]
```

### Arguments

| Flag | Type | Default | Description |
|---|---|---|---|
| `--mode` | str | `full` | `train` / `predict` / `full` |
| `--config` | str | `configs/config.yaml` | Path to YAML config |
| `--model` | str | `models/matcher.pkl` | Path to save/load model |

### Examples
```bash
# Train only (save model + threshold)
python src/run_pipeline.py --mode train

# Predict only (requires trained model)
python src/run_pipeline.py --mode predict

# Full pipeline (train then predict)
python src/run_pipeline.py --mode full

# Custom config
python src/run_pipeline.py --mode full --config configs/config_experiment2.yaml
```

---

## 2. Progress Output (stdout)

The pipeline prints to both stdout and `pipeline.log`:

```
2026-09-25 10:00:01 [INFO] run_pipeline: ============================================================
2026-09-25 10:00:01 [INFO] run_pipeline: STAGE: TRAINING
2026-09-25 10:00:01 [INFO] run_pipeline: ============================================================
2026-09-25 10:00:01 [INFO] data_loader: Loaded dataset/train/train_source1.tsv: 12430 rows, 4 cols
2026-09-25 10:00:02 [INFO] data_loader: Loaded dataset/train/train_source2.tsv: 15620 rows, 4 cols
2026-09-25 10:00:02 [INFO] data_loader: Loaded dataset/train/train_source3.tsv: 14890 rows, 4 cols
2026-09-25 10:00:03 [INFO] normalizer: Loaded abbreviations: 38 name, 22 address
2026-09-25 10:01:10 [INFO] embedder: Loading embedding model: sentence-transformers/paraphrase-multilingual-mpnet-base-v2
2026-09-25 10:02:45 [INFO] embedder: Encoding 12430 texts (batch_size=256)...
2026-09-25 10:04:20 [INFO] blocker: BK-1: TF-IDF ANN blocking...
2026-09-25 10:04:45 [INFO] blocker: Blocking done: 284,500 total candidates, 9944/9944 S1 entities have candidates
2026-09-25 10:04:46 [INFO] blocker: BLOCKING RECALL: 0.9913 (12847/12959 pairs)
2026-09-25 10:05:30 [INFO] feature_engineer: Building features for 284,500 candidate pairs...
2026-09-25 10:07:15 [INFO] matcher: Training LightGBM: 45,230 pairs, 12847 pos, 32383 neg
2026-09-25 10:07:45 [INFO] matcher: Best threshold: 0.47 → Val F₀.₅: 0.9231
============================================================
EVALUATION REPORT
============================================================
  Macro F₀.₅:          0.9231
  Macro Precision:      0.9445
  Macro Recall:         0.8723
  Total S1 Entities:    2486
  Singletons:           1102
  Correct Singletons:   1089
  False Merges:         13
  Missed All Matches:   47
  Singleton Accuracy:   0.9882
============================================================
2026-09-25 10:07:50 [INFO] run_pipeline: ✅ Prediction complete!
```

---

## 3. Output Files Spec

### output/matching_results.tsv
- Encoding: UTF-8
- Delimiter: TAB (`\t`)
- Line ending: Unix (`\n`)
- Header: exactly `source1_entity_id\tmatched_entity_ids`
- No BOM, no trailing tabs

### output/candidate_pairs.tsv
- Same format as matching_results.tsv
- Header: exactly `source1_entity_id\tcandidate_entity_ids`

### models/matcher.pkl
- Joblib-serialized `(LGBMClassifier, List[str])` tuple
- Feature name list stored alongside model for versioning safety

### models/threshold.json
```json
{"threshold": 0.47, "val_f05": 0.9231}
```

### pipeline.log
- Full run log with timestamps
- Useful for debugging failed submissions

---

## 4. Makefile Quick Reference

```bash
make install    # Install dependencies
make train      # Train model
make predict    # Run inference
make validate   # Validate output files
make package    # Create submission zip
make test       # Run unit tests
make clean      # Remove output and logs
```
