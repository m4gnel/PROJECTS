import json
from supabase import Client
from .state import AgentState
from .planner import update_agent_run
from model_router import ModelRouter, AllProvidersExhaustedError

async def startup_generator_node(state: AgentState, config: dict):
    supabase: Client = config["configurable"]["supabase"]
    model_router: ModelRouter = config["configurable"].get("startup_router")
    session_id = state["session_id"]
    query = state["query"]
    market_analysis = state.get("market_analysis", {})
    
    update_agent_run(supabase, session_id, "startup_generator", "running")
    
    if not model_router:
        update_agent_run(supabase, session_id, "startup_generator", "failed", error_detail="Router not configured")
        return {"startup_concepts": []}

    prompt = f"""
    Act as a Startup Generator for the topic: "{query}".
    
    Market Context:
    {json.dumps(market_analysis)}
    
    Propose 2-3 ranked startup concepts. 
    Return a JSON array of objects with keys:
    - "rank": integer (1, 2, or 3)
    - "name": string (Concept name)
    - "target_user": string
    - "monetization_model": string
    - "differentiator": string (How it beats existing players)
    
    Output ONLY valid JSON.
    """
    
    try:
        response = await model_router.call(prompt)
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].strip()
            
        concepts_data = json.loads(text)
        
        processed_concepts = []
        for c in concepts_data:
            db_concept = {
                "session_id": session_id,
                "rank": c.get("rank", 1),
                "name": c.get("name", ""),
                "target_user": c.get("target_user", ""),
                "monetization_model": c.get("monetization_model", ""),
                "differentiator": c.get("differentiator", "")
            }
            res = supabase.table("startup_concepts").insert(db_concept).execute()
            if res.data:
                processed_concepts.append(res.data[0])
                
        update_agent_run(supabase, session_id, "startup_generator", "done", raw_output={"startup_concepts": processed_concepts})
        return {"startup_concepts": processed_concepts}

    except AllProvidersExhaustedError as e:
        update_agent_run(supabase, session_id, "startup_generator", "degraded", error_detail=str(e))
        return {"status": "degraded", "errors": [f"Startup generator degraded: {e}"]}
    except Exception as e:
        update_agent_run(supabase, session_id, "startup_generator", "failed", error_detail=str(e))
        return {"status": "failed", "errors": [f"Startup generator failed: {e}"]}
