import React from 'react';
import { Search, Image as ImageIcon, Newspaper, PlayCircle, BarChart2, Sparkles } from 'lucide-react';

export default function QuickChips({ onSelectAction }) {
  const chips = [
    { id: 'deep_search', icon: Search, label: 'Deep Search' },
    { id: 'create_images', icon: ImageIcon, label: 'Create Images' },
    { id: 'latest_news', icon: Newspaper, label: 'Latest News' },
    { id: 'generate_video', icon: PlayCircle, label: 'Generate Video' },
    { id: 'metrics', icon: BarChart2, label: '99.36% Metrics' }
  ];

  return (
    <div className="quick-chips-row">
      {chips.map((chip) => {
        const IconComponent = chip.icon;
        return (
          <button 
            key={chip.id} 
            className="chip-btn"
            onClick={() => onSelectAction(chip.id)}
          >
            <IconComponent size={14} />
            <span>{chip.label}</span>
          </button>
        );
      })}
    </div>
  );
}
