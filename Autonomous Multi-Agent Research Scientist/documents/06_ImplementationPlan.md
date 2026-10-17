# Implementation Plan

**Product:** AMRS — Autonomous Multi-Agent Research Scientist & Startup Intelligence Platform
**Version:** 1.0
**Date:** June 2026

---

## 1. Purpose

This plan sequences the build across phases, maps work to the roles defined for the team, and sets realistic milestones for a final-year project timeline. Durations assume a small student team (3–6 people) working part-time alongside coursework; adjust proportionally for your actual team size and availability.

---

## 2. Team Roles and Responsibilities

| Role | Responsibilities | Primary Documents Owned |
|---|---|---|
| AI/ML Engineer | Build agent prompts and logic, integrate LLM providers, implement Model Router and fallback logic, build RAG pipeline | TRD §3, §4 |
| Backend Developer | FastAPI endpoints, LangGraph orchestration wiring, database access layer, auth integration | TRD §5, Backend Schema |
| Frontend Developer | Next.js UI, all screens in App Flow, component library from UI/UX doc | App Flow, UI/UX |
| Data Engineer | Qdrant/Neo4j setup and ingestion pipelines, embedding pipeline, data retention jobs | Backend Schema §3–4 |
| DevOps Engineer | CI/CD, hosting setup (Cloudflare/Render/Supabase), monitoring, secrets management | TRD §7 |
| QA/Test Engineer | Test plans per agent, pipeline integration tests, load testing within free-tier limits | All documents (verification) |
| Product Manager / Lead | Scope control, demo script, stakeholder presentation, PRD ownership | PRD |

On a small team, one person may hold 2–3 of these roles; the responsibilities above should still be explicitly assigned so nothing is assumed to be "someone else's job."

---

## 3. Phased Plan

### Phase 0 — Setup (Week 1)
- Provision all accounts: Supabase, Qdrant Cloud, Neo4j Aura, Cloudflare Pages, Render, GitHub repo, Google AI Studio, Groq, OpenRouter.
- Scaffold Next.js frontend and FastAPI backend repos with CI pipeline (lint + basic test on push).
- Implement and test the Model Router fallback class (TRD §3.2) in isolation, before any agent depends on it — this is the highest-risk component and should be validated early with deliberate failure-injection tests (e.g., force a 429 and confirm fallback fires).

**Exit criteria:** A "hello world" FastAPI endpoint deployed on Render, callable from a deployed Next.js page on Cloudflare Pages, with the Model Router successfully completing a test call and successfully falling back when the primary provider is deliberately blocked.

### Phase 1 — Daily Assistant Mode + Core Auth (Weeks 2–3)
- Supabase Auth integration (email + Google OAuth).
- `POST /api/v1/chat/daily` endpoint with streaming.
- Daily Assistant Chat UI screen.
- Guest mode with rate limiting.

**Exit criteria:** A user can sign up, log in, and have a working streamed chat conversation in production, with guest rate-limiting verified.

### Phase 2 — Research Pipeline Core (Weeks 4–7)
- LangGraph state machine skeleton with Planner → Research → Fact Checker → Report Writer as the minimum linear path (TRD §4.1).
- Source retrieval integrations: arXiv, Semantic Scholar, PubMed, Crossref.
- `research_sessions`, `agent_runs`, `sources`, `claims`, `reports` tables live (Backend Schema §2).
- Query Composer and Agent Monitoring Dashboard UI screens (App Flow §3.6–3.7).
- Report View UI with Fact-Check Table (UI/UX §3.5).

**Exit criteria:** A user can submit a research query and receive a basic report with cited sources and a fact-check table, end-to-end, in production.

### Phase 3 — Critic, Business, and Startup Agents (Weeks 8–10)
- Critic Agent integrated (TRD §4.4).
- Business Analyst + Startup Generator agents integrated, gated by the optional toggles in Query Composer.
- `critic_notes`, `startup_concepts` tables populated.
- Confidence/Evaluator scoring implemented (TRD §4.11) and surfaced in Report View header.

**Exit criteria:** Full report includes critic notes, market analysis, and startup concepts when toggles are enabled, with a visible confidence score.

### Phase 4 — Technical Architect, Knowledge Graph, Memory (Weeks 11–13)
- Technical Architect Agent producing architecture sketch + roadmap section.
- Knowledge Graph Agent + Neo4j integration; basic graph view (can be a simple visualization, not a polished interactive graph UI, for v1).
- Memory Agent: session embedding on completion, semantic search endpoint (`GET /api/v1/sessions/search`), Saved Library UI.

**Exit criteria:** Full feature set from PRD §7.2 is functional; a user can search past sessions semantically.

### Phase 5 — Hardening, Monitoring, Security Pass (Weeks 14–15)
- OpenTelemetry instrumentation + Grafana dashboards.
- Security pass: confirm RBAC enforcement at the API layer (not just frontend), audit logging, secrets review.
- Failure-injection testing across all agent fallback chains (re-run the Phase 0 test methodology against every agent, not just the router in isolation).
- Performance pass against TRD §8 targets.

**Exit criteria:** All NFR targets from PRD §8 and TRD §8 are measured (not assumed) and documented with actual numbers, including honest reporting where a target is not yet met.

### Phase 6 — Demo Prep and Documentation (Weeks 16–17)
- Finalize demo script using PRD Appendix A example queries.
- Rehearse failure scenarios live (e.g., deliberately show a degraded section recovering) — this is a stronger demo moment than hoping nothing fails, since it proves the reliability architecture rather than just claiming it.
- Polish README, architecture diagrams, and presentation deck.
- Final QA pass across both modes.

**Exit criteria:** Project is demo-ready with a rehearsed script, a deployed production instance, and complete documentation (this document set).

---

## 4. Milestone Summary Table

| Phase | Weeks | Key Deliverable |
|---|---|---|
| 0 — Setup | 1 | Deployed skeleton + working Model Router with verified fallback |
| 1 — Daily Assistant | 2–3 | Working chat mode in production |
| 2 — Research Core | 4–7 | End-to-end basic research report |
| 3 — Critic/Business/Startup | 8–10 | Full report with confidence scoring |
| 4 — Architect/Graph/Memory | 11–13 | Full PRD v1 feature set complete |
| 5 — Hardening | 14–15 | Measured (not assumed) NFR compliance |
| 6 — Demo Prep | 16–17 | Final, rehearsed, documented deliverable |

**Total: 17 weeks**, matching the original phase estimate, restructured here around testable exit criteria at each stage rather than feature lists alone — so progress is verifiable, not just claimed.

---

## 5. Definition of Done (Project-Level)

A feature is not "done" when the code is written. It is done when:
1. It works against at least one live fallback scenario (primary provider deliberately disabled), not just the happy path.
2. Its data is correctly persisted in the schema defined in the Backend Schema document.
3. Its UI matches the states defined in the UI/UX document, including degraded/error states — not just the success state.
4. It has been demoed live by someone other than the person who built it.

---

## 6. Presentation Guidance for Faculty/HR/Investor Review

When presenting this project, lead with the architecture and the reliability engineering (Model Router, fallback chains, confidence scoring), not with accuracy claims. A reviewer with real engineering background will be more impressed by *"here's how we handle a provider going down mid-demo"* than by any unverifiable accuracy percentage. This plan is built so that story is literally true and demonstrable, not just asserted.
