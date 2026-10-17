import logging
from typing import List, Dict, Any
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Send

from backend.agents.state import AgriSageState
from backend.agents.router_agent import router_node
from backend.agents.translator_agent import translator_pre_node, translator_post_node
from backend.agents.weather_agent import weather_node
from backend.agents.soil_agent import soil_node
from backend.agents.pest_agent import pest_node
from backend.agents.market_agent import market_node
from backend.agents.crop_advisor_agent import crop_advisor_node
from backend.agents.irrigation_agent import irrigation_node
from backend.agents.fertilizer_agent import fertilizer_node
from backend.agents.sowing_agent import sowing_node
from backend.agents.synthesizer_agent import synthesizer_node
from backend.agents.alert_agent import alert_node
from backend.agents.analytics_agent import analytics_node

logger = logging.getLogger(__name__)


def dispatch_agents(state: AgriSageState) -> List[Send]:
    sends = []
    intents = state.get("query_intent", [])

    if "WEATHER" in intents:
        sends.append(Send("weather_agent", state))
    if "PEST" in intents:
        sends.append(Send("pest_agent", state))
    if "MARKET" in intents:
        sends.append(Send("market_agent", state))
    if any(i in intents for i in ["FERTILIZER", "IRRIGATION", "CROP_ADVICE", "GENERAL"]):
        sends.append(Send("crop_advisor", state))
        if "FERTILIZER" in intents:
            sends.append(Send("fertilizer_agent", state))
        if "IRRIGATION" in intents:
            sends.append(Send("irrigation_agent", state))

    # SoilAgent always runs
    sends.append(Send("soil_agent", state))

    if not sends:
        sends.append(Send("crop_advisor", state))

    return sends


def route_post_synthesis(state: AgriSageState) -> str:
    intents = state.get("query_intent", [])
    if "SOWING" in intents:
        return "sowing_agent"
    return "translator_post"


# Build StateGraph using exact LangGraph 1.0.8 API
builder = StateGraph(AgriSageState)

# Add all nodes
builder.add_node("translator_pre", translator_pre_node)
builder.add_node("router", router_node)
builder.add_node("weather_agent", weather_node)
builder.add_node("soil_agent", soil_node)
builder.add_node("pest_agent", pest_node)
builder.add_node("market_agent", market_node)
builder.add_node("crop_advisor", crop_advisor_node)
builder.add_node("fertilizer_agent", fertilizer_node)
builder.add_node("irrigation_agent", irrigation_node)
builder.add_node("synthesizer", synthesizer_node)
builder.add_node("sowing_agent", sowing_node)
builder.add_node("translator_post", translator_post_node)
builder.add_node("alert_agent", alert_node)
builder.add_node("analytics_agent", analytics_node)

# Control flow edges
builder.add_edge(START, "translator_pre")
builder.add_edge("translator_pre", "router")

# Parallel fan-out after router
builder.add_conditional_edges("router", dispatch_agents)

# Fan-in into synthesizer
builder.add_edge("weather_agent", "synthesizer")
builder.add_edge("soil_agent", "synthesizer")
builder.add_edge("pest_agent", "synthesizer")
builder.add_edge("market_agent", "synthesizer")
builder.add_edge("crop_advisor", "synthesizer")
builder.add_edge("fertilizer_agent", "synthesizer")
builder.add_edge("irrigation_agent", "synthesizer")

# Post synthesis routing
builder.add_conditional_edges("synthesizer", route_post_synthesis, {
    "sowing_agent": "sowing_agent",
    "translator_post": "translator_post"
})
builder.add_edge("sowing_agent", "translator_post")
builder.add_edge("translator_post", "alert_agent")
builder.add_edge("alert_agent", "analytics_agent")
builder.add_edge("analytics_agent", END)

# Compile graph with MemorySaver checkpointer
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)
