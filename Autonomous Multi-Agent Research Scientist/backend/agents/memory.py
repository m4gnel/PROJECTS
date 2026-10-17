import uuid
from supabase import Client
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from .state import AgentState
from .planner import update_agent_run
from config import settings
import httpx # for local lightweight embedding or we can use the LLM to get embeddings if supported
import json

# For MVP, we might mock embeddings or use a lightweight model
# We'll use Qdrant client to store and retrieve.
# We will create a collection "amrs_memory" if it doesn't exist.

async def ensure_qdrant_collection(client: AsyncQdrantClient, collection_name: str = "amrs_memory"):
    try:
        collections = await client.get_collections()
        if not any(c.name == collection_name for c in collections.collections):
            await client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE) # Assuming 768 dim for embeddings
            )
    except Exception as e:
        print(f"Error ensuring Qdrant collection: {e}")

async def memory_node(state: AgentState, config: dict):
    supabase: Client = config["configurable"]["supabase"]
    session_id = state["session_id"]
    query = state["query"]
    
    update_agent_run(supabase, session_id, "memory", "running")
    
    # Check if Qdrant is configured
    if not settings.qdrant_url or not settings.qdrant_api_key:
        update_agent_run(supabase, session_id, "memory", "degraded", error_detail="Qdrant not configured")
        return {"past_context": "No memory available (Qdrant not configured)."}
        
    try:
        q_client = AsyncQdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
        await ensure_qdrant_collection(q_client)
        
        # In a real scenario, we would use an embedding model (like text-embedding-004) to get the vector.
        # For this MVP code, we'll create a dummy vector of 768 dimensions for the search to demonstrate the flow.
        dummy_vector = [0.01] * 768 
        
        # Search for past memories
        search_result = await q_client.search(
            collection_name="amrs_memory",
            query_vector=dummy_vector,
            limit=3
        )
        
        context_strs = []
        for hit in search_result:
            context_strs.append(f"- {hit.payload.get('query', '')} (Confidence: {hit.payload.get('confidence_score', 0)})")
            
        past_context = "\n".join(context_strs) if context_strs else "No relevant past context found."
        
        # After report generation, we should IDEALLY store the new memory in a separate step or end of graph.
        # For now, we just retrieve.
        
        update_agent_run(supabase, session_id, "memory", "done", raw_output={"memories_retrieved": len(search_result)})
        return {"past_context": past_context}

    except Exception as e:
        update_agent_run(supabase, session_id, "memory", "failed", error_detail=str(e))
        return {"status": "failed", "errors": [f"Memory agent failed: {e}"]}
