"""
blocker_scalable.py
Scalable blocking for 2.2M S1 + 10.3M S2+S3 records.

Strategy: Process S1 in chunks, TF-IDF cosine against all S2+S3.
No FAISS needed. Uses sklearn sparse matrices which handle large scale well.
Saves candidates to disk in chunks to avoid OOM.

Expected runtime: 30-90 minutes on CPU.
Expected RAM: 4-8 GB peak.
"""
import gc
import logging
import os
import pickle
from collections import defaultdict
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


def soundex(name: str) -> str:
    """Simple Soundex for phonetic blocking."""
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


def get_first_token(text: str) -> str:
    tokens = str(text).strip().split()
    return tokens[0].lower() if tokens else ""


# ── BK-A: TF-IDF Chunked Cosine ───────────────────────────────────────────────

def build_tfidf_candidates_chunked(
    s1_df: pd.DataFrame,
    s23_df: pd.DataFrame,
    top_k: int = 20,
    chunk_size: int = 50_000,
    cache_dir: str = "models/blocking_cache",
    use_cache: bool = True,
) -> Dict[str, List[str]]:
    """
    Chunked TF-IDF cosine blocking.

    Processes S1 in chunks of `chunk_size` rows.
    For each chunk, computes cosine similarity against ALL S2+S3.
    Saves results to disk per chunk, then merges.

    RAM peak: ~4-6 GB (vectorizer + one chunk's similarity matrix).
    """
    cache_file = os.path.join(cache_dir, "tfidf_candidates.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    if use_cache and os.path.exists(cache_file):
        logger.info(f"Loading TF-IDF candidates from cache: {cache_file}")
        with open(cache_file, "rb") as f:
            return pickle.load(f)

    logger.info(f"Building TF-IDF index on {len(s23_df):,} S2+S3 records...")

    s23_texts = s23_df["norm_text"].fillna("").tolist()
    s23_ids = s23_df["entity_id"].tolist()
    s1_texts = s1_df["norm_text"].fillna("").tolist()
    s1_ids = s1_df["entity_id"].tolist()

    # Fit vectorizer on ALL texts for a shared vocabulary
    logger.info("Fitting TF-IDF vectorizer on all texts (this takes 5-10 min)...")
    vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(2, 4),
        min_df=2,
        max_features=200_000,
        sublinear_tf=True,
    )
    # Fit on a sample of all texts to get vocabulary
    sample_size = min(500_000, len(s23_texts))
    import random
    sample_texts = random.sample(s23_texts, sample_size) + s1_texts[:50_000]
    vectorizer.fit(sample_texts)
    del sample_texts
    gc.collect()

    # Transform S2+S3 in one shot (sparse matrix - manageable)
    logger.info(f"Transforming {len(s23_texts):,} S2+S3 texts...")
    s23_vectors = vectorizer.transform(s23_texts)
    logger.info(f"S2+S3 matrix: {s23_vectors.shape}, nnz={s23_vectors.nnz:,}")

    all_candidates: Dict[str, List[str]] = {}
    n_chunks = (len(s1_ids) + chunk_size - 1) // chunk_size

    for chunk_idx in range(n_chunks):
        start = chunk_idx * chunk_size
        end = min(start + chunk_size, len(s1_ids))

        chunk_texts = s1_texts[start:end]
        chunk_ids = s1_ids[start:end]

        logger.info(
            f"TF-IDF chunk {chunk_idx+1}/{n_chunks}: "
            f"S1[{start:,}:{end:,}] ({len(chunk_ids):,} records)"
        )

        chunk_vectors = vectorizer.transform(chunk_texts)
        # Compute cosine similarity: (chunk_size, len_s23)
        # This is the memory-intensive step
        sims = cosine_similarity(chunk_vectors, s23_vectors)

        for j, s1_id in enumerate(chunk_ids):
            row = sims[j]
            if top_k >= len(row):
                top_indices = np.argsort(row)[::-1]
            else:
                top_indices = np.argpartition(row, -top_k)[-top_k:]
                top_indices = top_indices[np.argsort(row[top_indices])[::-1]]

            candidates = [s23_ids[idx] for idx in top_indices if row[idx] > 0.01]
            all_candidates[s1_id] = candidates

        del sims, chunk_vectors
        gc.collect()

        # Periodic save in case of crash
        if (chunk_idx + 1) % 10 == 0:
            with open(cache_file + ".partial", "wb") as f:
                pickle.dump(all_candidates, f)

    # Save final cache
    with open(cache_file, "wb") as f:
        pickle.dump(all_candidates, f)
    logger.info(f"TF-IDF candidates cached to {cache_file}")

    return all_candidates


# ── BK-B: Name Token Inverted Index ───────────────────────────────────────────

def build_name_token_candidates(
    s1_df: pd.DataFrame,
    s23_df: pd.DataFrame,
    min_shared_tokens: int = 2,
    max_candidates_per_s1: int = 50,
    cache_dir: str = "models/blocking_cache",
    use_cache: bool = True,
) -> Dict[str, List[str]]:
    """
    Fast inverted index on normalized name tokens.
    Two records are candidates if they share >= min_shared_tokens.
    """
    cache_file = os.path.join(cache_dir, "token_candidates.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    if use_cache and os.path.exists(cache_file):
        logger.info(f"Loading token candidates from cache: {cache_file}")
        with open(cache_file, "rb") as f:
            return pickle.load(f)

    logger.info(f"Building name token inverted index on {len(s23_df):,} records...")

    # Build index: token → [s23_ids]
    token_to_s23: Dict[str, List[str]] = defaultdict(list)
    s23_tokens: Dict[str, set] = {}

    for _, row in s23_df.iterrows():
        eid = row["entity_id"]
        name = str(row.get("norm_name", ""))
        # Only meaningful tokens (length >= 3, not stopwords)
        tokens = {t for t in name.split() if len(t) >= 3}
        s23_tokens[eid] = tokens
        for tok in tokens:
            token_to_s23[tok].append(eid)

    logger.info(f"Index built: {len(token_to_s23):,} unique tokens")

    candidates: Dict[str, List[str]] = {}
    for i, row in enumerate(s1_df.itertuples(), 1):
        s1_id = row.entity_id
        name = str(getattr(row, "norm_name", ""))
        s1_tok = {t for t in name.split() if len(t) >= 3}

        if not s1_tok:
            candidates[s1_id] = []
            continue

        # Count shared tokens
        counts: Dict[str, int] = defaultdict(int)
        for tok in s1_tok:
            for eid in token_to_s23.get(tok, []):
                counts[eid] += 1

        # Keep those with enough shared tokens
        top = sorted(
            [(eid, cnt) for eid, cnt in counts.items() if cnt >= min_shared_tokens],
            key=lambda x: -x[1]
        )[:max_candidates_per_s1]

        candidates[s1_id] = [eid for eid, _ in top]

        if i % 200_000 == 0:
            logger.info(f"  Name token index: {i:,}/{len(s1_df):,}")

    with open(cache_file, "wb") as f:
        pickle.dump(candidates, f)
    logger.info(f"Token candidates cached to {cache_file}")
    return candidates


# ── BK-C: Country + Soundex key ───────────────────────────────────────────────

def build_soundex_candidates(
    s1_df: pd.DataFrame,
    s23_df: pd.DataFrame,
    cache_dir: str = "models/blocking_cache",
    use_cache: bool = True,
) -> Dict[str, List[str]]:
    """Phonetic blocking: (country, soundex_of_first_name_word)."""
    cache_file = os.path.join(cache_dir, "soundex_candidates.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    if use_cache and os.path.exists(cache_file):
        logger.info(f"Loading soundex candidates from cache: {cache_file}")
        with open(cache_file, "rb") as f:
            return pickle.load(f)

    logger.info("Building Soundex blocking index...")

    key_to_s23: Dict[str, List[str]] = defaultdict(list)
    for _, row in s23_df.iterrows():
        country = str(row.get("country", "")).lower()
        first = get_first_token(str(row.get("norm_name", "")))
        key = f"{country}_{soundex(first)}"
        key_to_s23[key].append(row["entity_id"])

    candidates: Dict[str, List[str]] = {}
    for _, row in s1_df.iterrows():
        country = str(row.get("country", "")).lower()
        first = get_first_token(str(row.get("norm_name", "")))
        key = f"{country}_{soundex(first)}"
        candidates[row["entity_id"]] = key_to_s23.get(key, [])

    with open(cache_file, "wb") as f:
        pickle.dump(candidates, f)
    return candidates


# ── Main: Union of all blocking keys ──────────────────────────────────────────

def build_blocking_index(
    s1_df: pd.DataFrame,
    s23_df: pd.DataFrame,
    s1_embeddings=None,      # unused - kept for API compat
    s23_embeddings=None,     # unused - kept for API compat
    train_s1_ids=None,       # unused - kept for API compat
    config=None,
    use_cache: bool = True,
) -> Dict[str, List[str]]:
    """
    Main blocking function. Union of BK-A, BK-B, BK-C.
    Returns {s1_id: [candidate_ids]} for every S1 entity.
    """
    cache_dir = "models/blocking_cache"
    top_k = getattr(config, "tfidf_top_k", 20) if config else 20
    max_cands = getattr(config, "max_candidates_per_s1", 100) if config else 100

    s1_ids = s1_df["entity_id"].tolist()
    valid_s23 = set(s23_df["entity_id"].tolist())

    # Run blocking keys
    logger.info("=== BLOCKING: BK-A TF-IDF chunked ===")
    bk_a = build_tfidf_candidates_chunked(
        s1_df, s23_df, top_k=top_k, cache_dir=cache_dir, use_cache=use_cache
    )

    logger.info("=== BLOCKING: BK-B Name token inverted index ===")
    bk_b = build_name_token_candidates(
        s1_df, s23_df, cache_dir=cache_dir, use_cache=use_cache
    )

    logger.info("=== BLOCKING: BK-C Soundex ===")
    bk_c = build_soundex_candidates(
        s1_df, s23_df, cache_dir=cache_dir, use_cache=use_cache
    )

    # Union all keys
    logger.info("Merging blocking keys (union)...")
    all_candidates: Dict[str, List[str]] = {}

    for s1_id in s1_ids:
        combined = set()
        combined.update(bk_a.get(s1_id, []))
        combined.update(bk_b.get(s1_id, []))
        combined.update(bk_c.get(s1_id, []))
        # Remove invalid IDs and cap
        combined = combined & valid_s23
        combined.discard(s1_id)
        all_candidates[s1_id] = list(combined)[:max_cands]

    total = sum(len(v) for v in all_candidates.values())
    with_cands = sum(1 for v in all_candidates.values() if v)
    logger.info(
        f"Blocking complete: {total:,} total candidates, "
        f"{with_cands:,}/{len(s1_ids):,} S1 entities have candidates"
    )

    return all_candidates


def compute_blocking_recall(
    candidates: Dict[str, List[str]],
    ground_truth: Dict[str, List[str]],
) -> Dict:
    """Measure fraction of GT pairs captured by blocking."""
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
