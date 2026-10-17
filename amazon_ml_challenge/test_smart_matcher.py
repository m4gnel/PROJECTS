import os
import time
import pandas as pd
import numpy as np
from rapidfuzz import fuzz

def compute_f05(precision, recall):
    if precision + recall == 0:
        return 0.0
    return (1.25 * precision * recall) / (0.25 * precision + recall)

def eval_subset():
    print("Evaluating smart matcher on 5,000 validation entities...")
    
    # Load normalized train data
    s1 = pd.read_parquet("models/blocking_cache/normalized/s1_norm.parquet").head(5000)
    s23 = pd.read_parquet("models/blocking_cache/normalized/s23_norm.parquet")
    
    # Load GT
    gt_df = pd.read_csv("dataset/train/train_ground_truth.tsv", sep="\t")
    gt_map = {}
    for row in gt_df.itertuples():
        gt_map[row.source1_entity_id] = set(str(row.matched_entity_ids).split(",")) if pd.notna(row.matched_entity_ids) and row.matched_entity_ids else set()

    # Index s23 by norm_name
    print("Indexing S23 by norm_name...")
    s23_by_name = {}
    s23_records = {}
    for row in s23.itertuples():
        name = str(getattr(row, "norm_name", "") or "").strip()
        country = str(getattr(row, "country", "") or "").lower()
        key = f"{country}||{name}"
        if key not in s23_by_name:
            s23_by_name[key] = []
        s23_by_name[key].append(row.entity_id)
        s23_records[row.entity_id] = (name, str(getattr(row, "norm_address", "") or "").strip(), country)

    print("Evaluating predictions with name+address scoring...")
    f05_scores = []
    
    for row in s1.itertuples():
        s1_id = row.entity_id
        s1_name = str(getattr(row, "norm_name", "") or "").strip()
        s1_addr = str(getattr(row, "norm_address", "") or "").strip()
        s1_country = str(getattr(row, "country", "") or "").lower()
        
        key = f"{s1_country}||{s1_name}"
        cands = s23_by_name.get(key, [])
        
        gt_set = gt_map.get(s1_id, set())
        
        if not cands:
            pred_set = set()
        else:
            # Score each candidate by address similarity
            scored = []
            for cid in cands:
                c_name, c_addr, c_country = s23_records[cid]
                if s1_addr and c_addr:
                    addr_sim = fuzz.token_set_ratio(s1_addr, c_addr) / 100.0
                elif not s1_addr and not c_addr:
                    addr_sim = 1.0
                else:
                    addr_sim = 0.5
                scored.append((cid, addr_sim))
            
            # Keep candidates with address_sim >= 0.60
            pred_set = {cid for cid, score in scored if score >= 0.60}
            
        # Compute precision, recall, f05 for this entity
        if not gt_set and not pred_set:
            score = 1.0
        elif not gt_set and pred_set:
            score = 0.0
        elif gt_set and not pred_set:
            score = 0.0
        else:
            tp = len(gt_set & pred_set)
            prec = tp / len(pred_set)
            rec = tp / len(gt_set)
            score = compute_f05(prec, rec)
            
        f05_scores.append(score)
        
    macro_f05 = np.mean(f05_scores)
    print(f"Validation Macro F0.5 Score: {macro_f05:.4f}")

if __name__ == "__main__":
    eval_subset()
