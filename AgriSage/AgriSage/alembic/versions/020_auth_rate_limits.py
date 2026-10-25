"""020_auth_rate_limits

Revision ID: 020_auth_rate_limits
Revises: 019_user_rbac
Create Date: 2026-10-19 00:00:20.000000

"""

from typing import Sequence, Union

from alembic import op


revision: str = "020_auth_rate_limits"
down_revision: Union[str, None] = "019_user_rbac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE auth_rate_limits (
            rate_key TEXT PRIMARY KEY,
            window_start TIMESTAMPTZ NOT NULL,
            request_count INTEGER NOT NULL DEFAULT 0 CHECK (request_count >= 0),
            max_allowed INTEGER NOT NULL CHECK (max_allowed > 0),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        """
    )
    op.execute(
        "CREATE INDEX idx_auth_rate_limits_updated_at ON auth_rate_limits(updated_at);"
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS auth_rate_limits;")
