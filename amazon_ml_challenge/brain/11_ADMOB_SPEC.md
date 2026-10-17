# 11_ADMOB_SPEC.md
# Experiment Tracking & Iteration Strategy
# (Repurposed from template — no ads/monetization in this project)

## Iteration Roadmap

### Tier 1 — Baseline (Day 1, must complete)
| Experiment | Expected Val F₀.₅ | Risk |
|---|---|---|
| EXP-001: TF-IDF blocking + LightGBM on string features only | ~0.82 | Low |
| EXP-002: Add multilingual embeddings as feature | ~0.88 | Low |
| EXP-003: Add hard negatives (5:1 ratio) | ~0.91 | Low |

### Tier 2 — Improvements (Day 2)
| Experiment | Expected Val F₀.₅ | Risk |
|---|---|---|
| EXP-004: All 5 blocking keys (union) | +0.01–0.02 | Low |
| EXP-005: Cross-encoder as additional feature | +0.01–0.03 | Medium |
| EXP-006: Ensemble 3× LightGBM (different seeds) | +0.005–0.01 | Low |
| EXP-007: Threshold per country | +0.005 | Medium |

### Tier 3 — Advanced (if time allows)
| Experiment | Expected Val F₀.₅ | Risk |
|---|---|---|
| EXP-008: Fine-tuned cross-encoder on our data | +0.02–0.04 | High (time) |
| EXP-009: BGE-M3 instead of mpnet-base-v2 | +0.01–0.02 | Medium |
| EXP-010: Two-stage threshold (name-only vs full) | ±0.005 | High (complexity) |

---

## Experiments Log

```json
[
  {
    "id": "EXP-001",
    "date": "",
    "description": "Baseline: TF-IDF + LightGBM string features",
    "val_f05": null,
    "public_lb": null,
    "threshold": null,
    "blocking_recall": null,
    "notes": "First run"
  }
]
```

---

## Key Decision Points

### After EXP-001:
- Blocking recall ≥ 0.98? → Proceed to EXP-002
- Blocking recall < 0.95? → Must fix blocking before anything else

### After EXP-002:
- Val F₀.₅ ≥ 0.90? → Good baseline, go to Tier 2
- Val F₀.₅ 0.85–0.90? → Add hard negatives first (EXP-003)
- Val F₀.₅ < 0.85? → Debug features — check feature importance

### Before any submission:
- validate_submission.py → PASS (mandatory)
- Spot-check 20 random predictions manually

---

## Score Tracking Table

| EXP | Description | Val F₀.₅ | LB F₀.₅ | Threshold | Notes |
|---|---|---|---|---|---|
| 001 | TF-IDF + LGB | - | - | - | |
| 002 | +Embeddings | - | - | - | |
| 003 | +Hard negs | - | - | - | |
| 004 | +All BKs | - | - | - | |
| BEST | | | | | |

---

## Common Pitfalls to Avoid

1. **Optimizing F₁ threshold** → Use F₀.₅ threshold search explicitly
2. **Ignoring singletons** → They are 30–50% of S1; getting them right matters
3. **Over-blocking** → Millions of candidates → OOM. Cap per S1 entity.
4. **Training on val split** → Feature engineering uses GT; never touch val GT for training
5. **Not deduplicating candidates** → Validator rejects duplicate IDs in lists
6. **Missing S1 entities in output** → Validator rejects; every S1 must have a row
7. **Using France data assumptions** → It's not in training; your pipeline must generalize
