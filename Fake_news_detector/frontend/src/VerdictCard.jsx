import React, { useState } from 'react';
import { 
  AlertTriangle, 
  CheckCircle2, 
  Copy, 
  Check, 
  Download, 
  Layers, 
  TrendingUp, 
  Sparkles,
  Info,
  ChevronDown,
  ChevronUp
} from 'lucide-react';

export default function VerdictCard({ 
  result, 
  onOpenMetrics, 
  onOpenArchitecture 
}) {
  const [copied, setCopied] = useState(false);
  const [showDetails, setShowDetails] = useState(true);
  const [activeWordTooltip, setActiveWordTooltip] = useState(null);

  if (!result) return null;

  const isFake = result.verdictClass === 'fake';
  const probPercentage = isFake 
    ? Math.round(result.fakeProbability * 100) 
    : Math.round(result.realProbability * 100);

  const handleCopy = () => {
    const textToCopy = `[TruthLens BiLSTM Analysis]\nVerdict: ${result.label}\nFake-Probability: ${result.fakeProbability}\nReal-Probability: ${result.realProbability}\nConfidence: ${result.confidence}%\nModel: BiLSTM (2,662,977 params, 99.36% test accuracy)`;
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const reportObj = {
      timestamp: new Date().toISOString(),
      model: result.modelArch,
      overallTestAccuracy: '99.36%',
      verdict: result.label,
      fakeProbability: result.fakeProbability,
      realProbability: result.realProbability,
      confidence: `${result.confidence}%`,
      cleanedText: result.preprocessing.cleanString,
      stylometry: result.stylometry,
      course: 'AIT-401 Foundations of Deep Learning - KTU'
    };
    const blob = new Blob([JSON.stringify(reportObj, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `truthlens-analysis-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className={`verdict-card ${result.verdictClass}`}>
      {/* Top Verdict Header */}
      <div className="verdict-header">
        <div className={`verdict-badge ${result.verdictClass}`}>
          {isFake ? <AlertTriangle size={18} /> : <CheckCircle2 size={18} />}
          <span>{result.label}</span>
        </div>
        <div className="verdict-metric-pill">
          p(fake | x) = {result.fakeProbability.toFixed(2)}
        </div>
      </div>

      {/* Probability Gauge Bar */}
      <div className="prob-meter-container">
        <div className="prob-meter-labels">
          <span>{isFake ? `Fake Probability: ${probPercentage}%` : `Real Probability: ${probPercentage}%`}</span>
          <span>BiLSTM Confidence: {result.confidence}%</span>
        </div>
        <div className="prob-meter-track">
          <div 
            className={`prob-meter-fill ${result.verdictClass}`}
            style={{ width: `${result.confidence}%` }}
          />
        </div>
      </div>

      {/* Preprocessing Stepper Trace */}
      <div className="pipeline-steps-grid">
        <div className="step-card">
          <span className="step-num">Step 01</span>
          <span className="step-title">Dateline Filter</span>
          <span className="step-detail">
            {result.preprocessing.datelineRemoved ? 'Removed Reuters leak tag' : 'No dateline shortcut'}
          </span>
        </div>

        <div className="step-card">
          <span className="step-num">Step 02</span>
          <span className="step-title">NLP Cleaning</span>
          <span className="step-detail">
            URLs & digits stripped, {result.preprocessing.stopwordsCount} stopwords dropped
          </span>
        </div>

        <div className="step-card">
          <span className="step-num">Step 03</span>
          <span className="step-title">WordNet Lemmatize</span>
          <span className="step-detail">
            Reduced to base dictionary roots ({result.preprocessing.cleanWordCount} clean tokens)
          </span>
        </div>

        <div className="step-card">
          <span className="step-num">Step 04</span>
          <span className="step-title">BiLSTM Recurrence</span>
          <span className="step-detail">
            64 forward + 64 backward hidden states merged
          </span>
        </div>
      </div>

      {/* LIME / Attention-style Word Attribution Box */}
      <div className="saliency-box">
        <div className="saliency-header">
          <div className="saliency-title">
            <Sparkles size={15} color="#38bdf8" />
            <span>LIME Word Attribution & Saliency Map</span>
          </div>
          <div className="saliency-legend">
            <span><span className="legend-dot fake"></span> Fake Cue</span>
            <span><span className="legend-dot real"></span> Credible Cue</span>
          </div>
        </div>

        <div className="tokens-flow">
          {result.tokenAttributions.map((token, idx) => {
            if (token.type === 'whitespace') {
              return <span key={idx}>{token.text}</span>;
            }
            return (
              <span
                key={idx}
                className={`token-highlight ${token.category}`}
                title={token.score !== 0 ? `Attribution impact: ${token.score > 0 ? '+' : ''}${token.score.toFixed(1)} (${token.score > 0 ? 'Fake' : 'Real'})` : 'Neutral'}
              >
                {token.text}
              </span>
            );
          })}
        </div>
      </div>

      {/* Stylometric indicators */}
      <div className="stylometry-grid">
        <div className="stat-metric-pill">
          <span className="stat-label">Sensationalism</span>
          <span className="stat-val" style={{ color: result.stylometry.sensationalismScore > 40 ? '#fb7185' : '#34d399' }}>
            {result.stylometry.sensationalismScore}/100
          </span>
        </div>
        <div className="stat-metric-pill">
          <span className="stat-label">Objectivity Index</span>
          <span className="stat-val" style={{ color: result.stylometry.objectivityScore > 60 ? '#34d399' : '#fb7185' }}>
            {result.stylometry.objectivityScore}%
          </span>
        </div>
        <div className="stat-metric-pill">
          <span className="stat-label">Lexical Diversity</span>
          <span className="stat-val">{result.stylometry.lexicalDiversity}</span>
        </div>
        <div className="stat-metric-pill">
          <span className="stat-label">Tokens Processed</span>
          <span className="stat-val">{result.preprocessing.cleanWordCount} / 300</span>
        </div>
      </div>

      {/* Action Buttons Row */}
      <div className="result-actions-row">
        <button className="btn-secondary" onClick={onOpenMetrics} title="Inspect 99.36% Accuracy Curves & Confusion Matrix">
          <TrendingUp size={14} />
          <span>Model Metrics</span>
        </button>
        <button className="btn-secondary" onClick={onOpenArchitecture} title="Inspect BiLSTM 6-Layer Architecture">
          <Layers size={14} />
          <span>Architecture</span>
        </button>
        <button className="btn-secondary" onClick={handleDownload} title="Export Analysis as JSON">
          <Download size={14} />
          <span>Export JSON</span>
        </button>
        <button className="btn-secondary" onClick={handleCopy} title="Copy Verdict to Clipboard">
          {copied ? <Check size={14} color="#34d399" /> : <Copy size={14} />}
          <span>{copied ? 'Copied!' : 'Copy'}</span>
        </button>
      </div>
    </div>
  );
}
