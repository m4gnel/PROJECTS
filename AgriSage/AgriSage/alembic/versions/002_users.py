"""002_users

Revision ID: 002_users
Revises: 001_extensions
Create Date: 2026-09-30 00:00:02.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '002_users'
down_revision: Union[str, None] = '001_extensions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE users (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        phone VARCHAR(15) UNIQUE NOT NULL,
        name VARCHAR(100),
        language VARCHAR(10) NOT NULL DEFAULT 'ml',
        location_lat DECIMAL(9,6), location_lon DECIMAL(9,6),
        district VARCHAR(100), state VARCHAR(100) DEFAULT 'Kerala',
        subscription_tier VARCHAR(20) NOT NULL DEFAULT 'free',
        subscription_expires TIMESTAMPTZ,
        trial_started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        advisories_this_month INT NOT NULL DEFAULT 0,
        advisories_reset_at DATE NOT NULL DEFAULT CURRENT_DATE,
        is_active BOOLEAN NOT NULL DEFAULT true,
        fcm_token VARCHAR(500),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        last_active_at TIMESTAMPTZ
    );
    """)
    op.execute("CREATE INDEX idx_users_phone ON users(phone);")

    op.execute("""
    CREATE TABLE otp_sessions (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        phone VARCHAR(15) NOT NULL,
        otp_hash VARCHAR(255) NOT NULL,
        expires_at TIMESTAMPTZ NOT NULL,
        attempts INT NOT NULL DEFAULT 0,
        used BOOLEAN NOT NULL DEFAULT false,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_otp_phone ON otp_sessions(phone);")

    op.execute("""
    CREATE TABLE refresh_tokens (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        token_hash VARCHAR(255) NOT NULL UNIQUE,
        expires_at TIMESTAMPTZ NOT NULL,
        revoked BOOLEAN NOT NULL DEFAULT false,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_refresh_tokens_user ON refresh_tokens(user_id);")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS refresh_tokens CASCADE;")
    op.execute("DROP TABLE IF EXISTS otp_sessions CASCADE;")
    op.execute("DROP TABLE IF EXISTS users CASCADE;")
