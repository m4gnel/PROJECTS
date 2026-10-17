# 16_CHANGELOG.md
# Changelog

## [Unreleased]

### Added
- Initial project structure
- Brain document suite (00–17)
- Complete pipeline architecture

---

## How to Use This File

Add an entry every time you:
- Submit to the leaderboard
- Make a significant code change
- Change hyperparameters
- Change blocking strategy
- Change model architecture

Format:
```
## [EXP-XXX] YYYY-MM-DD — Short Description

### Changed
- What changed

### Score
- Val F₀.₅: X.XXX
- Public LB F₀.₅: X.XXX (or "not submitted yet")

### Notes
- Any observations
```

---

## [EXP-001] 2026-09-25 — Initial Baseline

### Added
- TF-IDF blocking (BK-1, BK-2)
- Levenshtein + Token-set features
- LightGBM baseline

### Score
- Val F₀.₅: TBD
- Public LB F₀.₅: TBD

### Notes
- First run. Measure blocking recall first.
