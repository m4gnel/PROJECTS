import React from 'react';
import { RiskLevel } from '../../types';
import { Flame, AlertTriangle, ShieldCheck, Info } from 'lucide-react';

interface RiskBadgeProps {
  level: RiskLevel;
  className?: string;
  showIcon?: boolean;
}

export const RiskBadge: React.FC<RiskBadgeProps> = ({ level, className = '', showIcon = true }) => {
  const getRiskStyle = () => {
    switch (level) {
      case 'CRITICAL':
        return {
          bg: 'var(--color-risk-critical-bg)',
          color: 'var(--color-risk-critical)',
          border: 'var(--color-risk-critical)',
          icon: Flame,
          label: 'CRITICAL RISK',
          labelMl: 'അതിതീവ്ര അപകടം'
        };
      case 'HIGH':
        return {
          bg: 'var(--color-risk-high-bg)',
          color: 'var(--color-risk-high)',
          border: 'var(--color-risk-high)',
          icon: AlertTriangle,
          label: 'HIGH RISK',
          labelMl: 'ഉയർന്ന അപകടം'
        };
      case 'MEDIUM':
        return {
          bg: 'var(--color-risk-medium-bg)',
          color: 'var(--color-risk-medium)',
          border: 'var(--color-risk-medium)',
          icon: Info,
          label: 'MEDIUM RISK',
          labelMl: 'ഇടത്തരം അപകടം'
        };
      case 'LOW':
      default:
        return {
          bg: 'var(--color-risk-low-bg)',
          color: 'var(--color-risk-low)',
          border: 'var(--color-risk-low)',
          icon: ShieldCheck,
          label: 'LOW RISK',
          labelMl: 'കുറഞ്ഞ അപകടം'
        };
    }
  };

  const style = getRiskStyle();
  const Icon = style.icon;

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider border ${className}`}
      style={{
        backgroundColor: style.bg,
        color: style.color,
        borderColor: style.border
      }}
    >
      {showIcon && <Icon size={13} className="shrink-0" />}
      <span>{style.label}</span>
    </span>
  );
};

export const ModelledBadge: React.FC<{ className?: string }> = ({ className = '' }) => (
  <span
    className={`inline-flex items-center gap-1 text-[11px] font-mono text-[var(--color-on-surface-tertiary)] italic ${className}`}
    title="Non-negotiable safety label: Physics/arithmetic projection, not guaranteed outcome."
  >
    * Modelled estimate (DSSAT v4.8)
  </span>
);
