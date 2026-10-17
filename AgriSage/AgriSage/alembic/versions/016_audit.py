"""016_audit

Revision ID: 016_audit
Revises: 015_expert
Create Date: 2026-09-30 00:00:16.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '016_audit'
down_revision: Union[str, None] = '015_expert'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE audit_logs (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        user_id UUID REFERENCES users(id),
        event_type VARCHAR(100) NOT NULL,
        event_data JSONB,
        ip_address INET,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_audit_type_date ON audit_logs(event_type, created_at DESC);")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS audit_logs CASCADE;")
