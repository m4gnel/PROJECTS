import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Column, String, Boolean, Integer, DateTime,
    ForeignKey, Index, UniqueConstraint, func, ARRAY, Text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB

from backend.database import Base


class AuditLog(Base):
    __tablename__ = "audit_log"
    __table_args__ = (
        Index("idx_audit_farmer", "farmer_id", "performed_at", postgresql_where=Column("farmer_id") != None),
        Index("idx_audit_table", "table_name", "performed_at"),
        {"schema": "system"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    table_schema = Column(String, nullable=False)
    table_name = Column(String, nullable=False)
    operation = Column(String(20), nullable=False)
    record_id = Column(UUID(as_uuid=True), nullable=True)
    farmer_id = Column(UUID(as_uuid=True), nullable=True)
    old_data = Column(JSONB, nullable=True)
    new_data = Column(JSONB, nullable=True)
    changed_fields = Column(ARRAY(Text), nullable=True)
    performed_at = Column(DateTime(timezone=True), primary_key=True, server_default=func.now())


class APIRateLimit(Base):
    __tablename__ = "api_rate_limits"
    __table_args__ = (
        Index("idx_rate_limit_farmer", "farmer_id", "window_start"),
        {"schema": "system"}
    )

    farmer_id = Column(UUID(as_uuid=True), ForeignKey("core.farmers.id", ondelete="CASCADE"), primary_key=True)
    window_start = Column(DateTime(timezone=True), primary_key=True)
    window_minutes = Column(Integer, nullable=False, default=60)
    request_count = Column(Integer, nullable=False, default=1)
    max_allowed = Column(Integer, nullable=False, default=100)
    is_limited = Column(Boolean, nullable=True)
