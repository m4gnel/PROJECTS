import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import (
    Column, String, Boolean, Float, Numeric, Date, DateTime,
    ForeignKey, Index, UniqueConstraint, func, Text
)
from sqlalchemy.dialects.postgresql import UUID

from backend.database import Base


class MarketRecommendation(Base):
    __tablename__ = "market_recommendations"
    __table_args__ = (
        Index("idx_market_rec_farmer", "farmer_id", "generated_at"),
        Index("idx_market_rec_crop", "crop_name", "state", "generated_at"),
        {"schema": "market"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("core.farmers.id", ondelete="CASCADE"), nullable=False)
    crop_name = Column(String, nullable=False)
    state = Column(String, nullable=False)
    district = Column(String, nullable=False)
    generated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    current_modal_price = Column(Numeric(10, 2), nullable=True)
    nearest_market = Column(String, nullable=True)
    price_date = Column(Date, nullable=True)

    recommendation = Column(String(30), nullable=False)
    rationale = Column(Text, nullable=False)
    rationale_native = Column(Text, nullable=True)
    target_price = Column(Numeric(10, 2), nullable=True)
    hold_until_estimate = Column(Date, nullable=True)

    price_trend_7d = Column(String(20), nullable=True)
    price_trend_30d = Column(String(20), nullable=True)
    pct_above_msp = Column(Float, nullable=True)
    seasonal_factor = Column(String, nullable=True)

    valid_until = Column(Date, nullable=True)
    was_helpful = Column(Boolean, nullable=True)


class PriceSubscription(Base):
    __tablename__ = "price_subscriptions"
    __table_args__ = (
        UniqueConstraint("farmer_id", "crop_name", "state"),
        Index("idx_price_subs_farmer", "farmer_id", postgresql_where=Column("is_active") == True),
        {"schema": "market"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("core.farmers.id", ondelete="CASCADE"), nullable=False)
    crop_name = Column(String, nullable=False)
    state = Column(String, nullable=False)
    alert_above = Column(Numeric(10, 2), nullable=True)
    alert_below = Column(Numeric(10, 2), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
