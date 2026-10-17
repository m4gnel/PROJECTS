import io
import re
import uuid
import hashlib
from datetime import date, timedelta
from typing import List, Dict, Any, Optional
import httpx
try:
    import structlog
    logger = structlog.get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

try:
    import fitz  # PyMuPDF 1.24.0
except ImportError:
    fitz = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

from sqlalchemy import text
from backend.database import AsyncSessionLocal
from backend.services.embedding_service import embed_service


class DocumentIngestionPipeline:
    async def fetch_document(self, url: str) -> bytes:
        """Fetch remote PDF/HTML document using HTTPX AsyncClient with 30s timeout."""
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.content

    def parse_pdf(self, content: bytes) -> str:
        """Extract plain text from PDF bytes using PyMuPDF (fitz), preserving paragraph structure."""
        if not fitz:
            logger.warning("PyMuPDF (fitz) not installed. PDF parsing unavailable.")
            return ""

        doc = fitz.open(stream=content, filetype="pdf")
        text_pages = []
        for page in doc:
            # Extract text
            page_text = page.get_text("text")
            text_pages.append(page_text)
        return "\n\n".join(text_pages)

    def parse_html(self, content: bytes) -> str:
        """Extract plain text from HTML bytes using BeautifulSoup."""
        if not BeautifulSoup:
            logger.warning("BeautifulSoup4 not installed. HTML parsing unavailable.")
            return content.decode("utf-8", errors="ignore")

        soup = BeautifulSoup(content, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        text_content = soup.get_text(separator="\n\n")
        lines = [line.strip() for line in text_content.splitlines()]
        return "\n\n".join([line for line in lines if line])

    def extract_metadata(self, text_content: str, url: str, manual_meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Detect crop, state, authority, dates from text and URL."""
        meta = manual_meta.copy() if manual_meta else {}

        lower_text = text_content.lower()

        # Crop detection
        if not meta.get("crop"):
            for crop in ["rice", "banana", "coconut", "tomato", "maize"]:
                if crop in lower_text or crop in url.lower():
                    meta["crop"] = crop
                    break

        # State detection
        if not meta.get("state"):
            for st in ["Kerala", "Tamil Nadu", "Karnataka", "Andhra Pradesh", "Maharashtra"]:
                if st.lower() in lower_text:
                    meta["state"] = st
                    break

        meta.setdefault("source_tier", 1)
        meta.setdefault("source_authority", "Agricultural Extension")
        meta.setdefault("language", "en")

        today = date.today()
        meta.setdefault("published_at", today.isoformat())
        meta.setdefault("valid_until", date(today.year + 2, today.month, today.day).isoformat())

        return meta

    def extract_chunks(self, text_content: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Split text at headings and paragraph boundaries.
        Chunks between 100 and 2000 chars (512 tokens), splitting strictly at sentence boundaries.
        """
        if not text_content:
            return []

        # Split into initial blocks by double newline or heading boundaries
        blocks = re.split(r'\n\n+|(?=\n[A-Z0-9\.\s]{3,40}\n)', text_content)
        chunks = []
        current_chunk = ""
        chunk_idx = 0

        for block in blocks:
            cleaned_block = block.strip()
            if not cleaned_block:
                continue

            if len(current_chunk) + len(cleaned_block) + 2 <= 2000:
                current_chunk = f"{current_chunk}\n\n{cleaned_block}".strip()
            else:
                if len(current_chunk) >= 100:
                    chunks.append({
                        "content": current_chunk,
                        "metadata": metadata,
                        "chunk_index": chunk_idx
                    })
                    chunk_idx += 1
                
                # Handle oversized single blocks
                if len(cleaned_block) > 2000:
                    sentences = re.split(r'(?<=[.!?])\s+', cleaned_block)
                    sub_chunk = ""
                    for sent in sentences:
                        if len(sub_chunk) + len(sent) + 1 <= 2000:
                            sub_chunk = f"{sub_chunk} {sent}".strip()
                        else:
                            if len(sub_chunk) >= 100:
                                chunks.append({
                                    "content": sub_chunk,
                                    "metadata": metadata,
                                    "chunk_index": chunk_idx
                                })
                                chunk_idx += 1
                            sub_chunk = sent
                    current_chunk = sub_chunk
                else:
                    current_chunk = cleaned_block

        if len(current_chunk) >= 100:
            chunks.append({
                "content": current_chunk,
                "metadata": metadata,
                "chunk_index": chunk_idx
            })

        return chunks

    async def embed_and_store(self, document_id: str, chunks: List[Dict[str, Any]], batch_size: int = 32):
        """Batch embed chunks with passage: prefix and bulk insert into PostgreSQL."""
        if not chunks:
            return

        async with AsyncSessionLocal() as session:
            chunk_sql = text("""
            INSERT INTO knowledge_chunks (
                id, document_id, chunk_index, content, embedding, metadata
            ) VALUES (
                :id, :document_id, :chunk_index, :content, :embedding, :metadata
            ) ON CONFLICT (id) DO NOTHING
            """)

            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i + batch_size]
                params = []
                for item in batch:
                    chunk_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{document_id}_{item['chunk_index']}"))
                    passage_emb = embed_service.embed_passage(item["content"])
                    params.append({
                        "id": chunk_id,
                        "document_id": document_id,
                        "chunk_index": item["chunk_index"],
                        "content": item["content"],
                        "embedding": passage_emb,
                        "metadata": item["metadata"]
                    })
                
                await session.execute(chunk_sql, params)
            await session.commit()

    async def ingest(self, url: str, title: str, manual_meta: Optional[Dict[str, Any]] = None) -> str:
        """Full pipeline execution: fetch, parse, metadata, chunk, embed, store."""
        raw_bytes = await self.fetch_document(url)
        if url.lower().endswith(".pdf") or raw_bytes.startswith(b"%PDF"):
            content_text = self.parse_pdf(raw_bytes)
        else:
            content_text = self.parse_html(raw_bytes)

        metadata = self.extract_metadata(content_text, url, manual_meta)
        content_hash = hashlib.sha256(raw_bytes).hexdigest()
        doc_id = str(uuid.uuid5(uuid.NAMESPACE_URL, url))

        async with AsyncSessionLocal() as session:
            doc_sql = text("""
            INSERT INTO knowledge_documents (
                id, title, crop, state, source_tier, source_authority,
                source_url, valid_until, status, content_hash
            ) VALUES (
                :id, :title, :crop, :state, :source_tier, :source_authority,
                :source_url, :valid_until, 'PUBLISHED', :content_hash
            ) ON CONFLICT (id) DO UPDATE SET
                title = EXCLUDED.title,
                content_hash = EXCLUDED.content_hash
            """)
            await session.execute(doc_sql, {
                "id": doc_id,
                "title": title,
                "crop": metadata.get("crop"),
                "state": metadata.get("state"),
                "source_tier": metadata.get("source_tier", 1),
                "source_authority": metadata.get("source_authority", "ICAR/KAU"),
                "source_url": url,
                "valid_until": metadata.get("valid_until"),
                "content_hash": content_hash
            })
            await session.commit()

        chunks = self.extract_chunks(content_text, metadata)
        await self.embed_and_store(doc_id, chunks)
        return doc_id

