# Agri-SAGE: Architectural Decisions and Action Plan (ADR & Roadmap)
**Document Version:** 1.0.0  
**Status:** Approved & Implementation-Ready  
**Date:** September 2026  
**Target Platform:** Web (Expert Agronomist Workstation & Farmer Advisory Explorer) + Mobile (Android Native / Flutter Hybrid)  
**Reference Specifications:** Agri-SAGE PRD, TRD, UI/UX Spec, Backend Schema, Implementation Plan, Security & Compliance, AI Prompt Handbook, QA Playbook, and Validation Report.

---

## 1. Executive Summary & Strategic Positioning

Agri-SAGE (*Scalable Agricultural Guidance Engine*) is an agricultural decision intelligence platform designed to replace fragmented, unverified, and high-latency advice with a unified, deterministic, simulation-grounded, and multi-agent system.

To compete with and outperform multinational agritech software (e.g., Bayer Climate FieldView, John Deere Operations Center, Plantix, Cropin), Agri-SAGE operates across two primary presentation surfaces:
1. **The Mobile Experience (`mobile/`)**: Optimized for smallholder farmers working in fields with intermittent connectivity, regional language constraints, and entry-level budget smartphones (Redmi 10A, 2GB RAM baseline).
2. **The Web Experience (`apps/web-expert/`)**: A desktop-grade workstation for institutional agronomists, extension officers (Krishi Vigyan Kendra / KVK), and cooperative (FPO) managers. It provides triage queues for low-confidence AI diagnoses, split-screen visual evidence inspection, CIB&RC chemical safety validation, and geospatial outbreak tracking.

This document formally records all architectural decisions, technology selections, design systems, and concrete action sequences for immediate implementation.

---

## 2. Architecture Decision Records (ADRs)

### ADR-001: Dual-Surface Architecture & Responsibility Split
- **Status:** Accepted
- **Context:** Farmers need an ultra-resilient, offline-capable mobile tool in the field. Agronomists and extension officers require dense data displays, multi-image comparison, audit tools, and keyboard-driven triage.
- **Decision:** Separate the frontends cleanly:
  - `apps/web-expert/`: Desktop/Tablet Web Application dedicated to Expert Review, Triage, Simulation Exploration, and Outbreak Monitoring.
  - `mobile/`: Android mobile application dedicated to Farmer Onboarding, Camera Diagnostics, Offline Cache, Voice Interaction, and Morning Briefings.
- **Consequences:** Eliminates compromise. The web app is not constrained by mobile screen dimensions, and the mobile app is not bloated by expert evaluation workflows.

---

### ADR-002: Frontend Technology Stack for the Web Workstation (`apps/web-expert/`)
- **Status:** Accepted
- **Context:** The web portal requires sub-second load times, crisp typography for regional scripts (Malayalam, Tamil, Telugu, Hindi, English), robust type safety, and responsive component libraries.
- **Decision:** Use **React 18 + Vite + TypeScript**.
  - **Bundler:** Vite (fastest HMR, zero-overhead builds, ES modules).
  - **Language:** TypeScript 5.x (strict null checks, explicit domain modeling matching Pydantic schemas).
  - **Styling:** Design-token-driven CSS system adhering 100% to `4_AgriSAGE_UIUX_Spec` (vanilla CSS custom properties, utility components, and responsive grid layouts).
  - **Icons:** Lucide React (feather-compatible, clean, accessible SVG vectors).
- **Consequences:** Maximum performance, zero runtime bloat, standard web accessibility (WCAG 2.1 AA), and zero licensing friction.

---

### ADR-003: Mobile Stack Strategy (Kotlin Compose vs. Flutter Evaluation)
- **Status:** Accepted (Hybrid-Ready Strategy)
- **Context:** The documents specify Kotlin + Jetpack Compose for Android. A question was evaluated regarding whether Flutter is superior.
- **Decision:**
  - **Primary Production Standard:** **Kotlin + Jetpack Compose** remains the reference standard for the Tier 3 baseline (Redmi 10A, 2GB RAM, Android 11) because it provides zero-copy camera frame processing via CameraX, direct Microsoft ONNX Runtime integration, and native Android `WorkManager` background sync without spawning high-overhead Dart isolates.
  - **Cross-Platform Alternative:** If multi-platform (iOS + Android) rapid delivery is prioritized, **Flutter** will be supported in `mobile/` with a **native Kotlin platform bridge** for the 5 FPS real-time Laplacian blur variance analysis and ONNX inference to prevent Dart thread contention.
  - **Web Rule:** Flutter Web is strictly **prohibited** for `apps/web-expert/` due to heavy canvas rendering, long initial load times, and poor text-selection UX on expert desktop displays.

---

### ADR-004: Design System, Tokens, and Typography
- **Status:** Accepted
- **Context:** UI/UX specification defines strict color palettes, typography scales, elevation tokens, and accessibility standards.
- **Decision:** Implement the complete 30-token design system as CSS Custom Properties:
  - **Primary Palette:** Forest Green (`color_primary: #2D7D2D`, `color_primary_dark: #1A5C1A`, `color_primary_light: #E8F5E8`, `color_primary_container: #C8E6C9`).
  - **Risk Palette:** Critical (`#C62828`), High (`#E65100`), Medium (`#F57F17`), Low (`#2E7D32`).
  - **Confidence Badges:** `CONFIRMED` (`#1B5E20`), `LIKELY` (`#2E7D32`), `POSSIBLE` (`#F57F17`), `UNCERTAIN` (`#BF360C`), `INSUFFICIENT_DATA` (`#757575`), `CONFLICTING_EVIDENCE` (`#E65100`), `OUT_OF_SCOPE` (`#616161`).
  - **Typography:** **Google Fonts Noto Sans & Noto Sans Malayalam** loaded globally. Browser defaults or system fonts are strictly banned to prevent missing glyphs on regional text.
  - **Touch & Accessibility:** Minimum 48px touch targets, 4.5:1 text contrast ratio, and semantic color independence (every status badge pairs an icon with text).

---

### ADR-005: Safety, Statutory Disclaimers, and Non-Negotiable Agricultural Rules
- **Status:** Accepted
- **Context:** Agricultural errors destroy farmer livelihoods. System hallucination or unverified chemical suggestions can result in crop failure or legal liability.
- **Decision:** Hardcode the following deterministic rules into all presentation layers:
  1. **CIB&RC Chemical Validation:** Every fungicide, pesticide, or fertilizer card must display its official CIB&RC registration status, verified dosage (per acre/hectare), and exact spray window (temperature, humidity, wind constraints).
  2. **Modelled Yield Disclaimers:** Any yield projection, income estimate, or simulation metric originating from DSSAT or mathematical models must visibly display: `* Modelled estimate`.
  3. **Statutory Scheme Caveat:** Every government subsidy/scheme display (PMFBY, PM-KISAN, RKVY) must render the required legal disclaimer: *"Final eligibility determined by concerned authority / അന്തിമ യോഗ്യത ബന്ധപ്പെട്ട അധികാരി നിർണ്ണയിക്കും"*.
  4. **Calibrated Confidence:** Never show a naked percentage. Always render one of the 7 discrete confidence states with its corresponding evidence bundle.

---

## 3. Web Architecture Diagram

```
apps/web-expert/
├── index.html                   <-- Noto Sans typography, meta headers, theme root
├── vite.config.ts               <-- Fast HMR build configuration
├── package.json                 <-- Dependencies: React 18, TS, Lucide, Canvas tools
├── src/
│   ├── assets/                  <-- SVGs, crop schematics, leaf symptom guides
│   ├── styles/
│   │   ├── tokens.css           <-- All 30 color tokens, spacing, typography, elevations
│   │   └── global.css           <-- Reset, CSS variables, utility classes, animations
│   ├── types/
│   │   ├── advisory.ts          <-- AdvisoryResponse, ConfidenceState, RiskLevel, Evidence
│   │   ├── expert.ts            <-- ExpertReviewQueueItem, VerdictPayload, AuditEntry
│   │   ├── farm.ts              <-- FarmProfile, Field, CropCycle, CropStage, GDD
│   │   └── simulation.ts        <-- DSSAT Scenario A/B/C, Yield Delta, Water Stress
│   ├── components/
│   │   ├── common/              <-- Button, Badge, Modal, Tabs, Dropdown, Tooltip
│   │   ├── cards/               <-- AdvisoryCard, EvidenceCard, ScenarioCard, RiskCard, SchemeCard
│   │   ├── triage/              <-- QueueTable, TriageFilter, UrgencyIndicator
│   │   ├── inspection/          <-- ImageZoomViewer, EvidenceSplitView, ChemicalVerifier
│   │   └── sandbox/             <-- MobileEmulatorFrame, CameraSimulator, RealtimeQualityBar
│   ├── views/
│   │   ├── ExpertDashboard.tsx   <-- Agronomist Review Queue & Daily Triage Center
│   │   ├── ReviewDetailView.tsx  <-- Deep Diagnosis Inspection & Overrule Console
│   │   ├── AdvisorySandbox.tsx   <-- Interactive Farmer Advisory & Scenario Simulator
│   │   ├── OutbreakRadar.tsx     <-- Regional Disease & Pest Geospatial Clusters
│   │   └── KnowledgeBrowser.tsx  <-- ICAR / KAU Verified Agricultural Library Explorer
│   ├── services/
│   │   ├── api.ts               <-- REST client for FastAPI backend with JWT
│   │   └── mockData.ts          <-- Comprehensive seed data from backend/data/*.json
│   ├── i18n/
│   │   ├── en.ts                <-- English strings
│   │   └── ml.ts                <-- Malayalam strings (from UI/UX Spec Section 8)
│   ├── App.tsx                  <-- Root shell with Navigation Bar & View Router
│   └── main.tsx                 <-- Entry point
```

---

## 4. Phase-by-Phase Web Implementation Action Plan

### Phase 1: Environment & Design System Scaffolding (Immediate Action)
- [ ] Initialize Vite + React + TypeScript inside `d:/work/Projects/AgriSage/AgriSage/apps/web-expert/`.
- [ ] Install core dependencies: `lucide-react`, standard development types, and CSS tooling.
- [ ] Create `tokens.css` with exact hex values, spacing (4dp to 48dp), radius (8dp to 24dp), and elevation shadows.
- [ ] Setup `index.html` with Google Fonts `Noto Sans` (Latin, Malayalam, Devanagari) to guarantee zero missing glyphs.

### Phase 2: Core Agricultural Component Library
- [ ] **Badges**:
  - `ConfidenceBadge` (`CONFIRMED`, `LIKELY`, `POSSIBLE`, `UNCERTAIN`, `INSUFFICIENT_DATA`, `CONFLICTING_EVIDENCE`).
  - `RiskBadge` (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`).
  - `ModelledBadge` (`* Modelled estimate`).
  - `OfflineBadge` & `CachedBadge`.
- [ ] **Action & Advisory Cards**:
  - `AdvisoryCard`: Diagnosis header, local Malayalam name, severity banner, action steps.
  - `EvidenceCard`: Expandable factor breakdown (Image pattern + Weather factor + GDD stage + ICAR literature citation).
  - `ScenarioCard`: 3-way DSSAT scenario comparison (A: Do nothing, B: Treat now [Recommended], C: Delayed intervention) with yield and cost deltas.
  - `SchemeCard`: Central/State scheme banner with statutory eligibility warning.
  - `MorningBriefingCard`: Audio narration player, daily risk summary, spray window alert.

### Phase 3: Expert Agronomist Review Workstation
- [ ] **Triage Queue**: Sortable, filterable list of pending farmer diagnoses requiring verification (flagged low-confidence, high-risk crop stages, or conflicting evidence).
- [ ] **Split-Screen Evidence Inspector**:
  - Left pane: Farmer-uploaded leaf photograph with interactive zoom, pan, and lighting analysis.
  - Right pane: Model inference breakdown (ONNX top-3 class probabilities, DFI weather index, crop growth GDD stage).
- [ ] **Chemical & Statutory Safety Console**:
  - Interactive lookup against the CIB&RC pesticide label registry.
  - Dosage safety validator with automatic warnings if active ingredient is prohibited or stage-inappropriate.
- [ ] **Verdict Form**:
  - One-click *Approve Diagnosis*, *Override Diagnosis*, or *Request Retake*.
  - Corrections editor and direct farmer notification dispatcher.

### Phase 4: Farmer Advisory Sandbox & Interactive Simulator
- [ ] Built-in **Mobile Device Preview** mode allowing developers and agronomists to test the mobile app flows directly on the web:
  - Language switcher (Malayalam / English / Tamil / Telugu / Hindi).
  - Virtual camera preview with interactive real-time blur and lighting quality degradation sliders.
  - Instant advisory calculation preview using seed datasets from `backend/data/`.

### Phase 5: Outbreak Radar & Geospatial Analytics
- [ ] Regional disease cluster heatmap displaying reports across Kerala districts (Wayanad, Palakkad, Thrissur, Alappuzha, Idukki).
- [ ] Weather alert correlation engine visualizing Disease Favorability Index (DFI) vs. field observations.

---

## 5. Verification & Quality Gates

To ensure this build meets master-grade production standards:
1. **Zero Console Errors & Type Safety**: Strict TypeScript configuration (`noImplicitAny`, `strictNullChecks`).
2. **Performance Benchmark**: Lighthouse score > 95 on Desktop, FCP < 0.8s.
3. **Accessibility**: Full keyboard navigation, ARIA attributes on all custom interactive cards, WCAG 2.1 AA compliant contrast.
4. **Localization Integrity**: Zero untranslated placeholder text when toggling between English and Malayalam.

---

## 6. Implementation Record: Frame 1 & 2 Supercharging

### Frame 1: 3D Scrollytelling Experience (`PublicLandingPage.tsx`)
- **Interactive 3D Three.js Background Canvas (`ThreeHeroCanvas.tsx`)**:
  - 450 bio-luminescent floating spores & data nodes with smooth camera mouse parallax.
  - Holographic planetary digital twin wireframe icosahedron with satellite orbit ring and orbiting beacon.
  - Zero-lag requestAnimationFrame rendering with automated cleanup and devicePixelRatio capping.
- **Cinematic Dual-Mode Hero Switcher**:
  - Mode 1: Orbital Farmland View (`hero_earth.jpg`) with high-altitude satellite telemetry.
  - Mode 2: 3D Sprout Macro Close-Up (`hero_sprout_macro.jpg`) with cellular bio-luminescence and water droplet refraction.
- **Interactive 3D Specular Tilt Cards (`GlassTiltCard.tsx`)**:
  - Perspective transforms (`rotateX`, `rotateY`, `scale3d`) tracking cursor with moving specular glare highlight.
  - Live bio-telemetry metrics: Temp 29.4°C, Moisture 64%, Humidity 78%, Disease Risk Low, Vitality 98%, Growth Rate 1.4 mm/h.
- **Chapter 02 The Problem**:
  - Draggable split-view slider comparing Daylight Human Vision vs. Agri-SAGE Thermal Bio-Spectra (`crop_split.jpg`).
  - Animated continuous laser scan bar (`laser-scanner-line`).
  - 5 biological warning indicators: Soil Dryness, Temperature Rise, Humidity Trapping, Leaf Stress, and Disease Begins.
- **Chapter 03 The Farm 360°**:
  - Isometric layered farm render (`farm_isometric.jpg`) with interactive layer chips (All, Satellite, Weather, Soil, Irrigation, Sensors, Farmer) and floating coordinate pins.
- **Chapter 04 See The Invisible**:
  - Microscopic cellular visualization (`cellular_macro.jpg`) with animated rotating reticle and spectral wavelength selector (Visible RGB, RedEdge, NIR, Thermal IR).
- **Chapter 05 & 06 Neural Pipeline & Multi-Agent Constellation**:
  - 4-stage interactive pipeline (Raw Data ➔ AI Core ➔ DSSAT Simulation ➔ CIB&RC Action).
  - Star-topology hub with 6 specialized agents (Vision, Weather, GDD Phenology, DSSAT, CIB&RC Critic, Vernacular Voice).
- **Chapter 07 Crop Simulation Studio**:
  - Time horizon slider (+1d, +3d, +7d, +14d) with live yield projection curves and mandatory `* Modelled estimate` disclaimer.
- **Chapter 08 Predict ➔ Prevent ➔ Protect**:
  - Interactive risk reduction pipeline demonstrating 72% initial danger crushing down to 10% protected residual risk.
- **Chapter 09 Farmer Advisory**:
  - Kerala farmer tablet visual (`farmer_tablet.jpg`) with floating glass advisory card, synthesized Malayalam audio player, and WhatsApp dispatch simulation.
- **Chapter 10 Global Network**:
  - Digital twin earth mesh (`network_globe.jpg`) with regional cluster selector (Palakkad, Punjab, Vidarbha, California, Rift Valley) and 1,000+ farms milestone badges.
- **Chapter 11 & 12 Platform Console & Final CTA**:
  - Interactive console preview tabs leading directly into the frozen, master-grade Frame 3 Workstation.
- **Scroll-Craft Timeline Scrubber**:
  - Precision scroll percentage tracking (`scrollProgress`) with continuous top gradient scrubber bar.
- **Web Audio Sound Synthesizer (`audioFX.ts`)**:
  - Zero-asset Web Audio API tone generator with navbar mute/unmute toggle.

### Frame 2: Enhanced Authentication Experience (`AuthPortal.tsx`)
- **3D GlassTiltCard Portal**:
  - Perspective-reactive card container with specular light glare.
  - Three.js particle ambient canvas layer behind authentication viewport.
- **Dual-Role Verification Workflows**:
  - Farmer Phone OTP: 6-box pin code input, 5-minute expiration countdown, and instant pre-fill button.
  - Agronomist KVK Portal: Institutional email/key validation with ICAR/CIB&RC compliance badges.
- **Biometric Passkey Simulation (FIDO2 / WebAuthn)**:
  - Simulated fingerprint verification pipeline for passwordless enterprise security.
- **Developer Fast-Path**:
  - Instant demo bypass for seamless navigation into Frame 3.

### Frame 1 & 2: SNAP ON SCROLL - GSAP Elementor Scrolltrigger (No Plugin Slider)
- **Native CSS / GSAP Scroll Snap (`global.css` & `useScrollTriggerSnap.ts`)**:
  - Pure CSS scroll snapping: `.snap-scroll-container` (`scroll-snap-type: y mandatory`) with smooth snapping sections `.snap-scroll-section` (`scroll-snap-align: start; scroll-snap-stop: always`).
  - Zero heavy slider plugin dependencies: no Swiper, no Slick, zero external carousel bloat.
  - Multi-layer element triggers on scroll (`.st-layer-1`, `.st-layer-2`, `.st-layer-3`, `.st-layer-4`):
    - `st-layer-1` (Tag / Category Badge): slides up at 0.05s delay.
    - `st-layer-2` (Headline & Narrative): slides up at 0.18s delay.
    - `st-layer-3` (Main Interactive Cards / Controls): pops with 3D elevation at 0.32s delay.
    - `st-layer-4` (Status Bars & Telemetry Badges): reveals at 0.48s delay.
  - Keyboard snapping support: ArrowDown / ArrowUp / PageDown / PageUp keys smoothly advance through snap chapters.
  - Automatic `IntersectionObserver` threshold trigger (`0.35`) activating `.is-active-snap` dynamically on scroll entrance.

---
*Status: Frame 1 & 2 supercharged with SNAP ON SCROLL & GSAP ScrollTrigger mechanics. Verified with HTTP 200 and zero build errors. Frame 3 frozen and intact.*

---

### Multi-Layer Parallax Floating Decorations Engine (`useParallaxLayers.ts`)
- **Architecture**: Custom React hook using `requestAnimationFrame` with passive scroll listener for buttery 60fps.
- **Data Attribute API**: Elements tagged with `data-parallax-speed` move at different rates:
  - `0.3` – Deep background (slowest, creates distant feel)
  - `0.5` – Mid-background ring decorations
  - `0.7` – Medium-depth orbs with glow pulse
  - `1.0` – Normal content speed (baseline)
  - `1.3–1.5` – Foreground elements (faster than scroll, "flying past" effect)
  - `-0.2` – Contra-parallax (moves opposite direction, very premium)
- **Optional Data Attributes**:
  - `data-parallax-direction`: `y` (default), `x`, or `both`
  - `data-parallax-rotate`: degrees per 1000px of scroll (subtle rotation)
- **CSS Classes** (`global.css`):
  - `.parallax-decoration` – base positioning (absolute, pointer-events: none, will-change: transform)
  - `.parallax-orb-emerald/cyan/amber/purple` – radial gradient orbs with box-shadow glow
  - `.parallax-ring` / `.parallax-ring-dashed` – hollow circle decorations
  - `.parallax-diamond` – rotated 45° rhombus shapes
  - `.parallax-cross` – plus/cross mark via ::before/::after
  - `.parallax-dotgrid` / `.parallax-hexgrid` – pattern fills
  - `.parallax-glow-pulse` / `-delayed` / `-slow` – ambient breathing animations
- **Chapter Distribution**: 7 elements in Hero (Ch01), 3 each in Ch03/07, 4 in Ch05, 3 in Ch10/12
- **Accessibility**: Full `prefers-reduced-motion: reduce` support (disables all transforms & animations)

### Scroll-Driven Image Sequence (`useScrollSequence.ts`)
- **Concept**: Apple-style scroll-scrubbed frame player (video-to-JPG effect)
- **5-Frame Bioluminescent Sprout Growth Sequence**:
  - Frame 1: Seed emergence (tiny shoot breaking soil)
  - Frame 2: Cotyledon stage (first leaves unfurling)
  - Frame 3: Leaf expansion (4 leaves with glowing veins)
  - Frame 4: Vegetative growth (6-8 leaves, strong stem)
  - Frame 5: Full canopy (mature branching plant)
- **Technical Implementation**:
  - Canvas-based rendering with cover-fit (maintains aspect ratio)
  - Preloads all frames on mount for zero-latency scrubbing
  - Maps container's viewport intersection to frame index (0→N)
  - RAF-throttled scroll handler for smooth performance
  - Responsive canvas resizing on window resize
- **Section Features**:
  - Progress bar with emerald-to-cyan gradient
  - Frame counter badge overlay
  - HUD overlay with phenological stage labels
  - Parallax decorations alongside the sequence container

---
*Status: Multi-Layer Parallax Engine & Scroll-Driven Image Sequence implemented. TypeScript compiles with zero errors. All 5 generated sprout frames deployed to public/images/.*

---

### Frame 1: Master "Dewdrop of Agri-Intelligence" SVG Animation Ecosystem
- **Core Visual Metaphor**:
  - A bio-luminescent, fluid droplet with surface tension physics, trailing micro-droplets, and dynamic refraction shaders that travels down a continuous capillary irrigation stream across the entire 12,000px height of Frame 1.
- **8 Core Motion Technologies Implemented**:
  1. **Scroll Tracking**:
     - **GSAP ScrollTrigger**: Scroll velocity and scroll progress tracking powering position interpolation.
     - **Framer Motion (`useScroll`, `useSpring`, `useTransform`)**: Smooth physics spring/lerp calculations for continuous fluid movement along the capillary track.
  2. **Viewport Detection**:
     - **Intersection Observer API + Framer Motion (`useInView`)**: Live chapter entry/exit triggers, dynamic biophilic color shifting, and waypoint glow state updates.
  3. **CSS Sticky Position**:
     - `.sticky-dewdrop-track` (`position: sticky; top: 0; height: 100vh; overflow: hidden; pointer-events: none; z-index: 35;`) keeps the Capillary Stream track and Telemetry HUD pinned seamlessly relative to the viewport while chapters scroll without blocking clicks.
     - Replaced `overflow-x-hidden` with `overflow-x-clip` on parent container to eliminate the CSS Sticky overflow trap.
  4. **Modern Motion Easing**:
     - Custom cubic-bezier spring physics ($k=240, c=26$) applied to velocity damping, teardrop stretching, and surface tension idle oscillations.
  5. **Kinetic Typography (SplitType)**:
     - `useSplitTypography.ts` hook: Splits chapter headlines into accessible words/lines, wraps lines in `.line-mask` (`overflow: hidden`), and animates characters with staggered GSAP `power4.out` reveals upon viewport entry while preserving WCAG `aria-label` accessibility.
  6. **Map Function (`.map()` & `mapRange()`)**:
     - Programmatic rendering of the 12 Waypoint Nodes, stream line segments, micro-droplets, and mathematical range mapping translating scroll progress to spline length, rotation angle, scale, and chapter-to-chapter chromatic transitions.
  7. **LERP (Linear Interpolation) Multi-Body Viscosity**:
     - `lerp()` and delta-time independent `damp()`: Main Dewdrop tracks scroll target with LERP damping ($\lambda = 14$); 3 trailing daughter droplets follow in a viscosity bead chain ($d_1, d_2, d_3$).
  8. **GPU Shaders**:
     - **SVG Liquid Refraction Filter Shader**: `<feTurbulence>`, `<feDisplacementMap>`, and `<feSpecularLighting>` producing authentic liquid glass refraction and caustic light glints directly on the SVG droplet.
     - **Canvas Fluid Ripple & Caustic Shockwave Shader (`FluidRippleShaderCanvas.tsx`)**: Concentric liquid shockwaves with chromatic wave rings emitted when the dewdrop crosses chapter milestones or experiences rapid scroll acceleration.
- **Interactive Scrollytelling HUD**:
  - Live biophysical telemetry readout (`CH 01-12`, biophilic theme colors, instant velocity bar in `px/s`).
  - 12 interactive clickable Waypoint Nodes with hover tooltips in Malayalam & English for direct chapter jumping.
- **Verification Status**:
  - Browser subagent verified full 12-chapter descent, smooth 60fps tracking, interactive waypoint jumps, and zero console errors.

### Hero Section Glitch Resolution
1. **Title/Subtitle Separation**:
   - Re-architected `<h1>` so `"Agri-SAGE"` is a standalone block title and `"Intelligence for Every Field."` is a pure-text subtitle element with `useSplitTypography`. Eliminated SplitType text collapse and line overlapping.
2. **Hook & Dispatcher Stability**:
   - Added `resolve.dedupe: ['react', 'react-dom']` in `vite.config.ts`.
   - Connected `DewdropScrollTracker` directly to `scrollProgress` from `useScrollTriggerSnap` with RAF `damp()` smoothing, removing external Framer Motion hook dispatcher exceptions.
3. **Telemetry HUD Contextual Visibility**:
   - Telemetry HUD on right rail is contextually hidden (`opacity-0`) during Chapter 1 (Hero) so it never collides with Hero 3D telemetry cards (`Palakkad Hectare #04`), then slides in smoothly (`opacity-100`) for Chapters 2 through 12.
4. **Hero Subtitle Visibility Restored**:
   - Removed SplitType ref from `"Intelligence for Every Field."`. Injected `line-mask` wrappers previously conflicted with `-webkit-background-clip: text` on `.text-shimmer`, making the text transparent. The subtitle now renders with 100% full visibility and its animated emerald-cyan metallic gradient shine intact.

### Full-Canvas 2D Sinuous Water Droplet Motion Engine
1. **Full-Canvas X-Axis Trajectory**:
   - Removed fixed right-gutter constraint; the water droplet now travels organically across the entire screen width on both X and Y axes via a 12-point Catmull-Rom Sinuous Spline:
     - Ch 01: Center-top atmosphere (50% X)
     - Ch 02: Weaving right past scanner (78% X)
     - Ch 03: Sweeping across left over soil layers (22% X)
     - Ch 04: Right of spectral bands (80% X)
     - Ch 05: Left into neural decision pipeline (36% X)
     - Ch 06: Right across multi-agent hub (74% X)
     - Ch 07: Left through crop simulation curves (24% X)
     - Ch 08: Right entering risk barrier (76% X)
     - Ch 09: Left into farmer advisory tablet (28% X)
     - Ch 10: Right orbiting global digital twin (80% X)
     - Ch 11: Left into workstation console (32% X)
     - Ch 12: Landing directly into the seed singularity portal (50% X)
2. **Dynamic Motion Vector Alignment & 4-Body Viscosity**:
   - Evaluates spline tangent $\vec{T} = (T_x, T_y)$ and velocity $\vec{v}$ to dynamically orient the teardrop tip along the true angle of motion.
   - 4 trailing daughter droplets ($D_1, D_2, D_3, D_4$) form a viscous bead chain following the 2D path with chained LERP damping.
3. **Zero Text Overlap & Docked Scrollytelling Pill**:
   - Droplet trajectory gracefully weaves through inter-column corridors and margins, never covering text.
   - Telemetry HUD is docked at `fixed bottom-6 right-6`, completely clear of all content, headlines, and cards.
   - Verified live in browser with 0 console errors and 60fps fluidity.

### Prominent 3D Water Droplet & 2D Hydrological Spline Trajectory
1. **100% Prominently Visible Water Droplet**:
   - Positioned in a dedicated `z-30` overlay container (`pointer-events: none`).
   - High-contrast 3D liquid glass appearance with bioluminescent radial gradient (`#00f0ff`, `#10b981`, `#a855f7`, `#f59e0b`), specular glints (`<circle cx="-6" cy="-2" r="4.0" />`), inner caustic ring, glowing corona (`filter="url(#dewdrop-glow)"`), and a pulsating biophilic core spark.
2. **Zero Waypoint Dots & Clean River Stream**:
   - Completely removed all waypoint circle markers, pulse rings, hover labels, and path dots.
   - The stream renders as an elegant, continuous, translucent light guide (`stroke="url(#stream-gradient)" strokeWidth="3.5"`).
3. **Full-Canvas Sinuous X-Y Weaving**:
   - Weaves continuously across the full screen width and height (50% X in Ch 01, 78% X in Ch 02, 22% X in Ch 03, 36% X in Ch 05, down to 50% X in Ch 12).
   - Dynamic motion vector rotation ($\text{atan2}(v_x, v_y)$) aligns the teardrop tip along the path.
   - 4 trailing daughter droplets ($D_1, D_2, D_3, D_4$) follow in a fluid viscosity chain.
4. **Zero Text Collisions & Crisp Typography**:
   - Hero headlines `"Agri-SAGE"` and `"Intelligence for Every Field."` are 100% visible, crisp, legible, with zero overlap.
   - Telemetry HUD is docked at `fixed bottom-6 right-6 z-50`.
   - Verified live in browser with 0 console errors and 60/120fps fluidity.

