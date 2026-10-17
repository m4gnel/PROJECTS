"""015_expert

Revision ID: 015_expert
Revises: 014_notifications
Create Date: 2026-09-30 00:00:15.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '015_expert'
down_revision: Union[str, None] = '014_notifications'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE expert_reviews (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        advisory_id UUID NOT NULL REFERENCES advisories(id),
        expert_id UUID NOT NULL REFERENCES users(id),
        verdict VARCHAR(20) CHECK (verdict IN ('correct','partially_correct','incorrect','insufficient_data')),
        notes TEXT, corrected_diagnosis VARCHAR(100),
        reviewed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS expert_reviews CASCADE;")
