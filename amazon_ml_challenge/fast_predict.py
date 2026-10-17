import os
import pickle
import time
import pandas as pd

def main():
    t0 = time.time()
    print("Generating HIGH-PRECISION submission (top 1 per source)...")
    
    test_s1_path = "dataset/test/test_source1.tsv"
    exact_path = "models/blocking_cache/test_exact_candidates.pkl"
    token_path = "models/blocking_cache/test_token_candidates.pkl"
    
    print("1. Loading test S1 IDs...")
    s1_df = pd.read_csv(test_s1_path, sep="\t", usecols=["entity_id"])
    s1_ids = s1_df["entity_id"].tolist()
    
    print("2. Loading exact blocking candidates...")
    exact_cands = {}
    if os.path.exists(exact_path):
        with open(exact_path, "rb") as f:
            exact_cands = pickle.load(f)
            
    print("3. Loading token candidates...")
    token_cands = {}
    if os.path.exists(token_path):
        with open(token_path, "rb") as f:
            token_cands = pickle.load(f)

    print("4. Filtering to TOP 1 match per source for maximum F0.5 Precision...")
    os.makedirs("output", exist_ok=True)
    
    matching_out = "output/matching_results.tsv"
    candidate_out = "output/candidate_pairs.tsv"
    
    with open(matching_out, "w", encoding="utf-8") as fm, open(candidate_out, "w", encoding="utf-8") as fc:
        fm.write("source1_entity_id\tmatched_entity_ids\n")
        fc.write("source1_entity_id\tcandidate_entity_ids\n")
        
        for s1_id in s1_ids:
            exact = exact_cands.get(s1_id, [])
            
            # Filter to at most 1 match from S2 and at most 1 match from S3 to maximize Precision
            s2_matches = [m for m in exact if m.startswith("S2-")][:1]
            s3_matches = [m for m in exact if m.startswith("S3-")][:1]
            high_prec_matches = s2_matches + s3_matches
            
            tok_cands = token_cands.get(s1_id, [])[:15]
            all_cands = list(set(exact + tok_cands))
            
            fm.write(f"{s1_id}\t{','.join(high_prec_matches)}\n")
            fc.write(f"{s1_id}\t{','.join(all_cands)}\n")
            
    print(f"5. Done in {time.time() - t0:.2f} seconds!")
    print(f"   Matching output: {matching_out} ({os.path.getsize(matching_out):,} bytes)")

if __name__ == "__main__":
    main()
