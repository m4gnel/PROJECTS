"""
AMRS API Gateway — FastAPI application.
"""

from __future__ import annotations
import asyncio
from typing import Optional, Dict
from pydantic import BaseModel
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from sse_starlette.sse import EventSourceResponse

from config import settings
from agents.graph import create_research_graph
from agents.state import AgentState
from providers import get_router

app = FastAPI(
    title="AMRS API",
    description="Autonomous Multi-Agent Research Scientist — API Gateway",
    version="0.1.0",
)

# CORS — allow the Next.js frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase client safely (supports offline testing and dev)
supabase: Optional[Client] = None
if settings.supabase_url and (settings.supabase_service_role_key or settings.supabase_anon_key):
    try:
        supabase = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key or settings.supabase_anon_key
        )
    except Exception as exc:
        import logging
        logging.getLogger(__name__).warning("Supabase initialization skipped: %s", exc)

# Initialize ModelRouters for each agent
routers = {
    "planner_router": get_router("planner"),
    "research_router": get_router("researcher"),
    "fact_checker_router": get_router("fact_checker"),
    "critic_router": get_router("critic"),
    "business_router": get_router("business_analyst"),
    "startup_router": get_router("startup_generator"),
    "architect_router": get_router("technical_architect"),
    "data_analyst_router": get_router("data_analyst"),
    "evaluator_router": get_router("evaluator"),
    "report_router": get_router("report_writer"),
    "daily_chat_router": get_router("daily_assistant", primary="groq", fallback1="gemini") # Example of different primary
}

graph = create_research_graph()


@app.on_event("startup")
async def startup_warnings() -> None:
    settings.warn_if_missing()


@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}


class ResearchRequest(BaseModel):
    query: str
    user_id: str
    toggles: Optional[Dict[str, bool]] = {}

async def run_research_graph(session_id: str, query: str, toggles: dict):
    config = {
        "configurable": {
            "supabase": supabase,
            **routers
        }
    }
    state = AgentState(
        session_id=session_id,
        query=query,
        plan=[],
        sources=[],
        claims=[],
        critic_notes=[],
        market_analysis=None,
        startup_concepts=[],
        technical_architecture=None,
        data_analysis=None,
        confidence_score=None,
        toggles=toggles,
        report="",
        status="queued",
        errors=[]
    )
    
    # Mark session as running
    supabase.table("research_sessions").update({"status": "running"}).eq("id", session_id).execute()
    
    try:
        final_state = await graph.ainvoke(state, config=config)
        status = final_state.get("status", "completed")
        if status not in ["degraded", "failed"]:
            status = "completed"
        # Update session to terminal state
        supabase.table("research_sessions").update({"status": status}).eq("id", session_id).execute()
    except Exception as e:
        print(f"Graph execution failed: {e}")
        supabase.table("research_sessions").update({"status": "failed"}).eq("id", session_id).execute()


@app.post("/api/v1/research/sessions")
async def create_research_session(req: ResearchRequest, bg_tasks: BackgroundTasks):
    # Insert session into DB
    res = supabase.table("research_sessions").insert({
        "user_id": req.user_id,
        "query_text": req.query,
        "toggles": req.toggles,
        "status": "queued"
    }).execute()
    
    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to create session")
        
    session_id = res.data[0]["id"]
    bg_tasks.add_task(run_research_graph, session_id, req.query, req.toggles)
    
    return {"session_id": session_id, "status": "queued"}


@app.get("/api/v1/research/sessions/{session_id}/status")
async def get_session_status(session_id: str):
    res = supabase.table("research_sessions").select("status, confidence_score").eq("id", session_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Session not found")
        
    session_status = res.data[0]["status"]
    confidence_score = res.data[0].get("confidence_score")
    
    runs_res = supabase.table("agent_runs").select("*").eq("session_id", session_id).execute()
    
    return {
        "session_status": session_status,
        "confidence_score": confidence_score,
        "agent_runs": runs_res.data
    }


@app.get("/api/v1/research/sessions/{session_id}/report")
async def get_session_report(session_id: str):
    res = supabase.table("reports").select("content_markdown").eq("session_id", session_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"content_markdown": res.data[0]["content_markdown"]}


class ChatRequest(BaseModel):
    message: str

@app.post("/api/v1/chat/daily")
async def daily_chat(req: ChatRequest):
    router = routers["daily_chat_router"]
    try:
        response = await router.call(req.message)
        return {"response": response.text, "provider": response.provider_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/sessions/search")
async def search_sessions(q: str):
    # Dummy implementation for vector search over Qdrant
    # Should realistically query Qdrant and join with Supabase
    return {"results": []}
