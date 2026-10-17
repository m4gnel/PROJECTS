# ✅ Pre-Start Checklist
## Complete Everything Here BEFORE Pasting Any Prompt Into Gemini

---

## 1. API Keys — Register These First

| Service | Where | Time | Key Name in .env |
|---|---|---|---|
| Gemini Flash | [aistudio.google.com](https://aistudio.google.com) | Instant | `GEMINI_API_KEY` |
| data.gov.in APMC | [data.gov.in](https://data.gov.in) → Register | 1–2 days | `DATA_GOV_IN_KEY` |
| NASA EarthData | [earthdata.nasa.gov](https://earthdata.nasa.gov) | Instant | `NASA_EARTHDATA_TOKEN` |
| Open-Meteo | No registration needed | — | No key required |
| NBAIR RSS | No registration needed | — | No key required |
| Railway | [railway.app](https://railway.app) → GitHub login | Instant | `RAILWAY_TOKEN` (from dashboard) |

> ⚠️ data.gov.in takes 1–2 days to activate. Register this first, before anything else.

---

## 2. Local Environment

```bash
# Check Python version (must be 3.11+)
python --version

# Check Node.js (for Android build tools)
node --version     # must be 18+

# Check Git
git --version

# Check Docker (for Dockerfile build in Phase 5)
docker --version
```

---

## 3. .env File Setup

```bash
# In your agrisage-backend/ directory
cp .env.example .env
```

Edit `.env` and fill in all values:

```env
# LLM
GEMINI_API_KEY=your_key_here

# Market data
DATA_GOV_IN_KEY=your_key_here

# Satellite NDVI
NASA_EARTHDATA_TOKEN=your_token_here

# Database (Railway provides this — use local for dev)
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/agrisage

# App settings
ENVIRONMENT=development
SECRET_KEY=generate_with_python_secrets_token_hex_32
ALLOWED_ORIGINS=*
```

Generate SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 4. Git Repository Setup

```bash
# In your project root
git init
git remote add origin https://github.com/YOUR_USERNAME/agrisage.git

# Create all team branches
git checkout -b dev/m1-backend && git push -u origin dev/m1-backend
git checkout main

git checkout -b dev/m2-android && git push -u origin dev/m2-android
git checkout main

git checkout -b dev/m3-rag && git push -u origin dev/m3-rag
git checkout main

git checkout -b dev/m4-agents && git push -u origin dev/m4-agents
git checkout main

git checkout -b dev/m5-tests && git push -u origin dev/m5-tests
git checkout main

# Verify all branches exist
git branch -a
```

Expected output:
```
* main
  dev/m1-backend
  dev/m2-android
  dev/m3-rag
  dev/m4-agents
  dev/m5-tests
  remotes/origin/main
  remotes/origin/dev/m1-backend
  ... (all 5 remote branches)
```

---

## 5. .gitignore — Verify These Are Present

Your `.gitignore` must include:

```gitignore
# Secrets — NEVER commit these
.env
*.env

# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
.venv/
venv/
dist/
build/

# macOS
.DS_Store

# IDE
.idea/
.vscode/
*.iml

# Android
android/local.properties
android/.gradle/
android/app/build/
android/build/

# Models (large files)
*.bin
*.pt
sentence_transformers_cache/
```

---

## 6. GitHub Secrets Setup

Go to **GitHub → Repo → Settings → Secrets and variables → Actions → New repository secret**

Add these 4 secrets before Phase 5:

| Secret Name | Where to Get It |
|---|---|
| `GEMINI_API_KEY` | aistudio.google.com |
| `DATA_GOV_IN_KEY` | data.gov.in |
| `RAILWAY_TOKEN` | railway.app → Account → Tokens → New Token |
| `RAILWAY_API_URL` | Your Railway deployment URL (after Phase 5 deploy) |

---

## 7. GitHub Labels Setup

Go to **GitHub → Repo → Issues → Labels → New label**

Create these labels (see `07-github-issues-guide.md` for colors):

```
phase-1    phase-2    phase-3    phase-4    phase-5
backend    agents     rag        android    devops
protected  needs-review
```

---

## 8. PostgreSQL + pgvector Local Setup

```bash
# Install PostgreSQL 16 + pgvector extension
# Option A: Docker (easiest)
docker run -d \
  --name agrisage-db \
  -e POSTGRES_DB=agrisage \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  pgvector/pgvector:pg16

# Option B: Local PostgreSQL
# After installing PostgreSQL 16:
psql -U postgres -c "CREATE DATABASE agrisage;"
psql -U postgres -d agrisage -c "CREATE EXTENSION vector;"

# Verify pgvector works
psql -U postgres -d agrisage -c "SELECT vector('[1,2,3]');"
# Should return: (1,2,3)
```

---

## 9. KAU PDF Documents

Download KAU Package of Practices PDFs before Phase 3:

- URL: [kau.in/package-of-practices](https://www.kau.in/package-of-practices)
- Download PDFs for: coconut, rice, banana, rubber, tapioca, pepper, cardamom
- Save to: `agrisage-backend/kau_docs/`
- Name them: `kau_coconut_pop.pdf`, `kau_rice_pop.pdf`, etc.

> These are free, publicly available PDFs from Kerala Agricultural University.

---

## 10. Android Prerequisites

```bash
# Verify Java 17 (required for Gradle)
java -version   # must be 17.x

# Verify Android SDK is installed
# (via Android Studio or command line tools)

# Create local.properties in android/ directory
echo "API_BASE_URL=http://10.0.2.2:8000/" > android/local.properties
# Note: 10.0.2.2 is localhost from Android emulator
```

---

## Final Verification

Run this before pasting the first prompt:

```bash
# Python
python --version        # 3.11+
pip show fastapi        # should show 0.115.0 (after Phase 1)

# Git
git status              # clean working tree
git branch              # main is current

# Database
curl -f http://localhost:5432 2>/dev/null || echo "DB check needs psql"
psql $DATABASE_URL -c "SELECT version();" 2>/dev/null | head -2

# .env
cat .env | grep -v "=" | wc -l   # should be 0 (all keys filled)
```

---

## You're Ready When

- [ ] All 4 API keys registered and in `.env`
- [ ] All 5 Git branches created and pushed
- [ ] `.gitignore` verified
- [ ] GitHub labels created
- [ ] PostgreSQL + pgvector running
- [ ] KAU PDFs downloaded to `kau_docs/`
- [ ] Java 17 verified for Android
- [ ] GitHub secrets will be added before Phase 5

---

> **Now paste `00-master-runner.md` into Gemini 2.5 Pro and start building. 🌾**
