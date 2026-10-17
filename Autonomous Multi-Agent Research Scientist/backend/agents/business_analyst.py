import json
from supabase import Client
from .state import AgentState
from .planner import update_agent_run
from model_router import ModelRouter, AllProvidersExhaustedError

async def business_analyst_node(state: AgentState, config: dict):
    supabase: Client = config["configurable"]["supabase"]
    model_router: ModelRouter = config["configurable"].get("business_router")
    session_id = state["session_id"]
    query = state["query"]
    claims = state.get("claims", [])
    
    update_agent_run(supabase, session_id, "business_analyst", "running")
    
    if not model_router:
        update_agent_run(supabase, session_id, "business_analyst", "failed", error_detail="Router not configured")
        return {"market_analysis": None}

    claims_text = "\n".join([f"- {c['claim_text']}" for c in claims])

    prompt = f"""
    Act as a Business Analyst evaluating the market for: "{query}".
    
    Based on these research claims:
    {claims_text}
    
    Estimate the TAM/SAM/SOM (Total Addressable, Serviceable Available, Serviceable Obtainable Market) and list the top 3 competitors in this space.
    Return a JSON object with keys:
    - "tam_estimate": string
    - "sam_estimate": string
    - "som_estimate": string
    - "competitors": list of strings (competitor names)
    - "assumptions": list of strings (why you arrived at these estimates)
    
    Output ONLY valid JSON.
    """
    
    try:
        response = await model_router.call(prompt)
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].strip()
            
        analysis = json.loads(text)
        
        # We store the raw market analysis as a dict in the state
        # In a more advanced implementation we could map this to a specific DB table
        update_agent_run(supabase, session_id, "business_analyst", "done", raw_output=analysis)
        return {"market_analysis": analysis}

    except AllProvidersExhaustedError as e:
        update_agent_run(supabase, session_id, "business_analyst", "degraded", error_detail=str(e))
        return {"status": "degraded", "errors": [f"Business analyst degraded: {e}"]}
    except Exception as e:
        update_agent_run(supabase, session_id, "business_analyst", "failed", error_detail=str(e))
        return {"status": "failed", "errors": [f"Business analyst failed: {e}"]}
