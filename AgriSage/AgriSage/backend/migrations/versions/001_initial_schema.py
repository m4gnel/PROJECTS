"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2026-10-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Enable pgvector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # === FARMERS TABLE ===
    op.create_table(
        'farmers',
        sa.Column('id', sa.String(36), primary_key=True, server_default=sa.text('uuid_generate_v4()::text')),
        sa.Column('phone', sa.String(15), unique=True, nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('village', sa.String(100), nullable=True),
        sa.Column('district', sa.String(50), nullable=True),
        sa.Column('state', sa.String(50), nullable=False, server_default='Kerala'),
        sa.Column('preferred_language', sa.String(5), nullable=False, server_default='ml'),
        sa.Column('latitude', sa.Float, nullable=True),
        sa.Column('longitude', sa.Float, nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='true'),
        sa.Column('fcm_token', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), onupdate=sa.text('NOW()')),
    )

    # === FIELDS TABLE ===
    op.create_table(
        'fields',
        sa.Column('id', sa.String(36), primary_key=True, server_default=sa.text('uuid_generate_v4()::text')),
        sa.Column('farmer_id', sa.String(36), sa.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('area_sq_m', sa.Float, nullable=False),
        sa.Column('latitude', sa.Float, nullable=False),
        sa.Column('longitude', sa.Float, nullable=False),
        sa.Column('soil_type', sa.String(50), nullable=True),
        sa.Column('irrigation_type', sa.String(50), nullable=True),  # "drip", "sprinkler", "flood", "rainfed"
        sa.Column('last_ndvi', sa.Float, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
    )

    # === CROP_RECORDS TABLE ===
    op.create_table(
        'crop_records',
        sa.Column('id', sa.String(36), primary_key=True, server_default=sa.text('uuid_generate_v4()::text')),
        sa.Column('field_id', sa.String(36), sa.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False),
        sa.Column('crop_name', sa.String(50), nullable=False),     # "rice", "coconut", "banana", "pepper"
        sa.Column('variety', sa.String(100), nullable=True),
        sa.Column('sowing_date', sa.Date, nullable=False),
        sa.Column('expected_harvest_date', sa.Date, nullable=True),
        sa.Column('actual_harvest_date', sa.Date, nullable=True),
        sa.Column('growth_stage', sa.String(50), nullable=True),   # "germination", "vegetative", "flowering", "ripening"
        sa.Column('yield_kg_ha', sa.Float, nullable=True),
        sa.Column('is_active', sa.Boolean, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
    )

    # === WEATHER_CACHE TABLE ===
    op.create_table(
        'weather_cache',
        sa.Column('id', sa.String(36), primary_key=True, server_default=sa.text('uuid_generate_v4()::text')),
        sa.Column('lat', sa.Float, nullable=False),
        sa.Column('lon', sa.Float, nullable=False),
        sa.Column('temperature_c', sa.Float, nullable=False),
        sa.Column('humidity_percent', sa.Integer, nullable=False),
        sa.Column('rainfall_mm', sa.Float, nullable=False, server_default='0'),
        sa.Column('wind_kmh', sa.Float, nullable=False),
        sa.Column('uv_index', sa.Float, nullable=True),
        sa.Column('weather_condition', sa.String(50), nullable=False),
        sa.Column('forecast_json', sa.Text, nullable=True),    # JSON string of 7-day forecast
        sa.Column('source', sa.String(20), nullable=False, server_default='open-meteo'),
        sa.Column('fetched_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
    )

    # === ALERTS TABLE ===
    op.create_table(
        'alerts',
        sa.Column('id', sa.String(36), primary_key=True, server_default=sa.text('uuid_generate_v4()::text')),
        sa.Column('farmer_id', sa.String(36), sa.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False),
        sa.Column('field_id', sa.String(36), sa.ForeignKey('fields.id', ondelete='SET NULL'), nullable=True),
        sa.Column('severity', sa.String(10), nullable=False),  # "CRITICAL", "WARNING", "INFO", "SUCCESS"
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('message', sa.Text, nullable=False),
        sa.Column('source_agent', sa.String(50), nullable=True),  # which agent generated this
        sa.Column('is_read', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
    )

    # === CHAT_SESSIONS TABLE ===
    op.create_table(
        'chat_sessions',
        sa.Column('id', sa.String(36), primary_key=True, server_default=sa.text('uuid_generate_v4()::text')),
        sa.Column('farmer_id', sa.String(36), sa.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False),
        sa.Column('language', sa.String(5), nullable=False, server_default='ml'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
    )

    # === CHAT_MESSAGES TABLE ===
    op.create_table(
        'chat_messages',
        sa.Column('id', sa.String(36), primary_key=True, server_default=sa.text('uuid_generate_v4()::text')),
        sa.Column('session_id', sa.String(36), sa.ForeignKey('chat_sessions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('is_from_user', sa.Boolean, nullable=False),
        sa.Column('confidence_score', sa.Float, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
    )

    # === KNOWLEDGE_CHUNKS TABLE (pgvector RAG) ===
    op.create_table(
        'knowledge_chunks',
        sa.Column('id', sa.String(36), primary_key=True, server_default=sa.text('uuid_generate_v4()::text')),
        sa.Column('source_file', sa.String(255), nullable=False),   # filename of KAU PDF
        sa.Column('chunk_index', sa.Integer, nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('crop_tags', sa.ARRAY(sa.String), nullable=True),  # ["rice", "coconut"]
        sa.Column('embedding', Vector(1024), nullable=True),         # multilingual-e5-large = 1024 dims
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
    )

    # === MARKET_PRICES TABLE ===
    op.create_table(
        'market_prices',
        sa.Column('id', sa.String(36), primary_key=True, server_default=sa.text('uuid_generate_v4()::text')),
        sa.Column('commodity', sa.String(100), nullable=False),
        sa.Column('market_name', sa.String(100), nullable=False),
        sa.Column('district', sa.String(50), nullable=False),
        sa.Column('min_price', sa.Float, nullable=False),
        sa.Column('max_price', sa.Float, nullable=False),
        sa.Column('modal_price', sa.Float, nullable=False),
        sa.Column('price_date', sa.Date, nullable=False),
        sa.Column('fetched_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
    )

    # === INDEXES ===
    op.create_index('idx_fields_farmer_id', 'fields', ['farmer_id'])
    op.create_index('idx_crop_records_field_id', 'crop_records', ['field_id'])
    op.create_index('idx_alerts_farmer_id', 'alerts', ['farmer_id'])
    op.create_index('idx_alerts_unread', 'alerts', ['farmer_id', 'is_read'])
    op.create_index('idx_chat_sessions_farmer_id', 'chat_sessions', ['farmer_id'])
    op.create_index('idx_chat_messages_session_id', 'chat_messages', ['session_id'])
    op.create_index('idx_market_prices_commodity', 'market_prices', ['commodity', 'price_date'])
    op.create_index('idx_weather_cache_location', 'weather_cache', ['lat', 'lon'])
    
    # HNSW index for pgvector (fast approximate nearest neighbor)
    op.execute("""
        CREATE INDEX idx_knowledge_embedding 
        ON knowledge_chunks 
        USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64)
    """)

def downgrade() -> None:
    op.drop_table('market_prices')
    op.drop_table('knowledge_chunks')
    op.drop_table('chat_messages')
    op.drop_table('chat_sessions')
    op.drop_table('alerts')
    op.drop_table('weather_cache')
    op.drop_table('crop_records')
    op.drop_table('fields')
    op.drop_table('farmers')
    op.execute('DROP EXTENSION IF EXISTS vector')
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp"')
