import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import (
    Column, String, Integer, Float, Numeric, Date, DateTime,
    ForeignKey, CheckConstraint, Index, UniqueConstraint, func, Text
)
from sqlalchemy.dialects.postgresql import UUID

from backend.database import Base


class FarmSeasonAnalytics(Base):
    __tablename__ = "farm_season_analytics"
    __table_args__ = (
        UniqueConstraint("farm_id", "crop_name", "season", "season_year"),
        Index("idx_season_analytics_farmer", "farmer_id"),
        Index("idx_season_analytics_crop", "crop_name", "season_year"),
        {"schema": "analytics"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(as_uuid=True), ForeignKey("core.farms.id"), nullable=False)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("core.farmers.id"), nullable=False)
    crop_name = Column(String, nullable=False)
    season = Column(String(20), nullable=False)
    season_year = Column(Integer, nullable=False)

    total_queries = Column(Integer, default=0)
    queries_about_pest = Column(Integer, default=0)
    queries_about_weather = Column(Integer, default=0)
    queries_about_market = Column(Integer, default=0)
    queries_about_soil = Column(Integer, default=0)
    advisories_followed = Column(Integer, default=0)
    advisories_ignored = Column(Integer, default=0)

    critical_alerts_received = Column(Integer, default=0)
    alerts_acted_upon = Column(Integer, default=0)

    actual_yield_kg_ha = Column(Float, nullable=True)
    dssat_predicted_yield = Column(Float, nullable=True)
    yield_accuracy_pct = Column(Float, nullable=True)
    sold_price_per_quintal = Column(Numeric(10, 2), nullable=True)
    total_revenue_inr = Column(Numeric(12, 2), nullable=True)

    overall_satisfaction = Column(Integer, nullable=True)
    nps_score = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())


class AgentPerformance(Base):
    __tablename__ = "agent_performance"
    __table_args__ = (
        UniqueConstraint("agent_name", "metric_date"),
        Index("idx_agent_perf_date", "metric_date"),
        Index("idx_agent_perf_name", "agent_name", "metric_date"),
        {"schema": "analytics"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_name = Column(String, nullable=False)
    metric_date = Column(Date, nullable=False)
    total_invocations = Column(Integer, default=0)
    successful = Column(Integer, default=0)
    failed = Column(Integer, default=0)
    success_rate_pct = Column(Float, nullable=True)

    avg_duration_ms = Column(Float, nullable=True)
    p50_duration_ms = Column(Float, nullable=True)
    p95_duration_ms = Column(Float, nullable=True)
    p99_duration_ms = Column(Float, nullable=True)
    total_gemini_calls = Column(Integer, default=0)
    total_tokens_used = Column(Integer, default=0)
    cache_hit_count = Column(Integer, default=0)
    cache_hit_rate_pct = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class PlatformMetrics(Base):
    __tablename__ = "platform_metrics"
    __table_args__ = (
        Index("idx_platform_metrics_date", "metric_date"),
        {"schema": "analytics"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric_date = Column(Date, unique=True, nullable=False)
    dau = Column(Integer, default=0)
    new_registrations = Column(Integer, default=0)
    total_registered = Column(Integer, default=0)
    total_queries = Column(Integer, default=0)
    avg_response_ms = Column(Float, nullable=True)
    p95_response_ms = Column(Float, nullable=True)
    total_agent_calls = Column(Integer, default=0)
    gemini_calls_total = Column(Integer, default=0)
    gemini_tokens_total = Column(Integer, default=0)
    alerts_sent = Column(Integer, default=0)
    fcm_success_rate_pct = Column(Float, nullable=True)
    error_count = Column(Integer, default=0)
    error_rate_pct = Column(Float, nullable=True)
    weather_cache_hits = Column(Integer, default=0)
    market_cache_hits = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class AdvisoryFeedback(Base):
    __tablename__ = "advisory_feedback"
    __table_args__ = (
        Index("idx_feedback_session", "session_id"),
        Index("idx_feedback_rating", "rating", "created_at"),
        {"schema": "analytics"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = Column(UUID(as_uuid=True), nullable=False)
    session_id = Column(UUID(as_uuid=True), ForeignKey("agents.advisory_sessions.id"), nullable=False)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("core.farmers.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    feedback_text = Column(Text, nullable=True)
    feedback_text_en = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
