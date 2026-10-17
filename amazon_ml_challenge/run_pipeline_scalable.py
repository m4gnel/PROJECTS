"""
run_pipeline.py
Scalable pipeline for 2.2M S1 + 10.3M S2+S3 records.

Key differences from the original:
- Chunked blocking (no OOM on large data)
- Disk-cached intermediate results (resume if crashed)
- String features only (no full-dataset embedding needed)
- Feature engineering in chunks
- Optimised for 8-16 GB RAM machines

Runtime estimate: 2-4 hours total on CPU.
"""
import argparse
import gc
import json
import logging
import os
import pickle
import sys
import time
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

# ── path fix so relative imports work when called from project root ──────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import load_config
from data_loader import load_sources, ground_truth_to_dict
from normalizer import initialize as init_normalizer, normalize_dataframe
from blocker import build_blocking_index, compute_blocking_recall
from feature_engineer import build_feature_matrix, FEATURE_COLS
from matcher import (
    train_matcher,
    load_matcher,
    predict_scores,
    calibrate_threshold,
    mine_hard_negatives,
)
from evaluator import compute_macro_f05, print_evaluation_report
from postprocessor import apply_threshold, write_output_files

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(module)s: %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


# ── Helpers ──────────────────────────────────────────────────────────────────

def df_to_record_dict(df: pd.DataFrame) -> Dict[str, dict]:
    """Convert DataFrame rows to {entity_id: row_dict} for fast lookup."""
    result = {}
    for row in df.itertuples():
        result[row.entity_id] = {
            "entity_id":    row.entity_id,
            "norm_name":    getattr(row, "norm_name",    ""),
            "norm_address": getattr(row, "norm_address", ""),
            "norm_text":    getattr(row, "norm_text",    ""),
            "country":      getattr(row, "country",      ""),
        }
    return result


def normalize_in_chunks(df: pd.DataFrame, chunk_size: int = 100_000) -> pd.DataFrame:
    """Normalize a large DataFrame in chunks to avoid RAM spikes."""
    logger.info(f"Normalising {len(df):,} records in chunks of {chunk_size:,}...")
    chunks = []
    for i in range(0, len(df), chunk_size):
        chunk = normalize_dataframe(df.iloc[i: i + chunk_size].copy())
        chunks.append(chunk)
        done = min(i + chunk_size, len(df))
        if (i // chunk_size + 1) % 5 == 0:
            logger.info(f"  Normalised {done:,}/{len(df):,}")
    result = pd.concat(chunks, ignore_index=True)
    del chunks
    gc.collect()
    return result


def build_feature_matrix_chunked(
    s1_records:     Dict[str, dict],
    s23_records:    Dict[str, dict],
    candidates:     Dict[str, List[str]],
    ground_truth:   Optional[Dict[str, List[str]]] = None,
    chunk_size:     int  = 500_000,
    cache_path:     Optional[str] = None,
) -> pd.DataFrame:
    """
    Build feature matrix for all candidate pairs in memory-safe chunks.
    If cache_path is provided and the file exists, load from disk instead.
    """
    if cache_path and os.path.exists(cache_path):
        logger.info(f"Loading cached features: {cache_path}")
        return pd.read_parquet(cache_path)

    # Flatten (s1_id, candidate_id) pairs
    all_pairs: List[tuple] = [
        (s1_id, cid)
        for s1_id, cands in candidates.items()
        for cid in cands
    ]
    logger.info(f"Building features for {len(all_pairs):,} pairs in chunks of {chunk_size:,}...")

    result_chunks = []
    for i in range(0, len(all_pairs), chunk_size):
        batch_pairs = all_pairs[i: i + chunk_size]

        # Rebuild candidate dict for just this batch
        batch_candidates: Dict[str, List[str]] = {}
        for s1_id, cid in batch_pairs:
            batch_candidates.setdefault(s1_id, []).append(cid)

        chunk_df = build_feature_matrix(
            s1_records=s1_records,
            candidate_records=s23_records,
            candidate_pairs=batch_candidates,
            ground_truth=ground_truth,
        )
        result_chunks.append(chunk_df)

        done = min(i + chunk_size, len(all_pairs))
        if (i // chunk_size + 1) % 5 == 0 or done == len(all_pairs):
            logger.info(f"  Features: {done:,}/{len(all_pairs):,} pairs")

        del chunk_df, batch_candidates
        gc.collect()

    result = pd.concat(result_chunks, ignore_index=True)
    del result_chunks
    gc.collect()

    if cache_path:
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        result.to_parquet(cache_path, index=False)
        logger.info(f"Features cached: {cache_path}")

    return result


# ── Training stage ────────────────────────────────────────────────────────────

def run_train(config, model_save_path: str = "models/matcher.pkl") -> float:
    """Full training pipeline. Returns best validation F0.5."""
    logger.info("=" * 60)
    logger.info("STAGE: TRAINING (SCALABLE PIPELINE)")
    logger.info("=" * 60)

    os.makedirs("models", exist_ok=True)
    os.makedirs("models/blocking_cache", exist_ok=True)
    norm_cache = "models/blocking_cache/normalized"
    os.makedirs(norm_cache, exist_ok=True)

    # 1. Load data ──────────────────────────────────────────────────────────
    logger.info("Stage 1: Loading training data...")
    sources = load_sources(config.data.train_dir, mode="train")
    s1  = sources["s1"]
    s2  = sources["s2"]
    s3  = sources["s3"]
    gt_df = sources["gt"]
    gt_dict = ground_truth_to_dict(gt_df)
    del gt_df
    gc.collect()
    logger.info(f"Loaded: S1={len(s1):,}, S2={len(s2):,}, S3={len(s3):,}")

    # 2. Normalize (with disk cache) ────────────────────────────────────────
    logger.info("Stage 2: Normalising text (cached to disk)...")
    init_normalizer(config.normalization.abbreviation_file)

    s1_norm_path  = f"{norm_cache}/s1_norm.parquet"
    s23_norm_path = f"{norm_cache}/s23_norm.parquet"

    if os.path.exists(s1_norm_path):
        logger.info("  Loading cached normalised S1...")
        s1 = pd.read_parquet(s1_norm_path)
    else:
        s1 = normalize_in_chunks(s1)
        s1.to_parquet(s1_norm_path, index=False)
        logger.info(f"  S1 normalised and cached → {s1_norm_path}")

    if os.path.exists(s23_norm_path):
        logger.info("  Loading cached normalised S2+S3...")
        s23 = pd.read_parquet(s23_norm_path)
    else:
        s2  = normalize_in_chunks(s2)
        s3  = normalize_in_chunks(s3)
        s23 = pd.concat([s2, s3], ignore_index=True)
        del s2, s3
        gc.collect()
        s23.to_parquet(s23_norm_path, index=False)
        logger.info(f"  S2+S3 normalised and cached → {s23_norm_path}")

    logger.info(f"  S2+S3 combined: {len(s23):,} records")

    # 3. Train / val split ──────────────────────────────────────────────────
    from sklearn.model_selection import train_test_split
    all_s1_ids = s1["entity_id"].tolist()
    train_s1_ids, val_s1_ids = train_test_split(
        all_s1_ids,
        test_size=config.validation.split_ratio,
        random_state=config.validation.random_seed,
    )
    train_s1_set = set(train_s1_ids)
    val_s1_set   = set(val_s1_ids)
    logger.info(f"  Train S1: {len(train_s1_ids):,} | Val S1: {len(val_s1_ids):,}")

    train_gt = {k: v for k, v in gt_dict.items() if k in train_s1_set}
    val_gt   = {k: v for k, v in gt_dict.items() if k in val_s1_set}
    train_s1 = s1[s1["entity_id"].isin(train_s1_set)].reset_index(drop=True)
    val_s1   = s1[s1["entity_id"].isin(val_s1_set  )].reset_index(drop=True)

    # 4. Blocking (chunked + disk-cached) ───────────────────────────────────
    logger.info("Stage 3: Building blocking candidates (TRAIN)...")
    train_candidates = build_blocking_index(
        train_s1, s23,
        config=config.blocking,
        use_cache=True,
    )

    # Measure blocking recall on a 50k-entity sample (full set is too slow)
    logger.info("  Measuring blocking recall on 50k-entity sample...")
    sample_gt    = {k: v for i, (k, v) in enumerate(train_gt.items()) if i < 50_000}
    sample_cands = {k: train_candidates.get(k, []) for k in sample_gt}
    recall_info  = compute_blocking_recall(sample_cands, sample_gt)
    logger.info(
        f"  BLOCKING RECALL (sample): {recall_info['blocking_recall']:.4f} "
        f"({recall_info['n_covered']}/{recall_info['n_gt_pairs']} pairs)"
    )
    if recall_info["blocking_recall"] < 0.90:
        logger.warning("⚠️  Blocking recall < 0.90 — raise tfidf_top_k in config.yaml")

    # 5. Hard negative mining ───────────────────────────────────────────────
    logger.info("Stage 4: Mining hard negatives...")
    enriched_candidates = mine_hard_negatives(
        train_s1_ids,
        train_candidates,
        train_gt,
        n_hard_per_positive=config.matching.hard_negative_ratio,
    )

    # 6. Record dicts ───────────────────────────────────────────────────────
    logger.info("Stage 5: Building record lookup dicts...")
    s1_records  = df_to_record_dict(train_s1)
    s23_records = df_to_record_dict(s23)

    # 7. Feature matrix ─────────────────────────────────────────────────────
    logger.info("Stage 6: Building training feature matrix...")
    train_feature_df = build_feature_matrix_chunked(
        s1_records, s23_records, enriched_candidates,
        ground_truth=train_gt,
        cache_path="models/blocking_cache/train_features.parquet",
    )
    logger.info(f"  Train feature matrix: {train_feature_df.shape}")

    # 8. Train LightGBM ─────────────────────────────────────────────────────
    logger.info("Stage 7: Training LightGBM...")
    model, feature_names = train_matcher(
        train_feature_df, config.matching, model_save_path
    )

    # 9. Validation (on 20k-entity subset for speed) ────────────────────────
    logger.info("Stage 8: Validation on 20k S1 subset...")
    val_s1_small    = val_s1.iloc[:20_000].reset_index(drop=True)
    val_s1_ids_sm   = val_s1_small["entity_id"].tolist()
    val_gt_small    = {k: v for k, v in val_gt.items() if k in set(val_s1_ids_sm)}
    val_s1_recs     = df_to_record_dict(val_s1_small)

    val_candidates  = build_blocking_index(
        val_s1_small, s23,
        config=config.blocking,
        use_cache=False,
    )
    val_feature_df  = build_feature_matrix_chunked(
        val_s1_recs, s23_records, val_candidates,
        ground_truth=val_gt_small,
        cache_path="models/blocking_cache/val_features.parquet",
    )

    best_thresh, best_f05 = calibrate_threshold(
        val_feature_df, val_gt_small, model, feature_names
    )
    config.matching.threshold = best_thresh

    val_scores = predict_scores(model, feature_names, val_feature_df)
    val_preds  = apply_threshold(val_feature_df, val_scores, best_thresh, val_s1_ids_sm)
    val_results = compute_macro_f05(val_preds, val_gt_small)
    print_evaluation_report(val_results)

    with open("models/threshold.json", "w") as f:
        json.dump({"threshold": best_thresh, "val_f05": best_f05}, f)
    logger.info(f"Threshold saved → models/threshold.json")

    return best_f05


# ── Prediction stage ──────────────────────────────────────────────────────────

def run_predict(config, model_path: str = "models/matcher.pkl") -> None:
    """Run inference on the test set and write output TSV files."""
    logger.info("=" * 60)
    logger.info("STAGE: PREDICTION (SCALABLE PIPELINE)")
    logger.info("=" * 60)

    # Load calibrated threshold
    threshold = config.matching.threshold
    if os.path.exists("models/threshold.json"):
        with open("models/threshold.json") as f:
            threshold = json.load(f)["threshold"]
    logger.info(f"Using threshold: {threshold:.3f}")

    # 1. Load test data ─────────────────────────────────────────────────────
    sources = load_sources(config.data.test_dir, mode="test")
    s1, s2, s3 = sources["s1"], sources["s2"], sources["s3"]
    logger.info(f"Test: S1={len(s1):,}, S2={len(s2):,}, S3={len(s3):,}")

    init_normalizer(config.normalization.abbreviation_file)

    # 2. Normalise (cached) ─────────────────────────────────────────────────
    test_norm = "models/blocking_cache/test_normalized"
    os.makedirs(test_norm, exist_ok=True)
    s1_path  = f"{test_norm}/s1.parquet"
    s23_path = f"{test_norm}/s23.parquet"

    if os.path.exists(s1_path):
        s1 = pd.read_parquet(s1_path)
    else:
        s1 = normalize_in_chunks(s1)
        s1.to_parquet(s1_path, index=False)

    if os.path.exists(s23_path):
        s23 = pd.read_parquet(s23_path)
    else:
        s2  = normalize_in_chunks(s2)
        s3  = normalize_in_chunks(s3)
        s23 = pd.concat([s2, s3], ignore_index=True)
        del s2, s3
        gc.collect()
        s23.to_parquet(s23_path, index=False)

    # 3. Blocking ───────────────────────────────────────────────────────────
    logger.info("Building test blocking candidates...")
    os.makedirs("models/blocking_cache/test_blocking", exist_ok=True)
    candidates = build_blocking_index(
        s1, s23, config=config.blocking, use_cache=True
    )

    # 4. Feature matrix ─────────────────────────────────────────────────────
    logger.info("Building test feature matrix...")
    s1_records  = df_to_record_dict(s1)
    s23_records = df_to_record_dict(s23)
    feature_df  = build_feature_matrix_chunked(
        s1_records, s23_records, candidates,
        cache_path="models/blocking_cache/test_features.parquet",
    )

    # 5. Inference ──────────────────────────────────────────────────────────
    logger.info("Running inference...")
    model, feature_names = load_matcher(model_path)

    if len(feature_df) == 0:
        logger.warning("No candidate pairs — all predictions will be singletons.")
        predictions = {sid: [] for sid in s1["entity_id"]}
    else:
        score_chunks = []
        batch_size   = 500_000
        for i in range(0, len(feature_df), batch_size):
            batch        = feature_df.iloc[i: i + batch_size]
            batch_scores = predict_scores(model, feature_names, batch)
            score_chunks.append(batch_scores)
            logger.info(f"  Scored {min(i + batch_size, len(feature_df)):,}/{len(feature_df):,}")
        all_scores  = pd.concat(score_chunks)
        predictions = apply_threshold(
            feature_df, all_scores, threshold, s1["entity_id"].tolist()
        )

    # 6. Write output ───────────────────────────────────────────────────────
    os.makedirs(config.data.output_dir, exist_ok=True)
    write_output_files(
        candidates=candidates,
        predictions=predictions,
        all_s1_ids=s1["entity_id"].tolist(),
        output_dir=config.data.output_dir,
    )
    logger.info("✅ Prediction complete!")
    logger.info(f"→ Upload output/matching_results.tsv to the Unstop portal")


# ── Entrypoint ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Amazon ML Challenge 2026 — Scalable ER Pipeline"
    )
    parser.add_argument("--mode",   choices=["train", "predict", "full"], default="full")
    parser.add_argument("--config", default="configs/config.yaml")
    parser.add_argument("--model",  default="models/matcher.pkl")
    args = parser.parse_args()

    config = load_config(args.config)
    t0     = time.time()

    if args.mode in ("train", "full"):
        val_f05 = run_train(config, model_save_path=args.model)
        logger.info(f"Training done. Val F₀.₅: {val_f05:.4f}")

    if args.mode in ("predict", "full"):
        run_predict(config, model_path=args.model)

    elapsed = time.time() - t0
    logger.info(f"Total time: {elapsed / 60:.1f} minutes")


if __name__ == "__main__":
    main()
