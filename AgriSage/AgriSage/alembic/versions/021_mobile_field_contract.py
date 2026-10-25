"""021_mobile_field_contract

Revision ID: 021_mobile_field_contract
Revises: 020_auth_rate_limits
Create Date: 2026-10-19 00:00:21.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "021_mobile_field_contract"
down_revision: Union[str, None] = "020_auth_rate_limits"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("farms", sa.Column("location_lat", sa.Numeric(9, 6), nullable=True))
    op.add_column("farms", sa.Column("location_lon", sa.Numeric(9, 6), nullable=True))
    op.add_column("fields", sa.Column("latitude", sa.Numeric(9, 6), nullable=True))
    op.add_column("fields", sa.Column("longitude", sa.Numeric(9, 6), nullable=True))


def downgrade() -> None:
    op.drop_column("fields", "longitude")
    op.drop_column("fields", "latitude")
    op.drop_column("farms", "location_lon")
    op.drop_column("farms", "location_lat")
