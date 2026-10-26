import React from 'react';
import { X, FileText, Download, ExternalLink, GraduationCap, Users } from 'lucide-react';
import { PROJECT_METADATA } from './modelData';

export default function ReportModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" style={{ maxWidth: '820px' }} onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title">
            <FileText size={20} color="#38bdf8" />
            <span>Course Project Report: Fake News Detection using LSTM</span>
          </div>
          <button className="icon-btn-ghost" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <div className="modal-body">
          {/* Institutional Header Banner */}
          <div 
            style={{
              background: 'linear-gradient(135deg, rgba(56, 189, 248, 0.1) 0%, rgba(99, 102, 241, 0.1) 100%)',
              border: '1px solid rgba(56, 189, 248, 0.25)',
              borderRadius: '12px',
              padding: '18px 20px',
              display: 'flex',
              flexDirection: 'column',
              gap: '6px'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#38bdf8', fontSize: '0.8rem', fontWeight: 600 }}>
              <GraduationCap size={16} />
              <span>APJ Abdul Kalam Technological University (KTU), Kerala</span>
            </div>
            <h3 style={{ fontSize: '1.25rem', color: '#ffffff', fontWeight: 700 }}>
              AIT-401 – Foundations of Deep Learning
            </h3>
            <p style={{ fontSize: '0.82rem', color: '#cbd5e1' }}>
              Adi Shankara Institute of Engineering and Technology, Kalady • Department of AI & DS (October 2026)
            </p>
          </div>

          {/* Authors & Supervision Team */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '12px' }}>
            <div style={{ background: '#090e1a', border: '1px solid #1a2336', borderRadius: '10px', padding: '14px' }}>
              <div style={{ fontSize: '0.72rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase', marginBottom: '6px' }}>
                Project Team (Students)
              </div>
              <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '0.85rem' }}>
                <li style={{ color: '#f1f5f9' }}>• <strong>Krishna Priya V R</strong> (ASI23CA039)</li>
                <li style={{ color: '#38bdf8' }}>• <strong>Magnel Olivero</strong> (ASI23CA040)</li>
                <li style={{ color: '#f1f5f9' }}>• <strong>Miliya Rose Sephy</strong> (ASI23CA041)</li>
              </ul>
            </div>

            <div style={{ background: '#090e1a', border: '1px solid #1a2336', borderRadius: '10px', padding: '14px' }}>
              <div style={{ fontSize: '0.72rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase', marginBottom: '6px' }}>
                Supervision & Approval
              </div>
              <div style={{ fontSize: '0.85rem', color: '#f1f5f9', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                <div><strong>Guide:</strong> Prof. Asha Rose Thomas</div>
                <div><strong>Head of Department:</strong> Dr. Sarika S</div>
                <div style={{ fontSize: '0.75rem', color: '#34d399' }}>✓ Bonafide Academic Project 2026–27</div>
              </div>
            </div>
          </div>

          {/* Table of Contents & Abstract Highlights */}
          <div style={{ background: '#090e1a', border: '1px solid #1a2336', borderRadius: '10px', padding: '16px' }}>
            <h4 style={{ fontSize: '0.9rem', color: '#e2e8f0', marginBottom: '8px' }}>Executive Summary & Findings</h4>
            <p style={{ fontSize: '0.82rem', color: '#94a3b8', lineHeight: '1.6', marginBottom: '12px' }}>
              Trained on 39,100 deduplicated articles from the Kaggle Fake and Real News dataset. An essential practical machine learning issue (CO1) was resolved: removing the <code>"CITY (Reuters) -"</code> dateline artifact that otherwise leaked the class label. On a held-out test set of 7,821 articles, the BiLSTM achieved <strong>99.36% accuracy</strong>, 0.99 precision, and 0.99 recall.
            </p>

            <h4 style={{ fontSize: '0.85rem', color: '#cbd5e1', marginBottom: '6px' }}>Report Chapters (Converted to PROJECT_REPORT.md):</h4>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '6px', fontSize: '0.78rem', color: '#94a3b8' }}>
              <div>• Chapter 1: Introduction & Objectives</div>
              <div>• Chapter 2: Literature Review & Baselines</div>
              <div>• Chapter 3: System Requirements & Architecture</div>
              <div>• Chapter 4: BiLSTM Implementation & Leakage</div>
              <div>• Chapter 5: Results & Confusion Matrix</div>
              <div>• Chapter 6: Conclusions & Outcomes</div>
              <div>• Chapter 7: Future Enhancements (BERT/LIME)</div>
              <div>• Chapter 8: References (Goodfellow, Chollet)</div>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
            <button 
              className="btn-secondary" 
              onClick={() => {
                const a = document.createElement('a');
                a.href = '#';
                window.open('/PROJECT_REPORT.md', '_blank');
              }}
            >
              <ExternalLink size={14} />
              <span>Open PROJECT_REPORT.md</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
