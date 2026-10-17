import uuid
import datetime
import json
from supabase import Client
from .state import AgentState

def update_agent_run(supabase: Client, session_id: str, agent_role: str, status: str, raw_output: dict = None, error_detail: str = None):
    data = {
        "status": status
    }
    if status == 'running':
        data["started_at"] = datetime.datetime.utcnow().isoformat()
    elif status in ['done', 'degraded', 'failed']:
        data["completed_at"] = datetime.datetime.utcnow().isoformat()
    
    if raw_output is not None:
        data["raw_output"] = raw_output
    if error_detail is not None:
        data["error_detail"] = error_detail

    res = supabase.table("agent_runs").select("id").eq("session_id", session_id).eq("agent_role", agent_role).execute()
    if len(res.data) > 0:
        supabase.table("agent_runs").update(data).eq("id", res.data[0]["id"]).execute()
    else:
        data["session_id"] = session_id
        data["agent_role"] = agent_role
        supabase.table("agent_runs").insert(data).execute()

async def planner_node(state: AgentState, config: dict):
    supabase: Client = config["configurable"]["supabase"]
    planner_router = config["configurable"].get("planner_router")
    session_id = state["session_id"]
    query = state["query"]
    toggles = state.get("toggles", {})
    
    update_agent_run(supabase, session_id, "planner", "running")
    
    # We define the core pipeline that always runs
    plan = ["researcher", "fact_checker", "critic"]
    
    if toggles.get("market_analysis"):
        plan.append("business_analyst")
    if toggles.get("startup_gen"):
        plan.append("startup_generator")
    if toggles.get("tech_arch"):
        plan.append("technical_architect")
        
    # We will use the planner_router just to structure the query maybe, 
    # or parse implicit intents if toggles are not provided.
    # For now, since the PRD says it uses toggles from Query Composer, we'll respect those.
    # Let's make a lightweight LLM call to extract any implicit toggles if they are empty
    if not toggles and planner_router:
        prompt = f"""
        Given the research query: "{query}"
        Does this query imply a need for:
        1. Market Analysis (competitors, TAM)
        2. Startup Concepts
        3. Technical Architecture
        
        Respond with ONLY a JSON object: {{"market_analysis": true/false, "startup_gen": true/false, "tech_arch": true/false}}
        """
        try:
            response = await planner_router.call(prompt)
            # Extremely basic JSON parsing for MVP
            text = response.text.strip()
            if "{" in text and "}" in text:
                text = text[text.find("{"):text.rfind("}")+1]
                inferred_toggles = json.loads(text)
                if inferred_toggles.get("market_analysis"): plan.append("business_analyst")
                if inferred_toggles.get("startup_gen"): plan.append("startup_generator")
                if inferred_toggles.get("tech_arch"): plan.append("technical_architect")
        except Exception as e:
            # Fallback to default linear pipeline if planning fails (TRD 4.1)
            update_agent_run(supabase, session_id, "planner", "degraded", error_detail=str(e))
            plan = ["researcher", "fact_checker", "report_writer"]
            return {"plan": plan}

    # All paths eventually lead to evaluator and report writer
    # The actual execution flow in LangGraph will be controlled by conditional edges or sequence
    plan.extend(["data_analyst", "knowledge_graph", "evaluator", "report_writer"])
    
    # Deduplicate while preserving order
    seen = set()
    final_plan = [x for x in plan if not (x in seen or seen.add(x))]
    
    update_agent_run(supabase, session_id, "planner", "done", raw_output={"plan": final_plan})
    
    return {"plan": final_plan}
