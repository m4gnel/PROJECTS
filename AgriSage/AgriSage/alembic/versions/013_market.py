"""013_market

Revision ID: 013_market
Revises: 012_schemes
Create Date: 2026-09-30 00:00:13.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '013_market'
down_revision: Union[str, None] = '012_schemes'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE market_prices (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        crop VARCHAR(50) NOT NULL, variety VARCHAR(100),
        market_name VARCHAR(200), district VARCHAR(100), state VARCHAR(100),
        price_min_inr DECIMAL(10,2), price_max_inr DECIMAL(10,2),
        price_modal_inr DECIMAL(10,2),
        recorded_date DATE NOT NULL,
        source VARCHAR(100) DEFAULT 'enam',
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_market_crop_date ON market_prices(crop, recorded_date DESC);")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS market_prices CASCADE;")
