import React from 'react';
import { SimulationScenario } from '../../types';
import { ModelledBadge } from '../common/RiskBadge';
import { CheckCircle2, TrendingUp, TrendingDown, DollarSign } from 'lucide-react';

interface ScenarioCardProps {
  scenarios: SimulationScenario[];
  lang?: 'en' | 'ml';
  onSelect?: (scenarioId: 'A' | 'B' | 'C') => void;
}

export const ScenarioCard: React.FC<ScenarioCardProps> = ({ scenarios, lang = 'en', onSelect }) => {
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between flex-wrap gap-2">
        <h3 className="text-sm font-bold text-[var(--color-on-surface)] flex items-center gap-2">
          <span>{lang === 'ml' ? 'ഓപ്ഷനുകൾ താരതമ്യം ചെയ്യുക' : 'Compare Decision Scenarios'}</span>
          <span className="text-xs font-normal text-[var(--color-on-surface-secondary)]">
            (DSSAT v4.8 Physics Engine)
          </span>
        </h3>
        <ModelledBadge />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {scenarios.map((s) => (
          <div
            key={s.id}
            onClick={() => onSelect && onSelect(s.id)}
            className={`relative rounded-xl p-3.5 border transition-all cursor-pointer ${
              s.isRecommended
                ? 'bg-[var(--color-primary-light)] border-[var(--color-primary)] ring-2 ring-[var(--color-primary)]/20 shadow-sm'
                : 'bg-white border-[var(--color-outline-variant)] hover:border-[var(--color-outline)] shadow-xs'
            }`}
          >
            {s.isRecommended && (
              <div className="absolute -top-2.5 right-3 bg-[var(--color-primary)] text-white text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full flex items-center gap-1 shadow-xs">
                <CheckCircle2 size={11} />
                <span>{lang === 'ml' ? 'ശുപാർശ ചെയ്യുന്നത്' : 'Recommended'}</span>
              </div>
            )}

            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold px-2 py-0.5 rounded bg-black/5 text-[var(--color-on-surface-secondary)] font-mono">
                Scenario {s.id}
              </span>
              {s.costInr > 0 ? (
                <span className="text-xs font-semibold text-[var(--color-on-surface)]">
                  ₹{s.costInr.toLocaleString()} / ha
                </span>
              ) : (
                <span className="text-xs text-[var(--color-on-surface-tertiary)]">₹0 cost</span>
              )}
            </div>

            <h4 className="text-sm font-bold text-[var(--color-on-surface)] mb-1 leading-snug">
              {lang === 'ml' ? s.titleMl : s.title}
            </h4>
            <p className="text-xs text-[var(--color-on-surface-secondary)] mb-3 line-clamp-2">
              {lang === 'ml' ? s.actionSummaryMl : s.actionSummary}
            </p>

            <div className="space-y-1.5 pt-2 border-t border-[var(--color-outline-variant)] text-xs">
              <div className="flex justify-between items-center">
                <span className="text-[var(--color-on-surface-secondary)]">
                  {lang === 'ml' ? 'പ്രതീക്ഷിക്കുന്ന വിളവ്' : 'Projected Yield'}:
                </span>
                <span className="font-mono font-bold text-[var(--color-on-surface)]">
                  {s.yieldEstimateKgHa.toLocaleString()} kg/ha
                </span>
              </div>

              <div className="flex justify-between items-center">
                <span className="text-[var(--color-on-surface-secondary)]">
                  {lang === 'ml' ? 'പ്രതീക്ഷിക്കുന്ന ലാഭം' : 'Net Margin'}:
                </span>
                <span
                  className={`font-mono font-bold flex items-center gap-0.5 ${
                    s.netReturnInrHa > 50000 ? 'text-[var(--color-primary-dark)]' : 'text-amber-800'
                  }`}
                >
                  ₹{s.netReturnInrHa.toLocaleString()} / ha
                </span>
              </div>

              <div className="flex justify-between items-center text-[11px] text-[var(--color-on-surface-tertiary)]">
                <span>{lang === 'ml' ? 'രോഗ നഷ്ടം' : 'Disease Loss'}:</span>
                <span className={`font-semibold ${s.diseaseLossPct > 20 ? 'text-red-700' : 'text-green-700'}`}>
                  {s.diseaseLossPct}%
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
