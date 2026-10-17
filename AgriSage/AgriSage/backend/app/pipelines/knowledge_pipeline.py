import os
import uuid
import logging
from pypdf import PdfReader
from sqlalchemy import text
from ..database import AsyncSessionLocal
from ..config import settings
from ..utils.embeddings import embed_passage

logger = logging.getLogger(__name__)


async def run_knowledge_pipeline():
    """Index KAU PDF documents into knowledge_chunks with pgvector embeddings."""
    pdf_dir = settings.KAU_PDF_DIR
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir, exist_ok=True)
        logger.info("Created KAU PDF dir at %s", pdf_dir)
        return

    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
    if not pdf_files:
        logger.info("No PDF files found in %s to index.", pdf_dir)
        return

    try:
        async with AsyncSessionLocal() as session:
            for pdf_file in pdf_files:
                pdf_path = os.path.join(pdf_dir, pdf_file)
                # Check if already indexed
                res = await session.execute(
                    text("SELECT count(*) FROM knowledge_chunks WHERE source_file = :src"),
                    {"src": pdf_file}
                )
                if res.scalar() > 0:
                    continue

                reader = PdfReader(pdf_path)
                full_text = ""
                for page in reader.pages:
                    full_text += (page.extract_text() or "") + "\n"

                # Simple chunking (e.g. 500 characters with 100 overlap)
                chunk_size = 500
                chunks = [full_text[i:i + chunk_size] for i in range(0, len(full_text), 400)]

                for idx, chunk_content in enumerate(chunks):
                    if not chunk_content.strip():
                        continue
                    embedding = embed_passage(chunk_content)
                    await session.execute(text("""
                        INSERT INTO knowledge_chunks (id, source_file, chunk_index, content, embedding, created_at)
                        VALUES (:id, :src, :idx, :content, :emb, NOW())
                    """), {
                        "id": str(uuid.uuid4()),
                        "src": pdf_file,
                        "idx": idx,
                        "content": chunk_content,
                        "emb": str(embedding),
                    })
            await session.commit()
            logger.info("knowledge_pipeline completed indexing.")
    except Exception as e:
        logger.error("knowledge_pipeline error: %s", str(e))
