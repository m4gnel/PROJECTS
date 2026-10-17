"""
notebooks/02_blocking_analysis.py
Measure blocking recall and reduction ratio.
Run AFTER: python notebooks/01_eda.py

Run: python notebooks/02_blocking_analysis.py
"""
import os
import sys
sys.path.insert(0, "code/business_entity_resolution/src")

import pandas as pd

from data_loader import load_sources, ground_truth_to_dict
from normalizer import initialize as init_normalizer, normalize_dataframe
from blocker import build_blocking_index, compute_blocking_recall, \
    _bk1_tfidf_ann, _bk2_ngram_index, _bk3_country_prefix, \
    _bk4_soundex, _bk5_address_overlap
from config import load_config

print("=" * 60)
print("BLOCKING ANALYSIS")
print("=" * 60)

config = load_config()

# Load and normalize
sources = load_sources(config.data.train_dir, mode="train")
s1, s2, s3, gt_df = sources["s1"], sources["s2"], sources["s3"], sources["gt"]
gt_dict = ground_truth_to_dict(gt_df)

init_normalizer(config.normalization.abbreviation_file)
s1 = normalize_dataframe(s1)
s2 = normalize_dataframe(s2)
s3 = normalize_dataframe(s3)
s23 = pd.concat([s2, s3], ignore_index=True)

total_possible_pairs = len(s1) * len(s23)
total_gt_pairs = sum(len(v) for v in gt_dict.values())
print(f"  S1: {len(s1):,}, S2+S3: {len(s23):,}")
print(f"  Total possible pairs: {total_possible_pairs:,}")
print(f"  GT positive pairs: {total_gt_pairs:,}")
print()

# Analyze each blocking key independently
print("── Individual Blocking Key Analysis ──")

for bk_name, bk_fn, kwargs in [
    ("BK-1 TF-IDF ANN", _bk1_tfidf_ann, {"top_k": 20}),
    ("BK-2 n-gram index", _bk2_ngram_index, {"ngram_size": 3, "min_sim": 0.2}),
    ("BK-3 country+prefix", _bk3_country_prefix, {}),
    ("BK-4 Soundex", _bk4_soundex, {}),
    ("BK-5 addr overlap", _bk5_address_overlap, {"min_overlap": 2}),
]:
    try:
        cands = bk_fn(s1, s23, **kwargs)
        n_total = sum(len(v) for v in cands.values())
        recall_result = compute_blocking_recall(cands, gt_dict)
        recall = recall_result["blocking_recall"]
        ratio = n_total / max(total_possible_pairs, 1)
        print(f"  {bk_name}:")
        print(f"    Candidates: {n_total:,} ({100*ratio:.2f}% of all pairs)")
        print(f"    Recall:     {recall:.4f} ({recall_result['n_covered']}/{recall_result['n_gt_pairs']} GT pairs)")
        print()
    except Exception as e:
        print(f"  {bk_name}: ERROR — {e}")
        print()

# Full union blocking
print("── Full Union Blocking ──")
full_candidates = build_blocking_index(s1, s23, config=config.blocking)
n_total_full = sum(len(v) for v in full_candidates.values())
recall_full = compute_blocking_recall(full_candidates, gt_dict)
ratio_full = n_total_full / max(total_possible_pairs, 1)

print(f"  Total candidates (union): {n_total_full:,} ({100*ratio_full:.2f}% of all pairs)")
print(f"  Blocking recall: {recall_full['blocking_recall']:.4f}")
print(f"  GT pairs covered: {recall_full['n_covered']}/{recall_full['n_gt_pairs']}")
print()

if recall_full["blocking_recall"] < 0.98:
    print("⚠️  WARNING: Blocking recall < 0.98!")
    print("   Missed pairs (sample):")
    for s1_id, mid in recall_full.get("missed_pairs", [])[:5]:
        print(f"     {s1_id} → {mid}")
    print()
    print("   ACTION: Add more blocking keys or lower ngram_min_sim threshold")
else:
    print(f"✅  Blocking recall {recall_full['blocking_recall']:.4f} ≥ 0.98 — GOOD!")

print()
print("  Candidate distribution per S1 entity:")
counts = [len(v) for v in full_candidates.values()]
print(f"    min={min(counts)}, median={sorted(counts)[len(counts)//2]}, "
      f"max={max(counts)}, mean={sum(counts)/len(counts):.1f}")
n_empty = sum(1 for c in counts if c == 0)
print(f"    S1 entities with 0 candidates: {n_empty:,} (auto-singletons)")
