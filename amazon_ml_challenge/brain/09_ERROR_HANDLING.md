# 09_ERROR_HANDLING.md
# Error Handling & Edge Cases

## 1. Data Loading Errors

| Error | Detection | Handler |
|---|---|---|
| Missing TSV file | `FileNotFoundError` | Log path, raise with helpful message |
| Wrong separator (comma vs tab) | Single-column DataFrame | Raise ValueError: "Did you forget sep='\\t'?" |
| Missing required column | `KeyError` | Raise ValueError listing missing columns |
| Duplicate entity_ids | `df.duplicated()` | Raise ValueError with duplicate IDs |
| Non-UTF8 encoding | `UnicodeDecodeError` | Retry with `errors='replace'`, log warning |
| Empty file | `df.shape[0] == 0` | Raise ValueError: "Empty source file" |

---

## 2. Normalization Edge Cases

| Input | Expected Output |
|---|---|
| `None` or `NaN` | `""` (empty string) |
| `"  "` (whitespace only) | `""` |
| `"Café Parisien"` | `"cafe parisien"` (unicode → ASCII approx) |
| `"AT&T Corp."` | `"att corporation"` |
| `"PVT. LTD."` | `"private limited"` |
| Very long string (>1000 chars) | Truncate to 500 chars, log warning |
| All-numeric name | Keep as-is |
| Repeated words `"Road Road"` | Normalize but don't deduplicate words |

---

## 3. Blocking Edge Cases

| Case | Handler |
|---|---|
| S1 entity with empty name AND empty address | Add to candidates via country-only key; flag as risky |
| S2/S3 record with empty name | Skip name-based BKs, use address-only |
| FAISS index empty (0 S2/S3 records) | Return empty candidates for all S1 |
| max_candidates exceeded | Rank by combined similarity score, keep top-N |
| All records from one country | Still works — no hard-coded country logic |

---

## 4. Feature Engineering Edge Cases

| Case | Handler |
|---|---|
| Both names empty | Set all name features = 0.0 |
| One name empty | Set features to 0.0; use address features only |
| Address has special chars | Normalize before feature computation |
| Same entity_id appears twice | This is a bug — raise ValueError |
| Embedding is NaN/Inf | Replace with zero vector, log warning |

---

## 5. Model Inference Edge Cases

| Case | Handler |
|---|---|
| No candidates for S1 entity | Output empty matched_entity_ids (singleton treatment) |
| model.predict_proba returns NaN | Treat as 0.0 (no match) |
| All candidates score below threshold | Output empty matched_entity_ids |
| All candidates score above threshold | This is suspicious — cap at max_candidates, log |
| Threshold calibration finds no improvement | Use default threshold 0.5 |

---

## 6. Output Writing Edge Cases

| Case | Handler |
|---|---|
| S1 entity missing from predictions | Auto-add with empty matched_entity_ids |
| Duplicate IDs in match list | Deduplicate with `list(dict.fromkeys(ids))` |
| S1 ID in matched_entity_ids | Remove it — S1 can only match S2/S3 |
| matched_entity_id not in test S2/S3 | Remove it — validator will reject |
| Output directory doesn't exist | Create with `os.makedirs(output_dir, exist_ok=True)` |

---

## 7. Validation Failures (Pre-Submission Checklist)

Run these checks BEFORE uploading:

```python
def pre_submission_check(matching_path, candidate_path, test_s1_ids, test_s23_ids):
    matching = pd.read_csv(matching_path, sep='\t', keep_default_na=False)
    candidates = pd.read_csv(candidate_path, sep='\t', keep_default_na=False)
    
    errors = []
    
    # Check 1: Every S1 test entity present
    missing = set(test_s1_ids) - set(matching['source1_entity_id'])
    if missing:
        errors.append(f"MISSING S1 IDs: {missing}")
    
    # Check 2: No duplicate rows
    if matching['source1_entity_id'].duplicated().any():
        errors.append("DUPLICATE source1_entity_id rows")
    
    # Check 3: All matched IDs are valid S2/S3 IDs
    for _, row in matching.iterrows():
        if not row['matched_entity_ids']:
            continue
        for mid in row['matched_entity_ids'].split(','):
            if mid not in test_s23_ids:
                errors.append(f"INVALID matched ID: {mid}")
    
    # Check 4: All matched IDs appear in candidates
    # ... (similar logic)
    
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return False
    print("PRE-SUBMISSION CHECK: PASS")
    return True
```

---

## 8. Logging Strategy

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(module)s: %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)
```

Log at key milestones:
- `INFO`: Stage start/end, record counts, blocking recall, F₀.₅ scores
- `WARNING`: Empty records, missing fields, recall below threshold
- `ERROR`: Validation failures, missing files
- `DEBUG`: Per-pair feature values (very verbose, off by default)
