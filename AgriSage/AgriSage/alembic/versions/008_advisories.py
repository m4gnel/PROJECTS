"""008_advisories

Revision ID: 008_advisories
Revises: 007_diagnoses
Create Date: 2026-09-30 00:00:08.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '008_advisories'
down_revision: Union[str, None] = '007_diagnoses'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE advisories (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        observation_id UUID NOT NULL REFERENCES observations(id) ON DELETE CASCADE,
        confidence_state VARCHAR(30) NOT NULL
            CHECK (confidence_state IN ('CONFIRMED','LIKELY','POSSIBLE','UNCERTAIN',
                   'INSUFFICIENT_DATA','CONFLICTING_EVIDENCE','OUT_OF_SCOPE')),
        confidence_score DECIMAL(4,2),
        recommended_scenario VARCHAR(5),
        scenarios_json JSONB NOT NULL,
        evidence_bundle_json JSONB NOT NULL,
        recommended_action_json JSONB NOT NULL,
        what_would_change_json JSONB,
        safe_to_act BOOLEAN NOT NULL DEFAULT true,
        sources_json JSONB,
        scheme_matches_json JSONB,
        model_version VARCHAR(50),
        knowledge_version VARCHAR(50),
        generation_ms INTEGER,
        farmer_feedback VARCHAR(20),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_adv_obs ON advisories(observation_id);")
    op.execute("CREATE INDEX idx_adv_created ON advisories(created_at DESC);")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS advisories CASCADE;")
