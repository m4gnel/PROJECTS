from typing import List

try:
    import structlog
    logger = structlog.get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

from backend.config import settings


class EmbeddingService:
    _model = None

    @classmethod
    def get_model(cls):
        """Lazy singleton loader for intfloat/multilingual-e5-large."""
        if not settings.ENABLE_EMBEDDINGS:
            return None

        if cls._model is None:
            try:
                from sentence_transformers import SentenceTransformer

                model_name = settings.EMBEDDING_MODEL_PATH or 'intfloat/multilingual-e5-large'
                cls._model = SentenceTransformer(model_name, device='cpu', local_files_only=True)
            except Exception as e:
                logger.warning("failed_loading_embedding_model", error=str(e))
        return cls._model

    def embed_query(self, text: str) -> List[float]:
        """Embed search query using sentence-transformers 3.3.0 with 'query: ' prefix."""
        model = self.get_model()
        if not model:
            # Fallback zero vector if model not loaded
            return [0.0] * 1024
        vec = model.encode(f"query: {text}", normalize_embeddings=True, convert_to_numpy=True)
        return vec.tolist()

    def embed_passage(self, text: str) -> List[float]:
        """Embed document passage using sentence-transformers 3.3.0 with 'passage: ' prefix."""
        model = self.get_model()
        if not model:
            return [0.0] * 1024
        vec = model.encode(f"passage: {text}", normalize_embeddings=True, convert_to_numpy=True)
        return vec.tolist()


embed_service = EmbeddingService()
