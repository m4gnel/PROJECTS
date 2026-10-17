"""006_weather

Revision ID: 006_weather
Revises: 005_observations
Create Date: 2026-09-30 00:00:06.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '006_weather'
down_revision: Union[str, None] = '005_observations'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE weather_cache (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        location_key VARCHAR(20) NOT NULL UNIQUE,
        data_json JSONB NOT NULL,
        cached_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS weather_cache CASCADE;")
