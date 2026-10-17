# 02_TRD.md
# Technical Requirements Document

## 1. Recommended Model Stack

### Primary Embedding Model
**`sentence-transformers/paraphrase-multilingual-mpnet-base-v2`**
- License: Apache 2.0 ✅
- Params: 278M ✅ (well under 8B)
- Language: 50+ languages including English, Hindi, French ✅
- Embedding dim: 768
- Use: encode business_name + business_address → dense vector

**Alternative / Fallback**
`BAAI/bge-m3` (Apache 2.0, ~570M params) — better cross-lingual, slightly slower

### Cross-Encoder Reranker
**`cross-encoder/ms-marco-MiniLM-L-6-v2`**
- License: Apache 2.0 ✅
- Params: 22M ✅
- Use: pairwise (query_text, candidate_text) → match score [0,1]
- Applied only to top-K candidates from blocking, not full dataset

---

## 2. Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Language | Python | 3.10+ |
| Data | pandas | 2.x |
| ML / Embeddings | sentence-transformers | 3.x |
| ANN Index | faiss-cpu | 1.8.x |
| String Similarity | rapidfuzz | 3.x |
| Cross-Encoder | sentence-transformers CrossEncoder | 3.x |
| Tokenization | transformers | 4.x |
| Serialization | joblib | 1.x |
| Validation | stdlib only (as per challenge rules) |
| Logging | Python logging | stdlib |

---

## 3. Hardware Requirements

| Tier | Minimum | Recommended |
|---|---|---|
| RAM | 8 GB | 16 GB |
| CPU | 4 cores | 8+ cores |
| GPU | Not required | CUDA 12+ (speeds up encoding 10x) |
| Disk | 5 GB | 10 GB |

---

## 4. Text Normalization Requirements

The normalizer must handle ALL of these before any similarity computation:

```
lowercase → strip whitespace → remove punctuation (keep alphanumeric + space)
→ expand abbreviations (Corp→Corporation, Pvt→Private, Rd→Road, St→Street …)
→ unicode normalize (NFC) → collapse multiple spaces
```

Abbreviation expansion must be:
- Country-agnostic (don't assume English only)
- Bidirectional (Corp→Corporation AND Corporation→Corp both normalize to canonical form)
- Applied BEFORE embedding — models see clean text

---

## 5. Blocking Strategy Requirements

The blocking stage MUST:
1. **Recall > 98%** on training GT (never miss a ground-truth pair)
2. **Reduction ratio > 95%** (compare < 5% of all possible pairs)
3. Use **at least 3 independent blocking keys** (n-gram, token, geo-prefix) for redundancy
4. Be country-agnostic (no hard-coded ZIP/PIN patterns)
5. Handle empty fields gracefully (if address is empty, block on name only)

### Required Blocking Keys
| Key | Method |
|---|---|
| BK-1 | 3-gram Jaccard on normalized name |
| BK-2 | TF-IDF top-K ANN on concatenated name+address |
| BK-3 | Sorted trigram overlap on address tokens |
| BK-4 | Country prefix + first token of business name |
| BK-5 | Soundex/Metaphone phonetic key on business name |

---

## 6. Feature Engineering Requirements

The matching model receives a feature vector for each candidate pair:

| Feature Group | Features |
|---|---|
| Name similarity | Levenshtein ratio, Jaro-Winkler, Token-sort ratio, Token-set ratio, Cosine TF-IDF |
| Address similarity | Levenshtein ratio, Token-set ratio, Jaccard on address tokens |
| Semantic | Cosine similarity of multilingual sentence embeddings |
| Structural | name_length_diff, address_token_count_diff, country_match (0/1) |
| Composite | name_sim × address_sim, max(name_sim, address_sim) |

---

## 7. Matching Model Requirements

- **Algorithm**: LightGBM or XGBoost gradient boosted classifier
  - Trained on positive pairs (GT matches) + negative pairs (hard negatives from blocking)
  - Output: probability score ∈ [0, 1]
- **Threshold**: Tuned on validation split to maximize F₀.₅ (NOT F₁)
- **Hard negatives**: For each S1 entity, mine top-10 blocking candidates that are NOT true matches → forces model to learn fine-grained discrimination
- **Class imbalance**: Use `scale_pos_weight` or `class_weight='balanced'` — negatives vastly outnumber positives

---

## 8. Threshold Calibration

```python
# Pseudo-code for threshold search
thresholds = np.arange(0.1, 0.95, 0.01)
best_thresh, best_f05 = 0.5, 0.0
for t in thresholds:
    preds = predict_with_threshold(val_candidates, t)
    f05 = compute_f05_macro(preds, val_ground_truth)
    if f05 > best_f05:
        best_f05, best_thresh = f05, t
```

---

## 9. Validation Protocol

- **Validation split**: 20% of training S1 entities (stratified by country)
- **Score**: Macro-average F₀.₅ including singletons
- **Blocking recall**: Fraction of GT pairs that appear in candidate_pairs
- **Never train on validation split** — use only for threshold calibration and architecture selection
