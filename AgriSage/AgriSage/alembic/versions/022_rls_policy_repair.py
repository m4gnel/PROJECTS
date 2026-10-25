"""022_rls_policy_repair

Revision ID: 022_rls_policy_repair
Revises: 021_mobile_field_contract
Create Date: 2026-10-19 00:00:22.000000

"""

from typing import Sequence, Union

from alembic import op


revision: str = "022_rls_policy_repair"
down_revision: Union[str, None] = "021_mobile_field_contract"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


_STAFF_POLICIES = (
    ("farms", "farms_operations_staff"),
    ("fields", "fields_operations_staff"),
    ("crop_cycles", "cycles_operations_staff"),
    ("observations", "observations_operations_staff"),
    ("advisories", "advisories_operations_staff"),
)

_EXPERT_POLICIES = (
    ("farms", "farms_expert_queue"),
    ("fields", "fields_expert_queue"),
    ("crop_cycles", "cycles_expert_queue"),
    ("observations", "observations_expert_queue"),
    ("advisories", "advisories_expert_queue"),
)

def _drop_policies() -> None:
    op.execute("DROP POLICY IF EXISTS adv_operations_staff ON advisories;")
    op.execute("DROP POLICY IF EXISTS images_owner ON images;")
    for table, policy in (*_STAFF_POLICIES, *_EXPERT_POLICIES):
        op.execute(f"DROP POLICY IF EXISTS {policy} ON {table};")


def _create_policies() -> None:
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
    for table, policy in _STAFF_POLICIES:
        op.execute(
            f"""
            CREATE POLICY {policy} ON {table}
            FOR SELECT
            USING (
                EXISTS (
                    SELECT 1 FROM users
                    WHERE users.id = NULLIF(current_setting('app.current_user_id', true), '')::UUID
                      AND users.role IN ('employee', 'officer')
                )
            );
            """
        )
    for table, policy in _EXPERT_POLICIES:
        op.execute(
            f"""
            CREATE POLICY {policy} ON {table}
            FOR SELECT
            USING (
                EXISTS (
                    SELECT 1 FROM users
                    WHERE users.id = NULLIF(current_setting('app.current_user_id', true), '')::UUID
                      AND (users.role = 'expert' OR users.subscription_tier = 'expert')
                )
            );
            """
        )


def upgrade() -> None:
    """Repair policy sets for databases that already applied migration 019."""

    _drop_policies()
    _create_policies()


def downgrade() -> None:
    # 021's canonical migration also contains the expanded policy set. Keep
    # that safe set when rolling back this compatibility repair rather than
    # leaving FORCE RLS tables with no staff/expert read policy.
    _drop_policies()
    _create_policies()
