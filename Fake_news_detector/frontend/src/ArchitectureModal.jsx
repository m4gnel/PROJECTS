import React from 'react';
import { X, Layers, Cpu, Database, Network } from 'lucide-react';
import { ARCHITECTURE_LAYERS, PROJECT_METADATA } from './modelData';

export default function ArchitectureModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title">
            <Layers size={20} color="#818cf8" />
            <span>Keras Sequential BiLSTM Architecture (2,662,977 Parameters)</span>
          </div>
          <button className="icon-btn-ghost" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <div className="modal-body">
          {/* Summary stats */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '12px' }}>
            <div className="stat-metric-pill">
              <span className="stat-label">Total Parameters</span>
              <span className="stat-val" style={{ color: '#818cf8' }}>2,662,977</span>
              <span style={{ fontSize: '0.68rem', color: '#64748b' }}>~10.7 MB at 32-bit float</span>
            </div>

            <div className="stat-metric-pill">
              <span className="stat-label">Vocabulary Size</span>
              <span className="stat-val">20,000</span>
              <span style={{ fontSize: '0.68rem', color: '#64748b' }}>Embedding dimension: 128</span>
            </div>

            <div className="stat-metric-pill">
              <span className="stat-label">Sequence Length</span>
              <span className="stat-val">300 tokens</span>
              <span style={{ fontSize: '0.68rem', color: '#64748b' }}>Post-padded & truncated</span>
            </div>

            <div className="stat-metric-pill">
              <span className="stat-label">Recurrent Units</span>
              <span className="stat-val">64 + 64</span>
              <span style={{ fontSize: '0.68rem', color: '#64748b' }}>Bidirectional LSTM (128 total)</span>
            </div>
          </div>

          {/* Layer by Layer Table from Section 3.6 of Report */}
          <div>
            <h4 style={{ fontSize: '0.9rem', color: '#f8fafc', marginBottom: '8px' }}>
              Sequential Layer Pipeline (Table 3.6 of Course Report)
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {ARCHITECTURE_LAYERS.map((layer, idx) => (
                <div 
                  key={idx}
                  style={{
                    background: '#090e1a',
                    border: '1px solid #1a2336',
                    borderRadius: '10px',
                    padding: '12px 14px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    gap: '12px'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div 
                      style={{
                        width: '28px',
                        height: '28px',
                        borderRadius: '6px',
                        background: 'rgba(99, 102, 241, 0.15)',
                        color: '#818cf8',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '0.75rem',
                        fontWeight: 700,
                        fontFamily: 'JetBrains Mono'
                      }}
                    >
                      {idx + 1}
                    </div>
                    <div>
                      <div style={{ fontWeight: 600, fontSize: '0.88rem', color: '#f1f5f9' }}>{layer.layerName}</div>
                      <div style={{ fontSize: '0.74rem', color: '#94a3b8' }}>{layer.description}</div>
                    </div>
                  </div>

                  <div style={{ textAlign: 'right', flexShrink: 0 }}>
                    <div className="font-mono" style={{ fontSize: '0.8rem', color: '#38bdf8' }}>{layer.outputShape}</div>
                    <div style={{ fontSize: '0.72rem', color: '#64748b' }}>{layer.params} params</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* LSTM Gating Equations from Section 4.6 of Report */}
          <div style={{ background: '#090e1a', border: '1px solid #1a2336', borderRadius: '12px', padding: '16px' }}>
            <h4 style={{ fontSize: '0.88rem', color: '#e2e8f0', marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Cpu size={15} color="#38bdf8" />
              <span>LSTM Memory Cell Gating Formulation</span>
            </h4>
            <div 
              className="font-mono" 
              style={{ 
                fontSize: '0.8rem', 
                color: '#cbd5e1', 
                lineHeight: '1.7', 
                background: '#050810', 
                padding: '12px 16px', 
                borderRadius: '8px',
                border: '1px solid rgba(255,255,255,0.05)'
              }}
            >
              <div>• Forget Gate:    f_t = σ(W_f · [h_t-1, x_t] + b_f)</div>
              <div>• Input Gate:     i_t = σ(W_i · [h_t-1, x_t] + b_i)</div>
              <div>• Candidate Cell: c~_t = tanh(W_c · [h_t-1, x_t] + b_c)</div>
              <div>• Updated Memory: c_t = f_t ⊙ c_t-1 + i_t ⊙ c~_t</div>
              <div>• Output Gate:    o_t = σ(W_o · [h_t-1, x_t] + b_o)</div>
              <div>• Hidden State:   h_t = o_t ⊙ tanh(c_t)</div>
            </div>
            <p style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '8px' }}>
              Bidirectional joining: concatenation of forward recurrent hidden state and backward recurrent state yields 128 context values per sample.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
