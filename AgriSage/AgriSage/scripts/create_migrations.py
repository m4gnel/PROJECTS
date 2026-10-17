import os, glob

versions_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'alembic', 'versions')
os.makedirs(versions_dir, exist_ok=True)

for f in glob.glob(os.path.join(versions_dir, '*.py')):
    os.remove(f)

migrations = {
    '001_extensions.py': '''"""001_extensions

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
    op.execute('CREATE EXTENSION IF NOT EXISTS postgis;')


def downgrade() -> None:
    op.execute('DROP EXTENSION IF EXISTS postgis;')
    op.execute('DROP EXTENSION IF EXISTS vector;')
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp";')
''',

    '002_users.py': '''"""002_users

Revision ID: 002_users
Revises: 001_extensions
Create Date: 2026-09-30 00:00:02.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '002_users'
down_revision: Union[str, None] = '001_extensions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE users (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        phone VARCHAR(15) UNIQUE NOT NULL,
        name VARCHAR(100),
        language VARCHAR(10) NOT NULL DEFAULT 'ml',
        location_lat DECIMAL(9,6), location_lon DECIMAL(9,6),
        district VARCHAR(100), state VARCHAR(100) DEFAULT 'Kerala',
        subscription_tier VARCHAR(20) NOT NULL DEFAULT 'free',
        subscription_expires TIMESTAMPTZ,
        trial_started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        advisories_this_month INT NOT NULL DEFAULT 0,
        advisories_reset_at DATE NOT NULL DEFAULT CURRENT_DATE,
        is_active BOOLEAN NOT NULL DEFAULT true,
        fcm_token VARCHAR(500),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        last_active_at TIMESTAMPTZ
    );
    """)
    op.execute("CREATE INDEX idx_users_phone ON users(phone);")

    op.execute("""
    CREATE TABLE otp_sessions (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        phone VARCHAR(15) NOT NULL,
        otp_hash VARCHAR(255) NOT NULL,
        expires_at TIMESTAMPTZ NOT NULL,
        attempts INT NOT NULL DEFAULT 0,
        used BOOLEAN NOT NULL DEFAULT false,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_otp_phone ON otp_sessions(phone);")

    op.execute("""
    CREATE TABLE refresh_tokens (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        token_hash VARCHAR(255) NOT NULL UNIQUE,
        expires_at TIMESTAMPTZ NOT NULL,
        revoked BOOLEAN NOT NULL DEFAULT false,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_refresh_tokens_user ON refresh_tokens(user_id);")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS refresh_tokens CASCADE;")
    op.execute("DROP TABLE IF EXISTS otp_sessions CASCADE;")
    op.execute("DROP TABLE IF EXISTS users CASCADE;")
''',

    '003_farms.py': '''"""003_farms

Revision ID: 003_farms
Revises: 002_users
Create Date: 2026-09-30 00:00:03.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '003_farms'
down_revision: Union[str, None] = '002_users'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE farms (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        name VARCHAR(200) NOT NULL,
        location_lat DECIMAL(9,6), location_lon DECIMAL(9,6),
        district VARCHAR(100), state VARCHAR(100),
        area_ha DECIMAL(8,2),
        is_active BOOLEAN NOT NULL DEFAULT true,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_farms_user ON farms(user_id);")

    op.execute("""
    CREATE TABLE fields (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        farm_id UUID NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
        name VARCHAR(100),
        area_ha DECIMAL(8,2), slope VARCHAR(20),
        irrigation VARCHAR(30), soil_type VARCHAR(50),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_fields_farm ON fields(farm_id);")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS fields CASCADE;")
    op.execute("DROP TABLE IF EXISTS farms CASCADE;")
''',

    '004_crop_cycles.py': '''"""004_crop_cycles

Revision ID: 004_crop_cycles
Revises: 003_farms
Create Date: 2026-09-30 00:00:04.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '004_crop_cycles'
down_revision: Union[str, None] = '003_farms'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE crop_cycles (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        field_id UUID NOT NULL REFERENCES fields(id) ON DELETE CASCADE,
        crop VARCHAR(50) NOT NULL CHECK (crop IN ('rice','banana','coconut','tomato','maize')),
        cultivar VARCHAR(100), season VARCHAR(20),
        planting_date DATE NOT NULL,
        expected_harvest DATE, actual_harvest DATE,
        status VARCHAR(20) NOT NULL DEFAULT 'active'
            CHECK (status IN ('active','harvested','abandoned')),
        notes TEXT,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_cycles_field ON crop_cycles(field_id);")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS crop_cycles CASCADE;")
''',

    '005_observations.py': '''"""005_observations

Revision ID: 005_observations
Revises: 004_crop_cycles
Create Date: 2026-09-30 00:00:05.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '005_observations'
down_revision: Union[str, None] = '004_crop_cycles'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE observations (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        crop_cycle_id UUID NOT NULL REFERENCES crop_cycles(id) ON DELETE CASCADE,
        location_lat DECIMAL(9,6), location_lon DECIMAL(9,6),
        problem_description TEXT,
        voice_note_key VARCHAR(500),
        irrigation_status VARCHAR(20),
        fertilizer_recent BOOLEAN, pesticide_recent BOOLEAN,
        observed_growth_stage VARCHAR(50),
        observed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_obs_cycle ON observations(crop_cycle_id);")

    op.execute("""
    CREATE TABLE images (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        observation_id UUID NOT NULL REFERENCES observations(id) ON DELETE CASCADE,
        r2_key VARCHAR(500) NOT NULL UNIQUE,
        mime_type VARCHAR(50) NOT NULL,
        file_size_bytes INTEGER, width_px INTEGER, height_px INTEGER,
        quality_score DECIMAL(4,2) CHECK (quality_score BETWEEN 0 AND 1),
        blur_score DECIMAL(8,2),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_images_obs ON images(observation_id);")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS images CASCADE;")
    op.execute("DROP TABLE IF EXISTS observations CASCADE;")
''',

    '006_weather.py': '''"""006_weather

Revision ID: 006_weather
Revises: 005_observations
Create Date: 2026-09-30 00:00:06.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '006_weather'
down_revision: Union[str, None] = '005_observations'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE weather_cache (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        location_key VARCHAR(20) NOT NULL UNIQUE,
        data_json JSONB NOT NULL,
        cached_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS weather_cache CASCADE;")
''',

    '007_diagnoses.py': '''"""007_diagnoses

Revision ID: 007_diagnoses
Revises: 006_weather
Create Date: 2026-09-30 00:00:07.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '007_diagnoses'
down_revision: Union[str, None] = '006_weather'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE diagnoses (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        observation_id UUID NOT NULL REFERENCES observations(id) ON DELETE CASCADE,
        pipeline_trace_id VARCHAR(100),
        started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        completed_at TIMESTAMPTZ,
        generation_ms INTEGER,
        model_version VARCHAR(50),
        status VARCHAR(20) DEFAULT 'pending'
    );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS diagnoses CASCADE;")
''',

    '008_advisories.py': '''"""008_advisories

Revision ID: 008_advisories
Revises: 007_diagnoses
Create Date: 2026-09-30 00:00:08.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '008_advisories'
down_revision: Union[str, None] = '007_diagnoses'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE advisories (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        observation_id UUID NOT NULL REFERENCES observations(id) ON DELETE CASCADE,
        confidence_state VARCHAR(30) NOT NULL
            CHECK (confidence_state IN ('CONFIRMED','LIKELY','POSSIBLE','UNCERTAIN',
                   'INSUFFICIENT_DATA','CONFLICTING_EVIDENCE','OUT_OF_SCOPE')),
        confidence_score DECIMAL(4,2),
        recommended_scenario VARCHAR(5),
        scenarios_json JSONB NOT NULL,
        evidence_bundle_json JSONB NOT NULL,
        recommended_action_json JSONB NOT NULL,
        what_would_change_json JSONB,
        safe_to_act BOOLEAN NOT NULL DEFAULT true,
        sources_json JSONB,
        scheme_matches_json JSONB,
        model_version VARCHAR(50),
        knowledge_version VARCHAR(50),
        generation_ms INTEGER,
        farmer_feedback VARCHAR(20),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_adv_obs ON advisories(observation_id);")
    op.execute("CREATE INDEX idx_adv_created ON advisories(created_at DESC);")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS advisories CASCADE;")
''',

    '009_interventions.py': '''"""009_interventions

Revision ID: 009_interventions
Revises: 008_advisories
Create Date: 2026-09-30 00:00:09.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '009_interventions'
down_revision: Union[str, None] = '008_advisories'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE interventions (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        crop_cycle_id UUID NOT NULL REFERENCES crop_cycles(id),
        advisory_id UUID REFERENCES advisories(id),
        intervention_type VARCHAR(50) NOT NULL,
        product_name VARCHAR(200), dosage VARCHAR(100),
        cost_inr DECIMAL(10,2), applied_at DATE,
        notes TEXT,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)

    op.execute("""
    CREATE TABLE outcomes (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        intervention_id UUID NOT NULL REFERENCES interventions(id),
        observed_at DATE NOT NULL,
        effectiveness VARCHAR(20),
        yield_actual_kgha DECIMAL(10,2),
        notes TEXT,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS outcomes CASCADE;")
    op.execute("DROP TABLE IF EXISTS interventions CASCADE;")
''',

    '010_simulation.py': '''"""010_simulation

Revision ID: 010_simulation
Revises: 009_interventions
Create Date: 2026-09-30 00:00:10.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '010_simulation'
down_revision: Union[str, None] = '009_interventions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE simulation_results (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        advisory_id UUID NOT NULL REFERENCES advisories(id),
        engine VARCHAR(20) DEFAULT 'dssat',
        scenario_id VARCHAR(5),
        params_json JSONB, results_json JSONB,
        yield_kgha DECIMAL(10,2), net_return_inr DECIMAL(12,2),
        is_modelled_estimate BOOLEAN NOT NULL DEFAULT true,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS simulation_results CASCADE;")
''',

    '011_knowledge.py': '''"""011_knowledge

Revision ID: 011_knowledge
Revises: 010_simulation
Create Date: 2026-09-30 00:00:11.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '011_knowledge'
down_revision: Union[str, None] = '010_simulation'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE knowledge_documents (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        title VARCHAR(500), crop VARCHAR(50), state VARCHAR(100),
        topic VARCHAR(100), growth_stage VARCHAR(50),
        source_tier INTEGER NOT NULL CHECK (source_tier BETWEEN 1 AND 6),
        source_authority VARCHAR(200), source_url VARCHAR(1000),
        language VARCHAR(10) NOT NULL DEFAULT 'en',
        published_at DATE, valid_until DATE NOT NULL,
        status VARCHAR(20) NOT NULL DEFAULT 'PUBLISHED'
            CHECK (status IN ('DISCOVERED','PARSED','VALIDATED','APPROVED',
                   'PUBLISHED','SUPERSEDED','ARCHIVED')),
        content_hash CHAR(64), version INTEGER NOT NULL DEFAULT 1,
        license VARCHAR(100),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)

    op.execute("""
    CREATE TABLE knowledge_chunks (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        document_id UUID NOT NULL REFERENCES knowledge_documents(id) ON DELETE CASCADE,
        chunk_index INTEGER NOT NULL,
        content TEXT NOT NULL,
        embedding vector(1024),
        metadata JSONB,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        UNIQUE(document_id, chunk_index)
    );
    """)

    op.execute("""
    CREATE INDEX idx_chunks_embedding ON knowledge_chunks
        USING hnsw (embedding vector_cosine_ops)
        WITH (m=16, ef_construction=64);
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS knowledge_chunks CASCADE;")
    op.execute("DROP TABLE IF EXISTS knowledge_documents CASCADE;")
''',

    '012_schemes.py': '''"""012_schemes

Revision ID: 012_schemes
Revises: 011_knowledge
Create Date: 2026-09-30 00:00:12.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '012_schemes'
down_revision: Union[str, None] = '011_knowledge'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE schemes (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        name VARCHAR(300) NOT NULL, short_name VARCHAR(50),
        authority VARCHAR(200), authority_level VARCHAR(20),
        state VARCHAR(100), crops_applicable JSONB,
        eligibility_rules JSONB NOT NULL, benefits_json JSONB,
        enrollment_url VARCHAR(500), helpline VARCHAR(50),
        valid_from DATE, valid_until DATE NOT NULL,
        status VARCHAR(20) NOT NULL DEFAULT 'active',
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS schemes CASCADE;")
''',

    '013_market.py': '''"""013_market

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
''',

    '014_notifications.py': '''"""014_notifications

Revision ID: 014_notifications
Revises: 013_market
Create Date: 2026-09-30 00:00:14.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '014_notifications'
down_revision: Union[str, None] = '013_market'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE notifications (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        type VARCHAR(50) NOT NULL,
        title VARCHAR(300), body TEXT,
        data_json JSONB, is_read BOOLEAN DEFAULT false,
        sent_at TIMESTAMPTZ, read_at TIMESTAMPTZ,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_notif_user ON notifications(user_id, created_at DESC);")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS notifications CASCADE;")
''',

    '015_expert.py': '''"""015_expert

Revision ID: 015_expert
Revises: 014_notifications
Create Date: 2026-09-30 00:00:15.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '015_expert'
down_revision: Union[str, None] = '014_notifications'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE expert_reviews (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        advisory_id UUID NOT NULL REFERENCES advisories(id),
        expert_id UUID NOT NULL REFERENCES users(id),
        verdict VARCHAR(20) CHECK (verdict IN ('correct','partially_correct','incorrect','insufficient_data')),
        notes TEXT, corrected_diagnosis VARCHAR(100),
        reviewed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS expert_reviews CASCADE;")
''',

    '016_audit.py': '''"""016_audit

Revision ID: 016_audit
Revises: 015_expert
Create Date: 2026-09-30 00:00:16.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '016_audit'
down_revision: Union[str, None] = '015_expert'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE audit_logs (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        user_id UUID REFERENCES users(id),
        event_type VARCHAR(100) NOT NULL,
        event_data JSONB,
        ip_address INET,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_audit_type_date ON audit_logs(event_type, created_at DESC);")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS audit_logs CASCADE;")
''',

    '017_rls.py': '''"""017_rls

Revision ID: 017_rls
Revises: 016_audit
Create Date: 2026-09-30 00:00:17.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '017_rls'
down_revision: Union[str, None] = '016_audit'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE farms ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE fields ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE crop_cycles ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE observations ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE images ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE advisories ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;")

    op.execute("""
    CREATE POLICY farms_owner ON farms
        USING (user_id = NULLIF(current_setting('app.current_user_id', true), '')::UUID);
    """)
    op.execute("""
    CREATE POLICY fields_owner ON fields
        USING (farm_id IN (SELECT id FROM farms WHERE user_id = NULLIF(current_setting('app.current_user_id', true), '')::UUID));
    """)
    op.execute("""
    CREATE POLICY cycles_owner ON crop_cycles
        USING (field_id IN (SELECT f.id FROM fields f JOIN farms fa ON f.farm_id=fa.id WHERE fa.user_id = NULLIF(current_setting('app.current_user_id', true), '')::UUID));
    """)
    op.execute("""
    CREATE POLICY obs_owner ON observations
        USING (crop_cycle_id IN (SELECT cc.id FROM crop_cycles cc JOIN fields f ON cc.field_id=f.id JOIN farms fa ON f.farm_id=fa.id WHERE fa.user_id = NULLIF(current_setting('app.current_user_id', true), '')::UUID));
    """)
    op.execute("""
    CREATE POLICY adv_owner ON advisories
        USING (observation_id IN (SELECT o.id FROM observations o JOIN crop_cycles cc ON o.crop_cycle_id=cc.id JOIN fields f ON cc.field_id=f.id JOIN farms fa ON f.farm_id=fa.id WHERE fa.user_id = NULLIF(current_setting('app.current_user_id', true), '')::UUID));
    """)
    op.execute("""
    CREATE POLICY notif_owner ON notifications
        USING (user_id = NULLIF(current_setting('app.current_user_id', true), '')::UUID);
    """)


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS notif_owner ON notifications;")
    op.execute("DROP POLICY IF EXISTS adv_owner ON advisories;")
    op.execute("DROP POLICY IF EXISTS obs_owner ON observations;")
    op.execute("DROP POLICY IF EXISTS cycles_owner ON crop_cycles;")
    op.execute("DROP POLICY IF EXISTS fields_owner ON fields;")
    op.execute("DROP POLICY IF EXISTS farms_owner ON farms;")
    op.execute("ALTER TABLE notifications DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE advisories DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE images DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE observations DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE crop_cycles DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE fields DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE farms DISABLE ROW LEVEL SECURITY;")
'''
}

if __name__ == '__main__':
    for filename, content in migrations.items():
        file_path = os.path.join(versions_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as fh:
            fh.write(content.strip() + '\n')
        print(f'Wrote migration {filename}')
    print('All 17 migration files created successfully.')
