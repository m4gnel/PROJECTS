# Cost Model & Unit Economics

**Product:** AMRS — Autonomous Multi-Agent Research Scientist & Startup Intelligence Platform
**Version:** 1.0
**Date:** June 2026
**Status:** Draft for Review

---

## 1. Purpose

Every other document in this set assumes "free tier" infrastructure. That assumption is correct for a final-year academic build at low usage, and it is the single assumption most likely to silently fail the moment AMRS has real, recurring users — which is the explicit goal stated for this project. This document does the arithmetic: what a research run actually costs once free-tier rate limits are exceeded, where the free stack's real ceiling is, and what a sustainable paid tier would need to charge. The goal is to replace "it's free" with "here is exactly when it stops being free, and what to do about it" — the same discipline applied to accuracy claims elsewhere in this document set applies here to cost claims.

---

## 2. Pricing Inputs (Verified June 2026)

All rates below are current standard pay-as-you-go API pricing, not free-tier rates, since the free tier is rate-limited rather than infinite — the paid rate is what governs cost the moment usage exceeds free quotas (TRD §3.1).

| Provider / Model | Input ($/1M tokens) | Output ($/1M tokens) | Notes |
|---|---|---|---|
| Gemini 2.5 Flash | $0.30 | $2.50 | Primary model for most agents per TRD §3.2 |
| Gemini 2.5 Flash-Lite | $0.10 | $0.40 | Cheaper alternative for low-complexity agent roles |
| Groq — Llama 3.3 70B Versatile | $0.59 | $0.79 | Fallback/primary for Critic, Startup Generator, Knowledge Graph per TRD §3.2 |
| Groq — Llama 3.1 8B Instant | $0.05 | $0.08 | Viable ultra-cheap option for simple extraction-style sub-tasks |

*Prices change over time and should be re-verified against the provider pricing pages (ai.google.dev/gemini-api/docs/pricing and groq.com/pricing) before any budget decision is finalized — treat every number in this document as a snapshot, consistent with the "pattern not permanent contract" framing in TRD §3.3.*

---

## 3. Cost Per Research Run (Worked Example)

This estimates token usage for one **full Deep Research run** with all optional stages enabled (Market Analysis, Startup Concepts, Tech Architecture) — the most expensive configuration, used here deliberately as a conservative upper bound rather than a best-case number.

### 3.1 Estimated Token Usage Per Agent Call

| Agent | Est. Input Tokens | Est. Output Tokens | Model Assumed |
|---|---|---|---|
| Planner | 1,500 | 500 | Gemini 2.5 Flash |
| Research (per source batch, ×3 source categories) | 4,000 ×3 | 1,200 ×3 | Gemini 2.5 Flash |
| Fact Checker | 6,000 | 1,500 | Gemini 2.5 Flash |
| Critic | 5,000 | 1,200 | Groq Llama 3.3 70B |
| Data Analyst | 3,000 | 800 | Gemini 2.5 Flash |
| Knowledge Graph | 3,500 | 1,000 | Groq Llama 3.3 70B |
| Business Analyst | 4,500 | 1,200 | Gemini 2.5 Flash |
| Startup Generator | 4,000 | 1,500 | Groq Llama 3.3 70B |
| Technical Architect | 4,000 | 1,800 | Gemini 2.5 Flash |
| Report Writer | 8,000 | 3,000 | Gemini 2.5 Flash |
| Evaluator | 5,000 | 600 | Gemini 2.5 Flash |
| **Totals** | **~56,500 input** | **~17,300 output** | mixed |

*(Memory Agent excluded — embedding cost, not chat-completion cost, modeled separately in §3.3.)*

### 3.2 Cost Calculation

Splitting by provider:

**Gemini 2.5 Flash share** (Planner, Research, Fact Checker, Data Analyst, Business Analyst, Technical Architect, Report Writer, Evaluator):
- Input: ~38,000 tokens × $0.30/1M = **$0.0114**
- Output: ~12,000 tokens × $2.50/1M = **$0.0300**

**Groq Llama 3.3 70B share** (Critic, Knowledge Graph, Startup Generator):
- Input: ~12,500 tokens × $0.59/1M = **$0.0074**
- Output: ~3,700 tokens × $0.79/1M = **$0.0029**

**Total estimated cost per full Deep Research run: approximately $0.052 (≈ 5.2 cents) at paid, non-free rates.**

This is a per-run estimate using mid-range token assumptions; real-world variance of 2–3x in either direction is normal depending on query complexity and source volume — treat this as an order-of-magnitude planning number, not an invoice-grade figure.

### 3.3 Memory Agent (Embedding) Cost

Embedding cost is priced separately and is typically an order of magnitude cheaper than chat completion per token. For planning purposes, assume embedding cost adds **less than $0.002 per session** — small enough to round into general infrastructure overhead rather than track per-run. *(Verify current embedding endpoint pricing at build time, since this document's main pricing search focused on chat-completion models, consistent with how the TRD flags this same model as needing verification at build time.)*

### 3.4 Daily Assistant Mode Cost (for comparison)

A single Daily Assistant exchange (no multi-agent pipeline, FR-1.3) — assume ~1,000 input / 500 output tokens on Gemini 2.5 Flash:
- Input: $0.0003, Output: $0.00125 → **~$0.0016 per message**, roughly 30x cheaper than a full Deep Research run. This gap is the financial justification for keeping the two modes architecturally separate (App Flow §3.5–3.6) rather than routing every chat through the heavy pipeline.

---

## 4. Where the Free Tier Actually Breaks

TRD §3.1 already states free tiers are rate-limited, not unlimited. Here is what that means numerically:

- A single Deep Research run makes roughly 12+ separate model calls across the pipeline (one per agent, more if Research Agent's 3 source-category calls are counted separately, plus retries).
- OpenRouter's free-tier pattern of roughly 200 requests/day per model (TRD §3.3) means, in the worst case of relying on a single free model for everything, **fewer than 17 full Deep Research runs per day** before that model's free quota is exhausted — before even accounting for other users or retries.
- Spreading calls across the 3-provider fallback chain (Gemini free tier + Groq free tier + OpenRouter free tier) multiplies effective free capacity roughly 3x, but each provider's own daily/per-minute cap still applies independently, and free-tier Pro-equivalent models are increasingly restricted (Gemini's free tier, for instance, no longer includes Pro-tier models as of April 2026 per current Google pricing pages — only Flash and Flash-Lite remain free).

**Practical implication:** the free-tier stack is genuinely sufficient for a final-year academic demo (low concurrent users, bursty not sustained usage, per Implementation Plan Phase 6 demo context) but will not survive even modest sustained daily usage from a real user base without moving to paid API tiers. This is not a flaw in the plan — it is exactly the kind of fact a cost model exists to surface before it becomes a production incident rather than after.

---

## 5. Monthly Cost Projection at Scale

Using the $0.052/run estimate from §3.2, scaled to different usage levels (paid-tier rates, since this is the regime that matters once free-tier ceilings in §4 are hit):

| Scenario | Deep Research runs/month | Daily Assistant messages/month | Estimated Monthly LLM Cost |
|---|---|---|---|
| Final-year demo / early beta | 200 | 2,000 | ~$10.40 + ~$3.20 = **~$13.60** |
| Small real user base (50 active users) | 1,500 | 20,000 | ~$78 + ~$32 = **~$110** |
| Growing product (500 active users) | 15,000 | 200,000 | ~$780 + ~$320 = **~$1,100** |

These figures cover **LLM API cost only.** They exclude:
- Qdrant Cloud, Neo4j Aura, Supabase usage beyond free tiers at higher scale (each has its own paid-tier pricing that should be modeled separately once approaching their free-tier limits).
- Hosting (Render/Cloudflare) beyond free tiers.
- Any human cost (support, moderation, the security monitoring described in the Security & Threat Model).

*[Note: these are planning-grade estimates built from a single worked example, not a substitute for instrumented, real production telemetry — TRD §6's "continuous evaluation" principle applies here too: replace these projections with actual measured per-run cost as soon as real usage data exists, rather than continuing to plan against this estimate indefinitely.]*

---

## 6. Cost Optimization Levers (Available Before Raising Prices)

Each of these is a concrete way to reduce the §3 cost-per-run figure, roughly in order of impact-to-effort ratio:

1. **Batch API discounts** — Gemini and Groq both offer ~50% discounts for asynchronous, non-latency-sensitive processing. Any agent step that doesn't need to stream to the user in real time (e.g., Knowledge Graph extraction, which isn't shown live in the Pipeline Running dashboard's primary view) is a batch-API candidate.
2. **Prompt caching** — system prompts and repeated context (e.g., the agent role instructions sent on every call) can be cached at roughly 10% of standard input cost on both Gemini and Groq. Since every one of the 12 agents sends a similar instructional preamble on every call, this is a high-leverage, low-effort optimization to implement early rather than as an afterthought.
3. **Model right-sizing** — not every agent needs Gemini 2.5 Flash. Simple extraction/classification-style sub-tasks (e.g., a piece of the Knowledge Graph Agent's entity-tagging work) can run on Gemini 2.5 Flash-Lite ($0.10/$0.40) or Groq's Llama 3.1 8B ($0.05/$0.08) at a fraction of the cost, reserving the stronger models for genuinely reasoning-heavy steps (Critic, Business Analyst, Technical Architect).
4. **Optional-stage gating** — the Query Composer toggles (App Flow §3.6) already let users skip Market Analysis/Startup Gen/Tech Architecture; this is already a cost lever by design, not just a UX nicety, and should be described to users in exactly those terms ("skipping unneeded stages keeps your research faster and your quota usage lower").
5. **Caching repeated research topics** — if multiple users research overlapping topics, cached/shared source retrieval (not full report caching, which would defeat personalization) can reduce redundant Research Agent calls.

---

## 7. Toward a Sustainable Pricing Model (Future, Post-Academic-Stage)

This section is explicitly forward-looking and **out of scope for the final-year deliverable itself** — included because the user explicitly framed this project as intended for real future users, and a cost model without at least a sketch of monetization would leave that goal unaddressed.

| Tier (illustrative, not finalized) | What it includes | Reasoning |
|---|---|---|
| Free | Daily Assistant Mode (rate-limited), small number of Deep Research runs/month | Matches guest/registered-user quota structure already defined in Backend Schema §2.1 |
| Individual paid | Higher Deep Research quota, priority queue (less affected by free-tier provider rate limits since paid API tiers are used) | At ~$0.05–0.15/run fully loaded cost (§3.2 plus margin for non-LLM infra), a price point in the range of other prosumer AI tools is plausible — exact pricing requires market research and is explicitly not decided here |
| Team/Enterprise | Multi-user workspaces (Phase 2 backlog per TRD §9), higher rate limits, dedicated support | Standard SaaS tiering pattern; revisit once core product-market fit is validated, not before |

**This pricing sketch is not a commitment and has not been validated against willingness-to-pay data.** It exists so the team has a directional answer if asked "how would this make money," consistent with treating the product seriously rather than leaving monetization as an afterthought — but it should not be presented to investors or users as a finalized plan without actual market validation.

---

## 8. Summary: What to Tell a Technical Reviewer

"Our free-tier stack is sufficient for the academic demo and early low-volume use, validated against current published API pricing as of June 2026. We've calculated that a full multi-agent research run costs approximately 5 cents at standard paid rates, identified specific optimization levers (batching, caching, model right-sizing) that can reduce that further, and know numerically where the free tier's ceiling is rather than assuming it doesn't exist. That's the difference between 'we hope this stays free' and 'we've done the unit economics.'"
