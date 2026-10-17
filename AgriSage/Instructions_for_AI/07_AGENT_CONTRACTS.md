# 07_AGENT_CONTRACTS.md — Exact Agent Signatures & LangGraph Structure
# ⚠️ ALL 14 AGENTS MUST MATCH THESE EXACT SIGNATURES. DO NOT INVENT NEW ONES.

---

## backend/app/agents/state.py — AgriState Definition (COPY EXACTLY)

```python
from typing import TypedDict, Annotated, Optional
from operator import add

class WeatherData(TypedDict):
    temperature: float          # Celsius
    humidity: float             # percentage
    rainfall_mm: float
    wind_speed: float           # km/h
    uv_index: float
    forecast_7day: list[dict]   # [{date, max_temp, min_temp, rainfall_mm}]

class SoilData(TypedDict):
    soil_type: str              # "laterite", "alluvial", "red_loam", "coastal_sandy"
    ph: float
    nitrogen_kg_ha: float
    phosphorus_kg_ha: float
    potassium_kg_ha: float
    organic_matter_percent: float

class CropInfo(TypedDict):
    crop_name: str              # e.g., "rice", "coconut", "banana", "pepper"
    variety: str
    sowing_date: str            # ISO format YYYY-MM-DD
    current_growth_stage: str
    field_area_hectares: float

class AgriState(TypedDict):
    # Input
    query: str
    language: str               # "ml", "en", "ta", "hi"
    farmer_id: str
    field_id: Optional[str]
    location_lat: float
    location_lon: float
    crop_info: Optional[CropInfo]

    # Data collected by agents (Annotated[list, add] = append-only)
    weather_data: Optional[WeatherData]
    soil_data: Optional[SoilData]
    ndvi_value: Optional[float]       # -1.0 to 1.0 from satellite
    pest_alerts: Annotated[list[str], add]
    market_prices: Annotated[list[dict], add]
    dssat_result: Optional[dict]      # crop simulation output

    # Intermediate results (Annotated[list, add] = append-only)
    agent_findings: Annotated[list[str], add]

    # Final output
    advisory_text: str          # in the farmer's language
    alerts_generated: Annotated[list[dict], add]
    confidence_score: float     # 0.0 to 1.0

    # Routing
    agents_needed: list[str]    # set by orchestrator
    agents_completed: Annotated[list[str], add]
    error_messages: Annotated[list[str], add]
```

---

## backend/app/agents/graph.py — Graph Construction (COPY EXACTLY)

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from .state import AgriState
from .orchestrator import orchestrator_node, should_continue
from .weather_agent import weather_node
from .soil_agent import soil_node
from .crop_agent import crop_node
from .pest_agent import pest_node
from .market_agent import market_node
from .dssat_agent import dssat_node
from .satellite_agent import satellite_node
from .irrigation_agent import irrigation_node
from .fertilizer_agent import fertilizer_node
from .harvest_agent import harvest_node
from .market_timing_agent import market_timing_node
from .rag_agent import rag_node
from .translator_agent import translator_node
from .alert_agent import alert_node

def build_graph() -> object:
    workflow = StateGraph(AgriState)

    # Add all nodes
    workflow.add_node("orchestrator", orchestrator_node)
    workflow.add_node("weather", weather_node)
    workflow.add_node("soil", soil_node)
    workflow.add_node("crop", crop_node)
    workflow.add_node("pest", pest_node)
    workflow.add_node("market", market_node)
    workflow.add_node("dssat", dssat_node)
    workflow.add_node("satellite", satellite_node)
    workflow.add_node("irrigation", irrigation_node)
    workflow.add_node("fertilizer", fertilizer_node)
    workflow.add_node("harvest", harvest_node)
    workflow.add_node("market_timing", market_timing_node)
    workflow.add_node("rag", rag_node)
    workflow.add_node("translator", translator_node)
    workflow.add_node("alert", alert_node)

    # Entry point
    workflow.add_edge(START, "orchestrator")

    # Orchestrator routes to agents based on agents_needed
    workflow.add_conditional_edges(
        "orchestrator",
        should_continue,
        {
            "weather": "weather",
            "soil": "soil",
            "crop": "crop",
            "pest": "pest",
            "market": "market",
            "dssat": "dssat",
            "satellite": "satellite",
            "rag": "rag",
            "alert": "alert",
            "translator": "translator",
            "end": END,
        }
    )

    # All data-collecting agents route back to orchestrator
    for node in ["weather", "soil", "crop", "pest", "market", "dssat",
                 "satellite", "irrigation", "fertilizer", "harvest",
                 "market_timing", "rag"]:
        workflow.add_edge(node, "orchestrator")

    # Alert and translator are final steps
    workflow.add_edge("alert", "translator")
    workflow.add_edge("translator", END)

    checkpointer = MemorySaver()
    return workflow.compile(checkpointer=checkpointer)

# Singleton — import this in routers
agri_graph = build_graph()
```

---

## Agent Function Signatures (ALL 14)

### Agent 01: weather_agent.py
```python
from .state import AgriState

async def weather_node(state: AgriState) -> dict:
    """
    Fetches from Open-Meteo API using state.location_lat, state.location_lon.
    Returns: {"weather_data": WeatherData, "agents_completed": ["weather"]}
    Data source: https://api.open-meteo.com/v1/forecast
    Parameters: latitude, longitude, hourly=[temperature_2m,precipitation,windspeed_10m,uv_index]
                daily=[temperature_2m_max,temperature_2m_min,precipitation_sum], forecast_days=7
    Never raises — returns error in error_messages on failure.
    """
```

### Agent 02: soil_agent.py
```python
async def soil_node(state: AgriState) -> dict:
    """
    Looks up soil data from NBSS API or local cache for Kerala.
    Fallback: hard-coded laterite soil defaults for Kerala if API fails.
    Returns: {"soil_data": SoilData, "agents_completed": ["soil"]}
    Kerala default: laterite, ph=5.8, low N, medium P/K, high organic matter
    """
```

### Agent 03: crop_agent.py
```python
async def crop_node(state: AgriState) -> dict:
    """
    Analyzes crop health from state.crop_info + weather + soil data.
    Uses Gemini Flash to generate crop health assessment.
    Returns: {"agent_findings": ["crop: <assessment>"], "agents_completed": ["crop"]}
    """
```

### Agent 04: pest_agent.py
```python
async def pest_node(state: AgriState) -> dict:
    """
    Fetches NBAIR RSS feed for pest/disease alerts relevant to:
    - state.location_lat, state.location_lon (Kerala region filter)
    - state.crop_info.crop_name (crop-specific pest filter)
    Returns: {"pest_alerts": [<alert strings>], "agents_completed": ["pest"]}
    RSS URL: from settings.NBAIR_RSS_URL
    """
```

### Agent 05: market_agent.py
```python
async def market_node(state: AgriState) -> dict:
    """
    Fetches commodity prices from data.gov.in API.
    Filters by: Kerala APMCs + state.crop_info.crop_name
    API endpoint: https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070
    Returns: {"market_prices": [{commodity, market, price, date}], "agents_completed": ["market"]}
    """
```

### Agent 06: dssat_agent.py
```python
async def dssat_node(state: AgriState) -> dict:
    """
    Runs DSSAT crop simulation via subprocess.
    Input: soil_data + weather_data + crop_info
    Only runs if: crop_name in ["rice", "maize", "wheat", "soybean"] (DSSAT supported)
    Subprocess: calls utils/dssat_runner.py
    Returns: {"dssat_result": {yield_kg_ha, days_to_maturity, water_stress}, "agents_completed": ["dssat"]}
    On unsupported crop: returns dssat_result=None, no error
    """
```

### Agent 07: satellite_agent.py
```python
async def satellite_node(state: AgriState) -> dict:
    """
    Fetches NDVI from NASA APPEEARS API or MODIS data.
    Endpoint: NASA EarthData for MODIS MOD13Q1 product
    Input: state.location_lat, state.location_lon, bounding box ±0.05 degrees
    Returns: {"ndvi_value": float (-1.0 to 1.0), "agents_completed": ["satellite"]}
    Interpretation stored in agent_findings: {"satellite": "NDVI <value>: <health status>"}
    NDVI thresholds: <0.2=bare/stressed, 0.2-0.4=sparse, 0.4-0.6=moderate, >0.6=healthy
    """
```

### Agent 08: irrigation_agent.py
```python
async def irrigation_node(state: AgriState) -> dict:
    """
    Calculates irrigation schedule from ETo (Evapotranspiration).
    Formula: ETo from Penman-Monteith simplified using weather_data
    Input: weather_data + soil_data + crop_info
    Returns: {"agent_findings": ["irrigation: <schedule>"], "agents_completed": ["irrigation"]}
    Output format: "Irrigate <X> mm every <Y> days for next <Z> days"
    """
```

### Agent 09: fertilizer_agent.py
```python
async def fertilizer_node(state: AgriState) -> dict:
    """
    Recommends fertilizer based on soil_data NPK deficit + crop requirement.
    Kerala crop NPK requirements stored as constants in this file.
    Returns: {"agent_findings": ["fertilizer: <recommendation>"], "agents_completed": ["fertilizer"]}
    """
```

### Agent 10: harvest_agent.py
```python
async def harvest_node(state: AgriState) -> dict:
    """
    Predicts harvest date from sowing_date + growth_stage + weather forecast.
    Uses crop-specific Growing Degree Days (GDD) model.
    Returns: {"agent_findings": ["harvest: Estimated harvest on <date>"], "agents_completed": ["harvest"]}
    """
```

### Agent 11: market_timing_agent.py
```python
async def market_timing_node(state: AgriState) -> dict:
    """
    Recommends when to sell based on price trend from market_prices history.
    Simple 7-day moving average trend analysis.
    Returns: {"agent_findings": ["market_timing: <sell/hold recommendation>"], "agents_completed": ["market_timing"]}
    """
```

### Agent 12: rag_agent.py
```python
async def rag_node(state: AgriState) -> dict:
    """
    Vector search over KAU (Kerala Agricultural University) PDF chunks in pgvector.
    Query embedding: multilingual-e5-large with "query: " prefix on state.query
    Search: top-5 chunks by cosine similarity
    Returns: {"agent_findings": ["rag: <relevant KAU advice>"], "agents_completed": ["rag"]}
    """
```

### Agent 13: translator_agent.py
```python
async def translator_node(state: AgriState) -> dict:
    """
    Translates advisory_text to state.language using Gemini Flash.
    Only runs if state.language != "en"
    System prompt: "You are an agricultural translator. Translate to {language}.
                   Use simple words. Keep technical terms in English. Be concise."
    Returns: {"advisory_text": "<translated text>", "agents_completed": ["translator"]}
    Language codes: ml=Malayalam, ta=Tamil, hi=Hindi, en=English (no translation)
    """
```

### Agent 14: alert_agent.py
```python
async def alert_node(state: AgriState) -> dict:
    """
    Generates structured alerts from pest_alerts + agent_findings.
    Severity levels: CRITICAL, WARNING, INFO, SUCCESS
    CRITICAL: disease outbreak, severe weather, immediate irrigation needed
    WARNING: pest risk, price drop >20%, water stress
    INFO: market update, harvest reminder
    SUCCESS: crop health normal, no threats detected
    Returns: {
        "alerts_generated": [{id, severity, title, message, timestamp}],
        "advisory_text": "<synthesized advisory>",
        "confidence_score": float,
        "agents_completed": ["alert"]
    }
    """
```

---

## Orchestrator Contract

```python
# orchestrator.py

def orchestrator_node(state: AgriState) -> dict:
    """
    First pass: parse query → determine which agents are needed.
    Subsequent passes: check agents_completed → route to next needed agent.
    Uses simple keyword matching + Gemini Flash for complex routing.
    
    Query → agents mapping:
    "weather" / "rain" / "mausam" → ["weather"]
    "soil" / "matti" → ["soil"]
    "pest" / "disease" / "keedam" → ["pest", "rag"]
    "fertilizer" / "valam" → ["soil", "fertilizer", "rag"]
    "irrigation" / "jeelam" → ["weather", "irrigation"]
    "harvest" / "vikasam" → ["weather", "crop", "harvest"]
    "price" / "market" / "vila" → ["market", "market_timing"]
    "general" / "help" → ["weather", "crop", "rag"]
    Default (unknown) → ["weather", "crop", "rag", "alert"]
    
    Always adds "alert" and "translator" at the end.
    """

def should_continue(state: AgriState) -> str:
    """
    Routing function for conditional edges.
    Returns the name of the next agent to run, or "end".
    Logic: find first agent in agents_needed not yet in agents_completed.
    Special: "alert" always runs before "translator". "translator" runs last.
    """
```

---

## How to Call the Graph from a Router

```python
# In backend/app/routers/chat.py — use this pattern exactly

async def process_chat(request: ChatRequest, db: AsyncSession) -> ChatResponse:
    config = {"configurable": {"thread_id": request.session_id}}
    
    initial_state: AgriState = {
        "query": request.message,
        "language": request.language,
        "farmer_id": str(request.farmer_id),
        "field_id": str(request.field_id) if request.field_id else None,
        "location_lat": request.latitude,
        "location_lon": request.longitude,
        "crop_info": request.crop_info,
        "weather_data": None,
        "soil_data": None,
        "ndvi_value": None,
        "pest_alerts": [],
        "market_prices": [],
        "dssat_result": None,
        "agent_findings": [],
        "advisory_text": "",
        "alerts_generated": [],
        "confidence_score": 0.0,
        "agents_needed": [],
        "agents_completed": [],
        "error_messages": [],
    }
    
    result = await agri_graph.ainvoke(initial_state, config=config)
    return ChatResponse(
        message=result["advisory_text"],
        alerts=result["alerts_generated"],
        confidence=result["confidence_score"],
        session_id=request.session_id,
    )
```
