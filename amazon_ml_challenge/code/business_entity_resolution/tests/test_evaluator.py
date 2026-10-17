"""
tests/test_evaluator.py
Unit tests for the F₀.₅ evaluation metric.
Run: pytest tests/test_evaluator.py -v
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from evaluator import compute_f05_per_entity, compute_macro_f05, compute_blocking_recall


class TestF05PerEntity:
    """Tests for compute_f05_per_entity()."""

    def test_both_empty_is_perfect_singleton(self):
        f05, prec, rec = compute_f05_per_entity([], [])
        assert f05 == 1.0
        assert prec == 1.0
        assert rec == 1.0

    def test_false_merge_on_singleton_is_zero(self):
        f05, prec, rec = compute_f05_per_entity(["S2-001"], [])
        assert f05 == 0.0

    def test_missed_all_is_zero(self):
        f05, prec, rec = compute_f05_per_entity([], ["S2-001"])
        assert f05 == 0.0

    def test_perfect_single_match(self):
        f05, prec, rec = compute_f05_per_entity(["S2-001"], ["S2-001"])
        assert f05 == 1.0
        assert prec == 1.0
        assert rec == 1.0

    def test_perfect_multiple_matches(self):
        f05, prec, rec = compute_f05_per_entity(
            ["S2-001", "S3-002"], ["S2-001", "S3-002"]
        )
        assert f05 == 1.0

    def test_partial_match_precision_recall(self):
        # predicted 3, GT 2, overlap 2
        # P = 2/3, R = 1.0
        # F0.5 = (1.25 * (2/3) * 1.0) / (0.25 * (2/3) + 1.0)
        #       = 0.8333 / (0.1667 + 1.0) = 0.8333 / 1.1667 ≈ 0.7143
        f05, prec, rec = compute_f05_per_entity(
            ["S2-001", "S2-002", "S2-003"],
            ["S2-001", "S2-002"]
        )
        assert abs(f05 - 0.7143) < 0.01
        assert abs(prec - 2/3) < 0.01
        assert abs(rec - 1.0) < 0.01

    def test_recall_zero_when_no_overlap(self):
        f05, prec, rec = compute_f05_per_entity(
            ["S2-999"],
            ["S2-001"]
        )
        assert f05 == 0.0

    def test_order_doesnt_matter(self):
        f05_a, _, _ = compute_f05_per_entity(["S2-001", "S2-002"], ["S2-002", "S2-001"])
        f05_b, _, _ = compute_f05_per_entity(["S2-002", "S2-001"], ["S2-001", "S2-002"])
        assert f05_a == f05_b == 1.0

    def test_duplicates_in_predicted_treated_as_set(self):
        # Duplicates in pred should be deduplicated (caller should do this,
        # but evaluator uses sets so it's safe either way)
        f05_a, _, _ = compute_f05_per_entity(["S2-001"], ["S2-001"])
        f05_b, _, _ = compute_f05_per_entity(["S2-001", "S2-001"], ["S2-001"])
        assert f05_a == f05_b

    def test_formula_correctness(self):
        """Verify F₀.₅ formula: (1.25 * P * R) / (0.25 * P + R)"""
        # P=0.8, R=0.5
        # F0.5 = (1.25 * 0.8 * 0.5) / (0.25 * 0.8 + 0.5)
        #       = 0.5 / (0.2 + 0.5) = 0.5 / 0.7 ≈ 0.7143
        f05, prec, rec = compute_f05_per_entity(
            ["S2-001", "S2-002", "S2-003", "S2-004", "S2-999"],  # 5 predicted
            ["S2-001", "S2-002", "S2-003", "S2-004", "S2-005", "S2-006",
             "S2-007", "S2-008", "S2-009", "S2-010"]  # 10 GT, overlap 4
        )
        # P = 4/5 = 0.8, R = 4/10 = 0.4
        # F0.5 = (1.25 * 0.8 * 0.4) / (0.25 * 0.8 + 0.4) = 0.4 / (0.2 + 0.4)
        #      = 0.4 / 0.6 ≈ 0.6667
        assert abs(prec - 0.8) < 0.01
        assert abs(rec - 0.4) < 0.01
        assert abs(f05 - 0.6667) < 0.01


class TestMacroF05:
    """Tests for compute_macro_f05()."""

    def test_all_singletons_correct(self):
        preds = {"S1-001": [], "S1-002": [], "S1-003": []}
        gt = {"S1-001": [], "S1-002": [], "S1-003": []}
        result = compute_macro_f05(preds, gt)
        assert result["macro_f05"] == 1.0
        assert result["n_singletons"] == 3
        assert result["n_correct_singletons"] == 3

    def test_mixed_singletons_and_matches(self):
        preds = {"S1-001": ["S2-001"], "S1-002": [], "S1-003": ["S3-001"]}
        gt = {"S1-001": ["S2-001"], "S1-002": [], "S1-003": []}
        result = compute_macro_f05(preds, gt)
        # S1-001: F₀.₅=1.0, S1-002: F₀.₅=1.0, S1-003: F₀.₅=0.0
        assert abs(result["macro_f05"] - (1.0 + 1.0 + 0.0) / 3) < 0.01

    def test_false_merge_on_singleton_penalized(self):
        preds = {"S1-001": ["S2-999"]}  # wrong match on singleton
        gt = {"S1-001": []}
        result = compute_macro_f05(preds, gt)
        assert result["macro_f05"] == 0.0
        assert result["n_false_merges"] == 1

    def test_missing_s1_in_predictions_treated_as_empty(self):
        # S1-002 missing from predictions → treated as []
        preds = {"S1-001": ["S2-001"]}
        gt = {"S1-001": ["S2-001"], "S1-002": []}
        result = compute_macro_f05(preds, gt)
        # S1-001: 1.0, S1-002: 1.0 (correct singleton)
        assert abs(result["macro_f05"] - 1.0) < 0.01


class TestBlockingRecall:
    """Tests for compute_blocking_recall()."""

    def test_perfect_recall(self):
        candidates = {"S1-001": ["S2-001", "S3-002"], "S1-002": ["S2-003"]}
        gt = {"S1-001": ["S2-001", "S3-002"], "S1-002": ["S2-003"]}
        result = compute_blocking_recall(candidates, gt)
        assert result["blocking_recall"] == 1.0

    def test_partial_recall(self):
        candidates = {"S1-001": ["S2-001"], "S1-002": ["S2-003"]}
        gt = {"S1-001": ["S2-001", "S3-002"], "S1-002": ["S2-003"]}
        # Covered: 2 out of 3 GT pairs
        result = compute_blocking_recall(candidates, gt)
        assert abs(result["blocking_recall"] - 2/3) < 0.01
        assert result["n_missed"] == 1

    def test_no_candidates_zero_recall(self):
        candidates = {"S1-001": []}
        gt = {"S1-001": ["S2-001"]}
        result = compute_blocking_recall(candidates, gt)
        assert result["blocking_recall"] == 0.0

    def test_empty_gt_no_pairs_full_recall(self):
        # No GT pairs means nothing to cover → recall = 1.0 (vacuously)
        candidates = {"S1-001": []}
        gt = {"S1-001": []}
        result = compute_blocking_recall(candidates, gt)
        assert result["n_gt_pairs"] == 0
