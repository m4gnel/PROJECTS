"""
matcher.py — LightGBM matching model.

Trains on (candidate_pair_features, label) and predicts match probability.
Includes threshold calibration for F₀.₅.
"""
import logging
import os
from typing import Dict, List, Optional, Tuple

import joblib
import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold

from evaluator import compute_macro_f05
from feature_engineer import FEATURE_COLS

logger = logging.getLogger(__name__)


def train_matcher(
    feature_df: pd.DataFrame,
    config,
    model_save_path: str = "models/matcher.pkl",
) -> lgb.LGBMClassifier:
    """
    Train LightGBM classifier on feature DataFrame.
    
    Args:
        feature_df: DataFrame with feature columns + 'label' column
        config: MatchingConfig dataclass
        model_save_path: path to save trained model
    
    Returns:
        Trained LGBMClassifier
    """
    if "label" not in feature_df.columns:
        raise ValueError("feature_df must have 'label' column for training")
    
    # Select feature columns that exist
    available_features = [c for c in FEATURE_COLS if c in feature_df.columns]
    X = feature_df[available_features].values.astype(np.float32)
    y = feature_df["label"].values.astype(int)
    
    n_pos = y.sum()
    n_neg = len(y) - n_pos
    scale_pos_weight = n_neg / max(n_pos, 1)
    
    logger.info(f"Training LightGBM: {len(X):,} pairs, {int(n_pos)} pos, {int(n_neg)} neg")
    logger.info(f"scale_pos_weight: {scale_pos_weight:.2f}")
    logger.info(f"Features: {available_features}")
    
    model = lgb.LGBMClassifier(
        n_estimators=config.n_estimators,
        learning_rate=config.learning_rate,
        max_depth=config.max_depth,
        num_leaves=config.num_leaves,
        scale_pos_weight=scale_pos_weight,
        random_state=config.random_seed,
        n_jobs=-1,
        verbose=-1,
    )
    
    model.fit(X, y)
    
    # Save model
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    joblib.dump((model, available_features), model_save_path)
    logger.info(f"Model saved to {model_save_path}")
    
    # Feature importance
    importances = pd.Series(model.feature_importances_, index=available_features)
    top_features = importances.nlargest(10)
    logger.info(f"Top features:\n{top_features.to_string()}")
    
    return model, available_features


def load_matcher(model_path: str) -> Tuple:
    """Load a saved model and its feature list."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found: {model_path}")
    model, features = joblib.load(model_path)
    logger.info(f"Loaded model from {model_path}")
    return model, features


def predict_scores(
    model: lgb.LGBMClassifier,
    feature_names: List[str],
    feature_df: pd.DataFrame,
) -> pd.Series:
    """
    Predict match probabilities for all candidate pairs.
    
    Returns:
        Series of float probabilities, indexed same as feature_df
    """
    available = [c for c in feature_names if c in feature_df.columns]
    X = feature_df[available].values.astype(np.float32)
    probs = model.predict_proba(X)[:, 1]
    return pd.Series(probs, index=feature_df.index)


def calibrate_threshold(
    val_feature_df: pd.DataFrame,
    val_ground_truth: Dict[str, List[str]],
    model: lgb.LGBMClassifier,
    feature_names: List[str],
) -> Tuple[float, float]:
    """
    Grid-search threshold [0.05, 0.95] in steps of 0.01.
    Returns (best_threshold, best_f05).
    
    Maximizes macro-F₀.₅ on validation set.
    """
    scores = predict_scores(model, feature_names, val_feature_df)
    
    # Build scored candidate pairs
    val_feature_df = val_feature_df.copy()
    val_feature_df["match_prob"] = scores.values
    
    best_thresh = 0.5
    best_f05 = 0.0
    
    thresholds = np.arange(0.05, 0.96, 0.01)
    
    for thresh in thresholds:
        # Apply threshold
        matched = (
            val_feature_df[val_feature_df["match_prob"] >= thresh]
            .groupby("s1_id")["candidate_id"]
            .apply(list)
            .to_dict()
        )
        
        # Fill in singletons (S1 entities with no matches above threshold)
        all_s1_ids = set(val_feature_df["s1_id"].unique())
        for s1_id in all_s1_ids:
            if s1_id not in matched:
                matched[s1_id] = []
        
        result = compute_macro_f05(matched, val_ground_truth)
        f05 = result["macro_f05"]
        
        if f05 > best_f05:
            best_f05 = f05
            best_thresh = thresh
    
    logger.info(f"Best threshold: {best_thresh:.2f} -> Val F0.5: {best_f05:.4f}")
    return float(best_thresh), float(best_f05)


def mine_hard_negatives(
    s1_ids: List[str],
    candidate_pairs: Dict[str, List[str]],
    ground_truth: Dict[str, List[str]],
    n_hard_per_positive: int = 5,
    n_random_per_positive: int = 2,
    rng: Optional[np.random.Generator] = None,
) -> Dict[str, List[str]]:
    """
    Create enriched candidate set with hard negatives for training.
    
    For each S1 entity:
    - Keep all GT positives
    - Add n_hard_per_positive blocking candidates that are NOT GT matches (hard negatives)
    - Add n_random_per_positive random non-GT candidates (random negatives)
    
    Returns:
        {s1_id: [positive_ids + hard_negative_ids + random_negative_ids]}
    """
    if rng is None:
        rng = np.random.default_rng(42)
    
    enriched = {}
    
    for s1_id in s1_ids:
        gt_matches = set(ground_truth.get(s1_id, []))
        blocking_candidates = candidate_pairs.get(s1_id, [])
        
        # Hard negatives: blocking candidates that are NOT GT matches
        hard_negs = [c for c in blocking_candidates if c not in gt_matches]
        
        # Sample hard negatives
        if len(hard_negs) > n_hard_per_positive * len(gt_matches):
            sampled_hard = list(rng.choice(hard_negs,
                                           size=n_hard_per_positive * max(len(gt_matches), 1),
                                           replace=False))
        else:
            sampled_hard = hard_negs
        
        enriched[s1_id] = list(gt_matches) + sampled_hard
    
    return enriched
