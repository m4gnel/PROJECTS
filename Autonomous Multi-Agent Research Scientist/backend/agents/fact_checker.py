import json
from supabase import Client
from .state import AgentState
from .planner import update_agent_run
from model_router import ModelRouter, AllProvidersExhaustedError

async def fact_checker_node(state: AgentState, config: dict):
    supabase: Client = config["configurable"]["supabase"]
    model_router: ModelRouter = config["configurable"]["fact_checker_router"]
    session_id = state["session_id"]
    sources = state.get("sources", [])
    
    update_agent_run(supabase, session_id, "fact_checker", "running")
    
    if not sources:
        update_agent_run(supabase, session_id, "fact_checker", "degraded", error_detail="No sources to check")
        return {"claims": []}

    # Format sources for LLM
    sources_text = "\n".join([f"Source {i+1} [ID: {s.get('id')}]: {s.get('title')} - {s.get('url')}" for i, s in enumerate(sources)])
    
    prompt = f"""
    Based on the following sources retrieved for the query "{state['query']}", extract 3 key factual claims.
    For each claim, cross-reference it against the sources and assign a verification status:
    - "verified": corroborated by >= 2 independent sources
    - "partially_verified": corroborated by 1 source
    - "unverified": not corroborated by any provided source
    - "contradicted": sources directly conflict

    Sources:
    {sources_text}

    Return a JSON array of objects with the exact keys:
    - "claim_text": string
    - "verification_status": string (one of the 4 exact enum values)
    - "supporting_source_ids": list of strings (the Source IDs)
    - "conflicting_source_ids": list of strings (the Source IDs)
    
    Output ONLY valid JSON.
    """
    
    try:
        response = await model_router.call(prompt)
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].strip()
            
        claims_data = json.loads(text)
        
        processed_claims = []
        for c in claims_data:
            # Insert into DB
            db_claim = {
                "session_id": session_id,
                "claim_text": c.get("claim_text", ""),
                "verification_status": c.get("verification_status", "unverified"),
                "supporting_source_ids": c.get("supporting_source_ids", []),
                "conflicting_source_ids": c.get("conflicting_source_ids", [])
            }
            res = supabase.table("claims").insert(db_claim).execute()
            if res.data:
                processed_claims.append(res.data[0])
                
        update_agent_run(supabase, session_id, "fact_checker", "done", raw_output={"claims": processed_claims})
        return {"claims": processed_claims}

    except AllProvidersExhaustedError as e:
        update_agent_run(supabase, session_id, "fact_checker", "degraded", error_detail=str(e))
        return {"status": "degraded", "errors": [f"Fact checker degraded: {e}"]}
    except Exception as e:
        update_agent_run(supabase, session_id, "fact_checker", "failed", error_detail=str(e))
        return {"status": "failed", "errors": [f"Fact checker failed: {e}"]}
