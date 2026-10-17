"""014_notifications

Revision ID: 014_notifications
Revises: 013_market
Create Date: 2026-09-30 00:00:14.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '014_notifications'
down_revision: Union[str, None] = '013_market'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE notifications (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        type VARCHAR(50) NOT NULL,
        title VARCHAR(300), body TEXT,
        data_json JSONB, is_read BOOLEAN DEFAULT false,
        sent_at TIMESTAMPTZ, read_at TIMESTAMPTZ,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_notif_user ON notifications(user_id, created_at DESC);")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS notifications CASCADE;")
