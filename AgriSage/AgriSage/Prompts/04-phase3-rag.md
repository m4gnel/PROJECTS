# 📚 PHASE 3 — KAU RAG Knowledge Pipeline
## Branch: `dev/m3-rag` · Owner: M3 · GitHub Issue: #3

---

## Paste This Into Gemini 2.5 Pro

```
=== AGRI-SAGE PHASE 3 — KAU RAG KNOWLEDGE PIPELINE ===

Run AUDIT-FIRST PROTOCOL on scripts/ and app/services/rag_service.py before writing.
Print the audit table. Build only MISSING and NEEDS_WORK files.

TARGET FILE STRUCTURE:
scripts/
├── ingest_kau_docs.py        ← PDF → chunks → embed → pgvector
└── validate_embeddings.py    ← Sanity check: query → top-5 results
app/services/
└── rag_service.py            ← Async retrieval function
tests/
└── test_rag.py               ← Pytest: ingestion + retrieval tests

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CRITICAL: multilingual-e5-large PREFIX RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ALWAYS use these prefixes — without them similarity drops 15–25%:
  Document chunks: "passage: [Kerala crop advisory] " + chunk_text
  User queries:    "query: "                           + farmer_question

Embedding dimension: 1024 (NOT 768, NOT 1536)
Model string: "intfloat/multilingual-e5-large" (exact)
Batch size for ingestion: 32 (larger crashes on low-RAM machines)
normalize_embeddings=True (mandatory for cosine similarity)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INGESTION SCRIPT (scripts/ingest_kau_docs.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#!/usr/bin/env python3
"""
Ingest KAU Package of Practices PDFs into pgvector.
Usage: python scripts/ingest_kau_docs.py --docs-dir ./kau_docs/
KAU PDF naming convention: kau_<crop>_pop.pdf
  e.g. kau_coconut_pop.pdf, kau_rice_pop.pdf, kau_banana_pop.pdf
"""

import argparse, uuid, os, re
import pypdf
import tiktoken
from sentence_transformers import SentenceTransformer
import asyncpg
from pgvector.asyncpg import register_vector

CHUNK_TOKENS   = 512
OVERLAP_TOKENS = 50
BATCH_SIZE     = 32
MODEL_NAME     = "intfloat/multilingual-e5-large"
EMBEDDING_DIM  = 1024

KERALA_CROP_MAP = {
    "coconut": ["coconut", "cocos nucifera", "thenga"],
    "rice":    ["rice", "paddy", "nellu"],
    "banana":  ["banana", "plantain", "ethapazham", "nendran"],
    "rubber":  ["rubber", "hevea"],
    "tapioca": ["tapioca", "cassava", "kappa"],
    "pepper":  ["pepper", "black pepper", "kurumulaku"],
    "cardamom":["cardamom", "elakka"],
    "ginger":  ["ginger", "inji"],
    "turmeric":["turmeric", "manjal"],
    "arecanut":["arecanut", "betel nut", "adakka"],
}

def detect_crop_from_filename(filename: str) -> str:
    """Extract crop name from KAU PDF filename: kau_coconut_pop.pdf → coconut"""
    name = os.path.basename(filename).lower()
    for crop in KERALA_CROP_MAP:
        if crop in name:
            return crop
    return "general"

def extract_text_from_pdf(pdf_path: str) -> str:
    reader = pypdf.PdfReader(pdf_path)
    return "\n".join(
        page.extract_text() or "" for page in reader.pages
    )

def chunk_text(text: str) -> list[str]:
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    chunks, i = [], 0
    while i < len(tokens):
        chunk_tokens = tokens[i : i + CHUNK_TOKENS]
        chunks.append(enc.decode(chunk_tokens))
        i += CHUNK_TOKENS - OVERLAP_TOKENS
    # Remove chunks shorter than 50 tokens (header/footer noise)
    return [c for c in chunks if len(enc.encode(c)) >= 50]

async def ingest_all(docs_dir: str, database_url: str):
    conn = await asyncpg.connect(database_url)
    await register_vector(conn)

    # Create HNSW index if not exists
    await conn.execute("""
        CREATE EXTENSION IF NOT EXISTS vector;
        CREATE TABLE IF NOT EXISTS kau_documents (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            source_file TEXT NOT NULL,
            crop_name TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            content TEXT NOT NULL,
            embedding vector(1024) NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS kau_hnsw_idx
        ON kau_documents USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64);
    """)

    model = SentenceTransformer(MODEL_NAME)
    total_chunks = 0

    pdf_files = [f for f in os.listdir(docs_dir) if f.endswith(".pdf")]
    print(f"Found {len(pdf_files)} PDF files")

    for pdf_file in pdf_files:
        pdf_path = os.path.join(docs_dir, pdf_file)
        crop_name = detect_crop_from_filename(pdf_file)
        print(f"Processing {pdf_file} → crop: {crop_name}")

        text = extract_text_from_pdf(pdf_path)
        if not text.strip():
            print(f"  WARNING: No text extracted from {pdf_file} — skipping")
            continue

        chunks = chunk_text(text)
        print(f"  {len(chunks)} chunks created")

        # Batch embed with mandatory passage: prefix
        for batch_start in range(0, len(chunks), BATCH_SIZE):
            batch = chunks[batch_start : batch_start + BATCH_SIZE]
            prefixed = [f"passage: [Kerala crop advisory] {c}" for c in batch]
            embeddings = model.encode(
                prefixed,
                normalize_embeddings=True,
                show_progress_bar=False
            )
            for i, (chunk, embedding) in enumerate(zip(batch, embeddings)):
                chunk_index = batch_start + i
                # Skip if already ingested (idempotent)
                existing = await conn.fetchval(
                    "SELECT id FROM kau_documents WHERE source_file=$1 AND chunk_index=$2",
                    pdf_file, chunk_index
                )
                if existing:
                    continue
                await conn.execute(
                    """INSERT INTO kau_documents
                       (source_file, crop_name, chunk_index, content, embedding)
                       VALUES ($1, $2, $3, $4, $5)""",
                    pdf_file, crop_name, chunk_index, chunk, embedding.tolist()
                )
                total_chunks += 1

    await conn.close()
    print(f"\n✅ Ingestion complete: {total_chunks} chunks inserted")

if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-dir", required=True)
    args = parser.parse_args()
    asyncio.run(ingest_all(args.docs_dir, os.environ["DATABASE_URL"].replace("+asyncpg","")))

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RAG SERVICE (app/services/rag_service.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from sentence_transformers import SentenceTransformer
from dataclasses import dataclass
import asyncpg
from pgvector.asyncpg import register_vector

MODEL_NAME = "intfloat/multilingual-e5-large"

@dataclass
class RAGResult:
    content: str
    source_file: str
    crop_name: str
    similarity: float

# Load model once at module level (not per-request)
_model = None
def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model

async def retrieve_kau_advice(
    query: str,
    crop: str | None = None,
    top_k: int = 5,
    similarity_threshold: float = 0.70,
    db_conn: asyncpg.Connection = None
) -> list[RAGResult]:
    """
    Retrieve top-k KAU document chunks relevant to the farmer's query.
    Always uses "query: " prefix for multilingual-e5-large.
    """
    model = get_model()

    # MANDATORY: "query: " prefix for retrieval queries
    query_embedding = model.encode(
        [f"query: {query}"],
        normalize_embeddings=True
    )[0].tolist()

    # Build SQL: cosine similarity search with optional crop filter
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
        rows = await db_conn.fetch(sql, query_embedding, crop,
                                   similarity_threshold, top_k)
    else:
        sql = """
            SELECT content, source_file, crop_name,
                   1 - (embedding <=> $1::vector) AS similarity
            FROM kau_documents
            WHERE 1 - (embedding <=> $1::vector) >= $2
            ORDER BY embedding <=> $1::vector
            LIMIT $3
        """
        rows = await db_conn.fetch(sql, query_embedding,
                                   similarity_threshold, top_k)

    if not rows:
        # Fallback: lower threshold and remove crop filter
        sql = """
            SELECT content, source_file, crop_name,
                   1 - (embedding <=> $1::vector) AS similarity
            FROM kau_documents
            ORDER BY embedding <=> $1::vector
            LIMIT $2
        """
        rows = await db_conn.fetch(sql, query_embedding, top_k)

    return [
        RAGResult(
            content=row["content"],
            source_file=row["source_file"],
            crop_name=row["crop_name"],
            similarity=float(row["similarity"])
        )
        for row in rows
    ]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CROP ADVISOR AGENT SYSTEM PROMPT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

In brain/05_AGENT_PROMPTS.md, add this for CropAdvisorAgent:

  "You are the CropAdvisorAgent for Agri-SAGE Kerala.
   You have been given excerpts from the KAU (Kerala Agricultural University)
   Package of Practices — the official crop management guide for Kerala farmers.

   Your job: Answer the farmer's question about {crop} using ONLY the provided excerpts.

   Rules:
   - Quote the specific practice number if mentioned in the excerpt
   - If the answer is not in the excerpts, say exactly:
     'For this specific question, please consult your nearest KAU Krishi Vigyan Kendra
      or call the Kerala Farmer Call Centre: 1800-425-1661 (free, Malayalam support)'
   - Never guess or hallucinate crop management advice
   - Always mention the source document name

   KAU Excerpts:
   {kau_rag_results}

   Farmer question: {farmer_query}"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VALIDATION SCRIPT (scripts/validate_embeddings.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TEST_QUERIES = [
    ("What is the NPK fertilizer dose for coconut?",       "coconut", 0.70),
    ("When should I spray fungicide on rice leaves?",      "rice",    0.70),
    ("Best time to harvest nendran banana in Kerala?",     "banana",  0.68),
    ("How to control Phytophthora in black pepper?",       "pepper",  0.70),
    ("What is the seed rate for rice cultivation?",        "rice",    0.70),
]

For each query:
  1. Call retrieve_kau_advice(query, crop, top_k=3)
  2. Print top result content (truncated to 200 chars)
  3. Print similarity score
  4. PASS if similarity >= threshold, FAIL otherwise
  5. At end: print "X/5 tests passed"
  6. Exit code 1 if any test fails (so CI can detect it)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TEST SPEC (tests/test_rag.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  test_chunk_text_produces_correct_chunks()
    input: 1500 token text
    assert len(chunks) == 3 (512/50 overlap)
    assert all chunks >= 50 tokens

  test_crop_detection_from_filename()
    assert detect_crop_from_filename("kau_coconut_pop.pdf") == "coconut"
    assert detect_crop_from_filename("kau_rice_package.pdf") == "rice"
    assert detect_crop_from_filename("unknown.pdf") == "general"

  test_passage_prefix_applied()
    mock SentenceTransformer.encode
    call chunk_embed(["test chunk"])
    assert encode was called with "passage: [Kerala crop advisory] test chunk"

  test_query_prefix_applied()
    mock SentenceTransformer.encode + asyncpg
    call retrieve_kau_advice("coconut fertilizer", "coconut")
    assert encode was called with "query: coconut fertilizer"

  test_retrieve_returns_rag_results()
    mock asyncpg returning 3 rows with similarity 0.82, 0.78, 0.71
    result = await retrieve_kau_advice("coconut NPK dose")
    assert len(result) == 3
    assert result[0].similarity == 0.82
    assert isinstance(result[0], RAGResult)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GITHUB ISSUE PROTOCOL — PHASE 3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After tests pass:
  python scripts/validate_embeddings.py → all 5 queries similarity >= 0.70
  pytest tests/test_rag.py -v → 0 failures

  git checkout dev/m3-rag
  git add -A
  git commit -m "feat(phase-3): KAU RAG pipeline — multilingual-e5-large, pgvector HNSW, 14-district soil data"
  git tag v0.3.0

Create GitHub Issue:
  Title: [Phase 3] KAU RAG Knowledge Pipeline
  Labels: phase-3, rag
  Assign: @M3
  Body: (list files created, validation output, test results, PROTECTED files)

Print: "✅ Phase 3 committed to dev/m3-rag. Issue created. Waiting for team review."
STOP — wait for confirmation before Phase 4.
```

---

## What This Phase Builds

| Component | Detail |
|---|---|
| `scripts/ingest_kau_docs.py` | PDF → 512-token chunks → embed → pgvector HNSW |
| `app/services/rag_service.py` | Async retrieval with `query:` prefix + fallback |
| `scripts/validate_embeddings.py` | 5 test queries, similarity ≥ 0.70 |
| `tests/test_rag.py` | 5 pytest tests with mocks |
| HNSW index | `m=16, ef_construction=64` on `embedding vector_cosine_ops` |
| Crop detection | Auto-detects from PDF filename |
| Idempotent ingestion | Skips already-ingested chunks |

## GitHub Issue Created After This Phase

```
Title: [Phase 3] KAU RAG Knowledge Pipeline
Branch: dev/m3-rag
Labels: phase-3, rag
Assign to: M3
```

---

> **Next:** Paste `05-phase4-android.md` after Issue #3 is reviewed and merged
