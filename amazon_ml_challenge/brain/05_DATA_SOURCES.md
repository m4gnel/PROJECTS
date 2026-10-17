# 05_DATA_SOURCES.md
# Data Sources & EDA Guide

## 1. Provided Data Sources

All data comes from the competition dataset. **No external data allowed.**

| File | Role | Expected Rows |
|---|---|---|
| `train_source1.tsv` | Reference (anchor) | ~5,000–50,000 |
| `train_source2.tsv` | Noisy source A | ~5,000–50,000 |
| `train_source3.tsv` | Noisy source B | ~5,000–50,000 |
| `train_ground_truth.tsv` | Labels | 1 row per S1 entity |
| `test_source1.tsv` | Test anchor | TBD |
| `test_source2.tsv` | Test noisy A | TBD |
| `test_source3.tsv` | Test noisy B | TBD |

---

## 2. EDA Checklist (run `notebooks/01_eda.ipynb`)

### 2.1 Basic Stats
```python
# For each source:
print(df.shape)
print(df.isnull().sum())
print(df['country'].value_counts())
print(df['business_name'].str.len().describe())
print(df['business_address'].str.len().describe())
```

### 2.2 Match Distribution
```python
gt = pd.read_csv('train_ground_truth.tsv', sep='\t')
gt['matched_entity_ids'] = gt['matched_entity_ids'].fillna('')
gt['n_matches'] = gt['matched_entity_ids'].apply(
    lambda x: len(x.split(',')) if x.strip() else 0
)
print(gt['n_matches'].value_counts().sort_index())
# Expected: heavy 0 (singletons), then 1, then 2+
```

### 2.3 Name Similarity Distribution (Positive Pairs)
```python
# Sample 1000 positive pairs from GT
# Compute Levenshtein ratio for each pair
# Plot histogram — guides threshold choices
```

### 2.4 Country Distribution
```python
for src in [s1, s2, s3]:
    print(src['country'].value_counts())
# Confirms US + India in train, no France
```

### 2.5 Noise Analysis
```python
# For random sample of positive pairs:
# Check: same country? (should be ~100%)
# Check: avg name Levenshtein ratio
# Check: avg address token-set ratio
# → guides which features matter most
```

### 2.6 Blocking Recall Baseline
```python
# Implement each blocking key independently
# Measure: fraction of GT pairs captured
# Target: each individual BK > 80%; union > 98%
```

---

## 3. Expected Data Patterns by Country

### United States
- Business names: English, common suffix Corp/LLC/Inc/Ltd
- Addresses: US format — [number] [Street Name], [City], [State] [ZIP]
- ZIP codes: 5 digits or 5+4
- State abbreviations: CA, TX, NY, etc.

### India
- Business names: Mix of English + transliterated Hindi/regional
- Suffixes: Pvt Ltd, Private Limited, Associates, Enterprises
- Addresses: Highly variable — plot numbers, sector, ward, near landmarks
- PIN codes: 6 digits
- City names may have multiple romanizations (Bengaluru/Bangalore)

### France (TEST ONLY — unseen at training)
- Business names: SARL, SAS, SA, EURL legal suffixes
- Addresses: French format — [number] [rue/avenue/boulevard] [Name], [postal code] [Ville]
- Postal codes: 5 digits
- Pipeline MUST generalize here without training data

---

## 4. Data Quality Red Flags to Watch

| Issue | How to Detect | Mitigation |
|---|---|---|
| Empty business_name | `df['business_name'].isnull()` | Use address-only features |
| Empty business_address | `df['business_address'].isnull()` | Use name-only features |
| Both fields empty | Both null | Treat as low-confidence, likely singleton |
| Duplicate entity_ids | `df['entity_id'].duplicated()` | Error — data integrity issue |
| Cross-source ID leakage | S1 IDs appearing in S2 file | Error — report |
| Non-UTF-8 chars | Encoding errors on read | Use `encoding='utf-8', errors='replace'` |

---

## 5. Negative Pair Mining Strategy

The training data only has positive pairs (GT matches). We must generate negatives:

### Strategy 1: Random Negatives
- For each S1 entity, randomly sample 5–10 S2/S3 records that are NOT in GT
- Easy negatives — model learns quickly but may overfit

### Strategy 2: Hard Negatives (CRITICAL)
- Run blocking on training data
- For each S1 entity, take blocking candidates that are NOT in GT
- These are semantically similar but actually different businesses
- Forces model to learn fine-grained discrimination
- **Ratio**: 1 positive : 5 hard negatives per S1 entity

### Strategy 3: Cross-Country Negatives
- Pair records from different countries — always negative
- Easy to generate, adds diversity
