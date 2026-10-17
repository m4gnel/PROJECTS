"""
normalizer.py — Text normalization for business names and addresses.

Pipeline per field:
  1. Handle None/NaN → ""
  2. unicodedata.normalize("NFC", text)
  3. text.lower()
  4. Expand abbreviations
  5. Remove non-alphanumeric chars (keep spaces)
  6. Collapse whitespace, strip
"""
import json
import logging
import os
import re
import unicodedata
from typing import Optional

logger = logging.getLogger(__name__)

# Default abbreviation maps (fallback if JSON not found)
DEFAULT_NAME_ABBREVS = {
    "corp": "corporation",
    "co": "company",
    "co.": "company",
    "pvt": "private",
    "ltd": "limited",
    "llc": "limited liability company",
    "inc": "incorporated",
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
    "entrprs": "enterprises",
    "sarl": "societe a responsabilite limitee",
    "sas": "societe par actions simplifiee",
    "sa": "societe anonyme",
    "eurl": "entreprise unipersonnelle a responsabilite limitee",
}

DEFAULT_ADDR_ABBREVS = {
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
    "nxt": "next to",
    "nxt": "next",
}

_NAME_ABBREVS = None
_ADDR_ABBREVS = None


def _load_abbreviations(abbrev_file: str) -> None:
    """Load abbreviation dicts from JSON file."""
    global _NAME_ABBREVS, _ADDR_ABBREVS
    
    if os.path.exists(abbrev_file):
        with open(abbrev_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        _NAME_ABBREVS = {k.lower(): v.lower() for k, v in data.get("name", {}).items()}
        _ADDR_ABBREVS = {k.lower(): v.lower() for k, v in data.get("address", {}).items()}
        logger.info(f"Loaded abbreviations: {len(_NAME_ABBREVS)} name, {len(_ADDR_ABBREVS)} address")
    else:
        logger.warning(f"Abbreviation file not found: {abbrev_file}, using defaults")
        _NAME_ABBREVS = DEFAULT_NAME_ABBREVS
        _ADDR_ABBREVS = DEFAULT_ADDR_ABBREVS


def initialize(abbrev_file: str = "configs/abbreviations.json") -> None:
    """Call once at startup to load abbreviations."""
    _load_abbreviations(abbrev_file)


def _expand_abbreviations(text: str, abbrev_dict: dict) -> str:
    """Replace abbreviated tokens with full forms."""
    tokens = text.split()
    expanded = []
    for token in tokens:
        # Try exact match, then strip trailing punctuation
        clean_token = token.rstrip(".")
        if token in abbrev_dict:
            expanded.append(abbrev_dict[token])
        elif clean_token in abbrev_dict:
            expanded.append(abbrev_dict[clean_token])
        else:
            expanded.append(token)
    return " ".join(expanded)


def normalize_text(text, field: str = "name") -> str:
    """
    Normalize a raw text field.
    
    Args:
        text: raw string (may be None, NaN, or empty)
        field: "name" or "address" — selects abbreviation dict
    
    Returns:
        Normalized string (lowercase, expanded abbreviations, punctuation-stripped).
        Returns "" if text is None/NaN/empty.
    """
    global _NAME_ABBREVS, _ADDR_ABBREVS
    
    # Initialize with defaults if not yet loaded
    if _NAME_ABBREVS is None:
        _NAME_ABBREVS = DEFAULT_NAME_ABBREVS
        _ADDR_ABBREVS = DEFAULT_ADDR_ABBREVS
    
    # Step 1: Handle None/NaN
    if text is None:
        return ""
    try:
        import math
        if isinstance(text, float) and math.isnan(text):
            return ""
    except (TypeError, ValueError):
        pass
    
    text = str(text).strip()
    if not text:
        return ""
    
    # Step 2: Unicode normalization
    text = unicodedata.normalize("NFC", text)
    
    # Step 3: Lowercase
    text = text.lower()
    
    # Step 4: Expand abbreviations
    abbrev_dict = _NAME_ABBREVS if field == "name" else _ADDR_ABBREVS
    text = _expand_abbreviations(text, abbrev_dict)
    
    # Step 5: Remove non-alphanumeric (keep spaces)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    
    # Step 6: Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    
    # Step 7: Truncate if too long
    if len(text) > 500:
        text = text[:500]
        logger.debug(f"Truncated text to 500 chars")
    
    return text


def build_combined_text(norm_name: str, norm_address: str) -> str:
    """Concatenate normalized name and address for embedding."""
    parts = [p for p in [norm_name, norm_address] if p]
    return " ".join(parts)


def normalize_dataframe(df, name_col: str = "business_name",
                        addr_col: str = "business_address"):
    """
    Add norm_name, norm_address, norm_text columns to DataFrame.
    Returns modified DataFrame (does not modify in place).
    """
    df = df.copy()
    df["norm_name"] = df[name_col].apply(lambda x: normalize_text(x, field="name"))
    df["norm_address"] = df[addr_col].apply(lambda x: normalize_text(x, field="address"))
    df["norm_text"] = df.apply(
        lambda row: build_combined_text(row["norm_name"], row["norm_address"]), axis=1
    )
    return df
