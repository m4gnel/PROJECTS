# 03_ARCHITECTURE.md
# System Architecture — Entity Resolution Pipeline

## Pipeline Overview

```
RAW TSVs
   │
   ▼
┌─────────────────────────────────┐
│  STAGE 1: Data Loading          │  src/data_loader.py
│  - Read all 6 TSV files         │
│  - Validate columns & IDs       │
│  - Build source lookup dicts    │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│  STAGE 2: Text Normalization    │  src/normalizer.py
│  - Unicode NFC                  │
│  - Lowercase                    │
│  - Abbreviation expansion       │
│  - Punctuation strip            │
│  - Whitespace collapse          │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│  STAGE 3: Blocking / Candidate  │  src/blocker.py
│  Generation                     │
│                                 │
│  BK-1: TF-IDF ANN (FAISS)      │
│  BK-2: n-gram inverted index    │
│  BK-3: Phonetic key             │
│  BK-4: Country+name-prefix      │
│  BK-5: Address token overlap    │
│                                 │
│  UNION of all blocking keys     │
│  → candidate_pairs.tsv          │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│  STAGE 4: Feature Engineering   │  src/feature_engineer.py
│  - String similarity features   │
│  - Semantic embedding cosine    │
│  - Structural features          │
│  → Feature matrix for each pair │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│  STAGE 5: ML Matching Model     │  src/matcher.py
│  - LightGBM classifier          │
│  - Trained on train split       │
│  - Threshold from val split     │
│  → Scored candidate pairs       │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│  STAGE 6: Post-processing       │  src/postprocessor.py
│  - Apply threshold              │
│  - Deduplicate IDs in lists     │
│  - Ensure every S1 has a row    │
│  - Empty matched_entity_ids     │
│    for singletons               │
│  → matching_results.tsv         │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│  STAGE 7: Validation            │  utils/validate_submission.py
│  - Run official validator       │
│  - Print PASS or issues list    │
└─────────────────────────────────┘
```

---

## Directory Structure

```
amazon_ml_challenge_submission/
├── brain/                          # Strategy & planning docs (this folder)
│   ├── 00_MASTER_RULES.md
│   ├── 01_PRD.md
│   ├── 02_TRD.md
│   ├── 03_ARCHITECTURE.md
│   ├── 04_DATA_MODEL.md
│   ├── 05_DATA_SOURCES.md
│   ├── 06_SCRAPING_SPEC.md        # (N/A - external data prohibited)
│   ├── 07_API_CONTRACT.md
│   ├── 08_UI_SPEC.md              # (N/A - no UI)
│   ├── 09_ERROR_HANDLING.md
│   ├── 10_SECURITY.md
│   ├── 11_ADMOB_SPEC.md           # (N/A - no ads)
│   ├── 12_GITHUB_ACTIONS.md
│   ├── 13_TESTING.md
│   ├── 14_PRODUCTION_CHECKLIST.md
│   ├── 15_MICROTASKS.md
│   ├── 16_CHANGELOG.md
│   └── 17_DECISIONS.md
│
├── dataset/
│   ├── train/
│   │   ├── train_source1.tsv
│   │   ├── train_source2.tsv
│   │   ├── train_source3.tsv
│   │   └── train_ground_truth.tsv
│   └── test/
│       ├── test_source1.tsv
│       ├── test_source2.tsv
│       └── test_source3.tsv
│
├── output/
│   ├── matching_results.tsv        # ← UPLOAD THIS TO LEADERBOARD
│   └── candidate_pairs.tsv
│
├── configs/
│   ├── config.yaml                 # All hyperparameters
│   └── abbreviations.json          # Abbreviation expansion dict
│
├── notebooks/
│   ├── 01_eda.ipynb                # EDA — run first
│   ├── 02_blocking_analysis.ipynb  # Measure blocking recall
│   └── 03_model_analysis.ipynb     # Feature importance, threshold tuning
│
├── code/
│   └── business_entity_resolution/
│       ├── src/
│       │   ├── __init__.py
│       │   ├── run_pipeline.py     # ENTRYPOINT: python src/run_pipeline.py
│       │   ├── data_loader.py
│       │   ├── normalizer.py
│       │   ├── blocker.py
│       │   ├── embedder.py
│       │   ├── feature_engineer.py
│       │   ├── matcher.py
│       │   ├── postprocessor.py
│       │   ├── evaluator.py
│       │   └── config.py
│       ├── utils/
│       │   └── validate_submission.py
│       ├── tests/
│       │   ├── test_normalizer.py
│       │   ├── test_blocker.py
│       │   ├── test_feature_engineer.py
│       │   └── test_evaluator.py
│       ├── README.md
│       └── requirements.txt
│
└── Documentation_template.md       # Filled methodology doc
```

---

## Module Responsibilities

| Module | Input | Output | Key Libraries |
|---|---|---|---|
| `data_loader.py` | TSV file paths | pandas DataFrames | pandas |
| `normalizer.py` | raw text string | normalized string | re, unicodedata |
| `blocker.py` | normalized DataFrames | Dict[s1_id → List[candidates]] | sklearn, faiss, rapidfuzz |
| `embedder.py` | List[str] | np.ndarray embeddings | sentence-transformers |
| `feature_engineer.py` | pair (s1_record, candidate_record) | feature dict | rapidfuzz, numpy |
| `matcher.py` | feature DataFrame | probability scores | lightgbm |
| `postprocessor.py` | scored pairs + threshold | matching_results DataFrame | pandas |
| `evaluator.py` | predictions + ground_truth | F₀.₅ score dict | numpy |
| `run_pipeline.py` | config.yaml | TSV output files | all above |

---

## Data Flow for Test Inference

```
test_source1.tsv → normalize → embed → build FAISS index (S1)
test_source2.tsv → normalize → embed → query FAISS against S1
test_source3.tsv → normalize → embed → query FAISS against S1
                                ↓
                   + n-gram blocking keys
                                ↓
                   candidate_pairs dict
                                ↓
                   feature_engineer (per candidate pair)
                                ↓
                   matcher.predict_proba()
                                ↓
                   postprocess(threshold=BEST_THRESH)
                                ↓
                   write matching_results.tsv
                   write candidate_pairs.tsv
```
