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
