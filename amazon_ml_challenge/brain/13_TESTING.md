# 13_TESTING.md
# Test Plan & Test Cases

## 1. Unit Tests

### test_normalizer.py
```python
import pytest
from src.normalizer import normalize_text

class TestNormalizeText:
    def test_none_input(self):
        assert normalize_text(None) == ""
    
    def test_nan_input(self):
        import math
        assert normalize_text(float('nan')) == ""
    
    def test_lowercase(self):
        assert normalize_text("GOOGLE LLC") == "google limited liability company"
    
    def test_corp_expansion(self):
        assert "corporation" in normalize_text("Amazon Corp")
    
    def test_pvt_ltd_expansion(self):
        result = normalize_text("Reliance Pvt Ltd")
        assert "private" in result and "limited" in result
    
    def test_ampersand_expansion(self):
        assert "and" in normalize_text("Johnson & Johnson")
    
    def test_address_rd_to_road(self):
        result = normalize_text("123 Main Rd", field="address")
        assert "road" in result
    
    def test_unicode_normalization(self):
        result = normalize_text("Café Parisien")
        assert result == "cafe parisien"
    
    def test_whitespace_collapse(self):
        assert normalize_text("  A   B  ") == "a b"
    
    def test_punctuation_removal(self):
        result = normalize_text("Google, Inc.")
        assert "," not in result and "." not in result
```

### test_blocker.py
```python
class TestBlocker:
    def test_blocking_recall_above_threshold(self, sample_train_data, sample_gt):
        candidates = build_blocking_index(sample_train_data['s1'], 
                                          sample_train_data['s23'])
        recall = compute_blocking_recall(candidates, sample_gt)
        assert recall >= 0.98, f"Blocking recall {recall:.3f} < 0.98"
    
    def test_all_s1_ids_in_candidates(self, sample_data):
        candidates = build_blocking_index(...)
        for s1_id in sample_data['s1']['entity_id']:
            assert s1_id in candidates
    
    def test_no_s1_ids_in_candidate_lists(self, sample_data):
        candidates = build_blocking_index(...)
        for s1_id, cand_list in candidates.items():
            for c in cand_list:
                assert not c.startswith("S1-"), f"S1 ID {c} in candidate list"
    
    def test_no_duplicate_candidates(self, sample_data):
        candidates = build_blocking_index(...)
        for cand_list in candidates.values():
            assert len(cand_list) == len(set(cand_list))
```

### test_evaluator.py
```python
class TestF05:
    def test_perfect_singleton(self):
        assert compute_f05_per_entity([], []) == 1.0
    
    def test_false_merge_singleton(self):
        assert compute_f05_per_entity(["S2-001"], []) == 0.0
    
    def test_missed_all(self):
        assert compute_f05_per_entity([], ["S2-001"]) == 0.0
    
    def test_perfect_match(self):
        assert compute_f05_per_entity(["S2-001"], ["S2-001"]) == 1.0
    
    def test_partial_match_formula(self):
        # predicted 3, GT 2, overlap 2
        # P = 2/3, R = 1.0
        # F0.5 = 1.25 * (2/3) * 1.0 / (0.25 * (2/3) + 1.0)
        predicted = ["S2-001", "S2-002", "S2-003"]
        gt = ["S2-001", "S2-002"]
        score = compute_f05_per_entity(predicted, gt)
        assert abs(score - 0.714) < 0.01
    
    def test_macro_average(self):
        predictions = {"S1-001": ["S2-001"], "S1-002": [], "S1-003": ["S3-001"]}
        gt = {"S1-001": ["S2-001"], "S1-002": [], "S1-003": []}
        result = compute_macro_f05(predictions, gt)
        # S1-001: 1.0, S1-002: 1.0, S1-003: 0.0 → macro = 0.667
        assert abs(result['macro_f05'] - 0.667) < 0.01
```

---

## 2. Integration Tests

### test_full_pipeline.py
```python
def test_pipeline_produces_valid_output(tmp_path):
    """Run full pipeline on small synthetic dataset, check output passes validator."""
    # Create synthetic TSVs (10 S1, 15 S2, 15 S3, 5 GT matches)
    # Run pipeline
    # Run validate_submission.py
    # Assert exit code 0
```

### test_output_format.py
```python
def test_every_s1_has_row(matching_results, test_s1_ids):
    assert set(matching_results['source1_entity_id']) == set(test_s1_ids)

def test_no_duplicate_rows(matching_results):
    assert not matching_results['source1_entity_id'].duplicated().any()

def test_matched_ids_only_s2_s3(matching_results, test_s23_ids):
    for _, row in matching_results.iterrows():
        if row['matched_entity_ids']:
            for mid in row['matched_entity_ids'].split(','):
                assert mid in test_s23_ids

def test_matching_subset_of_candidates(matching_results, candidate_pairs):
    # All matched IDs must appear in candidate_pairs
    ...
```

---

## 3. Regression Tests

After any code change, verify:
1. Blocking recall on training set stays ≥ 0.98
2. Validation F₀.₅ stays ≥ previous best
3. `validate_submission.py` returns PASS

---

## 4. Test Data (Synthetic)

Store in `tests/fixtures/`:
- `mini_source1.tsv` — 20 records
- `mini_source2.tsv` — 25 records
- `mini_source3.tsv` — 25 records
- `mini_ground_truth.tsv` — 8 matches, 12 singletons

Covers:
- Exact name match
- Name with abbreviation difference
- Name with typo
- Address only partial
- Singleton (no match)
- Multi-match (1 S1 → 2 S2 records)
- Cross-source match (S1 → S2 AND S3)
- Empty address field
