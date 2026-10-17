"""
feature_engineer.py — Compute similarity features for candidate pairs.

Features computed per pair:
  Name group:    Levenshtein ratio, Jaro-Winkler, Token-sort, Token-set, TF-IDF cosine
  Address group: Levenshtein ratio, Token-sort, Token-set, Jaccard tokens
  Semantic:      Cosine of multilingual sentence embeddings
  Structural:    name_len_diff, addr_token_diff, country_match
  Composite:     name_sim × addr_sim, max_sim
"""
import logging
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from rapidfuzz import fuzz, distance

logger = logging.getLogger(__name__)


def _jaccard_tokens(text_a: str, text_b: str) -> float:
    """Jaccard similarity on token sets."""
    tokens_a = set(text_a.split())
    tokens_b = set(text_b.split())
    if not tokens_a and not tokens_b:
        return 1.0
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b
    return len(intersection) / len(union)


def _token_count(text: str) -> int:
    return len(text.split()) if text else 0


def compute_pair_features(
    s1_record: dict,
    candidate_record: dict,
    s1_embedding: Optional[np.ndarray] = None,
    candidate_embedding: Optional[np.ndarray] = None,
) -> Dict[str, float]:
    """
    Compute all similarity features for one (S1, candidate) pair.
    """
    s1_name = s1_record.get("norm_name", "")
    s1_addr = s1_record.get("norm_address", "")
    s1_country = s1_record.get("country", "")
    
    c_name = candidate_record.get("norm_name", "")
    c_addr = candidate_record.get("norm_address", "")
    c_country = candidate_record.get("country", "")
    
    # Name features
    if s1_name or c_name:
        lev_name = fuzz.ratio(s1_name, c_name) / 100.0
        jw_name = 1.0 - distance.JaroWinkler.normalized_distance(s1_name, c_name)
        ts_name = fuzz.token_sort_ratio(s1_name, c_name) / 100.0
        tset_name = fuzz.token_set_ratio(s1_name, c_name) / 100.0
        partial_name = fuzz.partial_ratio(s1_name, c_name) / 100.0
    else:
        lev_name = jw_name = ts_name = tset_name = partial_name = 0.0
    
    # Address features
    if s1_addr or c_addr:
        lev_addr = fuzz.ratio(s1_addr, c_addr) / 100.0
        ts_addr = fuzz.token_sort_ratio(s1_addr, c_addr) / 100.0
        tset_addr = fuzz.token_set_ratio(s1_addr, c_addr) / 100.0
        jaccard_addr = _jaccard_tokens(s1_addr, c_addr)
        partial_addr = fuzz.partial_ratio(s1_addr, c_addr) / 100.0
    else:
        lev_addr = ts_addr = tset_addr = jaccard_addr = partial_addr = 0.0
    
    # Semantic feature
    if s1_embedding is not None and candidate_embedding is not None:
        cos_embed = float(np.dot(s1_embedding, candidate_embedding))
        cos_embed = max(0.0, min(1.0, cos_embed))
    else:
        cos_embed = 0.0
    
    # Structural features
    name_max_len = max(len(s1_name), len(c_name), 1)
    len_diff_name = abs(len(s1_name) - len(c_name)) / name_max_len
    token_diff_addr = abs(_token_count(s1_addr) - _token_count(c_addr))
    country_match = 1 if s1_country and c_country and s1_country == c_country else 0
    
    # Empty field flags
    s1_name_empty = 1 if not s1_name else 0
    s1_addr_empty = 1 if not s1_addr else 0
    c_name_empty = 1 if not c_name else 0
    c_addr_empty = 1 if not c_addr else 0
    
    # Composite features
    name_x_addr = tset_name * tset_addr
    max_name_sim = max(lev_name, ts_name, tset_name, jw_name)
    max_addr_sim = max(lev_addr, ts_addr, tset_addr, jaccard_addr)
    max_sim = max(max_name_sim, max_addr_sim, cos_embed)
    
    return {
        "lev_name": lev_name,
        "jw_name": jw_name,
        "ts_name": ts_name,
        "tset_name": tset_name,
        "partial_name": partial_name,
        "lev_addr": lev_addr,
        "ts_addr": ts_addr,
        "tset_addr": tset_addr,
        "jaccard_addr": jaccard_addr,
        "partial_addr": partial_addr,
        "cos_embed": cos_embed,
        "len_diff_name": len_diff_name,
        "token_diff_addr": float(token_diff_addr),
        "country_match": float(country_match),
        "s1_name_empty": float(s1_name_empty),
        "s1_addr_empty": float(s1_addr_empty),
        "c_name_empty": float(c_name_empty),
        "c_addr_empty": float(c_addr_empty),
        "name_x_addr": name_x_addr,
        "max_name_sim": max_name_sim,
        "max_addr_sim": max_addr_sim,
        "max_sim": max_sim,
    }


FEATURE_COLS = [
    "lev_name", "jw_name", "ts_name", "tset_name", "partial_name",
    "lev_addr", "ts_addr", "tset_addr", "jaccard_addr", "partial_addr",
    "cos_embed",
    "len_diff_name", "token_diff_addr", "country_match",
    "s1_name_empty", "s1_addr_empty", "c_name_empty", "c_addr_empty",
    "name_x_addr", "max_name_sim", "max_addr_sim", "max_sim",
]


def build_feature_matrix(
    s1_records: Dict[str, dict],
    candidate_records: Dict[str, dict],
    candidate_pairs: Dict[str, List[str]],
    s1_embeddings: Optional[Dict[str, np.ndarray]] = None,
    candidate_embeddings: Optional[Dict[str, np.ndarray]] = None,
    ground_truth: Optional[Dict[str, List[str]]] = None,
) -> pd.DataFrame:
    """
    Build full feature DataFrame for candidate pairs using pre-allocated numpy arrays.
    Memory-efficient: zero object heap overhead.
    """
    gt_set = {}
    if ground_truth:
        gt_set = {s1_id: set(matches) for s1_id, matches in ground_truth.items()}
    
    total_pairs = sum(len(v) for v in candidate_pairs.values())
    logger.info(f"Building features for {total_pairs:,} candidate pairs...")
    
    s1_id_list = [None] * total_pairs
    cand_id_list = [None] * total_pairs
    
    feat_arrays = {c: np.empty(total_pairs, dtype=np.float32) for c in FEATURE_COLS}
    labels = np.empty(total_pairs, dtype=np.int8) if ground_truth is not None else None
    
    processed = 0
    for s1_id, candidates in candidate_pairs.items():
        s1_rec = s1_records.get(s1_id)
        if s1_rec is None:
            continue
        
        s1_emb = s1_embeddings.get(s1_id) if s1_embeddings else None
        
        for cand_id in candidates:
            cand_rec = candidate_records.get(cand_id)
            if cand_rec is None:
                continue
            
            cand_emb = candidate_embeddings.get(cand_id) if candidate_embeddings else None
            
            features = compute_pair_features(s1_rec, cand_rec, s1_emb, cand_emb)
            
            s1_id_list[processed] = s1_id
            cand_id_list[processed] = cand_id
            
            for col_name, val in features.items():
                feat_arrays[col_name][processed] = val
                
            if labels is not None:
                s1_gt = gt_set.get(s1_id, set())
                labels[processed] = 1 if cand_id in s1_gt else 0
            
            processed += 1
            
            if processed % 50000 == 0:
                logger.info(f"  Processed {processed:,}/{total_pairs:,} pairs")
    
    # Trim arrays if any records were skipped
    if processed < total_pairs:
        s1_id_list = s1_id_list[:processed]
        cand_id_list = cand_id_list[:processed]
        for c in FEATURE_COLS:
            feat_arrays[c] = feat_arrays[c][:processed]
        if labels is not None:
            labels = labels[:processed]
            
    df_dict = {
        "s1_id": s1_id_list,
        "candidate_id": cand_id_list,
    }
    for c in FEATURE_COLS:
        df_dict[c] = feat_arrays[c]
        
    if labels is not None:
        df_dict["label"] = labels
        
    df = pd.DataFrame(df_dict)
    logger.info(f"Feature matrix built: {df.shape}")
    
    if labels is not None:
        pos = int(labels.sum())
        neg = len(labels) - pos
        logger.info(f"Label distribution: {pos:,} positives, {neg:,} negatives (ratio 1:{neg//max(pos,1)})")
    
    return df
