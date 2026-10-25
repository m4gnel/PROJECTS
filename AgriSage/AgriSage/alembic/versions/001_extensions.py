"""001_extensions

Revision ID: 001_extensions
Revises: 
Create Date: 2026-09-30 00:00:01.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '001_extensions'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.execute('CREATE EXTENSION IF NOT EXISTS vector;')


def downgrade() -> None:
    op.execute('DROP EXTENSION IF EXISTS vector;')
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp";')
