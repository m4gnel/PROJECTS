"""019_user_rbac

Revision ID: 019_user_rbac
Revises: 018_master_database_schema
Create Date: 2026-10-18 00:00:19.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "019_user_rbac"
down_revision: Union[str, None] = "018_master_database_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add additive role/permission state to the existing public users table."""

    op.add_column("users", sa.Column("role", sa.String(length=20), nullable=True))
    op.add_column(
        "users",
        sa.Column("permissions", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.execute("UPDATE users SET role = 'farmer' WHERE role IS NULL;")
    op.execute("UPDATE users SET permissions = '[]'::jsonb WHERE permissions IS NULL;")
    op.alter_column("users", "role", nullable=False, server_default="farmer")
    op.alter_column(
        "users",
        "permissions",
        nullable=False,
        server_default=sa.text("'[]'::jsonb"),
    )
    op.create_check_constraint(
        "chk_users_role",
        "users",
        "role IN ('farmer','employee','officer','expert')",
    )
    op.create_check_constraint(
        "chk_users_permissions_array",
        "users",
        "jsonb_typeof(permissions) = 'array'",
    )
    op.create_index("idx_users_role", "users", ["role"])

    # Existing FORCE RLS policies otherwise hide the global advisory queue from
    # staff. These policies are scoped to the authenticated session user and
    # persisted role; they do not grant access based on an untrusted JWT claim.
    for table, policy in (
        ("farms", "farms_operations_staff"),
        ("fields", "fields_operations_staff"),
        ("crop_cycles", "cycles_operations_staff"),
        ("observations", "observations_operations_staff"),
        ("advisories", "advisories_operations_staff"),
    ):
        op.execute(
            f"""
            CREATE POLICY {policy} ON {table}
            FOR SELECT
            USING (
                EXISTS (
                    SELECT 1
                    FROM users
                    WHERE users.id = NULLIF(current_setting('app.current_user_id', true), '')::UUID
                      AND users.role IN ('employee', 'officer')
                )
            );
            """
        )
    for table, policy in (
        ("farms", "farms_expert_queue"),
        ("fields", "fields_expert_queue"),
        ("crop_cycles", "cycles_expert_queue"),
        ("observations", "observations_expert_queue"),
        ("advisories", "advisories_expert_queue"),
    ):
        op.execute(
            f"""
            CREATE POLICY {policy} ON {table}
            FOR SELECT
            USING (
                EXISTS (
                    SELECT 1
                    FROM users
                    WHERE users.id = NULLIF(current_setting('app.current_user_id', true), '')::UUID
                      AND (users.role = 'expert' OR users.subscription_tier = 'expert')
                )
            );
            """
        )


def downgrade() -> None:
    for table, policy in (
        ("advisories", "advisories_expert_queue"),
        ("observations", "observations_expert_queue"),
        ("crop_cycles", "cycles_expert_queue"),
        ("fields", "fields_expert_queue"),
        ("farms", "farms_expert_queue"),
    ):
        op.execute(f"DROP POLICY IF EXISTS {policy} ON {table};")
    for table, policy in (
        ("advisories", "advisories_operations_staff"),
        ("observations", "observations_operations_staff"),
        ("crop_cycles", "cycles_operations_staff"),
        ("fields", "fields_operations_staff"),
        ("farms", "farms_operations_staff"),
    ):
        op.execute(f"DROP POLICY IF EXISTS {policy} ON {table};")
    op.drop_index("idx_users_role", table_name="users")
    op.drop_constraint("chk_users_permissions_array", "users", type_="check")
    op.drop_constraint("chk_users_role", "users", type_="check")
    op.drop_column("users", "permissions")
    op.drop_column("users", "role")
