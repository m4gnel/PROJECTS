"""
data_loader.py — Load and validate all TSV source files.
"""
import logging
import os
from typing import Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_SOURCE_COLS = {"entity_id", "business_name", "business_address", "country"}
REQUIRED_GT_COLS = {"source1_entity_id", "matched_entity_ids"}


def load_tsv(path: str, required_cols: set = None) -> pd.DataFrame:
    """Load a TSV file with validation."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required file not found: {path}")
    
    try:
        df = pd.read_csv(path, sep="\t", dtype=str, keep_default_na=False)
    except Exception as e:
        raise ValueError(f"Failed to read {path}: {e}")
    
    if df.shape[1] == 1:
        raise ValueError(
            f"File {path} appears to have only 1 column. "
            "Did you forget sep='\\t'? The file must be tab-separated."
        )
    
    if required_cols:
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"File {path} missing required columns: {missing}")
    
    logger.info(f"Loaded {path}: {df.shape[0]} rows, {df.shape[1]} cols")
    return df


def validate_entity_ids(df: pd.DataFrame, expected_prefix: str) -> None:
    """Validate entity_id format and uniqueness."""
    if df["entity_id"].duplicated().any():
        dups = df[df["entity_id"].duplicated(keep=False)]["entity_id"].tolist()
        raise ValueError(f"Duplicate entity_ids found: {dups[:10]}")
    
    bad_ids = df[~df["entity_id"].str.startswith(expected_prefix)]["entity_id"].tolist()
    if bad_ids:
        raise ValueError(
            f"entity_ids should start with '{expected_prefix}', found: {bad_ids[:5]}"
        )


def load_sources(data_dir: str, mode: str = "train") -> Dict[str, pd.DataFrame]:
    """
    Load all source TSV files.
    
    Args:
        data_dir: path to directory containing source TSVs
        mode: "train" or "test"
    
    Returns:
        Dict with keys "s1", "s2", "s3", and (if mode="train") "gt"
    """
    prefix = f"{mode}_"
    result = {}
    
    # Load source files
    for src_num, src_prefix in [("s1", "S1-"), ("s2", "S2-"), ("s3", "S3-")]:
        path = os.path.join(data_dir, f"{prefix}source{src_num[-1]}.tsv")
        df = load_tsv(path, REQUIRED_SOURCE_COLS)
        validate_entity_ids(df, src_prefix)
        result[src_num] = df
    
    # Load ground truth (train only)
    if mode == "train":
        gt_path = os.path.join(data_dir, "train_ground_truth.tsv")
        gt = load_tsv(gt_path, REQUIRED_GT_COLS)
        # Ensure matched_entity_ids is treated as empty string (not NaN)
        gt["matched_entity_ids"] = gt["matched_entity_ids"].fillna("")
        result["gt"] = gt
    
    return result


def ground_truth_to_dict(gt_df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Convert ground truth DataFrame to dict: {s1_id: [matched_ids]}.
    Singletons have empty list.
    """
    gt_dict = {}
    for _, row in gt_df.iterrows():
        s1_id = row["source1_entity_id"]
        matched_str = row["matched_entity_ids"].strip()
        if matched_str:
            matched = [m.strip() for m in matched_str.split(",") if m.strip()]
        else:
            matched = []
        gt_dict[s1_id] = matched
    return gt_dict


def get_all_s23_ids(s2_df: pd.DataFrame, s3_df: pd.DataFrame) -> set:
    """Get set of all valid S2/S3 entity IDs."""
    return set(s2_df["entity_id"].tolist()) | set(s3_df["entity_id"].tolist())
