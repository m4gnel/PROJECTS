import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, useNavigate, useParams, Navigate } from 'react-router-dom';
import { PublicLandingPage } from './views/PublicLandingPage';
import { AccessPortal } from './views/AccessPortal';
import { ExpertDashboard } from './views/ExpertDashboard';
import { FarmerAdvisorySandbox } from './views/FarmerAdvisorySandbox';
import { ReviewDetailView } from './views/ReviewDetailView';
import { OperationsConsole } from './views/OperationsConsole';
import { StaffWorkspaceFrame } from './components/staff/StaffWorkspaceFrame';
import { clearPortalSession, getRoleHome, readPortalSession, savePortalSession } from './auth/session';
import { REGIONAL_OUTBREAKS, SEED_ADVISORIES } from './data/seedData';
import { DiagnosticAdvisory } from './types';
import type { PortalRole, PortalSession } from './auth/session';
import { isLiveApiConfigured, revokeRefreshToken } from './api/client';
import type { AuthResponse } from './api/client';

const readThemePreference = (): 'dark' | 'light' => {
  if (typeof window === 'undefined') return 'dark';
  try {
    const stored = window.localStorage.getItem('agrisage_theme');
    return stored === 'light' ? 'light' : 'dark';
  } catch {
    return 'dark';
  }
};

function LandingRoute({
  lang,
  onToggleLang,
  theme,
  onToggleTheme,
  onEnterSignup,
}: {
  lang: 'en' | 'ml';
  onToggleLang: () => void;
  theme: 'dark' | 'light';
  onToggleTheme: () => void;
  onEnterSignup: () => void;
}) {
  const navigate = useNavigate();
  return (
    <PublicLandingPage
      onEnterAuth={() => navigate('/auth')}
      onDirectPlatformAccess={() => navigate('/sandbox')}
      onOperationsAccess={() => navigate('/auth?mode=login&role=employee')}
      onEnterSignup={onEnterSignup}
      lang={lang}
      onToggleLang={onToggleLang}
      theme={theme}
      onToggleTheme={onToggleTheme}
    />
  );
}

function AuthRoute({
  lang,
  onToggleLang,
  theme,
  onToggleTheme,
  onAuthenticated,
}: {
  lang: 'en' | 'ml';
  onToggleLang: () => void;
  theme: 'dark' | 'light';
  onToggleTheme: () => void;
  onAuthenticated: (session: PortalSession) => void;
}) {
  const navigate = useNavigate();
  return (
    <AccessPortal
      onAuthenticated={onAuthenticated}
      onBackToLanding={() => navigate('/')}
      lang={lang}
      onToggleLang={onToggleLang}
      theme={theme}
      onToggleTheme={onToggleTheme}
    />
  );
}

function DashboardRoute({
  advisories,
  lang,
  session,
  onSignOut,
}: {
  advisories: DiagnosticAdvisory[];
  lang: 'en' | 'ml';
  session: PortalSession;
  onSignOut: () => void;
}) {
  const navigate = useNavigate();
  return (
    <StaffWorkspaceFrame session={session} onSignOut={onSignOut}>
      {session.mode === 'backend' && (
        <div className="mb-4 rounded-xl border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-950" role="status">
          The review queue is currently a local seed snapshot. Verdict changes are kept in this browser session until the protected review-write API is connected.
        </div>
      )}
      <ExpertDashboard
        advisories={advisories}
        onSelectAdvisory={(advisory) => navigate(`/review/${advisory.id}`)}
        lang={lang}
      />
    </StaffWorkspaceFrame>
  );
}

function ReviewDetailRoute({
  advisories,
  onSaveVerdict,
  lang,
  session,
  onSignOut,
}: {
  advisories: DiagnosticAdvisory[];
  onSaveVerdict: (id: string, verdict: 'AGREE' | 'DISAGREE' | 'PARTIAL', notes: string, safetyOk: boolean) => void;
  lang: 'en' | 'ml';
  session: PortalSession;
  onSignOut: () => void;
}) {
  const navigate = useNavigate();
  const { advisory_id } = useParams<{ advisory_id: string }>();
  const advisory = advisories.find((a) => a.id === advisory_id);

  return (
    <StaffWorkspaceFrame session={session} onSignOut={onSignOut}>
      {advisory ? (
        <ReviewDetailView
          advisory={advisory}
          onBack={() => navigate('/dashboard')}
          onSaveVerdict={(id, verdict, notes, safetyOk) => {
            onSaveVerdict(id, verdict, notes, safetyOk);
            navigate('/dashboard');
          }}
          lang={lang}
        />
      ) : (
        <section className="glass-panel p-8 text-center" aria-labelledby="missing-case-title">
          <h1 id="missing-case-title" className="text-2xl font-bold text-[var(--color-on-surface)]">Case not found</h1>
          <p className="mt-2 text-sm text-[var(--color-on-surface-secondary)]">This advisory is not available in the current workspace snapshot.</p>
          <button type="button" className="btn btn-primary mt-6" onClick={() => navigate('/dashboard')}>Return to review queue</button>
        </section>
      )}
    </StaffWorkspaceFrame>
  );
}

function SandboxRoute({
  lang,
  onToggleLang,
  session,
  onSessionRefresh,
  onSessionExpired,
}: {
  lang: 'en' | 'ml';
  onToggleLang: () => void;
  session: PortalSession | null;
  onSessionRefresh: (response: AuthResponse) => void;
  onSessionExpired: () => void;
}) {
  return (
    <FarmerAdvisorySandbox
      lang={lang}
      onToggleLang={onToggleLang}
      accessToken={session?.mode === 'backend' ? session.accessToken : undefined}
      refreshToken={session?.mode === 'backend' ? session.refreshToken : undefined}
      farmerId={session?.userId}
      onSessionRefresh={onSessionRefresh}
      onSessionExpired={onSessionExpired}
    />
  );
}

function OperationsRoute({
  advisories,
  theme,
  onToggleTheme,
  session,
  onSignOut,
  onSessionRefresh,
}: {
  advisories: DiagnosticAdvisory[];
  theme: 'dark' | 'light';
  onToggleTheme: () => void;
  session: PortalSession;
  onSignOut: () => void;
  onSessionRefresh: (response: AuthResponse) => void;
}) {
  return (
    <OperationsConsole
      advisories={advisories}
      outbreaks={REGIONAL_OUTBREAKS}
      theme={theme}
      onToggleTheme={onToggleTheme}
      operatorName={session.displayName}
      operatorRole={session.role}
      accessToken={session.mode === 'backend' ? session.accessToken : undefined}
      refreshToken={session.mode === 'backend' ? session.refreshToken : undefined}
      onSessionRefresh={onSessionRefresh}
      onSignOut={onSignOut}
    />
  );
}

function RequireSession({
  session,
  allowedRoles,
  children,
}: {
  session: PortalSession | null;
  allowedRoles?: PortalRole[];
  children: React.ReactNode;
}) {
  if (!session) return <Navigate to="/auth?mode=login" replace />;
  if (allowedRoles && !allowedRoles.includes(session.role)) {
    return <Navigate to={getRoleHome(session.role)} replace />;
  }
  return <>{children}</>;
}

function AppRoutes({
  lang,
  theme,
  advisories,
  session,
  onToggleLang,
  onToggleTheme,
  onAuthenticated,
  onSignOut,
  onSessionRefresh,
  onSaveVerdict,
}: {
  lang: 'en' | 'ml';
  theme: 'dark' | 'light';
  advisories: DiagnosticAdvisory[];
  session: PortalSession | null;
  onToggleLang: () => void;
  onToggleTheme: () => void;
  onAuthenticated: (nextSession: PortalSession) => void;
  onSignOut: () => void;
  onSessionRefresh: (response: AuthResponse) => void;
  onSaveVerdict: (id: string, verdict: 'AGREE' | 'DISAGREE' | 'PARTIAL', notes: string, safetyOk: boolean) => void;
}) {
  const navigate = useNavigate();
  const handleSignOut = () => {
    onSignOut();
    navigate('/');
  };

  return (
    <Routes>
      <Route
        path="/"
        element={
          <LandingRoute
            lang={lang}
            onToggleLang={onToggleLang}
            theme={theme}
            onToggleTheme={onToggleTheme}
            onEnterSignup={() => navigate('/auth?mode=signup')}
          />
        }
      />
      <Route
        path="/auth"
        element={
          <AuthRoute
            lang={lang}
            onToggleLang={onToggleLang}
            theme={theme}
            onToggleTheme={onToggleTheme}
            onAuthenticated={(nextSession) => {
              onAuthenticated(nextSession);
              navigate(getRoleHome(nextSession.role), { replace: true });
            }}
          />
        }
      />
      <Route
        path="/login"
        element={<Navigate to="/auth?mode=login" replace />}
      />
      <Route
        path="/dashboard"
        element={
           <RequireSession session={session} allowedRoles={['expert']}>
            <DashboardRoute
              advisories={advisories}
              lang={lang}
               session={session as PortalSession}
               onSignOut={handleSignOut}
            />
          </RequireSession>
        }
      />
      <Route
        path="/sandbox"
        element={
          <SandboxRoute
            lang={lang}
            onToggleLang={onToggleLang}
            session={session}
            onSessionRefresh={onSessionRefresh}
            onSessionExpired={handleSignOut}
          />
        }
      />
      <Route
        path="/operations"
        element={
            <RequireSession session={session} allowedRoles={['employee', 'officer']}>
             <OperationsRoute
              advisories={advisories}
              theme={theme}
              onToggleTheme={onToggleTheme}
               session={session as PortalSession}
               onSignOut={handleSignOut}
               onSessionRefresh={onSessionRefresh}
             />
          </RequireSession>
        }
      />
      <Route
        path="/review/:advisory_id"
        element={
           <RequireSession session={session} allowedRoles={['expert']}>
            <ReviewDetailRoute
              advisories={advisories}
              onSaveVerdict={onSaveVerdict}
              lang={lang}
              session={session as PortalSession}
              onSignOut={handleSignOut}
            />
          </RequireSession>
        }
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default function App() {
  const [lang, setLang] = useState<'en' | 'ml'>('en');
  const [theme, setTheme] = useState<'dark' | 'light'>(readThemePreference);
  const [advisories, setAdvisories] = useState<DiagnosticAdvisory[]>(SEED_ADVISORIES);
  const [session, setSession] = useState<PortalSession | null>(() => readPortalSession({ allowBackend: isLiveApiConfigured }));

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
      document.documentElement.classList.remove('light');
    } else {
      document.documentElement.classList.add('light');
      document.documentElement.classList.remove('dark');
    }
    try {
      localStorage.setItem('agrisage_theme', theme);
    } catch {
      // Theme preference is optional; the current render still follows the selected theme.
    }
  }, [theme]);

  const toggleLang = () => setLang((prev) => (prev === 'en' ? 'ml' : 'en'));
  const toggleTheme = () => setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));

  const handleSaveVerdict = (
    id: string,
    verdict: 'AGREE' | 'DISAGREE' | 'PARTIAL',
    notes: string,
    safetyOk: boolean,
  ) => {
    setAdvisories((prev) =>
      prev.map((advisory) =>
        advisory.id === id
          ? {
              ...advisory,
              triageStatus: verdict === 'AGREE' ? 'VERIFIED_APPROVED' : 'OVERRIDDEN',
              expertReview: {
                reviewerName: session?.displayName || 'Demo reviewer',
                verdict,
                reviewedAt: new Date().toISOString(),
                safetyApproved: safetyOk,
                expertNotes: notes,
              },
            }
          : advisory,
      ),
    );
  };

  const basename = import.meta.env.BASE_URL || '/';

  return (
    <BrowserRouter basename={basename}>
      <AppRoutes
        lang={lang}
        theme={theme}
        advisories={advisories}
        session={session}
        onToggleLang={toggleLang}
        onToggleTheme={toggleTheme}
        onAuthenticated={(nextSession) => {
          savePortalSession(nextSession);
          setSession(nextSession);
        }}
         onSignOut={() => {
           const refreshToken = session?.mode === 'backend' ? session.refreshToken : undefined;
           clearPortalSession();
           setSession(null);
           if (refreshToken) void revokeRefreshToken(refreshToken).catch(() => undefined);
         }}
        onSessionRefresh={(response) => {
          setSession((current) => {
            if (!current || current.mode !== 'backend') return current;
            const refreshed: PortalSession = {
              ...current,
              accessToken: response.access_token,
              refreshToken: response.refresh_token,
            };
            savePortalSession(refreshed);
            return refreshed;
          });
        }}
        onSaveVerdict={handleSaveVerdict}
      />
    </BrowserRouter>
  );
}

