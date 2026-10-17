# 15_MICROTASKS.md
# Microtask Breakdown — Sprint Plan

## PRIORITY ORDER: Do these in sequence. Do not skip.

---

## BLOCK 1: Setup (30 min)

### MT-001: Environment Setup
```
pip install pandas sentence-transformers faiss-cpu rapidfuzz lightgbm scikit-learn \
            transformers numpy scipy jupyter pytest black
```
- Pin versions: `pip freeze > requirements.txt`

### MT-002: Data Download & Verify
- Download dataset from competition portal
- Place in `dataset/train/` and `dataset/test/`
- Verify: `python -c "import pandas as pd; df = pd.read_csv('dataset/train/train_source1.tsv', sep='\t'); print(df.shape, df.columns.tolist())"`

### MT-003: Copy validate_submission.py
- Copy the official validator from `student_resource/utils/validate_submission.py`
- Place in `code/business_entity_resolution/utils/validate_submission.py`

---

## BLOCK 2: Data Understanding (45 min)

### MT-004: Run EDA Notebook
- Open `notebooks/01_eda.ipynb`
- Execute all cells
- Note: data shapes, null counts, country distribution, match distribution
- Note: are there entities with both name AND address empty?
- Note: what fraction of S1 entities are singletons in GT?

### MT-005: Analyze Positive Pairs
- For random 500 positive pairs from GT:
  - Compute Levenshtein ratio for name pairs
  - Compute token-set ratio for address pairs
  - Plot distributions
  - Note: what is the minimum similarity you see among true matches?

---

## BLOCK 3: Core Pipeline (2–3 hours)

### MT-006: Implement normalizer.py
- Functions: `normalize_text()`, `build_combined_text()`
- Load abbreviations from `configs/abbreviations.json`
- Write unit tests in `tests/test_normalizer.py`
- Test coverage ≥ 15 test cases

### MT-007: Implement data_loader.py
- Functions: `load_sources()`, `validate_entity_ids()`
- Handle: missing columns, wrong separator, empty file
- Add entity_id prefix validation

### MT-008: Implement embedder.py
- Load `paraphrase-multilingual-mpnet-base-v2`
- Batch encode with L2 normalization
- Build FAISS IndexFlatIP
- Test: encode 100 strings, search top-5, verify indices are valid

### MT-009: Implement blocker.py (CRITICAL — affects upper bound)
- Implement all 5 blocking keys (BK-1 through BK-5)
- Implement union + deduplication
- Implement `compute_blocking_recall()`
- **Validate: run on training data, confirm recall ≥ 0.98**
- If recall < 0.98: add more blocking keys (do NOT proceed)

### MT-010: Implement feature_engineer.py
- Compute all features from `02_TRD.md` Feature Engineering section
- Test: verify no NaN or Inf in feature output
- Test: perfect match pair → all similarities near 1.0
- Test: completely different pair → all similarities near 0.0

### MT-011: Build Training Dataset
- Run blocking on training data
- For each S1 entity:
  - Positive pairs: GT matches
  - Hard negative pairs: blocking candidates that are NOT GT matches (top 5)
  - Random negative pairs: random S2/S3 not in blocking (2 per S1)
- Build feature matrix with labels
- Check class imbalance ratio

### MT-012: Train LightGBM Matcher
- Split training GT into 80/20 (seed=42)
- Train on 80% feature matrix
- Calibrate threshold on 20% validation set
- Log: val F₀.₅, val precision, val recall, best threshold
- Save model: `models/matcher.pkl`

---

## BLOCK 4: Test Inference (1 hour)

### MT-013: Run Full Test Inference
- Execute: `python src/run_pipeline.py --mode predict --config configs/config.yaml`
- Verify: both output files created in `output/`

### MT-014: Validate Output
- Execute: `python utils/validate_submission.py ...`
- Must see: PASS
- Fix any issues before proceeding

### MT-015: First Submission
- Upload `output/matching_results.tsv` to Portal
- Record public leaderboard score

---

## BLOCK 5: Improvement Iterations (remaining time)

### MT-016: Add Cross-Encoder Reranking
- For top-20 candidates per S1, run cross-encoder
- Combine cross-encoder score with LightGBM score
- Re-calibrate threshold

### MT-017: Hard Negative Mining Round 2
- Analyze false positives from val set
- Add those specific types as additional hard negatives
- Retrain model

### MT-018: Ensemble
- Train 3 LightGBM models with different seeds
- Average probabilities
- Recalibrate threshold

### MT-019: Country-Specific Threshold
- Analyze val F₀.₅ by country (US vs India)
- If country-specific thresholds improve: implement per-country thresholding

### MT-020: Final Submission Package
- Follow Phase 5 in `14_PRODUCTION_CHECKLIST.md`
- Fill in `Documentation_template.md`
- Create zip
