# Privacy Policy & Terms of Service

**Product:** AMRS — Autonomous Multi-Agent Research Scientist & Startup Intelligence Platform
**Version:** 1.0 (Draft)
**Date:** June 2026
**Status:** Draft — Requires Legal Review Before Public Launch

---

## Important Notice Before Use

**This document is drafted to be consistent with the data handling commitments already specified in the Backend Schema document (§6, Data Retention and Privacy) and the technical controls in the Security & Threat Model.** It is written by the engineering/product team to a professional standard, but it is not a substitute for review by a qualified lawyer before this product is made available to real users beyond an academic demo context. Specific gaps requiring legal review are flagged inline throughout this document. Treat this as a strong, accurate first draft — not a final, signed-off legal instrument.

---

# Part A: Privacy Policy

## A.1 What This Policy Covers

This Privacy Policy explains what information AMRS collects, how it is used, how long it is kept, and what control users have over it. It applies to both Daily Assistant Mode and Deep Research Mode, and to both registered users and guests.

## A.2 Information We Collect

| Category | What's collected | Why |
|---|---|---|
| Account information | Email address, OAuth provider identity (e.g., Google account ID), authentication tokens | To create and secure your account |
| Usage content | Chat messages (Daily Assistant), research queries, uploaded documents, generated reports | To provide the core service |
| Derived data | Embeddings of your research sessions, entity/relationship data extracted into the knowledge graph | To power semantic search over your own past sessions (Memory Agent) |
| Technical metadata | IP address, timestamps, which agent/provider served a given request, error logs | Security, abuse prevention, and reliability monitoring (Security & Threat Model §6) |
| Guest usage | Session-scoped only; not persisted beyond the active browser session | Per Backend Schema §6 — guest interactions are not stored after the session ends |

**We do not collect** payment information in v1 (no paid tier exists at this stage), biometric data, or precise location data.

## A.3 How We Use Your Information

- To operate the service: running your research queries through the agent pipeline, storing your session history, enabling search over your past sessions.
- To maintain security and reliability: rate limiting, abuse detection, and the monitoring described in the Security & Threat Model.
- To improve the product: in aggregate, anonymized form only (e.g., "the Fact Checker agent's accuracy on golden-dataset category X this month"), never by reviewing your specific session content for this purpose without separate, explicit consent.

## A.4 What We Do Not Do

- **We do not use your research session content, uploaded documents, or chat messages to train or fine-tune any AI model, without your explicit, separately-recorded opt-in.** This matches the non-functional requirement already stated in PRD §8 and Backend Schema §6, made into an actual user-facing commitment here.
- We do not sell user data to third parties.
- We do not share your specific research content with other users, regardless of whether your topic overlaps with theirs.

*[Legal review flag: if a future paid tier or enterprise offering introduces any data-sharing arrangement with model providers beyond standard API processing, this section must be updated and users re-notified before that change takes effect.]*

## A.5 Third-Party Processors

Your data passes through the following categories of third-party infrastructure to make the product work. We choose providers based on their own stated security and privacy practices, but we do not control their internal policies directly:

| Category | Examples (per TRD §5) | What they process |
|---|---|---|
| LLM providers | Google (Gemini), Groq, OpenRouter, DeepSeek | Your query text and retrieved source content, to generate agent outputs |
| Database/hosting | Supabase, Qdrant Cloud, Neo4j Aura, Render, Cloudflare | Stored account data, session content, embeddings, and graph data |
| Academic source APIs | arXiv, Semantic Scholar, PubMed, Crossref | Receive your search terms when the Research Agent queries them, not your account identity |

*[Legal review flag: confirm each provider's data processing terms are compatible with the commitments in this policy — particularly whether any free-tier provider's terms permit them to log or use submitted prompts to improve their own models, which would need to be disclosed here explicitly if true. The OpenRouter free-tier model agreements, for example, have varied by individual model on this point and should be checked at integration time, not assumed.]*

## A.6 Data Retention

- Registered user research sessions are retained until the user deletes them or deletes their account.
- Guest sessions are not retained beyond the active browser session (Backend Schema §6).
- Audit logs (Backend Schema §2.10) record that a deletion occurred, not the deleted content itself, and are retained for a limited period for security/abuse-investigation purposes.
- Upon account deletion, associated `research_sessions`, `agent_runs`, `sources`, `claims`, `critic_notes`, `startup_concepts`, `reports`, and vector store entries are deleted within a defined window (target: 30 days, to allow for backup rotation cycles — *[legal review flag: confirm this window meets applicable regulatory requirements for your eventual user base's jurisdictions, e.g., GDPR's "without undue delay" standard if EU users are in scope]*).

## A.7 Your Rights and Controls

- **Access:** you can view all your stored research sessions via the Saved Library (App Flow §3.9).
- **Deletion:** you can delete individual sessions or your entire account via Account Settings (App Flow §3.10).
- **Export:** reports are exportable as PDF/DOCX (PRD FR-2.9); a full account data export option is a near-term roadmap item, not yet implemented in v1.
- **Correction:** you can edit your account profile information directly; research session content itself is not user-editable post-generation but can be deleted and re-run.

*[Legal review flag: if launching to users in jurisdictions with specific statutory rights (GDPR's right to portability and erasure, CCPA's right to know/delete), confirm the mechanisms above satisfy the specific procedural requirements — e.g., response time limits — of those regimes before claiming compliance.]*

## A.8 Children's Privacy

AMRS is not directed at, marketed to, or knowingly used to collect data from children. *[Legal review flag: set and state an explicit minimum age (commonly 13 or 16 depending on jurisdiction) before public launch, and implement an age-gate at signup if required.]*

## A.9 Security

Technical and organizational measures protecting your data are described in the Security & Threat Model document, including encryption in transit and at rest, role-based access control, and the monitoring practices in that document's §6. No security measure eliminates all risk; in the event of a data breach affecting your information, we will notify affected users in a manner consistent with applicable law. *[Legal review flag: confirm specific breach-notification timelines required in your operating jurisdictions.]*

## A.10 Changes to This Policy

We will notify registered users of material changes to this policy (e.g., via email or an in-app notice) before the changes take effect, rather than via silent updates to this page alone.

---

# Part B: Terms of Service

## B.1 Acceptance of Terms

By creating an account or using AMRS as a guest, you agree to these Terms of Service and the Privacy Policy in Part A.

## B.2 Description of Service

AMRS provides AI-generated research synthesis, fact-checking support, business/market analysis, and technical planning content, produced by a multi-agent pipeline as described in the PRD and TRD. The service operates in two modes: Daily Assistant (general-purpose AI chat) and Deep Research (the full multi-agent pipeline).

## B.3 Not Professional Advice

**This is the most important section of these Terms and should be presented prominently in the product UI, not buried here.**

AMRS-generated content — including but not limited to market sizing estimates, startup concept suggestions, technical architecture recommendations, and any analysis of legal, medical, financial, or regulatory documents — is **AI-generated informational content, not professional advice.** Specifically:

- Market and business analysis is **not** investment, financial, or business advice and should not be relied upon as the sole basis for a business or investment decision.
- Any analysis of legal documents or contracts is **not** legal advice and does not create any attorney-client relationship; consult a licensed attorney for legal matters.
- AMRS does not provide medical, health, or clinical advice under any circumstance.
- All confidence scores and verification statuses (TRD §6, Security & Threat Model) are **heuristic indicators of relative reliability, not certifications of accuracy.** A "Verified" claim has been cross-referenced against available sources at the time of the research run — it has not been independently fact-checked by a qualified human expert in the relevant field.

## B.4 No Guarantee of Accuracy

Consistent with the engineering philosophy stated throughout the PRD and TRD: AMRS does not, and cannot, guarantee 100% accuracy, completeness, or error-free operation. No AI system — from any provider — can make that guarantee. AMRS is designed to maximize measurable reliability (Security & Threat Model, AI Evaluation & Test Plan) and to disclose uncertainty rather than hide it, but users remain responsible for independently verifying any information before relying on it for consequential decisions.

## B.5 Acceptable Use

You agree not to:
- Use AMRS to generate content for illegal purposes, or to attempt to extract harmful technical information (Security & Threat Model §4.7).
- Attempt to circumvent rate limits, quotas, or access controls (§4.3 of the Security & Threat Model).
- Upload content you do not have the legal right to upload, or that infringes a third party's intellectual property.
- Attempt to use the platform's free-tier-backed infrastructure for automated bulk scraping or resale of outputs at scale without separate written agreement.
- Attempt prompt injection, adversarial probing, or other security testing against the production system without prior written authorization (responsible disclosure of vulnerabilities found incidentally is welcomed and should be reported per §B.9).

## B.6 Intellectual Property

- You retain ownership of content you upload and of the specific research queries you submit.
- AMRS-generated reports are provided to you for your use; the underlying platform, agent architecture, prompts, and codebase remain the property of the project/company operating AMRS.
- *[Legal review flag: define explicitly whether users receive an exclusive or non-exclusive license to generated report content, particularly relevant if startup concepts or technical architectures generated by the platform are later commercialized by the user — this is a real scenario given the product's stated purpose, and should not be left ambiguous before any user generates a concept they intend to act on commercially.]*

## B.7 Service Availability

AMRS targets, but does not guarantee, the availability levels stated in PRD §8 and TRD §8 (best-effort targets on free/low-cost infrastructure, not a contractual SLA in v1). The service depends on third-party providers (TRD §3, §5) whose own availability is outside our direct control; the Model Router's fallback design (TRD §3.2) is intended to reduce, not eliminate, the impact of any single provider's outage.

## B.8 Limitation of Liability

*[Legal review flag: this section requires jurisdiction-specific legal drafting and is included here only as a placeholder reflecting standard structure, not as usable legal language.]* To the maximum extent permitted by law, the AMRS team's liability for any claim arising from use of the service is limited, and the service is provided "as is" without warranties of any kind, express or implied, regarding accuracy, fitness for a particular purpose, or non-infringement.

## B.9 Vulnerability Reporting

If you discover a security vulnerability, please report it to [project contact email] rather than disclosing it publicly, consistent with responsible disclosure practice. We will acknowledge reports and work to remediate confirmed issues, prioritized per the Security & Threat Model's likelihood/impact ratings.

## B.10 Termination

We may suspend or terminate accounts that violate §B.5, with notice where practicable except in cases of active abuse (e.g., active quota-exhaustion attacks per Security & Threat Model §4.3) where immediate suspension may be necessary to protect service availability for other users.

## B.11 Changes to These Terms

Material changes will be communicated to registered users before taking effect, consistent with Part A §A.10.

## B.12 Governing Law

*[Legal review flag: specify governing jurisdiction — this should match wherever the operating entity is legally established, and must be filled in by counsel before public launch, not assumed.]*

---

## Document Status Summary

| Section | Status |
|---|---|
| Data collection, use, retention descriptions | Accurate to current technical implementation (cross-checked against Backend Schema §6 and Security & Threat Model) |
| User rights mechanisms | Accurate to current App Flow screens |
| Sections flagged "[Legal review flag]" | **Require qualified legal review before public launch** — these are the specific points where engineering-level accuracy is not sufficient and jurisdiction-specific legal judgment is required |

This document should be re-reviewed any time the Backend Schema, Security & Threat Model, or feature set changes in a way that affects data handling — it is meant to stay synchronized with what the system actually does, not drift into aspirational language that the implementation doesn't match.
