"""
embedder.py — Sentence embedding using multilingual transformer.

Model: paraphrase-multilingual-mpnet-base-v2 (Apache 2.0, 278M params)
Embeddings are L2-normalized so dot product = cosine similarity.
"""
import logging
from typing import List, Optional

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

_model: Optional[SentenceTransformer] = None
_model_name: str = ""


def _get_model(model_name: str, device: str = "auto") -> SentenceTransformer:
    """Load and cache the sentence transformer model."""
    global _model, _model_name
    
    if _model is None or _model_name != model_name:
        logger.info(f"Loading embedding model: {model_name}")
        _model = SentenceTransformer(model_name, device=device if device != "auto" else None)
        _model_name = model_name
        logger.info(f"Model loaded. Embedding dim: {_model.get_sentence_embedding_dimension()}")
    
    return _model


def encode_texts(
    texts: List[str],
    model_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    batch_size: int = 256,
    device: str = "auto",
    normalize: bool = True,
) -> np.ndarray:
    """
    Encode list of texts to L2-normalized embeddings.
    
    Args:
        texts: list of strings to encode
        model_name: HuggingFace model identifier
        batch_size: encoding batch size
        device: "cuda" / "cpu" / "auto"
        normalize: if True, L2-normalize so dot = cosine
    
    Returns:
        np.ndarray of shape (len(texts), embedding_dim), dtype=float32
    """
    model = _get_model(model_name, device)
    
    # Replace empty strings with a special placeholder
    processed_texts = [t if t else "[EMPTY]" for t in texts]
    
    logger.info(f"Encoding {len(texts):,} texts (batch_size={batch_size})...")
    
    embeddings = model.encode(
        processed_texts,
        batch_size=batch_size,
        normalize_embeddings=normalize,
        show_progress_bar=True,
        convert_to_numpy=True,
    )
    
    # Ensure float32
    embeddings = embeddings.astype(np.float32)
    
    # Safety: re-normalize in case of float precision issues
    if normalize:
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1.0, norms)
        embeddings = embeddings / norms
    
    logger.info(f"Embeddings shape: {embeddings.shape}")
    return embeddings


def encode_dataframe(
    df: pd.DataFrame,
    config,
    text_col: str = "norm_text",
) -> np.ndarray:
    """
    Encode a DataFrame's text column.
    Returns embeddings in same order as DataFrame rows.
    """
    texts = df[text_col].fillna("").tolist()
    return encode_texts(
        texts,
        model_name=config.model_name,
        batch_size=config.batch_size,
        device=config.device,
    )


def compute_cosine_similarity(
    emb_a: np.ndarray,
    emb_b: np.ndarray,
) -> float:
    """Cosine similarity between two L2-normalized vectors."""
    return float(np.dot(emb_a, emb_b))
