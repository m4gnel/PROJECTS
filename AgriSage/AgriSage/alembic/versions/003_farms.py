"""003_farms

Revision ID: 003_farms
Revises: 002_users
Create Date: 2026-09-30 00:00:03.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '003_farms'
down_revision: Union[str, None] = '002_users'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE farms (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        name VARCHAR(200) NOT NULL,
        location_lat DECIMAL(9,6), location_lon DECIMAL(9,6),
        district VARCHAR(100), state VARCHAR(100),
        area_ha DECIMAL(8,2),
        is_active BOOLEAN NOT NULL DEFAULT true,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_farms_user ON farms(user_id);")

    op.execute("""
    CREATE TABLE fields (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        farm_id UUID NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
        name VARCHAR(100),
        area_ha DECIMAL(8,2), slope VARCHAR(20),
        irrigation VARCHAR(30), soil_type VARCHAR(50),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_fields_farm ON fields(farm_id);")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS fields CASCADE;")
    op.execute("DROP TABLE IF EXISTS farms CASCADE;")
