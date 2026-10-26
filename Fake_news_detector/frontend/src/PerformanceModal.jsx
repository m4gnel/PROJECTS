import React from 'react';
import { X, TrendingUp, CheckCircle, AlertCircle, Award } from 'lucide-react';
import { TRAINING_EPOCHS, CONFUSION_MATRIX, CLASSIFICATION_REPORT, PROJECT_METADATA } from './modelData';

export default function PerformanceModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title">
            <TrendingUp size={20} color="#34d399" />
            <span>BiLSTM Model Performance & Evaluation (99.36% Accuracy)</span>
          </div>
          <button className="icon-btn-ghost" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <div className="modal-body">
          {/* Key Metric Highlights */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '12px' }}>
            <div className="stat-metric-pill" style={{ background: 'rgba(52, 211, 153, 0.1)', borderColor: 'rgba(52, 211, 153, 0.3)' }}>
              <span className="stat-label">Test Accuracy</span>
              <span className="stat-val" style={{ color: '#34d399' }}>99.36%</span>
              <span style={{ fontSize: '0.68rem', color: '#6ee7b7' }}>7,771 / 7,821 correct</span>
            </div>

            <div className="stat-metric-pill">
              <span className="stat-label">Precision / Recall</span>
              <span className="stat-val" style={{ color: '#38bdf8' }}>0.99 / 0.99</span>
              <span style={{ fontSize: '0.68rem', color: '#64748b' }}>Balanced across classes</span>
            </div>

            <div className="stat-metric-pill">
              <span className="stat-label">Optimal Checkpoint</span>
              <span className="stat-val" style={{ color: '#fbbf24' }}>Epoch 2</span>
              <span style={{ fontSize: '0.68rem', color: '#64748b' }}>EarlyStopping restored</span>
            </div>

            <div className="stat-metric-pill">
              <span className="stat-label">Test Articles</span>
              <span className="stat-val">7,821</span>
              <span style={{ fontSize: '0.68rem', color: '#64748b' }}>4,239 Real / 3,582 Fake</span>
            </div>
          </div>

          {/* Interactive Confusion Matrix */}
          <div>
            <h4 style={{ fontSize: '0.9rem', color: '#f8fafc', marginBottom: '8px' }}>
              Held-Out Test Set Confusion Matrix (N = 7,821)
            </h4>
            <div className="cm-container">
              <div className="cm-grid">
                <div className="cm-cell header"></div>
                <div className="cm-cell header">Predicted Real</div>
                <div className="cm-cell header">Predicted Fake</div>

                <div className="cm-cell header" style={{ textAlign: 'right', paddingRight: '10px' }}>Actual Real</div>
                <div className="cm-cell hit-real">
                  <span className="cm-val">{CONFUSION_MATRIX.trueReal.toLocaleString()}</span>
                  <span className="cm-tag">True Real (99.4%)</span>
                </div>
                <div className="cm-cell miss">
                  <span className="cm-val">{CONFUSION_MATRIX.falseFake}</span>
                  <span className="cm-tag">False Fake (0.6%)</span>
                </div>

                <div className="cm-cell header" style={{ textAlign: 'right', paddingRight: '10px' }}>Actual Fake</div>
                <div className="cm-cell miss">
                  <span className="cm-val">{CONFUSION_MATRIX.falseReal}</span>
                  <span className="cm-tag">False Real (0.7%)</span>
                </div>
                <div className="cm-cell hit-fake">
                  <span className="cm-val">{CONFUSION_MATRIX.trueFake.toLocaleString()}</span>
                  <span className="cm-tag">True Fake (99.3%)</span>
                </div>
              </div>
              <p style={{ fontSize: '0.75rem', color: '#94a3b8', textAlign: 'center' }}>
                Balanced errors: exactly 25 false positives and 25 false negatives across 7,821 held-out test articles.
              </p>
            </div>
          </div>

          {/* Training Curve History Table */}
          <div>
            <h4 style={{ fontSize: '0.9rem', color: '#f8fafc', marginBottom: '8px' }}>
              Epoch-by-Epoch Convergence (Adam Optimizer, Batch 64)
            </h4>
            <table className="metric-table">
              <thead>
                <tr>
                  <th>Epoch</th>
                  <th>Train Accuracy</th>
                  <th>Train Loss</th>
                  <th>Val Accuracy</th>
                  <th>Val Loss</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {TRAINING_EPOCHS.map((ep) => (
                  <tr key={ep.epoch} style={{ background: ep.epoch === 2 ? 'rgba(59, 130, 246, 0.1)' : 'transparent' }}>
                    <td style={{ fontWeight: 600, color: ep.epoch === 2 ? '#60a5fa' : 'inherit' }}>
                      Epoch {ep.epoch} {ep.epoch === 2 && '★ Best'}
                    </td>
                    <td>{ep.trainAcc}%</td>
                    <td className="font-mono">{ep.trainLoss.toFixed(4)}</td>
                    <td style={{ fontWeight: 600 }}>{ep.valAcc}%</td>
                    <td className="font-mono" style={{ color: ep.epoch === 2 ? '#34d399' : 'inherit' }}>
                      {ep.valLoss.toFixed(4)}
                    </td>
                    <td style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{ep.note}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Classification Report */}
          <div>
            <h4 style={{ fontSize: '0.9rem', color: '#f8fafc', marginBottom: '8px' }}>
              Precision, Recall & F1-Score Breakdown
            </h4>
            <table className="metric-table">
              <thead>
                <tr>
                  <th>Class</th>
                  <th>Precision</th>
                  <th>Recall</th>
                  <th>F1-Score</th>
                  <th>Support</th>
                </tr>
              </thead>
              <tbody>
                {CLASSIFICATION_REPORT.map((row, idx) => (
                  <tr key={idx}>
                    <td style={{ fontWeight: 600 }}>{row.class}</td>
                    <td>{row.precision.toFixed(2)}</td>
                    <td>{row.recall.toFixed(2)}</td>
                    <td style={{ color: '#38bdf8' }}>{row.f1.toFixed(2)}</td>
                    <td>{row.support.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
