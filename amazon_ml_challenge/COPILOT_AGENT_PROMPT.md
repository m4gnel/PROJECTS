# COPILOT AGENT PROMPT
# Paste this entire file into GitHub Copilot Chat in VS Code
# AFTER you have run fix_structure.bat and install.bat successfully

---

I am building an ML solution for the Amazon ML Challenge 2026 — Business Entity Resolution.

## My project is already set up at D:\WORK\PROJECTS\AMAZON_ML_CHALLENGE\

The full pipeline code already exists. Here is what I need you to help with:

## CURRENT STATE
All source files are written and in place:
- code/business_entity_resolution/src/ has all Python modules
- configs/config.yaml has all hyperparameters  
- dataset/train/ and dataset/test/ have all TSV data files
- requirements.txt has all dependencies (already installed)

## TASK: Run the pipeline and fix any errors

### Step 1 — Run the tests first
```
cd D:\WORK\PROJECTS\AMAZON_ML_CHALLENGE
python -m pytest code\business_entity_resolution\tests\ -v
```
If any tests fail, read the error and fix the corresponding file in code\business_entity_resolution\src\

### Step 2 — Run EDA
```
python notebooks\01_eda.py
```
Tell me what you see: how many rows, what countries, what singleton rate.

### Step 3 — Run blocking analysis
```
python notebooks\02_blocking_analysis.py
```
THE BLOCKING RECALL MUST BE >= 0.98. If it is not, edit blocker.py to fix it:
- Lower ngram_min_sim in configs/config.yaml from 0.2 to 0.1
- Increase tfidf_top_k from 20 to 30
- In blocker.py _bk2_ngram_index(), lower min_sim parameter

### Step 4 — Train
```
python code\business_entity_resolution\src\run_pipeline.py --mode train --config configs\config.yaml
```
Report the Val F0.5 score. It should be above 0.90.

### Step 5 — Predict
```
python code\business_entity_resolution\src\run_pipeline.py --mode predict --config configs\config.yaml
```

### Step 6 — Validate
```
python code\business_entity_resolution\utils\validate_submission.py --matching output\matching_results.tsv --candidate output\candidate_pairs.tsv --test-dir dataset\test
```
Must show PASS.

## IMPORTANT RULES — NEVER BREAK THESE
1. Never add any external API calls (no requests.get, no urllib, no geocoding)
2. Never one-hot encode the country column — only use country_match binary feature
3. The threshold calibration must optimize F0.5 NOT F1 — the code already does this correctly
4. Every S1 entity must appear in the output — even singletons with empty matched_entity_ids
5. Models must be MIT or Apache 2.0 license, maximum 8 billion parameters
6. Never train on the validation split (20% held out, seed=42)

## IF TESTS FAIL — COMMON FIXES

### ImportError / ModuleNotFoundError
Run: pip install -r code\business_entity_resolution\requirements.txt

### test_normalizer fails on abbreviation expansion
In normalizer.py, check that _NAME_ABBREVS is loaded before calling _expand_abbreviations()
The initialize() function must be called first. In the test, add:
```python
from normalizer import initialize
initialize()
```

### test_blocker fails on blocking recall < 0.95
This is OK on the mini synthetic dataset. The real test is on actual competition data.

### test_evaluator F0.5 formula mismatch
The exact formula is: F0.5 = (1.25 * P * R) / (0.25 * P + R)
Verify this is what evaluator.py computes in compute_f05_per_entity()

## AFTER FIRST SUCCESSFUL SUBMISSION

Once we get our baseline score, improve in this order:

### Improvement 1: Better blocking (do this if blocking recall < 0.99)
In configs/config.yaml:
- Change tfidf_top_k: 20 to tfidf_top_k: 30
- Change ngram_min_sim: 0.2 to ngram_min_sim: 0.15
- Change max_candidates_per_s1: 100 to max_candidates_per_s1: 150

### Improvement 2: Add cross-encoder feature
In feature_engineer.py, add this to compute_pair_features():
```python
from sentence_transformers import CrossEncoder
# Load once globally at module level:
_ce_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")  # Apache 2.0, 22M params

# In compute_pair_features():
s1_text = s1_record.get("norm_text", "")
c_text = candidate_record.get("norm_text", "")
if s1_text and c_text:
    ce_score = float(_ce_model.predict([(s1_text, c_text)])[0])
    ce_score = max(0.0, min(1.0, (ce_score + 10) / 20))  # normalize to [0,1]
else:
    ce_score = 0.0
```
Add "ce_score" to the returned dict and to FEATURE_COLS list.

### Improvement 3: Ensemble
In matcher.py train_matcher(), train 3 models with seeds 42, 123, 777.
In predict_scores(), average the predict_proba outputs from all 3 models.

## FILE STRUCTURE FOR REFERENCE
```
D:\WORK\PROJECTS\AMAZON_ML_CHALLENGE\
├── code\business_entity_resolution\src\
│   ├── run_pipeline.py     ← ENTRYPOINT
│   ├── blocker.py          ← Edit if blocking recall < 0.98
│   ├── feature_engineer.py ← Edit to add cross-encoder feature
│   ├── matcher.py          ← Edit for ensemble
│   ├── evaluator.py        ← F0.5 formula (don't change)
│   └── postprocessor.py    ← Output writer (don't change)
├── configs\config.yaml     ← Tune hyperparameters here
├── dataset\train\          ← Training TSVs
├── dataset\test\           ← Test TSVs
└── output\                 ← Results go here
```
