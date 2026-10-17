import React, { useState } from 'react';
import { SEED_ADVISORIES } from '../data/seedData';
import { DiagnosticAdvisory } from '../types';
import { ConfidenceBadge } from '../components/common/ConfidenceBadge';
import { RiskBadge, ModelledBadge } from '../components/common/RiskBadge';
import { RealtimeQualityBar } from '../components/sandbox/RealtimeQualityBar';
import { SafeImage } from '../components/common/SafeImage';
import { MorningBriefingCard } from '../components/cards/MorningBriefingCard';
import { EvidenceCard } from '../components/cards/EvidenceCard';
import { ScenarioCard } from '../components/cards/ScenarioCard';
import { SchemeCard } from '../components/cards/SchemeCard';
import {
  Smartphone,
  Camera,
  RotateCw,
  Sliders,
  CheckCircle,
  Clock,
  Droplets,
  Calendar,
  Layers,
  ArrowRight,
  Sparkles,
  HelpCircle,
  ThumbsUp,
  ThumbsDown
} from 'lucide-react';

interface FarmerAdvisorySandboxProps {
  lang: 'en' | 'ml';
  onToggleLang: () => void;
}

export const FarmerAdvisorySandbox: React.FC<FarmerAdvisorySandboxProps> = ({
  lang,
  onToggleLang
}) => {
  const [selectedAdvisory, setSelectedAdvisory] = useState<DiagnosticAdvisory>(SEED_ADVISORIES[0]);
  const [activeScreen, setActiveScreen] = useState<'HOME' | 'CAMERA' | 'ADVISORY'>('ADVISORY');

  // Camera simulation state
  const [blurValue, setBlurValue] = useState<number>(145);      // threshold: <100 blur
  const [brightnessValue, setBrightnessValue] = useState<number>(130); // threshold: 60 - 220
  const [framingValue, setFramingValue] = useState<number>(85);   // threshold: <30% too far

  const isCameraQualityAcceptable = blurValue >= 100 && brightnessValue >= 60 && brightnessValue <= 220 && framingValue >= 30;

  return (
    <div className="space-y-6">
      {/* Sandbox Control Header */}
      <div className="p-4 bg-white rounded-xl border border-[var(--color-outline-variant)] shadow-xs flex items-center justify-between flex-wrap gap-3">
        <div>
          <div className="flex items-center gap-2">
            <Smartphone size={20} className="text-[var(--color-primary)]" />
            <h2 className="text-base font-bold text-[var(--color-on-surface)]">
              Farmer Mobile Advisory Experience & Diagnostic Studio
            </h2>
          </div>
          <p className="text-xs text-[var(--color-on-surface-secondary)] mt-0.5">
            Interactive simulator testing all flows from <code>4_AgriSAGE_UIUX_Spec</code> and <code>3_AgriSAGE_AppFlow</code>.
          </p>
        </div>

        {/* Screen switcher */}
        <div className="flex items-center gap-2">
          <div className="flex p-1 rounded-lg bg-[var(--color-surface-variant)] border border-[var(--color-outline-variant)] text-xs font-semibold">
            <button
              type="button"
              onClick={() => setActiveScreen('HOME')}
              className={`px-3 py-1 rounded-md transition-all ${
                activeScreen === 'HOME'
                  ? 'bg-white text-[var(--color-primary-dark)] shadow-xs'
                  : 'text-[var(--color-on-surface-secondary)]'
              }`}
            >
              1. Home & Briefing
            </button>
            <button
              type="button"
              onClick={() => setActiveScreen('CAMERA')}
              className={`px-3 py-1 rounded-md transition-all ${
                activeScreen === 'CAMERA'
                  ? 'bg-white text-[var(--color-primary-dark)] shadow-xs'
                  : 'text-[var(--color-on-surface-secondary)]'
              }`}
            >
              2. Camera Quality Check
            </button>
            <button
              type="button"
              onClick={() => setActiveScreen('ADVISORY')}
              className={`px-3 py-1 rounded-md transition-all ${
                activeScreen === 'ADVISORY'
                  ? 'bg-white text-[var(--color-primary-dark)] shadow-xs'
                  : 'text-[var(--color-on-surface-secondary)]'
              }`}
            >
              3. Advisory Result
            </button>
          </div>

          {/* Crop sample selector */}
          <select
            value={selectedAdvisory.id}
            onChange={(e) => {
              const found = SEED_ADVISORIES.find((a) => a.id === e.target.value);
              if (found) setSelectedAdvisory(found);
            }}
            className="px-3 py-1.5 text-xs font-semibold rounded-lg border border-[var(--color-outline)] bg-white text-[var(--color-on-surface)]"
          >
            {SEED_ADVISORIES.map((adv) => (
              <option key={adv.id} value={adv.id}>
                {adv.farmerContext.crop}: {adv.diagnosisNameEn}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Main Sandbox Layout: Left Phone Viewport, Right Controls & Diagnostics */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left: Mobile Viewport Container (5 cols) */}
        <div className="lg:col-span-5 flex justify-center">
          <div className="w-full max-w-[420px] rounded-[36px] border-[10px] border-slate-900 bg-white shadow-2xl overflow-hidden min-h-[720px] flex flex-col relative">
            {/* Phone Speaker Notch */}
            <div className="h-6 bg-slate-900 w-full flex items-center justify-center">
              <div className="w-20 h-3.5 bg-black rounded-b-xl" />
            </div>

            {/* Mobile Top App Bar (UI/UX Spec Section 4.5: 56dp height, color_primary_dark) */}
            <div className="h-14 bg-[var(--color-primary-dark)] text-white px-4 flex items-center justify-between shrink-0 shadow-sm">
              <div className="flex items-center gap-2">
                <span className="font-bold text-sm tracking-wide">Agri-SAGE</span>
                <span className="text-[10px] bg-white/20 px-1.5 py-0.5 rounded font-mono">
                  {selectedAdvisory.farmerContext.village}
                </span>
              </div>

              <div className="flex items-center gap-2 text-xs">
                <button
                  type="button"
                  onClick={onToggleLang}
                  className="px-2 py-0.5 rounded bg-white/15 hover:bg-white/30 text-[11px] font-bold"
                  title="Toggle Language"
                >
                  {lang === 'ml' ? 'ENG' : 'മലയാളം'}
                </button>
              </div>
            </div>

            {/* Viewport Content based on active screen */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-[var(--color-surface)]">
              {/* SCREEN 1: HOME & BRIEFING */}
              {activeScreen === 'HOME' && (
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

                  {/* 2x2 Action Tiles (UI/UX Spec Section 5.5) */}
                  <div className="grid grid-cols-2 gap-3 text-xs">
                    <button
                      type="button"
                      onClick={() => setActiveScreen('CAMERA')}
                      className="p-3.5 rounded-xl bg-white border border-[var(--color-outline-variant)] shadow-xs hover:border-[var(--color-primary)] text-left flex flex-col justify-between h-24 transition-all"
                    >
                      <Camera size={22} className="text-[var(--color-primary)]" />
                      <div>
                        <strong className="block text-sm font-bold text-[var(--color-on-surface)]">
                          {lang === 'ml' ? 'വിള പരിശോധിക്കുക' : 'Check Crop'}
                        </strong>
                        <span className="text-[11px] text-[var(--color-on-surface-tertiary)]">
                          Camera diagnostic
                        </span>
                      </div>
                    </button>

                    <button
                      type="button"
                      onClick={() => setActiveScreen('ADVISORY')}
                      className="p-3.5 rounded-xl bg-white border border-[var(--color-outline-variant)] shadow-xs hover:border-[var(--color-primary)] text-left flex flex-col justify-between h-24 transition-all"
                    >
                      <Layers size={22} className="text-blue-600" />
                      <div>
                        <strong className="block text-sm font-bold text-[var(--color-on-surface)]">
                          {lang === 'ml' ? 'അവസാന ഉപദേശം' : 'Latest Advisory'}
                        </strong>
                        <span className="text-[11px] text-[var(--color-on-surface-tertiary)]">
                          View details
                        </span>
                      </div>
                    </button>
                  </div>
                </div>
              )}

              {/* SCREEN 2: CAMERA QUALITY ANALYZER */}
              {activeScreen === 'CAMERA' && (
                <div className="space-y-4 animate-fade-in">
                  <div className="relative rounded-2xl overflow-hidden border-2 border-[var(--color-outline)] aspect-[4/3] bg-black flex items-center justify-center">
                    <SafeImage
                      src={selectedAdvisory.imageUrl}
                      alt="Crop Preview"
                      style={{
                        filter: `blur(${Math.max(0, (100 - blurValue) / 15)}px) brightness(${brightnessValue / 130})`
                      }}
                      className="w-full h-full object-cover select-none"
                    />

                    {/* Camera Guidance Overlay */}
                    <div className="absolute inset-0 border-2 border-dashed border-white/50 m-6 rounded-xl pointer-events-none flex items-center justify-center">
                      <span className="text-[10px] text-white/70 bg-black/40 px-2 py-0.5 rounded font-mono">
                        Framing Box
                      </span>
                    </div>

                    {/* Top Quality Bar in Viewfinder */}
                    <div className="absolute top-2 inset-x-2 bg-black/70 backdrop-blur-xs p-2.5 rounded-xl border border-white/20">
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
                    onClick={() => setActiveScreen('ADVISORY')}
                    className={`btn w-full text-sm font-bold h-12 flex items-center justify-center gap-2 ${
                      isCameraQualityAcceptable ? 'btn-primary' : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    }`}
                  >
                    <Camera size={18} />
                    <span>
                      {isCameraQualityAcceptable
                        ? lang === 'ml'
                          ? 'ഫോട്ടോ പരിശോധിക്കുക'
                          : 'Capture & Analyze Crop'
                        : lang === 'ml'
                        ? 'വ്യക്തത പോരാ — ക്രമീകരിക്കുക'
                        : 'Improve Quality to Capture'}
                    </span>
                  </button>
                </div>
              )}

              {/* SCREEN 3: ADVISORY RESULT SCREEN */}
              {activeScreen === 'ADVISORY' && (
                <div className="space-y-4 animate-fade-in text-xs">
                  {/* Sticky Header Box */}
                  <div className="p-3.5 bg-white rounded-xl border border-[var(--color-outline-variant)] shadow-xs space-y-2">
                    <div className="flex items-center justify-between">
                      <ConfidenceBadge
                        state={selectedAdvisory.confidence}
                        score={selectedAdvisory.confidenceScore}
                      />
                      <RiskBadge level={selectedAdvisory.severityRisk} />
                    </div>

                    <div>
                      <h3 className="text-base font-bold text-[var(--color-on-surface)] leading-snug">
                        {lang === 'ml' ? selectedAdvisory.diagnosisNameMl : selectedAdvisory.diagnosisNameEn}
                      </h3>
                      <p className="text-xs text-[var(--color-on-surface-secondary)] font-medium">
                        {lang === 'ml' ? selectedAdvisory.diagnosisNameEn : selectedAdvisory.diagnosisNameMl}
                      </p>
                    </div>
                  </div>

                  {/* Action Plan Card (UI/UX Spec Section 4.2: color_primary_light with 2dp border) */}
                  <div className="p-4 rounded-xl bg-[var(--color-primary-light)] border-2 border-[var(--color-primary)] space-y-3 shadow-xs">
                    <div>
                      <span className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-primary-dark)] block mb-0.5">
                        {lang === 'ml' ? 'എന്ത് ചെയ്യണം (നിർദ്ദേശം)' : 'What To Do'}
                      </span>
                      <strong className="text-sm font-bold text-[var(--color-on-surface)] block">
                        {lang === 'ml' ? selectedAdvisory.actionPlan.whatMl : selectedAdvisory.actionPlan.what}
                      </strong>
                    </div>

                    <div className="pt-2 border-t border-[var(--color-primary-container)]">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-primary-dark)] block mb-0.5">
                        {lang === 'ml' ? 'എപ്പോൾ ചെയ്യണം' : 'When'}
                      </span>
                      <p className="text-xs font-semibold text-[var(--color-on-surface)]">
                        {lang === 'ml' ? selectedAdvisory.actionPlan.whenMl : selectedAdvisory.actionPlan.when}
                      </p>
                    </div>

                    <div className="pt-2 border-t border-[var(--color-primary-container)]">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-primary-dark)] block mb-0.5">
                        {lang === 'ml' ? 'തളിക്കേണ്ട രീതി' : 'How To Apply'}
                      </span>
                      <p className="text-xs text-[var(--color-on-surface-secondary)] leading-relaxed">
                        {lang === 'ml' ? selectedAdvisory.actionPlan.howMl : selectedAdvisory.actionPlan.how}
                      </p>
                    </div>

                    {/* Spray Window & Cost Row */}
                    <div className="flex items-center justify-between pt-2 border-t border-[var(--color-primary-container)] text-xs font-semibold">
                      <div className="flex items-center gap-1.5 text-emerald-800">
                        <Clock size={14} />
                        <span>
                          {selectedAdvisory.actionPlan.sprayWindow?.startTime} - {selectedAdvisory.actionPlan.sprayWindow?.endTime}
                        </span>
                      </div>
                      <div className="text-[var(--color-primary-dark)] font-mono">
                        ₹{selectedAdvisory.actionPlan.costEstimate.minInr} - ₹{selectedAdvisory.actionPlan.costEstimate.maxInr} / acre
                      </div>
                    </div>
                  </div>

                  {/* Evidence Card */}
                  <EvidenceCard evidenceList={selectedAdvisory.evidenceBundle} lang={lang} />

                  {/* DSSAT Scenario Cards */}
                  <ScenarioCard scenarios={selectedAdvisory.scenarios} lang={lang} />

                  {/* Government Schemes */}
                  <SchemeCard schemes={selectedAdvisory.schemesMatched} lang={lang} />

                  {/* Feedback CTA */}
                  <div className="p-3 bg-white rounded-xl border border-[var(--color-outline-variant)] flex items-center justify-between">
                    <span className="text-xs font-semibold text-[var(--color-on-surface)]">
                      {lang === 'ml' ? 'ഉപകാരപ്പെട്ടോ?' : 'Was this advisory helpful?'}
                    </span>
                    <div className="flex gap-2">
                      <button type="button" className="p-1.5 rounded-lg border hover:bg-gray-100 text-emerald-700">
                        <ThumbsUp size={16} />
                      </button>
                      <button type="button" className="p-1.5 rounded-lg border hover:bg-gray-100 text-red-700">
                        <ThumbsDown size={16} />
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Mobile Bottom Navigation (UI/UX Spec Section 4.5: 56dp height) */}
            <div className="h-14 bg-white border-t border-[var(--color-outline-variant)] px-4 flex items-center justify-around shrink-0 text-xs">
              <button
                type="button"
                onClick={() => setActiveScreen('HOME')}
                className={`flex flex-col items-center gap-0.5 ${
                  activeScreen === 'HOME' ? 'text-[var(--color-primary)] font-bold' : 'text-gray-400'
                }`}
              >
                <Smartphone size={18} />
                <span className="text-[10px]">Home</span>
              </button>

              <button
                type="button"
                onClick={() => setActiveScreen('CAMERA')}
                className="w-11 h-11 -mt-4 rounded-full bg-[var(--color-primary)] text-white flex items-center justify-center shadow-md hover:scale-105 transition-transform"
                title="Diagnose"
              >
                <Camera size={20} />
              </button>

              <button
                type="button"
                onClick={() => setActiveScreen('ADVISORY')}
                className={`flex flex-col items-center gap-0.5 ${
                  activeScreen === 'ADVISORY' ? 'text-[var(--color-primary)] font-bold' : 'text-gray-400'
                }`}
              >
                <Layers size={18} />
                <span className="text-[10px]">Advisory</span>
              </button>
            </div>
          </div>
        </div>

        {/* Right: Diagnostic Simulator Controls & Hardware Parameters (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          <div className="bg-white rounded-xl border border-[var(--color-outline-variant)] p-5 shadow-xs space-y-4">
            <div className="flex items-center gap-2 pb-3 border-b border-[var(--color-outline-variant)]">
              <Sliders size={18} className="text-[var(--color-primary)]" />
              <h3 className="text-sm font-bold text-[var(--color-on-surface)]">
                Field Camera Quality Simulation Controls
              </h3>
            </div>
            <p className="text-xs text-[var(--color-on-surface-secondary)] leading-relaxed">
              Agri-SAGE executes real-time computer-vision filtering (Laplacian blur variance and brightness histogramming) at 5 FPS before allowing image acquisition. Adjust the parameters below to verify how the mobile viewfinder guides the farmer in real time.
            </p>

            {/* Slider 1: Blur */}
            <div className="space-y-1.5">
              <div className="flex justify-between text-xs">
                <label className="font-semibold text-[var(--color-on-surface)]">
                  Motion Blur / Focus (Laplacian Variance):
                </label>
                <span className={`font-mono font-bold ${blurValue < 100 ? 'text-red-600' : 'text-emerald-700'}`}>
                  {blurValue} / 200 {blurValue < 100 ? '(Blurry - REJECT)' : '(Sharp - PASS)'}
                </span>
              </div>
              <input
                type="range"
                min="20"
                max="200"
                value={blurValue}
                onChange={(e) => setBlurValue(Number(e.target.value))}
                className="w-full accent-[var(--color-primary)]"
              />
            </div>

            {/* Slider 2: Brightness */}
            <div className="space-y-1.5">
              <div className="flex justify-between text-xs">
                <label className="font-semibold text-[var(--color-on-surface)]">
                  Ambient Lighting & Solar Glare:
                </label>
                <span className={`font-mono font-bold ${brightnessValue < 60 || brightnessValue > 220 ? 'text-red-600' : 'text-emerald-700'}`}>
                  {brightnessValue} / 255 {brightnessValue < 60 ? '(Too Dark)' : brightnessValue > 220 ? '(Overexposed)' : '(Balanced)'}
                </span>
              </div>
              <input
                type="range"
                min="20"
                max="255"
                value={brightnessValue}
                onChange={(e) => setBrightnessValue(Number(e.target.value))}
                className="w-full accent-[var(--color-primary)]"
              />
            </div>

            {/* Slider 3: Crop Area Framing */}
            <div className="space-y-1.5">
              <div className="flex justify-between text-xs">
                <label className="font-semibold text-[var(--color-on-surface)]">
                  Affected Foliage Coverage in Frame:
                </label>
                <span className={`font-mono font-bold ${framingValue < 30 ? 'text-amber-700' : 'text-emerald-700'}`}>
                  {framingValue}% {framingValue < 30 ? '(Too Far - Fill Frame)' : '(Optimal Framing)'}
                </span>
              </div>
              <input
                type="range"
                min="10"
                max="100"
                value={framingValue}
                onChange={(e) => setFramingValue(Number(e.target.value))}
                className="w-full accent-[var(--color-primary)]"
              />
            </div>
          </div>

          {/* Calibrated Confidence States Specification Reference */}
          <div className="bg-white rounded-xl border border-[var(--color-outline-variant)] p-5 shadow-xs space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-[var(--color-on-surface-secondary)]">
              Agri-SAGE Calibrated Confidence Taxonomy (PRD Rule FR-003-03)
            </h3>
            <p className="text-xs text-[var(--color-on-surface-secondary)] leading-relaxed">
              Unlike generic AI platforms that output unreliable percentage numbers, Agri-SAGE categorizes every advisory into one of seven discrete states:
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
              <div className="p-2 rounded-lg bg-[var(--color-surface-variant)] border border-[var(--color-outline-variant)]">
                <ConfidenceBadge state="CONFIRMED" />
                <p className="text-[11px] text-[var(--color-on-surface-secondary)] mt-1">
                  High model probability + multiple symptom matches + stage match.
                </p>
              </div>
              <div className="p-2 rounded-lg bg-[var(--color-surface-variant)] border border-[var(--color-outline-variant)]">
                <ConfidenceBadge state="LIKELY" />
                <p className="text-[11px] text-[var(--color-on-surface-secondary)] mt-1">
                  Strong visual match + favorable environmental factors.
                </p>
              </div>
              <div className="p-2 rounded-lg bg-[var(--color-surface-variant)] border border-[var(--color-outline-variant)]">
                <ConfidenceBadge state="POSSIBLE" />
                <p className="text-[11px] text-[var(--color-on-surface-secondary)] mt-1">
                  Symptoms consistent but weather or stage does not strongly corroborate.
                </p>
              </div>
              <div className="p-2 rounded-lg bg-[var(--color-surface-variant)] border border-[var(--color-outline-variant)]">
                <ConfidenceBadge state="UNCERTAIN" />
                <p className="text-[11px] text-[var(--color-on-surface-secondary)] mt-1">
                  Top-2 class scores close; escalates to expert review queue.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
