"use client";

import { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { AppShell } from '@/components/AppShell';
import { AgentTracePanel } from '@/components/AgentTracePanel';
import { FactCheckTable } from '@/components/FactCheckTable';
import { ArrowUpRight, Building2, Code2, Loader2, Play, Settings2, Sparkles } from 'lucide-react';

export default function ResearchPage() {
  const [query, setQuery] = useState('');
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [sessionStatus, setSessionStatus] = useState<string>('idle');
  const [confidenceScore, setConfidenceScore] = useState<number | null>(null);
  const [agentRuns, setAgentRuns] = useState<any[]>([]);
  const [report, setReport] = useState<string | null>(null);
  const [claims, setClaims] = useState<any[]>([]);
  const [toggles, setToggles] = useState({
    market_analysis: false,
    startup_gen: false,
    tech_arch: false,
  });

  useEffect(() => {
    if (!sessionId || sessionStatus === 'completed' || sessionStatus === 'degraded' || sessionStatus === 'failed') return;

    const interval = setInterval(async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/v1/research/sessions/${sessionId}/status`);
        if (res.ok) {
          const data = await res.json();
          setSessionStatus(data.session_status);
          setConfidenceScore(data.confidence_score);
          setAgentRuns(data.agent_runs || []);
        }
      } catch (err) {
        console.error('Polling error', err);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [sessionId, sessionStatus]);

  useEffect(() => {
    if (sessionId && (sessionStatus === 'completed' || sessionStatus === 'degraded')) {
      fetch(`http://localhost:8000/api/v1/research/sessions/${sessionId}/report`)
        .then((res) => res.json())
        .then((data) => setReport(data.content_markdown))
        .catch(console.error);

      const fcRun = agentRuns.find((item) => item.agent_role === 'fact_checker');
      if (fcRun?.raw_output?.claims) {
        setClaims(fcRun.raw_output.claims);
      }
    }
  }, [sessionId, sessionStatus, agentRuns]);

  const handleRunResearch = async () => {
    if (!query.trim()) return;
    setSessionStatus('queued');
    setSessionId(null);
    setAgentRuns([]);
    setReport(null);
    setClaims([]);
    setConfidenceScore(null);

    try {
      const res = await fetch('http://localhost:8000/api/v1/research/sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query,
          user_id: '00000000-0000-0000-0000-000000000000',
          toggles,
        }),
      });
      const data = await res.json();
      setSessionId(data.session_id);
    } catch (err) {
      console.error(err);
      setSessionStatus('failed');
    }
  };

  const getStatusColor = (status: string) => {
    if (status === 'running') return 'border-[#305b60] bg-[#142728] text-[#8cc7cb]';
    if (status === 'done') return 'border-[#2f4432] bg-[#18271a] text-[#86b77b]';
    if (status === 'failed') return 'border-[#473029] bg-[#2b1e1a] text-[#c58b7f]';
    if (status === 'degraded') return 'border-[#4a401f] bg-[#2b2617] text-[#c1b170]';
    return 'border-[#2d2925] bg-[#1b1816] text-[#a79d90]';
  };

  const AGENT_ORDER = [
    'memory',
    'planner',
    'researcher',
    'fact_checker',
    'critic',
    'business_analyst',
    'startup_generator',
    'technical_architect',
    'data_analyst',
    'knowledge_graph',
    'evaluator',
    'report_writer',
  ];

  return (
    <AppShell activeItem="search" title="Deep research" subtitle="Multi-agent analysis with source-forward answers">
      <div className="mx-auto flex max-w-5xl flex-col gap-6">
        <div className="rounded-[28px] border border-[#322d29] bg-[#191715] p-5 shadow-[0_10px_40px_rgba(0,0,0,0.18)]">
          <div className="mb-4 flex items-center gap-2 text-[12px] uppercase tracking-[0.25em] text-[#7f766e]">
            <Sparkles className="h-3.5 w-3.5 text-[#5d9ea4]" />
            Ask a research question
          </div>
          <textarea
            className="min-h-[120px] w-full rounded-[22px] border border-[#342f2a] bg-[#171615] p-4 text-[15px] leading-7 text-[#f3eadf] outline-none transition focus:border-[#5d9ea4] focus:shadow-[0_0_0_2px_rgba(93,158,164,0.2)]"
            placeholder="What would you like to research today?"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={!['idle', 'completed', 'failed', 'degraded'].includes(sessionStatus)}
          />

          <div className="mt-4 flex flex-wrap gap-3">
            {[
              { key: 'market_analysis', label: 'Market analysis', icon: Building2 },
              { key: 'startup_gen', label: 'Startup generator', icon: Sparkles },
              { key: 'tech_arch', label: 'Technical architecture', icon: Code2 },
            ].map(({ key, label, icon: Icon }) => (
              <label key={key} className="flex items-center gap-2 rounded-full border border-[#342f2a] bg-[#181614] px-3 py-2 text-[13px] text-[#bdb1a4]">
                <input
                  type="checkbox"
                  checked={toggles[key as keyof typeof toggles]}
                  onChange={(e) => setToggles((prev) => ({ ...prev, [key]: e.target.checked }))}
                  className="h-4 w-4 rounded border-[#3d352f] bg-transparent text-[#5d9ea4]"
                />
                <Icon className="h-3.5 w-3.5" />
                {label}
              </label>
            ))}
          </div>

          <div className="mt-5 flex items-center justify-between gap-3">
            <div className="text-[13px] text-[#8f857c]">Grounded answers and source-forward synthesis</div>
            <button
              onClick={handleRunResearch}
              disabled={!['idle', 'completed', 'failed', 'degraded'].includes(sessionStatus)}
              className="flex items-center gap-2 rounded-full bg-[#5d9ea4] px-4 py-2 text-[13px] font-medium text-[#0f1110] transition-colors hover:bg-[#6ca7ab] disabled:cursor-not-allowed disabled:bg-[#2d2824] disabled:text-[#6c635a]"
            >
              {!['idle', 'completed', 'failed', 'degraded'].includes(sessionStatus) ? (
                <><Loader2 className="h-4 w-4 animate-spin" /> Processing...</>
              ) : (
                <><Play className="h-4 w-4" /> Run research</>
              )}
            </button>
          </div>
        </div>

        {sessionId ? (
          <section className="rounded-[24px] border border-[#322d29] bg-[#191715] p-5 shadow-[0_10px_30px_rgba(0,0,0,0.12)]">
            <div className="mb-4 flex items-center justify-between gap-3">
              <div className="flex items-center gap-2 text-[12px] uppercase tracking-[0.25em] text-[#7f766e]">
                <Settings2 className="h-3.5 w-3.5 text-[#5d9ea4]" />
                Research pipeline
              </div>
              <span className="rounded-full border border-[#2d2925] bg-[#141211] px-3 py-1 text-[12px] text-[#bdb1a4]">
                {sessionStatus.toUpperCase()}
              </span>
            </div>
            <div className="grid gap-3 md:grid-cols-4">
              {AGENT_ORDER.map((role) => {
                const run = agentRuns.find((item) => item.agent_role === role);
                const isOptional = ['business_analyst', 'startup_generator', 'technical_architect'].includes(role);
                const shouldShow = !isOptional || run;
                if (!shouldShow) return null;
                const status = run?.status || 'pending';
                return (
                  <div key={role} className={`rounded-[16px] border px-3 py-3 text-sm ${getStatusColor(status)}`}>
                    <div className="text-[11px] uppercase tracking-[0.25em] opacity-80">{role.replace('_', ' ')}</div>
                    <div className="mt-1 font-medium capitalize">{status}</div>
                  </div>
                );
              })}
            </div>
            <AgentTracePanel runs={agentRuns} />
          </section>
        ) : null}

        {report ? (
          <section className="rounded-[24px] border border-[#322d29] bg-[#191715] p-5 shadow-[0_10px_30px_rgba(0,0,0,0.12)]">
            <div className="mb-4 flex items-center justify-between gap-3">
              <div className="text-[12px] uppercase tracking-[0.25em] text-[#7f766e]">Answer</div>
              <div className="text-[13px] text-[#8f857c]">Confidence: {confidenceScore ? `${confidenceScore.toFixed(1)}%` : 'N/A'}</div>
            </div>
            <div className="prose prose-invert max-w-none text-[15px] leading-7 text-[#d8cdbd] prose-p:my-2 prose-strong:text-[#f3eadf]">
              <ReactMarkdown>{report}</ReactMarkdown>
            </div>
            <div className="mt-5 flex flex-wrap gap-2">
              {['Sources', 'Citations', 'Follow-up'].map((item) => (
                <button key={item} type="button" className="rounded-full border border-[#342f2a] px-3 py-1.5 text-[12px] text-[#bdb1a4] transition-colors hover:border-[#5d9ea4] hover:text-[#f3eadf]">
                  {item}
                </button>
              ))}
            </div>
          </section>
        ) : null}

        {claims.length > 0 ? (
          <section className="rounded-[24px] border border-[#322d29] bg-[#191715] p-5 shadow-[0_10px_30px_rgba(0,0,0,0.12)]">
            <div className="mb-3 flex items-center justify-between gap-3">
              <div className="text-[12px] uppercase tracking-[0.25em] text-[#7f766e]">Citations</div>
              <button type="button" className="flex items-center gap-2 text-[13px] text-[#5d9ea4]">
                Open sources <ArrowUpRight className="h-3.5 w-3.5" />
              </button>
            </div>
            <FactCheckTable claims={claims} />
          </section>
        ) : null}
      </div>
    </AppShell>
  );
}
