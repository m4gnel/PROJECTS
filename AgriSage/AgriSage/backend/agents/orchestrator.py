import time
import asyncio
from typing import Dict, Any
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from backend.agents.state import AgriSAGEState
from backend.agents.intake import IntakeAgent
from backend.agents.vision import VisionAgent
from backend.agents.weather import WeatherAgent
from backend.agents.crop_stage import CropStageAgent
from backend.agents.knowledge import KnowledgeAgent
from backend.agents.critic import CriticAgent
from backend.agents.scheme import SchemeAgent
from backend.agents.simulation import SimulationAgent
from backend.agents.decision import DecisionAgent
from backend.agents.explanation import ExplanationAgent

# Instantiate agent singletons
intake_agent = IntakeAgent()
vision_agent = VisionAgent()
weather_agent = WeatherAgent()
crop_stage_agent = CropStageAgent()
knowledge_agent = KnowledgeAgent()
critic_agent = CriticAgent()
scheme_agent = SchemeAgent()
simulation_agent = SimulationAgent()
decision_agent = DecisionAgent()
explanation_agent = ExplanationAgent()


# Node wrapper functions returning isolated state updates for parallel execution in LangGraph
async def intake_node(state: AgriSAGEState) -> dict:
    start_ms = state.get("pipeline_start_ms") or int(time.time() * 1000)
    res = await intake_agent.run(state)
    return {
        "crop": res.get("crop"),
        "farm_state": res.get("farm_state"),
        "language": res.get("language", "ml"),
        "pipeline_start_ms": start_ms,
    }

async def vision_node(state: AgriSAGEState) -> dict:
    res = await vision_agent.run(state)
    return {"vision_result": res.get("vision_result")}

async def weather_node(state: AgriSAGEState) -> dict:
    res = await weather_agent.run(state)
    return {"weather_result": res.get("weather_result")}

async def crop_stage_node(state: AgriSAGEState) -> dict:
    res = await crop_stage_agent.run(state)
    return {"crop_stage_result": res.get("crop_stage_result")}

async def knowledge_node(state: AgriSAGEState) -> dict:
    res = await knowledge_agent.run(state)
    return {"knowledge_result": res.get("knowledge_result")}

async def critic_node(state: AgriSAGEState) -> dict:
    res = await critic_agent.run(state)
    conf_st = res.get("confidence_state") or (res.get("critic_result") or {}).get("confidence_state")
    print(f"[DEBUG critic_node] conf_st = {conf_st}")
    return {
        "critic_result": res.get("critic_result"),
        "confidence_state": conf_st or "CONFIRMED",
        "run_simulation": res.get("run_simulation", False)
    }


async def scheme_node(state: AgriSAGEState) -> dict:
    res = await scheme_agent.run(state)
    return {"scheme_result": res.get("scheme_result")}

async def simulation_node(state: AgriSAGEState) -> dict:
    res = await simulation_agent.run(state)
    return {"simulation_result": res.get("simulation_result")}

async def decision_node(state: AgriSAGEState) -> dict:
    res = await decision_agent.run(state)
    return {"decision_result": res.get("decision_result")}

async def explanation_node(state: AgriSAGEState) -> dict:
    res = await explanation_agent.run(state)
    gen_ms = None
    if state.get("pipeline_start_ms"):
        gen_ms = int(time.time() * 1000) - state["pipeline_start_ms"]
    return {
        "advisory": res.get("advisory"),
        "generation_ms": gen_ms or res.get("generation_ms"),
        "confidence_state": state.get("confidence_state") or "CONFIRMED"
    }







# Router condition for critic node
def route_critic(state: AgriSAGEState) -> list[str]:
    if state.get("run_simulation", False):
        return ["scheme", "simulation"]
    return ["scheme"]


# Build StateGraph using LangGraph 1.0.8 API
builder = StateGraph(AgriSAGEState)

# Add all nodes
builder.add_node("intake", intake_node)
builder.add_node("vision", vision_node)
builder.add_node("weather", weather_node)
builder.add_node("crop_stage", crop_stage_node)
builder.add_node("knowledge", knowledge_node)
builder.add_node("critic", critic_node)
builder.add_node("scheme", scheme_node)
builder.add_node("simulation", simulation_node)
builder.add_node("decision", decision_node)
builder.add_node("explanation", explanation_node)

# Flow edges: Intake -> Vision -> Weather -> CropStage -> Knowledge -> Critic -> Scheme -> Simulation -> Decision -> Explanation
builder.add_edge(START, "intake")
builder.add_edge("intake", "vision")
builder.add_edge("vision", "weather")
builder.add_edge("weather", "crop_stage")
builder.add_edge("crop_stage", "knowledge")
builder.add_edge("knowledge", "critic")
builder.add_edge("critic", "scheme")
builder.add_edge("scheme", "simulation")
builder.add_edge("simulation", "decision")
builder.add_edge("decision", "explanation")
builder.add_edge("explanation", END)


# Compile with MemorySaver
memory = MemorySaver()
advisory_graph = builder.compile(checkpointer=memory)


async def run_advisory_pipeline(initial_state: AgriSAGEState, thread_id: str) -> AgriSAGEState:
    """Run advisory pipeline with 15-second timeout."""
    config = {"configurable": {"thread_id": thread_id}}
    try:
        raw_res = await asyncio.wait_for(
            advisory_graph.ainvoke(initial_state, config=config),
            timeout=15.0
        )

        snapshot = advisory_graph.get_state(config)

        res = dict(raw_res) if isinstance(raw_res, dict) else {}
        if snapshot and snapshot.values:
            res.update(dict(snapshot.values))

        crit_res = res.get("critic_result") or {}
        conf_state = res.get("confidence_state") or crit_res.get("confidence_state") or "CONFIRMED"
        res["confidence_state"] = conf_state
        res["critic_result"] = crit_res or {"confidence_state": conf_state, "safe_to_act": True}

        # Update initial_state in place and return res
        initial_state.update(res)
        return initial_state
    except asyncio.TimeoutError:
        initial_state["errors"] = initial_state.get("errors", []) + ["Pipeline timeout after 10s"]
        initial_state["generation_ms"] = -1
        return initial_state





