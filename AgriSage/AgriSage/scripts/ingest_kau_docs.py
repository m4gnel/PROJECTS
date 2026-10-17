#!/usr/bin/env python3
"""
Ingest KAU Package of Practices PDFs into pgvector.
Usage: python scripts/ingest_kau_docs.py --docs-dir ./kau_docs/
KAU PDF naming convention: kau_<crop>_pop.pdf
"""

import argparse
import asyncio
import os
import re
import uuid
from typing import List

try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import tiktoken
except ImportError:
    tiktoken = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

CHUNK_TOKENS = 512
OVERLAP_TOKENS = 50
BATCH_SIZE = 32
MODEL_NAME = "intfloat/multilingual-e5-large"
EMBEDDING_DIM = 1024

KERALA_CROP_MAP = {
    "coconut": ["coconut", "cocos nucifera", "thenga"],
    "rice": ["rice", "paddy", "nellu"],
    "banana": ["banana", "plantain", "ethapazham", "nendran"],
    "rubber": ["rubber", "hevea"],
    "tapioca": ["tapioca", "cassava", "kappa"],
    "pepper": ["pepper", "black pepper", "kurumulaku"],
    "cardamom": ["cardamom", "elakka"],
    "ginger": ["ginger", "inji"],
    "turmeric": ["turmeric", "manjal"],
    "arecanut": ["arecanut", "betel nut", "adakka"],
}


def detect_crop_from_filename(filename: str) -> str:
    """Extract crop name from KAU PDF filename: kau_coconut_pop.pdf -> coconut"""
    name = os.path.basename(filename).lower()
    for crop in KERALA_CROP_MAP:
        if crop in name:
            return crop
    return "general"


def extract_text_from_pdf(pdf_path: str) -> str:
    if pypdf is None:
        return ""
    reader = pypdf.PdfReader(pdf_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def chunk_text(text: str) -> List[str]:
    if not text.strip():
        return []
    if tiktoken is not None:
        enc = tiktoken.get_encoding("cl100k_base")
        tokens = enc.encode(text)
        chunks, i = [], 0
        while i < len(tokens):
            chunk_tokens = tokens[i : i + CHUNK_TOKENS]
            chunks.append(enc.decode(chunk_tokens))
            i += CHUNK_TOKENS - OVERLAP_TOKENS
        return [c for c in chunks if len(enc.encode(c)) >= 50]
    else:
        # Simple word chunking fallback
        words = text.split()
        chunks, i = [], 0
        while i < len(words):
            chunk = " ".join(words[i : i + 400])
            chunks.append(chunk)
            i += 350
        return chunks


async def ingest_all(docs_dir: str, database_url: str):
    if not os.path.exists(docs_dir):
        print(f"Directory {docs_dir} does not exist. Creating it.")
        os.makedirs(docs_dir, exist_ok=True)
        return

    pdf_files = [f for f in os.listdir(docs_dir) if f.endswith(".pdf")]
    print(f"Found {len(pdf_files)} PDF files in {docs_dir}")

    if not pdf_files:
        print("No PDF files to ingest.")
        return

    model = SentenceTransformer(MODEL_NAME) if SentenceTransformer is not None else None
    print(f"Loaded embedding model: {MODEL_NAME}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-dir", default="./kau_docs/")
    parser.add_argument("--database-url", default=os.getenv("DATABASE_URL", ""))
    args = parser.parse_args()
    asyncio.run(ingest_all(args.docs_dir, args.database_url))
