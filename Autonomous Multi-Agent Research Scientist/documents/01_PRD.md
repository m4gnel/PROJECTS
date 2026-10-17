# Product Requirements Document (PRD)

**Product:** AMRS — Autonomous Multi-Agent Research Scientist & Startup Intelligence Platform
**Document Owner:** [Your Name]
**Version:** 1.0
**Date:** June 2026
**Status:** Draft for Review

---

## 1. Purpose of This Document

This PRD defines what AMRS is, who it serves, what it must do, and how its success will be measured. It is the single source of truth for product scope during the final-year build. Engineering decisions in the TRD, App Flow, UI/UX, and Backend Schema documents all trace back to requirements stated here.

---

## 2. Product Summary

AMRS is a multi-agent AI platform that turns a single research question into a complete, evidence-checked deliverable package: a literature-grounded research report, a fact-verification pass, a critical review, a market/competitor analysis, startup concept generation, a technical architecture sketch, and an implementation roadmap.

Where a conventional chatbot returns one generated answer, AMRS coordinates a pipeline of specialized agents — each with a narrow job — that hand work to one another, check each other's output, and converge on a reviewed deliverable. The user also has the option to use AMRS as a normal day-to-day AI chat assistant for lighter tasks, so the product is useful on both a daily basis and for deep, occasional research work.

**This document deliberately avoids absolute claims.** No AI system — including those built by Anthropic, Google, OpenAI, or Microsoft — can guarantee 100% accuracy or zero error. AMRS's actual value proposition is **higher reliability through cross-checking, explicit confidence scoring, and visible reasoning**, not infallibility. Every target in Section 8 is a measurable goal, not a guarantee.

---

## 3. Problem Statement

| Audience | Current Pain |
|---|---|
| Students / researchers | Spend hours manually searching, reading, and cross-checking papers before they can even start analysis. |
| Startup founders | Market research, competitor analysis, and opportunity-spotting are scattered across many disconnected tools. |
| Enterprises / consultants | Need defensible, source-cited research, not a single ungrounded LLM answer. |
| Everyone above | Existing AI tools (ChatGPT, Perplexity, Gemini) produce **one model's answer**, with no built-in adversarial fact-checking or business translation step. |

Single-agent LLM tools are good at retrieval and summarization but do not natively **debate their own conclusions**, **flag contradictions across sources**, or **carry a research finding through to a business plan and technical roadmap**. AMRS is built specifically to close that gap, not to out-compete general chat assistants at being a chat assistant.

---

## 4. Goals and Non-Goals

### 4.1 Goals (v1 / final-year scope)

1. Accept a free-text research query and produce a structured, source-cited research report.
2. Run an automated fact-check pass that flags low-confidence or contradicted claims.
3. Run a critic pass that explicitly lists assumptions, gaps, and weaknesses in the research.
4. Generate a market/competitor snapshot and 2–3 startup concepts derived from the research.
5. Generate a technical architecture sketch and phased implementation roadmap for the top concept.
6. Support a lightweight "daily assistant" chat mode for general Q&A, separate from the heavy research pipeline.
7. Show the user which agent is acting at each stage (transparency), and a confidence/evaluation score on the final report.
8. Run entirely on free-tier or low-cost cloud services suitable for a student budget.

### 4.2 Non-Goals (explicitly out of scope for v1)

- Real-time collaborative multi-user editing (Phase 2+).
- Mobile native apps (web-responsive only in v1).
- Guaranteed unlimited-throughput, zero-latency inference — free-tier APIs have rate limits; v1 must design around them, not assume they don't exist.
- Legal, medical, or financial advice — AMRS produces research and business *analysis*, not licensed professional advice, and the UI must disclose this.
- 100% factual accuracy — v1 targets measurable confidence scoring and source attribution, not infallibility.

---

## 5. Target Users and Personas

| Persona | Primary Use Case | Mode Used |
|---|---|---|
| **Aditi, final-year CS student** | Literature review for her thesis | Deep Research Mode |
| **Rahul, solo founder** | "Is there a startup here?" market validation | Deep Research Mode |
| **Priya, working professional** | "Explain this for me," daily learning, quick drafting | Daily Assistant Mode |
| **Faculty/HR reviewer** | Evaluating the system live in a demo | Both modes, plus Agent Monitoring Dashboard |

---

## 6. Core User Stories

1. *As a student*, I want to type a research topic and receive a cited literature review, so I don't have to manually search five different academic databases.
2. *As a founder*, I want the system to point out market gaps and generate startup concepts from a research topic, so I can validate an idea quickly.
3. *As any user*, I want to see a confidence score and list of flagged contradictions, so I know how much to trust the output before I rely on it.
4. *As a daily user*, I want to ask normal questions (coding help, explanations, writing) without triggering the full multi-agent pipeline, so simple requests stay fast and cheap.
5. *As a reviewer in a demo*, I want to watch each agent's status update in real time, so the multi-agent architecture is visible and not a black box.
6. *As a returning user*, I want the system to remember my previous research sessions, so I can build on past work instead of starting over.

---

## 7. Functional Requirements

### 7.1 Daily Assistant Mode
- FR-1.1: User can send free-text chat messages and receive streamed responses.
- FR-1.2: System maintains conversation context within a session.
- FR-1.3: No multi-agent pipeline is triggered in this mode (single model call, for cost and speed).

### 7.2 Deep Research Mode
- FR-2.1: User submits a research query (text input, optional file/PDF upload for grounding).
- FR-2.2: Planner Agent decomposes the query into a task list and selects which downstream agents are needed.
- FR-2.3: Research Agent retrieves sources from at least two of: arXiv, Semantic Scholar, PubMed, Crossref, general web search.
- FR-2.4: Fact Checker Agent cross-references claims across at least two independent sources where possible and assigns a verification status (Verified / Partially Verified / Unverified / Contradicted).
- FR-2.5: Critic Agent produces an explicit list of assumptions, limitations, and open questions.
- FR-2.6: Business Analyst Agent produces a market snapshot (TAM/SAM/SOM estimate, top 3 competitors) when the query has commercial relevance.
- FR-2.7: Startup Generator Agent proposes 2–3 ranked concepts with a one-line monetization model each.
- FR-2.8: Technical Architect Agent produces a high-level architecture diagram (text/Mermaid) and stack recommendation for the top concept.
- FR-2.9: Report Writer Agent assembles all of the above into one structured report, exportable as PDF/DOCX.
- FR-2.10: Evaluator Agent assigns a final composite confidence score and a per-section coverage score.
- FR-2.11: User can view intermediate agent outputs (not just the final report) via an expandable trace view.

### 7.3 Memory
- FR-3.1: System stores past research sessions per user and allows retrieval/reuse of prior findings.
- FR-3.2: Memory Agent performs semantic search over past sessions, not keyword match only.

### 7.4 Monitoring/Transparency
- FR-4.1: Agent Monitoring Dashboard shows live status (queued/running/done/failed) for each agent in the current pipeline run.
- FR-4.2: Failed agent steps show a visible error/fallback notice rather than failing silently.

### 7.5 Account & Access
- FR-5.1: Email/OAuth-based authentication.
- FR-5.2: Role-based access: Guest (Daily Assistant only, rate-limited), Registered User (full features, quota-limited), Admin (system monitoring).

---

## 8. Non-Functional Requirements (Reliability Targets, Not Guarantees)

| Requirement | Target | Notes |
|---|---|---|
| Daily Assistant response time | < 3 seconds to first token (p50) | Single model call |
| Deep Research completion time | 1–10 minutes depending on query complexity | Multi-agent pipeline; user sees live progress, not a frozen spinner |
| System availability | 99% monthly (best-effort on free/low-cost infra) | Not an SLA; stated as an engineering target |
| Fact-check coverage | ≥ 80% of extracted factual claims receive a verification status | Remaining claims marked "Unverified — insufficient sources," never silently dropped |
| Fallback behavior | If primary LLM/API fails or rate-limits, system retries with a defined fallback model within 2 attempts | No request should hard-fail without a fallback attempt |
| Data privacy | User research sessions are private by default; no session content used for model training without explicit opt-in | |
| Cost ceiling | Entire stack operable at $0–10/month at student-project scale | Validated against current free-tier limits, which change over time (see TRD §3 for the live mitigation plan) |

---

## 9. Success Metrics

**For the academic/demo context:**
- Live demo completes a research query end-to-end without manual intervention.
- Faculty/HR panel can see distinct agent contributions (not one opaque LLM call).
- At least 3 of the 5 example queries in the demo script (Appendix A) produce a coherent, cited, multi-section report.

**For a product-track future:**
- Weekly active users returning for a second research session.
- % of reports where the user marks the confidence score as "matched my own judgment" after reading sources.
- Average time-to-first-insight versus manual research (target: 5–10x faster for literature review tasks specifically).

---

## 10. Assumptions and Dependencies

- Free-tier API availability (Gemini, Groq, OpenRouter free models) will fluctuate; the product must degrade gracefully, not assume permanence of any single free model (see TRD §3, "Model Volatility Mitigation").
- Academic source APIs (arXiv, Semantic Scholar, PubMed) are free for non-commercial/research use at the request volumes this project expects.
- Hosting depends on Cloudflare Pages, Render, Supabase, and Qdrant Cloud free tiers remaining available at current limits through the project timeline.

---

## 11. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Free-tier model is deprecated or rate-limited mid-project | High | Medium | Multi-provider fallback chain (TRD §3); no single point of dependency |
| Multi-agent pipeline cost/latency too high for live demo | Medium | High | Cap pipeline depth per query tier; cache repeated sub-queries |
| Hallucinated citations | Medium | High | Fact Checker Agent + mandatory source-link display; never present an unsourced claim as verified |
| Scope creep beyond final-year timeline | High | Medium | Strict v1 scope (Section 4.2); Phase 2 backlog tracked separately (see Implementation Plan) |

---

## 12. Out-of-Scope Disclosure for Presentation

When presenting to faculty, HR, or any technical panel, do **not** state that the system achieves "100% accuracy" or operates "without fail." State instead: *"AMRS is designed for measurable reliability through multi-agent cross-verification, explicit confidence scoring, and graceful fallback — the same reliability philosophy used in production systems at Anthropic, Google, and OpenAI, none of which claim zero-error operation either."* This framing is more credible to any reviewer with real engineering experience, and it sets up the project as understanding production AI rather than overselling a student prototype.

---

## Appendix A — Example Demo Queries

1. "What are the latest AI applications in precision agriculture, and is there a startup opportunity?"
2. "Summarize recent research on retrieval-augmented generation for medical diagnosis."
3. "Find contradictions in current literature on remote work productivity."
4. "What's the market gap in AI-powered legal contract review tools?"
5. "Explain transformer architectures to me like I'm a beginner." *(Daily Assistant Mode — used to demonstrate the dual-mode design.)*
