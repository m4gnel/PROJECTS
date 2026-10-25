import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { SEED_ADVISORIES } from '../data/seedData';
import { DiagnosticAdvisory } from '../types';
import {
  ApiError,
  isLiveApiConfigured,
  refreshAccessToken,
  requestAdvisory,
} from '../api/client';
import type { AuthResponse, AdvisoryResponse } from '../api/client';
import { ConfidenceBadge } from '../components/common/ConfidenceBadge';
import { RiskBadge } from '../components/common/RiskBadge';
import { RealtimeQualityBar } from '../components/sandbox/RealtimeQualityBar';
import { SafeImage } from '../components/common/SafeImage';
import { MorningBriefingCard } from '../components/cards/MorningBriefingCard';
import { EvidenceCard } from '../components/cards/EvidenceCard';
import { ScenarioCard } from '../components/cards/ScenarioCard';
import { SchemeCard } from '../components/cards/SchemeCard';
import {
  Smartphone,
  Camera,
  Sliders,
  Clock,
  Layers,
  ThumbsUp,
  ThumbsDown,
  ArrowLeft,
  Sparkles,
  Send,
  Droplets,
  Thermometer,
  CloudRain,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  Monitor,
  RotateCcw,
  Volume2,
  ExternalLink,
  ChevronRight,
  Info,
  DollarSign,
  Zap,
} from 'lucide-react';

interface FarmerAdvisorySandboxProps {
  lang: 'en' | 'ml';
  onToggleLang: () => void;
  accessToken?: string;
  refreshToken?: string;
  farmerId?: string;
  onSessionRefresh?: (response: AuthResponse) => void;
  onSessionExpired?: () => void;
}

export const FarmerAdvisorySandbox: React.FC<FarmerAdvisorySandboxProps> = ({
  lang,
  onToggleLang,
  accessToken,
  refreshToken,
  farmerId,
  onSessionRefresh,
  onSessionExpired,
}) => {
  const navigate = useNavigate();

  // Active Advisory / Crop Case Study
  const [selectedAdvisory, setSelectedAdvisory] = useState<DiagnosticAdvisory>(SEED_ADVISORIES[0]);

  // View Mode: 'workbench' (Desktop Studio Dashboard) vs 'mobile' (Smartphone Simulator)
  const [viewMode, setViewMode] = useState<'workbench' | 'mobile'>('workbench');

  // Workbench active protocol tab
  const [activeTab, setActiveTab] = useState<'PROTOCOL' | 'SCENARIOS' | 'EVIDENCE' | 'SCHEMES'>('PROTOCOL');

  // Mobile simulator active screen
  const [activeMobileScreen, setActiveMobileScreen] = useState<'HOME' | 'CAMERA' | 'ADVISORY'>('ADVISORY');

  // Live Advisory Q&A State
  const [question, setQuestion] = useState('');
  const [liveAnswer, setLiveAnswer] = useState<string | null>(null);
  const [liveWarnings, setLiveWarnings] = useState<string[]>([]);
  const [isAsking, setIsAsking] = useState(false);
  const [liveError, setLiveError] = useState<string | null>(null);
  const [isLiveResultFromBackend, setIsLiveResultFromBackend] = useState<boolean>(false);

  // Advisory feedback
  const [feedback, setFeedback] = useState<'helpful' | 'not-helpful' | null>(null);

  // Camera Simulation State (Computer Vision Quality Gate)
  const [blurValue, setBlurValue] = useState<number>(145); // threshold: >= 100 PASS
  const [brightnessValue, setBrightnessValue] = useState<number>(130); // threshold: 60 - 220 PASS
  const [framingValue, setFramingValue] = useState<number>(85); // threshold: >= 30% PASS

  const isCameraQualityAcceptable =
    blurValue >= 100 && brightnessValue >= 60 && brightnessValue <= 220 && framingValue >= 30;

  // Preset Handlers for CV Quality Gate
  const applyPreset = (preset: 'optimal' | 'blur' | 'glare' | 'framing') => {
    switch (preset) {
      case 'optimal':
        setBlurValue(155);
        setBrightnessValue(130);
        setFramingValue(85);
        break;
      case 'blur':
        setBlurValue(45);
        setBrightnessValue(130);
        setFramingValue(85);
        break;
      case 'glare':
        setBlurValue(155);
        setBrightnessValue(245);
        setFramingValue(85);
        break;
      case 'framing':
        setBlurValue(155);
        setBrightnessValue(130);
        setFramingValue(20);
        break;
    }
  };

  // Crop Switching Handler
  const handleSelectCrop = (advisory: DiagnosticAdvisory) => {
    setSelectedAdvisory(advisory);
    setLiveAnswer(null);
    setLiveWarnings([]);
    setLiveError(null);
    setFeedback(null);
  };

  // Ask Agri-SAGE Advisory (Calls Live Gemini Backend if authenticated, or intelligent offline ag-model)
  const handleAskAgriSage = async (customPrompt?: string) => {
    const promptToAsk = (customPrompt || question).trim();
    if (!promptToAsk) return;

    if (customPrompt) {
      setQuestion(customPrompt);
    }

    setIsAsking(true);
    setLiveError(null);

    // If authenticated with backend session, call the real live Gemini endpoint
    if (accessToken && farmerId) {
      try {
        const request = (token: string) =>
          requestAdvisory(
            {
              farmer_id: farmerId,
              query: promptToAsk,
              language: lang === 'ml' ? 'ml' : 'en',
              state: 'India',
              district: selectedAdvisory.farmerContext.district,
              crops: [selectedAdvisory.farmerContext.crop.toLowerCase()],
            },
            token,
          );

        let response: AdvisoryResponse;
        try {
          response = await request(accessToken);
        } catch (requestError) {
          if (!(requestError instanceof ApiError) || requestError.status !== 401 || !refreshToken || !onSessionRefresh) {
            throw requestError;
          }

          try {
            const refreshed = await refreshAccessToken(refreshToken);
            onSessionRefresh(refreshed);
            response = await request(refreshed.access_token);
          } catch (refreshError) {
            onSessionExpired?.();
            throw refreshError;
          }
        }
        setLiveAnswer(response.answer_native || response.answer_en);
        setLiveWarnings(response.warnings || []);
        setIsLiveResultFromBackend(true);
      } catch (error) {
        setLiveError(
          error instanceof ApiError ? error.message : 'The live advisory service could not be reached. Reverting to field model.',
        );
      } finally {
        setIsAsking(false);
      }
      return;
    }

    // Unauthenticated demo fallback: Instant, high-fidelity agronomic recommendation
    setTimeout(() => {
      setIsAsking(false);
      setIsLiveResultFromBackend(false);

      if (selectedAdvisory.farmerContext.crop === 'Rice') {
        if (lang === 'ml') {
          setLiveAnswer(
            'വയനാട്ടിലെ നിലവിലെ ഉയർന്ന അന്തരീക്ഷ ഈർപ്പവും (89%) കതിരുകൾ പൊട്ടുന്ന ഘട്ടവും കണക്കിലെടുക്കുമ്പോൾ, ട്രൈസൈക്ലാസോൾ 75% WP (ലിറ്ററിന് 0.6 ഗ്രാം) ഇന്ന് രാവിലെ 7:30 മുതൽ 10:30 നുള്ളിൽ തളിക്കാൻ ശുപാർശ ചെയ്യുന്നു. അടുത്ത 24 മണിക്കൂറിൽ മഴയ്ക്ക് 25% സാധ്യതയുള്ളതിനാൽ ഇലയുടെ അടിഭാഗം വരെ നനയുന്ന തരത്തിൽ തളിക്കുക. രോഗം പൂർണ്ണമായി മാറുന്നതുവരെ അമിതമായ യൂറിയ പ്രയോഗം ഒഴിവാക്കുക.',
          );
          setLiveWarnings(['മഴ പെയ്യാൻ സാധ്യതയുള്ളതിനാൽ സ്പ്രേ ചെയ്ത ശേഷം 2 മണിക്കൂർ മഴ പെയ്യാതിരിക്കാൻ ശ്രദ്ധിക്കുക.']);
        } else {
          setLiveAnswer(
            'Based on Wayanad’s current high relative humidity (89%) and the tillering stage, apply Tricyclazole 75% WP (0.6g per liter) today between 7:30 AM and 10:30 AM. With a 25% rain probability tomorrow, this morning window ensures proper systemic absorption. Suspend nitrogen/urea top-dressing for 7 days to avoid excess foliar succulence which exacerbates Magnaporthe oryzae.',
          );
          setLiveWarnings([
            'Ensure spray nozzles produce fine mist (<200 microns) for complete canopy penetration.',
            'CIB&RC safety notice: Maintain minimum 30 days pre-harvest interval (PHI).',
          ]);
        }
      } else if (selectedAdvisory.farmerContext.crop === 'Banana') {
        if (lang === 'ml') {
          setLiveAnswer(
            'പാലക്കാട് ചിറ്റൂരിലെ താപനിലയും കാലാവസ്ഥയും കണക്കിലെടുക്കുമ്പോൾ സിഗറ്റോക്ക ഇലപ്പുള്ളി രോഗം വേഗത്തിൽ പടരാൻ സാധ്യതയുണ്ട്. പ്രോപ്പികൊണസോൾ 25% EC (ലിറ്ററിന് 1 മി.ലി) മിനറൽ ഓയിലുമായി ചേർത്ത് നാളെ രാവിലെ തളിക്കുക. തളിക്കുന്നതിന് മുൻപ് ഏറ്റവും അടിയിലുള്ള കരിഞ്ഞ ഇലകൾ വെട്ടി തീയിട്ട് നശിപ്പിക്കുന്നത് ഫലപ്രാപ്തി 40% വർദ്ധിപ്പിക്കും.',
          );
          setLiveWarnings(['കുലയുടെ മേൽ നേരിട്ട് മരുന്ന് വീഴാതിരിക്കാൻ ശ്രദ്ധിക്കുക.']);
        } else {
          setLiveAnswer(
            'Black Sigatoka progression accelerates at temperatures above 28°C. For Nendran banana in Palakkad, apply Propiconazole 25% EC (1.0 ml/L) emulsified with 10ml agricultural spray oil. Before spraying, de-leaf and burn severely spotted lower leaves to reduce inoculum density by over 40%.',
          );
          setLiveWarnings([
            'Rotate with contact fungicide (Copper Oxychloride) after 21 days to prevent pathogen resistance.',
          ]);
        }
      } else {
        // Coconut or other
        if (lang === 'ml') {
          setLiveAnswer(
            'ആലപ്പുഴ കുട്ടനാട്ടിലെ ഈ ലക്ഷണങ്ങൾ കാറ്റുവീഴ്ചയോ അല്ലെങ്കിൽ തീവ്രമായ പൊട്ടാഷ്/മഗ്നീഷ്യം അപര്യാപ്തതയോ ആകാം. അനാവശ്യമായി രാസകുമിൾനാശിനികൾ തളിക്കരുത്. ഒരു തെങ്ങിന് 500 ഗ്രാം മഗ്നീഷ്യം സൾഫേറ്റും തുല്യമായ NPK വളവും നൽകുക. അടുത്ത 48 മണിക്കൂറിനുള്ളിൽ കൃഷി ഓഫീസറുടെ നേരിട്ടുള്ള പരിശോധന ആവശ്യമാണ്.',
          );
          setLiveWarnings(['കുമിൾനാശിനി തളിക്കുന്നത് ഫലപ്രദമല്ല; മണ്ണ് പരിശോധന നടത്തി കൃത്യമായ വളപ്രയോഗം നടത്തുക.']);
        } else {
          setLiveAnswer(
            'Foliar flaccidity in Kuttanad sandy soils closely mirrors both Phytoplasma Root Wilt and advanced Magnesium/Potassium deficiency. Do NOT apply indiscriminate chemical fungicides. Apply 500g Magnesium Sulphate (MgSO4) + Borax per palm and maintain green manuring. A physical agronomist inspection has been scheduled.',
          );
          setLiveWarnings([
            'Calibrated state UNCERTAIN: Awaiting secondary tissue review before chemical intervention.',
          ]);
        }
      }
    }, 600);
  };

  // Sample prompt chips
  const promptSuggestions = [
    {
      en: 'Should I spray fungicide before tomorrow’s rain?',
      ml: 'നാളെ മഴയ്ക്ക് സാധ്യതയുള്ളതിനാൽ ഇന്ന് മരുന്ന് തളിക്കാമോ?',
    },
    {
      en: 'What are safe organic or bio-control alternatives?',
      ml: 'ഇതിന് ജൈവ അല്ലെങ്കിൽ പ്രകൃതിദത്ത പ്രതിവിധികൾ എന്തൊക്കെയാണ്?',
    },
    {
      en: 'What is the projected economic loss if left untreated?',
      ml: 'ചികിത്സിച്ചില്ലെങ്കിൽ എത്രത്തോളം വിളനഷ്ടം ഉണ്ടാകും?',
    },
  ];

  return (
    <div className="min-h-screen bg-[var(--color-bg-base)] text-[var(--color-on-surface)]">
      {/* 1. TOP GLOBAL STUDIO COMMAND BAR */}
      <header className="sticky top-0 z-40 border-b border-[var(--color-surface-glass-border)] bg-[var(--color-surface-glass)] backdrop-blur-xl transition-all">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3 sm:px-6">
          {/* Left: Brand & Back link */}
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={() => navigate('/')}
              className="flex items-center gap-1.5 rounded-lg border border-[var(--color-outline-variant)] bg-[var(--color-surface-variant)] px-3 py-1.5 text-xs font-semibold text-[var(--color-on-surface-secondary)] transition-colors hover:border-[var(--color-primary)] hover:text-[var(--color-primary)]"
              title="Return to Main Portal"
            >
              <ArrowLeft size={14} />
              <span className="hidden sm:inline">Portal Home</span>
            </button>

            <div className="h-5 w-px bg-[var(--color-outline-variant)]" />

            <div>
              <div className="flex items-center gap-2">
                <span className="flex h-2.5 w-2.5 rounded-full bg-[var(--color-primary)] animate-pulse" />
                <h1 className="text-sm font-extrabold tracking-tight text-[var(--color-on-surface)] sm:text-base">
                  Agri-SAGE Studio
                </h1>
                <span className="hidden rounded-md bg-[var(--color-primary-container)] px-2 py-0.5 text-[10px] font-bold text-[var(--color-primary)] sm:inline-block">
                  v2.5 Hybrid Workbench
                </span>
              </div>
              <p className="text-[11px] text-[var(--color-on-surface-secondary)]">
                Field Diagnostic Quality Gate & Gemini Advisory Simulator
              </p>
            </div>
          </div>

          {/* Right: Mode Switcher, Language & Auth Status */}
          <div className="flex items-center gap-2 sm:gap-3">
            {/* View Mode Toggle: Workbench vs Mobile */}
            <div className="flex rounded-lg border border-[var(--color-outline-variant)] bg-[var(--color-surface-variant)] p-1 text-xs font-semibold">
              <button
                type="button"
                onClick={() => setViewMode('workbench')}
                className={`flex items-center gap-1.5 rounded-md px-3 py-1 transition-all ${
                  viewMode === 'workbench'
                    ? 'bg-[var(--color-primary)] text-white shadow-xs'
                    : 'text-[var(--color-on-surface-secondary)] hover:text-[var(--color-on-surface)]'
                }`}
                title="Full Desktop Diagnostic Workbench"
              >
                <Monitor size={14} />
                <span className="hidden md:inline">Studio Workbench</span>
                <span className="md:hidden">Studio</span>
              </button>
              <button
                type="button"
                onClick={() => setViewMode('mobile')}
                className={`flex items-center gap-1.5 rounded-md px-3 py-1 transition-all ${
                  viewMode === 'mobile'
                    ? 'bg-[var(--color-primary)] text-white shadow-xs'
                    : 'text-[var(--color-on-surface-secondary)] hover:text-[var(--color-on-surface)]'
                }`}
                title="Farmer Smartphone Device Emulator"
              >
                <Smartphone size={14} />
                <span className="hidden md:inline">Mobile Preview</span>
                <span className="md:hidden">Mobile</span>
              </button>
            </div>

            {/* Language Switcher */}
            <button
              type="button"
              onClick={onToggleLang}
              className="rounded-lg border border-[var(--color-outline-variant)] bg-[var(--color-surface-variant)] px-2.5 py-1.5 text-xs font-bold text-[var(--color-on-surface)] transition-all hover:border-[var(--color-primary)]"
              title="Toggle Language"
            >
              {lang === 'ml' ? 'ENG' : 'മലയാളം'}
            </button>

            {/* Auth / Live Backend Pill */}
            {accessToken ? (
              <span className="hidden items-center gap-1.5 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-2.5 py-1 text-[11px] font-bold text-emerald-400 sm:flex">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-ping" />
                Live Gemini Connected
              </span>
            ) : (
              <Link
                to="/auth?mode=login"
                className="hidden items-center gap-1.5 rounded-full border border-amber-500/30 bg-amber-500/10 px-2.5 py-1 text-[11px] font-bold text-amber-400 transition hover:bg-amber-500/20 sm:flex"
                title="Click to sign in with live credentials"
              >
                <span className="h-1.5 w-1.5 rounded-full bg-amber-400" />
                Demo Mode • Sign In
              </Link>
            )}
          </div>
        </div>
      </header>

      {/* 2. CROP CASE STUDY SELECTOR BAR */}
      <section className="border-b border-[var(--color-surface-glass-border)] bg-[var(--color-surface)]/60 px-4 py-3">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-bold uppercase tracking-wider text-[var(--color-on-surface-tertiary)]">
              Select Field Specimen Case:
            </span>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            {SEED_ADVISORIES.map((adv) => {
              const isSelected = selectedAdvisory.id === adv.id;
              return (
                <button
                  key={adv.id}
                  type="button"
                  onClick={() => handleSelectCrop(adv)}
                  className={`group flex items-center gap-2.5 rounded-xl border px-3 py-2 text-left text-xs transition-all ${
                    isSelected
                      ? 'border-[var(--color-primary)] bg-[var(--color-primary-light)] ring-1 ring-[var(--color-primary)]'
                      : 'border-[var(--color-outline-variant)] bg-[var(--color-surface-variant)] hover:border-[var(--color-outline)]'
                  }`}
                >
                  <div
                    className={`flex h-7 w-7 items-center justify-center rounded-lg text-sm font-bold ${
                      isSelected
                        ? 'bg-[var(--color-primary)] text-white'
                        : 'bg-[var(--color-surface)] text-[var(--color-on-surface-secondary)] group-hover:text-[var(--color-on-surface)]'
                    }`}
                  >
                    {adv.farmerContext.crop === 'Rice' && '🌾'}
                    {adv.farmerContext.crop === 'Banana' && '🍌'}
                    {adv.farmerContext.crop === 'Coconut' && '🥥'}
                  </div>
                  <div>
                    <strong className="block text-xs font-bold text-[var(--color-on-surface)]">
                      {adv.farmerContext.crop}: {lang === 'ml' ? adv.diagnosisNameMl : adv.diagnosisNameEn.split('(')[0]}
                    </strong>
                    <span className="text-[10px] text-[var(--color-on-surface-secondary)]">
                      {adv.farmerContext.village}, {adv.farmerContext.district} • {adv.confidence}
                    </span>
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      </section>

      {/* 3. MAIN CONTENT: WORKBENCH OR MOBILE VIEW */}
      <main className="mx-auto max-w-7xl p-4 sm:p-6">
        {viewMode === 'workbench' ? (
          /* ============================================================ */
          /* MODE A: FULL STUDIO WORKBENCH (DESKTOP / TABLET ERGONOMIC)  */
          /* ============================================================ */
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-12 items-start">
            {/* LEFT COLUMN: SPECIMEN LAB & LIVE GEMINI ADVISORY BRIDGE (5 cols) */}
            <div className="space-y-6 lg:col-span-5">
              {/* Card 1: Interactive Specimen & Vision Viewfinder */}
              <div className="glass-panel overflow-hidden p-5">
                <div className="flex items-center justify-between pb-3 border-b border-[var(--color-outline-variant)]">
                  <div className="flex items-center gap-2">
                    <Camera size={18} className="text-[var(--color-primary)]" />
                    <h2 className="text-sm font-bold text-[var(--color-on-surface)]">
                      Foliage Specimen & Edge CV Gate
                    </h2>
                  </div>
                  <span
                    className={`rounded-full px-2 py-0.5 text-[10px] font-mono font-bold uppercase tracking-wider ${
                      isCameraQualityAcceptable
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                        : 'bg-red-500/10 text-red-400 border border-red-500/30'
                    }`}
                  >
                    {isCameraQualityAcceptable ? '✓ Quality Gate: PASS' : '⚠ Quality Gate: REJECT'}
                  </span>
                </div>

                {/* Viewfinder Canvas */}
                <div className="relative mt-4 aspect-[4/3] w-full overflow-hidden rounded-xl border border-[var(--color-outline-variant)] bg-black shadow-inner">
                  <SafeImage
                    src={selectedAdvisory.imageUrl}
                    alt={selectedAdvisory.diagnosisNameEn}
                    style={{
                      filter: `blur(${Math.max(0, (100 - blurValue) / 12)}px) brightness(${brightnessValue / 130})`,
                      transform: `scale(${Math.max(0.7, framingValue / 85)})`,
                    }}
                    className="h-full w-full object-cover select-none transition-all duration-200"
                  />

                  {/* Diagnostic Bounding Box */}
                  <div className="absolute inset-8 rounded-lg border-2 border-dashed border-emerald-400/80 pointer-events-none flex items-start justify-between p-2">
                    <span className="rounded bg-black/70 px-1.5 py-0.5 text-[9px] font-mono font-bold text-emerald-300 backdrop-blur-xs">
                      ROI: {selectedAdvisory.diseaseCode}
                    </span>
                    <span className="rounded bg-black/70 px-1.5 py-0.5 text-[9px] font-mono font-bold text-white/90 backdrop-blur-xs">
                      5 FPS Edge Telemetry
                    </span>
                  </div>

                  {/* Realtime Quality Bar Header */}
                  <div className="absolute top-2 inset-x-2 rounded-lg bg-black/75 p-2 backdrop-blur-md border border-white/10">
                    <RealtimeQualityBar
                      blurVariance={blurValue}
                      brightnessLevel={brightnessValue}
                      cropCoveragePct={framingValue}
                      lang={lang}
                    />
                  </div>
                </div>

                {/* Preset Testing Buttons */}
                <div className="mt-4">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-[var(--color-on-surface-tertiary)] block mb-2">
                    Test Edge-CV Quality Conditions:
                  </span>
                  <div className="grid grid-cols-2 gap-2 text-xs sm:grid-cols-4">
                    <button
                      type="button"
                      onClick={() => applyPreset('optimal')}
                      className="rounded-lg border border-emerald-500/30 bg-emerald-500/10 px-2 py-1.5 text-center font-semibold text-emerald-400 hover:bg-emerald-500/20 transition"
                    >
                      ✨ Optimal
                    </button>
                    <button
                      type="button"
                      onClick={() => applyPreset('blur')}
                      className="rounded-lg border border-red-500/30 bg-red-500/10 px-2 py-1.5 text-center font-semibold text-red-400 hover:bg-red-500/20 transition"
                    >
                      🌫 Blur Defect
                    </button>
                    <button
                      type="button"
                      onClick={() => applyPreset('glare')}
                      className="rounded-lg border border-amber-500/30 bg-amber-500/10 px-2 py-1.5 text-center font-semibold text-amber-400 hover:bg-amber-500/20 transition"
                    >
                      ☀️ High Glare
                    </button>
                    <button
                      type="button"
                      onClick={() => applyPreset('framing')}
                      className="rounded-lg border border-purple-500/30 bg-purple-500/10 px-2 py-1.5 text-center font-semibold text-purple-400 hover:bg-purple-500/20 transition"
                    >
                      📐 Too Far
                    </button>
                  </div>
                </div>

                {/* Manual Sliders */}
                <div className="mt-4 space-y-3 pt-3 border-t border-[var(--color-outline-variant)]">
                  {/* Slider 1: Blur */}
                  <div>
                    <div className="flex justify-between text-xs mb-1">
                      <label htmlFor="workbench-blur" className="font-semibold text-[var(--color-on-surface)]">
                        Laplacian Focus Variance:
                      </label>
                      <span className={`font-mono font-bold ${blurValue < 100 ? 'text-red-400' : 'text-emerald-400'}`}>
                        {blurValue} / 200 {blurValue < 100 ? '(Blurry)' : '(Sharp)'}
                      </span>
                    </div>
                    <input
                      id="workbench-blur"
                      type="range"
                      min="20"
                      max="200"
                      value={blurValue}
                      onChange={(e) => setBlurValue(Number(e.target.value))}
                      className="w-full accent-[var(--color-primary)] cursor-pointer"
                    />
                  </div>

                  {/* Slider 2: Brightness */}
                  <div>
                    <div className="flex justify-between text-xs mb-1">
                      <label htmlFor="workbench-brightness" className="font-semibold text-[var(--color-on-surface)]">
                        Ambient Lux & Solar Exposure:
                      </label>
                      <span
                        className={`font-mono font-bold ${
                          brightnessValue < 60 || brightnessValue > 220 ? 'text-red-400' : 'text-emerald-400'
                        }`}
                      >
                        {brightnessValue} / 255{' '}
                        {brightnessValue < 60 ? '(Dark)' : brightnessValue > 220 ? '(Overexposed)' : '(Balanced)'}
                      </span>
                    </div>
                    <input
                      id="workbench-brightness"
                      type="range"
                      min="20"
                      max="255"
                      value={brightnessValue}
                      onChange={(e) => setBrightnessValue(Number(e.target.value))}
                      className="w-full accent-[var(--color-primary)] cursor-pointer"
                    />
                  </div>

                  {/* Slider 3: Foliage Framing */}
                  <div>
                    <div className="flex justify-between text-xs mb-1">
                      <label htmlFor="workbench-framing" className="font-semibold text-[var(--color-on-surface)]">
                        Target Canopy Framing:
                      </label>
                      <span className={`font-mono font-bold ${framingValue < 30 ? 'text-amber-400' : 'text-emerald-400'}`}>
                        {framingValue}% {framingValue < 30 ? '(Too Far)' : '(Optimal)'}
                      </span>
                    </div>
                    <input
                      id="workbench-framing"
                      type="range"
                      min="10"
                      max="100"
                      value={framingValue}
                      onChange={(e) => setFramingValue(Number(e.target.value))}
                      className="w-full accent-[var(--color-primary)] cursor-pointer"
                    />
                  </div>
                </div>
              </div>

              {/* Card 2: Live AI Advisory Bridge (Gemini 2.5 Flash) */}
              <div className="glass-panel p-5">
                <div className="flex items-center justify-between pb-3 border-b border-[var(--color-outline-variant)]">
                  <div className="flex items-center gap-2">
                    <Sparkles size={18} className="text-[var(--color-primary)]" />
                    <h2 className="text-sm font-bold text-[var(--color-on-surface)]">
                      Live AI Agronomic Advisory
                    </h2>
                  </div>
                  <span className="rounded-full bg-[var(--color-primary-container)] px-2 py-0.5 text-[10px] font-bold text-[var(--color-primary)]">
                    Gemini 2.5 Flash
                  </span>
                </div>

                <p className="mt-2 text-xs text-[var(--color-on-surface-secondary)] leading-relaxed">
                  Ask conversational field questions grounded in current crop stage (
                  <strong className="text-[var(--color-on-surface)]">{selectedAdvisory.farmerContext.estimatedGrowthStage}</strong>
                  ) and local weather metrics.
                </p>

                {/* Prompt Suggestions */}
                <div className="mt-3 flex flex-wrap gap-1.5">
                  {promptSuggestions.map((s, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => handleAskAgriSage(lang === 'ml' ? s.ml : s.en)}
                      className="rounded-lg border border-[var(--color-outline-variant)] bg-[var(--color-surface-variant)] px-2.5 py-1 text-[11px] text-[var(--color-on-surface-secondary)] hover:border-[var(--color-primary)] hover:text-[var(--color-on-surface)] transition text-left"
                    >
                      💬 {lang === 'ml' ? s.ml : s.en}
                    </button>
                  ))}
                </div>

                {/* Question Input */}
                <div className="mt-3 flex gap-2">
                  <input
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleAskAgriSage()}
                    placeholder={
                      lang === 'ml'
                        ? 'വിളയെക്കുറിച്ചുള്ള ചോദ്യം ചോദിക്കുക...'
                        : `Ask about this ${selectedAdvisory.farmerContext.crop}...`
                    }
                    className="min-h-11 flex-1 rounded-xl border border-[var(--color-outline)] bg-[var(--color-surface)] px-4 text-xs text-[var(--color-on-surface)] outline-none transition focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)]"
                    disabled={isAsking}
                  />
                  <button
                    type="button"
                    onClick={() => handleAskAgriSage()}
                    disabled={!question.trim() || isAsking}
                    className="btn btn-primary px-4 text-xs font-bold shrink-0"
                  >
                    {isAsking ? (
                      <span className="flex items-center gap-1.5">
                        <RotateCcw size={14} className="animate-spin" />
                        Thinking...
                      </span>
                    ) : (
                      <span className="flex items-center gap-1.5">
                        <Send size={14} />
                        Ask
                      </span>
                    )}
                  </button>
                </div>

                {liveError && (
                  <div className="mt-3 rounded-lg border border-red-500/30 bg-red-500/10 p-3 text-xs text-red-400">
                    {liveError}
                  </div>
                )}

                {/* Live Answer Box */}
                {liveAnswer && (
                  <div className="mt-4 rounded-xl border border-[var(--color-primary)]/40 bg-[var(--color-primary-light)] p-4 shadow-sm animate-fade-in">
                    <div className="flex items-center justify-between pb-2 mb-2 border-b border-[var(--color-primary)]/20">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-primary)] flex items-center gap-1">
                        <Sparkles size={12} />
                        {isLiveResultFromBackend ? 'Gemini 2.5 Live Response' : 'Agri-SAGE Grounded Advisory'}
                      </span>
                      <span className="text-[10px] text-[var(--color-on-surface-tertiary)] font-mono">
                        Confidence: {(selectedAdvisory.confidenceScore * 100).toFixed(0)}%
                      </span>
                    </div>

                    <p className="text-xs leading-relaxed text-[var(--color-on-surface)]">
                      {liveAnswer}
                    </p>

                    {liveWarnings.length > 0 && (
                      <div className="mt-3 rounded-lg bg-amber-500/10 border border-amber-500/20 p-2.5">
                        <span className="text-[10px] font-bold uppercase tracking-wider text-amber-400 block mb-1">
                          Field Precautions & Warnings:
                        </span>
                        <ul className="list-disc pl-4 space-y-1 text-[11px] text-amber-300/90">
                          {liveWarnings.map((warning, wIdx) => (
                            <li key={wIdx}>{warning}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>

            {/* RIGHT COLUMN: AGRONOMIC PROTOCOL & DSSAT SCENARIOS (7 cols) */}
            <div className="space-y-6 lg:col-span-7">
              {/* Active Diagnosis Overview Banner */}
              <div className="glass-panel p-5">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <ConfidenceBadge
                        state={selectedAdvisory.confidence}
                        score={selectedAdvisory.confidenceScore}
                      />
                      <RiskBadge level={selectedAdvisory.severityRisk} />
                    </div>
                    <h2 className="text-xl font-extrabold text-[var(--color-on-surface)] leading-tight">
                      {lang === 'ml' ? selectedAdvisory.diagnosisNameMl : selectedAdvisory.diagnosisNameEn}
                    </h2>
                    <p className="text-xs text-[var(--color-on-surface-secondary)] mt-0.5">
                      {lang === 'ml' ? selectedAdvisory.diagnosisNameEn : selectedAdvisory.diagnosisNameMl}
                      {selectedAdvisory.pronunciationMl && (
                        <span className="ml-2 font-mono text-[11px] text-[var(--color-primary)]">
                          [{selectedAdvisory.pronunciationMl}]
                        </span>
                      )}
                    </p>
                  </div>

                  {/* Quick Farmer Context Pill */}
                  <div className="rounded-xl border border-[var(--color-outline-variant)] bg-[var(--color-surface-variant)] p-3 text-right text-xs">
                    <span className="text-[10px] uppercase font-bold text-[var(--color-on-surface-tertiary)] block">
                      Farmer & Plot
                    </span>
                    <strong className="text-xs text-[var(--color-on-surface)] block">
                      {selectedAdvisory.farmerContext.farmerName}
                    </strong>
                    <span className="text-[11px] text-[var(--color-on-surface-secondary)]">
                      {selectedAdvisory.farmerContext.cultivar} • {selectedAdvisory.farmerContext.farmAreaHa} Ha
                    </span>
                  </div>
                </div>

                {/* Weather & Microclimate Telemetry Bar */}
                <div className="mt-4 grid grid-cols-2 gap-2 rounded-xl border border-[var(--color-outline-variant)] bg-[var(--color-surface-variant)]/60 p-3 sm:grid-cols-4 text-xs">
                  <div className="flex items-center gap-2">
                    <Thermometer size={16} className="text-amber-400 shrink-0" />
                    <div>
                      <span className="text-[10px] text-[var(--color-on-surface-tertiary)] block">Ambient Temp</span>
                      <strong className="font-mono text-xs">{selectedAdvisory.weatherIndicators.temperatureC}°C</strong>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Droplets size={16} className="text-cyan-400 shrink-0" />
                    <div>
                      <span className="text-[10px] text-[var(--color-on-surface-tertiary)] block">Rel. Humidity</span>
                      <strong className="font-mono text-xs">{selectedAdvisory.weatherIndicators.humidityPct}%</strong>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <CloudRain size={16} className="text-blue-400 shrink-0" />
                    <div>
                      <span className="text-[10px] text-[var(--color-on-surface-tertiary)] block">Rain 24h Risk</span>
                      <strong className="font-mono text-xs">{selectedAdvisory.weatherIndicators.rainForecastNext24hPct}%</strong>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Zap size={16} className="text-red-400 shrink-0" />
                    <div>
                      <span className="text-[10px] text-[var(--color-on-surface-tertiary)] block">Pathogen Index</span>
                      <strong className="font-mono text-xs text-red-400">
                        {(selectedAdvisory.weatherIndicators.diseaseFavorabilityIndex * 100).toFixed(0)}% High
                      </strong>
                    </div>
                  </div>
                </div>
              </div>

              {/* Protocol Segmented Tab Strip */}
              <div className="flex rounded-xl border border-[var(--color-outline-variant)] bg-[var(--color-surface-variant)] p-1 text-xs font-semibold">
                <button
                  type="button"
                  onClick={() => setActiveTab('PROTOCOL')}
                  className={`flex flex-1 items-center justify-center gap-1.5 rounded-lg py-2 transition-all ${
                    activeTab === 'PROTOCOL'
                      ? 'bg-[var(--color-primary)] text-white shadow-xs'
                      : 'text-[var(--color-on-surface-secondary)] hover:text-[var(--color-on-surface)]'
                  }`}
                >
                  <ShieldCheck size={14} />
                  <span>1. Action Plan</span>
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab('SCENARIOS')}
                  className={`flex flex-1 items-center justify-center gap-1.5 rounded-lg py-2 transition-all ${
                    activeTab === 'SCENARIOS'
                      ? 'bg-[var(--color-primary)] text-white shadow-xs'
                      : 'text-[var(--color-on-surface-secondary)] hover:text-[var(--color-on-surface)]'
                  }`}
                >
                  <Layers size={14} />
                  <span>2. DSSAT Scenarios</span>
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab('EVIDENCE')}
                  className={`flex flex-1 items-center justify-center gap-1.5 rounded-lg py-2 transition-all ${
                    activeTab === 'EVIDENCE'
                      ? 'bg-[var(--color-primary)] text-white shadow-xs'
                      : 'text-[var(--color-on-surface-secondary)] hover:text-[var(--color-on-surface)]'
                  }`}
                >
                  <Info size={14} />
                  <span>3. Scientific Evidence</span>
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab('SCHEMES')}
                  className={`flex flex-1 items-center justify-center gap-1.5 rounded-lg py-2 transition-all ${
                    activeTab === 'SCHEMES'
                      ? 'bg-[var(--color-primary)] text-white shadow-xs'
                      : 'text-[var(--color-on-surface-secondary)] hover:text-[var(--color-on-surface)]'
                  }`}
                >
                  <DollarSign size={14} />
                  <span>4. Govt Schemes</span>
                </button>
              </div>

              {/* TAB 1: IMMEDIATE ACTION PLAN */}
              {activeTab === 'PROTOCOL' && (
                <div className="space-y-4 animate-fade-in">
                  <div className="glass-panel p-5 space-y-4">
                    {/* Primary Action Box */}
                    <div className="rounded-xl border border-[var(--color-primary)]/50 bg-[var(--color-primary-light)] p-4">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-primary)] block mb-1">
                        {lang === 'ml' ? 'നിർദ്ദിഷ്ട പരിഹാരം (What To Do)' : 'Primary Agronomic Prescription'}
                      </span>
                      <strong className="text-base font-bold text-[var(--color-on-surface)] block">
                        {lang === 'ml' ? selectedAdvisory.actionPlan.whatMl : selectedAdvisory.actionPlan.what}
                      </strong>
                    </div>

                    {/* When & Spray Window */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                      <div className="rounded-xl border border-[var(--color-outline-variant)] bg-[var(--color-surface-variant)] p-3">
                        <span className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-on-surface-tertiary)] block mb-1 flex items-center gap-1">
                          <Clock size={12} className="text-emerald-400" />
                          {lang === 'ml' ? 'എപ്പോൾ ചെയ്യണം' : 'Application Window'}
                        </span>
                        <p className="font-semibold text-[var(--color-on-surface)]">
                          {lang === 'ml' ? selectedAdvisory.actionPlan.whenMl : selectedAdvisory.actionPlan.when}
                        </p>
                        {selectedAdvisory.actionPlan.sprayWindow && (
                          <span className="inline-block mt-2 rounded bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 text-[11px] font-mono text-emerald-400">
                            Optimal Spray: {selectedAdvisory.actionPlan.sprayWindow.startTime} - {selectedAdvisory.actionPlan.sprayWindow.endTime}
                          </span>
                        )}
                      </div>

                      {/* Economics & Cost */}
                      <div className="rounded-xl border border-[var(--color-outline-variant)] bg-[var(--color-surface-variant)] p-3">
                        <span className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-on-surface-tertiary)] block mb-1">
                          Estimated Cost Per Acre
                        </span>
                        <p className="text-base font-extrabold font-mono text-[var(--color-primary)]">
                          ₹{selectedAdvisory.actionPlan.costEstimate.minInr} – ₹{selectedAdvisory.actionPlan.costEstimate.maxInr}
                        </p>
                        <span className="text-[10px] text-[var(--color-on-surface-secondary)]">
                          Includes active chemical and labor application estimate
                        </span>
                      </div>
                    </div>

                    {/* How to Apply */}
                    <div className="rounded-xl border border-[var(--color-outline-variant)] bg-[var(--color-surface-variant)] p-4 text-xs space-y-2">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-on-surface-tertiary)] block">
                        {lang === 'ml' ? 'തളിക്കേണ്ട രീതി' : 'Standard Operating Procedure (How to Apply)'}
                      </span>
                      <p className="leading-relaxed text-[var(--color-on-surface-secondary)]">
                        {lang === 'ml' ? selectedAdvisory.actionPlan.howMl : selectedAdvisory.actionPlan.how}
                      </p>
                    </div>

                    {/* Chemical & Biological Safety Standards */}
                    {selectedAdvisory.actionPlan.chemicalSafety && (
                      <div className="rounded-xl border border-cyan-500/20 bg-cyan-500/5 p-4 text-xs space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="text-[10px] font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-1">
                            <ShieldCheck size={13} />
                            CIB&RC Registered Safety Specification
                          </span>
                          <span className="rounded bg-cyan-500/20 px-1.5 py-0.5 text-[10px] font-mono font-bold text-cyan-300">
                            {selectedAdvisory.actionPlan.chemicalSafety.cibrcStatus}
                          </span>
                        </div>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px] pt-1">
                          <div>
                            <span className="text-[var(--color-on-surface-tertiary)]">Active Molecule: </span>
                            <span className="font-semibold">{selectedAdvisory.actionPlan.chemicalSafety.activeIngredient}</span>
                          </div>
                          <div>
                            <span className="text-[var(--color-on-surface-tertiary)]">Dosage Rate: </span>
                            <span className="font-semibold font-mono">{selectedAdvisory.actionPlan.chemicalSafety.dosagePerLiter}</span>
                          </div>
                          <div>
                            <span className="text-[var(--color-on-surface-tertiary)]">Registration: </span>
                            <span className="font-mono text-[10px]">{selectedAdvisory.actionPlan.chemicalSafety.cibrcRegNumber}</span>
                          </div>
                          <div>
                            <span className="text-[var(--color-on-surface-tertiary)]">Brand Reference: </span>
                            <span className="font-semibold">{selectedAdvisory.actionPlan.chemicalSafety.commercialBrand}</span>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* TAB 2: DSSAT SCENARIOS */}
              {activeTab === 'SCENARIOS' && (
                <div className="glass-panel p-5 animate-fade-in">
                  <ScenarioCard scenarios={selectedAdvisory.scenarios} lang={lang} />
                </div>
              )}

              {/* TAB 3: SCIENTIFIC EVIDENCE */}
              {activeTab === 'EVIDENCE' && (
                <div className="glass-panel p-5 animate-fade-in">
                  <EvidenceCard evidenceList={selectedAdvisory.evidenceBundle} lang={lang} />
                </div>
              )}

              {/* TAB 4: GOVERNMENT SCHEMES */}
              {activeTab === 'SCHEMES' && (
                <div className="glass-panel p-5 animate-fade-in">
                  {selectedAdvisory.schemesMatched.length > 0 ? (
                    <SchemeCard schemes={selectedAdvisory.schemesMatched} lang={lang} />
                  ) : (
                    <div className="text-center py-8 text-xs text-[var(--color-on-surface-secondary)]">
                      <p>No localized emergency subsidy schemes currently matched for this crop stage.</p>
                      <p className="mt-1 text-[11px] text-[var(--color-on-surface-tertiary)]">
                        Standard PMFBY yield-loss cover remains applicable through district agrarian banks.
                      </p>
                    </div>
                  )}
                </div>
              )}

              {/* Bottom Advisory Feedback */}
              <div className="glass-panel p-4 flex items-center justify-between flex-wrap gap-3">
                <span className="text-xs font-semibold text-[var(--color-on-surface)]">
                  {lang === 'ml' ? 'ഈ പരിശോധനാ ഫലം തൃപ്തികരമാണോ?' : 'Was this diagnostic recommendation accurate and actionable?'}
                </span>
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => setFeedback('helpful')}
                    className={`flex items-center gap-1.5 rounded-lg border px-3 py-1.5 text-xs font-semibold transition ${
                      feedback === 'helpful'
                        ? 'border-emerald-500 bg-emerald-500/20 text-emerald-400'
                        : 'border-[var(--color-outline-variant)] bg-[var(--color-surface-variant)] text-[var(--color-on-surface-secondary)] hover:text-emerald-400'
                    }`}
                  >
                    <ThumbsUp size={14} />
                    <span>Helpful</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setFeedback('not-helpful')}
                    className={`flex items-center gap-1.5 rounded-lg border px-3 py-1.5 text-xs font-semibold transition ${
                      feedback === 'not-helpful'
                        ? 'border-red-500 bg-red-500/20 text-red-400'
                        : 'border-[var(--color-outline-variant)] bg-[var(--color-surface-variant)] text-[var(--color-on-surface-secondary)] hover:text-red-400'
                    }`}
                  >
                    <ThumbsDown size={14} />
                    <span>Review Needed</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        ) : (
          /* ============================================================ */
          /* MODE B: FLAGSHIP MOBILE DEVICE PREVIEW (SMARTPHONE SIMULATOR) */
          /* ============================================================ */
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-12 items-start justify-center">
            {/* Center: Smartphone Frame (6 cols) */}
            <div className="flex justify-center lg:col-span-6">
              <div className="relative flex min-h-[760px] w-full max-w-[390px] flex-col overflow-hidden rounded-[44px] border-[10px] border-slate-900 bg-[var(--color-surface)] shadow-2xl">
                {/* Dynamic Island / Speaker Notch */}
                <div className="flex h-7 w-full shrink-0 items-center justify-center bg-slate-900">
                  <div className="h-4 w-24 rounded-full bg-black flex items-center justify-center">
                    <span className="h-1.5 w-1.5 rounded-full bg-slate-800" />
                  </div>
                </div>

                {/* Mobile Top App Bar */}
                <div className="flex h-14 shrink-0 items-center justify-between bg-[var(--color-primary-dark)] px-4 text-white shadow-sm">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-bold tracking-wide">Agri-SAGE</span>
                    <span className="rounded bg-white/20 px-1.5 py-0.5 font-mono text-[10px]">
                      {selectedAdvisory.farmerContext.village}
                    </span>
                  </div>

                  <button
                    type="button"
                    onClick={onToggleLang}
                    className="rounded bg-white/15 px-2 py-0.5 text-[11px] font-bold hover:bg-white/30"
                  >
                    {lang === 'ml' ? 'ENG' : 'മലയാളം'}
                  </button>
                </div>

                {/* Mobile Scrollable Viewport */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4">
                  {/* SCREEN 1: MORNING BRIEFING */}
                  {activeMobileScreen === 'HOME' && (
                    <div className="space-y-4 animate-fade-in">
                      <MorningBriefingCard
                        farmerName={selectedAdvisory.farmerContext.farmerName}
                        cropName={selectedAdvisory.farmerContext.crop}
                        stageName={selectedAdvisory.farmerContext.estimatedGrowthStage}
                        topRisk={selectedAdvisory.diagnosisNameEn}
                        weatherSummary={`${selectedAdvisory.weatherIndicators.temperatureC}°C, Humidity ${selectedAdvisory.weatherIndicators.humidityPct}%`}
                        sprayWindowSummary={
                          selectedAdvisory.actionPlan.sprayWindow?.isOptimalToday
                            ? `${selectedAdvisory.actionPlan.sprayWindow.startTime} - ${selectedAdvisory.actionPlan.sprayWindow.endTime}`
                            : 'Rain Risk'
                        }
                        primaryAction={selectedAdvisory.actionPlan.what}
                        primaryActionMl={selectedAdvisory.actionPlan.whatMl}
                        lang={lang}
                      />

                      <div className="grid grid-cols-2 gap-3 text-xs">
                        <button
                          type="button"
                          onClick={() => setActiveMobileScreen('CAMERA')}
                          className="flex h-24 flex-col justify-between rounded-xl border border-[var(--color-outline-variant)] bg-[var(--color-surface-variant)] p-3.5 text-left transition hover:border-[var(--color-primary)]"
                        >
                          <Camera size={22} className="text-[var(--color-primary)]" />
                          <div>
                            <strong className="block text-xs font-bold text-[var(--color-on-surface)]">
                              {lang === 'ml' ? 'വിള പരിശോധിക്കുക' : 'Scan Foliage'}
                            </strong>
                            <span className="text-[10px] text-[var(--color-on-surface-tertiary)]">
                              Camera CV Gate
                            </span>
                          </div>
                        </button>

                        <button
                          type="button"
                          onClick={() => setActiveMobileScreen('ADVISORY')}
                          className="flex h-24 flex-col justify-between rounded-xl border border-[var(--color-outline-variant)] bg-[var(--color-surface-variant)] p-3.5 text-left transition hover:border-[var(--color-primary)]"
                        >
                          <Layers size={22} className="text-cyan-400" />
                          <div>
                            <strong className="block text-xs font-bold text-[var(--color-on-surface)]">
                              {lang === 'ml' ? 'അവസാന ഉപദേശം' : 'Latest Advisory'}
                            </strong>
                            <span className="text-[10px] text-[var(--color-on-surface-tertiary)]">
                              View Protocol
                            </span>
                          </div>
                        </button>
                      </div>
                    </div>
                  )}

                  {/* SCREEN 2: CAMERA QUALITY GATE */}
                  {activeMobileScreen === 'CAMERA' && (
                    <div className="space-y-4 animate-fade-in">
                      <div className="relative aspect-[4/3] w-full overflow-hidden rounded-2xl border-2 border-[var(--color-outline)] bg-black">
                        <SafeImage
                          src={selectedAdvisory.imageUrl}
                          alt="Crop Preview"
                          style={{
                            filter: `blur(${Math.max(0, (100 - blurValue) / 15)}px) brightness(${brightnessValue / 130})`,
                          }}
                          className="h-full w-full object-cover select-none"
                        />

                        {/* Framing Reticle */}
                        <div className="absolute inset-4 rounded-xl border-2 border-dashed border-white/60 pointer-events-none flex items-center justify-center">
                          <span className="rounded bg-black/50 px-2 py-0.5 text-[10px] font-mono text-white/80">
                            Aim at Affected Leaf Area
                          </span>
                        </div>

                        {/* Top Quality HUD */}
                        <div className="absolute top-2 inset-x-2 rounded-xl bg-black/75 p-2 backdrop-blur-xs border border-white/20">
                          <RealtimeQualityBar
                            blurVariance={blurValue}
                            brightnessLevel={brightnessValue}
                            cropCoveragePct={framingValue}
                            lang={lang}
                          />
                        </div>
                      </div>

                      <button
                        type="button"
                        disabled={!isCameraQualityAcceptable}
                        onClick={() => setActiveMobileScreen('ADVISORY')}
                        className={`btn w-full h-12 text-xs font-bold flex items-center justify-center gap-2 ${
                          isCameraQualityAcceptable
                            ? 'btn-primary'
                            : 'bg-gray-700 text-gray-400 cursor-not-allowed border border-gray-600'
                        }`}
                      >
                        <Camera size={18} />
                        <span>
                          {isCameraQualityAcceptable
                            ? lang === 'ml'
                              ? 'ഫോട്ടോ പരിശോധിക്കുക'
                              : 'Capture & Analyze Foliage'
                            : lang === 'ml'
                            ? 'വ്യക്തത പോരാ — ക്രമീകരിക്കുക'
                            : 'Adjust Camera Quality to Proceed'}
                        </span>
                      </button>
                    </div>
                  )}

                  {/* SCREEN 3: ADVISORY RESULT */}
                  {activeMobileScreen === 'ADVISORY' && (
                    <div className="space-y-4 animate-fade-in text-xs">
                      {/* Diagnostic Badges */}
                      <div className="rounded-xl border border-[var(--color-outline-variant)] bg-[var(--color-surface-variant)] p-3.5 space-y-2">
                        <div className="flex items-center justify-between">
                          <ConfidenceBadge
                            state={selectedAdvisory.confidence}
                            score={selectedAdvisory.confidenceScore}
                          />
                          <RiskBadge level={selectedAdvisory.severityRisk} />
                        </div>
                        <h3 className="text-base font-bold text-[var(--color-on-surface)] leading-snug">
                          {lang === 'ml' ? selectedAdvisory.diagnosisNameMl : selectedAdvisory.diagnosisNameEn}
                        </h3>
                      </div>

                      {/* Action Plan */}
                      <div className="rounded-xl border-2 border-[var(--color-primary)] bg-[var(--color-primary-light)] p-3.5 space-y-2.5">
                        <span className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-primary)] block">
                          {lang === 'ml' ? 'എന്ത് ചെയ്യണം' : 'What To Do'}
                        </span>
                        <strong className="text-xs font-bold text-[var(--color-on-surface)] block">
                          {lang === 'ml' ? selectedAdvisory.actionPlan.whatMl : selectedAdvisory.actionPlan.what}
                        </strong>

                        <div className="pt-2 border-t border-[var(--color-primary-container)]">
                          <span className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-primary)] block">
                            {lang === 'ml' ? 'എപ്പോൾ ചെയ്യണം' : 'Optimal Timing'}
                          </span>
                          <p className="text-[11px] font-semibold text-[var(--color-on-surface)]">
                            {lang === 'ml' ? selectedAdvisory.actionPlan.whenMl : selectedAdvisory.actionPlan.when}
                          </p>
                        </div>
                      </div>

                      {/* Evidence Card */}
                      <EvidenceCard evidenceList={selectedAdvisory.evidenceBundle} lang={lang} />
                    </div>
                  )}
                </div>

                {/* Mobile Bottom Navigation Bar */}
                <div className="flex h-14 shrink-0 items-center justify-around border-t border-[var(--color-outline-variant)] bg-[var(--color-surface-variant)] px-4 text-xs">
                  <button
                    type="button"
                    onClick={() => setActiveMobileScreen('HOME')}
                    className={`flex flex-col items-center gap-0.5 ${
                      activeMobileScreen === 'HOME' ? 'text-[var(--color-primary)] font-bold' : 'text-gray-400'
                    }`}
                  >
                    <Smartphone size={18} />
                    <span className="text-[10px]">Briefing</span>
                  </button>

                  <button
                    type="button"
                    onClick={() => setActiveMobileScreen('CAMERA')}
                    className="flex h-11 w-11 -mt-4 items-center justify-center rounded-full bg-[var(--color-primary)] text-white shadow-md transition hover:scale-105"
                    title="Camera Scanner"
                  >
                    <Camera size={20} />
                  </button>

                  <button
                    type="button"
                    onClick={() => setActiveMobileScreen('ADVISORY')}
                    className={`flex flex-col items-center gap-0.5 ${
                      activeMobileScreen === 'ADVISORY' ? 'text-[var(--color-primary)] font-bold' : 'text-gray-400'
                    }`}
                  >
                    <Layers size={18} />
                    <span className="text-[10px]">Advisory</span>
                  </button>
                </div>
              </div>
            </div>

            {/* Right: Companion Telemetry & Simulator Controls (6 cols) */}
            <div className="space-y-5 lg:col-span-6">
              <div className="glass-panel p-5 space-y-4">
                <div className="flex items-center gap-2 pb-3 border-b border-[var(--color-outline-variant)]">
                  <Sliders size={18} className="text-[var(--color-primary)]" />
                  <h3 className="text-sm font-bold text-[var(--color-on-surface)]">
                    Mobile Viewport Controller
                  </h3>
                </div>

                <p className="text-xs text-[var(--color-on-surface-secondary)] leading-relaxed">
                  Use this companion panel to test how the mobile phone responds to changing field light, motion blur, and framing. Adjusting sliders instantly updates the phone screen.
                </p>

                {/* Screen Quick Switches */}
                <div>
                  <span className="text-[11px] font-bold uppercase tracking-wider text-[var(--color-on-surface-tertiary)] block mb-2">
                    Switch Phone View:
                  </span>
                  <div className="flex gap-2">
                    {(['HOME', 'CAMERA', 'ADVISORY'] as const).map((screen) => (
                      <button
                        key={screen}
                        type="button"
                        onClick={() => setActiveMobileScreen(screen)}
                        className={`flex-1 rounded-lg border py-2 text-xs font-semibold transition ${
                          activeMobileScreen === screen
                            ? 'border-[var(--color-primary)] bg-[var(--color-primary-light)] text-[var(--color-primary)]'
                            : 'border-[var(--color-outline-variant)] bg-[var(--color-surface-variant)] text-[var(--color-on-surface-secondary)] hover:text-[var(--color-on-surface)]'
                        }`}
                      >
                        {screen === 'HOME' && '1. Briefing'}
                        {screen === 'CAMERA' && '2. Camera HUD'}
                        {screen === 'ADVISORY' && '3. Advisory'}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Camera Sliders */}
                <div className="space-y-3 pt-3 border-t border-[var(--color-outline-variant)]">
                  <div>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="font-semibold text-[var(--color-on-surface)]">Laplacian Sharpness:</span>
                      <span className={`font-mono font-bold ${blurValue < 100 ? 'text-red-400' : 'text-emerald-400'}`}>
                        {blurValue} / 200
                      </span>
                    </div>
                    <input
                      type="range"
                      min="20"
                      max="200"
                      value={blurValue}
                      onChange={(e) => setBlurValue(Number(e.target.value))}
                      className="w-full accent-[var(--color-primary)] cursor-pointer"
                    />
                  </div>

                  <div>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="font-semibold text-[var(--color-on-surface)]">Sunlight Exposure:</span>
                      <span
                        className={`font-mono font-bold ${
                          brightnessValue < 60 || brightnessValue > 220 ? 'text-red-400' : 'text-emerald-400'
                        }`}
                      >
                        {brightnessValue} / 255
                      </span>
                    </div>
                    <input
                      type="range"
                      min="20"
                      max="255"
                      value={brightnessValue}
                      onChange={(e) => setBrightnessValue(Number(e.target.value))}
                      className="w-full accent-[var(--color-primary)] cursor-pointer"
                    />
                  </div>
                </div>
              </div>

              {/* Specifications Card */}
              <div className="glass-panel p-5 space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-[var(--color-on-surface-secondary)]">
                  Agri-SAGE Mobile Interaction Spec
                </h4>
                <ul className="space-y-2 text-xs text-[var(--color-on-surface-secondary)]">
                  <li className="flex items-start gap-2">
                    <CheckCircle2 size={14} className="text-emerald-400 mt-0.5 shrink-0" />
                    <span>Viewfinder enforces 5 FPS client-side quality filtering before upload.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 size={14} className="text-emerald-400 mt-0.5 shrink-0" />
                    <span>Calibrated confidence taxonomy prevents arbitrary AI hallucinations.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 size={14} className="text-emerald-400 mt-0.5 shrink-0" />
                    <span>Direct weather synchronization dynamically shifts spray window times.</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};
