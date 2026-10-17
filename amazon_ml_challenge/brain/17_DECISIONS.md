# 17_DECISIONS.md
# Architecture Decision Records (ADRs)

---

## ADR-001: LightGBM over Neural Pairwise Classifier

**Date**: 2026-09-25  
**Status**: ACCEPTED

**Context**: We need a matching classifier. Options: LightGBM on hand-crafted features, or a neural cross-encoder fine-tuned end-to-end.

**Decision**: Use LightGBM as primary classifier, optionally augmented with cross-encoder scores as a feature.

**Reasoning**:
- LightGBM trains in seconds; cross-encoder fine-tuning requires hours + GPU
- Feature importance is interpretable → easier to debug
- LightGBM handles tabular features better than raw cross-encoder for structured similarity data
- Cross-encoder as a FEATURE (not classifier) gives best of both worlds

**Consequences**:
- Feature engineering is critical path
- Must mine hard negatives for LightGBM to discriminate well

---

## ADR-002: F₀.₅ Threshold Optimization over F₁

**Date**: 2026-09-25  
**Status**: ACCEPTED

**Context**: The metric is F₀.₅, which weights precision 2× over recall. A naive threshold of 0.5 is not optimal.

**Decision**: Grid-search threshold from 0.1 to 0.95 in steps of 0.01, maximizing F₀.₅ on validation set.

**Reasoning**:
- Optimizing F₁ threshold gives wrong answer for F₀.₅
- The optimal F₀.₅ threshold is typically HIGHER than F₁ threshold (more conservative, fewer matches)
- Singletons: predict empty is always safe → threshold should be set conservatively

---

## ADR-003: Multilingual Embedding Model

**Date**: 2026-09-25  
**Status**: ACCEPTED

**Context**: Data includes US English, Indian English + Hindi transliterations, and unseen French. A monolingual English model will fail on French test data.

**Decision**: Use `paraphrase-multilingual-mpnet-base-v2` (Apache 2.0, 278M params).

**Reasoning**:
- Supports 50+ languages including French, Hindi
- Under 8B param limit
- Apache 2.0 license ✅
- Benchmark: strong performance on cross-lingual STS tasks
- Alternative `BAAI/bge-m3` is slightly better but 570M params and may be slower

---

## ADR-004: Hard Negative Mining Strategy

**Date**: 2026-09-25  
**Status**: ACCEPTED

**Context**: Without hard negatives, the model sees easy negatives (random pairs) and can't distinguish truly ambiguous cases like "McDonald's Corp" vs "McDonald's Corporation" (same) vs "McDonald's Bakery" (different).

**Decision**: For each S1 entity, mine top-10 blocking candidates that are NOT in GT as hard negatives. Ratio: 1 positive : 5 hard negatives.

**Reasoning**:
- Hard negatives force the model to learn fine-grained discrimination
- 1:5 ratio avoids overwhelming the model with negatives (empirical best practice in ER literature)
- Supplement with random negatives (1:2) for diversity

---

## ADR-005: Country as Open String, Not One-Hot

**Date**: 2026-09-25  
**Status**: ACCEPTED

**Context**: Problem statement explicitly says: "Treat country as an open set of string labels: do not hard-code, filter, or one-hot your pipeline to only {US, India}."

**Decision**: Use country only as a binary feature: `country_match = 1 if s1.country == s2.country else 0`. Never one-hot encode.

**Reasoning**:
- France appears in test set but not training → one-hot would add unknown category
- Binary match signal is sufficient and generalizes to any country

---

## ADR-006: Union of Blocking Keys (Not Intersection)

**Date**: 2026-09-25  
**Status**: ACCEPTED

**Context**: Multiple blocking keys each have different recall. Should we use union or intersection?

**Decision**: UNION. A pair is a candidate if ANY blocking key triggers it.

**Reasoning**:
- Union maximizes recall (upper bound of final F₀.₅)
- Reduction ratio is maintained by the matching classifier (precision stage)
- Intersection would miss pairs where only one BK fires (common for noisy data)
- The matching model exists precisely to filter false positives from the union

---

## ADR-007: No External Data — Strict Compliance

**Date**: 2026-09-25  
**Status**: ACCEPTED

**Context**: Competition prohibits any external data lookup.

**Decision**: All address normalization and name normalization is done using ONLY:
1. The abbreviation dictionary in `configs/abbreviations.json` (hand-crafted, not scraped)
2. Standard Python string operations
3. The training data itself (for TF-IDF vocabulary)

**No geocoding. No business registry lookup. No Wikipedia. No Google Maps API.**

Non-compliance = disqualification.
