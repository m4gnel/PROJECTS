# AGRI-SAGE — GITHUB ACTIONS & DEVOPS

## Repository Structure
```
agrisage/                    ← Private GitHub repo
├── brain/                   ← AI agent context files (this folder)
├── .github/workflows/
│   ├── ci.yml              ← Runs on every PR
│   └── security.yml        ← Security checks
```

## Branch Strategy
```
main          ← Protected. Never commit directly. Only merge from branches.
dev/m1-backend
dev/m2-agents
dev/m3-android
dev/m4-data
dev/m5-tests
```

## .github/workflows/ci.yml
```yaml
name: CI Pipeline
on:
  push:
    branches: [main, dev/*]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      db:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_DB: agrisage_test
          POSTGRES_USER: agrisage
          POSTGRES_PASSWORD: testpassword
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r backend/requirements.txt
      - name: Run migrations
        env:
          DATABASE_URL: postgresql+asyncpg://agrisage:testpassword@localhost/agrisage_test
          SECRET_KEY: test-secret-key-for-ci-only
          ENVIRONMENT: test
        run: alembic upgrade head
      - name: Run tests
        env:
          DATABASE_URL: postgresql+asyncpg://agrisage:testpassword@localhost/agrisage_test
          SECRET_KEY: test-secret-key-for-ci-only
          ENVIRONMENT: test
        run: pytest tests/ -v --tb=short --asyncio-mode=auto

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install black ruff
      - run: black --check backend/
      - run: ruff check backend/

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Check hardcoded secrets
        run: |
          if grep -rn --include="*.py" --include="*.kt" \
             -E '(SECRET_KEY|API_KEY|PASSWORD)\s*=\s*"[a-zA-Z0-9+/]{20,}"' .; then
            echo "FAIL: Hardcoded secret found"
            exit 1
          fi
      - name: Verify .env not committed
        run: |
          if git ls-files --error-unmatch .env 2>/dev/null; then
            echo "FAIL: .env is tracked by git"
            exit 1
          fi
      - name: Dependency vulnerability scan
        run: |
          pip install pip-audit
          pip-audit -r backend/requirements.txt --fail-on CRITICAL
      - name: SAST scan
        run: |
          pip install bandit
          bandit -r backend/ -lll
```

## Production Deployment (Oracle Always-Free)

### One-time Server Setup
```bash
# On Oracle instance (Ubuntu 22.04)
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-v2 nginx certbot
sudo usermod -aG docker ubuntu
# Install Ollama (free local LLM)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen3:7b-q4_K_M   # 4-bit quantized — fits 6GB RAM
ollama pull qwen3:1.7b
```

### scripts/deploy.sh
```bash
#!/bin/bash
set -e
cd /home/ubuntu/agrisage
git pull origin main
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d --no-deps backend
sleep 5
alembic upgrade head
python scripts/smoke_tests.py
echo "Deploy complete"
```

### docker-compose.prod.yml
```yaml
version: '3.9'
services:
  db:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: agrisage_prod
      POSTGRES_USER: agrisage
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  backend:
    build: .
    command: uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 2
    env_file: .env
    depends_on:
      db:
        condition: service_healthy
    restart: always
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

volumes:
  postgres_data:
```

## Free Infrastructure Checklist
- [ ] Oracle Cloud Always-Free account created
- [ ] 2 AMD instances provisioned (use 1 for backend+DB, 1 spare)
- [ ] Cloudflare R2 bucket created (free 10GB)
- [ ] Cloudflare DNS pointing to Oracle IP
- [ ] Let's Encrypt SSL via Cloudflare
- [ ] Firebase project created (FCM free)
- [ ] Grafana Cloud free tier monitoring set up
- [ ] Sentry free tier error tracking
