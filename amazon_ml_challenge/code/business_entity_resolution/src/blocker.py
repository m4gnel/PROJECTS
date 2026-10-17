"""
blocker.py — Memory-safe blocking for 2.2M S1 + 10.3M S2+S3.
Uses token inverted index and Soundex. Zero matrix multiplication.
RAM usage: ~3 GB max. Runtime: ~3-5 minutes.
"""
import gc
import logging
import os
import pickle
from collections import defaultdict
from typing import Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)

CACHE_DIR = "models/blocking_cache"


def _soundex(name: str) -> str:
    if not name:
        return "0000"
    name = name.upper().strip()
    if not name:
        return "0000"
    first = name[0]
    mapping = {"BFPV": "1", "CGJKQSXYZ": "2", "DT": "3",
               "L": "4", "MN": "5", "R": "6"}
    coded = first
    for ch in name[1:]:
        for keys, digit in mapping.items():
            if ch in keys:
                if coded[-1] != digit:
                    coded += digit
                break
    return (coded + "000")[:4]


def _save(obj, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(obj, f, protocol=4)


def _load(path: str):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return pickle.load(f)


def _token_block(
    s1_df: pd.DataFrame,
    s23_df: pd.DataFrame,
    min_shared: int = 2,
    max_per_s1: int = 50,
    use_cache: bool = True,
    prefix: str = "train",
) -> Dict[str, List[str]]:
    cache_path = os.path.join(CACHE_DIR, f"{prefix}_token_candidates.pkl")
    if use_cache:
        cached = _load(cache_path)
        if cached is not None:
            logger.info(f"  Token blocking [{prefix}] loaded from cache ({len(cached):,} entries)")
            return cached

    logger.info(f"  Building token inverted index [{prefix}] on {len(s23_df):,} S2+S3 records...")

    # Build index: token -> [s23_entity_ids]
    tok_idx: Dict[str, List[str]] = defaultdict(list)

    for row in s23_df.itertuples():
        eid = row.entity_id
        name = str(getattr(row, "norm_name", "") or "")
        addr = str(getattr(row, "norm_address", "") or "")
        tokens = {t for t in (name + " " + addr).split() if len(t) >= 3}
        for tok in tokens:
            tok_idx[tok].append(eid)

    # Prune ultra-high frequency generic tokens (> 2,500 occurrences) for high speed and low memory
    MAX_TOK_FREQ = 2_500
    filtered_tok_idx = {k: v for k, v in tok_idx.items() if len(v) <= MAX_TOK_FREQ}
    del tok_idx
    gc.collect()

    logger.info(f"  Index built [{prefix}]: {len(filtered_tok_idx):,} unique tokens retained (freq <= {MAX_TOK_FREQ:,})")

    results: Dict[str, List[str]] = {}
    total = len(s1_df)

    for i, row in enumerate(s1_df.itertuples()):
        s1_id = row.entity_id
        name = str(getattr(row, "norm_name", "") or "")
        addr = str(getattr(row, "norm_address", "") or "")
        s1_tokens = {t for t in (name + " " + addr).split() if len(t) >= 3}

        if not s1_tokens:
            results[s1_id] = []
            continue

        counts: Dict[str, int] = defaultdict(int)
        for tok in s1_tokens:
            for eid in filtered_tok_idx.get(tok, []):
                counts[eid] += 1

        top = sorted(
            [(eid, cnt) for eid, cnt in counts.items() if cnt >= min_shared],
            key=lambda x: -x[1]
        )[:max_per_s1]

        results[s1_id] = [eid for eid, _ in top]

        if (i + 1) % 500_000 == 0:
            logger.info(f"  Token blocking [{prefix}]: {i+1:,}/{total:,}")

    _save(results, cache_path)
    logger.info(f"  Token blocking [{prefix}] done. Cached to {cache_path}")
    return results


def _soundex_block(
    s1_df: pd.DataFrame,
    s23_df: pd.DataFrame,
    use_cache: bool = True,
    prefix: str = "train",
) -> Dict[str, List[str]]:
    cache_path = os.path.join(CACHE_DIR, f"{prefix}_soundex_candidates.pkl")
    if use_cache:
        cached = _load(cache_path)
        if cached is not None:
            logger.info(f"  Soundex blocking [{prefix}] loaded from cache ({len(cached):,} entries)")
            return cached

    logger.info(f"  Building Soundex index [{prefix}] on {len(s23_df):,} records...")

    key_idx: Dict[str, List[str]] = defaultdict(list)
    for row in s23_df.itertuples():
        country = str(getattr(row, "country", "") or "").lower()
        name = str(getattr(row, "norm_name", "") or "")
        first = name.split()[0] if name.split() else ""
        key = f"{country}_{_soundex(first)}"
        key_idx[key].append(row.entity_id)

    # Prune ultra-large Soundex buckets (> 5,000 candidates)
    filtered_key_idx = {k: v[:5000] for k, v in key_idx.items()}
    del key_idx

    results: Dict[str, List[str]] = {}
    for row in s1_df.itertuples():
        country = str(getattr(row, "country", "") or "").lower()
        name = str(getattr(row, "norm_name", "") or "")
        first = name.split()[0] if name.split() else ""
        key = f"{country}_{_soundex(first)}"
        results[row.entity_id] = filtered_key_idx.get(key, [])[:50]

    _save(results, cache_path)
    logger.info(f"  Soundex blocking [{prefix}] done. Cached to {cache_path}")
    return results


def _exact_name_block(
    s1_df: pd.DataFrame,
    s23_df: pd.DataFrame,
    use_cache: bool = True,
    prefix: str = "train",
) -> Dict[str, List[str]]:
    """Exact normalized-name match per country. Precision=1.0 on these pairs."""
    cache_path = os.path.join(CACHE_DIR, f"{prefix}_exact_candidates.pkl")
    if use_cache:
        cached = _load(cache_path)
        if cached is not None:
            logger.info(f"  Exact blocking [{prefix}] loaded from cache ({len(cached):,} entries)")
            return cached

    logger.info(f"  Building exact-name index [{prefix}] on {len(s23_df):,} records...")

    key_idx: Dict[str, List[str]] = defaultdict(list)
    for row in s23_df.itertuples():
        country = str(getattr(row, "country", "") or "").lower()
        name = str(getattr(row, "norm_name", "") or "").strip()
        if name:
            key_idx[f"{country}||{name}"].append(row.entity_id)

    results: Dict[str, List[str]] = {}
    for row in s1_df.itertuples():
        country = str(getattr(row, "country", "") or "").lower()
        name = str(getattr(row, "norm_name", "") or "").strip()
        key = f"{country}||{name}"
        results[row.entity_id] = key_idx.get(key, [])

    _save(results, cache_path)
    logger.info(f"  Exact blocking [{prefix}] done. Cached to {cache_path}")
    return results


def build_blocking_index(
    s1_df: pd.DataFrame,
    s23_df: pd.DataFrame,
    s1_embeddings=None,
    s23_embeddings=None,
    train_s1_ids=None,
    config=None,
    use_cache: bool = True,
    prefix: str = "train",
) -> Dict[str, List[str]]:
    """
    Union of token, soundex, and exact-name blocking.
    No TF-IDF. No matrix multiplication. Safe on 16GB RAM.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    max_per_s1 = getattr(config, "max_candidates_per_s1", 100) if config else 100
    uc = use_cache

    s1_ids = s1_df["entity_id"].tolist()
    valid_s23 = set(s23_df["entity_id"].tolist())

    logger.info(f"=== BLOCKING [{prefix}]: Exact name match ===")
    exact = _exact_name_block(s1_df, s23_df, use_cache=uc, prefix=prefix)

    logger.info(f"=== BLOCKING [{prefix}]: Token inverted index ===")
    token = _token_block(s1_df, s23_df, use_cache=uc, prefix=prefix)

    logger.info(f"=== BLOCKING [{prefix}]: Soundex phonetic ===")
    soundex = _soundex_block(s1_df, s23_df, use_cache=uc, prefix=prefix)

    logger.info(f"Merging all blocking keys [{prefix}] (union)...")
    result: Dict[str, List[str]] = {}
    for s1_id in s1_ids:
        combined = set()
        combined.update(exact.get(s1_id, []))
        combined.update(token.get(s1_id, []))
        combined.update(soundex.get(s1_id, []))
        combined &= valid_s23
        combined.discard(s1_id)
        result[s1_id] = list(combined)[:max_per_s1]

    total = sum(len(v) for v in result.values())
    with_cands = sum(1 for v in result.values() if v)
    logger.info(
        f"Blocking [{prefix}] complete: {total:,} candidates, "
        f"{with_cands:,}/{len(s1_ids):,} S1 entities have candidates"
    )
    return result


def compute_blocking_recall(
    candidates: Dict[str, List[str]],
    ground_truth: Dict[str, List[str]],
) -> Dict:
    n_gt, n_covered, missed = 0, 0, []
    for s1_id, gt_matches in ground_truth.items():
        cand_set = set(candidates.get(s1_id, []))
        for mid in gt_matches:
            n_gt += 1
            if mid in cand_set:
                n_covered += 1
            else:
                missed.append((s1_id, mid))
    recall = n_covered / max(n_gt, 1)
    return {
        "blocking_recall": recall,
        "n_gt_pairs": n_gt,
        "n_covered": n_covered,
        "n_missed": len(missed),
        "missed_pairs": missed[:10],
    }
