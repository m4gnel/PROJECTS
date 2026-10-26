import React, { useState, useRef } from 'react';
import { 
  Paperclip, 
  SlidersHorizontal, 
  Sparkles, 
  ChevronDown, 
  ArrowUp,
  Check
} from 'lucide-react';
import { AVAILABLE_MODELS } from './modelData';

export default function PromptCard({ 
  inputValue, 
  setInputValue, 
  onSubmit, 
  isLoading,
  selectedModel,
  setSelectedModel,
  onOpenTools,
  onAttachSample
}) {
  const [modelDropdownOpen, setModelDropdownOpen] = useState(false);
  const textareaRef = useRef(null);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (inputValue.trim()) {
        onSubmit();
      }
    }
  };

  const currentModel = AVAILABLE_MODELS.find(m => m.id === selectedModel) || AVAILABLE_MODELS[0];

  return (
    <div className="prompt-card">
      <textarea
        ref={textareaRef}
        className="prompt-textarea"
        placeholder="Ask me anything... or paste a news article, headline, or claim to verify..."
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={handleKeyDown}
        rows={3}
      />

      <div className="prompt-card-bottom">
        <div className="prompt-tools-left">
          {/* Attachment button */}
          <button 
            type="button" 
            className="btn-icon-soft" 
            onClick={onAttachSample} 
            title="Load sample article or upload text"
          >
            <Paperclip size={18} />
          </button>

          {/* Tools pill */}
          <button 
            type="button" 
            className="tools-pill-btn" 
            onClick={onOpenTools} 
            title="Configure NLP Preprocessing & Leakage Filters"
          >
            <SlidersHorizontal size={15} />
            <span>Tools</span>
          </button>

          {/* Model Selector Dropdown (Matches Screenshot) */}
          <div style={{ position: 'relative' }}>
            <button 
              type="button" 
              className="model-selector-pill" 
              onClick={() => setModelDropdownOpen(!modelDropdownOpen)}
              title="Select deep learning or reasoning model"
            >
              <Sparkles size={14} className="model-sparkle" style={{ color: currentModel.iconColor }} />
              <span>{currentModel.name}</span>
              <ChevronDown size={14} style={{ color: '#94a3b8' }} />
            </button>

            {modelDropdownOpen && (
              <div 
                style={{
                  position: 'absolute',
                  bottom: 'calc(100% + 8px)',
                  left: 0,
                  width: '280px',
                  background: '#0d1322',
                  border: '1px solid #1e293b',
                  borderRadius: '14px',
                  boxShadow: '0 12px 30px rgba(0,0,0,0.6)',
                  padding: '8px',
                  zIndex: 50,
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '4px'
                }}
              >
                <div style={{ fontSize: '0.72rem', color: '#64748b', padding: '4px 8px', fontWeight: 600, textTransform: 'uppercase' }}>
                  Select Model Engine
                </div>
                {AVAILABLE_MODELS.map(m => (
                  <button
                    key={m.id}
                    onClick={() => {
                      setSelectedModel(m.id);
                      setModelDropdownOpen(false);
                    }}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '8px 10px',
                      borderRadius: '8px',
                      background: selectedModel === m.id ? 'rgba(59, 130, 246, 0.15)' : 'transparent',
                      border: 'none',
                      color: selectedModel === m.id ? '#60a5fa' : '#cbd5e1',
                      cursor: 'pointer',
                      textAlign: 'left',
                      fontSize: '0.84rem'
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <Sparkles size={14} style={{ color: m.iconColor }} />
                      <div>
                        <div style={{ fontWeight: 600 }}>{m.name}</div>
                        <div style={{ fontSize: '0.7rem', color: '#64748b' }}>{m.badge}</div>
                      </div>
                    </div>
                    {selectedModel === m.id && <Check size={14} />}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Submit circular button matching screenshot */}
        <div className="prompt-actions-right">
          <button 
            type="button" 
            className={`btn-submit-circle ${inputValue.trim() ? 'active' : ''}`}
            onClick={onSubmit}
            disabled={!inputValue.trim() || isLoading}
            title={isLoading ? "Processing..." : "Verify Article (Enter)"}
          >
            <ArrowUp size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
