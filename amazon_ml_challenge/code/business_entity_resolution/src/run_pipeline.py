"""
run_pipeline.py — Scalable ER pipeline for Amazon ML Challenge 2026.
Memory-safe: uses token/soundex blocking, PyArrow dataset feature streaming, instant feature caching.
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
import pyarrow.dataset as ds

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import load_config
from data_loader import load_sources, ground_truth_to_dict
from normalizer import initialize as init_normalizer, normalize_dataframe
from blocker import build_blocking_index, compute_blocking_recall
from feature_engineer import build_feature_matrix, FEATURE_COLS
from matcher import train_matcher, load_matcher, predict_scores, calibrate_threshold, mine_hard_negatives
from evaluator import compute_macro_f05, print_evaluation_report
from postprocessor import apply_threshold, write_output_files

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(module)s: %(message)s",
    handlers=[logging.FileHandler("pipeline.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

CACHE_DIR = "models/blocking_cache"


def _save(df_or_obj, path: str):
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    try:
        if isinstance(df_or_obj, pd.DataFrame):
            df_or_obj.to_parquet(path, index=False)
        else:
            with open(path, "wb") as f:
                pickle.dump(df_or_obj, f, protocol=4)
    except Exception:
        pkl = path.replace(".parquet", ".pkl")
        with open(pkl, "wb") as f:
            pickle.dump(df_or_obj, f, protocol=4)
        logger.info(f"Saved as pickle: {pkl}")


def _load(path: str):
    for p in [path, path.replace(".parquet", ".pkl")]:
        if not os.path.exists(p):
            continue
        try:
            if p.endswith(".parquet"):
                return pd.read_parquet(p)
            with open(p, "rb") as f:
                return pickle.load(f)
        except Exception:
            continue
    return None


def df_to_records(df: pd.DataFrame) -> Dict[str, dict]:
    result = {}
    for row in df.itertuples():
        result[row.entity_id] = {
            "entity_id":    row.entity_id,
            "norm_name":    str(getattr(row, "norm_name",    "") or ""),
            "norm_address": str(getattr(row, "norm_address", "") or ""),
            "norm_text":    str(getattr(row, "norm_text",    "") or ""),
            "country":      str(getattr(row, "country",      "") or ""),
        }
    return result


def normalize_in_chunks(df: pd.DataFrame, chunk_size: int = 100_000) -> pd.DataFrame:
    logger.info(f"Normalising {len(df):,} records...")
    parts = []
    for i in range(0, len(df), chunk_size):
        parts.append(normalize_dataframe(df.iloc[i: i + chunk_size].copy()))
        done = min(i + chunk_size, len(df))
        if (i // chunk_size + 1) % 5 == 0:
            logger.info(f"  {done:,}/{len(df):,}")
    out = pd.concat(parts, ignore_index=True)
    del parts
    gc.collect()
    return out


def build_features_chunked(
    s1_recs: Dict[str, dict],
    s23_recs: Dict[str, dict],
    candidates: Dict[str, List[str]],
    ground_truth: Optional[Dict[str, List[str]]] = None,
    chunk: int = 200_000,
    cache: Optional[str] = None,
) -> pd.DataFrame:
    parts_dir = cache.replace(".pkl", "_parts").replace(".parquet", "_parts") if cache else "models/blocking_cache/feature_parts"
    
    if os.path.exists(parts_dir) and len(os.listdir(parts_dir)) > 0:
        logger.info(f"Loading feature matrix directly from parts directory: {parts_dir}")
        dataset = ds.dataset(parts_dir, format="parquet")
        return dataset.to_table().to_pandas()

    if cache and os.path.exists(cache):
        cached = _load(cache)
        if cached is not None:
            logger.info(f"Features loaded from cache: {cache} ({len(cached):,} rows)")
            return cached

    os.makedirs(parts_dir, exist_ok=True)
    pairs = [(s, c) for s, cands in candidates.items() for c in cands]
    logger.info(f"Building features for {len(pairs):,} pairs in chunks of {chunk:,}...")

    n_chunks = (len(pairs) + chunk - 1) // chunk
    chunk_paths = []

    for i in range(0, len(pairs), chunk):
        chunk_idx = i // chunk
        part_path = os.path.join(parts_dir, f"part_{chunk_idx}.parquet")
        chunk_paths.append(part_path)

        if os.path.exists(part_path):
            continue

        batch = pairs[i: i + chunk]
        batch_cands: Dict[str, List[str]] = {}
        for s, c in batch:
            batch_cands.setdefault(s, []).append(c)

        part = build_feature_matrix(
            s1_records=s1_recs,
            candidate_records=s23_recs,
            candidate_pairs=batch_cands,
            ground_truth=ground_truth,
        )
        part.to_parquet(part_path, index=False)
        logger.info(f"  Chunk {chunk_idx + 1}/{n_chunks} done and cached to {part_path}")
        del part, batch_cands
        gc.collect()

    logger.info("Combining all feature chunks using PyArrow Dataset...")
    dataset = ds.dataset(parts_dir, format="parquet")
    result = dataset.to_table().to_pandas()
    gc.collect()

    if cache:
        _save(result, cache)
        logger.info(f"Features cached to main path: {cache}")
    return result


def run_train(config, model_path: str = "models/matcher.pkl") -> float:
    logger.info("=" * 60)
    logger.info("TRAINING — memory-safe token/soundex blocking")
    logger.info("=" * 60)
    os.makedirs("models", exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)

    # 1. Load data
    logger.info("Stage 1: Loading data...")
    sources = load_sources(config.data.train_dir, mode="train")
    s1, s2, s3 = sources["s1"], sources["s2"], sources["s3"]
    gt_dict = ground_truth_to_dict(sources["gt"])
    del sources
    gc.collect()
    logger.info(f"S1={len(s1):,} S2={len(s2):,} S3={len(s3):,}")

    # 2. Normalize (use cache if exists)
    logger.info("Stage 2: Normalising...")
    init_normalizer(config.normalization.abbreviation_file)
    norm_dir = os.path.join(CACHE_DIR, "normalized")
    os.makedirs(norm_dir, exist_ok=True)

    s1_path  = os.path.join(norm_dir, "s1_norm.parquet")
    s23_path = os.path.join(norm_dir, "s23_norm.parquet")

    cached_s1 = _load(s1_path)
    if cached_s1 is not None:
        logger.info("  S1 norm loaded from cache")
        s1 = cached_s1
    else:
        s1 = normalize_in_chunks(s1)
        _save(s1, s1_path)

    cached_s23 = _load(s23_path)
    if cached_s23 is not None:
        logger.info("  S2+S3 norm loaded from cache")
        s23 = cached_s23
    else:
        s2 = normalize_in_chunks(s2)
        s3 = normalize_in_chunks(s3)
        s23 = pd.concat([s2, s3], ignore_index=True)
        del s2, s3
        gc.collect()
        _save(s23, s23_path)
    logger.info(f"  S2+S3: {len(s23):,} records")
    s23_recs = df_to_records(s23)

    # 3. Split
    from sklearn.model_selection import train_test_split
    all_ids = s1["entity_id"].tolist()
    tr_ids, va_ids = train_test_split(
        all_ids, test_size=config.validation.split_ratio,
        random_state=config.validation.random_seed
    )
    tr_set, va_set = set(tr_ids), set(va_ids)
    tr_gt = {k: v for k, v in gt_dict.items() if k in tr_set}
    va_gt = {k: v for k, v in gt_dict.items() if k in va_set}
    tr_s1 = s1[s1["entity_id"].isin(tr_set)].reset_index(drop=True)
    va_s1 = s1[s1["entity_id"].isin(va_set)].reset_index(drop=True)
    logger.info(f"  Train={len(tr_ids):,} Val={len(va_ids):,}")

    # 4-6. Blocking & Feature Matrix (Fast-path if model or features exist on disk)
    feat_cache = os.path.join(CACHE_DIR, "train_features.parquet")
    feat_parts_dir = os.path.join(CACHE_DIR, "train_features_parts")

    if os.path.exists(model_path):
        logger.info(f"Stage 6: LightGBM model already trained and saved to {model_path} — loading trained model directly!")
        model, feat_names = load_matcher(model_path)
    else:
        if os.path.exists(feat_cache) or (os.path.exists(feat_parts_dir) and len(os.listdir(feat_parts_dir)) >= 180):
            logger.info("Stage 3-5: Training feature matrix already exists on disk — loading directly via PyArrow Dataset!")
            dataset = ds.dataset(feat_parts_dir if os.path.exists(feat_parts_dir) else feat_cache, format="parquet")
            tr_feats = dataset.to_table().to_pandas()
            gc.collect()
            logger.info(f"  Loaded train features from disk: {tr_feats.shape}")
        else:
            logger.info("Stage 3: Blocking (token + soundex + exact name)...")
            tr_cands = build_blocking_index(tr_s1, s23, config=config.blocking, use_cache=True, prefix="train")

            sample_gt    = {k: v for i, (k, v) in enumerate(tr_gt.items()) if i < 30_000}
            sample_cands = {k: tr_cands.get(k, []) for k in sample_gt}
            rec = compute_blocking_recall(sample_cands, sample_gt)
            logger.info(
                f"BLOCKING RECALL (30k sample): {rec['blocking_recall']:.4f} "
                f"({rec['n_covered']}/{rec['n_gt_pairs']} pairs)"
            )

            logger.info("Stage 4: Mining hard negatives...")
            enriched = mine_hard_negatives(
                tr_ids, tr_cands, tr_gt,
                n_hard_per_positive=config.matching.hard_negative_ratio
            )

            logger.info("Stage 5: Feature engineering (train)...")
            tr_recs  = df_to_records(tr_s1)
            tr_feats = build_features_chunked(
                tr_recs, s23_recs, enriched,
                ground_truth=tr_gt,
                cache=feat_cache,
            )
            logger.info(f"  Train features: {tr_feats.shape}")

        # Train LightGBM
        logger.info("Stage 6: Training LightGBM...")
        model, feat_names = train_matcher(tr_feats, config.matching, model_path)

    # 8. Validation (20k subset)
    logger.info("Stage 7: Validation on 20k S1 subset...")
    va_small    = va_s1.iloc[:20_000].reset_index(drop=True)
    va_ids_sm   = va_small["entity_id"].tolist()
    va_gt_sm    = {k: v for k, v in va_gt.items() if k in set(va_ids_sm)}
    va_recs     = df_to_records(va_small)
    va_cands    = build_blocking_index(va_small, s23, config=config.blocking, use_cache=True, prefix="val")
    va_feats    = build_features_chunked(
        va_recs, s23_recs, va_cands, ground_truth=va_gt_sm,
        cache=os.path.join(CACHE_DIR, "val_features.parquet"),
    )

    best_t, best_f = calibrate_threshold(va_feats, va_gt_sm, model, feat_names)
    va_scores = predict_scores(model, feat_names, va_feats)
    va_preds  = apply_threshold(va_feats, va_scores, best_t, va_ids_sm)
    print_evaluation_report(compute_macro_f05(va_preds, va_gt_sm))

    with open("models/threshold.json", "w") as f:
        json.dump({"threshold": best_t, "val_f05": best_f}, f)
    logger.info(f"Best threshold {best_t:.3f} saved.")
    return best_f


def run_predict(config, model_path: str = "models/matcher.pkl") -> None:
    logger.info("=" * 60)
    logger.info("PREDICTION")
    logger.info("=" * 60)

    threshold = config.matching.threshold
    if os.path.exists("models/threshold.json"):
        threshold = json.load(open("models/threshold.json"))["threshold"]
    threshold = min(threshold, 0.50)
    logger.info(f"Threshold for inference: {threshold:.3f}")

    sources = load_sources(config.data.test_dir, mode="test")
    s1, s2, s3 = sources["s1"], sources["s2"], sources["s3"]
    logger.info(f"Test: S1={len(s1):,} S2={len(s2):,} S3={len(s3):,}")

    init_normalizer(config.normalization.abbreviation_file)
    test_norm = os.path.join(CACHE_DIR, "test_normalized")
    os.makedirs(test_norm, exist_ok=True)

    cached = _load(os.path.join(test_norm, "s1.parquet"))
    s1 = cached if cached is not None else normalize_in_chunks(s1)
    if cached is None:
        _save(s1, os.path.join(test_norm, "s1.parquet"))

    cached23 = _load(os.path.join(test_norm, "s23.parquet"))
    if cached23 is not None:
        s23 = cached23
    else:
        s2 = normalize_in_chunks(s2)
        s3 = normalize_in_chunks(s3)
        s23 = pd.concat([s2, s3], ignore_index=True)
        del s2, s3
        gc.collect()
        _save(s23, os.path.join(test_norm, "s23.parquet"))

    logger.info("Blocking test set...")
    candidates = build_blocking_index(s1, s23, config=config.blocking, use_cache=True, prefix="test")

    s1_recs  = df_to_records(s1)
    s23_recs = df_to_records(s23)
    feats    = build_features_chunked(
        s1_recs, s23_recs, candidates,
        cache=os.path.join(CACHE_DIR, "test_features.parquet"),
    )

    model, feat_names = load_matcher(model_path)
    if len(feats) == 0:
        preds = {sid: [] for sid in s1["entity_id"]}
    else:
        all_scores = pd.concat([
            predict_scores(model, feat_names, feats.iloc[i: i + 500_000])
            for i in range(0, len(feats), 500_000)
        ])
        preds = apply_threshold(feats, all_scores, threshold, s1["entity_id"].tolist())

    os.makedirs(config.data.output_dir, exist_ok=True)
    write_output_files(candidates, preds, s1["entity_id"].tolist(), config.data.output_dir)
    logger.info("Prediction complete. Upload output/matching_results.tsv to Unstop.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mode",   choices=["train", "predict", "full"], default="full")
    p.add_argument("--config", default="configs/config.yaml")
    p.add_argument("--model",  default="models/matcher.pkl")
    a = p.parse_args()
    cfg = load_config(a.config)
    t0  = time.time()
    if a.mode in ("train", "full"):
        f = run_train(cfg, a.model)
        logger.info(f"Val F0.5: {f:.4f}")
    if a.mode in ("predict", "full"):
        run_predict(cfg, a.model)
    logger.info(f"Total: {(time.time()-t0)/60:.1f} min")


if __name__ == "__main__":
    main()
