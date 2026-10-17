"""
evaluator.py — F₀.₅ evaluation metric.

F₀.₅ = (1.25 × Precision × Recall) / (0.25 × Precision + Recall)
Macro-averaged per S1 entity, including singletons.
"""
import logging
from typing import Dict, List, Tuple

import numpy as np

logger = logging.getLogger(__name__)


def compute_f05_per_entity(
    predicted: List[str], ground_truth: List[str]
) -> Tuple[float, float, float]:
    """
    Compute F₀.₅, Precision, Recall for a single S1 entity.
    
    Args:
        predicted: list of predicted matched IDs
        ground_truth: list of true matched IDs
    
    Returns:
        (f05, precision, recall) all in [0, 1]
    
    Edge cases:
        Both empty → (1.0, 1.0, 1.0)
        GT empty, pred non-empty → (0.0, 0.0, 1.0) — false merge
        GT non-empty, pred empty → (0.0, 1.0, 0.0) — missed all
    """
    pred_set = set(predicted)
    gt_set = set(ground_truth)
    
    # Both empty: correct singleton
    if not pred_set and not gt_set:
        return 1.0, 1.0, 1.0
    
    # GT empty but predicted something: false merge
    if not gt_set:
        return 0.0, 0.0, 1.0
    
    # GT non-empty but predicted nothing: missed all
    if not pred_set:
        return 0.0, 1.0, 0.0
    
    tp = len(pred_set & gt_set)
    precision = tp / len(pred_set)
    recall = tp / len(gt_set)
    
    if precision == 0 and recall == 0:
        return 0.0, 0.0, 0.0
    
    # F₀.₅ formula
    beta_sq = 0.25  # β=0.5, β²=0.25
    f05 = (1 + beta_sq) * precision * recall / (beta_sq * precision + recall)
    
    return f05, precision, recall


def compute_macro_f05(
    predictions: Dict[str, List[str]],
    ground_truth: Dict[str, List[str]],
) -> Dict:
    """
    Compute macro-average F₀.₅ across all S1 entities.
    
    Args:
        predictions: {s1_id: [predicted_matched_ids]}
        ground_truth: {s1_id: [true_matched_ids]}
    
    Returns:
        Dict with macro_f05, macro_precision, macro_recall, and breakdown stats
    """
    # All S1 entities that should be scored = union of both dicts
    all_s1_ids = set(ground_truth.keys()) | set(predictions.keys())
    
    f05_scores = []
    precision_scores = []
    recall_scores = []
    
    n_singletons = 0
    n_correct_singletons = 0
    n_false_merges = 0
    n_missed = 0
    
    for s1_id in all_s1_ids:
        pred = predictions.get(s1_id, [])
        gt = ground_truth.get(s1_id, [])
        
        f05, prec, rec = compute_f05_per_entity(pred, gt)
        f05_scores.append(f05)
        precision_scores.append(prec)
        recall_scores.append(rec)
        
        # Stats
        if not gt:
            n_singletons += 1
            if not pred:
                n_correct_singletons += 1
            else:
                n_false_merges += 1
        elif not pred:
            n_missed += 1
    
    macro_f05 = float(np.mean(f05_scores))
    macro_precision = float(np.mean(precision_scores))
    macro_recall = float(np.mean(recall_scores))
    
    result = {
        "macro_f05": macro_f05,
        "macro_precision": macro_precision,
        "macro_recall": macro_recall,
        "n_entities": len(all_s1_ids),
        "n_singletons": n_singletons,
        "n_correct_singletons": n_correct_singletons,
        "n_false_merges": n_false_merges,
        "n_missed_all": n_missed,
        "singleton_accuracy": n_correct_singletons / max(n_singletons, 1),
    }
    
    return result


def compute_blocking_recall(
    candidates: Dict[str, List[str]],
    ground_truth: Dict[str, List[str]],
) -> Dict:
    """
    Measure what fraction of GT positive pairs appear in the candidate set.
    This is the upper-bound recall your ML model can achieve.
    
    Returns:
        Dict with recall, n_gt_pairs, n_covered_pairs, missed_pairs list
    """
    n_gt_pairs = 0
    n_covered = 0
    missed = []
    
    for s1_id, gt_matches in ground_truth.items():
        cand_set = set(candidates.get(s1_id, []))
        for match_id in gt_matches:
            n_gt_pairs += 1
            if match_id in cand_set:
                n_covered += 1
            else:
                missed.append((s1_id, match_id))
    
    recall = n_covered / max(n_gt_pairs, 1)
    
    return {
        "blocking_recall": recall,
        "n_gt_pairs": n_gt_pairs,
        "n_covered": n_covered,
        "n_missed": len(missed),
        "missed_pairs": missed[:20],  # sample for debugging
    }


def print_evaluation_report(results: Dict) -> None:
    """Print a formatted evaluation report."""
    print("\n" + "="*60)
    print("EVALUATION REPORT")
    print("="*60)
    print(f"  Macro F0.5:          {results['macro_f05']:.4f}")
    print(f"  Macro Precision:      {results['macro_precision']:.4f}")
    print(f"  Macro Recall:         {results['macro_recall']:.4f}")
    print(f"  Total S1 Entities:    {results['n_entities']:,}")
    print(f"  Singletons:           {results['n_singletons']:,}")
    print(f"  Correct Singletons:   {results['n_correct_singletons']:,}")
    print(f"  False Merges:         {results['n_false_merges']:,}")
    print(f"  Missed All Matches:   {results['n_missed_all']:,}")
    print(f"  Singleton Accuracy:   {results['singleton_accuracy']:.4f}")
    print("="*60 + "\n")
