import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Column, String, Boolean, Integer, Float, DateTime, LargeBinary,
    ForeignKey, CheckConstraint, Index, UniqueConstraint, func, ARRAY, Text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

try:
    from pgvector.sqlalchemy import Vector
except ImportError:
    # Safe fallback if pgvector package is missing in local test runner environment
    from sqlalchemy.types import UserDefinedType
    class Vector(UserDefinedType):
        def __init__(self, dim=1024):
            self.dim = dim
        def get_col_spec(self, **kw):
            return f"vector({self.dim})"

from backend.database import Base


class AdvisorySession(Base):
    __tablename__ = "advisory_sessions"
    __table_args__ = (
        Index("idx_sessions_farmer", "farmer_id", "started_at"),
        Index("idx_sessions_active", "farmer_id", postgresql_where=Column("is_active") == True),
        Index("idx_sessions_token", "session_token"),
        {"schema": "agents"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("core.farmers.id", ondelete="CASCADE"), nullable=False)
    session_token = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    language = Column(String(10), nullable=False, default="hi")
    state = Column(String, nullable=False)
    district = Column(String, nullable=False)
    primary_crop = Column(String, nullable=True)
    active_field_id = Column(UUID(as_uuid=True), ForeignKey("core.fields.id"), nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)
    message_count = Column(Integer, nullable=False, default=0)
    total_tokens_used = Column(Integer, default=0)
    total_cost_usd = Column(Float, default=0)

    avg_response_ms = Column(Float, nullable=True)
    farmer_satisfaction = Column(Integer, nullable=True)

    started_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_message_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    messages = relationship("AdvisoryMessage", back_populates="session", cascade="all, delete-orphan")
    invocations = relationship("AgentInvocation", back_populates="session", cascade="all, delete-orphan")


class AdvisoryMessage(Base):
    __tablename__ = "advisory_messages"
    __table_args__ = (
        Index("idx_messages_session", "session_id", "sequence_no"),
        Index("idx_messages_farmer", "farmer_id", "created_at"),
        Index("idx_messages_role", "role", "created_at"),
        {"schema": "agents"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("agents.advisory_sessions.id", ondelete="CASCADE"), nullable=False)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("core.farmers.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), nullable=False)
    sequence_no = Column(Integer, nullable=False)

    content_native = Column(Text, nullable=False)
    content_en = Column(Text, nullable=True)
    language = Column(String(10), nullable=False)

    agents_used = Column(ARRAY(Text), default=[])
    intent_detected = Column(ARRAY(Text), default=[])
    confidence_score = Column(Float, nullable=True)
    response_ms = Column(Integer, nullable=True)
    model_used = Column(String, default="gemini-1.5-flash")
    tokens_in = Column(Integer, nullable=True)
    tokens_out = Column(Integer, nullable=True)

    used_weather_data = Column(Boolean, default=False)
    used_soil_data = Column(Boolean, default=False)
    used_pest_data = Column(Boolean, default=False)
    used_market_data = Column(Boolean, default=False)
    used_rag_docs = Column(Boolean, default=False)
    used_dssat = Column(Boolean, default=False)
    used_ndvi = Column(Boolean, default=False)

    was_helpful = Column(Boolean, nullable=True)
    was_acted_upon = Column(Boolean, nullable=True)

    created_at = Column(DateTime(timezone=True), primary_key=True, server_default=func.now())

    session = relationship("AdvisorySession", back_populates="messages")


class AgentInvocation(Base):
    __tablename__ = "agent_invocations"
    __table_args__ = (
        Index("idx_invocations_session", "session_id"),
        Index("idx_invocations_agent", "agent_name", "started_at"),
        Index("idx_invocations_errors", "agent_name", postgresql_where=Column("succeeded") == False),
        Index("idx_invocations_slow", "duration_ms", postgresql_where=Column("duration_ms") > 3000),
        {"schema": "agents"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = Column(UUID(as_uuid=True), nullable=False)
    session_id = Column(UUID(as_uuid=True), ForeignKey("agents.advisory_sessions.id"), nullable=False)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("core.farmers.id"), nullable=False)
    agent_name = Column(String, nullable=False)

    started_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration_ms = Column(Integer, nullable=True)

    succeeded = Column(Boolean, nullable=False, default=True)
    error_type = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    input_summary = Column(JSONB, nullable=True)
    output_summary = Column(JSONB, nullable=True)
    gemini_calls = Column(Integer, default=0)
    gemini_tokens = Column(Integer, default=0)
    cache_hit = Column(Boolean, default=False)

    session = relationship("AdvisorySession", back_populates="invocations")


class KauDocument(Base):
    __tablename__ = "kau_documents"
    __table_args__ = (
        UniqueConstraint("source_file", "chunk_index"),
        Index("idx_kau_crop", "crop_name"),
        Index("idx_kau_org", "source_org"),
        Index("idx_kau_state", "state_relevance", postgresql_using="gin"),
        Index("idx_kau_stage", "crop_stage_relevance", postgresql_using="gin"),
        Index("idx_kau_type", "doc_type"),
        {"schema": "agents"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_file = Column(Text, nullable=False)
    source_org = Column(Text, nullable=False, default="KAU")
    crop_name = Column(Text, nullable=False)
    state_relevance = Column(ARRAY(Text), default=[])
    chunk_index = Column(Integer, nullable=False)
    total_chunks = Column(Integer, nullable=True)
    content = Column(Text, nullable=False)
    content_length = Column(Integer, nullable=True)

    embedding = Column(Vector(1024), nullable=False)

    doc_type = Column(String(50), nullable=True)
    crop_stage_relevance = Column(ARRAY(Text), default=[])
    season_relevance = Column(ARRAY(Text), default=[])

    ingested_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_retrieved_at = Column(DateTime(timezone=True), nullable=True)
    retrieval_count = Column(Integer, default=0)
    avg_similarity_score = Column(Float, nullable=True)


class LangGraphCheckpoint(Base):
    __tablename__ = "langgraph_checkpoints"
    __table_args__ = (
        Index("idx_lg_checkpoints_thread", "thread_id", "created_at"),
        {"schema": "agents"}
    )

    thread_id = Column(Text, primary_key=True)
    checkpoint_ns = Column(Text, primary_key=True, default="")
    checkpoint_id = Column(Text, primary_key=True)

    checkpoint = Column(JSONB, nullable=False)
    metadata_ = Column("metadata", JSONB, nullable=False, default={})
    parent_checkpoint_id = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class LangGraphCheckpointWrite(Base):
    __tablename__ = "langgraph_checkpoint_writes"
    __table_args__ = (
        Index("idx_lg_writes_thread", "thread_id", "checkpoint_id"),
        {"schema": "agents"}
    )

    thread_id = Column(Text, primary_key=True)
    checkpoint_ns = Column(Text, primary_key=True, default="")
    checkpoint_id = Column(Text, primary_key=True)
    task_id = Column(Text, primary_key=True)
    idx = Column(Integer, primary_key=True)

    channel = Column(Text, nullable=False)
    type = Column(Text, nullable=True)
    blob = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
