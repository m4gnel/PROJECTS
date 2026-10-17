# Makefile for Amazon ML Challenge 2026 — Business Entity Resolution
# Run from project root directory: amazon_ml_challenge/

.PHONY: install test eda blocking train predict validate package clean help

PYTHON = python3
CONFIG = configs/config.yaml
MODEL = models/matcher.pkl
MATCHING = output/matching_results.tsv
CANDIDATE = output/candidate_pairs.tsv
TEST_DIR = dataset/test
TEAM_NAME = TeamName

help:
	@echo "Amazon ML Challenge 2026 — Entity Resolution Pipeline"
	@echo ""
	@echo "  make install    Install all Python dependencies"
	@echo "  make test       Run unit tests"
	@echo "  make eda        Run exploratory data analysis"
	@echo "  make blocking   Analyze blocking recall and reduction"
	@echo "  make train      Train model (saves to models/matcher.pkl)"
	@echo "  make predict    Run inference on test set"
	@echo "  make full       Train + predict (full pipeline)"
	@echo "  make validate   Validate output files against submission rules"
	@echo "  make package    Create submission zip"
	@echo "  make clean      Remove output files and logs"
	@echo ""

install:
	pip install -r code/business_entity_resolution/requirements.txt

test:
	cd code/business_entity_resolution && \
	$(PYTHON) -m pytest tests/ -v --tb=short 2>&1 | head -100

eda:
	$(PYTHON) notebooks/01_eda.py

blocking:
	$(PYTHON) notebooks/02_blocking_analysis.py

train:
	$(PYTHON) code/business_entity_resolution/src/run_pipeline.py \
		--mode train \
		--config $(CONFIG) \
		--model $(MODEL)

predict:
	$(PYTHON) code/business_entity_resolution/src/run_pipeline.py \
		--mode predict \
		--config $(CONFIG) \
		--model $(MODEL)

full:
	$(PYTHON) code/business_entity_resolution/src/run_pipeline.py \
		--mode full \
		--config $(CONFIG) \
		--model $(MODEL)

validate:
	$(PYTHON) code/business_entity_resolution/utils/validate_submission.py \
		--matching $(MATCHING) \
		--candidate $(CANDIDATE) \
		--test-dir $(TEST_DIR)

package:
	@echo "Creating submission package..."
	@mkdir -p $(TEAM_NAME)_submission/output
	@mkdir -p $(TEAM_NAME)_submission/code
	@cp output/matching_results.tsv $(TEAM_NAME)_submission/output/
	@cp output/candidate_pairs.tsv $(TEAM_NAME)_submission/output/
	@cp -r code/business_entity_resolution $(TEAM_NAME)_submission/code/
	@cp Documentation_template.md $(TEAM_NAME)_submission/
	@zip -r $(TEAM_NAME)_submission.zip $(TEAM_NAME)_submission/
	@rm -rf $(TEAM_NAME)_submission/
	@echo "Created: $(TEAM_NAME)_submission.zip"
	@ls -lh $(TEAM_NAME)_submission.zip

clean:
	rm -f output/matching_results.tsv output/candidate_pairs.tsv
	rm -f pipeline.log
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "Clean complete."

# Quick submission workflow
submit: full validate
	@echo ""
	@echo "✅ Pipeline complete and validated."
	@echo "Upload output/matching_results.tsv to the competition portal."
	@echo "Then run: make package"
