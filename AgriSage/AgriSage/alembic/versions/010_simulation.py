"""010_simulation

Revision ID: 010_simulation
Revises: 009_interventions
Create Date: 2026-09-30 00:00:10.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '010_simulation'
down_revision: Union[str, None] = '009_interventions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE simulation_results (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        advisory_id UUID NOT NULL REFERENCES advisories(id),
        engine VARCHAR(20) DEFAULT 'dssat',
        scenario_id VARCHAR(5),
        params_json JSONB, results_json JSONB,
        yield_kgha DECIMAL(10,2), net_return_inr DECIMAL(12,2),
        is_modelled_estimate BOOLEAN NOT NULL DEFAULT true,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS simulation_results CASCADE;")
