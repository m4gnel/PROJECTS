# Business Entity Resolution — Amazon ML Challenge 2026

## Quick Start (Run Everything)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Place dataset files (see Dataset Setup below)

# 3. Run full pipeline (train + predict)
python src/run_pipeline.py --mode full --config configs/config.yaml

# 4. Validate output
python utils/validate_submission.py \
    --matching output/matching_results.tsv \
    --candidate output/candidate_pairs.tsv \
    --test-dir dataset/test

# 5. Upload output/matching_results.tsv to the leaderboard portal
```

---

## Dataset Setup

```
amazon_ml_challenge/
├── dataset/
│   ├── train/
│   │   ├── train_source1.tsv     ← from competition portal
│   │   ├── train_source2.tsv
│   │   ├── train_source3.tsv
│   │   └── train_ground_truth.tsv
│   └── test/
│       ├── test_source1.tsv
│       ├── test_source2.tsv
│       └── test_source3.tsv
```

All files are tab-separated. Read with `pd.read_csv(..., sep='\t')`.

---

## Pipeline Architecture

```
Raw TSVs → Normalize → Embed → Block → Features → LightGBM → Output
```

| Stage | Script | Purpose |
|---|---|---|
| Load | `data_loader.py` | Read and validate TSVs |
| Normalize | `normalizer.py` | Clean text, expand abbreviations |
| Embed | `embedder.py` | Multilingual sentence embeddings |
| Block | `blocker.py` | Generate candidate pairs (5 strategies) |
| Features | `feature_engineer.py` | Similarity features per pair |
| Match | `matcher.py` | LightGBM train/predict + threshold calibration |
| Output | `postprocessor.py` | Write TSV output files |
| Score | `evaluator.py` | F₀.₅ metric computation |

---

## Step-by-Step Reproduction

### Step 1: Environment
```bash
pip install -r requirements.txt
```

### Step 2: Train model
```bash
python src/run_pipeline.py --mode train --config configs/config.yaml
```
This will:
- Load training data
- Normalize text
- Build multilingual embeddings
- Run 5 blocking strategies (target recall ≥ 98%)
- Mine hard negatives
- Train LightGBM classifier
- Calibrate threshold on validation split (20%)
- Save model to `models/matcher.pkl`
- Save threshold to `models/threshold.json`
- Print validation F₀.₅ score

### Step 3: Predict on test set
```bash
python src/run_pipeline.py --mode predict --config configs/config.yaml
```
This will:
- Load test data
- Generate embeddings and blocking candidates
- Run model inference
- Apply calibrated threshold
- Write `output/matching_results.tsv` and `output/candidate_pairs.tsv`

### Step 4: Validate
```bash
python utils/validate_submission.py \
    --matching output/matching_results.tsv \
    --candidate output/candidate_pairs.tsv \
    --test-dir dataset/test
```
Expected: `PASS`

---

## Key Hyperparameters (`configs/config.yaml`)

| Parameter | Default | Effect |
|---|---|---|
| `embedding.model_name` | `paraphrase-multilingual-mpnet-base-v2` | Multilingual embedding model |
| `blocking.tfidf_top_k` | 20 | ANN neighbors per query |
| `blocking.max_candidates_per_s1` | 100 | Hard cap on candidates |
| `matching.n_estimators` | 500 | LightGBM trees |
| `matching.threshold` | 0.5 | Overwritten by calibration |
| `validation.split_ratio` | 0.2 | Train/val split |

---

## Evaluation Metric

**F₀.₅ (precision-weighted, macro-averaged)**

```
F₀.₅ = (1.25 × P × R) / (0.25 × P + R)
```

- Weights precision 2× over recall
- Macro-averaged per S1 entity (including singletons)
- Singleton with no GT match: predict empty → score 1.0

---

## Model Details

- **Embedding**: `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`
  - Apache 2.0 license ✅, 278M params ✅, 50+ languages ✅
- **Classifier**: LightGBM
  - Input: 22 hand-crafted similarity features
  - Output: match probability ∈ [0, 1]
  - Threshold: calibrated on val split for max F₀.₅

---

## Output Format

### matching_results.tsv
```
source1_entity_id	matched_entity_ids
S1-00001	S2-00047,S3-00812
S1-00002	S2-00193
S1-00003	
```

### candidate_pairs.tsv
```
source1_entity_id	candidate_entity_ids
S1-00001	S2-00047,S2-00193,S3-00812,S3-00999
S1-00002	S2-00193
S1-00003	
```

---

## Running Tests
```bash
pytest tests/ -v
```
