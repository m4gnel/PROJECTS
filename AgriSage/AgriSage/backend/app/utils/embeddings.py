from sentence_transformers import SentenceTransformer

_model = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("intfloat/multilingual-e5-large")
    return _model


def embed_query(text: str) -> list[float]:
    """For queries: prefix with 'query: '"""
    model = get_model()
    embedding = model.encode(f"query: {text}", normalize_embeddings=True)
    return embedding.tolist()


def embed_passage(text: str) -> list[float]:
    """For documents/passages: prefix with 'passage: '"""
    model = get_model()
    embedding = model.encode(f"passage: {text}", normalize_embeddings=True)
    return embedding.tolist()
