# 12_GITHUB_ACTIONS.md
# CI/CD & Automation

## 1. Recommended Workflow

Since this is a competition (not production), CI is lightweight:

```
Local dev → run tests → run pipeline → validate output → submit
```

## 2. Makefile (run from project root)

```makefile
.PHONY: install test eda train predict validate clean

install:
	pip install -r code/business_entity_resolution/requirements.txt

test:
	pytest code/business_entity_resolution/tests/ -v --tb=short

eda:
	jupyter nbconvert --to notebook --execute notebooks/01_eda.ipynb

train:
	python code/business_entity_resolution/src/run_pipeline.py \
		--mode train \
		--config configs/config.yaml

predict:
	python code/business_entity_resolution/src/run_pipeline.py \
		--mode predict \
		--config configs/config.yaml

validate:
	python code/business_entity_resolution/utils/validate_submission.py \
		--matching output/matching_results.tsv \
		--candidate output/candidate_pairs.tsv \
		--test-dir dataset/test

package:
	zip -r TeamName_submission.zip \
		output/ \
		code/business_entity_resolution/ \
		Documentation_template.md

clean:
	rm -f output/matching_results.tsv output/candidate_pairs.tsv
	rm -f pipeline.log
	find . -type d -name __pycache__ -exec rm -rf {} +
```

## 3. Git Workflow

```
main         ← stable, submission-ready only
  └── dev    ← active development
        ├── feature/blocking-improvements
        ├── feature/hard-negative-mining
        └── experiment/bge-m3-embeddings
```

## 4. Pre-commit Hooks (.pre-commit-config.yaml)

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
        language_version: python3.10

  - repo: https://github.com/PyCQA/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=100]
```

## 5. Experiment Tracking (Manual)

Since external services are prohibited during inference, use local logging:

```python
# configs/experiments.json — manually maintained
{
  "experiments": [
    {
      "id": "exp_001",
      "date": "2026-09-25",
      "description": "Baseline: TF-IDF blocking + LightGBM",
      "val_f05": 0.871,
      "public_lb_f05": null,
      "threshold": 0.52,
      "blocking_recall": 0.983,
      "notes": "Strong baseline. Hard negatives missing."
    },
    {
      "id": "exp_002",
      "date": "2026-09-26",
      "description": "Add multilingual embeddings + hard negatives",
      "val_f05": 0.913,
      "public_lb_f05": 0.907,
      "threshold": 0.48,
      "blocking_recall": 0.991,
      "notes": "Major improvement. France recall unknown (no train data)."
    }
  ]
}
```
