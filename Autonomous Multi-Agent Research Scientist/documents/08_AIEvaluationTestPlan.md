# AI Evaluation & Test Plan

**Product:** AMRS — Autonomous Multi-Agent Research Scientist & Startup Intelligence Platform
**Version:** 1.0
**Date:** June 2026
**Status:** Draft for Review

---

## 1. Purpose

The PRD and TRD both make a specific claim: AMRS's value comes from measurable reliability through cross-checking, not from claiming perfection. This document is what makes that claim verifiable rather than just well-argued. It defines how every agent is tested in isolation, how the pipeline is tested end-to-end, how AI-specific failure modes (hallucination, contradiction-blindness, injection susceptibility) are measured over time, and what evidence a faculty panel, recruiter, or future user should expect to see before trusting a report.

A system that asserts its own reliability without a test plan is making a marketing claim. A system that measures and reports its reliability is making an engineering claim. This document is what moves AMRS from the first category to the second.

---

## 2. Testing Layers Overview

| Layer | What it tests | Tooling |
|---|---|---|
| Unit tests | Individual functions: API client wrappers, schema validation, the Model Router's fallback logic itself | pytest (backend), Jest (frontend) |
| Agent-level evaluation | Each agent's output quality against a golden dataset, independent of the rest of the pipeline | Custom eval harness (this document, §4) |
| Integration tests | Multi-agent handoffs: does Critic Agent correctly receive Fact Checker's output structure | pytest with mocked LLM responses |
| End-to-end tests | Full pipeline run against known queries, checking final report structure and completion | Playwright (UI) + backend E2E suite |
| Failure-injection tests | Does the system behave correctly when a provider fails, a document is malicious, a quota is exhausted | Custom chaos scripts (this document, §6) |
| Human evaluation | Does a domain-knowledgeable human agree with the system's confidence scores and flags | Structured review protocol (this document, §5) |

Unit, integration, and end-to-end tests follow standard software engineering practice and are not elaborated further here beyond the table above — the focus of this document is the layers specific to an AI system: agent-level evaluation, human evaluation, and failure injection.

---

## 3. Why Standard Software Testing Is Not Sufficient Here

A normal CRUD endpoint either returns the right value or it doesn't — testing is deterministic. AMRS's agents produce natural-language judgments (is this claim verified? is this market gap real? is this architecture sound?) where there often isn't one single correct answer, and the same prompt can produce different output across runs. Three problems standard testing doesn't solve, and what this plan uses instead:

1. **No single ground truth for most outputs** → use a golden dataset with human-agreed labels, and measure agreement rate rather than pass/fail.
2. **Output varies run-to-run** → run each golden test case multiple times (default: 5 runs) and report a consistency rate alongside accuracy, not just one sample.
3. **Errors are often subtle, not crashes** → a hallucinated citation doesn't throw an exception; it looks like a normal, well-formatted answer. Evaluation must specifically check for this class of error, not just "did the code run without an error."

---

## 4. Agent-Level Evaluation (Golden Datasets)

Each agent with a non-trivial judgment task gets its own small, hand-curated golden dataset before it is considered ready for integration. Minimum size and composition below are deliberately achievable within a final-year timeline — these are starting benchmarks, expandable over time, not exhaustive certification suites.

### 4.1 Fact Checker Agent
- **Dataset:** 40 claims minimum — 10 clearly true (well-established, multi-source-corroborated facts), 10 clearly false, 10 genuinely contradicted-in-literature (real debates where sources disagree), 10 ambiguous/insufficiently-sourced.
- **Metric:** % of claims assigned the expected status category (`Verified` / `Contradicted` / `Unverified`). Target: ≥ 80% agreement with human-labeled expectation on the clear-true and clear-false subsets; the contradicted and ambiguous subsets are explicitly harder and tracked separately rather than averaged in, since conflating them would hide where the agent actually struggles.
- **Critical check:** false positive rate on the "clearly false" subset (claims the agent incorrectly marks Verified) is tracked as its own headline number, since this is the single most damaging failure mode for user trust.

### 4.2 Critic Agent
- **Dataset:** 15 research summaries with known, planted weaknesses (e.g., a summary with an unstated sample-size limitation, one with a logical leap, one with no actual weaknesses — a "clean" case to test for over-criticism).
- **Metric:** % of planted weaknesses correctly identified (recall), and rate of false weaknesses invented on the clean case (precision). Both reported — an agent that flags everything as risky scores well on recall and badly on precision, and both numbers matter.

### 4.3 Business Analyst Agent
- **Dataset:** 10 well-known markets with independently verifiable TAM/SAM/SOM ranges from public sources (e.g., published market research summaries).
- **Metric:** estimate falls within the same order of magnitude as the reference range, and the stated methodology/assumptions are present and coherent (this is graded qualitatively, since market sizing is inherently approximate — the test checks "is this a defensible estimate with shown reasoning," not "is this the exact right number").

### 4.4 Startup Generator Agent
- **Dataset:** 10 research topics with known existing real-world solutions.
- **Metric:** generated concepts are checked against a simple novelty/differentiation rubric — does the concept acknowledge the existing players found by the Research Agent, or does it propose something that already exists without acknowledging it (a real failure mode: regenerating an existing product as if it were a new idea).

### 4.5 Knowledge Graph Agent
- **Dataset:** 10 short texts with a manually-built reference entity-relationship graph.
- **Metric:** precision/recall on entity extraction and relationship correctness against the reference graph.

### 4.6 Evaluator Agent (meta-evaluation)
- This is the hardest agent to evaluate, since it scores the other agents' combined output. Method: for each completed golden-dataset run above, compare the Evaluator's composite confidence score against a human reviewer's independent confidence judgment on the same report (see §5). Track correlation, not exact match — the goal is that the Evaluator's score and a knowledgeable human's gut-check move in the same direction, not that they produce identical numbers.

### 4.7 Memory Agent
- **Dataset:** 10 past sessions with 10 follow-up queries that should retrieve specific prior sessions semantically (not by exact keyword match).
- **Metric:** retrieval precision@3 (is the correct prior session in the top 3 results).

---

## 5. Human Evaluation Protocol

Automated golden-dataset scoring catches regressions; it does not catch "this report is technically correct but not actually useful," which only a human reviewer notices. Minimum protocol for the final-year project:

1. Recruit 3–5 reviewers (can be teammates, faculty, or volunteer target users — students/founders from the personas in PRD §5) who did not build the system.
2. Each reviewer independently runs 3 of the PRD Appendix A example queries (or their own real questions) through the full pipeline.
3. For each report, reviewer rates on a simple 1–5 scale: *Would I trust this enough to act on it without independently re-checking the sources myself?* and separately, *Did the confidence score match my own impression after reading the report?*
4. Aggregate scores and qualitative comments inform the Phase 5 hardening pass (Implementation Plan §3, Phase 5) before the final demo.
5. Repeat this protocol at least once more after any major agent prompt change — a single round of human evaluation done once at the end is not sufficient; it should bracket any significant change to agent behavior.

This is the layer that ultimately validates (or disproves) the product's central claim. Automated scores can look good while still producing reports nobody would actually trust; this protocol exists specifically to catch that gap.

---

## 6. Failure-Injection Test Suite

This directly tests the reliability mechanisms described in TRD §6 and the Security & Threat Model — not as a one-time check during Phase 0, but as a repeatable suite run before every major milestone.

| Test ID | Scenario | Expected Behavior |
|---|---|---|
| FI-01 | Primary model provider returns a 429 rate-limit error | Model Router falls back to next provider in chain within the configured retry window; request still completes |
| FI-02 | All providers in an agent's fallback chain fail | That pipeline step returns a `degraded` status; other completed sections still reach the user; nothing hard-crashes (App Flow §5) |
| FI-03 | Uploaded PDF contains a hidden prompt-injection string (see Security & Threat Model §4.1) | Fact Checker's verification status is not flipped by the injected instruction; the dual-source verification rule holds |
| FI-04 | A research query returns zero usable sources | Research Agent reports "insufficient sources found" rather than fabricating a summary; downstream agents handle an empty input gracefully |
| FI-05 | User submits a query matching the harmful-content policy filter (Security & Threat Model §4.7) | Request is declined before any downstream agent runs; decline reason is logged |
| FI-06 | Qdrant or Neo4j free-tier quota is artificially exhausted (test environment) | Memory Agent / Knowledge Graph Agent steps degrade gracefully; core report generation still completes without them |
| FI-07 | Two independent sources directly contradict each other on the same claim | Fact Checker assigns `Contradicted`, not an averaged or silently-resolved status; both sources are shown to the user |
| FI-08 | A single source is used to support a claim (no second corroborating source available) | Status is `Partially Verified` or `Unverified`, never `Verified` — the dual-source rule is enforced, not bypassed when convenient |

Each test ID above should map to an actual automated or manually-rehearsed test case before the Phase 6 demo (Implementation Plan §3) — and per the Implementation Plan's own guidance, deliberately demonstrating FI-01 or FI-02 live in the demo is a stronger credibility signal than only showing the happy path.

---

## 7. Regression Tracking

- Every agent's golden-dataset score (§4) is re-run and logged whenever its prompt, model assignment, or upstream dependency changes — a simple spreadsheet or lightweight dashboard tracking score-over-time per agent is sufficient for this project's scale.
- A score drop of more than 10 percentage points on any golden dataset after a change blocks merging that change until investigated — this is the AI-system equivalent of "don't merge code that fails CI."

---

## 8. What "Done" Looks Like for This Plan

By the end of Phase 5 (Implementation Plan), the team should be able to produce, on request:

1. Current golden-dataset scores for all seven agents in §4, with the false-positive rate for the Fact Checker called out specifically.
2. Human evaluation results from at least one full round (§5).
3. A completed failure-injection run log showing all eight scenarios in §6 behaving as expected.
4. A short written summary translating these results into the same honest framing used throughout the rest of this document set: specific, measured reliability numbers — not a claim of perfection, but evidence of engineering rigor that a technical reviewer can actually verify rather than just take on faith.
