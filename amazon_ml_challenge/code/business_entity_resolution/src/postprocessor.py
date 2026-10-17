"""
postprocessor.py — Apply threshold, deduplicate, write output files.
"""
import logging
import os
from typing import Dict, List, Set

import pandas as pd

logger = logging.getLogger(__name__)


def apply_threshold(
    feature_df: pd.DataFrame,
    scores: pd.Series,
    threshold: float,
    all_s1_ids: List[str],
) -> Dict[str, List[str]]:
    """
    Apply probability threshold to get final predictions.
    
    Args:
        feature_df: DataFrame with s1_id and candidate_id columns
        scores: match probabilities (same index as feature_df)
        threshold: minimum probability to be a match
        all_s1_ids: complete list of S1 IDs (includes singletons)
    
    Returns:
        {s1_id: [matched_candidate_ids]}  — every s1_id present, singletons have []
    """
    df = feature_df.copy()
    df["match_prob"] = scores.values
    
    # Filter by threshold
    matched_df = df[df["match_prob"] >= threshold]
    
    # Group by s1_id
    predictions: Dict[str, List[str]] = {}
    for s1_id, group in matched_df.groupby("s1_id"):
        # Sort by probability descending
        sorted_group = group.sort_values("match_prob", ascending=False)
        matched_ids = sorted_group["candidate_id"].tolist()
        # Deduplicate preserving order
        seen: Set[str] = set()
        deduped = []
        for mid in matched_ids:
            if mid not in seen:
                seen.add(mid)
                deduped.append(mid)
        predictions[s1_id] = deduped
    
    # Ensure all S1 IDs are present
    for s1_id in all_s1_ids:
        if s1_id not in predictions:
            predictions[s1_id] = []
    
    n_with_matches = sum(1 for v in predictions.values() if v)
    n_singletons = sum(1 for v in predictions.values() if not v)
    logger.info(
        f"Threshold {threshold:.2f}: {n_with_matches:,} with matches, "
        f"{n_singletons:,} singletons"
    )
    
    return predictions


def write_matching_results(
    predictions: Dict[str, List[str]],
    output_path: str,
) -> None:
    """Write matching_results.tsv."""
    rows = []
    for s1_id, matches in predictions.items():
        rows.append({
            "source1_entity_id": s1_id,
            "matched_entity_ids": ",".join(matches) if matches else "",
        })
    
    df = pd.DataFrame(rows, columns=["source1_entity_id", "matched_entity_ids"])
    df.to_csv(output_path, sep="\t", index=False)
    logger.info(f"Written matching_results.tsv: {len(df):,} rows → {output_path}")


def write_candidate_pairs(
    candidates: Dict[str, List[str]],
    all_s1_ids: List[str],
    output_path: str,
) -> None:
    """Write candidate_pairs.tsv."""
    rows = []
    for s1_id in all_s1_ids:
        cands = candidates.get(s1_id, [])
        # Deduplicate
        seen: Set[str] = set()
        deduped = []
        for c in cands:
            if c not in seen:
                seen.add(c)
                deduped.append(c)
        rows.append({
            "source1_entity_id": s1_id,
            "candidate_entity_ids": ",".join(deduped) if deduped else "",
        })
    
    df = pd.DataFrame(rows, columns=["source1_entity_id", "candidate_entity_ids"])
    df.to_csv(output_path, sep="\t", index=False)
    logger.info(f"Written candidate_pairs.tsv: {len(df):,} rows → {output_path}")


def validate_matched_subset_of_candidates(
    predictions: Dict[str, List[str]],
    candidates: Dict[str, List[str]],
) -> List[str]:
    """
    Check that every matched ID appears in the candidate set.
    Returns list of violations (should be empty).
    """
    violations = []
    for s1_id, matched in predictions.items():
        cand_set = set(candidates.get(s1_id, []))
        for mid in matched:
            if mid not in cand_set:
                violations.append(f"{s1_id}: matched {mid} not in candidates")
    return violations


def write_output_files(
    candidates: Dict[str, List[str]],
    predictions: Dict[str, List[str]],
    all_s1_ids: List[str],
    output_dir: str,
) -> None:
    """Write both output TSV files."""
    os.makedirs(output_dir, exist_ok=True)
    
    matching_path = os.path.join(output_dir, "matching_results.tsv")
    candidates_path = os.path.join(output_dir, "candidate_pairs.tsv")
    
    # Validate before writing
    violations = validate_matched_subset_of_candidates(predictions, candidates)
    if violations:
        logger.warning(f"Pipeline bug: {len(violations)} matched IDs not in candidates:")
        for v in violations[:5]:
            logger.warning(f"  {v}")
    
    write_matching_results(predictions, matching_path)
    write_candidate_pairs(candidates, all_s1_ids, candidates_path)
    
    logger.info(f"Output files written to {output_dir}/")
