"""
tests/test_feature_engineer.py
Unit tests for feature engineering.
Run: pytest tests/test_feature_engineer.py -v
"""
import sys
import os
import math

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from feature_engineer import compute_pair_features, FEATURE_COLS


def _make_record(entity_id, norm_name, norm_address, country="US"):
    return {
        "entity_id": entity_id,
        "norm_name": norm_name,
        "norm_address": norm_address,
        "country": country,
    }


class TestComputePairFeatures:
    """Tests for compute_pair_features()."""

    def test_returns_all_expected_keys(self):
        s1 = _make_record("S1-001", "google corporation", "1600 amphitheatre parkway")
        c = _make_record("S2-001", "google corporation", "1600 amphitheatre parkway")
        features = compute_pair_features(s1, c)
        for col in FEATURE_COLS:
            assert col in features, f"Missing feature: {col}"

    def test_identical_records_high_similarity(self):
        s1 = _make_record("S1-001", "amazon incorporated", "410 terry avenue north")
        c = _make_record("S2-001", "amazon incorporated", "410 terry avenue north")
        features = compute_pair_features(s1, c)
        assert features["lev_name"] > 0.95
        assert features["tset_name"] > 0.95
        assert features["lev_addr"] > 0.95
        assert features["max_sim"] > 0.95

    def test_completely_different_records_low_similarity(self):
        s1 = _make_record("S1-001", "apple corporation", "one apple park way cupertino")
        c = _make_record("S2-001", "reliance private limited", "navi mumbai maharashtra")
        features = compute_pair_features(s1, c)
        assert features["lev_name"] < 0.5
        assert features["lev_addr"] < 0.5

    def test_same_country_returns_one(self):
        s1 = _make_record("S1-001", "abc", "def", country="US")
        c = _make_record("S2-001", "abc", "def", country="US")
        features = compute_pair_features(s1, c)
        assert features["country_match"] == 1.0

    def test_different_country_returns_zero(self):
        s1 = _make_record("S1-001", "abc", "def", country="US")
        c = _make_record("S2-001", "abc", "def", country="India")
        features = compute_pair_features(s1, c)
        assert features["country_match"] == 0.0

    def test_empty_name_sets_flags(self):
        s1 = _make_record("S1-001", "", "100 main road")
        c = _make_record("S2-001", "apple", "100 main road")
        features = compute_pair_features(s1, c)
        assert features["s1_name_empty"] == 1.0
        assert features["c_name_empty"] == 0.0

    def test_empty_address_sets_flags(self):
        s1 = _make_record("S1-001", "apple", "")
        c = _make_record("S2-001", "apple", "")
        features = compute_pair_features(s1, c)
        assert features["s1_addr_empty"] == 1.0
        assert features["c_addr_empty"] == 1.0

    def test_no_nan_or_inf_in_features(self):
        s1 = _make_record("S1-001", "test company", "123 test road")
        c = _make_record("S2-001", "test corp", "123 test rd")
        features = compute_pair_features(s1, c)
        for k, v in features.items():
            assert not math.isnan(v), f"NaN in feature: {k}"
            assert not math.isinf(v), f"Inf in feature: {k}"

    def test_no_nan_when_both_fields_empty(self):
        s1 = _make_record("S1-001", "", "")
        c = _make_record("S2-001", "", "")
        features = compute_pair_features(s1, c)
        for k, v in features.items():
            assert not math.isnan(v), f"NaN in feature {k} when both fields empty"

    def test_embedding_cosine_with_identical_vectors(self):
        emb = np.array([0.5, 0.5, 0.5, 0.5], dtype=np.float32)
        emb = emb / np.linalg.norm(emb)  # L2-normalize
        s1 = _make_record("S1-001", "test", "test")
        c = _make_record("S2-001", "test", "test")
        features = compute_pair_features(s1, c, s1_embedding=emb, candidate_embedding=emb)
        assert abs(features["cos_embed"] - 1.0) < 0.01

    def test_name_x_addr_is_product(self):
        s1 = _make_record("S1-001", "amazon", "410 terry avenue")
        c = _make_record("S2-001", "amazon corporation", "410 terry ave")
        features = compute_pair_features(s1, c)
        expected = features["tset_name"] * features["tset_addr"]
        assert abs(features["name_x_addr"] - expected) < 0.01

    def test_all_features_in_zero_one_range(self):
        """All similarity features must be in [0, 1]."""
        s1 = _make_record("S1-001", "google corporation", "1600 amphitheatre")
        c = _make_record("S2-001", "googl corp", "1600 amphitheatre pkwy")
        features = compute_pair_features(s1, c)
        bounded = [
            "lev_name", "jw_name", "ts_name", "tset_name", "partial_name",
            "lev_addr", "ts_addr", "tset_addr", "jaccard_addr", "partial_addr",
            "cos_embed", "len_diff_name", "max_name_sim", "max_addr_sim", "max_sim",
        ]
        for feat in bounded:
            v = features[feat]
            assert 0.0 <= v <= 1.0, f"Feature {feat}={v} out of [0,1]"

    def test_token_word_reorder_detected_by_token_set(self):
        # "abc xyz" vs "xyz abc" — token_set_ratio should be high
        s1 = _make_record("S1-001", "abc xyz", "")
        c = _make_record("S2-001", "xyz abc", "")
        features = compute_pair_features(s1, c)
        assert features["tset_name"] > 0.9
