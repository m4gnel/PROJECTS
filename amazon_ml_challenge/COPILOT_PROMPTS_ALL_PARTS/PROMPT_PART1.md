AMAZON ML CHALLENGE 2026 — COPILOT MASTER PROMPT — PART 1 of 4
==============================================================
READ THIS ENTIRE PART BEFORE DOING ANYTHING. DO NOT START CODING YET.

=== SITUATION ===
I am competing in Amazon ML Challenge 2026 (Business Entity Resolution).
I have 5 hours left to submit. I need a working submission uploaded to Unstop.

Hardware: Lenovo LOQ, RTX 4050 6GB VRAM, 16GB RAM, 20GB free SSD, Windows 11
Project:  D:\work\Projects\amazon_ml_challenge\
Venv:     D:\work\Projects\amazon_ml_challenge\venv\  (Python 3.11, already set up)

=== WHAT ALREADY EXISTS AND WORKS ===
- venv with: pandas, numpy, lightgbm, rapidfuzz, scikit-learn, pyarrow, sentence-transformers
- dataset/train/ has all 4 TSV files (S1=2.2M rows, S2=5M, S3=5.3M, GT=2.2M)
- dataset/test/ has all 3 TSV files
- models/blocking_cache/normalized/s1_norm.parquet  ← S1 already normalized, DO NOT redo
- models/blocking_cache/normalized/s23_norm.parquet ← S2+S3 already normalized, DO NOT redo
- code/business_entity_resolution/src/ has all pipeline Python files
- configs/config.yaml exists
- output/ folder exists

=== WHAT FAILED AND WHY ===
The TF-IDF blocking failed with MemoryError. Root cause:
TF-IDF requires computing a (chunk_size × 10,320,219) dense similarity matrix.
Even at chunk_size=1000, that is 1000 × 10.3M × 4 bytes = 39 GB. Impossible on 16GB RAM.

=== THE PLAN (DO NOT DEVIATE FROM THIS) ===
Replace TF-IDF blocking entirely with TOKEN INVERTED INDEX blocking.
This uses a Python dict — zero matrix multiplication — fits in 3GB RAM.

The pipeline will be:
1. Load cached normalized data (already done, instant)
2. Token inverted index blocking (new - replaces TF-IDF)
3. Soundex phonetic blocking (already works)
4. Union the two blockers
5. Build string similarity features with rapidfuzz
6. Train LightGBM classifier
7. Predict on test set
8. Validate output
9. Done

=== KEY CONSTRAINTS (NEVER VIOLATE) ===
- NO TF-IDF cosine similarity anywhere in blocker.py
- NO dense matrix multiplication against 10M records
- NO external API calls
- NO one-hot encoding of country column
- Model must be MIT/Apache 2.0, max 8B params
- Every S1 entity must appear in output/matching_results.tsv
- Threshold must optimize F0.5 not F1
- Use the existing venv at D:\work\Projects\amazon_ml_challenge\venv\

=== DO NOT START CODING YET ===
Reply "READY FOR PART 2" to receive the exact code to write.
