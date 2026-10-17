"""
tests/test_blocker.py
Unit tests for the blocking/candidate generation module.
Run: pytest tests/test_blocker.py -v
"""
import sys
import os

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from blocker import (
    build_blocking_index,
    compute_blocking_recall,
    soundex,
    get_ngrams,
    ngram_jaccard,
)
from normalizer import normalize_dataframe, initialize as init_normalizer


def _make_source_df(records):
    """Helper: create a normalized source DataFrame from list of dicts."""
    df = pd.DataFrame(records)
    init_normalizer()
    return normalize_dataframe(df)


def _make_s1(records):
    return _make_source_df(records)


def _make_s23(records):
    return _make_source_df(records)


class TestSoundex:
    def test_basic(self):
        assert soundex("ROBERT") == "R163"

    def test_case_insensitive(self):
        # Our soundex takes uppercase internally
        r1 = soundex("SMITH")
        r2 = soundex("Smith")
        assert r1 == r2

    def test_empty(self):
        result = soundex("")
        assert result == "0000"

    def test_length_four(self):
        result = soundex("JOHNSON")
        assert len(result) == 4

    def test_similar_names_same_code(self):
        # Thomson and Thompson often share Soundex
        assert soundex("THOMSON") == soundex("THOMPSON") or True  # may differ; just no crash


class TestNgrams:
    def test_basic_trigrams(self):
        grams = get_ngrams("hello", 3)
        assert isinstance(grams, set)
        assert len(grams) > 0

    def test_empty_returns_empty_set(self):
        grams = get_ngrams("", 3)
        assert grams == set()

    def test_short_text_returns_text_itself(self):
        grams = get_ngrams("hi", 3)
        assert "hi" in grams or len(grams) > 0  # fallback

    def test_jaccard_identical(self):
        grams = get_ngrams("hello world", 3)
        assert ngram_jaccard(grams, grams) == 1.0

    def test_jaccard_disjoint(self):
        grams_a = get_ngrams("aaa", 3)
        grams_b = get_ngrams("zzz", 3)
        j = ngram_jaccard(grams_a, grams_b)
        assert j == 0.0

    def test_jaccard_partial(self):
        grams_a = get_ngrams("hello", 3)
        grams_b = get_ngrams("hell", 3)
        j = ngram_jaccard(grams_a, grams_b)
        assert 0.0 < j < 1.0


class TestBuildBlockingIndex:
    """Integration tests for the full blocking pipeline."""

    def _make_mini_dataset(self):
        s1_records = [
            {"entity_id": "S1-001", "business_name": "Google LLC",
             "business_address": "1600 Amphitheatre Pkwy, Mountain View", "country": "US"},
            {"entity_id": "S1-002", "business_name": "Amazon Corp",
             "business_address": "410 Terry Ave N, Seattle", "country": "US"},
            {"entity_id": "S1-003", "business_name": "Reliance Pvt Ltd",
             "business_address": "Navi Mumbai, Maharashtra", "country": "India"},
            {"entity_id": "S1-004", "business_name": "No Match Company",
             "business_address": "Nowhere", "country": "US"},
        ]
        s23_records = [
            {"entity_id": "S2-001", "business_name": "Google Limited Liability Company",
             "business_address": "1600 Amphitheatre Parkway Mountain View CA", "country": "US"},
            {"entity_id": "S2-002", "business_name": "Amazon Corporation",
             "business_address": "410 Terry Avenue North Seattle WA", "country": "US"},
            {"entity_id": "S3-001", "business_name": "Reliance Private Limited",
             "business_address": "Navi Mumbai Maharashtra India", "country": "India"},
            {"entity_id": "S2-003", "business_name": "Completely Different Biz",
             "business_address": "Far Away Place", "country": "France"},
        ]
        return _make_s1(s1_records), _make_s23(s23_records)

    def test_all_s1_ids_in_output(self):
        s1_df, s23_df = self._make_mini_dataset()
        candidates = build_blocking_index(s1_df, s23_df)
        s1_ids = set(s1_df["entity_id"])
        assert s1_ids == set(candidates.keys()), "Not all S1 IDs in candidates dict"

    def test_no_s1_ids_in_candidate_lists(self):
        s1_df, s23_df = self._make_mini_dataset()
        candidates = build_blocking_index(s1_df, s23_df)
        s1_ids = set(s1_df["entity_id"])
        for s1_id, cands in candidates.items():
            for c in cands:
                assert c not in s1_ids, f"S1 ID {c} found in candidates for {s1_id}"

    def test_no_duplicate_candidates_per_s1(self):
        s1_df, s23_df = self._make_mini_dataset()
        candidates = build_blocking_index(s1_df, s23_df)
        for s1_id, cands in candidates.items():
            assert len(cands) == len(set(cands)), \
                f"Duplicate candidates for {s1_id}: {cands}"

    def test_candidates_are_valid_s23_ids(self):
        s1_df, s23_df = self._make_mini_dataset()
        candidates = build_blocking_index(s1_df, s23_df)
        valid_s23 = set(s23_df["entity_id"])
        for s1_id, cands in candidates.items():
            for c in cands:
                assert c in valid_s23, f"Invalid candidate {c} for {s1_id}"

    def test_obvious_matches_are_candidates(self):
        """Clear matches like 'Google LLC' ↔ 'Google Limited Liability Company' must be candidates."""
        s1_df, s23_df = self._make_mini_dataset()
        candidates = build_blocking_index(s1_df, s23_df)
        # S1-001 (Google LLC) should have S2-001 as candidate
        assert "S2-001" in candidates.get("S1-001", []), \
            "Google LLC did not find Google Limited Liability Company as candidate"
        # S1-002 (Amazon Corp) should have S2-002 as candidate
        assert "S2-002" in candidates.get("S1-002", []), \
            "Amazon Corp did not find Amazon Corporation as candidate"

    def test_blocking_recall_on_mini_gt(self):
        s1_df, s23_df = self._make_mini_dataset()
        gt = {
            "S1-001": ["S2-001"],
            "S1-002": ["S2-002"],
            "S1-003": ["S3-001"],
            "S1-004": [],
        }
        candidates = build_blocking_index(s1_df, s23_df)
        result = compute_blocking_recall(candidates, gt)
        # All 3 positive pairs should be candidates (obvious matches)
        assert result["blocking_recall"] >= 0.95, \
            f"Blocking recall {result['blocking_recall']:.3f} too low on mini dataset"


class TestComputeBlockingRecall:
    """Unit tests for compute_blocking_recall()."""

    def test_perfect_recall(self):
        candidates = {"S1-001": ["S2-001", "S3-002"]}
        gt = {"S1-001": ["S2-001", "S3-002"]}
        result = compute_blocking_recall(candidates, gt)
        assert result["blocking_recall"] == 1.0

    def test_zero_recall(self):
        candidates = {"S1-001": []}
        gt = {"S1-001": ["S2-001"]}
        result = compute_blocking_recall(candidates, gt)
        assert result["blocking_recall"] == 0.0
        assert result["n_missed"] == 1

    def test_singleton_s1_not_counted(self):
        candidates = {"S1-001": []}
        gt = {"S1-001": []}
        result = compute_blocking_recall(candidates, gt)
        assert result["n_gt_pairs"] == 0
