"""009_interventions

Revision ID: 009_interventions
Revises: 008_advisories
Create Date: 2026-09-30 00:00:09.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '009_interventions'
down_revision: Union[str, None] = '008_advisories'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE interventions (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        crop_cycle_id UUID NOT NULL REFERENCES crop_cycles(id),
        advisory_id UUID REFERENCES advisories(id),
        intervention_type VARCHAR(50) NOT NULL,
        product_name VARCHAR(200), dosage VARCHAR(100),
        cost_inr DECIMAL(10,2), applied_at DATE,
        notes TEXT,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)

    op.execute("""
    CREATE TABLE outcomes (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        intervention_id UUID NOT NULL REFERENCES interventions(id),
        observed_at DATE NOT NULL,
        effectiveness VARCHAR(20),
        yield_actual_kgha DECIMAL(10,2),
        notes TEXT,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS outcomes CASCADE;")
    op.execute("DROP TABLE IF EXISTS interventions CASCADE;")
