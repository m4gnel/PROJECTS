import os
from supabase import Client
from neo4j import AsyncGraphDatabase
from .state import AgentState
from .planner import update_agent_run
from config import settings

async def knowledge_graph_node(state: AgentState, config: dict):
    supabase: Client = config["configurable"]["supabase"]
    session_id = state["session_id"]
    query = state["query"]
    claims = state.get("claims", [])
    
    update_agent_run(supabase, session_id, "knowledge_graph", "running")
    
    if not settings.neo4j_uri or not settings.neo4j_password:
        update_agent_run(supabase, session_id, "knowledge_graph", "degraded", error_detail="Neo4j not configured")
        return {"knowledge_graph": "Neo4j not configured"}

    try:
        driver = AsyncGraphDatabase.driver(
            settings.neo4j_uri, 
            auth=(settings.neo4j_username or "neo4j", settings.neo4j_password)
        )
        
        async with driver.session() as session:
            # We insert the query as a Topic node
            await session.run(
                "MERGE (t:Topic {name: $query}) "
                "ON CREATE SET t.created_at = timestamp()",
                query=query
            )
            
            # Link claims to the topic
            for claim in claims:
                text = claim.get("claim_text", "")
                status = claim.get("verification_status", "")
                if text:
                    await session.run(
                        """
                        MATCH (t:Topic {name: $query})
                        MERGE (c:Claim {text: $claim_text})
                        ON CREATE SET c.status = $status
                        MERGE (t)-[:HAS_CLAIM]->(c)
                        """,
                        query=query,
                        claim_text=text[:200], # truncate for safety
                        status=status
                    )
                    
        await driver.close()
        
        update_agent_run(supabase, session_id, "knowledge_graph", "done", raw_output={"nodes_added": len(claims) + 1})
        return {"knowledge_graph": "Updated Neo4j successfully."}

    except Exception as e:
        update_agent_run(supabase, session_id, "knowledge_graph", "failed", error_detail=str(e))
        return {"status": "failed", "errors": [f"Knowledge Graph failed: {e}"]}
