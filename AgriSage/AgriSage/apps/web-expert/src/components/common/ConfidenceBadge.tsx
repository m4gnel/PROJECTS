import React from 'react';
import { ConfidenceState } from '../../types';
import { CheckCircle2, AlertCircle, HelpCircle, AlertTriangle, XCircle } from 'lucide-react';

interface ConfidenceBadgeProps {
  state: ConfidenceState;
  score?: number;
  className?: string;
}

export const ConfidenceBadge: React.FC<ConfidenceBadgeProps> = ({ state, score, className = '' }) => {
  const getBadgeConfig = () => {
    switch (state) {
      case 'CONFIRMED':
        return {
          bg: '#E8F5E9',
          color: 'var(--color-confidence-confirmed)',
          borderColor: 'var(--color-confidence-confirmed)',
          icon: CheckCircle2,
          label: 'CONFIRMED',
          labelMl: 'സ്ഥിരീകരിച്ചത്'
        };
      case 'LIKELY':
        return {
          bg: '#E8F5E9',
          color: 'var(--color-confidence-likely)',
          borderColor: 'var(--color-confidence-likely)',
          icon: CheckCircle2,
          label: 'LIKELY',
          labelMl: 'സാധ്യത കൂടുതൽ'
        };
      case 'POSSIBLE':
        return {
          bg: '#FFF8E1',
          color: 'var(--color-confidence-possible)',
          borderColor: 'var(--color-confidence-possible)',
          icon: AlertCircle,
          label: 'POSSIBLE',
          labelMl: 'സാധ്യതയുണ്ട്'
        };
      case 'UNCERTAIN':
        return {
          bg: '#FBE9E7',
          color: 'var(--color-confidence-uncertain)',
          borderColor: 'var(--color-confidence-uncertain)',
          icon: HelpCircle,
          label: 'UNCERTAIN',
          labelMl: 'ഉറപ്പില്ല'
        };
      case 'CONFLICTING_EVIDENCE':
        return {
          bg: '#FFF3E0',
          color: 'var(--color-confidence-conflicting)',
          borderColor: 'var(--color-confidence-conflicting)',
          icon: AlertTriangle,
          label: 'CONFLICTING EVIDENCE',
          labelMl: 'വൈരുദ്ധ്യമുള്ള തെളിവുകൾ'
        };
      case 'INSUFFICIENT_DATA':
        return {
          bg: '#F5F5F5',
          color: 'var(--color-confidence-insufficient)',
          borderColor: 'var(--color-confidence-insufficient)',
          icon: HelpCircle,
          label: 'INSUFFICIENT DATA',
          labelMl: 'വിവരങ്ങൾ അപൂർണ്ണമാണ്'
        };
      case 'OUT_OF_SCOPE':
      default:
        return {
          bg: '#EEEEEE',
          color: 'var(--color-confidence-outofscope)',
          borderColor: 'var(--color-confidence-outofscope)',
          icon: XCircle,
          label: 'OUT OF SCOPE',
          labelMl: 'പിന്തുണയ്ക്കാത്ത വിള'
        };
    }
  };

  const config = getBadgeConfig();
  const Icon = config.icon;

  return (
    <div
      className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold tracking-wide border shadow-xs ${className}`}
      style={{
        backgroundColor: config.bg,
        color: config.color,
        borderColor: config.borderColor
      }}
      title={`Calibrated State: ${config.label}${score !== undefined ? ` (${Math.round(score * 100)}%)` : ''}`}
    >
      <Icon size={14} className="shrink-0" />
      <span>{config.label}</span>
      {score !== undefined && (
        <span className="opacity-80 text-[11px] font-mono">
          ({Math.round(score * 100)}%)
        </span>
      )}
    </div>
  );
};
