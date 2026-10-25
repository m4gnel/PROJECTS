SHELL := /bin/sh

PYTHON ?= python3
PYTHON_VERSION ?= 3.11.9
FRONTEND_DIR ?= apps/web-expert
ROOT_DIR := $(CURDIR)
COMPOSE ?= docker compose
NODE_VERSION ?= 20.19.0
SMOKE_BASE_URL ?= http://localhost:8000

.PHONY: preflight test compose-config prod-config smoke

preflight:
	@set -eu; \
	for required in \
		Dockerfile \
		docker-compose.yml \
		docker-compose.prod.yml \
		.env.example \
		.nvmrc \
		.python-version \
		requirements.txt \
		requirements.lock \
		requirements-dev.lock \
		package-lock.json \
		$(FRONTEND_DIR)/package-lock.json \
		$(FRONTEND_DIR)/.env.example \
		.github/workflows/ci.yml \
		.github/workflows/backend-ci.yml \
		.github/workflows/android-ci.yml \
		.github/workflows/deploy.yml \
		.github/workflows/deploy-railway.yml \
		scripts/smoke_tests.py; do \
		if [ ! -f "$$required" ]; then \
			echo "ERROR: required release file is missing: $$required" >&2; \
			exit 1; \
		fi; \
	done; \
	if [ -f backend/Dockerfile ]; then \
		echo "ERROR: retired backend/Dockerfile must not be deployed; use the root Dockerfile" >&2; \
		exit 1; \
	fi; \
	if ! command -v "$(PYTHON)" >/dev/null 2>&1; then \
		echo "ERROR: $(PYTHON) is required; install the pinned Python runtime before running release checks" >&2; \
		exit 1; \
	fi; \
	"$(PYTHON)" -c 'from pathlib import Path; import platform; import sys; expected_selector = Path(".python-version").read_text(encoding="utf-8").strip(); expected = "$(PYTHON_VERSION)"; actual = platform.python_version(); sys.exit(f"Python {actual} does not match pinned Python $(PYTHON_VERSION) or .python-version ({expected_selector})") if actual != expected or actual != expected_selector else None'; \
	echo "Preflight checks passed (Python $$("$(PYTHON)" -c 'import platform; print(platform.python_version())'))"

compose-config: preflight
	@set -eu; \
	if [ ! -f .env ]; then \
		echo "ERROR: .env is missing; copy .env.example to .env before validating Compose" >&2; \
		exit 1; \
	fi; \
	$(COMPOSE) config --quiet

prod-config: preflight
	@set -eu; \
	if [ ! -f .env ]; then \
		echo "ERROR: .env is missing; provide production settings through the secret manager or .env" >&2; \
		exit 1; \
	fi; \
	$(COMPOSE) -f docker-compose.prod.yml config --quiet

smoke: preflight
	@"$(PYTHON)" scripts/smoke_tests.py --base-url "$(SMOKE_BASE_URL)"

test: preflight
	@set -eu; \
	root_dir="$(ROOT_DIR)"; \
	frontend_dir="$$root_dir/$(FRONTEND_DIR)"; \
	if ! "$(PYTHON)" -c 'import pytest' >/dev/null 2>&1; then \
		echo "ERROR: pytest is unavailable; install requirements-dev.lock before running make test" >&2; \
		exit 1; \
	fi; \
	if ! command -v node >/dev/null 2>&1; then \
		echo "ERROR: node is unavailable; install the pinned Node.js runtime before running make test" >&2; \
		exit 1; \
	fi; \
	node_version=$$(node --version); \
	node_version=$${node_version#v}; \
	if [ "$$node_version" != "$(NODE_VERSION)" ]; then \
		echo "ERROR: Node.js $$node_version is installed; make test requires $(NODE_VERSION)" >&2; \
		exit 1; \
	fi; \
	for tool in tsc vite oxlint; do \
		if [ ! -x "$$frontend_dir/node_modules/.bin/$$tool" ]; then \
			echo "ERROR: frontend tool $$tool is unavailable; run npm ci in $$frontend_dir" >&2; \
			exit 1; \
		fi; \
	done; \
	echo "==> Python syntax"; \
	"$(PYTHON)" -m compileall -q backend tests scripts alembic; \
	echo "==> Python tests"; \
	"$(PYTHON)" -m pytest tests/ -v --tb=short --asyncio-mode=auto; \
	"$(PYTHON)" -m pytest backend/tests/ -v --tb=short --asyncio-mode=auto; \
	echo "==> Frontend typecheck"; \
	( cd "$$frontend_dir" && "$$frontend_dir/node_modules/.bin/tsc" --build ); \
	build_dir=$$(mktemp -d "$${TMPDIR:-/tmp}/agrisage-frontend.XXXXXX"); \
	trap 'status=$$?; rm -rf "$$build_dir"; exit $$status' EXIT; \
	echo "==> Frontend build"; \
	( cd "$$frontend_dir" && "$$frontend_dir/node_modules/.bin/vite" build --outDir "$$build_dir" --emptyOutDir ); \
	echo "==> Frontend lint"; \
	( cd "$$frontend_dir" && "$$frontend_dir/node_modules/.bin/oxlint" )
