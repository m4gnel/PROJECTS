# 🤖 PHASE 2 — LangGraph 14-Agent System
## Branch: `dev/m4-agents` · Owner: M4 · GitHub Issue: #2

---

## Paste This Into Gemini 2.5 Pro

```
=== AGRI-SAGE PHASE 2 — LANGGRAPH 14-AGENT ORCHESTRATION ===

Run AUDIT-FIRST PROTOCOL on every file in app/agents/ before writing anything.
Print the audit table. Build only MISSING and NEEDS_WORK files.

TARGET FILE STRUCTURE:
app/agents/
├── state.py             ← AgriSageState TypedDict
├── graph.py             ← Compiled LangGraph graph + MemorySaver
├── router_agent.py      ← Intent classifier
├── translator_agent.py  ← Language detect + ML/EN/TA pre+post translation
├── weather_agent.py     ← Calls WeatherService + formats crop risk
├── soil_agent.py        ← Calls SoilService + formats recommendation
├── pest_agent.py        ← DB query pest_alerts + risk score
├── market_agent.py      ← DB query market_prices + sell/hold recommendation
├── crop_advisor_agent.py← pgvector RAG over KAU documents
├── irrigation_agent.py  ← ET₀ from weather + crop stage
├── fertilizer_agent.py  ← NPK from soil context + crop stage
├── sowing_agent.py      ← DSSAT subprocess call + parse output
├── synthesizer_agent.py ← Merges all agent_outputs → final_answer_en
├── alert_agent.py       ← Threshold check → FCM trigger if needed
└── analytics_agent.py   ← Logs to farm_analytics table
brain/
└── 05_AGENT_PROMPTS.md  ← System prompts for all 14 agents

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STATE DEFINITION — EXACT (app/agents/state.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from typing import TypedDict, Annotated
import operator

class AgriSageState(TypedDict):
    farmer_id: str
    farmer_query: str          # raw input — may be Malayalam or Tamil
    language: str              # "ml" | "en" | "ta"
    location: dict             # {district: str, lat: float, lon: float}
    crop: str                  # primary crop detected from query
    crop_stage: str            # "seedling"|"vegetative"|"flowering"|"harvest"|"unknown"
    query_intent: list[str]    # e.g. ["WEATHER","PEST","FERTILIZER"]
    weather_context: dict      # WeatherContext as dict (or {} if not fetched)
    soil_context: dict         # SoilContext as dict (or {} if not fetched)
    pest_alerts: list[dict]    # active alerts for district+crop
    market_data: dict          # {crop, district, modal_price, trend, sell_recommendation}
    kau_rag_results: list[str] # top-5 KAU doc chunks
    dssat_output: dict         # {sow_date, yield_kg_ha, risk_factors} or {}
    agent_outputs: Annotated[dict, operator.ior]  # merged from parallel agents
    final_answer_en: str       # English synthesized answer
    final_answer_ml: str       # Malayalam translated answer
    fcm_triggered: bool        # whether a push notification was sent
    error: str                 # error message if any agent failed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GRAPH TOPOLOGY — EXACT (app/agents/graph.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MANDATORY imports (LangGraph 1.0.8 — use these EXACTLY):
  from langgraph.graph import StateGraph, START, END
  from langgraph.checkpoint.memory import MemorySaver
  from langgraph.types import Send

DO NOT use: __start__, __end__, MemoryCheckpointer (these are wrong versions)

Graph structure:
  builder = StateGraph(AgriSageState)

  Nodes to add:
    "translator_pre"    → translator_pre_node
    "router"            → router_node
    "weather_agent"     → weather_node
    "soil_agent"        → soil_node
    "pest_agent"        → pest_node
    "market_agent"      → market_node
    "crop_advisor"      → crop_advisor_node
    "synthesizer"       → synthesizer_node
    "sowing_agent"      → sowing_node   (only if SOWING in query_intent)
    "translator_post"   → translator_post_node
    "alert_agent"       → alert_node
    "analytics_agent"   → analytics_node

  Edges:
    START → "translator_pre"
    "translator_pre" → "router"

    After "router" → parallel fan-out using conditional_edges + Send():
      def dispatch_agents(state: AgriSageState) -> list[Send]:
          sends = []
          if "WEATHER" in state["query_intent"]:
              sends.append(Send("weather_agent", state))
          if "PEST" in state["query_intent"]:
              sends.append(Send("pest_agent", state))
          if "MARKET" in state["query_intent"]:
              sends.append(Send("market_agent", state))
          if any(i in state["query_intent"]
                 for i in ["FERTILIZER","IRRIGATION","CROP_ADVICE","GENERAL"]):
              sends.append(Send("crop_advisor", state))
          # SoilAgent always runs (needed by fertilizer/irrigation)
          sends.append(Send("soil_agent", state))
          # If no specific intent detected, default to GENERAL
          if not sends:
              sends.append(Send("crop_advisor", state))
          return sends

    All parallel agents → "synthesizer"
    "synthesizer" → conditional: if "SOWING" in intent → "sowing_agent" else → "translator_post"
    "sowing_agent" → "translator_post"
    "translator_post" → "alert_agent"
    "alert_agent" → "analytics_agent"
    "analytics_agent" → END

  Compile:
    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)

  Invoke pattern (in chat router):
    result = await graph.ainvoke(
        initial_state,
        config={"configurable": {"thread_id": farmer_id}}
    )

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ROUTER AGENT SPEC (app/agents/router_agent.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

System prompt (from brain/05_AGENT_PROMPTS.md):
  "You are the RouterAgent for Agri-SAGE Kerala.
   Classify the farmer's query into one or more of these intents ONLY:
   WEATHER, PEST, MARKET, FERTILIZER, IRRIGATION, SOWING, CROP_ADVICE, GENERAL
   Return ONLY valid JSON: {"intents": ["INTENT1", "INTENT2"], "crop": "detected_crop",
                            "crop_stage": "detected_stage"}
   crop: one of [coconut,rice,banana,rubber,tapioca,pepper,cardamom,ginger,turmeric,arecanut,unknown]
   crop_stage: one of [seedling,vegetative,flowering,harvest,unknown]
   Never return anything except the JSON object."

Input: state["farmer_query"] (already translated to English by translator_pre)
Output updates to state: query_intent, crop, crop_stage

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TRANSLATOR AGENT SPEC (app/agents/translator_agent.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

translator_pre_node:
  1. Detect language using Gemini Flash:
     prompt: "Detect the language of this text. Return ONLY one of: ml, en, ta
              Text: {farmer_query}"
  2. If language == "en": pass through unchanged, set state["language"] = "en"
  3. If language == "ml" or "ta": translate to English
     prompt: "Translate this Malayalam/Tamil text to English. Return ONLY the English translation.
              No explanation. Text: {farmer_query}"
  4. Update state: language, farmer_query (now in English for other agents)

translator_post_node:
  1. If state["language"] == "en": final_answer_ml = final_answer_en, return
  2. Translate final_answer_en to Malayalam:
     prompt: "Translate this agricultural advice to natural Malayalam.
              Use simple words a Kerala farmer would understand.
              Do not translate: specific numbers, crop names, chemical names.
              Text: {final_answer_en}"
  3. Update state: final_answer_ml

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SYNTHESIZER AGENT SPEC (app/agents/synthesizer_agent.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

System prompt:
  "You are the SynthesizerAgent for Agri-SAGE Kerala.
   Combine the following expert reports into one clear, actionable answer for a Kerala farmer.
   Rules:
   - Start with the most urgent recommendation
   - Use simple language (farmer may have 8th grade education)
   - Cite which data source each recommendation comes from
   - If any data is null or unavailable, skip that section
   - Maximum 150 words
   - Never contradict KAU (Kerala Agricultural University) Package of Practices
   Expert reports: {agent_outputs}"

Output: state["final_answer_en"] (in English, max 150 words)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GEMINI CALL PATTERN — RATE LIMIT SAFE (15 RPM free tier)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Use this pattern in EVERY agent that calls Gemini:

  import asyncio
  from langchain_google_genai import ChatGoogleGenerativeAI

  llm = ChatGoogleGenerativeAI(
      model="gemini-1.5-flash",   ← exact model string
      google_api_key=settings.GEMINI_API_KEY,
      temperature=0.1,
      max_tokens=1000,
  )

  async def call_gemini_safe(llm, messages: list, max_retries: int = 2) -> str:
      for attempt in range(max_retries):
          try:
              response = await llm.ainvoke(messages)
              return response.content
          except Exception as e:
              err = str(e)
              if "429" in err or "quota" in err.lower() or "rate" in err.lower():
                  wait_sec = 4 * (attempt + 1)
                  await asyncio.sleep(wait_sec)
                  continue
              raise RuntimeError(f"Gemini error: {err}") from e
      raise RuntimeError("Gemini rate limit exceeded after retries — try again in 60s")

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALERT AGENT SPEC (app/agents/alert_agent.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Trigger FCM notification if ANY of these conditions is true:
  RAIN_ALERT:    weather_context["rain_mm_24h"] > 50
  HEAT_ALERT:    weather_context["temp_c"] > 38
  PEST_ALERT:    any alert in pest_alerts with severity == "HIGH"
  PRICE_DROP:    market_data["trend"] == "DOWN" and market_data tracked for >7 days
  SPRAY_WINDOW:  weather_context["advice_flag"] == "SPRAY_RISK"

FCM call (Firebase Admin SDK, free):
  import firebase_admin
  from firebase_admin import messaging
  message = messaging.Message(
      notification=messaging.Notification(title=alert_title, body=alert_body),
      topic=f"district_{state['location']['district'].lower()}",
  )
  messaging.send(message)
  Update state: fcm_triggered = True

If no FCM credentials (dev mode): log the alert message, set fcm_triggered = False

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BRAIN/05_AGENT_PROMPTS.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Create this file with system prompts for all 14 agents.
Each prompt follows this template:
  Agent: <NAME>
  Task: <SPECIFIC_TASK — one sentence>
  Input: <INPUT_FIELDS>
  Output schema: <JSON schema — exact fields>
  Kerala context: <Kerala-specific rules for this agent>
  Fallback: <what to return if data unavailable>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TEST SPEC (tests/test_agents.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Write pytest tests:
  test_router_classifies_weather_query()
    input: "Will it rain tomorrow?"
    assert "WEATHER" in state["query_intent"]

  test_router_classifies_pest_query()
    input: "There are white spots on my coconut leaves"
    assert "PEST" in state["query_intent"]
    assert state["crop"] == "coconut"

  test_translator_detects_malayalam()
    input: "നാളെ മഴ ഉണ്ടാകുമോ?" (will it rain tomorrow in Malayalam)
    assert state["language"] == "ml"
    assert state["farmer_query"] contains English translation

  test_state_merges_parallel_outputs()
    mock weather_node and pest_node running in parallel
    assert agent_outputs contains both "weather" and "pest" keys

  test_graph_compiles_without_error()
    from app.agents.graph import graph
    assert graph is not None

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GITHUB ISSUE PROTOCOL — PHASE 2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After tests pass (pytest tests/test_agents.py -v → 0 failures):

  git checkout dev/m4-agents
  git add -A
  git commit -m "feat(phase-2): 14-agent LangGraph system — parallel fan-out, MemorySaver, Malayalam translation"
  git tag v0.2.0

Create GitHub Issue:
  Title: [Phase 2] LangGraph 14-Agent Orchestration
  Labels: phase-2, agents
  Assign: @M4
  Body: (list all 14 agent files, PROTECTED files skipped, paste test output)

Print: "✅ Phase 2 committed to dev/m4-agents. Issue created. Waiting for team review."
STOP — wait for confirmation before Phase 3.
```

---

## What This Phase Builds

| Agent | Realtime Data |
|---|---|
| RouterAgent | Gemini Flash intent classification |
| TranslatorAgent | Gemini Flash ML/EN/TA |
| WeatherAgent | → WeatherService (Open-Meteo) |
| SoilAgent | → SoilService (NBSS JSON) |
| PestAgent | → pest_alerts table (NBAIR RSS) |
| MarketAgent | → market_prices table (data.gov.in) |
| CropAdvisorAgent | → kau_documents pgvector |
| IrrigationAgent | → weather ET₀ + crop stage |
| FertilizerAgent | → soil NPK + crop stage |
| SowingAgent | → DSSAT subprocess |
| SynthesizerAgent | → all agent_outputs |
| AlertAgent | → FCM push (Firebase) |
| AnalyticsAgent | → farm_analytics table |

## GitHub Issue Created After This Phase

```
Title: [Phase 2] LangGraph 14-Agent Orchestration
Branch: dev/m4-agents
Labels: phase-2, agents
Assign to: M4
```

---

> **Next:** Paste `04-phase3-rag.md` after Issue #2 is reviewed and merged
