import pytest
from unittest.mock import MagicMock, patch
from scripts.ingest_kau_docs import detect_crop_from_filename, chunk_text
from backend.services.rag_service import retrieve_kau_advice, RAGResult, get_model


def test_chunk_text_produces_correct_chunks():
    sample_text = ("Kerala Agricultural University Package of Practices advisory. " * 30)
    chunks = chunk_text(sample_text)
    assert len(chunks) >= 1
    assert isinstance(chunks[0], str)


def test_crop_detection_from_filename():
    assert detect_crop_from_filename("kau_coconut_pop.pdf") == "coconut"
    assert detect_crop_from_filename("kau_rice_package.pdf") == "rice"
    assert detect_crop_from_filename("kau_banana_guide.pdf") == "banana"
    assert detect_crop_from_filename("unknown_document.pdf") == "general"


def test_passage_prefix_applied():
    from backend.services.embedding_service import embed_service
    mock_model = MagicMock()
    mock_model.encode.return_value = MagicMock(tolist=lambda: [0.1] * 1024)

    with patch.object(embed_service, "get_model", return_value=mock_model):
        vec = embed_service.embed_passage("coconut fertilizer dose")
        assert len(vec) == 1024
        mock_model.encode.assert_called_once_with(
            "passage: coconut fertilizer dose",
            normalize_embeddings=True,
            convert_to_numpy=True
        )


@pytest.mark.asyncio
async def test_query_prefix_applied():
    results = await retrieve_kau_advice("coconut fertilizer dose", crop="coconut")
    assert len(results) >= 1
    assert isinstance(results[0], RAGResult)
    assert results[0].similarity >= 0.70


@pytest.mark.asyncio
async def test_retrieve_returns_rag_results():
    results = await retrieve_kau_advice("rice pest control", crop="rice", top_k=2)
    assert len(results) == 2
    assert results[0].crop_name == "rice"
