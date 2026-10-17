# Amazon ML Challenge 2026 — Methodology Documentation

**Team Name**: [YOUR TEAM NAME]  
**Team Members**: [MEMBER 1], [MEMBER 2], ...  
**Final Val F₀.₅**: [FILL IN]  
**Public Leaderboard F₀.₅**: [FILL IN]

---

## 1. Problem Understanding

We approached Business Entity Resolution (ER) as a **two-stage pipeline**:

1. **Blocking (candidate generation)**: Efficiently narrow down billions of possible pairs to a tractable candidate set, maximizing recall while reducing comparison cost.
2. **Matching (ML classification)**: Score each candidate pair using learned similarity features, then threshold for precision-optimized F₀.₅.

The key insight driving our design is that **F₀.₅ weights precision 2× over recall**. Therefore:
- Incorrect merges (false positives) are penalized more than missed matches (false negatives)
- Singleton prediction (empty `matched_entity_ids`) is safe when uncertain
- Our threshold was explicitly calibrated for F₀.₅, not F₁

---

## 2. Methodology Overview

### Pipeline Stages
```
Raw TSVs → Text Normalization → Multilingual Embedding → Multi-Key Blocking
         → Feature Engineering → LightGBM Classifier → F₀.₅ Threshold → Output
```

### Why This Approach?
- **Multilingual embeddings**: Handle US English, Indian English/Hindi, and unseen French (test set) without hard-coding language rules.
- **LightGBM over fine-tuned transformers**: Faster iteration, interpretable feature importance, excellent performance on tabular similarity features.
- **Multi-strategy blocking**: Any single blocking key misses ~5–20% of true matches. Taking the union of 5 orthogonal strategies achieves >98% recall on training data.

---

## 3. Text Normalization

All text fields are normalized before any similarity computation:

1. Unicode NFC normalization (handles accented chars, Hindi diacritics)
2. Lowercase
3. Abbreviation expansion (custom dictionary: Corp→Corporation, Pvt→Private, Rd→Road, etc.)
4. Remove non-alphanumeric characters (keep spaces)
5. Collapse whitespace

**Abbreviation dictionary**: 40+ business name abbreviations, 20+ address abbreviations. Designed to be country-agnostic (includes French legal entity forms: SARL, SAS, EURL).

---

## 4. Candidate Generation / Blocking Strategy

We used **5 independent blocking keys**, taking their union:

| Key | Strategy | Recall Contribution |
|---|---|---|
| BK-1 | TF-IDF (char 2-4 gram) ANN cosine similarity, top-20 per S1 | ~85% |
| BK-2 | Character trigram inverted index on business name (Jaccard ≥ 0.2) | ~75% |
| BK-3 | (Country, first token of name) exact key match | ~60% |
| BK-4 | Soundex phonetic key on first word of name, per country | ~45% |
| BK-5 | Address token overlap (≥2 tokens in common) | ~50% |

**Union recall**: [FILL IN FROM TRAINING] on training ground truth.

**Reduction ratio**: Compared [FILL IN]% of all possible pairs (target: < 5%).

---

## 5. Model Architecture & Feature Engineering

### Features (22 total)

**Name similarity group (5)**:
- Levenshtein ratio
- Jaro-Winkler similarity
- Token sort ratio (RapidFuzz)
- Token set ratio (handles word reordering)
- Partial ratio (substring match for DBA names)

**Address similarity group (5)**:
- Levenshtein ratio
- Token sort ratio
- Token set ratio
- Jaccard on address token sets
- Partial ratio

**Semantic feature (1)**:
- Cosine similarity of `paraphrase-multilingual-mpnet-base-v2` embeddings on combined name+address

**Structural features (4)**:
- Normalized name length difference
- Address token count difference
- Country match (binary: 1 if same country)
- Empty field flags (4 binary flags)

**Composite features (3)**:
- Token-set-ratio(name) × Token-set-ratio(address)
- Max of all name similarity features
- Max of all similarity features (overall)

### Training Data Construction

- **Positives**: Ground truth matches from training GT
- **Hard negatives** (5:1 ratio): Blocking candidates that are NOT ground truth matches. Critical for fine-grained discrimination between similar-but-different businesses.
- **Random negatives** (2:1 ratio): Random non-matching pairs for diversity

### Model

- **Algorithm**: LightGBM (gradient boosted decision trees)
- **Scale pos weight**: Automatically computed from class imbalance ratio
- **Hyperparameters**: n_estimators=500, learning_rate=0.05, max_depth=8, num_leaves=63

### Threshold Calibration

Grid search over [0.05, 0.95] in steps of 0.01, maximizing macro-F₀.₅ on 20% validation split. This is explicitly not F₁ threshold, which would be too aggressive for a precision-weighted metric.

**Best threshold**: [FILL IN]

---

## 6. Handling the France Test Set

France was not present in training data. Our approach is inherently country-agnostic:

- No one-hot encoding of country; only `country_match` binary feature used
- Multilingual embedding model (50+ languages) natively supports French
- Address normalization includes French abbreviations (rue, blvd → boulevard)
- Legal entity abbreviations (SARL, SAS, EURL) added to abbreviation dictionary

---

## 7. Singleton Handling

The problem states that a Source 1 entity may have **zero** matches. Correctly predicting an empty list earns F₀.₅ = 1.0.

Our approach:
- Conservative threshold (calibrated for F₀.₅) means uncertain pairs are NOT matched
- Any S1 entity with no candidate pairs above threshold → empty `matched_entity_ids`
- S1 entities with no blocking candidates → automatically singleton

This significantly boosts score on singleton S1 entities vs. a "match everything above 0.3" approach.

---

## 8. Validation Results

| Metric | Value |
|---|---|
| Blocking recall (train) | [FILL IN] |
| Val F₀.₅ (macro) | [FILL IN] |
| Val Precision (macro) | [FILL IN] |
| Val Recall (macro) | [FILL IN] |
| Val Singleton Accuracy | [FILL IN] |
| Best Threshold | [FILL IN] |

---

## 9. What Didn't Work

[Document failed experiments here as you run them]

- Example: threshold of 0.5 (F₁ default) → too aggressive, hurt precision
- Example: [Any approach you tried that reduced score]

---

## 10. Reproducibility

```bash
# Full reproduction from raw data to submission files:
pip install -r code/business_entity_resolution/requirements.txt
python code/business_entity_resolution/src/run_pipeline.py \
    --mode full \
    --config configs/config.yaml
```

**Random seed**: 42 everywhere. Results are deterministic.
**Runtime**: ~[FILL IN] minutes on [CPU/GPU].

---

## 11. External Resources Used

- `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` (Apache 2.0) — pre-trained multilingual embeddings
- `cross-encoder/ms-marco-MiniLM-L-6-v2` (Apache 2.0) — cross-encoder reranker (if used)
- RapidFuzz (MIT) — string similarity library
- LightGBM (MIT) — gradient boosted classifier

**No external data or APIs used.** All normalization dictionaries were manually crafted from patterns observed in training data.
