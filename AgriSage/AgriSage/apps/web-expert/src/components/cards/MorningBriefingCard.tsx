import React, { useState } from 'react';
import { Volume2, VolumeX, Sparkles, Sun, ShieldAlert, Sprout, CheckCircle2, Activity } from 'lucide-react';

interface MorningBriefingCardProps {
  farmerName: string;
  cropName: string;
  stageName: string;
  topRisk: string;
  weatherSummary: string;
  sprayWindowSummary: string;
  primaryAction: string;
  primaryActionMl: string;
  lang?: 'en' | 'ml';
}

export const MorningBriefingCard: React.FC<MorningBriefingCardProps> = ({
  farmerName,
  cropName,
  stageName,
  topRisk,
  weatherSummary,
  sprayWindowSummary,
  primaryAction,
  primaryActionMl,
  lang = 'en'
}) => {
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);

  const handleVoicePlayback = () => {
    if (!('speechSynthesis' in window)) {
      alert('Speech synthesis is not supported on this browser.');
      return;
    }

    if (isPlayingAudio) {
      window.speechSynthesis.cancel();
      setIsPlayingAudio(false);
      return;
    }

    const textToSpeak =
      lang === 'ml'
        ? `നമസ്കാരം ${farmerName}. ഇന്നത്തെ കൃഷി വിവരങ്ങൾ: നിങ്ങളുടെ ${cropName} വിള ഇപ്പോൾ ${stageName} ഘട്ടത്തിലാണ്. പ്രധാന അപകടം: ${topRisk}. ഇന്നത്തെ നിർദ്ദേശം: ${primaryActionMl}.`
        : `Good morning ${farmerName}. Today's farm briefing: Your ${cropName} is in ${stageName} stage. Main risk alert: ${topRisk}. Recommended action for today: ${primaryAction}.`;

    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    utterance.lang = lang === 'ml' ? 'ml-IN' : 'en-IN';
    utterance.rate = 0.95;

    utterance.onstart = () => setIsPlayingAudio(true);
    utterance.onend = () => setIsPlayingAudio(false);
    utterance.onerror = () => setIsPlayingAudio(false);

    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
  };

  return (
    <div className="relative overflow-hidden rounded-2xl border border-[var(--color-primary-container)] bg-gradient-to-br from-[var(--color-surface-glass)] to-[var(--color-primary-light)]/70 backdrop-blur-md p-5 shadow-md transition-all hover:shadow-lg">
      {/* Decorative ambient light source */}
      <div className="absolute top-0 right-0 -mt-8 -mr-8 w-40 h-40 bg-[var(--color-primary)]/15 rounded-full blur-3xl pointer-events-none" />

      {/* Header Row */}
      <div className="flex items-center justify-between gap-3 mb-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-gradient-to-tr from-[var(--color-primary-dark)] to-[var(--color-primary)] text-white shadow-md shadow-emerald-500/20">
            <Sparkles size={20} />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-base font-bold text-[var(--color-on-surface)]">
                {lang === 'ml' ? `പ്രഭാത ബ്രീഫിംഗ് — ${farmerName}` : `Daily Morning Briefing — ${farmerName}`}
              </h2>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 border border-emerald-500/20 uppercase tracking-wider">
                Live AI
              </span>
            </div>
            <p className="text-xs text-[var(--color-on-surface-secondary)]">
              {new Date().toLocaleDateString(lang === 'ml' ? 'ml-IN' : 'en-IN', {
                weekday: 'long',
                month: 'short',
                day: 'numeric'
              })}
            </p>
          </div>
        </div>

        {/* Audio Narration Button with Equalizer Wave */}
        <button
          type="button"
          onClick={handleVoicePlayback}
          className={`flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-bold border transition-all ${
            isPlayingAudio
              ? 'bg-[var(--color-primary)] text-white border-[var(--color-primary)] shadow-md shadow-emerald-500/30'
              : 'bg-white/80 hover:bg-white text-[var(--color-primary-dark)] border-[var(--color-outline-variant)] shadow-xs hover:border-[var(--color-primary)]'
          }`}
          title="Voice narration powered by Bhashini Speech Engine"
        >
          {isPlayingAudio ? (
            <div className="flex items-end gap-0.5 h-4 w-4">
              <span className="w-1 bg-white rounded-full eq-bar-1" />
              <span className="w-1 bg-white rounded-full eq-bar-2" />
              <span className="w-1 bg-white rounded-full eq-bar-3" />
              <span className="w-1 bg-white rounded-full eq-bar-4" />
            </div>
          ) : (
            <Volume2 size={16} />
          )}
          <span>
            {isPlayingAudio
              ? lang === 'ml'
                ? 'നിർത്തുക'
                : 'Pause Audio'
              : lang === 'ml'
              ? 'കേൾക്കുക'
              : 'Listen Audio'}
          </span>
        </button>
      </div>

      {/* 4 Core Briefing Grid Tiles */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-4 text-xs">
        {/* Row 1: Crop & Stage */}
        <div className="flex items-center gap-3 p-3 rounded-xl bg-white/70 backdrop-blur-xs border border-[var(--color-outline-variant)] hover:border-[var(--color-primary)]/40 transition-colors">
          <div className="p-2 rounded-lg bg-emerald-50 text-[var(--color-primary)]">
            <Sprout size={18} />
          </div>
          <div>
            <span className="text-[var(--color-on-surface-tertiary)] block text-[11px] font-medium">
              {lang === 'ml' ? 'വിള & വളർച്ചാ ഘട്ടം' : 'Crop & Growth Stage'}
            </span>
            <strong className="text-[var(--color-on-surface)] text-sm font-semibold">
              {cropName} · {stageName}
            </strong>
          </div>
        </div>

        {/* Row 2: Top Risk */}
        <div className="flex items-center gap-3 p-3 rounded-xl bg-white/70 backdrop-blur-xs border border-[var(--color-outline-variant)] hover:border-amber-400/40 transition-colors">
          <div className="p-2 rounded-lg bg-amber-50 text-amber-600">
            <ShieldAlert size={18} />
          </div>
          <div>
            <span className="text-[var(--color-on-surface-tertiary)] block text-[11px] font-medium">
              {lang === 'ml' ? 'ഇന്നത്തെ പ്രധാന അപകടം' : 'Top Disease Risk'}
            </span>
            <strong className="text-amber-700 text-sm font-semibold">{topRisk}</strong>
          </div>
        </div>

        {/* Row 3: Weather */}
        <div className="flex items-center gap-3 p-3 rounded-xl bg-white/70 backdrop-blur-xs border border-[var(--color-outline-variant)] hover:border-blue-400/40 transition-colors">
          <div className="p-2 rounded-lg bg-blue-50 text-blue-600">
            <Sun size={18} />
          </div>
          <div>
            <span className="text-[var(--color-on-surface-tertiary)] block text-[11px] font-medium">
              {lang === 'ml' ? 'കാലാവസ്ഥ' : 'Farm Weather'}
            </span>
            <strong className="text-[var(--color-on-surface)] text-sm font-semibold">
              {weatherSummary}
            </strong>
          </div>
        </div>

        {/* Row 4: Spray Window */}
        <div className="flex items-center gap-3 p-3 rounded-xl bg-white/70 backdrop-blur-xs border border-[var(--color-outline-variant)] hover:border-emerald-400/40 transition-colors">
          <div className="p-2 rounded-lg bg-emerald-50 text-emerald-600">
            <CheckCircle2 size={18} />
          </div>
          <div>
            <span className="text-[var(--color-on-surface-tertiary)] block text-[11px] font-medium">
              {lang === 'ml' ? 'മരുന്ന് തളിക്കാൻ അനുയോജ്യ സമയം' : 'Optimal Spray Window'}
            </span>
            <strong className="text-emerald-700 text-sm font-semibold">
              {sprayWindowSummary}
            </strong>
          </div>
        </div>
      </div>

      {/* Primary Action Callout with Neon Edge */}
      <div className="p-3.5 rounded-xl bg-white border border-[var(--color-primary)]/40 shadow-xs relative overflow-hidden">
        <div className="absolute left-0 top-0 bottom-0 w-1.5 bg-gradient-to-b from-[var(--color-primary)] to-[var(--color-secondary)]" />
        <div className="pl-2">
          <div className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-primary-dark)] mb-0.5 flex items-center gap-1.5">
            <Activity size={12} className="text-[var(--color-primary)]" />
            <span>{lang === 'ml' ? 'ഇന്ന് ചെയ്യേണ്ട പ്രധാന കാര്യം' : 'Key Action For Today'}</span>
          </div>
          <p className="text-sm font-bold text-[var(--color-on-surface)] leading-snug">
            {lang === 'ml' ? primaryActionMl : primaryAction}
          </p>
        </div>
      </div>
    </div>
  );
};
