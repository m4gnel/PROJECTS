"""007_diagnoses

Revision ID: 007_diagnoses
Revises: 006_weather
Create Date: 2026-09-30 00:00:07.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '007_diagnoses'
down_revision: Union[str, None] = '006_weather'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE diagnoses (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        observation_id UUID NOT NULL REFERENCES observations(id) ON DELETE CASCADE,
        pipeline_trace_id VARCHAR(100),
        started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        completed_at TIMESTAMPTZ,
        generation_ms INTEGER,
        model_version VARCHAR(50),
        status VARCHAR(20) DEFAULT 'pending'
    );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS diagnoses CASCADE;")
