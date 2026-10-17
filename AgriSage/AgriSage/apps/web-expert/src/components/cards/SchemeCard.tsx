import React from 'react';
import { GovernmentScheme } from '../../types';
import { Landmark, Calendar, ExternalLink, ShieldAlert } from 'lucide-react';

interface SchemeCardProps {
  schemes: GovernmentScheme[];
  lang?: 'en' | 'ml';
}

export const SchemeCard: React.FC<SchemeCardProps> = ({ schemes, lang = 'en' }) => {
  if (!schemes || schemes.length === 0) return null;

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-bold text-[var(--color-scheme-text)] flex items-center gap-2">
          <Landmark size={18} />
          <span>{lang === 'ml' ? 'ലഭ്യമായ സർക്കാർ പദ്ധതികൾ' : 'Applicable Government Schemes'}</span>
        </h3>
        <span className="text-xs bg-[var(--color-scheme-bg)] text-[var(--color-scheme-text)] font-semibold px-2 py-0.5 rounded-full">
          {schemes.length} {lang === 'ml' ? 'പദ്ധതികൾ' : 'Schemes'}
        </span>
      </div>

      <div className="space-y-2.5">
        {schemes.map((scheme) => (
          <div
            key={scheme.id}
            className="p-3.5 rounded-xl border border-purple-200 bg-[var(--color-scheme-bg)] shadow-xs relative overflow-hidden"
          >
            <div className="flex items-start justify-between gap-3 mb-1.5">
              <div>
                <h4 className="text-sm font-bold text-[var(--color-scheme-text)]">
                  {lang === 'ml' ? scheme.nameMl : scheme.name}
                </h4>
                <p className="text-xs text-purple-900/70 font-medium">
                  {scheme.authority}
                </p>
              </div>
              <div className="flex items-center gap-1 text-[11px] font-semibold text-purple-900 bg-white/60 px-2 py-0.5 rounded border border-purple-300">
                <Calendar size={12} />
                <span>{scheme.deadline}</span>
              </div>
            </div>

            <p className="text-xs text-purple-950 font-medium mb-3">
              {lang === 'ml' ? scheme.benefitMl : scheme.benefit}
            </p>

            {/* MANDATORY STATUTORY CAVEAT (PRD RULE) */}
            <div className="p-2 rounded-lg bg-white/70 border border-purple-200/80 flex items-start gap-2 text-[11px] text-purple-900">
              <ShieldAlert size={14} className="shrink-0 text-amber-700 mt-0.5" />
              <span>
                <strong>{lang === 'ml' ? 'ശ്രദ്ധിക്കുക:' : 'Notice:'}</strong>{' '}
                {lang === 'ml'
                  ? 'അന്തിമ യോഗ്യത ബന്ധപ്പെട്ട അധികാരി നിർണ്ണയിക്കും.'
                  : 'Final eligibility determined by concerned authority.'}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
