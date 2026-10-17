from typing import List, Dict, Any, Optional
from sqlalchemy import text
from backend.database import AsyncSessionLocal
from backend.services.embedding_service import embed_service

try:
    import structlog
    logger = structlog.get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)


class HybridRetriever:
    """
    Hybrid retriever using pgvector dense vector search + PostgreSQL Full Text Search (FTS)
    merged with Reciprocal Rank Fusion (RRF, k=60) and authority tier boost (1.3x for tier 1).
    """

    async def retrieve(
        self,
        query: str,
        crop: Optional[str] = None,
        state: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        # Generate query vector with 'query: ' prefix
        query_embedding = embed_service.embed_query(query)

        async with AsyncSessionLocal() as session:
            # 1. Dense search
            dense_sql = text("""
            SELECT kc.id, kc.content, kc.metadata, kd.source_tier, kd.source_authority, kd.title,
                   (kc.embedding <=> :query_embedding) as distance
            FROM knowledge_chunks kc
            JOIN knowledge_documents kd ON kc.document_id = kd.id
            WHERE kd.valid_until > CURRENT_DATE AND kd.status = 'PUBLISHED'
              AND (:crop IS NULL OR kd.crop = :crop OR kd.crop IS NULL)
            ORDER BY kc.embedding <=> :query_embedding
            LIMIT 20
            """)
            dense_res = await session.execute(
                dense_sql,
                {"query_embedding": str(query_embedding), "crop": crop}
            )
            dense_rows = dense_res.fetchall()

            # 2. Sparse FTS search
            sparse_sql = text("""
            SELECT kc.id, kc.content, kc.metadata, kd.source_tier, kd.source_authority, kd.title,
                   ts_rank(to_tsvector('english', kc.content), plainto_tsquery('english', :keywords)) as rank
            FROM knowledge_chunks kc
            JOIN knowledge_documents kd ON kc.document_id = kd.id
            WHERE to_tsvector('english', kc.content) @@ plainto_tsquery('english', :keywords)
              AND kd.valid_until > CURRENT_DATE AND kd.status = 'PUBLISHED'
              AND (:crop IS NULL OR kd.crop = :crop OR kd.crop IS NULL)
            ORDER BY rank DESC
            LIMIT 20
            """)
            sparse_res = await session.execute(
                sparse_sql,
                {"keywords": query, "crop": crop}
            )
            sparse_rows = sparse_res.fetchall()

        # 3. Reciprocal Rank Fusion (RRF)
        scores = {}
        items = {}
        rrf_k = 60

        for rank_idx, row in enumerate(dense_rows):
            cid = str(row.id)
            rrf_score = 1.0 / (rrf_k + (rank_idx + 1))
            scores[cid] = scores.get(cid, 0.0) + rrf_score
            items[cid] = row

        for rank_idx, row in enumerate(sparse_rows):
            cid = str(row.id)
            rrf_score = 1.0 / (rrf_k + (rank_idx + 1))
            scores[cid] = scores.get(cid, 0.0) + rrf_score
            if cid not in items:
                items[cid] = row

        # 4. Authority Tier Boost (1.3x for source_tier == 1)
        final_results = []
        for cid, base_score in scores.items():
            row = items[cid]
            multiplier = 1.3 if getattr(row, 'source_tier', 2) == 1 else 1.0
            final_score = base_score * multiplier
            final_results.append({
                "chunk_id": cid,
                "content": row.content,
                "title": getattr(row, 'title', ''),
                "source_tier": getattr(row, 'source_tier', 1),
                "source_authority": getattr(row, 'source_authority', ''),
                "metadata": row.metadata,
                "score": final_score
            })

        # Sort by final score descending
        final_results.sort(key=lambda x: x["score"], reverse=True)
        return final_results[:top_k]


retriever = HybridRetriever()
