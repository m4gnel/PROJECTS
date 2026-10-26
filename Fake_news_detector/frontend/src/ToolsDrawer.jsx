import React from 'react';
import { X, SlidersHorizontal, ShieldCheck, Filter, SpellCheck, Cpu } from 'lucide-react';

export default function ToolsDrawer({ 
  isOpen, 
  onClose, 
  nlpOptions, 
  setNlpOptions 
}) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" style={{ maxWidth: '560px' }} onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title">
            <SlidersHorizontal size={18} color="#38bdf8" />
            <span>NLP Preprocessing & Pipeline Settings</span>
          </div>
          <button className="icon-btn-ghost" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <div className="modal-body">
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {/* Dateline Leak Remover (Crucial for honest evaluation) */}
            <div 
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '12px 14px',
                background: '#090e1a',
                border: '1px solid #1a2336',
                borderRadius: '10px'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <ShieldCheck size={18} color="#34d399" />
                <div>
                  <div style={{ fontSize: '0.86rem', fontWeight: 600, color: '#f1f5f9' }}>
                    Dateline Leak Remover
                  </div>
                  <div style={{ fontSize: '0.74rem', color: '#64748b' }}>
                    Strips "CITY (Reuters) -" artifacts to prevent label shortcutting (CO1)
                  </div>
                </div>
              </div>
              <input 
                type="checkbox" 
                checked={nlpOptions.removeDateline} 
                onChange={(e) => setNlpOptions({ ...nlpOptions, removeDateline: e.target.checked })}
                style={{ width: '18px', height: '18px', accentColor: '#3b82f6', cursor: 'pointer' }}
              />
            </div>

            {/* Stopword Removal */}
            <div 
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '12px 14px',
                background: '#090e1a',
                border: '1px solid #1a2336',
                borderRadius: '10px'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Filter size={18} color="#38bdf8" />
                <div>
                  <div style={{ fontSize: '0.86rem', fontWeight: 600, color: '#f1f5f9' }}>
                    Stopword Removal
                  </div>
                  <div style={{ fontSize: '0.74rem', color: '#64748b' }}>
                    Filters common non-informative English tokens ("the", "on", "is")
                  </div>
                </div>
              </div>
              <input 
                type="checkbox" 
                checked={nlpOptions.removeStopwords} 
                onChange={(e) => setNlpOptions({ ...nlpOptions, removeStopwords: e.target.checked })}
                style={{ width: '18px', height: '18px', accentColor: '#3b82f6', cursor: 'pointer' }}
              />
            </div>

            {/* WordNet Lemmatization */}
            <div 
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '12px 14px',
                background: '#090e1a',
                border: '1px solid #1a2336',
                borderRadius: '10px'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <SpellCheck size={18} color="#818cf8" />
                <div>
                  <div style={{ fontSize: '0.86rem', fontWeight: 600, color: '#f1f5f9' }}>
                    WordNet Lemmatization
                  </div>
                  <div style={{ fontSize: '0.74rem', color: '#64748b' }}>
                    Morphological reduction of inflected words to base dictionary forms
                  </div>
                </div>
              </div>
              <input 
                type="checkbox" 
                checked={nlpOptions.applyLemmatizer} 
                onChange={(e) => setNlpOptions({ ...nlpOptions, applyLemmatizer: e.target.checked })}
                style={{ width: '18px', height: '18px', accentColor: '#3b82f6', cursor: 'pointer' }}
              />
            </div>

            {/* Sequence Length */}
            <div 
              style={{
                padding: '12px 14px',
                background: '#090e1a',
                border: '1px solid #1a2336',
                borderRadius: '10px',
                display: 'flex',
                flexDirection: 'column',
                gap: '8px'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '0.86rem', fontWeight: 600, color: '#f1f5f9' }}>
                  Max Padded Sequence Length
                </span>
                <span className="font-mono" style={{ fontSize: '0.82rem', color: '#38bdf8' }}>
                  {nlpOptions.maxLen} tokens
                </span>
              </div>
              <input 
                type="range" 
                min={100} 
                max={500} 
                step={50}
                value={nlpOptions.maxLen} 
                onChange={(e) => setNlpOptions({ ...nlpOptions, maxLen: Number(e.target.value) })}
                style={{ width: '100%', accentColor: '#3b82f6', cursor: 'pointer' }}
              />
              <div style={{ fontSize: '0.72rem', color: '#64748b' }}>
                Matches model training specification in Section 4.5: sequences are padded/truncated to 300 words.
              </div>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '10px' }}>
            <button className="btn-secondary" onClick={onClose}>
              Done
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
