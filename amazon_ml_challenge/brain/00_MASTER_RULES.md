# 00_MASTER_RULES.md
# Amazon ML Challenge 2026 — Master Rules & Non-Negotiables

## Competition Snapshot
| Field | Value |
|---|---|
| Challenge | Amazon ML Challenge 2026 |
| Problem | Business Entity Resolution (ER) |
| Task | Match S2/S3 records → S1 reference entities |
| Metric | **F₀.₅ (precision-weighted macro-average)** |
| Model License | MIT or Apache 2.0 only |
| Model Max Size | ≤ 8 Billion parameters |
| External Data | **STRICTLY PROHIBITED** |
| Output Files | `matching_results.tsv`, `candidate_pairs.tsv` |

---

## Golden Rules (never violate)

1. **Every S1 entity must appear exactly once** in both output files — including singletons.
2. **matched_entity_ids must only reference S2 or S3 IDs** that exist in the test set.
3. **No duplicate IDs** inside any comma-separated list.
4. **No external APIs / databases** — no geocoding, no business lookup, no internet at inference time.
5. **Every matched ID must first appear in candidate_pairs.tsv** (matched ⊆ candidates).
6. **Model ≤ 8B params, MIT/Apache 2.0** — verify license before using any HuggingFace model.
7. **Run `validate_submission.py` before every submission upload**.
8. **Optimize for Precision first** — F₀.₅ weights precision 2× over recall. One bad false positive costs more than one missed match.
9. **Singletons earn 1.0** if correctly predicted empty. Don't over-match.
10. **France (unseen country)** will appear in test set. Pipeline must be country-agnostic.

---

## F₀.₅ Formula (memorize)
```
F₀.₅ = (1.25 × P × R) / (0.25 × P + R)
```
- Macro-averaged per S1 entity.
- Singleton with no GT matches: predict empty → score 1.0; predict anything → score 0.0.
- **Implication: When in doubt, DON'T match.**

---

## Noise Patterns to Handle
| Type | Examples |
|---|---|
| Name abbrev | Corp/Corporation, Pvt/Private, Ltd/Limited, &/and |
| Name typos | Levenshtein distance 1-2, transpositions |
| Name DBA | Trade name vs legal name |
| Address abbrev | Rd/Road, St/Street, Ave/Avenue, Blvd/Boulevard |
| Address missing | No ZIP, no state, partial street |
| Address landmark | "Near SBI ATM", "Opp. Big Bazaar" |
| Transliteration | Hindi place names in multiple romanizations |
| Country-specific | US ZIP vs India PIN vs France postal codes |

---

## File Format Rules
- All files: **tab-separated** (.tsv)
- ID lists: **comma-separated, no spaces, no quotes**
- Empty match: leave `matched_entity_ids` column blank (not "None", not "[]")
- Column headers: exactly `source1_entity_id` and `matched_entity_ids`

---

## Decision Log Path
All strategic decisions → `17_DECISIONS.md`
All architecture changes → `03_ARCHITECTURE.md`
