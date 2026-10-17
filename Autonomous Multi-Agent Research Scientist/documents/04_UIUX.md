# UI/UX Design Document

**Product:** AMRS — Autonomous Multi-Agent Research Scientist & Startup Intelligence Platform
**Version:** 1.0
**Date:** June 2026

---

## 1. Design Principles

1. **Transparency over magic.** The multi-agent architecture is a selling point, not an implementation detail to hide. The UI should make agent activity visible (Agent Monitoring Dashboard), not pretend a single black box produced the report.
2. **Honest confidence, not false certainty.** Confidence scores, contradiction flags, and "degraded" states are first-class UI elements, not buried in fine print. This is a design requirement directly inherited from PRD §12 and TRD §6 — the product's credibility depends on never visually implying perfection.
3. **Two speeds, one product.** Daily Assistant Mode should feel as fast and lightweight as any chat app. Deep Research Mode should feel deliberate and substantial — different pacing, same visual language.
4. **Progressive disclosure.** Default views show conclusions; raw agent traces, source lists, and methodology notes are one click away, not hidden entirely and not dumped all at once.

---

## 2. Visual Identity

| Element | Decision | Rationale |
|---|---|---|
| Primary typeface | Inter (UI), IBM Plex Mono (code/data/agent logs) | Inter is highly legible at small sizes for dense report UI; a monospace face visually distinguishes raw/technical output from authored prose |
| Color system | Neutral slate base (#0F172A dark / #F8FAFC light) with a single accent (indigo, #4F46E5) for primary actions; status colors kept semantically consistent: green = verified, amber = partial/degraded, red = contradicted/failed | Avoids a "generic AI gradient" look; status color consistency is functionally important since the product's value depends on the user trusting status indicators |
| Density | Medium-density layout for reports (not maximally spacious marketing-site style) | Reports are working documents users will scan repeatedly, not landing-page hero content |
| Iconography | Outline icon set, consistent stroke weight, one icon per agent role used consistently across Dashboard and Trace views | Builds a visual vocabulary so a returning user recognizes "Critic Agent" by icon, not just by re-reading a label |

---

## 3. Key Screens

### 3.1 Home / Hub
- Top bar: logo, mode toggle (segmented control: Daily Assistant | Deep Research), account menu.
- Left sidebar: Recent (chats + reports, merged and timestamp-sorted), New Research button (prominent, since this is the differentiated feature).
- Main panel: contextual — shows chat input if Daily mode is active, or the Query Composer if Deep Research is active.
- Usage indicator (e.g., "3 of 5 research runs remaining this week" for free-tier users) — visible but not alarmist; amber only when near limit.

### 3.2 Daily Assistant Chat
- Standard chat layout: message bubbles, streamed text, markdown rendering, code block support with copy button.
- Subtle, persistent affordance: "Need deeper research on this?" link appears under any assistant message that looks like a research-style question (heuristic-triggered), offering one-click escalation to Deep Research mode.

### 3.3 Deep Research — Query Composer
- Large, prominent textarea (this is the primary input of the product).
- Below it: three optional toggle chips — "Market Analysis," "Startup Concepts," "Tech Architecture" — each with a one-line tooltip explaining what it adds and that it adds to run time.
- File upload zone (drag-and-drop + click), supporting PDF/DOCX grounding documents.
- Estimated time-to-completion shown next to the "Run Research" button before submission (e.g., "Typically 2–6 minutes with current selections") — sets expectations honestly rather than showing a generic spinner.

### 3.4 Agent Monitoring Dashboard (Pipeline Running)
- Horizontal pipeline visualization: each agent is a card in sequence (with parallel branches shown as side-by-side lanes, matching the App Flow §4 structure).
- Card states: Queued (gray, outline), Running (accent color, animated pulse — not a spinning loader, to avoid implying indeterminate progress when in fact pipeline position is known), Done (green check), Degraded (amber, with a one-line reason), Failed-with-fallback-recovered (small "recovered via fallback" tag — this is a deliberate transparency choice to make the reliability engineering visible, not just claimed).
- Live findings feed below the pipeline cards, populated as each agent completes (per App Flow §3.7).

### 3.5 Report View
- Sticky header: query title, confidence score (large, with a "What does this mean?" info affordance that opens a short explainer — never just a bare number presented as fact), export/save/follow-up actions.
- Tabbed or scroll-anchored sections matching PRD deliverables: Research Summary, Fact-Check Table, Critic's Notes, Market Analysis, Startup Concepts, Technical Architecture, Roadmap.
- **Fact-Check Table** is a literal table: Claim | Status (color-coded badge) | Supporting Sources | Conflicting Sources (if any). This is the single most trust-critical UI element in the product and is treated as a first-class table, not folded into prose.
- **Critic's Notes** rendered visually distinct from the main report body (e.g., a left border accent, slightly different background) so it reads as "this is the system challenging itself," reinforcing the design principle in §1.2.
- Per-section "View Agent Trace" toggle reveals the raw output and which model/provider actually served that step (useful for both transparency and for engineering debugging during demos).

### 3.6 Saved Library
- Card grid or list (user-toggleable), each card showing title, date, confidence score badge, and mode used.
- Search/filter by date and confidence range.

---

## 4. Component Inventory (for Frontend Implementation)

| Component | Used In | Notes |
|---|---|---|
| `ModeToggle` | Home/Hub header | Segmented control, persists selection in user preferences |
| `AgentStatusCard` | Pipeline Running | Props: agent name, icon, status enum, optional degraded-reason string |
| `ConfidenceBadge` | Report View, Saved Library | Color scale tied to score range; always paired with an info tooltip, never shown bare |
| `FactCheckTable` | Report View | Sortable by status; expandable rows for source lists |
| `AgentTracePanel` | Report View (per section) | Collapsed by default; shows raw agent output + model/provider used |
| `QueryComposer` | Deep Research entry | Textarea + toggle chips + file upload + time estimate |
| `UsageMeter` | Home/Hub sidebar | Quota remaining, color-shifts only near limit |

---

## 5. Accessibility Requirements

- All status colors (verified/partial/contradicted/degraded) paired with text labels and icons — never color alone, for colorblind accessibility.
- Pipeline Dashboard animations respect `prefers-reduced-motion`.
- Full keyboard navigation for Query Composer and Report View (tab order follows visual/logical reading order).
- Minimum AA contrast ratios across both light and dark themes.

---

## 6. Responsive Behavior

- **Desktop (primary target for v1):** full sidebar + main panel layout as described above.
- **Tablet:** sidebar collapses to an icon rail, expandable on tap.
- **Mobile (v1: functional, not optimized):** single-column stack; Agent Monitoring Dashboard switches from horizontal pipeline to a vertical step list to fit narrow viewports; full mobile-native optimization is explicitly deferred (see PRD §4.2 Non-Goals).

---

## 7. Tone of Microcopy

- Never use absolute language ("100% accurate," "guaranteed," "perfect"). Approved patterns: "Verified against 3 sources," "Flagged as uncertain — review before relying on this," "This step used a fallback provider."
- Error states are specific, not generic. Avoid "Something went wrong" alone; pair with what happened and what the user can do ("The Business Analyst step couldn't complete — your report is missing the Market Analysis section. You can re-run just this section.").
