# Technical Requirements Document (TRD)

**Product:** AMRS — Autonomous Multi-Agent Research Scientist & Startup Intelligence Platform
**Version:** 1.0
**Date:** June 2026
**Status:** Draft for Review

---

## 1. Purpose

This TRD translates the PRD into concrete technical decisions: architecture, agent design, model selection strategy, infrastructure, and the reliability mechanisms that make a free/low-cost stack viable for a multi-agent system. It corrects a common but technically inaccurate assumption — that any provider offers "unlimited free" API access — and replaces it with the actual engineering pattern used to handle this in production: **multi-provider fallback with circuit breaking**, not a single infinite key.

---

## 2. Architecture Overview

```
                        ┌─────────────────┐
                        │   Next.js Web    │
                        │  (Frontend SPA)  │
                        └─────────┬────────┘
                                  │ HTTPS/REST + SSE
                        ┌─────────▼────────┐
                        │   API Gateway     │
                        │   (FastAPI)       │
                        └─────────┬────────┘
                                  │
                  ┌───────────────▼───────────────┐
                  │   Orchestration Layer          │
                  │   (LangGraph state machine)     │
                  └───────────────┬───────────────┘
                                  │
        ┌─────────────────────────┴─────────────────────────┐
        │                  Agent Coordinator                  │
        └─────────────────────────┬─────────────────────────┘
                                  │
    ┌───────┬────────┬────────┬───┴────┬────────┬────────┬───────┐
    │Planner│Research│  Fact  │ Critic │Business│Startup │ ...   │
    │ Agent │ Agent  │Checker │ Agent  │Analyst │Gen     │       │
    └───┬───┴───┬────┴───┬────┴───┬────┴───┬────┴───┬────┴───────┘
        │       │        │        │        │        │
        └───────┴────────┴───┬────┴────────┴────────┘
                              │
                  ┌───────────▼───────────┐
                  │   Model Router Layer   │
                  │ (provider fallback +   │
                  │  circuit breaker)      │
                  └───────────┬───────────┘
                              │
      ┌───────────┬───────────┼───────────┬───────────┐
      │  Gemini    │   Groq    │ OpenRouter│  Local     │
      │  API       │   API     │  (router) │  fallback  │
      └───────────┴───────────┴───────────┴───────────┘

                  ┌───────────────────────┐
                  │   RAG / Memory Layer   │
                  │  Qdrant + Postgres     │
                  └───────────────────────┘
```

---

## 3. Model Strategy — The Honest Version

### 3.1 Why "unlimited free API" is not a real option

No provider — Google, Groq, OpenRouter, DeepSeek, Anthropic, or any other — offers truly unlimited free inference. As of June 2026:

- OpenRouter's free-tier models are real production weights but are rate-limited (commonly around 20 requests/minute and 200 requests/day per free model) and the list of which models are free **changes without notice** — several models that were free earlier in 2026 (e.g., certain DeepSeek and Qwen variants) lost free status mid-year.
- Google AI Studio's Gemini free tier has its own daily/per-minute request caps, which vary by model tier.
- Groq's free developer tier is fast but similarly rate-limited, not unlimited.

Designing AMRS around "one unlimited free key" would mean the system breaks the first time that provider throttles or deprecates the model. The correct engineering response is a **fallback chain**, not a search for a mythical unlimited key.

### 3.2 Model Router Design

Each agent role is mapped to a **primary model + ordered fallback list**, not a single hardcoded model:

| Agent | Primary | Fallback 1 | Fallback 2 |
|---|---|---|---|
| Planner | Gemini 2.5 Flash | Groq (Llama 3.3 70B) | OpenRouter free router |
| Research | Gemini 2.5 Flash | OpenRouter free router | Groq |
| Fact Checker | Gemini 2.5 Flash | Groq | OpenRouter free router |
| Critic | Groq (Llama 3.3 70B) | Gemini 2.5 Flash | OpenRouter free router |
| Data Analyst | Gemini 2.5 Flash | Groq | — |
| Knowledge Graph extraction | Groq (Llama 3.3 70B) | Gemini 2.5 Flash | — |
| Business Analyst | Gemini 2.5 Flash | Groq | OpenRouter free router |
| Startup Generator | Groq (Llama 3.3 70B) | Gemini 2.5 Flash | — |
| Technical Architect | Gemini 2.5 Flash | Groq | — |
| Report Writer | Gemini 2.5 Flash | Groq | — |
| Evaluator | Gemini 2.5 Flash | Groq | — |
| Memory Agent | No LLM — embedding model only (see §3.4) | — | — |

**Implementation pattern (circuit breaker + retry):**

```python
class ModelRouter:
    def __init__(self, role: str, chain: list[ModelProvider]):
        self.role = role
        self.chain = chain  # ordered: primary -> fallback1 -> fallback2
        self.breaker_state = {p.name: "closed" for p in chain}

    async def call(self, prompt: str, **kwargs) -> ModelResponse:
        last_error = None
        for provider in self.chain:
            if self.breaker_state[provider.name] == "open":
                continue  # skip providers known to be down/limited right now
            try:
                response = await provider.complete(prompt, **kwargs)
                self.breaker_state[provider.name] = "closed"
                return response
            except (RateLimitError, ProviderUnavailableError) as e:
                last_error = e
                self.breaker_state[provider.name] = "open"
                continue
        raise AllProvidersExhaustedError(self.role, last_error)
```

- A provider that fails is marked "open" (skipped) for a cooldown window, then retried.
- Every agent call is wrapped in this router — never a direct hardcoded API call.
- If **all** providers in a chain are exhausted, the pipeline step returns a clearly labeled `"status": "degraded"` result rather than crashing the whole run — this satisfies PRD requirement FR-4.2.

### 3.3 Where to obtain each provider's API key

| Provider | Console URL | Free tier notes |
|---|---|---|
| Google AI Studio (Gemini) | https://aistudio.google.com/app/apikey | Generous free tier; rate-limited per minute/day; limits documented in console |
| Groq | https://console.groq.com/keys | Free developer tier; very fast inference; rate-limited |
| OpenRouter | https://openrouter.ai/keys (sign in, then Keys page) | Free models marked `:free`; 20 req/min, 200 req/day typical per model; list changes — check https://openrouter.ai/models filtered by price before relying on a specific slug |
| DeepSeek Platform | https://platform.deepseek.com/api_keys | Low-cost, not free-unlimited; useful as a paid escalation tier if free chain is exhausted during a live demo |

**Engineering note for the team:** treat every model slug in this document as **a pattern, not a permanent contract**. Before each milestone demo, re-verify the free model list at the OpenRouter models page, since slugs are added and removed regularly.

### 3.4 Memory / Embeddings

Memory Agent does not need a chat LLM. It needs an embedding model:
- Primary: Gemini embedding endpoint (`text-embedding-004` or current equivalent — verify current model name in Google AI Studio docs at build time).
- Fallback: open-source embedding model run via a free-tier inference endpoint (e.g., a sentence-transformers model via Hugging Face Inference API free tier), or local CPU inference for small batches if needed (lightweight enough not to require a GPU).

---

## 4. Agent Specifications

Each agent is implemented as a LangGraph node with a defined input schema, output schema, and timeout.

### 4.1 Planner Agent
- **Input:** raw user query, user tier (guest/registered)
- **Output:** task graph (ordered list of downstream agents to invoke + parameters)
- **Timeout:** 15s
- **Failure mode:** falls back to a default linear pipeline (Research → FactCheck → Report) if planning fails

### 4.2 Research Agent
- **Input:** sub-query list from Planner
- **Tools:** arXiv API, Semantic Scholar API, PubMed E-utilities, Crossref API, general web search
- **Output:** ranked list of sources with title, abstract/snippet, URL, publication date
- **Timeout:** 45s per source category, parallelized across sources

### 4.3 Fact Checker Agent
- **Input:** claims extracted from Research Agent output
- **Output:** per-claim verification status (`Verified` / `Partially Verified` / `Unverified` / `Contradicted`) + supporting/conflicting source links
- **Logic:** a claim is "Verified" only if corroborated by ≥ 2 independent sources; "Contradicted" if sources directly conflict — both states must surface to the user, never silently resolved in one direction

### 4.4 Critic Agent
- **Input:** Research + Fact Checker outputs
- **Output:** structured list of `{assumption, risk_level, explanation}` and `{gap, why_it_matters}`
- **Design intent:** explicitly told (via prompt) to argue against the research findings to surface weaknesses — this is the "debate" mechanism, implemented as a single adversarial-prompted pass in v1, not a literal multi-turn agent argument (see §9, Phase 2 backlog, for true multi-turn debate)

### 4.5 Data Analyst Agent
- **Input:** any structured/numeric data found during research
- **Tools:** pandas, numpy for trend extraction on structured inputs
- **Output:** summary statistics, trend description (text, not guaranteed statistical significance — disclosed in output)

### 4.6 Knowledge Graph Agent
- **Input:** entities extracted from research text
- **Output:** entity-relationship triples stored in Neo4j Aura free tier
- **v1 scope note:** lightweight entity-relationship extraction via prompted LLM call, not a dedicated NER model — sufficient for demo-scale graphs (tens to low hundreds of nodes)

### 4.7 Business Analyst Agent
- **Input:** research topic + findings
- **Output:** TAM/SAM/SOM rough estimate (labeled as an estimate, with stated assumptions), top 3 competitor list with source links
- **Disclosure requirement:** market-size figures must show the estimation method, since these are inherently approximate

### 4.8 Startup Generator Agent
- **Input:** research + business analysis
- **Output:** 2–3 ranked startup concepts, each with target user, monetization model, and one key differentiator vs. existing players

### 4.9 Technical Architect Agent
- **Input:** top startup concept
- **Output:** text/Mermaid architecture diagram, recommended stack, rough build-phase breakdown

### 4.10 Report Writer Agent
- **Input:** all upstream agent outputs
- **Output:** assembled report (Markdown internally, exported to PDF/DOCX on request)

### 4.11 Evaluator Agent
- **Input:** full pipeline output
- **Output:** composite confidence score (0–100) and per-section coverage score, computed from a weighted rubric (source count, contradiction count, critic-flagged risk count) — **a heuristic score, explicitly disclosed as such, not a certified accuracy measure**

### 4.12 Memory Agent
- **Input:** completed session
- **Output:** embeds and stores session summary in Qdrant for future semantic retrieval; no LLM reasoning call required

---

## 5. Technology Stack

| Layer | Technology | Justification |
|---|---|---|
| Frontend | Next.js 15+, TypeScript, Tailwind CSS, ShadCN UI | Modern, widely-used, free hosting compatible |
| Backend | FastAPI, Python 3.13+, Pydantic v2 | Async-friendly, strong typing for agent I/O schemas |
| Orchestration | LangGraph | Purpose-built for stateful multi-agent graphs with conditional routing |
| Relational DB | PostgreSQL via Supabase | Free tier, includes auth, generous limits for student scale |
| Vector DB | Qdrant Cloud (free tier) | Purpose-built vector search, generous free quota |
| Knowledge Graph | Neo4j Aura (free tier) | Native graph queries for entity relationships |
| Auth | Supabase Auth (or Clerk free tier) | OAuth + email, integrates with Postgres |
| Hosting (frontend) | Cloudflare Pages | Free, global CDN |
| Hosting (backend) | Render (free/starter tier) | Simplest free Python deployment with persistent processes |
| CI/CD | GitHub Actions | Free for public/student repos |
| Monitoring | OpenTelemetry + Grafana Cloud free tier | Standard observability stack with a free entry tier |

---

## 6. Reliability, Evaluation, and Fault Tolerance (Replacing "100% Accuracy")

This section is the technical answer to "zero error, without fail" — what is actually achievable and how it's engineered:

1. **Redundancy, not perfection.** Every agent call goes through the Model Router (§3.2). No single provider outage takes down the pipeline.
2. **Explicit confidence, not silence.** The Evaluator Agent's score and the Fact Checker's per-claim status make uncertainty visible instead of hiding it behind a confident-sounding paragraph.
3. **Graceful degradation.** If the Knowledge Graph or Business Analyst step fails, the pipeline still returns the sections that succeeded, clearly marked, rather than failing the entire request (FR-4.2).
4. **Human-in-the-loop framing.** The UI must never present AMRS output as final truth — every report carries a visible "AI-generated, verify before relying on this for high-stakes decisions" notice, consistent with how production AI products at every major lab present their outputs.
5. **Continuous evaluation.** Track real outcomes over time (Section 8 metrics in PRD) rather than asserting accuracy a priori.

---

## 7. Security Architecture

- **Auth:** OAuth 2.0 + JWT session tokens, managed via Supabase Auth.
- **Authorization:** Role-based access control — Guest, Registered, Admin — enforced at the FastAPI dependency-injection layer, not just in the frontend.
- **Secrets management:** All provider API keys stored as environment variables / secret manager entries, never committed to source control or exposed to the frontend.
- **Rate limiting:** Per-user request quotas enforced at the API Gateway, separate from (and in addition to) upstream provider rate limits.
- **Encryption:** TLS in transit (enforced by Cloudflare/Render defaults); encryption at rest via Supabase/Qdrant managed encryption.
- **Audit logging:** All Deep Research Mode runs logged with user ID, timestamp, and pipeline outcome for traceability — not full prompt/response bodies by default, to limit sensitive data retention.

---

## 8. Performance Targets

| Metric | Target |
|---|---|
| Daily Assistant first-token latency | < 3s (p50) |
| Deep Research full pipeline | 1–10 minutes depending on query breadth and provider latency |
| Concurrent demo-day users | 10–50 (realistic for final-year demo; PRD's "1000+" framing is reserved for a future scaled deployment, not committed for v1) |
| API fallback engagement | System should successfully complete a request via fallback in ≥ 95% of cases where the primary provider fails, rather than hard-failing |

---

## 9. Phase 2 Backlog (Explicitly Deferred)

- True multi-turn agent debate (agents iterating on each other's critiques across multiple rounds, not a single adversarial pass).
- Real-time multi-user collaboration workspace.
- Voice input/output.
- 100+ language support (v1: English-first, architecture allows future i18n).
- Dedicated fine-tuned models for specific agent roles, replacing general-purpose model calls.

---

## 10. Open Engineering Risks

| Risk | Mitigation Owner | Notes |
|---|---|---|
| Free model deprecation mid-build | Backend/AI lead | Router pattern in §3.2 isolates this; re-verify model list before each milestone |
| LangGraph version changes | Backend lead | Pin dependency versions; test before upgrading |
| Qdrant/Neo4j free tier quota exhaustion at demo scale | Data engineer | Monitor usage dashboards; have a data-retention/cleanup job for old sessions |
| Cold-start latency on Render free tier | DevOps | Consider a lightweight keep-alive ping or accept first-request latency in demo script |
