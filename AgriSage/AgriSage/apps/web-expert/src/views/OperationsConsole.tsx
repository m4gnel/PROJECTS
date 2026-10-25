import { useEffect, useMemo, useRef, useState } from 'react';
import type { RefObject } from 'react';
import type { LucideIcon } from 'lucide-react';
import {
  Activity,
  AlertTriangle,
  ArrowUpRight,
  ChevronRight,
  CircleAlert,
  ClipboardCheck,
  CloudOff,
  Database,
  ExternalLink,
  Eye,
  Inbox,
  Info,
  LayoutDashboard,
  LogOut,
  Map as MapIcon,
  MapPin,
  Menu,
  Moon,
  RefreshCw,
  Search,
  ServerCog,
  ShieldCheck,
  Sparkles,
  Sun,
  Users,
  X,
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { REGIONAL_OUTBREAKS } from '../data/seedData';
import { getRoleLabel } from '../auth/session';
import type { DiagnosticAdvisory, OutbreakAlert, RiskLevel } from '../types';
import type { PortalRole } from '../auth/session';
import { ApiError, fetchOperationsSnapshot, refreshAccessToken } from '../api/client';
import type { AuthResponse, OperationsQueueItem, OperationsSnapshot } from '../api/client';
import '../styles/operations.css';

type Theme = 'dark' | 'light';
type TriageFilter = 'ALL' | 'NEEDS_REVIEW' | 'ESCALATED' | 'RESOLVED';
type SnapshotStatus = 'ready' | 'loading' | 'empty' | 'error';
type PillTone =
  | 'critical'
  | 'high'
  | 'medium'
  | 'low'
  | 'pending'
  | 'escalated'
  | 'approved'
  | 'demo'
  | 'offline'
  | 'attention'
  | 'neutral';

interface OperationsConsoleProps {
  advisories?: DiagnosticAdvisory[];
  outbreaks?: OutbreakAlert[];
  theme: Theme;
  onToggleTheme: () => void;
  operatorName?: string;
  operatorRole?: PortalRole;
  accessToken?: string;
  refreshToken?: string;
  onSessionRefresh?: (response: AuthResponse) => void;
  onSignOut?: () => void;
}

interface NavItem {
  label: string;
  target: string;
  icon: LucideIcon;
  current?: boolean;
}

const NAV_ITEMS: NavItem[] = [
  { label: 'Overview', target: '#overview', icon: LayoutDashboard, current: true },
  { label: 'Triage queue', target: '#triage', icon: ClipboardCheck },
  { label: 'Regional risk', target: '#regional-risk', icon: MapIcon },
  { label: 'Service health', target: '#service-health', icon: Activity },
];

const FILTER_OPTIONS: Array<{ value: TriageFilter; label: string }> = [
  { value: 'ALL', label: 'All cases' },
  { value: 'NEEDS_REVIEW', label: 'Needs review' },
  { value: 'ESCALATED', label: 'Escalated' },
  { value: 'RESOLVED', label: 'Resolved' },
];

const RISK_ORDER: Record<RiskLevel, number> = {
  CRITICAL: 0,
  HIGH: 1,
  MEDIUM: 2,
  LOW: 3,
};

const formatNumber = (value: number) => new Intl.NumberFormat('en-IN').format(value);

const formatSnapshotDate = (value?: string) => {
  if (!value) return 'Not available';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return 'Not available';

  return new Intl.DateTimeFormat('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'Asia/Kolkata',
  }).format(date);
};

const getInitials = (name: string) =>
  name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() ?? '')
    .join('');

const getStatusLabel = (status: DiagnosticAdvisory['triageStatus']) => {
  switch (status) {
    case 'PENDING_REVIEW':
      return 'Pending review';
    case 'ESCALATED':
      return 'Escalated';
    case 'VERIFIED_APPROVED':
      return 'Approved';
    case 'OVERRIDDEN':
      return 'Overridden';
    default:
      return 'Needs review';
  }
};

const getStatusTone = (status: DiagnosticAdvisory['triageStatus']): PillTone => {
  switch (status) {
    case 'ESCALATED':
      return 'escalated';
    case 'VERIFIED_APPROVED':
      return 'approved';
    case 'OVERRIDDEN':
      return 'attention';
    default:
      return 'pending';
  }
};

const isResolved = (status: DiagnosticAdvisory['triageStatus']) =>
  status === 'VERIFIED_APPROVED' || status === 'OVERRIDDEN';

function StatusPill({ tone, label }: { tone: PillTone; label: string }) {
  return <span className={`operations-pill operations-pill--${tone}`}>{label}</span>;
}

function OperationsSidebar({ isOpen, onClose, live }: { isOpen: boolean; onClose: () => void; live: boolean }) {
  return (
    <>
      {isOpen && (
        <button
          type="button"
          className="operations-sidebar-backdrop"
          aria-label="Close operations navigation"
          onClick={onClose}
        />
      )}

      <aside className={`operations-sidebar${isOpen ? ' operations-sidebar--open' : ''}`}>
        <div className="operations-sidebar-brand">
          <div className="operations-brand-mark" aria-hidden="true">
            <Sparkles size={18} />
          </div>
          <div>
            <strong>Agri-SAGE</strong>
            <span>Operations desk</span>
          </div>
          <button
            type="button"
            className="operations-icon-button operations-sidebar-close"
            onClick={onClose}
            aria-label="Close operations navigation"
          >
            <X size={18} aria-hidden="true" />
          </button>
        </div>

        <div className="operations-team-context">
          <div className="operations-team-avatar" aria-hidden="true">
            <Users size={17} />
          </div>
          <div>
            <span className="operations-context-label">Team context</span>
            <strong>India field operations</strong>
             <span>{live ? 'Protected staff API' : 'Duty officer · seed demo'}</span>
          </div>
        </div>

        <nav className="operations-nav" aria-label="Operations navigation">
          <span className="operations-nav-label">Workspace</span>
          {NAV_ITEMS.map(({ label, target, icon: Icon, current }) => (
            <a
              key={target}
              href={target}
              className={`operations-nav-link${current ? ' operations-nav-link--active' : ''}`}
              aria-current={current ? 'page' : undefined}
              onClick={onClose}
            >
              <Icon size={18} aria-hidden="true" />
              <span>{label}</span>
              {current && <span className="operations-nav-indicator" aria-hidden="true" />}
            </a>
          ))}
        </nav>

        <div className="operations-sidebar-footer">
          <div className="operations-sidebar-note">
            <Database size={16} aria-hidden="true" />
            <div>
               <strong>{live ? 'API snapshot' : 'Seed snapshot'}</strong>
               <span>{live ? 'Authenticated read-only' : 'Read-only preview'}</span>
            </div>
          </div>
          <Link to="/" className="operations-nav-link operations-nav-link--quiet" onClick={onClose}>
            <ExternalLink size={17} aria-hidden="true" />
            <span>Public experience</span>
          </Link>
        </div>
      </aside>
    </>
  );
}

function OperationsTopbar({
  theme,
  onToggleTheme,
  onOpenMenu,
  onOpenCommand,
  commandTriggerRef,
  operatorName,
  operatorRole,
  onSignOut,
  live,
}: {
  theme: Theme;
  onToggleTheme: () => void;
  onOpenMenu: () => void;
  onOpenCommand: () => void;
  commandTriggerRef: RefObject<HTMLButtonElement | null>;
  operatorName?: string;
  operatorRole?: PortalRole;
  onSignOut?: () => void;
  live: boolean;
}) {
  return (
    <header className="operations-topbar">
      <div className="operations-topbar-left">
        <button
          type="button"
          className="operations-icon-button operations-menu-button"
          onClick={onOpenMenu}
          aria-label="Open operations navigation"
        >
          <Menu size={20} aria-hidden="true" />
        </button>
        <div className="operations-breadcrumbs" aria-label="Breadcrumb">
          <span>Internal workspace</span>
          <ChevronRight size={14} aria-hidden="true" />
          <strong>Operations overview</strong>
        </div>
      </div>

      <div className="operations-topbar-actions">
        <button
          ref={commandTriggerRef}
          type="button"
          className="operations-command-trigger"
          onClick={onOpenCommand}
          aria-haspopup="dialog"
          aria-label="Open command search"
        >
          <Search size={17} aria-hidden="true" />
          <span>Search cases, districts, commands</span>
          <kbd>Ctrl K</kbd>
        </button>
        <button
          type="button"
          className="operations-icon-button"
          onClick={onToggleTheme}
          aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}
          title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}
        >
          {theme === 'dark' ? <Sun size={18} aria-hidden="true" /> : <Moon size={18} aria-hidden="true" />}
        </button>
        <div className="operations-user-context">
          <div className="operations-user-avatar" aria-hidden="true">DO</div>
          <div>
            <strong>{operatorName || 'Duty officer'}</strong>
             <span>{operatorRole ? `${getRoleLabel(operatorRole)} · ${live ? 'live' : 'demo'}` : 'Staff preview'}</span>
          </div>
        </div>
        {onSignOut && (
          <button type="button" className="operations-signout-button" onClick={onSignOut}>
            <LogOut size={16} aria-hidden="true" />
            <span>Sign out</span>
          </button>
        )}
      </div>
    </header>
  );
}

function CommandDialog({
  isOpen,
  onClose,
  onSelect,
}: {
  isOpen: boolean;
  onClose: () => void;
  onSelect: (target: string) => void;
}) {
  const [query, setQuery] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const commands = [
    { label: 'Jump to triage queue', description: 'Review pending and escalated advisory cases', target: 'triage' },
    { label: 'Open regional risk', description: 'See district coverage and affected farms', target: 'regional-risk' },
    { label: 'Check service health', description: 'Review local snapshot and sync indicators', target: 'service-health' },
    { label: 'Open expert review queue', description: 'Use the existing expert review workflow', target: 'expert-queue' },
  ];

  const results = commands.filter((command) =>
    `${command.label} ${command.description}`.toLowerCase().includes(query.trim().toLowerCase()),
  );

  useEffect(() => {
    if (isOpen) {
      window.requestAnimationFrame(() => inputRef.current?.focus());
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const selectFirstResult = () => {
    const firstResult = results[0];
    if (firstResult) onSelect(firstResult.target);
  };

  return (
    <div
      className="operations-command-backdrop"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) onClose();
      }}
    >
      <div className="operations-command-dialog" role="dialog" aria-modal="true" aria-labelledby="command-dialog-title">
        <div className="operations-command-header">
          <div>
            <span className="operations-eyebrow">Quick navigation</span>
            <h2 id="command-dialog-title">Command search</h2>
          </div>
          <button type="button" className="operations-icon-button" onClick={onClose} aria-label="Close command search">
            <X size={18} aria-hidden="true" />
          </button>
        </div>
        <div className="operations-command-input-wrap">
          <Search size={18} aria-hidden="true" />
          <label htmlFor="operations-command-input" className="visually-hidden">Search operations commands</label>
          <input
            ref={inputRef}
            id="operations-command-input"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === 'Escape') onClose();
              if (event.key === 'Enter') selectFirstResult();
            }}
            placeholder="Try “triage” or “regional risk”"
            autoComplete="off"
          />
          <kbd>Esc</kbd>
        </div>
        <div className="operations-command-results" aria-live="polite">
          {results.length > 0 ? (
            results.map((command) => (
              <button
                type="button"
                key={command.target}
                className="operations-command-result"
                onClick={() => onSelect(command.target)}
              >
                <div>
                  <strong>{command.label}</strong>
                  <span>{command.description}</span>
                </div>
                <ArrowUpRight size={17} aria-hidden="true" />
              </button>
            ))
          ) : (
            <div className="operations-command-empty">
              <Search size={18} aria-hidden="true" />
              <span>No commands match “{query}”.</span>
            </div>
          )}
        </div>
        <p className="operations-command-hint">Use <kbd>Ctrl K</kbd> anytime to open this menu.</p>
      </div>
    </div>
  );
}

function KpiCard({
  label,
  value,
  detail,
  icon: Icon,
  tone,
}: {
  label: string;
  value: string;
  detail: string;
  icon: LucideIcon;
  tone: 'primary' | 'amber' | 'critical' | 'cyan';
}) {
  return (
    <article className={`operations-kpi-card operations-kpi-card--${tone}`}>
      <div className="operations-kpi-icon" aria-hidden="true">
        <Icon size={19} />
      </div>
      <div className="operations-kpi-copy">
        <span>{label}</span>
        <strong>{value}</strong>
        <small>{detail}</small>
      </div>
    </article>
  );
}

function OperationsLoadingState({ live }: { live: boolean }) {
  return (
    <div className="operations-state-card" role="status" aria-live="polite">
      <div className="operations-state-icon operations-state-icon--loading" aria-hidden="true">
        <RefreshCw size={24} />
      </div>
       <h2>{live ? 'Refreshing live operations data' : 'Refreshing the demo snapshot'}</h2>
       <p>{live ? 'Reading the authenticated, read-only operations API.' : 'Rebuilding the local operations view. No network request is being made.'}</p>
      <div className="operations-loading-grid" aria-hidden="true">
        <span />
        <span />
        <span />
      </div>
    </div>
  );
}

function OperationsEmptyState({ live }: { live: boolean }) {
  return (
    <div className="operations-state-card" role="status" aria-live="polite">
      <div className="operations-state-icon" aria-hidden="true">
        <Inbox size={24} />
      </div>
       <h2>No advisory cases in this snapshot</h2>
       <p>{live ? 'The protected operations API is healthy, but no pending advisory cases were returned.' : 'The operations console is ready, but the supplied demo dataset has no cases to summarize yet.'}</p>
    </div>
  );
}

function OperationsErrorState({ onRetry, live }: { onRetry: () => void; live: boolean }) {
  return (
    <div className="operations-state-card operations-state-card--error" role="alert">
      <div className="operations-state-icon operations-state-icon--error" aria-hidden="true">
        <CircleAlert size={24} />
      </div>
      <h2>Snapshot data is unavailable</h2>
       <p>
         {live
           ? 'The authenticated operations API could not be read. No write operation was attempted.'
           : 'This staff preview could not read its local advisory payload. No live operations or writes were attempted.'}
       </p>
      <button type="button" className="operations-button operations-button-primary" onClick={onRetry}>
        <RefreshCw size={16} aria-hidden="true" />
        Try again
      </button>
    </div>
  );
}

function OperationsLiveQueue({ items }: { items: OperationsQueueItem[] }) {
  return (
    <div className="operations-backlog-list" id="triage-panel" role="tabpanel" aria-label="Live triage cases" aria-live="polite">
      {items.length === 0 ? (
        <div className="operations-inline-empty">
          <Inbox size={21} aria-hidden="true" />
          <div>
            <strong>No pending advisory cases.</strong>
            <span>The authenticated operations API returned an empty review queue.</span>
          </div>
        </div>
      ) : (
        items.map((item) => (
          <article className="operations-backlog-item" key={item.advisory_id}>
            <div className="operations-case-avatar" aria-hidden="true">
              {getInitials(item.farmer_name)}
            </div>
            <div className="operations-case-main">
              <div className="operations-case-meta">
                <span className="operations-case-id">{item.advisory_id}</span>
                <StatusPill tone={getStatusTone(item.triage_status)} label={getStatusLabel(item.triage_status)} />
                <StatusPill tone={item.safe_to_act ? 'approved' : 'critical'} label={item.safe_to_act ? 'Safe to act' : 'Safety hold'} />
              </div>
              <h3>{item.crop || 'Unclassified crop'} advisory</h3>
              <div className="operations-case-details">
                <span>{item.farmer_name}</span>
                <span className="operations-detail-separator" aria-hidden="true">·</span>
                <span className="operations-detail-with-icon">
                  <MapPin size={13} aria-hidden="true" />
                  {item.district || 'District unavailable'}
                </span>
                {item.farm_name && (
                  <>
                    <span className="operations-detail-separator" aria-hidden="true">·</span>
                    <span>{item.farm_name}</span>
                  </>
                )}
              </div>
            </div>
            <div className="operations-case-confidence">
              <span>Model confidence</span>
              <strong>{item.confidence_score == null ? '—' : `${Math.round(item.confidence_score * 100)}%`}</strong>
              <small>{formatSnapshotDate(item.created_at || undefined)}</small>
            </div>
            <span className="operations-button operations-button-secondary operations-case-action" aria-label="Live review action not connected">
              <Eye size={16} aria-hidden="true" />
              <span>Read-only</span>
            </span>
          </article>
        ))
      )}
    </div>
  );
}

function OperationsConsole({
  advisories,
  outbreaks = REGIONAL_OUTBREAKS,
  theme,
  onToggleTheme,
  operatorName,
  operatorRole,
  accessToken,
  refreshToken,
  onSessionRefresh,
  onSignOut,
}: OperationsConsoleProps) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isCommandOpen, setIsCommandOpen] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [liveSnapshot, setLiveSnapshot] = useState<OperationsSnapshot | null>(null);
  const [liveError, setLiveError] = useState(false);
  const [backlogFilter, setBacklogFilter] = useState<TriageFilter>('ALL');
  const [backlogQuery, setBacklogQuery] = useState('');
  const commandTriggerRef = useRef<HTMLButtonElement>(null);
  const refreshTimerRef = useRef<ReturnType<typeof window.setTimeout> | null>(null);
  const isLive = Boolean(accessToken);

  const hasValidPayload = Array.isArray(advisories) && Array.isArray(outbreaks);
  const safeAdvisories = useMemo(
    () => (Array.isArray(advisories) ? advisories : []),
    [advisories],
  );
  const safeOutbreaks = useMemo(
    () => (Array.isArray(outbreaks) ? outbreaks : []),
    [outbreaks],
  );
  const snapshotStatus: SnapshotStatus = isLive
    ? isRefreshing
      ? 'loading'
      : liveError
        ? 'error'
        : liveSnapshot && liveSnapshot.queue.items.length === 0
          ? 'empty'
          : liveSnapshot
            ? 'ready'
            : 'loading'
    : !hasValidPayload
      ? 'error'
      : isRefreshing
        ? 'loading'
        : safeAdvisories.length === 0
          ? 'empty'
          : 'ready';

  const loadLiveSnapshot = async () => {
    if (!accessToken) return;
    setIsRefreshing(true);
    setLiveError(false);
    try {
      setLiveSnapshot(await fetchOperationsSnapshot(accessToken));
    } catch (caughtError) {
      if (caughtError instanceof ApiError && caughtError.status === 401 && refreshToken && onSessionRefresh) {
        try {
          const refreshed = await refreshAccessToken(refreshToken);
          onSessionRefresh(refreshed);
          return;
        } catch {
          // A failed refresh means the browser session is no longer authorized.
          onSignOut?.();
          return;
        }
      }
      if (caughtError instanceof ApiError && caughtError.status === 401) {
        onSignOut?.();
        return;
      }
      setLiveSnapshot(null);
      setLiveError(true);
    } finally {
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    if (isLive) void loadLiveSnapshot();
    // The token is the only live-data input; refresh is intentionally manual.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [accessToken, isLive]);

  useEffect(() => {
    const onGlobalKeyDown = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault();
        setIsCommandOpen(true);
      }

      if (event.key === 'Escape' && isSidebarOpen) {
        setIsSidebarOpen(false);
      }
    };

    window.addEventListener('keydown', onGlobalKeyDown);
    return () => window.removeEventListener('keydown', onGlobalKeyDown);
  }, [isSidebarOpen]);

  useEffect(() => {
    return () => {
      if (refreshTimerRef.current) window.clearTimeout(refreshTimerRef.current);
    };
  }, []);

  const handleRefresh = () => {
    if (isRefreshing) return;
    if (isLive) {
      void loadLiveSnapshot();
      return;
    }
    setIsRefreshing(true);
    refreshTimerRef.current = window.setTimeout(() => {
      setIsRefreshing(false);
      refreshTimerRef.current = null;
    }, 650);
  };

  const handleCloseCommand = () => {
    setIsCommandOpen(false);
    window.requestAnimationFrame(() => commandTriggerRef.current?.focus());
  };

  const handleCommandSelect = (target: string) => {
    handleCloseCommand();
    if (target === 'expert-queue') {
      window.location.assign(`${import.meta.env.BASE_URL}dashboard`);
      return;
    }

    window.requestAnimationFrame(() => {
      const section = document.getElementById(target);
      section?.scrollIntoView({
        behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
        block: 'start',
      });
    });
  };

  const metrics = useMemo(() => {
    const pending = safeAdvisories.filter((advisory) => advisory.triageStatus === 'PENDING_REVIEW').length;
    const escalated = safeAdvisories.filter((advisory) => advisory.triageStatus === 'ESCALATED').length;
    const highRisk = safeAdvisories.filter(
      (advisory) => advisory.severityRisk === 'CRITICAL' || advisory.severityRisk === 'HIGH',
    ).length;
    const averageConfidence = safeAdvisories.length
      ? Math.round(
          (safeAdvisories.reduce((total, advisory) => total + advisory.confidenceScore, 0) /
            safeAdvisories.length) *
            100,
        )
      : 0;
    const latestAdvisory = safeAdvisories.reduce<DiagnosticAdvisory | null>((latest, advisory) => {
      if (!latest || new Date(advisory.createdAt).getTime() > new Date(latest.createdAt).getTime()) return advisory;
      return latest;
    }, null);

    return { pending, escalated, highRisk, averageConfidence, latestAdvisory };
  }, [safeAdvisories]);

  const displayMetrics = liveSnapshot
    ? {
        active: liveSnapshot.summary.active_advisories,
        pending: liveSnapshot.summary.needs_review,
        escalated: 0,
        highRisk: liveSnapshot.summary.high_confidence,
        averageConfidence: Math.round(liveSnapshot.summary.average_confidence * 100),
      }
    : {
        active: safeAdvisories.length,
        pending: metrics.pending,
        escalated: metrics.escalated,
        highRisk: metrics.highRisk,
        averageConfidence: metrics.averageConfidence,
      };

  const regionRows = useMemo(() => {
    const districtCounts = new Map<string, number>();
    safeAdvisories.forEach((advisory) => {
      const district = advisory.farmerContext.district;
      districtCounts.set(district, (districtCounts.get(district) ?? 0) + 1);
    });

    return safeOutbreaks.map((outbreak) => ({
      ...outbreak,
      advisoryCount: districtCounts.get(outbreak.district) ?? 0,
    }));
  }, [safeAdvisories, safeOutbreaks]);

  const coveredRegions = regionRows.filter((region) => region.advisoryCount > 0).length;
  const coveragePercent = regionRows.length ? Math.round((coveredRegions / regionRows.length) * 100) : 0;
  const affectedFarms = safeOutbreaks.reduce((total, outbreak) => total + outbreak.affectedFarmsReported, 0);

  const filteredBacklog = useMemo(() => {
    const normalizedQuery = backlogQuery.trim().toLowerCase();
    return [...safeAdvisories]
      .filter((advisory) => {
        if (backlogFilter === 'NEEDS_REVIEW' && isResolved(advisory.triageStatus)) return false;
        if (backlogFilter === 'ESCALATED' && advisory.triageStatus !== 'ESCALATED') return false;
        if (backlogFilter === 'RESOLVED' && !isResolved(advisory.triageStatus)) return false;
        if (!normalizedQuery) return true;

        return [
          advisory.id,
          advisory.farmerContext.farmerName,
          advisory.farmerContext.district,
          advisory.farmerContext.crop,
          advisory.diagnosisNameEn,
        ].some((value) => value.toLowerCase().includes(normalizedQuery));
      })
      .sort((first, second) => {
        const riskDelta = RISK_ORDER[first.severityRisk] - RISK_ORDER[second.severityRisk];
        if (riskDelta !== 0) return riskDelta;
        return new Date(second.createdAt).getTime() - new Date(first.createdAt).getTime();
      });
  }, [backlogFilter, backlogQuery, safeAdvisories]);

  const filterCounts = useMemo(
    () => ({
      ALL: safeAdvisories.length,
      NEEDS_REVIEW: safeAdvisories.filter((advisory) => !isResolved(advisory.triageStatus)).length,
      ESCALATED: safeAdvisories.filter((advisory) => advisory.triageStatus === 'ESCALATED').length,
      RESOLVED: safeAdvisories.filter((advisory) => isResolved(advisory.triageStatus)).length,
    }),
    [safeAdvisories],
  );

  const latestSnapshot = formatSnapshotDate(liveSnapshot?.summary.generated_at || metrics.latestAdvisory?.createdAt);

  return (
    <div className="operations-console">
      <a className="operations-skip-link" href="#operations-main">
        Skip to main content
      </a>

       <OperationsSidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} live={isLive} />

      <div className="operations-content">
        <OperationsTopbar
          theme={theme}
          onToggleTheme={onToggleTheme}
          onOpenMenu={() => setIsSidebarOpen(true)}
          onOpenCommand={() => setIsCommandOpen(true)}
          commandTriggerRef={commandTriggerRef}
           operatorName={operatorName}
           operatorRole={operatorRole}
           live={isLive}
           onSignOut={onSignOut}
        />

        <main
          id="operations-main"
          className="operations-main"
          tabIndex={-1}
          aria-busy={snapshotStatus === 'loading'}
        >
          <div className="operations-page">
            <section id="overview" className="operations-page-header" aria-labelledby="operations-title">
              <div className="operations-page-header-meta">
                <div className="operations-eyebrow-row">
                  <span className="operations-live-dot" aria-hidden="true" />
                  <span className="operations-eyebrow">Operations console</span>
                  <span className="operations-meta-divider" aria-hidden="true" />
                   <span className="operations-muted-label">Internal staff workspace</span>
                 </div>
                 <StatusPill tone={isLive ? 'approved' : 'demo'} label={isLive ? 'Live API snapshot' : 'Seed/demo snapshot'} />
              </div>
              <div className="operations-title-row">
                <div>
                  <h1 id="operations-title">Make the next field decision visible.</h1>
                  <p>
                    A nationwide view for field operations: prioritize uncertain diagnoses, monitor regional risk,
                    and keep the review team moving.
                  </p>
                </div>
                <Link to="#triage" className="operations-button operations-button-primary operations-title-action">
                  <ClipboardCheck size={17} aria-hidden="true" />
                  Review priority cases
                </Link>
              </div>
            </section>

            <section className="operations-demo-banner" aria-label="Demo data notice">
              <div className="operations-demo-banner-copy">
                <div className="operations-demo-banner-icon" aria-hidden="true">
                  <Database size={18} />
                </div>
                <div>
                     <strong>{isLive ? 'Authenticated staff view · read-only API data' : 'Staff UX preview · read-only demo data'}</strong>
                     <span>
                       {isLive
                         ? 'Metrics and triage rows are read from the protected operations API. Review writes remain outside this console.'
                         : 'Authentication, live sync, and persistence are not connected. Values below are computed from the bundled advisory seed snapshot.'}
                     </span>
                </div>
              </div>
              <button
                type="button"
                className="operations-button operations-button-secondary"
                onClick={handleRefresh}
                disabled={isRefreshing}
              >
                <RefreshCw size={16} aria-hidden="true" className={isRefreshing ? 'operations-spin' : undefined} />
                {isRefreshing ? 'Refreshing…' : 'Refresh snapshot'}
              </button>
            </section>

            {snapshotStatus !== 'ready' ? (
              <section className="operations-state-region" aria-label="Snapshot state">
                 {snapshotStatus === 'loading' && <OperationsLoadingState live={isLive} />}
                 {snapshotStatus === 'empty' && <OperationsEmptyState live={isLive} />}
                 {snapshotStatus === 'error' && <OperationsErrorState onRetry={handleRefresh} live={isLive} />}
              </section>
            ) : (
              <>
                <section className="operations-kpi-grid" aria-label="Operations key performance indicators">
                  <KpiCard
                    label="Active advisories"
                     value={formatNumber(displayMetrics.active)}
                     detail={isLive ? 'Protected API total' : 'Cases in this seed snapshot'}
                    icon={ClipboardCheck}
                    tone="primary"
                  />
                  <KpiCard
                    label="Needs triage"
                     value={formatNumber(displayMetrics.pending + displayMetrics.escalated)}
                     detail={isLive ? `${displayMetrics.pending} requiring review` : `${displayMetrics.pending} pending · ${displayMetrics.escalated} escalated`}
                    icon={AlertTriangle}
                    tone="amber"
                  />
                  <KpiCard
                    label="High-confidence advisories"
                    value={formatNumber(displayMetrics.highRisk)}
                    detail={isLive ? 'Protected API confidence threshold' : 'Priority cases to route first'}
                    icon={ShieldCheck}
                    tone="critical"
                  />
                  <KpiCard
                    label="Avg. model confidence"
                     value={`${displayMetrics.averageConfidence}%`}
                     detail={isLive ? 'Average API confidence score' : 'Across seeded diagnostic outputs'}
                    icon={Activity}
                    tone="cyan"
                  />
                </section>

                <section id="triage" className="operations-card operations-section" aria-labelledby="triage-heading">
                  <div className="operations-section-header">
                    <div>
                      <div className="operations-section-kicker">
                        <ClipboardCheck size={15} aria-hidden="true" />
                        <span>Decision queue</span>
                      </div>
                      <h2 id="triage-heading">Triage &amp; review backlog</h2>
                       <p>
                         {isLive
                           ? 'Live queue records are read-only here; use the authorized expert review workflow for review writes.'
                           : 'Sorted by risk first, then newest intake. Open a case in the existing expert review flow.'}
                       </p>
                     </div>
                     {!isLive && (
                       <Link to="/dashboard" className="operations-text-link">
                         Open full expert queue
                         <ArrowUpRight size={15} aria-hidden="true" />
                       </Link>
                     )}
                  </div>

                   {!isLive && <div className="operations-backlog-toolbar">
                    <div className="operations-search-field">
                      <Search size={17} aria-hidden="true" />
                      <label htmlFor="operations-backlog-search" className="visually-hidden">Search triage queue</label>
                      <input
                        id="operations-backlog-search"
                        type="search"
                        value={backlogQuery}
                        onChange={(event) => setBacklogQuery(event.target.value)}
                        placeholder="Search case, farmer, crop, or district"
                      />
                    </div>
                    <div className="operations-filter-group" role="tablist" aria-label="Triage queue filters">
                      {FILTER_OPTIONS.map((option) => (
                        <button
                          key={option.value}
                          type="button"
                          role="tab"
                          aria-selected={backlogFilter === option.value}
                          aria-controls="triage-panel"
                          className={`operations-filter-button${backlogFilter === option.value ? ' operations-filter-button--active' : ''}`}
                          onClick={() => setBacklogFilter(option.value)}
                        >
                          {option.label}
                          <span>{filterCounts[option.value]}</span>
                        </button>
                      ))}
                    </div>
                   </div>}

                   {isLive ? (
                     <OperationsLiveQueue items={liveSnapshot?.queue.items ?? []} />
                   ) : (
                     <div
                       className="operations-backlog-list"
                       id="triage-panel"
                       role="tabpanel"
                       aria-label={`${FILTER_OPTIONS.find((option) => option.value === backlogFilter)?.label} triage cases`}
                       aria-live="polite"
                     >
                       {filteredBacklog.length === 0 ? (
                         <div className="operations-inline-empty">
                           <Inbox size={21} aria-hidden="true" />
                           <div>
                             <strong>No cases match this view.</strong>
                             <span>Clear the search or choose another queue filter to see more seed records.</span>
                           </div>
                           <button
                             type="button"
                             className="operations-button operations-button-secondary"
                             onClick={() => {
                               setBacklogQuery('');
                               setBacklogFilter('ALL');
                             }}
                           >
                             Clear filters
                           </button>
                         </div>
                       ) : (
                         filteredBacklog.map((advisory) => (
                           <article className="operations-backlog-item" key={advisory.id}>
                             <div className="operations-case-avatar" aria-hidden="true">
                               {getInitials(advisory.farmerContext.farmerName)}
                             </div>
                             <div className="operations-case-main">
                               <div className="operations-case-meta">
                                 <span className="operations-case-id">{advisory.id}</span>
                                 <StatusPill tone={getStatusTone(advisory.triageStatus)} label={getStatusLabel(advisory.triageStatus)} />
                                 <StatusPill tone={advisory.severityRisk.toLowerCase() as PillTone} label={`${advisory.severityRisk} risk`} />
                               </div>
                               <h3>{advisory.diagnosisNameEn}</h3>
                               <div className="operations-case-details">
                                 <span>{advisory.farmerContext.farmerName}</span>
                                 <span className="operations-detail-separator" aria-hidden="true">·</span>
                                 <span className="operations-detail-with-icon">
                                   <MapPin size={13} aria-hidden="true" />
                                   {advisory.farmerContext.district}
                                 </span>
                                 <span className="operations-detail-separator" aria-hidden="true">·</span>
                                 <span>{advisory.farmerContext.crop}</span>
                               </div>
                             </div>
                             <div className="operations-case-confidence">
                               <span>Model confidence</span>
                               <strong>{Math.round(advisory.confidenceScore * 100)}%</strong>
                               <small>{formatSnapshotDate(advisory.createdAt)}</small>
                             </div>
                             <Link
                               to={`/review/${advisory.id}`}
                               className="operations-button operations-button-secondary operations-case-action"
                               aria-label={`Review ${advisory.diagnosisNameEn} for ${advisory.farmerContext.farmerName}`}
                             >
                               <Eye size={16} aria-hidden="true" />
                               <span>Review</span>
                               <ChevronRight size={15} aria-hidden="true" />
                             </Link>
                           </article>
                         ))
                       )}
                     </div>
                   )}
                 </section>

                <div className="operations-secondary-grid">
                  <section id="regional-risk" className="operations-card operations-section" aria-labelledby="regional-risk-heading">
                    <div className="operations-section-header">
                      <div>
                        <div className="operations-section-kicker">
                          <MapIcon size={15} aria-hidden="true" />
                          <span>Field coverage</span>
                        </div>
                        <h2 id="regional-risk-heading">Regional risk &amp; coverage</h2>
                        <p>District alerts from the bundled regional outbreak snapshot.</p>
                      </div>
                      <StatusPill tone="attention" label={`${formatNumber(affectedFarms)} farms reported`} />
                    </div>

                    <div className="operations-coverage-summary">
                      <div className="operations-coverage-number">
                        <strong>{coveragePercent}%</strong>
                        <span>case coverage</span>
                      </div>
                      <div className="operations-coverage-copy">
                        <strong>{coveredRegions} of {regionRows.length} alert districts have a case record</strong>
                        <span>Coverage here means an advisory in the local seed dataset, not verified field surveillance.</span>
                        <div
                          className="operations-progress-track"
                          role="progressbar"
                          aria-label="Regional case coverage"
                          aria-valuemin={0}
                          aria-valuemax={100}
                          aria-valuenow={coveragePercent}
                        >
                          <span style={{ width: `${coveragePercent}%` }} />
                        </div>
                      </div>
                    </div>

                    <div className="operations-region-list">
                      {regionRows.length === 0 ? (
                        <div className="operations-inline-empty operations-inline-empty--compact">
                          <MapPin size={19} aria-hidden="true" />
                          <span>No regional alerts are available in this snapshot.</span>
                        </div>
                      ) : (
                        regionRows.map((region) => (
                          <div className="operations-region-row" key={region.id}>
                            <div className="operations-region-marker" aria-hidden="true">
                              <MapPin size={16} />
                            </div>
                            <div className="operations-region-copy">
                              <div>
                                <strong>{region.district}</strong>
                                <StatusPill tone={region.severity.toLowerCase() as PillTone} label={region.severity} />
                              </div>
                              <span>{region.crop} · {region.disease}</span>
                            </div>
                            <div className="operations-region-count">
                              <strong>{region.advisoryCount}</strong>
                              <span>{region.advisoryCount === 1 ? 'case' : 'cases'}</span>
                            </div>
                          </div>
                        ))
                      )}
                    </div>
                  </section>

                  <section id="service-health" className="operations-card operations-section" aria-labelledby="service-health-heading">
                    <div className="operations-section-header">
                      <div>
                        <div className="operations-section-kicker">
                          <ServerCog size={15} aria-hidden="true" />
                          <span>Reliability</span>
                        </div>
                        <h2 id="service-health-heading">Service health</h2>
                         <p>{isLive ? 'Protected API status and explicit service boundaries.' : 'Clear boundaries for what this preview can and cannot report.'}</p>
                       </div>
                       <StatusPill tone={isLive ? 'approved' : 'offline'} label={isLive ? 'API connected' : 'No live sync'} />
                    </div>

                    <div className="operations-service-list">
                      {[
                        {
                          name: 'Advisory snapshot',
                           detail: isLive ? 'Protected database · read-only' : 'Local seed data · read-only',
                           lastSync: `Snapshot ${latestSnapshot}`,
                           tone: isLive ? 'approved' as PillTone : 'demo' as PillTone,
                           status: isLive ? 'API ready' : 'Demo ready',
                          icon: Database,
                        },
                        {
                          name: 'Expert review writes',
                           detail: isLive ? 'Separate expert authorization' : 'In-memory session only',
                           lastSync: isLive ? 'No write path in operations console' : 'Persistence not connected',
                          tone: 'attention' as PillTone,
                          status: 'Local only',
                          icon: ClipboardCheck,
                        },
                        {
                          name: 'Regional alert feed',
                          detail: 'Bundled outbreak records',
                          lastSync: 'Live feed not connected',
                          tone: 'demo' as PillTone,
                          status: 'Demo ready',
                          icon: MapIcon,
                        },
                        {
                          name: 'Notifications & sync',
                          detail: 'No delivery provider configured',
                          lastSync: 'Last sync: unavailable',
                          tone: 'offline' as PillTone,
                          status: 'Offline',
                          icon: CloudOff,
                        },
                      ].map((service) => {
                        const ServiceIcon = service.icon;
                        return (
                          <div className="operations-service-row" key={service.name}>
                            <div className="operations-service-icon" aria-hidden="true">
                              <ServiceIcon size={17} />
                            </div>
                            <div className="operations-service-copy">
                              <div>
                                <strong>{service.name}</strong>
                                <StatusPill tone={service.tone} label={service.status} />
                              </div>
                              <span>{service.detail}</span>
                              <small>{service.lastSync}</small>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </section>
                </div>

                <footer className="operations-footnote">
                  <Info size={16} aria-hidden="true" />
                  <span>
                     {isLive
                       ? 'Operations metrics and queue rows are authenticated read-only API data. Regional alerts and review writes remain separate service boundaries.'
                       : 'This is a staff-facing interface preview. Use the public experience or existing expert dashboard for the other demo flows; do not treat these values as live operational status.'}
                  </span>
                </footer>
              </>
            )}
          </div>
        </main>
      </div>

      <CommandDialog
        key={isCommandOpen ? 'command-open' : 'command-closed'}
        isOpen={isCommandOpen}
        onClose={handleCloseCommand}
        onSelect={handleCommandSelect}
      />
    </div>
  );
}

export { OperationsConsole };
