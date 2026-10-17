# Backend Schema Document

**Product:** AMRS — Autonomous Multi-Agent Research Scientist & Startup Intelligence Platform
**Version:** 1.0
**Date:** June 2026

---

## 1. Purpose

This document defines the relational schema (PostgreSQL via Supabase), vector store schema (Qdrant), knowledge graph schema (Neo4j), and core API contracts. It implements the data model implied by the TRD's agent specifications and the App Flow's screen requirements.

---

## 2. Relational Schema (PostgreSQL)

### 2.1 `users`
| Column | Type | Notes |
|---|---|---|
| id | uuid, PK | |
| email | text, unique | |
| auth_provider | text | 'email', 'google', 'guest' |
| role | text | 'guest', 'registered', 'admin' |
| created_at | timestamptz | |
| default_mode | text | 'daily', 'research', set during onboarding |
| quota_research_runs_remaining | integer | resets on a rolling window job |
| quota_reset_at | timestamptz | |

### 2.2 `projects`
A `project` groups related research sessions (e.g., all sessions for one thesis topic).
| Column | Type | Notes |
|---|---|---|
| id | uuid, PK | |
| user_id | uuid, FK → users.id | |
| title | text | |
| created_at | timestamptz | |

### 2.3 `research_sessions`
| Column | Type | Notes |
|---|---|---|
| id | uuid, PK | |
| project_id | uuid, FK → projects.id, nullable | session may be standalone |
| user_id | uuid, FK → users.id | |
| query_text | text | original user query |
| toggles | jsonb | which optional stages were requested, e.g. `{"market_analysis": true, "startup_gen": true, "tech_arch": false}` |
| status | text | 'queued', 'running', 'completed', 'degraded', 'failed' |
| confidence_score | integer, nullable | 0–100, set by Evaluator Agent on completion |
| created_at | timestamptz | |
| completed_at | timestamptz, nullable | |

### 2.4 `agent_runs`
One row per agent invocation within a session — this is what powers the Agent Monitoring Dashboard and Agent Trace panels.
| Column | Type | Notes |
|---|---|---|
| id | uuid, PK | |
| session_id | uuid, FK → research_sessions.id | |
| agent_role | text | 'planner', 'research', 'fact_checker', 'critic', 'data_analyst', 'knowledge_graph', 'business_analyst', 'startup_generator', 'technical_architect', 'report_writer', 'evaluator', 'memory' |
| status | text | 'queued', 'running', 'done', 'degraded', 'failed' |
| provider_used | text, nullable | which model provider actually served this call, e.g. 'gemini', 'groq', 'openrouter' |
| fallback_used | boolean | true if the primary provider failed and a fallback served the request |
| started_at | timestamptz, nullable | |
| completed_at | timestamptz, nullable | |
| raw_output | jsonb | full structured agent output, surfaced in the Trace panel |
| error_detail | text, nullable | populated when status = 'degraded' or 'failed' |

### 2.5 `sources`
| Column | Type | Notes |
|---|---|---|
| id | uuid, PK | |
| session_id | uuid, FK → research_sessions.id | |
| title | text | |
| url | text | |
| source_type | text | 'arxiv', 'semantic_scholar', 'pubmed', 'crossref', 'web' |
| published_date | date, nullable | |
| retrieved_at | timestamptz | |

### 2.6 `claims`
Output of the Fact Checker Agent (FR-2.4 / TRD §4.3).
| Column | Type | Notes |
|---|---|---|
| id | uuid, PK | |
| session_id | uuid, FK → research_sessions.id | |
| claim_text | text | |
| verification_status | text | 'verified', 'partially_verified', 'unverified', 'contradicted' |
| supporting_source_ids | uuid[] | array of `sources.id` |
| conflicting_source_ids | uuid[] | array of `sources.id`, empty unless contradicted |

### 2.7 `critic_notes`
| Column | Type | Notes |
|---|---|---|
| id | uuid, PK | |
| session_id | uuid, FK → research_sessions.id | |
| note_type | text | 'assumption', 'gap', 'risk' |
| content | text | |
| severity | text | 'low', 'medium', 'high' |

### 2.8 `startup_concepts`
| Column | Type | Notes |
|---|---|---|
| id | uuid, PK | |
| session_id | uuid, FK → research_sessions.id | |
| rank | integer | 1, 2, or 3 |
| name | text | |
| target_user | text | |
| monetization_model | text | |
| differentiator | text | |

### 2.9 `reports`
The final assembled, exportable artifact.
| Column | Type | Notes |
|---|---|---|
| id | uuid, PK | |
| session_id | uuid, FK → research_sessions.id, unique | one report per session |
| content_markdown | text | canonical internal format |
| pdf_export_url | text, nullable | generated on demand, cached |
| docx_export_url | text, nullable | generated on demand, cached |

### 2.10 `audit_logs`
| Column | Type | Notes |
|---|---|---|
| id | uuid, PK | |
| user_id | uuid, FK → users.id, nullable | nullable for system events |
| action | text | e.g. 'session_created', 'export_requested', 'data_deleted' |
| metadata | jsonb | |
| created_at | timestamptz | |

---

## 3. Vector Store Schema (Qdrant)

### Collection: `session_embeddings`
| Field | Type | Notes |
|---|---|---|
| id | uuid (matches `research_sessions.id`) | |
| vector | float[768] (or current Gemini embedding dimension — verify at build time) | |
| payload.user_id | uuid | for filtered semantic search per user |
| payload.session_title | text | |
| payload.summary | text | short summary used for retrieval preview |
| payload.created_at | timestamptz | |

### Collection: `source_chunks`
Used for RAG grounding when a user uploads a PDF for context.
| Field | Type | Notes |
|---|---|---|
| id | uuid | |
| vector | float[768] | |
| payload.session_id | uuid | |
| payload.chunk_text | text | |
| payload.source_filename | text | |
| payload.chunk_index | integer | |

---

## 4. Knowledge Graph Schema (Neo4j)

### Node Labels
- `(:Topic {name})`
- `(:Entity {name, type})` — type ∈ {organization, technology, concept, person}
- `(:Source {url, title})`
- `(:Session {id})`

### Relationship Types
- `(:Entity)-[:RELATES_TO {description}]->(:Entity)`
- `(:Entity)-[:MENTIONED_IN]->(:Source)`
- `(:Session)-[:PRODUCED]->(:Entity)`
- `(:Topic)-[:HAS_ENTITY]->(:Entity)`

This schema is intentionally kept minimal for v1 scope (TRD §4.6) — sufficient for visualizing entity relationships per session without over-engineering a general-purpose graph model.

---

## 5. Core API Contracts (FastAPI)

### `POST /api/v1/research/sessions`
Creates a new research session and starts the pipeline.
```json
// Request
{
  "query_text": "What are the latest AI applications in precision agriculture?",
  "toggles": { "market_analysis": true, "startup_gen": true, "tech_arch": false },
  "project_id": "uuid | null"
}

// Response (202 Accepted)
{
  "session_id": "uuid",
  "status": "queued"
}
```

### `GET /api/v1/research/sessions/{session_id}/status`
Polled or subscribed via SSE by the Agent Monitoring Dashboard.
```json
{
  "session_id": "uuid",
  "status": "running",
  "agents": [
    { "agent_role": "planner", "status": "done", "fallback_used": false },
    { "agent_role": "research", "status": "running", "fallback_used": false },
    { "agent_role": "fact_checker", "status": "queued" }
  ]
}
```

### `GET /api/v1/research/sessions/{session_id}/report`
Returns the assembled report once available.
```json
{
  "session_id": "uuid",
  "confidence_score": 78,
  "sections": {
    "research_summary": "...",
    "fact_check_table": [
      { "claim": "...", "status": "verified", "supporting_sources": ["..."], "conflicting_sources": [] }
    ],
    "critic_notes": [
      { "type": "gap", "content": "...", "severity": "medium" }
    ],
    "market_analysis": { "tam_estimate": "...", "competitors": ["..."] },
    "startup_concepts": [ { "rank": 1, "name": "...", "monetization_model": "..." } ],
    "technical_architecture": "...",
    "roadmap": "..."
  },
  "degraded_sections": []
}
```

### `POST /api/v1/chat/daily`
Lightweight single-call endpoint for Daily Assistant Mode (FR-1.1–1.3) — deliberately separate from the research pipeline endpoints to keep this path fast and cheap.
```json
// Request
{ "message": "Explain transformers to me simply", "conversation_id": "uuid | null" }

// Response (streamed via SSE)
{ "delta": "Transformers are a neural network architecture..." }
```

### `GET /api/v1/sessions/search?q=...`
Semantic search over past sessions via the Memory Agent (FR-3.2), backed by Qdrant `session_embeddings`.

---

## 6. Data Retention and Privacy

- `raw_output` in `agent_runs` and full chat history are retained per the user's account but deletable on request (`audit_logs` records the deletion event, not the deleted content).
- Guest sessions (`auth_provider = 'guest'`) are not persisted beyond the active browser session — no `research_sessions` row is created for guest users; Daily Assistant only, per PRD FR scope.
- No session content is used to train or fine-tune any model without explicit, separately-recorded user opt-in (PRD §8 NFR).
