"""018_master_database_schema

Revision ID: 018_master_database_schema
Revises: 017_rls
Create Date: 2026-10-06 18:00:00.000000

"""
import os
from typing import Sequence, Union
from alembic import op

revision: str = '018_master_database_schema'
down_revision: Union[str, None] = '017_rls'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sql_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'backend', 'init_master_database.sql')
    if os.path.exists(sql_path):
        with open(sql_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        op.execute(sql_content)
    else:
        # Fallback inline execution
        op.execute("CREATE SCHEMA IF NOT EXISTS core;")
        op.execute("CREATE SCHEMA IF NOT EXISTS realtime;")
        op.execute("CREATE SCHEMA IF NOT EXISTS agents;")
        op.execute("CREATE SCHEMA IF NOT EXISTS intelligence;")
        op.execute("CREATE SCHEMA IF NOT EXISTS alerts;")
        op.execute("CREATE SCHEMA IF NOT EXISTS market;")
        op.execute("CREATE SCHEMA IF NOT EXISTS analytics;")
        op.execute("CREATE SCHEMA IF NOT EXISTS system;")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS system CASCADE;")
    op.execute("DROP SCHEMA IF EXISTS analytics CASCADE;")
    op.execute("DROP SCHEMA IF EXISTS market CASCADE;")
    op.execute("DROP SCHEMA IF EXISTS alerts CASCADE;")
    op.execute("DROP SCHEMA IF EXISTS intelligence CASCADE;")
    op.execute("DROP SCHEMA IF EXISTS agents CASCADE;")
    op.execute("DROP SCHEMA IF EXISTS realtime CASCADE;")
    op.execute("DROP SCHEMA IF EXISTS core CASCADE;")
