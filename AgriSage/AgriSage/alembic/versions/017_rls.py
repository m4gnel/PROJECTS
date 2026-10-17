"""017_rls

Revision ID: 017_rls
Revises: 016_audit
Create Date: 2026-09-30 00:00:17.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '017_rls'
down_revision: Union[str, None] = '016_audit'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE farms ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE fields ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE crop_cycles ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE observations ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE images ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE advisories ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;")

    op.execute("""
    CREATE POLICY farms_owner ON farms
        USING (user_id = NULLIF(current_setting('app.current_user_id', true), '')::UUID);
    """)
    op.execute("""
    CREATE POLICY fields_owner ON fields
        USING (farm_id IN (SELECT id FROM farms WHERE user_id = NULLIF(current_setting('app.current_user_id', true), '')::UUID));
    """)
    op.execute("""
    CREATE POLICY cycles_owner ON crop_cycles
        USING (field_id IN (SELECT f.id FROM fields f JOIN farms fa ON f.farm_id=fa.id WHERE fa.user_id = NULLIF(current_setting('app.current_user_id', true), '')::UUID));
    """)
    op.execute("""
    CREATE POLICY obs_owner ON observations
        USING (crop_cycle_id IN (SELECT cc.id FROM crop_cycles cc JOIN fields f ON cc.field_id=f.id JOIN farms fa ON f.farm_id=fa.id WHERE fa.user_id = NULLIF(current_setting('app.current_user_id', true), '')::UUID));
    """)
    op.execute("""
    CREATE POLICY adv_owner ON advisories
        USING (observation_id IN (SELECT o.id FROM observations o JOIN crop_cycles cc ON o.crop_cycle_id=cc.id JOIN fields f ON cc.field_id=f.id JOIN farms fa ON f.farm_id=fa.id WHERE fa.user_id = NULLIF(current_setting('app.current_user_id', true), '')::UUID));
    """)
    op.execute("""
    CREATE POLICY notif_owner ON notifications
        USING (user_id = NULLIF(current_setting('app.current_user_id', true), '')::UUID);
    """)


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS notif_owner ON notifications;")
    op.execute("DROP POLICY IF EXISTS adv_owner ON advisories;")
    op.execute("DROP POLICY IF EXISTS obs_owner ON observations;")
    op.execute("DROP POLICY IF EXISTS cycles_owner ON crop_cycles;")
    op.execute("DROP POLICY IF EXISTS fields_owner ON fields;")
    op.execute("DROP POLICY IF EXISTS farms_owner ON farms;")
    op.execute("ALTER TABLE notifications DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE advisories DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE images DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE observations DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE crop_cycles DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE fields DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE farms DISABLE ROW LEVEL SECURITY;")
