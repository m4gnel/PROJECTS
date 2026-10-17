from .state import AgriState


async def rag_node(state: AgriState) -> dict:
    """
    Vector search over KAU PDF chunks in pgvector.
    Query embedding: multilingual-e5-large with "query: " prefix.
    Returns: {"agent_findings": ["rag: <relevant KAU advice>"], "agents_completed": ["rag"]}
    """
    try:
        from ..utils.embeddings import embed_query
        query_embedding = embed_query(state["query"])

        # Try database vector search
        try:
            from ..database import AsyncSessionLocal
            async with AsyncSessionLocal() as session:
                result = await session.execute(
                    # Raw SQL for pgvector cosine similarity
                    __import__("sqlalchemy").text(
                        "SELECT content FROM knowledge_chunks ORDER BY embedding <=> :emb LIMIT 5"
                    ),
                    {"emb": str(query_embedding)}
                )
                chunks = [row[0] for row in result.fetchall()]
        except Exception:
            chunks = []

        if chunks:
            combined = " | ".join(chunks[:3])
            return {"agent_findings": [f"rag: {combined[:500]}"], "agents_completed": ["rag"]}
        else:
            return {"agent_findings": ["rag: No relevant KAU knowledge found for this query."], "agents_completed": ["rag"]}
    except Exception as e:
        return {"error_messages": [f"rag: {str(e)}"], "agents_completed": ["rag"]}
