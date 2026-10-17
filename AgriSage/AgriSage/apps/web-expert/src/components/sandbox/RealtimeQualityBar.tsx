import React from 'react';
import { Camera, AlertCircle, CheckCircle, ShieldAlert } from 'lucide-react';

export type QualityState = 'GOOD' | 'WARNING' | 'CRITICAL';

interface RealtimeQualityBarProps {
  blurVariance: number;      // 0 - 200 (threshold < 100 = blurry)
  brightnessLevel: number;   // 0 - 255 (threshold < 60 = too dark, > 220 = too bright)
  cropCoveragePct: number;   // 0 - 100 (threshold < 30% = too far)
  lang?: 'en' | 'ml';
}

export const RealtimeQualityBar: React.FC<RealtimeQualityBarProps> = ({
  blurVariance,
  brightnessLevel,
  cropCoveragePct,
  lang = 'en'
}) => {
  // Determine quality feedback
  const getQualityAssessment = (): { state: QualityState; message: string; messageMl: string } => {
    if (blurVariance < 100) {
      return {
        state: 'CRITICAL',
        message: 'Photo is blurry — hold steady and move closer',
        messageMl: 'ഫോട്ടോ മങ്ങിയിരിക്കുന്നു — ഫോൺ അനക്കാതെ പിടിക്കുക'
      };
    }
    if (brightnessLevel < 60) {
      return {
        state: 'CRITICAL',
        message: 'Too dark — step into open canopy daylight',
        messageMl: 'വെളിച്ചം കുറവാണ് — കൂടുതൽ വെളിച്ചമുള്ളിടത്തേക്ക് മാറുക'
      };
    }
    if (brightnessLevel > 220) {
      return {
        state: 'WARNING',
        message: 'Harsh glare / overexposed — shade the leaf with your hand',
        messageMl: 'കഠിനമായ വെയിൽ — ഇലയ്ക്ക് അല്പം തണൽ നൽകുക'
      };
    }
    if (cropCoveragePct < 30) {
      return {
        state: 'WARNING',
        message: 'Fill at least 50% of the frame with the affected plant area',
        messageMl: 'രോഗം ബാധിച്ച ഭാഗം ഫോക്കസ് ചെയ്ത് ഫ്രെയിമിൽ നിറയ്ക്കുക'
      };
    }
    return {
      state: 'GOOD',
      message: 'Excellent quality — ready to analyze',
      messageMl: 'നല്ല വ്യക്തതയുണ്ട് — വിശകലനം ചെയ്യാൻ തയ്യാറാണ്'
    };
  };

  const assessment = getQualityAssessment();

  const getBarColor = () => {
    switch (assessment.state) {
      case 'GOOD':
        return '#4CAF50';
      case 'WARNING':
        return '#FF9800';
      case 'CRITICAL':
      default:
        return '#F44336';
    }
  };

  return (
    <div className="w-full space-y-1.5">
      {/* 8dp quality indicator bar */}
      <div className="w-full h-2 rounded-full bg-gray-200 overflow-hidden relative">
        <div
          className="h-full transition-all duration-300 rounded-full"
          style={{
            backgroundColor: getBarColor(),
            width: assessment.state === 'GOOD' ? '100%' : assessment.state === 'WARNING' ? '65%' : '35%'
          }}
        />
      </div>

      {/* Dynamic guidance message */}
      <div className="flex items-center justify-between text-xs px-1">
        <div className="flex items-center gap-1.5 font-medium" style={{ color: getBarColor() }}>
          {assessment.state === 'GOOD' ? (
            <CheckCircle size={14} />
          ) : assessment.state === 'WARNING' ? (
            <AlertCircle size={14} />
          ) : (
            <ShieldAlert size={14} />
          )}
          <span>{lang === 'ml' ? assessment.messageMl : assessment.message}</span>
        </div>

        {/* Metrics readout */}
        <div className="text-[10px] font-mono text-[var(--color-on-surface-tertiary)] flex gap-2">
          <span>Blur: {Math.round(blurVariance)}/100</span>
          <span>Light: {Math.round(brightnessLevel)}/255</span>
        </div>
      </div>
    </div>
  );
};
