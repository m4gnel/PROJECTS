import json
from supabase import Client
from .state import AgentState
from .planner import update_agent_run
from model_router import ModelRouter, AllProvidersExhaustedError

async def technical_architect_node(state: AgentState, config: dict):
    supabase: Client = config["configurable"]["supabase"]
    model_router: ModelRouter = config["configurable"].get("architect_router")
    session_id = state["session_id"]
    query = state["query"]
    concepts = state.get("startup_concepts", [])
    
    update_agent_run(supabase, session_id, "technical_architect", "running")
    
    if not model_router:
        update_agent_run(supabase, session_id, "technical_architect", "failed", error_detail="Router not configured")
        return {"technical_architecture": None}

    # Find top concept
    top_concept = next((c for c in concepts if c["rank"] == 1), None)
    if not top_concept:
        top_concept = {"name": "General Architecture for " + query, "differentiator": "N/A"}

    prompt = f"""
    Act as a Technical Architect. Design a high-level architecture for the following startup concept:
    Name: {top_concept['name']}
    Differentiator: {top_concept['differentiator']}
    
    Provide:
    1. A short textual description of the architecture.
    2. Recommended technology stack.
    3. A Mermaid.js diagram representing the architecture (enclosed in ```mermaid ... ```).
    4. A phased implementation roadmap (Phase 1, Phase 2, Phase 3).
    
    Format the output as a clean Markdown string. Do not output JSON.
    """
    
    try:
        response = await model_router.call(prompt)
        text = response.text.strip()
        
        update_agent_run(supabase, session_id, "technical_architect", "done", raw_output={"architecture": text})
        return {"technical_architecture": text}

    except AllProvidersExhaustedError as e:
        update_agent_run(supabase, session_id, "technical_architect", "degraded", error_detail=str(e))
        return {"status": "degraded", "errors": [f"Technical architect degraded: {e}"]}
    except Exception as e:
        update_agent_run(supabase, session_id, "technical_architect", "failed", error_detail=str(e))
        return {"status": "failed", "errors": [f"Technical architect failed: {e}"]}
