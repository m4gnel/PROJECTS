"""
notebooks/01_eda.py
Exploratory Data Analysis — run this FIRST after downloading dataset.

Run: python notebooks/01_eda.py
Produces: printed stats + saves plots to notebooks/figures/
"""
import os
import sys
sys.path.insert(0, "code/business_entity_resolution/src")

import pandas as pd
import numpy as np

# ── Load data ──────────────────────────────────────────────────────────────────
print("=" * 60)
print("EDA: Amazon ML Challenge 2026 — Business Entity Resolution")
print("=" * 60)

TRAIN_DIR = "dataset/train"

def load_tsv(path):
    return pd.read_csv(path, sep="\t", dtype=str, keep_default_na=False)

try:
    s1 = load_tsv(os.path.join(TRAIN_DIR, "train_source1.tsv"))
    s2 = load_tsv(os.path.join(TRAIN_DIR, "train_source2.tsv"))
    s3 = load_tsv(os.path.join(TRAIN_DIR, "train_source3.tsv"))
    gt = load_tsv(os.path.join(TRAIN_DIR, "train_ground_truth.tsv"))
    print("[OK] All training files loaded.\n")
except FileNotFoundError as e:
    print(f"[ERROR] {e}")
    print("Place dataset files in dataset/train/ first.")
    sys.exit(1)

# ── Section 1: Basic Shapes ────────────────────────────────────────────────────
print("── SECTION 1: Data Shapes ──")
for name, df in [("Source 1", s1), ("Source 2", s2), ("Source 3", s3), ("Ground Truth", gt)]:
    print(f"  {name}: {df.shape[0]:,} rows × {df.shape[1]} cols")

print()

# ── Section 2: Null Analysis ───────────────────────────────────────────────────
print("── SECTION 2: Null / Empty Values ──")
for name, df in [("S1", s1), ("S2", s2), ("S3", s3)]:
    for col in ["business_name", "business_address"]:
        n_null = (df[col].isnull() | (df[col].str.strip() == "")).sum()
        pct = 100 * n_null / len(df)
        print(f"  {name}.{col}: {n_null:,} empty ({pct:.1f}%)")
print()

# ── Section 3: Country Distribution ───────────────────────────────────────────
print("── SECTION 3: Country Distribution ──")
for name, df in [("S1", s1), ("S2", s2), ("S3", s3)]:
    print(f"  {name}:")
    print(df["country"].value_counts().to_string(header=False))
    print()

# ── Section 4: Match Distribution ─────────────────────────────────────────────
print("── SECTION 4: Match Cardinality Distribution ──")
gt["matched_entity_ids"] = gt["matched_entity_ids"].fillna("")
gt["n_matches"] = gt["matched_entity_ids"].apply(
    lambda x: len(x.split(",")) if x.strip() else 0
)
dist = gt["n_matches"].value_counts().sort_index()
print("  n_matches → count:")
for k, v in dist.items():
    pct = 100 * v / len(gt)
    print(f"    {k} match(es): {v:,} S1 entities ({pct:.1f}%)")
print()

n_singletons = (gt["n_matches"] == 0).sum()
n_with_matches = (gt["n_matches"] > 0).sum()
print(f"  Singletons (0 matches): {n_singletons:,} ({100*n_singletons/len(gt):.1f}%)")
print(f"  Has matches (≥1):       {n_with_matches:,} ({100*n_with_matches/len(gt):.1f}%)")
print()

# ── Section 5: Name/Address Length Stats ──────────────────────────────────────
print("── SECTION 5: Text Length Stats ──")
for name, df in [("S1", s1), ("S2", s2), ("S3", s3)]:
    name_lens = df["business_name"].str.len()
    addr_lens = df["business_address"].str.len()
    print(f"  {name} name length:  min={name_lens.min()}, median={name_lens.median():.0f}, max={name_lens.max()}")
    print(f"  {name} addr length:  min={addr_lens.min()}, median={addr_lens.median():.0f}, max={addr_lens.max()}")
print()

# ── Section 6: Sample Positive Pairs ─────────────────────────────────────────
print("── SECTION 6: Sample Positive Pairs (manual inspection) ──")
s1_dict = s1.set_index("entity_id").to_dict("index")
s2_dict = s2.set_index("entity_id").to_dict("index")
s3_dict = s3.set_index("entity_id").to_dict("index")
s23_dict = {**s2_dict, **s3_dict}

positive_pairs = []
for _, row in gt.iterrows():
    s1_id = row["source1_entity_id"]
    if row["matched_entity_ids"].strip():
        for mid in row["matched_entity_ids"].split(","):
            mid = mid.strip()
            if mid:
                positive_pairs.append((s1_id, mid))

print(f"  Total positive pairs in GT: {len(positive_pairs):,}")
print(f"  Sampling 5 for inspection:")
print()
import random
random.seed(42)
sample = random.sample(positive_pairs, min(5, len(positive_pairs)))
for s1_id, mid in sample:
    s1_rec = s1_dict.get(s1_id, {})
    c_rec = s23_dict.get(mid, {})
    print(f"  S1: {s1_id}")
    print(f"    name: '{s1_rec.get('business_name', '')}'")
    print(f"    addr: '{s1_rec.get('business_address', '')}'")
    print(f"  {mid[0:2]}: {mid}")
    print(f"    name: '{c_rec.get('business_name', '')}'")
    print(f"    addr: '{c_rec.get('business_address', '')}'")
    print()

# ── Section 7: Similarity Stats on Positive Pairs ─────────────────────────────
print("── SECTION 7: Similarity Stats on Positive Pairs ──")
try:
    from rapidfuzz import fuzz
    sample_pairs = random.sample(positive_pairs, min(500, len(positive_pairs)))
    lev_scores = []
    tset_scores = []
    for s1_id, mid in sample_pairs:
        s1_rec = s1_dict.get(s1_id, {})
        c_rec = s23_dict.get(mid, {})
        n1 = s1_rec.get("business_name", "").lower()
        n2 = c_rec.get("business_name", "").lower()
        lev_scores.append(fuzz.ratio(n1, n2) / 100.0)
        tset_scores.append(fuzz.token_set_ratio(n1, n2) / 100.0)

    print(f"  Name Levenshtein on {len(sample_pairs)} positive pairs:")
    print(f"    min={min(lev_scores):.3f}, median={np.median(lev_scores):.3f}, mean={np.mean(lev_scores):.3f}")
    print(f"    Pairs with lev < 0.5: {sum(1 for s in lev_scores if s < 0.5)}")
    print()
    print(f"  Name TokenSet on {len(sample_pairs)} positive pairs:")
    print(f"    min={min(tset_scores):.3f}, median={np.median(tset_scores):.3f}, mean={np.mean(tset_scores):.3f}")
    print(f"    Pairs with tset < 0.5: {sum(1 for s in tset_scores if s < 0.5)}")
    print()
    print(f"  ⚠️  Min similarity = {min(lev_scores):.3f} — blocking threshold must be below this")
except ImportError:
    print("  rapidfuzz not installed. Run: pip install rapidfuzz")

print()
print("=" * 60)
print("EDA COMPLETE")
print("=" * 60)
print()
print("Next steps:")
print("  1. Review sample positive pairs above for noise patterns")
print("  2. Check null rates — if >5% name null, adjust blocking")
print("  3. Note singleton % — singletons are scored too")
print("  4. Run: python src/run_pipeline.py --mode train")
