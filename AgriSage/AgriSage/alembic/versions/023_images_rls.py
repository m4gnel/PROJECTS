"""023_images_rls

Revision ID: 023_images_rls
Revises: 022_rls_policy_repair
Create Date: 2026-10-21 00:00:23.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = "023_images_rls"
down_revision: Union[str, None] = "022_rls_policy_repair"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Repair the missing owner policy on the FORCE-RLS images table."""
    op.execute("DROP POLICY IF EXISTS images_owner ON images;")
    op.execute(
        """
        CREATE POLICY images_owner ON images
        USING (observation_id IN (
            SELECT o.id
            FROM observations o
            JOIN crop_cycles cc ON o.crop_cycle_id = cc.id
            JOIN fields f ON cc.field_id = f.id
            JOIN farms fa ON f.farm_id = fa.id
            WHERE fa.user_id = NULLIF(current_setting('app.current_user_id', true), '')::UUID
        ))
        WITH CHECK (observation_id IN (
            SELECT o.id
            FROM observations o
            JOIN crop_cycles cc ON o.crop_cycle_id = cc.id
            JOIN fields f ON cc.field_id = f.id
            JOIN farms fa ON f.farm_id = fa.id
            WHERE fa.user_id = NULLIF(current_setting('app.current_user_id', true), '')::UUID
        ));
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS images_owner ON images;")
