from .state import AgriState


# Keyword → agent mapping
KEYWORD_AGENT_MAP = [
    (["weather", "rain", "mausam", "mazha", "kalavarsham"], ["weather"]),
    (["soil", "matti", "mannu"], ["soil"]),
    (["pest", "disease", "keedam", "roga"], ["pest", "rag"]),
    (["fertilizer", "valam", "feeder"], ["soil", "fertilizer", "rag"]),
    (["irrigation", "jeelam", "water", "vellam"], ["weather", "irrigation"]),
    (["harvest", "vikasam", "grain", "wheat"], ["weather", "crop", "harvest"]),
    (["price", "market", "vila", "moolya", "sell", "vilkka"], ["market", "market_timing"]),
    (["satellite", "ndvi", "field health"], ["satellite"]),
    (["general", "help", "sahayam"], ["weather", "crop", "rag"]),
]


def _determine_agents(query: str) -> list[str]:
    query_lower = query.lower()
    for keywords, agents in KEYWORD_AGENT_MAP:
        if any(k in query_lower for k in keywords):
            return agents
    # Default: broad assessment
    return ["weather", "crop", "rag", "alert"]


def orchestrator_node(state: AgriState) -> dict:
    """
    First pass: parse query → determine which agents are needed.
    Subsequent passes: check agents_completed → route to next needed agent.
    Always adds "alert" and "translator" at the end.
    """
    agents_needed = list(state.get("agents_needed", []))
    agents_completed = list(state.get("agents_completed", []))

    # First call: determine agents
    if not agents_needed:
        base_agents = _determine_agents(state["query"])
        # Always ensure alert + translator at end
        agents_needed = base_agents
        if "alert" not in agents_needed:
            agents_needed.append("alert")
        if "translator" not in agents_needed:
            agents_needed.append("translator")

    return {"agents_needed": agents_needed}


def should_continue(state: AgriState) -> str:
    """
    Routing function for conditional edges.
    Returns the name of the next agent to run, or "end".
    Special: "alert" always runs before "translator". "translator" runs last.
    """
    agents_needed = state.get("agents_needed", [])
    agents_completed = list(state.get("agents_completed", []))

    # Find first uncompleted agent
    for agent in agents_needed:
        if agent not in agents_completed:
            # Only route to agents with conditional edges
            if agent in ["weather", "soil", "crop", "pest", "market", "dssat",
                         "satellite", "rag", "alert", "translator"]:
                return agent
            # For agents routed via direct edges (irrigation, fertilizer, harvest,
            # market_timing) we skip them here and handle via direct edges
            # Mark as completed to avoid infinite loop
            agents_completed.append(agent)

    return "end"
