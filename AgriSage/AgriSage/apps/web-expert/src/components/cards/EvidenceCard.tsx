import React, { useState } from 'react';
import { EvidenceItem } from '../../types';
import { ChevronDown, ChevronUp, Leaf, CloudRain, Calendar, BookOpen, AlertCircle, ShieldAlert } from 'lucide-react';

interface EvidenceCardProps {
  evidenceList: EvidenceItem[];
  lang?: 'en' | 'ml';
}

export const EvidenceCard: React.FC<EvidenceCardProps> = ({ evidenceList, lang = 'en' }) => {
  const [isExpanded, setIsExpanded] = useState(true);

  const getIcon = (type: EvidenceItem['type']) => {
    switch (type) {
      case 'image_pattern':
        return <Leaf size={18} className="text-[var(--color-primary)]" />;
      case 'weather_factor':
        return <CloudRain size={18} className="text-blue-600" />;
      case 'crop_stage':
        return <Calendar size={18} className="text-amber-600" />;
      case 'scientific_literature':
      default:
        return <BookOpen size={18} className="text-purple-600" />;
    }
  };

  return (
    <div className="border border-[var(--color-outline-variant)] rounded-xl overflow-hidden bg-[var(--color-info-bg)] shadow-xs transition-all">
      <button
        type="button"
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between p-3.5 bg-white/70 hover:bg-white text-left font-semibold text-sm transition-colors border-b border-[var(--color-outline-variant)]"
      >
        <div className="flex items-center gap-2 text-[var(--color-on-surface)]">
          <ShieldAlert size={18} className="text-[var(--color-primary)]" />
          <span>
            {lang === 'ml' ? 'ഇത് എന്തുകൊണ്ട്? (തെളിവുകൾ)' : 'Why We Think This (Evidence Bundle)'}
          </span>
          <span className="text-xs bg-[var(--color-primary-container)] text-[var(--color-primary-dark)] px-2 py-0.5 rounded-full font-bold">
            {evidenceList.length} {lang === 'ml' ? 'ഘടകങ്ങൾ' : 'Factors'}
          </span>
        </div>
        {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
      </button>

      {isExpanded && (
        <div className="p-3.5 space-y-3">
          {evidenceList.map((item) => (
            <div
              key={item.id}
              className="flex items-start gap-3 p-3 bg-white rounded-lg border border-[var(--color-outline-variant)] shadow-2xs hover:border-[var(--color-primary)] transition-all"
            >
              <div className="p-2 bg-[var(--color-surface-variant)] rounded-md shrink-0 mt-0.5">
                {getIcon(item.type)}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2 flex-wrap mb-1">
                  <h4 className="text-sm font-semibold text-[var(--color-on-surface)]">
                    {item.factor}
                  </h4>
                  {item.sourceTier && (
                    <span className="text-[11px] px-2 py-0.5 rounded-full bg-[var(--color-surface-variant)] text-[var(--color-on-surface-secondary)] font-medium border border-[var(--color-outline-variant)]">
                      {item.sourceTier}
                    </span>
                  )}
                </div>
                <p className="text-xs text-[var(--color-on-surface-secondary)] leading-relaxed mb-1.5">
                  {item.description}
                </p>
                {item.citation && (
                  <div className="text-[11px] text-[var(--color-primary-dark)] font-medium flex items-center gap-1.5">
                    <BookOpen size={12} />
                    <span>Citation: {item.citation}</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
