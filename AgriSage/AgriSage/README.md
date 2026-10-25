# Agri-SAGE (Scalable Agricultural Guidance Engine)

[![Architecture: Multi-Agent](https://img.shields.io/badge/Architecture-14--Agent%20LangGraph-2D7D2D.svg)](#)
[![Simulation: DSSAT](https://img.shields.io/badge/Simulation-DSSAT%20Physics--Grounded-1A5C1A.svg)](#)
[![Safety: CIB%26RC](https://img.shields.io/badge/Safety-CIB%26RC%20Label%20Verified-C62828.svg)](#)
[![Localization: Malayalam%20First](https://img.shields.io/badge/Language-Malayalam%20%7C%20English%20%7C%20Tamil%20%7C%20Telugu%20%7C%20Hindi-558B2F.svg)](#)
[![License: Open Source](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](#)

Agri-SAGE (*Scalable Agricultural Guidance Engine*) is a professional, offline-first, simulation-grounded, multi-agent agricultural decision intelligence platform engineered for smallholder farmers, Krishi Vigyan Kendra (KVK) extension officers, and institutional agronomists across India and global developing markets. The platform seamlessly unifies on-device vision diagnostics (EfficientNet-B3 ONNX), physics-based crop growth simulation (DSSAT CSM), statutory chemical safety verification (CIB&RC), local weather indicators, and 7-state calibrated confidence scoring into actionable, evidence-grounded advisories delivered natively in regional languages (Malayalam, English, Hindi, Tamil, Telugu).

---

## 👥 Team Member Roles & Responsibilities

| Team Member | Technical Focus & Core Responsibilities |
| :--- | :--- |
| **Member 1 (Team Lead)** | **Backend & Auth Infrastructure Lead**: FastAPI core setup, PostgreSQL + pgvector schema design, JWT/OTP authentication, Alembic migrations, and security compliance. |
| **Member 2** | **AI & Multi-Agent Orchestration Lead**: 14-Agent LangGraph orchestration framework, prompt engineering, RAG retrieval engine (ICAR/KAU), and DSSAT simulation adapters. |
| **Member 3** | **Mobile UI & Android Client Lead**: Kotlin + Jetpack Compose mobile application, CameraX real-time quality analyzer, offline SQLite cache (Room), and Bhashini Malayalam voice player. |
| **Member 4** | **ML Engineering & Vision Lead**: EfficientNet-B3 disease classification model training, PyTorch quantization, ONNX Runtime Android integration, and golden dataset evaluation. |
| **Member 5** | **QA, Testing & Data Engineering Lead**: End-to-end integration testing playbook, pytest-asyncio test suites, CIB&RC chemical safety database validation, and CI/CD pipelines. |

---

## 📁 Documentation & Specifications Directory (`docs/`)

Complete product design, architectural decision records (ADRs), backend schemas, security compliance, and testing specifications are available in the [`docs/`](docs/) directory:

- 📄 **[1_AgriSAGE_PRD.docx](docs/1_AgriSAGE_PRD.docx)** — Product Requirements Document
- 📄 **[2_AgriSAGE_TRD.docx](docs/2_AgriSAGE_TRD.docx)** — Technical Requirements Document
- 📄 **[3_AgriSAGE_AppFlow.docx](docs/3_AgriSAGE_AppFlow.docx)** — App Flow & Multi-Surface Architecture
- 📄 **[4_AgriSAGE_UIUX_Spec.docx](docs/4_AgriSAGE_UIUX_Spec.docx)** — UI/UX Design System & Tokens
- 📄 **[5_AgriSAGE_BackendSchema.docx](docs/5_AgriSAGE_BackendSchema.docx)** — Complete PostgreSQL DDL, Schemas & Agent I/O
- 📄 **[6_AgriSAGE_ImplementationPlan.docx](docs/6_AgriSAGE_ImplementationPlan.docx)** — Master Implementation Plan & Timelines
- 📄 **[7_AgriSAGE_Security_Compliance.docx](docs/7_AgriSAGE_Security_Compliance.docx)** — Security Architecture & Compliance Guidelines
- 📄 **[8_AgriSAGE_AI_Prompt_Handbook.docx](docs/8_AgriSAGE_AI_Prompt_Handbook.docx)** — System Prompts & Guardrails Handbook
- 📄 **[9_AgriSAGE_Testing_QA_Playbook.docx](docs/9_AgriSAGE_Testing_QA_Playbook.docx)** — Comprehensive QA & Test Strategy
- 📄 **[10_AgriSAGE_Validation_Report.docx](docs/10_AgriSAGE_Validation_Report.docx)** — Architectural & System Validation Report
- 📄 **[11.1_AgriSAGE_Master_Build_Guide.docx](docs/11.1_AgriSAGE_Master_Build_Guide.docx)** — Step-by-Step Master Build Guide
- 📄 **[12_AgriSAGE_Team_Sprint_Plan.docx](docs/12_AgriSAGE_Team_Sprint_Plan.docx)** — Team Sprint Plan & GitHub Architecture
- 📄 **[13_AgriSAGE_Version_Update_Report.docx](docs/13_AgriSAGE_Version_Update_Report.docx)** — Version History & System Updates

---

## 🛠 Project Directory Structure

```
AgriSage/
├── apps/
│   └── web-expert/            # Agronomist Triage Workstation & Advisory Sandbox (React + Vite + TS)
├── mobile/                    # Mobile Application (Kotlin Jetpack Compose Android app)
├── backend/                   # FastAPI backend, 14 LangGraph agents, PostgreSQL + pgvector
│   ├── agents/                # 14 Multi-agent implementations (Vision, Weather, CropStage, Critic, etc.)
│   ├── api/v1/                # REST API endpoints (auth, farms, operations, diagnose, risk, schemes, simulate)
│   ├── data/                  # Standardized data schemas, GDD tables, disease classes, Malayalam dictionaries
│   ├── knowledge/             # ICAR / KAU document ingestion, hybrid RRF retrieval
│   ├── ml/                    # ONNX vision model pipelines and training scripts
│   ├── safety/                # Chemical safety blocker and hallucination detection
│   ├── services/              # LLM wrapper, embeddings, image security, morning briefing
│   └── simulation/            # DSSAT crop growth simulation adapters and scenario generators
├── alembic/                   # Alembic database migration scripts (001-022)
├── docs/                      # Specification Documents
├── DECISIONS_AND_ACTIONS.md   # Architectural Decision Records (ADRs) & Action Plan
├── LICENSE_REGISTRY.md        # Open-source dependency license registry
├── docker-compose.yml         # Local development container orchestration
└── Dockerfile                 # Backend container definition
```

---

## 🚀 Quick Start (development)

The commands below run from this repository root. They use the canonical
FastAPI application in `backend.main:app` and the Vite application in
`apps/web-expert/`.

### Prerequisites

- Python 3.11.9 (the repository selector is `.python-version`; Docker and CI use this exact runtime)
- Node.js 20.19.0 (the repository selector is `.nvmrc`; CI and `make test` use this exact runtime)
- GNU Make for the repository release/test commands
- Docker Engine with Docker Compose v2 and at least 8 GB of free disk space
- JDK 17 and an Android SDK only when building the mobile app

For the reproducible local checks, select Python 3.11.9 and Node.js 20.19.0
before running `make test` (for example, `nvm install 20.19.0 && nvm use 20.19.0`
when using nvm).

### Backend and database

```bash
cp .env.example .env
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install --require-hashes -r requirements.lock -r requirements-dev.lock
make preflight
docker compose up -d db
alembic upgrade head
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

The tracked Python lockfiles target Python 3.11 on x86_64 Linux and include
package hashes. Regenerate them with the `uv pip compile` command recorded in
their headers when changing the dependency inputs.

The frontend uses `apps/web-expert/package-lock.json`; run `npm ci` rather
than `npm install` for a clean, lockfile-respecting install.

The local `.env.example` values are development-only. Replace the JWT secret,
provider keys, and database settings before sharing the service or using
`ENVIRONMENT=production`. The API is available at `http://localhost:8000`;
`/health` is the liveness endpoint, `/ready` is the database-backed readiness
endpoint, and `/docs` is enabled only in development.

Embedding model loading is opt-in (`ENABLE_EMBEDDINGS=false`) so clean/offline
startup does not download a large Hugging Face model. Enable it only after the
model is available in the deployment environment and the knowledge/RAG path
has been validated.

#### OTP provider contract

Production sign-in requires `OTP_PROVIDER=generic_http`, an HTTPS
`OTP_PROVIDER_URL`, and `OTP_PROVIDER_KEY`. The backend sends a JSON `POST`
request with a bearer token and this body:

```json
{
  "to": "+919876543210",
  "otp": "123456",
  "message": "Your Agri-SAGE verification code is 123456.",
  "sender": "Agri-SAGE"
}
```

Any 2xx provider response means the message was accepted. Provider-specific
adapters can replace this generic adapter without changing the mobile API.
`OTP_DEV_MODE=true` is permitted only for local development and prints the OTP
to the local console; it is rejected by production configuration validation.

### Expert web app

```bash
cp apps/web-expert/.env.example apps/web-expert/.env
cd apps/web-expert
npm ci
npm run dev
```

Set `VITE_API_BASE_URL` in `apps/web-expert/.env` to the HTTPS origin of the
canonical FastAPI service when enabling backend authentication and live staff
operations data. Leave it empty for the local seed/demo preview:

```bash
# edit apps/web-expert/.env and set VITE_API_BASE_URL=https://api.example.org
```

The Vite development server normally runs at `http://localhost:5173`. Build a
static artifact with `npm run build`; preview it with `npm run preview`.

Web preview routes:

- `/` — public product/download experience.
- `/auth?mode=login` or `/auth?mode=signup` — role-aware farmer and employee/officer preview access.
- `/sandbox` — farmer advisory experience.
- `/operations` — employee/officer operations-console preview.
- `/dashboard` — expert review queue preview.

Without `VITE_API_BASE_URL`, the access portal and operations console stay in an
explicit local demo mode using browser session state and seeded data. With the
variable set, the portal uses the canonical OTP/JWT endpoints and the operations
console reads protected, read-only staff metrics and queue data. Employee/officer
roles still require server-side provisioning; review writes remain in the separate
expert workflow and are not exposed by the operations console.

### One offline-capable verification command

After the locked Python and frontend dependencies are installed, run:

```bash
make test
```

It runs Python syntax/tests and the local frontend typecheck, build, and lint
tools without downloading dependencies. It fails early when a pinned runtime
or local tool is missing instead of treating an incomplete check as a pass.
The direct commands are also useful for targeted work:

```bash
python -m pytest tests/ -v
python -m pytest backend/tests/ -v
cd apps/web-expert && npm run typecheck && npm run build && npm run lint
```

### Docker Compose stack

Validate both Compose files before starting anything:

```bash
make compose-config
make prod-config  # run with the real production secret environment only
```

Run the complete local stack, including migrations, with:

```bash
docker compose up --build -d
docker compose exec -T backend python scripts/smoke_tests.py --base-url http://127.0.0.1:8000
```

The backend container waits for PostgreSQL, applies Alembic migrations before
starting Uvicorn, and exposes a database-backed `/ready` health check. The
same migration-before-traffic command is the default Docker image command and
the production Compose command. Stop it with `docker compose down`.

The smoke script only performs read-only `GET /health` and `GET /ready`
requests. It does not call OTP, payment, or external-provider endpoints. Run
it against another environment with `make smoke SMOKE_BASE_URL=https://...`
only after the environment owner has approved that read-only check.

### Android client

```bash
cd mobile/android
cp local.properties.example local.properties
chmod +x gradlew
./gradlew test
./gradlew assembleDebug
```

Set `API_BASE_URL` in `local.properties` for the target environment. Firebase
push notifications additionally require a developer-provided
`app/google-services.json`; this file is intentionally ignored and is never
part of a clean checkout. CI builds the debug APK without that private file.

## 🚢 Production deployment checklist

1. Provision PostgreSQL with the `vector` extension and a separate, least-
   privilege runtime role; for the Dockerfile/Railway deployment set a strong
   `SECRET_KEY`, `DATABASE_URL`, explicit HTTPS `PUBLIC_BASE_URL`, and trusted
   `CORS_ORIGINS`. The tracked production Compose profile uses its `db` service
   and constructs its internal `DATABASE_URL` from `DB_PASSWORD`; do not leave
   the development `localhost` URL from `.env.example` in a production Compose
   environment.
2. Configure the external providers required by the features you enable:
   Gemini, weather/data feeds, R2, FCM, OTP delivery, Razorpay, and the DSSAT
   binary/model assets. The service fails closed for production JWT defaults,
   unconfigured payment endpoints, and unconfigured OTP delivery.
3. Supply `.env` through the secret manager (never commit it), then run
   `make preflight`, `make prod-config`, and build the tracked `Dockerfile`.
   Production Compose fails before startup when `DB_PASSWORD`, `SECRET_KEY`,
   `PUBLIC_BASE_URL`, or `CORS_ORIGINS` is missing. The image health check uses
   `/ready`; migrations must complete before the application receives traffic.
   Run the read-only smoke checks from the backend container after the service
   is healthy.
4. Configure Android signing, Firebase, Play Console metadata, privacy/terms,
   and a real-device test matrix. A debug APK is not a release artifact.
5. Run `alembic upgrade head` through migration `022_rls_policy_repair` against a fresh
   staging database. Provision staff roles through a controlled server-side
   process, smoke-test JWT/RBAC and the protected `/api/v1/operations/*` routes,
   verify audit rows, and confirm RLS behavior before enabling real users.
6. Run API, web, Android, security, accessibility, and agronomist safety review
   before enabling real users or payments.

## Known validation boundaries

The repository contains working offline tests and frontend checks, but a local
run cannot prove external credentials, provider quotas, production database
permissions, Android signing, model quality, CIB&RC data freshness, or real
farmer safety outcomes. A Compose config check and a local image build do not
prove that an external deployment is live. Those provider, infrastructure,
and human-review checks remain explicit release gates, not assumptions.

