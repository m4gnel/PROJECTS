"""004_crop_cycles

Revision ID: 004_crop_cycles
Revises: 003_farms
Create Date: 2026-09-30 00:00:04.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '004_crop_cycles'
down_revision: Union[str, None] = '003_farms'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE crop_cycles (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        field_id UUID NOT NULL REFERENCES fields(id) ON DELETE CASCADE,
        crop VARCHAR(50) NOT NULL CHECK (crop IN ('rice','banana','coconut','tomato','maize')),
        cultivar VARCHAR(100), season VARCHAR(20),
        planting_date DATE NOT NULL,
        expected_harvest DATE, actual_harvest DATE,
        status VARCHAR(20) NOT NULL DEFAULT 'active'
            CHECK (status IN ('active','harvested','abandoned')),
        notes TEXT,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_cycles_field ON crop_cycles(field_id);")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS crop_cycles CASCADE;")
