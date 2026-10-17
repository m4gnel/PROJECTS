# MASTER AGENT PROMPT
# Amazon ML Challenge 2026 — Entity Resolution
# Give this ENTIRE file to GitHub Copilot / Cursor / any vibe-coding agent

---

## ROLE
You are an expert ML engineer helping me win the Amazon ML Challenge 2026. The task is Business Entity Resolution (ER): matching noisy business records across 3 data sources. The scoring metric is **F₀.₅** (precision-weighted — false positives are penalized 2× more than false negatives). I need to place **first**.

---

## PROJECT STRUCTURE (already created — do not recreate)

```
amazon_ml_challenge/
├── brain/                         # All strategy docs (already written)
├── configs/
│   ├── config.yaml                # Hyperparameters
│   └── abbreviations.json         # Abbreviation expansion dict
├── dataset/
│   ├── train/                     # Put competition TSV files here
│   └── test/
├── output/                        # Pipeline writes here
├── models/                        # Trained model saved here
├── notebooks/
│   ├── 01_eda.py
│   └── 02_blocking_analysis.py
├── code/business_entity_resolution/
│   ├── src/
│   │   ├── run_pipeline.py        # MAIN ENTRYPOINT
│   │   ├── config.py
│   │   ├── data_loader.py
│   │   ├── normalizer.py
│   │   ├── blocker.py
│   │   ├── embedder.py
│   │   ├── feature_engineer.py
│   │   ├── matcher.py
│   │   ├── postprocessor.py
│   │   └── evaluator.py
│   ├── tests/
│   │   ├── test_normalizer.py
│   │   ├── test_evaluator.py
│   │   ├── test_feature_engineer.py
│   │   └── test_blocker.py
│   ├── utils/
│   │   └── validate_submission.py
│   ├── README.md
│   └── requirements.txt
├── Documentation_template.md
└── Makefile
```

---

## TASK 1 — SETUP (do this first)

```bash
cd amazon_ml_challenge
pip install -r code/business_entity_resolution/requirements.txt
```

Then place the competition data files in `dataset/train/` and `dataset/test/`:
- `train_source1.tsv`, `train_source2.tsv`, `train_source3.tsv`, `train_ground_truth.tsv`
- `test_source1.tsv`, `test_source2.tsv`, `test_source3.tsv`

---

## TASK 2 — RUN EDA

```bash
python notebooks/01_eda.py
```

Read the output carefully. Note:
- How many rows per source
- Null rates in business_name and business_address
- Country distribution (US, India in train; France also in test)
- Singleton rate (S1 entities with 0 GT matches)
- Sample positive pairs — what kinds of noise do you see?

---

## TASK 3 — TEST THE CODE

```bash
cd code/business_entity_resolution
python -m pytest tests/ -v
```

ALL tests must pass. If any fail, fix the corresponding source file in `src/`. Do not change the tests unless there is a genuine design error.

Common fixes needed:
- `test_normalizer.py` — check abbreviation expansion logic in `normalizer.py`
- `test_evaluator.py` — verify F₀.₅ formula in `evaluator.py`
- `test_blocker.py` — verify all 5 blocking keys fire correctly

---

## TASK 4 — ANALYZE BLOCKING

```bash
python notebooks/02_blocking_analysis.py
```

**CRITICAL GATE**: Blocking recall must be ≥ 0.98. If it is not:
1. Lower `ngram_min_sim` in `configs/config.yaml` from 0.2 to 0.1
2. Increase `tfidf_top_k` from 20 to 30
3. Add a 6th blocking key in `blocker.py`: trigrams on address
4. Do NOT proceed to training until blocking recall ≥ 0.98

---

## TASK 5 — TRAIN MODEL

```bash
python code/business_entity_resolution/src/run_pipeline.py --mode train --config configs/config.yaml
```

Watch the output for:
1. `BLOCKING RECALL: X.XXXX` — must be ≥ 0.98
2. `Best threshold: X.XX → Val F₀.₅: X.XXXX` — target ≥ 0.90
3. Feature importance log — top features should be tset_name, cos_embed, tset_addr

If Val F₀.₅ < 0.85:
- Check feature matrix for NaN values
- Increase hard_negative_ratio to 8
- Add more blocking keys

---

## TASK 6 — PREDICT ON TEST SET

```bash
python code/business_entity_resolution/src/run_pipeline.py --mode predict --config configs/config.yaml
```

This writes:
- `output/matching_results.tsv`
- `output/candidate_pairs.tsv`

---

## TASK 7 — VALIDATE OUTPUT (MANDATORY)

```bash
python code/business_entity_resolution/utils/validate_submission.py \
    --matching output/matching_results.tsv \
    --candidate output/candidate_pairs.tsv \
    --test-dir dataset/test
```

**Must see: `PASS`**. Do NOT submit if you see any ERROR.

Common errors and fixes:
- "Missing S1 entities" → postprocessor.py not adding all s1_ids
- "matched ID not in test S2/S3" → ID filtering bug in postprocessor.py
- "duplicate source1_entity_id rows" → deduplication bug
- "matched-but-not-candidate" → candidate set not including all matches

---

## TASK 8 — SUBMIT TO LEADERBOARD

Upload `output/matching_results.tsv` to the competition portal.
Record the public leaderboard F₀.₅ score.

---

## TASK 9 — ITERATE TO WIN

After baseline submission, try these improvements IN ORDER:

### Improvement A: Increase blocking top_k (quick win)
In `configs/config.yaml`, change `tfidf_top_k: 20` → `tfidf_top_k: 30`
Then retrain and resubmit. This increases recall ceiling.

### Improvement B: Add cross-encoder reranking
Install: `pip install sentence-transformers`
Add to `src/feature_engineer.py`:
```python
from sentence_transformers import CrossEncoder
ce_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")  # Apache 2.0

def get_cross_encoder_score(text_a, text_b, model):
    score = model.predict([(text_a, text_b)])[0]
    return float(score)
```
Add `ce_score` to features. Expected improvement: +0.01–0.03 F₀.₅.

### Improvement C: Ensemble LightGBM
Train 3 models with seeds 42, 123, 777.
Average their predict_proba outputs before thresholding.
Expected improvement: +0.005–0.01 F₀.₅.

### Improvement D: Better embedding model
Change `model_name` in config.yaml to `BAAI/bge-m3` (Apache 2.0, ~570M params).
This is stronger for multilingual matching especially for French test entities.

### Improvement E: Feature engineering additions
Add to `feature_engineer.py`:
- Longest common subsequence ratio
- Number of shared tokens (intersection count)
- Number of unique tokens in each (for length normalization)
- First-token-exact-match binary flag

---

## ABSOLUTE RULES (NEVER VIOLATE)

1. **NO external APIs** — no requests.get(), no geocoding, no business lookup
2. **Model ≤ 8B params, MIT/Apache 2.0** — check license before using any model
3. **Never one-hot encode country** — use only `country_match` binary feature
4. **Always run validate_submission.py before uploading**
5. **Threshold must optimize F₀.₅, not F₁** — the calibration code already does this
6. **Every S1 entity must have exactly one row in output** — even singletons
7. **matched_entity_ids must only contain S2/S3 IDs from the test set**
8. **France is in the test set but not in training** — never hard-code country logic

---

## COMPETITION SCORING

```
F₀.₅ = (1.25 × Precision × Recall) / (0.25 × Precision + Recall)
```

- Macro-averaged per S1 entity
- Singleton correctly predicted empty → 1.0
- Singleton with any prediction → 0.0
- **When uncertain: predict empty (singleton). Safety > recall.**

---

## QUICK REFERENCE COMMANDS

```bash
# Full pipeline in one shot
make full

# Validate before submit (never skip this)
make validate

# Run tests
make test

# Package for final zip submission
make package
```

---

## FILES TO WATCH DURING DEVELOPMENT

| File | When to edit |
|---|---|
| `configs/config.yaml` | Tune hyperparameters |
| `configs/abbreviations.json` | Add new abbrev patterns |
| `src/blocker.py` | Blocking recall < 0.98 |
| `src/feature_engineer.py` | Add new similarity features |
| `src/matcher.py` | Change model type or neg sampling |
| `brain/17_DECISIONS.md` | Record all architectural decisions |
| `brain/16_CHANGELOG.md` | Record every experiment result |
| `Documentation_template.md` | Fill in before final submission |

---

## EXPECTED TIMELINE

| Time | Task | Expected Score |
|---|---|---|
| Hour 1 | Setup + EDA + tests pass | - |
| Hour 2 | Blocking analysis (recall ≥ 0.98) | - |
| Hour 3 | Train + first submission | ~0.85–0.88 |
| Hour 4 | Add embeddings + hard negatives | ~0.90–0.92 |
| Hour 5 | Cross-encoder + ensemble | ~0.93–0.95 |
| Final | Package + documentation | TOP 3 |

---

## START COMMAND

Run this to begin:
```bash
cd amazon_ml_challenge && make eda
```
