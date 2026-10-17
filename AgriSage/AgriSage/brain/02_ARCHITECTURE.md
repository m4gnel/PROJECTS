# AGRI-SAGE — SYSTEM ARCHITECTURE

## Six Layers
1. Input & Context — image, voice, location, farm history
2. 14 AI Agents — LangGraph orchestrated
3. Knowledge Base — verified RAG (ICAR + KAU)
4. Simulation — DSSAT crop physics
5. Decision Engine — deterministic scoring
6. Delivery — voice + text + alerts in Malayalam

## LangGraph Pipeline (1.0.8)
START → intake → [vision, weather, crop_stage, knowledge] PARALLEL
→ critic BARRIER → scheme (always) + simulation (conditional)
→ decision → explanation → END

## Backend Services
Auth | Farm | Advisory (LangGraph) | Vision | Weather | Knowledge
Scheme | Market | Simulation | Notification | Sync

## Android Architecture (MVVM)
Compose Screens → ViewModels (StateFlow) → UseCases
→ Repositories → Room (local) + Retrofit (remote)

## Connectivity States
ONLINE: full pipeline | LIMITED: local ONNX + cached | OFFLINE: ONNX + templates

## Infrastructure
Backend: Oracle Always-Free (2x AMD, 24GB RAM)
Storage: Cloudflare R2 (free 10GB, zero egress)
CDN + SSL: Cloudflare free | Monitoring: Grafana Cloud free

## Key Rules
1. Every external service behind abstraction interface
2. WeatherProvider, SimulationEngine, SpeechProvider all abstract
3. LLM outputs go through schema validator before use
4. User text never in LLM system prompt — only structured data
5. SimulationParams typed struct only — never free text to DSSAT
