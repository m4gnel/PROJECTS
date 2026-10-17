import json
from supabase import Client
from .state import AgentState
from .planner import update_agent_run
from model_router import ModelRouter, AllProvidersExhaustedError

async def critic_node(state: AgentState, config: dict):
    supabase: Client = config["configurable"]["supabase"]
    model_router: ModelRouter = config["configurable"].get("critic_router")
    session_id = state["session_id"]
    query = state["query"]
    claims = state.get("claims", [])
    
    update_agent_run(supabase, session_id, "critic", "running")
    
    if not model_router:
        update_agent_run(supabase, session_id, "critic", "failed", error_detail="Router not configured")
        return {"critic_notes": []}

    claims_text = "\n".join([f"- {c['claim_text']} ({c['verification_status']})" for c in claims])

    prompt = f"""
    Act as a harsh, adversarial critic. Review the findings for the topic "{query}".
    
    Here are the claims extracted so far:
    {claims_text}
    
    Argue against these findings. Identify underlying assumptions, logical gaps, and risks.
    Return a JSON array of objects with keys:
    - "note_type": exactly one of "assumption", "gap", "risk"
    - "content": string explaining the weakness
    - "severity": exactly one of "low", "medium", "high"
    
    Output ONLY valid JSON. Provide up to 3 most important notes.
    """
    
    try:
        response = await model_router.call(prompt)
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].strip()
            
        notes_data = json.loads(text)
        
        processed_notes = []
        for n in notes_data:
            db_note = {
                "session_id": session_id,
                "note_type": n.get("note_type", "risk"),
                "content": n.get("content", ""),
                "severity": n.get("severity", "medium")
            }
            res = supabase.table("critic_notes").insert(db_note).execute()
            if res.data:
                processed_notes.append(res.data[0])
                
        update_agent_run(supabase, session_id, "critic", "done", raw_output={"critic_notes": processed_notes})
        return {"critic_notes": processed_notes}

    except AllProvidersExhaustedError as e:
        update_agent_run(supabase, session_id, "critic", "degraded", error_detail=str(e))
        return {"status": "degraded", "errors": [f"Critic degraded: {e}"]}
    except Exception as e:
        update_agent_run(supabase, session_id, "critic", "failed", error_detail=str(e))
        return {"status": "failed", "errors": [f"Critic failed: {e}"]}
