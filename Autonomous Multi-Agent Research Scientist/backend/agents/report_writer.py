import datetime
from supabase import Client
from .state import AgentState
from .planner import update_agent_run
from model_router import ModelRouter, AllProvidersExhaustedError

async def report_writer_node(state: AgentState, config: dict):
    supabase: Client = config["configurable"]["supabase"]
    model_router: ModelRouter = config["configurable"]["report_router"]
    session_id = state["session_id"]
    
    update_agent_run(supabase, session_id, "report_writer", "running")
    
    query = state.get("query", "Unknown Topic")
    claims = state.get("claims", [])
    critic_notes = state.get("critic_notes", [])
    market_analysis = state.get("market_analysis", {})
    startup_concepts = state.get("startup_concepts", [])
    tech_arch = state.get("technical_architecture")
    data_analysis = state.get("data_analysis")
    score = state.get("confidence_score", "N/A")
    
    prompt = f"""
    Write a comprehensive, professional Markdown report for the topic: "{query}".
    
    Incorporate the following information:
    
    ## Fact Checked Claims
    {claims}
    
    ## Critic Review
    {critic_notes}
    
    ## Market Analysis
    {market_analysis}
    
    ## Startup Concepts
    {startup_concepts}
    
    ## Technical Architecture
    {tech_arch}
    
    ## Data Analysis
    {data_analysis}
    
    ## Confidence Score
    {score}/100
    
    Format the output cleanly with proper headers, bullet points, and paragraphs.
    Do not output JSON, output pure Markdown.
    """
    
    try:
        response = await model_router.call(prompt)
        report_content = response.text.strip()
        
        # Try to update first, else insert (UNIQUE constraint on session_id)
        res = supabase.table("reports").select("id").eq("session_id", session_id).execute()
        if len(res.data) > 0:
            supabase.table("reports").update({"content_markdown": report_content}).eq("id", res.data[0]["id"]).execute()
        else:
            supabase.table("reports").insert({
                "session_id": session_id,
                "content_markdown": report_content
            }).execute()
            
        update_agent_run(supabase, session_id, "report_writer", "done", raw_output={"length": len(report_content)})
        
        return {"report": report_content}
        
    except AllProvidersExhaustedError as e:
        update_agent_run(supabase, session_id, "report_writer", "degraded", error_detail=str(e))
        return {"status": "degraded", "errors": [f"Report writer degraded: {e}"]}
    except Exception as e:
        update_agent_run(supabase, session_id, "report_writer", "failed", error_detail=str(e))
        return {"status": "failed", "errors": [f"Report writer failed: {e}"]}
