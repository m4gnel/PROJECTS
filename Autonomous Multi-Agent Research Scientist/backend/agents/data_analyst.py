import json
from supabase import Client
from .state import AgentState
from .planner import update_agent_run
from model_router import ModelRouter, AllProvidersExhaustedError

async def data_analyst_node(state: AgentState, config: dict):
    supabase: Client = config["configurable"]["supabase"]
    model_router: ModelRouter = config["configurable"].get("data_analyst_router")
    session_id = state["session_id"]
    query = state["query"]
    
    update_agent_run(supabase, session_id, "data_analyst", "running")
    
    if not model_router:
        update_agent_run(supabase, session_id, "data_analyst", "failed", error_detail="Router not configured")
        return {"data_analysis": None}

    # Simulate data fetching & analysis or synthesize from claims
    prompt = f"""
    Act as a Data Analyst. Based on the topic "{query}", identify any publicly available datasets, APIs, or key statistical metrics that would be relevant.
    
    Format the output as a Markdown string with:
    1. Key Metrics & Trends
    2. Recommended Datasets (with descriptions)
    
    Do not output JSON.
    """
    
    try:
        response = await model_router.call(prompt)
        text = response.text.strip()
        
        update_agent_run(supabase, session_id, "data_analyst", "done", raw_output={"analysis": text})
        return {"data_analysis": text}

    except AllProvidersExhaustedError as e:
        update_agent_run(supabase, session_id, "data_analyst", "degraded", error_detail=str(e))
        return {"status": "degraded", "errors": [f"Data analyst degraded: {e}"]}
    except Exception as e:
        update_agent_run(supabase, session_id, "data_analyst", "failed", error_detail=str(e))
        return {"status": "failed", "errors": [f"Data analyst failed: {e}"]}
