"""005_observations

Revision ID: 005_observations
Revises: 004_crop_cycles
Create Date: 2026-09-30 00:00:05.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '005_observations'
down_revision: Union[str, None] = '004_crop_cycles'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE observations (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        crop_cycle_id UUID NOT NULL REFERENCES crop_cycles(id) ON DELETE CASCADE,
        location_lat DECIMAL(9,6), location_lon DECIMAL(9,6),
        problem_description TEXT,
        voice_note_key VARCHAR(500),
        irrigation_status VARCHAR(20),
        fertilizer_recent BOOLEAN, pesticide_recent BOOLEAN,
        observed_growth_stage VARCHAR(50),
        observed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_obs_cycle ON observations(crop_cycle_id);")

    op.execute("""
    CREATE TABLE images (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        observation_id UUID NOT NULL REFERENCES observations(id) ON DELETE CASCADE,
        r2_key VARCHAR(500) NOT NULL UNIQUE,
        mime_type VARCHAR(50) NOT NULL,
        file_size_bytes INTEGER, width_px INTEGER, height_px INTEGER,
        quality_score DECIMAL(4,2) CHECK (quality_score BETWEEN 0 AND 1),
        blur_score DECIMAL(8,2),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_images_obs ON images(observation_id);")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS images CASCADE;")
    op.execute("DROP TABLE IF EXISTS observations CASCADE;")
