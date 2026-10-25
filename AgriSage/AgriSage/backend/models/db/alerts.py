import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Column, String, Boolean, Integer, Float, DateTime,
    ForeignKey, CheckConstraint, Index, func, Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from backend.database import Base


class FarmerAlert(Base):
    __tablename__ = "farmer_alerts"
    __table_args__ = (
        Index("idx_farmer_alerts_farmer", "farmer_id", "created_at"),
        Index("idx_farmer_alerts_unread", "farmer_id", postgresql_where=(Column("is_read") == False) & (Column("is_dismissed") == False)),
        Index("idx_farmer_alerts_severity", "severity", "created_at"),
        Index("idx_farmer_alerts_expires", "expires_at"),
        {"schema": "alerts"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("core.farmers.id", ondelete="CASCADE"), nullable=False)
    field_id = Column(UUID(as_uuid=True), ForeignKey("core.fields.id"), nullable=True)

    category = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)
    title_native = Column(Text, nullable=False)
    title_en = Column(Text, nullable=False)
    body_native = Column(Text, nullable=False)
    body_en = Column(Text, nullable=False)
    language = Column(String(10), nullable=False)

    source_agent = Column(String, nullable=True)
    source_data_type = Column(String, nullable=True)
    source_data_id = Column(UUID(as_uuid=True), nullable=True)

    action_type = Column(String(50), nullable=True)
    action_deep_link = Column(String, nullable=True)

    fcm_sent = Column(Boolean, default=False)
    fcm_sent_at = Column(DateTime(timezone=True), nullable=True)
    fcm_message_id = Column(String, nullable=True)

    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime(timezone=True), nullable=True)
    is_dismissed = Column(Boolean, default=False)
    dismissed_at = Column(DateTime(timezone=True), nullable=True)
    was_acted_upon = Column(Boolean, nullable=True)
    acted_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), primary_key=True, server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)


class FCMDeliveryLog(Base):
    __tablename__ = "fcm_delivery_log"
    __table_args__ = (
        Index("idx_fcm_log_farmer", "farmer_id", "sent_at"),
        Index("idx_fcm_log_status", "status", postgresql_where=Column("status") != "delivered"),
        {"schema": "alerts"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alert_id = Column(UUID(as_uuid=True), nullable=False)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("core.farmers.id"), nullable=False)
    fcm_token = Column(Text, nullable=False)
    fcm_message_id = Column(String, nullable=True)
    topic = Column(String, nullable=True)
    status = Column(String(30), nullable=False)
    error_code = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    delivered_at = Column(DateTime(timezone=True), nullable=True)
