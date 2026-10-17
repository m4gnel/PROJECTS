# AMRS — Autonomous Multi-Agent Research Scientist & Startup Intelligence Platform

A multi-agent AI platform that turns a single research question into a complete, evidence-checked deliverable package: literature-grounded research report, fact-verification, critical review, market/competitor analysis, startup concepts, technical architecture sketch, and implementation roadmap.

## Architecture

- **Frontend:** Next.js 15+, TypeScript, Tailwind CSS
- **Backend:** FastAPI, Python 3.13+, Pydantic v2
- **Orchestration:** LangGraph (multi-agent state machine)
- **Database:** PostgreSQL via Supabase
- **Vector DB:** Qdrant Cloud
- **Knowledge Graph:** Neo4j Aura

## Quick Start

### Prerequisites

- Python 3.13+
- Node.js 20+
- A Supabase project (free tier)

### 1. Environment Setup

```bash
cp .env.example .env
# Fill in your API keys in .env
```

### 2. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
# → http://localhost:8000/health should return {"status": "ok"}
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

### 4. Run Tests

```bash
pytest tests/test_model_router.py -v
pytest tests/test_health.py -v
```

## Project Structure

```
├── .gitignore
├── .env.example
├── backend/
│   ├── main.py              # FastAPI app with /health
│   ├── config.py            # Pydantic Settings
│   ├── model_router.py      # ModelRouter + circuit breaker
│   └── agents/              # EMPTY until Milestone 1
├── frontend/                # Next.js app
├── tests/
│   ├── test_model_router.py # Fallback verification test
│   └── test_health.py       # Health endpoint test
└── documents/               # PRD, TRD, and design docs
```

## Documentation

See the `documents/` folder for the full specification set (PRD, TRD, App Flow, UI/UX, Backend Schema, Implementation Plan, Security Threat Model, etc.).
