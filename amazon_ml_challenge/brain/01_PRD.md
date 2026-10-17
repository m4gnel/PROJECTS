# 01_PRD.md
# Product Requirements Document — Business Entity Resolution System

## 1. Problem Definition

Given business records from **3 independent data sources** with noisy, inconsistent fields,
determine which records across sources refer to the **same real-world business entity**.

- **Source 1**: Deduplicated reference (anchor). Every S1 entity gets one output row.
- **Source 2 & 3**: Noisy sources. Find which S2/S3 records match each S1 entity.
- **Match cardinality**: A S1 entity may match 0, 1, or many S2/S3 records.

---

## 2. Inputs & Outputs

### Inputs
| File | Description |
|---|---|
| `train_source1.tsv` | S1 training records (entity_id, business_name, business_address, country) |
| `train_source2.tsv` | S2 training records |
| `train_source3.tsv` | S3 training records |
| `train_ground_truth.tsv` | GT: source1_entity_id → matched_entity_ids (comma-separated) |
| `test_source1.tsv` | S1 test records (generate predictions for ALL of these) |
| `test_source2.tsv` | S2 test records |
| `test_source3.tsv` | S3 test records |

### Outputs
| File | Description |
|---|---|
| `output/matching_results.tsv` | Final predictions — scored on leaderboard |
| `output/candidate_pairs.tsv` | Blocking candidates — pipeline audit |

---

## 3. Success Metrics

| Metric | Target |
|---|---|
| F₀.₅ on validation split | > 0.90 |
| F₀.₅ on public leaderboard | > 0.92 |
| Blocking recall (candidates) | > 0.98 (don't miss GT pairs at blocking) |
| Blocking reduction ratio | > 95% (prune candidate space aggressively) |
| Runtime (full test inference) | < 30 minutes on single GPU or CPU |

---

## 4. User Stories

### US-01: Pipeline Reproducibility
As a judge reviewing our submission, I can run `python src/run_pipeline.py` end-to-end
and regenerate identical output files from raw TSV data.

### US-02: Validation Gating
As a developer, before I upload any submission, I run `validate_submission.py` and see
`PASS` with zero issues.

### US-03: Country Generalization
As the system, when I encounter France records in the test set (never seen in training),
I apply the same text normalization and similarity pipeline without hard-coded country logic.

### US-04: Singleton Handling
As the system, when a S1 entity has no plausible candidates after blocking, I output an empty
`matched_entity_ids` field, earning a full 1.0 for that entity.

### US-05: Precision Guard
As the matching model, I only emit a match when the similarity score exceeds a calibrated
threshold. I do NOT default to matching everything. I would rather miss a match than create
a false merge.

---

## 5. Non-Functional Requirements

| NFR | Requirement |
|---|---|
| NFR-01 Licensing | All models: MIT or Apache 2.0 only |
| NFR-02 Size | Embedding model ≤ 8B params |
| NFR-03 No External Data | Zero API calls at inference time |
| NFR-04 Determinism | Same seed → same output on rerun |
| NFR-05 Portability | Runs on Python 3.10+, Linux/Mac |
| NFR-06 Dependencies | All in `requirements.txt` with pinned versions |

---

## 6. Out of Scope

- Building a UI or API endpoint
- Real-time streaming inference
- Multi-GPU distributed training (single-GPU or CPU only)
- Using closed-source models (GPT-4, Claude, Gemini) — even for feature generation
