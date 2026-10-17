AMAZON ML CHALLENGE 2026 — COPILOT MASTER PROMPT — PART 4 of 4
==============================================================
ACTION: Run the full pipeline and produce the submission file.

=== STEP A: Delete stale blocking cache (CRITICAL) ===
The old TF-IDF cache files from failed runs must be removed.
Run in terminal:
  cd D:\work\Projects\amazon_ml_challenge
  venv\Scripts\activate

  del /Q models\blocking_cache\tfidf_candidates.pkl 2>nul
  del /Q models\blocking_cache\token_candidates.pkl 2>nul
  del /Q models\blocking_cache\soundex_candidates.pkl 2>nul
  del /Q models\blocking_cache\exact_candidates.pkl 2>nul
  del /Q models\blocking_cache\train_features.pkl 2>nul
  del /Q models\blocking_cache\val_features.pkl 2>nul
  del /Q models\blocking_cache\test_features.pkl 2>nul
  del /Q models\matcher.pkl 2>nul
  del /Q models\threshold.json 2>nul

DO NOT delete:
  models\blocking_cache\normalized\s1_norm.parquet   (keep - saves 5 min)
  models\blocking_cache\normalized\s23_norm.parquet  (keep - saves 10 min)

=== STEP B: Start training ===
Run this command and leave it running:
  python code\business_entity_resolution\src\run_pipeline.py --mode train --config configs\config.yaml

Monitor progress in a SECOND terminal:
  Get-Content pipeline.log -Tail 20 -Wait

Expected output sequence (do not interrupt):
  Stage 1: Loading data...                    (~2 min)
  Stage 2: Normalising... loaded from cache   (~1 min, uses cached files)
  Stage 3: Blocking (token + soundex + exact) (~30-45 min)
    - Exact blocking done
    - Token inverted index: 200,000/2,206,821 (updates every 200k)
    - Soundex blocking done
    - Blocking complete: X,XXX,XXX candidates
  BLOCKING RECALL: 0.9X  (target: above 0.85)
  Stage 4: Mining hard negatives...           (~2 min)
  Stage 5: Feature engineering...             (~45-90 min)
    - Features: 500,000/XX,XXX,XXX
    - Features cached
  Stage 6: Training LightGBM...               (~5-10 min)
    - Top features printed
    - Model saved to models/matcher.pkl
  Stage 7: Validation...                      (~15 min)
    - Best threshold: 0.XX
    - Macro F0.5: 0.XXXX
  Threshold saved to models/threshold.json

=== STEP C: If training crashes with MemoryError ===
Open configs\config.yaml and change:
  max_candidates_per_s1: 100  →  max_candidates_per_s1: 50
Delete models\blocking_cache\token_candidates.pkl
Re-run training. It will resume using cached normalization.

=== STEP D: After training finishes - run prediction ===
Run immediately after training completes:
  python code\business_entity_resolution\src\run_pipeline.py --mode predict --config configs\config.yaml

Expected output:
  Test: S1=X,XXX,XXX S2=X,XXX,XXX S3=X,XXX,XXX
  Blocking test set...
  Building features...
  Running inference...
  Prediction complete. Upload output/matching_results.tsv to Unstop.

=== STEP E: Validate submission ===
  python code\business_entity_resolution\utils\validate_submission.py --matching output\matching_results.tsv --candidate output\candidate_pairs.tsv --test-dir dataset\test

MUST see: PASS
If you see any ERROR — paste it here immediately.

=== STEP F: Upload ===
Go to Unstop competition portal.
Upload ONLY the file: output\matching_results.tsv
Do NOT upload the zip yet — just this one file for the leaderboard score.

=== STEP G: Report the score ===
After upload, Unstop shows your F0.5 score on the public leaderboard.
Come back to Claude and share that number.
Target: above 0.90 for first run, then we improve further.

=== IF TRAINING RUNS FOR MORE THAN 3 HOURS ===
It is likely stuck on feature engineering. Do NOT cancel it.
Open a second terminal and check RAM:
  tasklist | findstr python

If RAM usage is above 12GB, the process will crash.
If it crashes, open configs\config.yaml and change chunk_size in build_features_chunked.
Actually - just wait. Feature engineering for 2.2M * 100 candidates = 220M pairs processed
in 300k chunks = ~733 iterations. At 5 seconds per chunk = ~1 hour total.

=== WHAT TO DO WHILE WAITING ===
1. Keep the training terminal open
2. Monitor with: Get-Content pipeline.log -Tail 5 -Wait
3. Do NOT open VS Code tasks that use a lot of RAM
4. Keep laptop plugged into power

=== SUMMARY OF WHAT THIS PIPELINE DOES ===
Blocker (token+soundex+exact): finds ~80-120 candidates per S1 entity
Features (rapidfuzz):          22 similarity scores per candidate pair
LightGBM:                      scores each pair, trained on GT + hard negatives
Threshold:                     F0.5-calibrated cutoff
Output:                        matching_results.tsv for Unstop upload

Expected F0.5 score: 0.88 - 0.93 on public leaderboard
