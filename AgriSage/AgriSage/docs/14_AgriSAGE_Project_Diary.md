# Agri-SAGE Project Diary

**Project:** Agri-SAGE — Scalable Agricultural Guidance Engine  
**Repository:** m4gnel/AgriSage  
**Branch:** main  
**Diary created:** 2026-10-01  
**Purpose:** Maintain a human-readable engineering history of the project's architecture, implementation decisions, major milestones, verification notes, and next actions.

> **Accuracy rule:** This diary records what is documented or present in the repository. Items marked **Planned** are not treated as completed merely because they appear in specifications.

---

## 2026-10-01 — Repository Review & Project Baseline

### What was verified

The repository is structured as a multi-surface agricultural decision-intelligence platform.

Top-level architecture currently includes:

- `apps/` — application surfaces
- `backend/` — backend/domain architecture
- `brain/` — project intelligence/agent-oriented area
- `docs/` — formal project specifications and engineering documents
- `public/` — public/static web assets
- `.agents/` — agent skills/configuration area
- `.github/workflows/` — CI/CD workflow area
- root-level Docker, environment, package, licensing, and architecture files

The README describes Agri-SAGE as an **offline-first, simulation-grounded, multi-agent agricultural decision intelligence platform** for smallholder farmers, extension officers, and agronomists.

### Core product concept

Agri-SAGE combines:

1. Multimodal image/sensor inputs
2. On-device/edge ML
3. Physics-based crop simulation using DSSAT
4. CIB&RC-based chemical safety validation
5. Calibrated confidence states
6. Agricultural knowledge retrieval
7. Regional-language presentation
8. Farmer-facing and expert-facing workflows

### Presentation surfaces

The documented product split is:

- **Expert Web Workstation:** `apps/web-expert/`
- **Farmer Mobile Application:** `mobile/`

The README and architecture documents describe the expert surface as an agronomist/extension workflow and the mobile surface as a low-spec, intermittent-connectivity farmer workflow.

---

# Phase 1 — Product Definition

## Product requirements

The repository contains a formal documentation set covering:

- Product Requirements Document
- Technical Requirements Document
- Application Flow
- UI/UX Specification
- Backend Schema
- Implementation Plan
- Security & Compliance
- AI Prompt Handbook
- Testing & QA Playbook
- Validation Report
- Master Build Guide
- Team Sprint Plan
- Version Update Report

These documents form the project's specification layer and should remain the source of truth when implementation questions arise.

### Engineering principle

The project is not intended to behave like a generic chatbot. Its documented architecture emphasizes evidence, deterministic safety checks, simulation, confidence calibration, and traceable agricultural knowledge.

---

# Phase 2 — Architecture Decisions

## ADR-001 — Dual-surface architecture

**Decision:** Separate expert and farmer experiences.

### Expert surface

`apps/web-expert/`

Responsibilities documented for this surface include:

- Expert review
- Diagnosis triage
- Evidence inspection
- Chemical verification
- Simulation exploration
- Outbreak monitoring
- Knowledge browsing

### Mobile surface

`mobile/`

Responsibilities documented for this surface include:

- Farmer onboarding
- Camera diagnostics
- Offline cache
- Voice interaction
- Morning briefings
- Field-oriented advisory workflows

### Reason recorded

The architecture avoids forcing expert workflows onto small mobile displays while also avoiding the overhead of putting dense expert functionality into the farmer experience.

---

# Phase 3 — Backend Architecture

The repository currently contains the following backend domains:

```
backend/
├── agents/
├── api/
├── config.py
├── data/
├── database.py
├── dependencies.py
├── knowledge/
├── main.py
├── ml/
├── safety/
├── services/
└── simulation/
```

### Intended responsibilities documented by the project

**agents/**  
Multi-agent agricultural reasoning components.

**api/**  
Versioned REST API surface for authentication, diagnosis, risk, schemes, simulation, expert workflows, and related operations.

**data/**  
Agricultural schemas and reference datasets such as crop-stage/GDD information, disease classes, and language dictionaries.

**knowledge/**  
Agricultural knowledge ingestion and retrieval, including ICAR/KAU-oriented sources and hybrid retrieval.

**ml/**  
ONNX-based vision/model pipelines and training-related code.

**safety/**  
Chemical safety blocking and hallucination/safety detection mechanisms.

**services/**  
Shared application services such as LLM integration, embeddings, image security, and briefing functionality.

**simulation/**  
DSSAT adapters and scenario-generation functionality.

---

# Phase 4 — Agricultural Intelligence Architecture

## Multi-agent approach

The project documentation specifies a multi-agent LangGraph architecture.

The README describes a **14-agent architecture**, while the public-facing scrollytelling documentation highlights a simplified visual constellation of six specialized agent roles.

The six roles explicitly represented in the visual architecture are:

1. Vision
2. Weather
3. GDD Phenology
4. DSSAT
5. CIB&RC Critic
6. Vernacular Voice

These visual roles should be understood as a presentation-level representation rather than evidence that only six agents exist in the full architecture.

## Evidence-oriented reasoning

The intended advisory pipeline combines:

```
Raw Data
   ↓
AI / Agent Processing
   ↓
Crop & Phenology Context
   ↓
Weather / Risk Context
   ↓
DSSAT Simulation
   ↓
CIB&RC Safety Validation
   ↓
Actionable Advisory
```

The architecture explicitly aims to prevent unsupported agricultural recommendations.

---

# Phase 5 — Safety & Regulatory Design

Safety is treated as a core architectural requirement rather than an optional feature.

## CIB&RC validation

The documented rule is that pesticide/fungicide/fertilizer recommendations should expose official registration/status information and validated usage information.

The system is designed to block or warn against unsafe chemical recommendations.

## DSSAT disclaimer

The architecture requires model-derived yield or simulation values to be presented as:

`* Modelled estimate`

This prevents a simulated value from being presented as a guaranteed real-world outcome.

## Government scheme disclaimer

Government agricultural scheme information is intended to include an eligibility caveat stating that final eligibility is determined by the relevant authority.

## Confidence calibration

The project specifies seven discrete confidence states rather than exposing an unexplained raw percentage.

Documented states include:

- CONFIRMED
- LIKELY
- POSSIBLE
- UNCERTAIN
- INSUFFICIENT_DATA
- CONFLICTING_EVIDENCE
- OUT_OF_SCOPE

---

# Phase 6 — Web Expert Workstation

## Documented technology direction

The architecture decision record specifies:

- React
- TypeScript
- Vite
- Lucide React
- CSS design tokens
- Noto Sans / Noto Sans Malayalam
- Responsive expert-oriented layouts

The repository's current root package manifest also contains modern React/Three.js/GSAP/Motion-related dependencies supporting the current visual experience.

## Planned/defined expert modules

The architecture document describes:

### Dashboard

Expert diagnosis queue and daily triage.

### Review Detail

Deep diagnosis inspection and expert override workflow.

### Advisory Sandbox

Farmer-advisory simulation/testing surface.

### Outbreak Radar

Regional disease/pest visualization.

### Knowledge Browser

ICAR/KAU-oriented agricultural knowledge explorer.

---

# Phase 7 — 3D Scrollytelling Experience

A major documented implementation milestone is the evolution of the public web experience into a 3D, scroll-driven agricultural intelligence story.

## Chapter structure

The repository documentation describes a 12-chapter experience:

### Chapter 01 — Hero

Introduces Agri-SAGE through an immersive agricultural/digital-twin visual system.

### Chapter 02 — The Problem

Human visual inspection versus machine-assisted agricultural sensing.

### Chapter 03 — The Farm 360°

Interactive farm layers representing satellite, weather, soil, irrigation, sensors, and farmer context.

### Chapter 04 — See The Invisible

Microscopic/spectral visualization explaining hidden crop signals.

### Chapter 05 — Neural Pipeline

Shows the transformation of raw agricultural information into structured intelligence.

### Chapter 06 — Multi-Agent Constellation

Visualizes specialized agricultural agents collaborating.

### Chapter 07 — Crop Simulation Studio

Introduces DSSAT scenario modelling and time-horizon comparisons.

### Chapter 08 — Predict → Prevent → Protect

Shows the intended risk-management narrative.

### Chapter 09 — Farmer Advisory

Connects system intelligence to a farmer-facing advisory experience, including regional-language/voice concepts.

### Chapter 10 — Global Network

Visualizes geographically distributed agricultural intelligence.

### Chapter 11 — Platform Console

Transitions toward the expert workstation.

### Chapter 12 — Final CTA

Concludes the public experience and directs the user toward the platform.

---

# Phase 8 — Motion & Interaction Engineering

The repository's architectural notes document several custom interaction systems.

## Scroll snapping

The public experience uses native CSS scroll snapping with:

- `scroll-snap-type`
- `scroll-snap-align`
- `scroll-snap-stop`

The project documentation explicitly avoids adding a heavy carousel/slider dependency for this behavior.

## ScrollTrigger-style chapter activation

Layered chapter elements are documented with staged reveal timing.

The project uses intersection-based activation to coordinate chapter transitions.

## Parallax engine

A custom parallax hook is documented with multiple speed layers.

The system supports:

- Y movement
- X movement
- Combined movement
- Rotation
- Contra-parallax
- Reduced-motion accessibility behavior

## Scroll-driven image sequence

The project documents an Apple-style scroll-scrubbed image sequence.

The documented sprout sequence contains five growth frames:

1. Seed emergence
2. Cotyledon stage
3. Leaf expansion
4. Vegetative growth
5. Full canopy

The sequence is rendered through a canvas and mapped to scroll progress.

---

# Phase 9 — Dewdrop Visual System

A central visual metaphor documented in the project is a luminous agricultural water droplet.

## Purpose

The dewdrop acts as a continuous visual guide through the long-form experience.

## Technical elements documented

- Scroll progress tracking
- Spring/lerp smoothing
- Intersection Observer
- Sticky viewport positioning
- Kinetic typography
- Programmatic waypoint mapping
- Multi-body viscosity simulation
- SVG liquid refraction
- Canvas ripple/caustic effects
- Sinuous X/Y trajectory
- Motion-vector alignment
- Trailing daughter droplets

## Accessibility

The documented motion architecture includes `prefers-reduced-motion: reduce` handling.

---

# Phase 10 — Authentication Experience

The project documentation describes a dual-role authentication concept.

## Farmer path

The documented experience includes:

- Phone OTP
- Six-digit input
- Expiration countdown
- Development/demo fast path

## Agronomist path

The documented concept includes:

- Institutional email/key validation
- ICAR/CIB&RC compliance context
- Enterprise-oriented verification

## Passkey concept

A FIDO2/WebAuthn biometric/passkey flow is documented as a passwordless security concept.

---

# Phase 11 — Design System

The architecture documentation specifies a token-based visual system.

## Core visual direction

The documented primary palette uses agricultural forest-green tones.

Risk states are differentiated into critical/high/medium/low levels.

Confidence states are visually distinct and are intended to be paired with text/icons so that color is not the only semantic signal.

## Typography

The project specifies Noto Sans and Noto Sans Malayalam to maintain consistent rendering across English and regional-language interfaces.

## Accessibility targets

Documented targets include:

- Minimum 48px interactive touch targets
- 4.5:1 text contrast
- Semantic status indicators
- Keyboard accessibility
- WCAG 2.1 AA intent

---

# Phase 12 — Quality & Verification Targets

The architecture roadmap defines quality gates including:

- Strict TypeScript checking
- Zero console errors
- Lighthouse performance target above 95 for desktop
- Fast first-contentful paint
- Keyboard navigation
- ARIA support
- Localization integrity
- Reduced-motion support

The repository documentation contains several statements of browser/build verification for portions of the visual implementation.

**Important:** These statements are recorded as project documentation claims; they are not independently re-run by this diary.

---

# Phase 13 — Current Repository Engineering State

At diary creation time, the repository contains:

- Root Node package configuration
- Vite/React-oriented web application structure
- Backend domain structure
- Documentation library
- Docker configuration placeholders/files
- Environment template
- GitHub workflow directory
- Agent skills directory
- Licensing files
- Public web directory

The root `package.json` identifies the project as `agrisage` version `0.1.0` and contains development/build/lint scripts.

The package manifest includes React, Vite, TypeScript, Three.js, GSAP, Framer Motion/Motion, Tailwind-related packages, SplitType, Lenis, and Lucide React dependencies.

---

# Project Status Legend

Use these labels in future diary entries:

- **VERIFIED IN REPOSITORY** — Directly confirmed by repository contents.
- **DOCUMENTED** — Described in project documentation but not independently re-tested during the diary update.
- **IMPLEMENTED CLAIM** — Documentation states that a feature was implemented/verified.
- **PLANNED** — Listed as an intended future implementation.
- **BLOCKED** — Implementation cannot proceed until a dependency/decision is resolved.
- **NEEDS VERIFICATION** — Exists or is claimed, but should be tested before being treated as production-ready.

---

# Next Engineering Priorities

These are proposed organization priorities based on the repository's documented architecture, not claims that the work is already completed.

1. Keep the README and architecture documents synchronized with actual source code.
2. Verify the real implementation depth of each backend domain.
3. Verify the actual web application directory against the architecture specification.
4. Establish clear backend API contracts between web/mobile and FastAPI.
5. Implement or validate the agricultural datasets under `backend/data/`.
6. Validate DSSAT integration with reproducible test scenarios.
7. Validate CIB&RC safety logic against authoritative source data.
8. Validate knowledge ingestion and retrieval provenance.
9. Establish automated unit/integration/end-to-end tests.
10. Establish CI checks for type safety, linting, builds, and tests.
11. Separate demo/mock data from production/validated agricultural data.
12. Maintain explicit model/version provenance for every ML/LLM component.
13. Validate offline behavior on the target low-spec Android baseline.
14. Validate regional-language rendering and voice workflows.
15. Perform security review before exposing public APIs.
16. Maintain this diary whenever a major architectural or implementation decision changes.

---

# Diary Maintenance Rules

Every major development session should add an entry containing:

### Date
When the work occurred.

### Goal
What was being attempted.

### Changes
What files/components/architecture changed.

### Technical decisions
Why a particular implementation was selected.

### Verification
What was actually tested and the result.

### Problems
Known bugs, limitations, or unresolved questions.

### Next action
The immediate next engineering task.

### Evidence
Reference the relevant source file, commit, PR, test output, or specification document.

---

## Initial Baseline Summary

**Agri-SAGE is currently documented as a large agricultural decision-intelligence system rather than a simple disease-classification application.**

Its central architecture connects:

```
Farmer / Field Data
        ↓
Multimodal + Edge ML
        ↓
Multi-Agent Agricultural Reasoning
        ↓
Weather + Phenology + Knowledge
        ↓
DSSAT Simulation
        ↓
CIB&RC Safety Validation
        ↓
Confidence-Calibrated Advisory
        ↓
Farmer / Agronomist Presentation
```

The repository already contains a significant documentation and architectural foundation. Future diary entries should distinguish the **documented target architecture** from the **source-code implementation that has actually been verified**.

---

**End of initial project diary baseline.**
