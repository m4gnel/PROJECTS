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
│   ├── api/v1/                # REST API endpoints (auth, farms, diagnose, risk, schemes, simulate)
│   ├── data/                  # Standardized data schemas, GDD tables, disease classes, Malayalam dictionaries
│   ├── knowledge/             # ICAR / KAU document ingestion, hybrid RRF retrieval
│   ├── ml/                    # ONNX vision model pipelines and training scripts
│   ├── safety/                # Chemical safety blocker and hallucination detection
│   ├── services/              # LLM wrapper, embeddings, image security, morning briefing
│   └── simulation/            # DSSAT crop growth simulation adapters and scenario generators
├── alembic/                   # Alembic database migration scripts (001-017)
├── docs/                      # Specification Documents
├── DECISIONS_AND_ACTIONS.md   # Architectural Decision Records (ADRs) & Action Plan
├── LICENSE_REGISTRY.md        # Open-source dependency license registry
├── docker-compose.yml         # Local development container orchestration
└── Dockerfile                 # Backend container definition
```

---

## 🚀 Quick Start

```bash
cp .env.example .env
docker compose up -d
alembic upgrade head
uvicorn backend.main:app --reload
```

