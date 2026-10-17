# 🌾 Agri-SAGE — Gemini 2.5 Pro Build Prompt System

> **Scalable Agricultural Guidance Engine** · Zero Budget · Kerala Smallholder Farmers · ASIET Kalady

---

## What This Is

This folder contains the complete, production-ready **Gemini 2.5 Pro build prompt system** for Agri-SAGE. Every prompt is paste-ready. Each phase creates a GitHub Issue so you control contribution, assignment, and review before anything merges.

---

## 3 Rules Baked Into Every Prompt

| Rule | What It Does |
|---|---|
| **AUDIT-FIRST** | Reads + scores every existing file before touching it. Score ≥8 = PROTECTED, never rewritten |
| **GITHUB ISSUES** | After each phase, Gemini creates a GitHub Issue with all changes listed — you assign and review before merge |
| **ZERO HALLUCINATION** | Exact pinned imports. If uncertain, prints uncertainty instead of guessing |

---

## File Index

| File | What's Inside |
|---|---|
| `00-master-runner.md` | Entry point — paste this first. Sets global rules + branch + issue structure |
| `01-audit-protocol.md` | The audit logic embedded in all phases (reference file) |
| `02-phase1-foundation.md` | FastAPI + brain/ folder + 4 realtime data services + migrations |
| `03-phase2-agents.md` | LangGraph 14-agent system + parallel fan-out + MemorySaver |
| `04-phase3-rag.md` | KAU PDF ingestion + pgvector HNSW + multilingual-e5-large retrieval |
| `05-phase4-android.md` | Kotlin + Jetpack Compose app + voice + Room + WorkManager |
| `06-phase5-deploy.md` | Railway + GitHub Actions CI/CD + Grafana monitoring |
| `07-github-issues-guide.md` | How GitHub Issues replace auto-push — contribution + review workflow |
| `08-checklist.md` | Pre-start checklist — API keys, branches, .env, tools |

---

## Execution Order

```
1. Complete 08-checklist.md first
2. Paste 00-master-runner.md into Gemini 2.5 Pro
3. Paste 02-phase1-foundation.md → Gemini creates Issue #1
4. You review Issue #1 → assign to M1 → M1 merges PR
5. Paste 03-phase2-agents.md → Gemini creates Issue #2
6. Continue through phase 5
```

---

## Team Branch Map

| Branch | Owner | Scope |
|---|---|---|
| `dev/m1-backend` | M1 | FastAPI, services, migrations |
| `dev/m2-android` | M2 | Kotlin app, Compose, Room |
| `dev/m3-rag` | M3 | KAU ingestion, pgvector, rag_service |
| `dev/m4-agents` | M4 | LangGraph agents, graph, state |
| `dev/m5-tests` | M5 | Pytest suites, integration tests |
| `main` | All (via PR) | Production-ready merged code |

---

*Zero Budget · Realtime Data · Malayalam-First · October 2026*
