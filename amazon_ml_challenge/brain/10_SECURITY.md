# 10_SECURITY.md
# Security & Compliance for Competition

## Fair Play Rules (from problem statement)
1. NO external data lookup (business registries, geocoding, Wikipedia, etc.)
2. NO commercial entity resolution APIs
3. NO internet access at inference time
4. Model must be MIT or Apache 2.0, ≤ 8B params

## What "No External Data" Means for Our Pipeline
- abbreviations.json: hand-crafted, not scraped ✅
- Embedding model weights: downloaded once from HuggingFace for offline use ✅
- TF-IDF vocabulary: built from provided training data only ✅
- No API calls in any .py file ✅

## Model License Verification Checklist
| Model | License | Params | Status |
|---|---|---|---|
| paraphrase-multilingual-mpnet-base-v2 | Apache 2.0 | 278M | ✅ |
| cross-encoder/ms-marco-MiniLM-L-6-v2 | Apache 2.0 | 22M | ✅ |
| LightGBM | MIT | N/A (no params) | ✅ |
| scikit-learn | BSD-3 | N/A | ✅ |

## Code Review Checklist (run before submitting code zip)
- [ ] No `requests.get()` or `urllib` calls in any source file
- [ ] No API keys or tokens in any file
- [ ] No hardcoded {US, India} lists — country is open set
- [ ] All model downloads happen from HuggingFace (offline cache OK)
- [ ] No subprocess calls to external tools
