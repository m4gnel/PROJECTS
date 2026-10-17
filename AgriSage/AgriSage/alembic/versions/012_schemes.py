"""012_schemes

Revision ID: 012_schemes
Revises: 011_knowledge
Create Date: 2026-09-30 00:00:12.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '012_schemes'
down_revision: Union[str, None] = '011_knowledge'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE schemes (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        name VARCHAR(300) NOT NULL, short_name VARCHAR(50),
        authority VARCHAR(200), authority_level VARCHAR(20),
        state VARCHAR(100), crops_applicable JSONB,
        eligibility_rules JSONB NOT NULL, benefits_json JSONB,
        enrollment_url VARCHAR(500), helpline VARCHAR(50),
        valid_from DATE, valid_until DATE NOT NULL,
        status VARCHAR(20) NOT NULL DEFAULT 'active',
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS schemes CASCADE;")
