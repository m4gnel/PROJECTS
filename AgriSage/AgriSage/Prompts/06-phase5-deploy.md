# 🚀 PHASE 5 — Deploy + CI/CD + Monitoring
## Branch: `main` (via PR) · Owner: M1 + M5 · GitHub Issue: #5

---

## Paste This Into Gemini 2.5 Pro

```
=== AGRI-SAGE PHASE 5 — RAILWAY DEPLOY + GITHUB ACTIONS + MONITORING ===

Run AUDIT-FIRST PROTOCOL on Dockerfile, .github/, railway.toml before writing.
Print audit table. Build only MISSING and NEEDS_WORK files.

TARGET FILE STRUCTURE:
├── Dockerfile
├── railway.toml
├── .github/
│   └── workflows/
│       ├── backend-ci.yml
│       └── android-ci.yml
├── app/
│   └── main.py              ← Verify /health endpoint exists
└── grafana/
    └── README.md            ← Setup guide for Grafana Cloud

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DOCKERFILE — MULTI-STAGE PRODUCTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl postgresql-client && rm -rf /var/lib/apt/lists/*
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", \
     "--port", "8000", "--workers", "2", "--log-level", "info"]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RAILWAY.TOML
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[build]
  builder = "dockerfile"
  dockerfilePath = "Dockerfile"

[deploy]
  startCommand = "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2"
  healthcheckPath = "/health"
  healthcheckTimeout = 30
  restartPolicyType = "on_failure"
  restartPolicyMaxRetries = 3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HEALTH CHECK — VERIFY IN app/main.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If /health endpoint is missing from app/main.py, ADD it (do not rewrite the file):

@app.get("/health", tags=["system"])
async def health_check():
    return {
        "status": "healthy",
        "service": "agrisage-backend",
        "version": "1.0.0"
    }

Also add Prometheus middleware if missing (append to app/main.py startup):
  from prometheus_fastapi_instrumentator import Instrumentator
  Instrumentator().instrument(app).expose(app, endpoint="/metrics")

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BACKEND CI (.github/workflows/backend-ci.yml)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

name: Agri-SAGE Backend CI/CD
on:
  push:
    branches:
      - dev/m1-backend
      - dev/m4-agents
      - dev/m3-rag
      - main
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_DB: agrisage_test
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Lint with ruff
        run: ruff check app/ --select E,F,W --ignore E501

      - name: Run tests
        run: pytest tests/ -v --tb=short --cov=app --cov-report=term-missing
        env:
          DATABASE_URL: postgresql+asyncpg://test:test@localhost:5432/agrisage_test
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          DATA_GOV_IN_KEY: ${{ secrets.DATA_GOV_IN_KEY }}
          ENVIRONMENT: test

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Railway CLI
        run: npm install -g @railway/cli

      - name: Deploy to Railway
        run: railway up --detach
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ANDROID CI (.github/workflows/android-ci.yml)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

name: Agri-SAGE Android CI
on:
  push:
    branches:
      - dev/m2-android
      - main
  pull_request:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "17"

      - uses: gradle/actions/setup-gradle@v4

      - name: Create local.properties
        run: |
          echo "API_BASE_URL=${{ secrets.RAILWAY_API_URL }}" \
            >> android/local.properties

      - name: Build debug APK
        run: |
          cd android
          ./gradlew assembleDebug --no-daemon
        env:
          GRADLE_OPTS: "-Dorg.gradle.daemon=false -Xmx2g"

      - name: Upload APK artifact
        uses: actions/upload-artifact@v4
        with:
          name: agrisage-debug-${{ github.sha }}
          path: android/app/build/outputs/apk/debug/app-debug.apk
          retention-days: 30

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RAILWAY ENVIRONMENT VARIABLES
(Set these in Railway dashboard — never in code)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DATABASE_URL         ← Railway auto-provides this for PostgreSQL plugin
GEMINI_API_KEY       ← From aistudio.google.com
DATA_GOV_IN_KEY      ← From data.gov.in registration
NASA_EARTHDATA_TOKEN ← From earthdata.nasa.gov
ENVIRONMENT          ← production
SECRET_KEY           ← python -c "import secrets; print(secrets.token_hex(32))"
ALLOWED_ORIGINS      ← * for demo, tighten to app domain in production

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GITHUB SECRETS TO ADD
(Settings → Secrets → Actions → New repository secret)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GEMINI_API_KEY       ← your Gemini Flash key
DATA_GOV_IN_KEY      ← your data.gov.in key
RAILWAY_TOKEN        ← from Railway dashboard → Account → Tokens
RAILWAY_API_URL      ← your Railway deployment URL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GRAFANA MONITORING (grafana/README.md)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Create grafana/README.md with these setup steps:
  1. Create free account at grafana.com (50 GB free)
  2. Add data source: Prometheus
     URL: https://your-railway-url.railway.app/metrics
  3. Import dashboard — 5 panels to create:
     Panel 1: API Response Time P95 (target < 3000ms)
       Query: histogram_quantile(0.95, http_request_duration_seconds_bucket)
     Panel 2: Gemini Calls Per Minute (alert > 13 = near 15 RPM limit)
       Query: rate(agrisage_gemini_calls_total[1m]) * 60
     Panel 3: Agent Error Rate (alert > 2%)
       Query: rate(agrisage_agent_errors_total[5m]) / rate(agrisage_agent_calls_total[5m])
     Panel 4: Weather Cache Hit Rate (target > 70%)
       Query: rate(agrisage_cache_hits_total[5m]) / rate(agrisage_cache_requests_total[5m])
     Panel 5: Active Farmers Today
       Query: agrisage_active_farmers_today

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CUSTOM PROMETHEUS METRICS (add to app/main.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If these counters are missing from app/main.py, ADD them:

from prometheus_client import Counter, Gauge

gemini_calls = Counter(
    "agrisage_gemini_calls_total",
    "Total Gemini Flash API calls",
    ["agent_name"]
)
agent_errors = Counter(
    "agrisage_agent_errors_total",
    "Total agent errors",
    ["agent_name", "error_type"]
)
agent_calls = Counter(
    "agrisage_agent_calls_total",
    "Total agent invocations",
    ["agent_name"]
)
cache_hits = Counter(
    "agrisage_cache_hits_total",
    "Weather/market cache hits"
)
cache_requests = Counter(
    "agrisage_cache_requests_total",
    "Total cache lookups"
)
active_farmers = Gauge(
    "agrisage_active_farmers_today",
    "Unique farmers who queried today"
)

Increment these in the appropriate services and agents.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GITHUB ISSUE PROTOCOL — PHASE 5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After health check passes:
  docker build -t agrisage-backend:test .
  docker run --rm -p 8000:8000 --env-file .env agrisage-backend:test &
  sleep 8
  curl -f http://localhost:8000/health
  Expected: {"status":"healthy","service":"agrisage-backend","version":"1.0.0"}

  git checkout main
  git add -A
  git commit -m "feat(phase-5): Railway deploy, GitHub Actions CI/CD, Prometheus + Grafana monitoring"
  git tag v1.0.0

Create GitHub Issue:
  Title: [Phase 5] Deploy + CI/CD + Monitoring
  Labels: phase-5, devops
  Assign: @M1 @M5
  Body:
    ## Deployment checklist
    - [ ] Railway environment variables set
    - [ ] GitHub secrets added (GEMINI_API_KEY, DATA_GOV_IN_KEY, RAILWAY_TOKEN, RAILWAY_API_URL)
    - [ ] /health endpoint verified
    - [ ] Backend CI workflow passes
    - [ ] Android CI builds APK
    - [ ] Grafana dashboard live

    ## Railway deployment URL
    https://<your-url>.railway.app

    ## APK download
    GitHub Actions → android-ci → Artifacts → agrisage-debug-<sha>

Print: "✅ Phase 5 complete. v1.0.0 tagged. Agri-SAGE is LIVE. Issue #5 created."
```

---

## Railway Free Tier — Design Within These Limits

| Resource | Free Limit | Agri-SAGE Usage |
|---|---|---|
| Compute | 500 hrs/month | ~21 days continuous |
| PostgreSQL | 1 GB storage | Sufficient for KAU + farm data |
| Egress | $5 credit/month | Route bulk fetches to cron |
| GitHub Actions | 2,000 min/month | Backend CI ~3min, Android ~6min |
| Grafana Cloud | 50 GB logs free | All FastAPI logs |

## GitHub Issue Created After This Phase

```
Title: [Phase 5] Deploy + CI/CD + Monitoring
Branch: main
Labels: phase-5, devops
Assign to: M1, M5
```

---

> **All 5 phases complete. Agri-SAGE v1.0.0 is live. 🌾**
