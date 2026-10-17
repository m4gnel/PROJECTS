"""
tests/test_normalizer.py
Unit tests for the text normalization module.
Run: pytest tests/test_normalizer.py -v
"""
import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from normalizer import normalize_text, build_combined_text, initialize


class TestNormalizeText:
    """Tests for normalize_text()."""

    def test_none_input_returns_empty(self):
        assert normalize_text(None) == ""

    def test_nan_input_returns_empty(self):
        assert normalize_text(float("nan")) == ""

    def test_empty_string_returns_empty(self):
        assert normalize_text("") == ""

    def test_whitespace_only_returns_empty(self):
        assert normalize_text("   ") == ""

    def test_lowercase(self):
        assert normalize_text("GOOGLE LLC") == normalize_text("google llc")

    def test_corp_expansion(self):
        result = normalize_text("Amazon Corp")
        assert "corporation" in result

    def test_pvt_expansion(self):
        result = normalize_text("Reliance Pvt Ltd")
        assert "private" in result
        assert "limited" in result

    def test_ampersand_expansion(self):
        result = normalize_text("Johnson & Johnson")
        assert " and " in result
        assert "&" not in result

    def test_llc_expansion(self):
        result = normalize_text("Acme LLC")
        assert "limited liability company" in result

    def test_inc_expansion(self):
        result = normalize_text("Nike Inc")
        assert "incorporated" in result

    def test_punctuation_removal(self):
        result = normalize_text("Google, Inc.")
        assert "," not in result
        assert "." not in result

    def test_whitespace_collapse(self):
        result = normalize_text("  A    B   C  ")
        assert "  " not in result
        assert result == result.strip()

    def test_address_rd_to_road(self):
        result = normalize_text("123 Main Rd", field="address")
        assert "road" in result

    def test_address_st_to_street(self):
        result = normalize_text("45 Park St", field="address")
        assert "street" in result

    def test_address_ave_to_avenue(self):
        result = normalize_text("100 5th Ave", field="address")
        assert "avenue" in result

    def test_unicode_lowercase(self):
        # NFC normalization + lowercase
        result = normalize_text("Éclat")
        assert result == result.lower()

    def test_numeric_preserved(self):
        result = normalize_text("Company 123")
        assert "123" in result

    def test_long_text_truncated(self):
        long_text = "a " * 400  # 800 chars
        result = normalize_text(long_text)
        assert len(result) <= 500

    def test_french_legal_sarl(self):
        result = normalize_text("Dupont SARL")
        # sarl should be expanded if in abbreviations dict
        # or at minimum remain lowercase
        assert "sarl" in result or "societe" in result

    def test_integer_input(self):
        # Sometimes pandas reads numeric IDs as int
        result = normalize_text(12345)
        assert result == "12345"


class TestBuildCombinedText:
    """Tests for build_combined_text()."""

    def test_both_fields(self):
        result = build_combined_text("google corporation", "1600 amphitheatre parkway")
        assert "google" in result
        assert "amphitheatre" in result

    def test_empty_address(self):
        result = build_combined_text("amazon incorporated", "")
        assert result == "amazon incorporated"

    def test_empty_name(self):
        result = build_combined_text("", "100 main road")
        assert result == "100 main road"

    def test_both_empty(self):
        result = build_combined_text("", "")
        assert result == ""

    def test_no_extra_spaces(self):
        result = build_combined_text("a", "b")
        assert "  " not in result
