import React from 'react';
import { X, Sparkles, CheckCircle, AlertTriangle, ArrowRight } from 'lucide-react';
import { SAMPLE_ARTICLES } from './nlpEngine';

export default function SamplesDrawer({ isOpen, onClose, onSelectSample }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" style={{ maxWidth: '640px' }} onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title">
            <Sparkles size={18} color="#fb923c" />
            <span>Select Benchmark Test Article</span>
          </div>
          <button className="icon-btn-ghost" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <div className="modal-body">
          <p style={{ fontSize: '0.82rem', color: '#94a3b8' }}>
            Choose an article from the Kaggle evaluation set and Course Project Report to immediately run the full NLP & BiLSTM inference pipeline:
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {SAMPLE_ARTICLES.map((sample) => {
              const isFake = sample.category === 'Fake News';
              return (
                <div
                  key={sample.id}
                  onClick={() => {
                    onSelectSample(sample.text);
                    onClose();
                  }}
                  style={{
                    background: '#090e1a',
                    border: '1px solid #1a2336',
                    borderRadius: '12px',
                    padding: '12px 16px',
                    cursor: 'pointer',
                    transition: 'all 0.15s ease',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '6px'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.borderColor = '#3b82f6';
                    e.currentTarget.style.background = '#10172a';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = '#1a2336';
                    e.currentTarget.style.background = '#090e1a';
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      {isFake ? (
                        <AlertTriangle size={15} color="#fb7185" />
                      ) : (
                        <CheckCircle size={15} color="#34d399" />
                      )}
                      <span style={{ fontSize: '0.88rem', fontWeight: 600, color: '#f8fafc' }}>
                        {sample.title}
                      </span>
                    </div>
                    <span 
                      style={{ 
                        fontSize: '0.72rem', 
                        padding: '2px 8px', 
                        borderRadius: '999px',
                        background: isFake ? 'rgba(244, 63, 94, 0.15)' : 'rgba(52, 211, 153, 0.15)',
                        color: isFake ? '#fda4af' : '#6ee7b7',
                        fontWeight: 600
                      }}
                    >
                      {sample.badge}
                    </span>
                  </div>

                  <p style={{ fontSize: '0.78rem', color: '#94a3b8', fontStyle: 'italic', lineHeight: '1.4' }}>
                    "{sample.text}"
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
