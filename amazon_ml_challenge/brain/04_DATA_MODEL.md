# 04_DATA_MODEL.md
# Data Model & Schema

## 1. Input Schema

### Source Files (source1/source2/source3)
```
entity_id          string    PK. Format: "S1-NNNNN" / "S2-NNNNN" / "S3-NNNNN"
business_name      string    May be null/empty. Noisy.
business_address   string    May be null/empty. Noisy. May contain commas.
country            string    Open set: "US", "India", "France", ... (not one-hot)
```

### Ground Truth File
```
source1_entity_id   string    FK → source1.entity_id
matched_entity_ids  string    Comma-separated S2/S3 entity_ids. May be empty string.
```

---

## 2. Internal Data Structures

### RecordDict (in-memory, per record)
```python
{
    "entity_id":         str,   # original ID
    "business_name":     str,   # raw
    "business_address":  str,   # raw
    "country":           str,   # raw
    "norm_name":         str,   # normalized name
    "norm_address":      str,   # normalized address
    "norm_text":         str,   # norm_name + " " + norm_address (for embedding)
    "embedding":         np.ndarray,  # shape (768,), float32
}
```

### CandidatePair
```python
{
    "s1_id":             str,
    "candidate_id":      str,   # S2 or S3
    "blocking_keys":     List[str],   # which BKs triggered this pair
    # Feature group: name similarity
    "lev_name":          float,  # Levenshtein ratio
    "jw_name":           float,  # Jaro-Winkler
    "ts_name":           float,  # Token-sort ratio
    "tset_name":         float,  # Token-set ratio
    "tfidf_name":        float,  # TF-IDF cosine on name
    # Feature group: address similarity
    "lev_addr":          float,
    "ts_addr":           float,
    "tset_addr":         float,
    "jaccard_addr":      float,
    # Feature group: semantic
    "cos_embed":         float,  # Cosine of multilingual embeddings
    # Feature group: structural
    "len_diff_name":     float,  # abs(len(s1_name) - len(s2_name)) / max_len
    "token_diff_addr":   int,    # abs(token_count_diff)
    "country_match":     int,    # 1 if same country, 0 otherwise
    # Composite
    "name_x_addr":       float,  # lev_name * lev_addr
    "max_sim":           float,  # max(lev_name, lev_addr, cos_embed)
    # Label (training only)
    "label":             int,    # 1 = match, 0 = non-match
    # Model output
    "match_prob":        float,  # model.predict_proba output
}
```

### GroundTruth (dict)
```python
{
    "S1-00001": ["S2-00047", "S3-00812"],
    "S1-00002": ["S2-00193"],
    "S1-00003": [],   # singleton
    ...
}
```

---

## 3. Output Schema

### matching_results.tsv
```
source1_entity_id   matched_entity_ids
S1-00001            S2-00047,S3-00812
S1-00002            S2-00193
S1-00003            
```
- Tab-separated
- Every S1 test ID has exactly one row
- `matched_entity_ids` is empty string for singletons

### candidate_pairs.tsv
```
source1_entity_id   candidate_entity_ids
S1-00001            S2-00047,S2-00193,S3-00812,S3-00999
S1-00002            S2-00193
S1-00003            
```
- Same format as matching_results.tsv
- Broader set — matching_results.tsv is a subset of this

---

## 4. Abbreviation Expansion Map (configs/abbreviations.json)

```json
{
  "name": {
    "corp": "corporation",
    "co": "company",
    "co.": "company",
    "pvt": "private",
    "ltd": "limited",
    "llc": "limited liability company",
    "inc": "incorporated",
    "inc.": "incorporated",
    "&": "and",
    "bros": "brothers",
    "mfg": "manufacturing",
    "intl": "international",
    "assoc": "associates",
    "dept": "department",
    "svc": "services",
    "svcs": "services",
    "tech": "technologies",
    "grp": "group",
    "hldgs": "holdings",
    "entrprs": "enterprises"
  },
  "address": {
    "rd": "road",
    "st": "street",
    "ave": "avenue",
    "blvd": "boulevard",
    "dr": "drive",
    "ln": "lane",
    "ct": "court",
    "pl": "place",
    "sq": "square",
    "hwy": "highway",
    "pkwy": "parkway",
    "apt": "apartment",
    "ste": "suite",
    "fl": "floor",
    "bldg": "building",
    "opp": "opposite",
    "nr": "near",
    "nxt": "next"
  }
}
```

---

## 5. Config Schema (configs/config.yaml)

```yaml
data:
  train_dir: "dataset/train"
  test_dir: "dataset/test"
  output_dir: "output"

normalization:
  abbreviation_file: "configs/abbreviations.json"
  unicode_form: "NFC"

embedding:
  model_name: "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
  batch_size: 256
  device: "auto"  # auto-detects CUDA

blocking:
  tfidf_top_k: 20         # ANN neighbors per query
  ngram_min_sim: 0.2      # minimum n-gram Jaccard to form candidate pair
  max_candidates_per_s1: 50  # hard cap to prevent explosion

matching:
  model_type: "lightgbm"
  n_estimators: 500
  learning_rate: 0.05
  max_depth: 8
  num_leaves: 63
  threshold: 0.5          # overwritten by val-set calibration

validation:
  split_ratio: 0.2
  random_seed: 42
```
