# App Flow Document

**Product:** AMRS — Autonomous Multi-Agent Research Scientist & Startup Intelligence Platform
**Version:** 1.0
**Date:** June 2026

---

## 1. Purpose

This document maps every screen-to-screen and state transition a user experiences, for both Daily Assistant Mode and Deep Research Mode, plus the system-side pipeline flow that powers Deep Research Mode. It is the bridge between the PRD (what) and the UI/UX document (how it looks).

---

## 2. Top-Level User Flow

```
Landing Page
   │
   ├──> Sign Up / Log In (OAuth or email) ──> Onboarding (mode selector)
   │
   └──> Continue as Guest (rate-limited, Daily Assistant only)
                                  │
                                  ▼
                        ┌─────────────────┐
                        │   Home / Hub     │
                        │ (mode toggle:    │
                        │ Daily | Research)│
                        └────┬────────┬────┘
                             │        │
                  ┌──────────▼┐    ┌──▼──────────────┐
                  │  Daily      │    │  Deep Research   │
                  │  Assistant  │    │  Mode             │
                  │  Chat       │    │  Query Composer   │
                  └─────────────┘    └────────┬─────────┘
                                               │
                                     ┌──────────▼──────────┐
                                     │  Pipeline Running     │
                                     │  (Agent Monitoring     │
                                     │   Dashboard view)      │
                                     └──────────┬──────────┘
                                                │
                                     ┌──────────▼──────────┐
                                     │  Report View           │
                                     │  (sections + trace +   │
                                     │   confidence score)    │
                                     └──────────┬──────────┘
                                                │
                              ┌──────────────────┼──────────────────┐
                              ▼                  ▼                  ▼
                       Export (PDF/DOCX)   Save to Library    Ask Follow-up
                                                                (re-enters pipeline
                                                                 with prior context)
```

---

## 3. Screen-by-Screen Flow

### 3.1 Landing Page
- **Entry point** for all new visitors.
- Content: one-line value proposition, "Try as Guest" CTA, "Sign Up" CTA, brief illustration of the two modes.
- **Exit transitions:** → Sign Up/Login, → Guest Home (limited).

### 3.2 Sign Up / Login
- OAuth (Google) or email/password via Supabase Auth.
- **Exit transitions:** → Onboarding (first-time users), → Home/Hub (returning users).

### 3.3 Onboarding (first-time only)
- 2-step micro-onboarding: (1) "What will you mostly use AMRS for?" (student / founder / professional / just exploring — sets default mode), (2) short explainer of Daily vs. Deep Research mode with a visual diagram.
- **Exit transition:** → Home/Hub, with selected default mode pre-set.

### 3.4 Home / Hub
- Central screen with a persistent mode toggle (Daily Assistant ↔ Deep Research) and a sidebar showing: recent chats, saved research reports, and account/usage indicator (quota remaining for free-tier users).
- **Exit transitions:** → Daily Assistant Chat, → Deep Research Query Composer, → Saved Report (from sidebar), → Account Settings.

### 3.5 Daily Assistant Chat
- Standard chat interface: message input, streamed responses, conversation history in-session.
- No agent pipeline visualization here — this mode is intentionally lightweight (FR-1.3).
- **Exit transitions:** → Home/Hub, → switch to Deep Research (carries current question over as a pre-filled research query, with user confirmation).

### 3.6 Deep Research — Query Composer
- Large text input for the research question.
- Optional: file/PDF upload for grounding context.
- Optional toggles: "Include market analysis," "Include startup generation," "Include technical architecture" (lets advanced users skip stages they don't need — controls Planner Agent's task graph).
- "Run Research" CTA.
- **Exit transition:** → Pipeline Running screen.

### 3.7 Pipeline Running (Agent Monitoring Dashboard)
- Live view showing each agent as a node/card with status: Queued → Running → Done / Failed (Degraded).
- Underneath: a running log of intermediate findings as they complete (e.g., "Research Agent found 14 sources" appears as soon as that step finishes, before the whole pipeline is done).
- If a step fails after fallback exhaustion, its card shows "Degraded — partial result" rather than freezing the whole screen.
- **Exit transition:** automatically → Report View once Report Writer + Evaluator steps complete. User may also navigate away; the run continues server-side and notifies on completion.

### 3.8 Report View
- Structured sections matching the PRD's deliverable list: Research Summary, Fact-Check Table, Critic's Notes, Market Analysis, Startup Concepts, Technical Architecture, Roadmap.
- Confidence score and per-section coverage score displayed prominently at the top, with a tooltip explaining the score is a heuristic, not a certified accuracy measure.
- Expandable "Agent Trace" panel per section, showing which agent produced it and its raw intermediate output.
- **Exit transitions:** → Export (PDF/DOCX), → Save to Library (persists to user's account, triggers Memory Agent embedding), → Ask Follow-up (re-opens Query Composer pre-filled with context from this report), → Home/Hub.

### 3.9 Saved Library
- List of past research sessions (title, date, confidence score badge).
- **Exit transitions:** → re-open a past Report View, → delete session, → Home/Hub.

### 3.10 Account Settings
- Profile, plan/quota info, connected OAuth accounts, data/privacy controls (delete my data).
- **Exit transition:** → Home/Hub.

---

## 4. System-Side Pipeline Flow (Deep Research Mode)

This is the backend flow triggered by "Run Research" in §3.6, corresponding to the agent specs in the TRD §4.

```
1. Query received by API Gateway
2. Planner Agent builds task graph
      └─ if Planner fails → fallback to default linear pipeline (TRD §4.1)
3. Research Agent executes parallel source retrieval
4. Fact Checker Agent processes extracted claims
5. Critic Agent reviews Research + Fact Checker output
6. [Conditional, based on Query Composer toggles]
      ├─ Business Analyst Agent runs
      ├─ Startup Generator Agent runs (depends on Business Analyst output)
      └─ Technical Architect Agent runs (depends on Startup Generator output)
7. Knowledge Graph Agent extracts entities (parallel to step 6)
8. Report Writer Agent assembles all completed sections
9. Evaluator Agent scores the assembled report
10. Memory Agent embeds and stores session (async, does not block report delivery)
11. Result pushed to frontend via Server-Sent Events; Report View renders
```

Each numbered step corresponds to a node in the LangGraph state machine (TRD §2). Steps 3–7 run with the Model Router fallback logic (TRD §3.2) wrapping every model call.

---

## 5. Error and Edge-Case Flows

| Scenario | Flow |
|---|---|
| Guest user hits rate limit in Daily Assistant | Inline message + CTA to sign up; chat input disabled until quota resets or user signs up |
| Registered user hits Deep Research quota | Query Composer shows quota-exceeded state with reset time; "Run Research" CTA disabled |
| All providers in a Model Router chain fail for one agent step | That section of the report is marked "Degraded — unavailable this run," other sections proceed normally (TRD §6.3) |
| User navigates away mid-pipeline | Pipeline continues server-side; user gets an in-app notification (and optional email) when the report is ready |
| Uploaded file fails to parse | Inline error in Query Composer before pipeline starts; user can retry upload or proceed without the file |

---

## 6. Mode-Switch Behavior

Switching between Daily Assistant and Deep Research mid-session does not lose context: the current conversation/question is offered as a pre-filled starting point in the destination mode, but the user must explicitly confirm before a Deep Research pipeline run starts (since it consumes quota and takes materially longer than a chat reply).
