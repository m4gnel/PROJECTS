import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, useNavigate, useParams, Navigate } from 'react-router-dom';
import { PublicLandingPage } from './views/PublicLandingPage';
import { AuthPortal } from './views/AuthPortal';
import { ExpertDashboard } from './views/ExpertDashboard';
import { FarmerAdvisorySandbox } from './views/FarmerAdvisorySandbox';
import { ReviewDetailView } from './views/ReviewDetailView';
import { SEED_ADVISORIES } from './data/seedData';
import { DiagnosticAdvisory } from './types';

function LandingRoute({
  lang,
  onToggleLang,
  theme,
  onToggleTheme,
}: {
  lang: 'en' | 'ml';
  onToggleLang: () => void;
  theme: 'dark' | 'light';
  onToggleTheme: () => void;
}) {
  const navigate = useNavigate();
  return (
    <PublicLandingPage
      onEnterAuth={() => navigate('/auth')}
      onDirectPlatformAccess={() => navigate('/sandbox')}
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
}: {
  lang: 'en' | 'ml';
  onToggleLang: () => void;
}) {
  const navigate = useNavigate();
  return (
    <AuthPortal
      onLoginSuccess={(role) => {
        if (role === 'expert') {
          navigate('/dashboard');
        } else {
          navigate('/sandbox');
        }
      }}
      onBackToLanding={() => navigate('/')}
      lang={lang}
      onToggleLang={onToggleLang}
    />
  );
}

function DashboardRoute({
  advisories,
  lang,
}: {
  advisories: DiagnosticAdvisory[];
  lang: 'en' | 'ml';
}) {
  const navigate = useNavigate();
  return (
    <ExpertDashboard
      advisories={advisories}
      onSelectAdvisory={(advisory) => navigate(`/review/${advisory.id}`)}
      lang={lang}
    />
  );
}

function ReviewDetailRoute({
  advisories,
  onSaveVerdict,
  lang,
}: {
  advisories: DiagnosticAdvisory[];
  onSaveVerdict: (id: string, verdict: 'AGREE' | 'DISAGREE' | 'PARTIAL', notes: string, safetyOk: boolean) => void;
  lang: 'en' | 'ml';
}) {
  const navigate = useNavigate();
  const { advisory_id } = useParams<{ advisory_id: string }>();
  const advisory = advisories.find((a) => a.id === advisory_id) || advisories[0];

  return (
    <ReviewDetailView
      advisory={advisory}
      onBack={() => navigate('/dashboard')}
      onSaveVerdict={(id, verdict, notes, safetyOk) => {
        onSaveVerdict(id, verdict, notes, safetyOk);
        navigate('/dashboard');
      }}
      lang={lang}
    />
  );
}

function SandboxRoute({
  lang,
  onToggleLang,
}: {
  lang: 'en' | 'ml';
  onToggleLang: () => void;
}) {
  return <FarmerAdvisorySandbox lang={lang} onToggleLang={onToggleLang} />;
}

export default function App() {
  const [lang, setLang] = useState<'en' | 'ml'>('en');
  const [theme, setTheme] = useState<'dark' | 'light'>(() => {
    return (localStorage.getItem('agrisage_theme') as 'dark' | 'light') || 'dark';
  });
  const [advisories, setAdvisories] = useState<DiagnosticAdvisory[]>(SEED_ADVISORIES);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
      document.documentElement.classList.remove('light');
    } else {
      document.documentElement.classList.add('light');
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('agrisage_theme', theme);
  }, [theme]);

  const toggleLang = () => setLang((prev) => (prev === 'en' ? 'ml' : 'en'));
  const toggleTheme = () => setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));

  const handleSaveVerdict = (
    id: string,
    verdict: 'AGREE' | 'DISAGREE' | 'PARTIAL',
    notes: string,
    safetyOk: boolean
  ) => {
    setAdvisories((prev) =>
      prev.map((adv) =>
        adv.id === id
          ? {
              ...adv,
              reviewStatus: verdict === 'AGREE' ? 'APPROVED' : 'REJECTED',
              expertNotes: notes,
            }
          : adv
      )
    );
  };

  const basename = import.meta.env.BASE_URL || '/';

  return (
    <BrowserRouter basename={basename}>
      <Routes>
        <Route
          path="/"
          element={
            <LandingRoute
              lang={lang}
              onToggleLang={toggleLang}
              theme={theme}
              onToggleTheme={toggleTheme}
            />
          }
        />
        <Route
          path="/auth"
          element={<AuthRoute lang={lang} onToggleLang={toggleLang} />}
        />
        <Route
          path="/login"
          element={<AuthRoute lang={lang} onToggleLang={toggleLang} />}
        />
        <Route
          path="/dashboard"
          element={<DashboardRoute advisories={advisories} lang={lang} />}
        />
        <Route
          path="/sandbox"
          element={<SandboxRoute lang={lang} onToggleLang={toggleLang} />}
        />
        <Route
          path="/review/:advisory_id"
          element={
            <ReviewDetailRoute
              advisories={advisories}
              onSaveVerdict={handleSaveVerdict}
              lang={lang}
            />
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

