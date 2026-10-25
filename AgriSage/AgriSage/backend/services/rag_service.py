import logging
from dataclasses import dataclass
from typing import Any, List, Optional
from backend.config import settings

logger = logging.getLogger(__name__)

MODEL_NAME = "intfloat/multilingual-e5-large"


@dataclass
class RAGResult:
    content: str
    source_file: str
    crop_name: str
    similarity: float


# Module-level model cache
_MODEL = None

def get_model():
    global _MODEL
    if not settings.ENABLE_EMBEDDINGS:
        return None

    if _MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer

            model_name = settings.EMBEDDING_MODEL_PATH or MODEL_NAME
            _MODEL = SentenceTransformer(model_name, device="cpu", local_files_only=True)
        except Exception as e:
            logger.warning(f"failed_loading_rag_embedding_model: {e}")
    return _MODEL


async def retrieve_kau_advice(
    query: str,
    crop: Optional[str] = None,
    top_k: int = 5,
    similarity_threshold: float = 0.70,
    db_conn: Any = None
) -> List[RAGResult]:
    """
    Retrieve top-k KAU document chunks relevant to the query.
    Mandatory: 'query: ' prefix for multilingual-e5-large retrieval.
    """
    model = get_model()
    prefixed_query = f"query: {query}"
    vec = None

    if model is not None:
        try:
            vec = model.encode([prefixed_query], normalize_embeddings=True)[0].tolist()
        except Exception as e:
            logger.warning(f"rag_embedding_encoding_error: {e}")

    # If db_conn provided, execute pgvector query
    if db_conn is not None and vec is not None:
        try:
            if crop and crop != "unknown":
                sql = """
                    SELECT content, source_file, crop_name,
                           1 - (embedding <=> $1::vector) AS similarity
                    FROM kau_documents
                    WHERE crop_name = $2
                      AND 1 - (embedding <=> $1::vector) >= $3
                    ORDER BY embedding <=> $1::vector
                    LIMIT $4
                """
                rows = await db_conn.fetch(sql, vec, crop, similarity_threshold, top_k)
            else:
                sql = """
                    SELECT content, source_file, crop_name,
                           1 - (embedding <=> $1::vector) AS similarity
                    FROM kau_documents
                    WHERE 1 - (embedding <=> $1::vector) >= $2
                    ORDER BY embedding <=> $1::vector
                    LIMIT $3
                """
                rows = await db_conn.fetch(sql, vec, similarity_threshold, top_k)

            if not rows:
                # Fallback: lower threshold and remove crop filter
                sql = """
                    SELECT content, source_file, crop_name,
                           1 - (embedding <=> $1::vector) AS similarity
                    FROM kau_documents
                    ORDER BY embedding <=> $1::vector
                    LIMIT $2
                """
                rows = await db_conn.fetch(sql, vec, top_k)

            return [
                RAGResult(
                    content=row["content"],
                    source_file=row["source_file"],
                    crop_name=row["crop_name"],
                    similarity=float(row["similarity"])
                )
                for row in rows
            ]
        except Exception as e:
            logger.warning(f"rag_db_query_error: {e}")

    # Never invent source documents or agronomic doses when the embedding model
    # or the authoritative database is unavailable.  Callers can present the
    # empty evidence set and retain the farmer-safety disclaimer instead.
    return []
