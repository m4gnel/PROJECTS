# 14_PRODUCTION_CHECKLIST.md
# Pre-Submission Production Checklist

## Phase 1: Development Complete ✅

- [ ] All modules implemented per API contracts in `07_API_CONTRACT.md`
- [ ] Unit tests pass: `pytest tests/ -v` → 0 failures
- [ ] Integration test passes: full pipeline runs end-to-end on mini dataset
- [ ] EDA complete: know data shapes, match distributions, country breakdown
- [ ] Abbreviation dict covers all observed patterns in training data
- [ ] Blocking recall measured: **must be ≥ 0.98 on training GT**
- [ ] Hard negatives mined and included in training data

## Phase 2: Model Trained & Validated ✅

- [ ] Train/validation split is FIXED (seed=42, 80/20)
- [ ] LightGBM trained on train split, never on val split
- [ ] Threshold calibrated on val split for F₀.₅ (NOT F₁)
- [ ] Val F₀.₅ ≥ 0.90
- [ ] Feature importance reviewed — top features make intuitive sense
- [ ] Model serialized to `models/matcher.pkl`

## Phase 3: Test Set Inference ✅

- [ ] Loaded `test_source1.tsv`, `test_source2.tsv`, `test_source3.tsv`
- [ ] Normalized all test records
- [ ] Generated embeddings for all test records
- [ ] Built blocking candidates for all test records
- [ ] Feature matrix built for all test candidate pairs
- [ ] Model inference complete
- [ ] Threshold applied
- [ ] `output/matching_results.tsv` written
- [ ] `output/candidate_pairs.tsv` written

## Phase 4: Output Validation ✅

- [ ] Run: `python utils/validate_submission.py --matching output/matching_results.tsv --candidate output/candidate_pairs.tsv --test-dir dataset/test`
- [ ] Result: **PASS (exit 0)**
- [ ] Manually spot-check 10 random rows — do they look reasonable?
- [ ] Count: number of predicted matches vs singletons — does ratio make sense?
- [ ] Verify: no S1 IDs appear in matched_entity_ids column
- [ ] Verify: file is tab-separated (open in text editor, check for tabs)

## Phase 5: Submission Package ✅

- [ ] `output/matching_results.tsv` is the SAME file validated in Phase 4
- [ ] `output/candidate_pairs.tsv` is present
- [ ] `code/business_entity_resolution/README.md` has step-by-step run instructions
- [ ] `requirements.txt` has ALL dependencies with pinned versions
- [ ] `Documentation_template.md` filled in completely
- [ ] Zip created: `<TeamName>_submission.zip`
- [ ] Zip structure matches required format (output/, code/, Documentation_template.md)

## Phase 6: Upload ✅

- [ ] Upload `output/matching_results.tsv` to Portal (NOT the zip)
- [ ] Check leaderboard for SCORED status (not FAILED or INVALID)
- [ ] Note public leaderboard F₀.₅ score in `configs/experiments.json`
- [ ] Final zip uploaded separately as required

---

## ⚠️ RED FLAGS — Stop and Fix Before Submitting

- Blocking recall < 0.95 on training GT → revisit blocking keys
- Val F₀.₅ < 0.85 → debug features or threshold
- `validate_submission.py` returns any ERROR → fix before uploading
- `output/matching_results.tsv` has no tab character → wrong delimiter
- Empty file or file < 1KB → something went wrong in postprocessing
- More than 5% of S1 entities predicted as all-matching → threshold too low
- 100% singletons predicted → threshold too high
