import json
from supabase import Client
from .state import AgentState
from .planner import update_agent_run
from model_router import ModelRouter, AllProvidersExhaustedError

async def evaluator_node(state: AgentState, config: dict):
    supabase: Client = config["configurable"]["supabase"]
    model_router: ModelRouter = config["configurable"].get("evaluator_router")
    session_id = state["session_id"]
    query = state["query"]
    claims = state.get("claims", [])
    
    update_agent_run(supabase, session_id, "evaluator", "running")
    
    if not model_router:
        update_agent_run(supabase, session_id, "evaluator", "failed", error_detail="Router not configured")
        return {"confidence_score": 0}

    claims_text = "\n".join([f"- {c['claim_text']} ({c['verification_status']})" for c in claims])

    prompt = f"""
    Evaluate the overall confidence of the research conducted for the query: "{query}".
    
    Claims:
    {claims_text}
    
    Assign a confidence score from 0 to 100 based on the verification status of the claims.
    Return ONLY a JSON object: {{"confidence_score": <integer>}}
    """
    
    try:
        response = await model_router.call(prompt)
        text = response.text.strip()
        if "{" in text and "}" in text:
            text = text[text.find("{"):text.rfind("}")+1]
            
        data = json.loads(text)
        score = data.get("confidence_score", 50)
        
        # Update session confidence score
        supabase.table("research_sessions").update({"confidence_score": score}).eq("id", session_id).execute()
        
        update_agent_run(supabase, session_id, "evaluator", "done", raw_output={"confidence_score": score})
        return {"confidence_score": score}

    except AllProvidersExhaustedError as e:
        update_agent_run(supabase, session_id, "evaluator", "degraded", error_detail=str(e))
        return {"status": "degraded", "errors": [f"Evaluator degraded: {e}"]}
    except Exception as e:
        update_agent_run(supabase, session_id, "evaluator", "failed", error_detail=str(e))
        return {"status": "failed", "errors": [f"Evaluator failed: {e}"]}
