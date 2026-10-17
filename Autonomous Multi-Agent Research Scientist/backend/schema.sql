-- AMRS Supabase Schema initialization for Milestone 2

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. users table (assuming it might exist, but we IF NOT EXISTS it)
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    auth_provider TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'guest',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    default_mode TEXT,
    quota_research_runs_remaining INTEGER DEFAULT 5,
    quota_reset_at TIMESTAMPTZ
);

-- 2. projects (optional grouping)
CREATE TABLE IF NOT EXISTS public.projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id),
    title TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. research_sessions
CREATE TABLE IF NOT EXISTS public.research_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES public.projects(id),
    user_id UUID REFERENCES public.users(id),
    query_text TEXT NOT NULL,
    toggles JSONB DEFAULT '{}'::jsonb,
    status TEXT NOT NULL DEFAULT 'queued', -- queued, running, completed, degraded, failed
    confidence_score INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- 4. agent_runs (Agent Trace and Dashboard)
CREATE TABLE IF NOT EXISTS public.agent_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES public.research_sessions(id) ON DELETE CASCADE,
    agent_role TEXT NOT NULL, -- planner, research, report_writer, etc.
    status TEXT NOT NULL DEFAULT 'queued', -- queued, running, done, degraded, failed
    provider_used TEXT,
    fallback_used BOOLEAN DEFAULT FALSE,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    raw_output JSONB,
    error_detail TEXT
);

-- 5. sources (from Research Agent)
CREATE TABLE IF NOT EXISTS public.sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES public.research_sessions(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    source_type TEXT NOT NULL, -- arxiv
    published_date DATE,
    retrieved_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. claims (from Fact Checker Agent)
CREATE TABLE IF NOT EXISTS public.claims (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES public.research_sessions(id) ON DELETE CASCADE,
    claim_text TEXT NOT NULL,
    verification_status TEXT NOT NULL, -- verified, partially_verified, unverified, contradicted
    supporting_source_ids UUID[] DEFAULT '{}',
    conflicting_source_ids UUID[] DEFAULT '{}'
);

-- 7. critic_notes (from Critic Agent)
CREATE TABLE IF NOT EXISTS public.critic_notes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES public.research_sessions(id) ON DELETE CASCADE,
    note_type TEXT NOT NULL, -- assumption, gap, risk
    content TEXT NOT NULL,
    severity TEXT NOT NULL -- low, medium, high
);

-- 8. startup_concepts (from Startup Generator Agent)
CREATE TABLE IF NOT EXISTS public.startup_concepts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES public.research_sessions(id) ON DELETE CASCADE,
    rank INTEGER NOT NULL,
    name TEXT NOT NULL,
    target_user TEXT NOT NULL,
    monetization_model TEXT NOT NULL,
    differentiator TEXT NOT NULL
);

-- 9. reports (from Report Writer Agent)
CREATE TABLE IF NOT EXISTS public.reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES public.research_sessions(id) ON DELETE CASCADE UNIQUE,
    content_markdown TEXT NOT NULL,
    pdf_export_url TEXT,
    docx_export_url TEXT
);

-- 10. audit_logs
CREATE TABLE IF NOT EXISTS public.audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS and setup policies (simplistic for dev)
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.research_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.claims ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.critic_notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.startup_concepts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

-- Allow service role to bypass RLS (Supabase does this by default, but we can also add policies)
CREATE POLICY "Enable all for users based on user_id" ON public.users FOR ALL USING (auth.uid() = id);
CREATE POLICY "Enable all for service_role" ON public.research_sessions FOR ALL USING (true);
CREATE POLICY "Enable all for service_role" ON public.agent_runs FOR ALL USING (true);
CREATE POLICY "Enable all for service_role" ON public.sources FOR ALL USING (true);
CREATE POLICY "Enable all for service_role" ON public.reports FOR ALL USING (true);
CREATE POLICY "Enable all for service_role" ON public.claims FOR ALL USING (true);
CREATE POLICY "Enable all for service_role" ON public.critic_notes FOR ALL USING (true);
CREATE POLICY "Enable all for service_role" ON public.startup_concepts FOR ALL USING (true);
CREATE POLICY "Enable all for service_role" ON public.audit_logs FOR ALL USING (true);
