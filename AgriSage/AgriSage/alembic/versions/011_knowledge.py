"""011_knowledge

Revision ID: 011_knowledge
Revises: 010_simulation
Create Date: 2026-09-30 00:00:11.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '011_knowledge'
down_revision: Union[str, None] = '010_simulation'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE knowledge_documents (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        title VARCHAR(500), crop VARCHAR(50), state VARCHAR(100),
        topic VARCHAR(100), growth_stage VARCHAR(50),
        source_tier INTEGER NOT NULL CHECK (source_tier BETWEEN 1 AND 6),
        source_authority VARCHAR(200), source_url VARCHAR(1000),
        language VARCHAR(10) NOT NULL DEFAULT 'en',
        published_at DATE, valid_until DATE NOT NULL,
        status VARCHAR(20) NOT NULL DEFAULT 'PUBLISHED'
            CHECK (status IN ('DISCOVERED','PARSED','VALIDATED','APPROVED',
                   'PUBLISHED','SUPERSEDED','ARCHIVED')),
        content_hash CHAR(64), version INTEGER NOT NULL DEFAULT 1,
        license VARCHAR(100),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)

    op.execute("""
    CREATE TABLE knowledge_chunks (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        document_id UUID NOT NULL REFERENCES knowledge_documents(id) ON DELETE CASCADE,
        chunk_index INTEGER NOT NULL,
        content TEXT NOT NULL,
        embedding vector(1024),
        metadata JSONB,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        UNIQUE(document_id, chunk_index)
    );
    """)

    op.execute("""
    CREATE INDEX idx_chunks_embedding ON knowledge_chunks
        USING hnsw (embedding vector_cosine_ops)
        WITH (m=16, ef_construction=64);
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS knowledge_chunks CASCADE;")
    op.execute("DROP TABLE IF EXISTS knowledge_documents CASCADE;")
