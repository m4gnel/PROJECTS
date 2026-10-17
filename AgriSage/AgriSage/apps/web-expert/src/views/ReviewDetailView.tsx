import React, { useState } from 'react';
import { DiagnosticAdvisory } from '../types';
import { ConfidenceBadge } from '../components/common/ConfidenceBadge';
import { RiskBadge } from '../components/common/RiskBadge';
import { EvidenceCard } from '../components/cards/EvidenceCard';
import { ScenarioCard } from '../components/cards/ScenarioCard';
import { SchemeCard } from '../components/cards/SchemeCard';
import { SafeImage } from '../components/common/SafeImage';
import {
  ArrowLeft,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  ShieldCheck,
  CloudRain,
  Thermometer,
  Wind,
  Droplets,
  User,
  MapPin,
  Send,
  Pencil,
  Layers,
  Sparkles,
  Scan,
  Maximize2
} from 'lucide-react';

interface ReviewDetailViewProps {
  advisory: DiagnosticAdvisory;
  onBack: () => void;
  onSaveVerdict: (advisoryId: string, verdict: 'AGREE' | 'DISAGREE' | 'PARTIAL', notes: string, safetyOk: boolean) => void;
  lang?: 'en' | 'ml';
}

export const ReviewDetailView: React.FC<ReviewDetailViewProps> = ({
  advisory,
  onBack,
  onSaveVerdict,
  lang = 'en'
}) => {
  const [zoomLevel, setZoomLevel] = useState(1);
  const [spectralMode, setSpectralMode] = useState<'RGB' | 'NDVI' | 'EDGE'>('RGB');
  const [verdict, setVerdict] = useState<'AGREE' | 'DISAGREE' | 'PARTIAL'>('AGREE');
  const [safetyApproved, setSafetyApproved] = useState(true);
  const [expertNotes, setExpertNotes] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleZoomIn = () => setZoomLevel((prev) => Math.min(prev + 0.3, 2.5));
  const handleZoomOut = () => setZoomLevel((prev) => Math.max(prev - 0.3, 0.8));
  const handleResetZoom = () => setZoomLevel(1);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!safetyApproved) {
      alert('You must verify chemical safety and CIB&RC compliance before submitting the verdict.');
      return;
    }
    onSaveVerdict(advisory.id, verdict, expertNotes, safetyApproved);
    setIsSubmitted(true);
  };

  const getImageFilterStyle = () => {
    switch (spectralMode) {
      case 'NDVI':
        // False-color NDVI simulated chlorophyll stress spectrum
        return {
          filter: 'hue-rotate(95deg) saturate(220%) contrast(140%)',
          transition: 'filter 300ms ease'
        };
      case 'EDGE':
        // High-contrast lesion boundary detection
        return {
          filter: 'contrast(240%) grayscale(100%) invert(15%)',
          transition: 'filter 300ms ease'
        };
      case 'RGB':
      default:
        return {
          filter: 'none',
          transition: 'filter 300ms ease'
        };
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Top Header Navigation */}
      <div className="flex items-center justify-between gap-4 flex-wrap pb-4 border-b border-[var(--color-outline-variant)]">
        <button
          type="button"
          onClick={onBack}
          className="btn btn-outline text-xs h-9 px-3 flex items-center gap-1.5"
        >
          <ArrowLeft size={16} />
          <span>Back to Triage Queue</span>
        </button>

        <div className="flex items-center gap-3">
          <span className="text-xs font-mono text-[var(--color-on-surface-tertiary)] bg-[var(--color-surface-variant)] px-2.5 py-1 rounded-md border border-[var(--color-outline-variant)]">
            Case Ref: {advisory.id}
          </span>
          <ConfidenceBadge state={advisory.confidence} score={advisory.confidenceScore} />
          <RiskBadge level={advisory.severityRisk} />
        </div>
      </div>

      {/* Main Split-Screen Workspace */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Visual Bio-Imaging Inspection (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          <div className="glass-panel p-4 shadow-sm space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-[var(--color-on-surface)] flex items-center gap-2">
                <Scan size={17} className="text-[var(--color-primary)]" />
                <span>Field Specimen Bio-Scanner</span>
              </h3>
              {/* Zoom & Viewport Controls */}
              <div className="flex items-center gap-1 bg-[var(--color-surface-variant)] p-1 rounded-lg border border-[var(--color-outline-variant)]">
                <button
                  type="button"
                  onClick={handleZoomIn}
                  className="p-1 hover:bg-white rounded text-[var(--color-on-surface)] transition-all"
                  title="Zoom In"
                >
                  <ZoomIn size={15} />
                </button>
                <button
                  type="button"
                  onClick={handleZoomOut}
                  className="p-1 hover:bg-white rounded text-[var(--color-on-surface)] transition-all"
                  title="Zoom Out"
                >
                  <ZoomOut size={15} />
                </button>
                <button
                  type="button"
                  onClick={handleResetZoom}
                  className="p-1 hover:bg-white rounded text-[var(--color-on-surface)] transition-all"
                  title="Reset"
                >
                  <RotateCcw size={15} />
                </button>
              </div>
            </div>

            {/* Futuristic Spectral Filter Selector Bar */}
            <div className="flex items-center justify-between bg-[var(--color-surface-variant)] p-1 rounded-lg text-xs font-semibold">
              <span className="text-[11px] text-[var(--color-on-surface-tertiary)] pl-2">
                Filter:
              </span>
              <div className="flex gap-1">
                <button
                  type="button"
                  onClick={() => setSpectralMode('RGB')}
                  className={`px-2.5 py-1 rounded transition-all ${
                    spectralMode === 'RGB'
                      ? 'bg-white text-[var(--color-primary-dark)] shadow-xs'
                      : 'text-[var(--color-on-surface-secondary)] hover:text-[var(--color-on-surface)]'
                  }`}
                >
                  RGB Visible
                </button>
                <button
                  type="button"
                  onClick={() => setSpectralMode('NDVI')}
                  className={`px-2.5 py-1 rounded transition-all flex items-center gap-1 ${
                    spectralMode === 'NDVI'
                      ? 'bg-emerald-600 text-white shadow-xs'
                      : 'text-[var(--color-on-surface-secondary)] hover:text-[var(--color-on-surface)]'
                  }`}
                >
                  <Sparkles size={11} />
                  <span>NDVI Heatmap</span>
                </button>
                <button
                  type="button"
                  onClick={() => setSpectralMode('EDGE')}
                  className={`px-2.5 py-1 rounded transition-all ${
                    spectralMode === 'EDGE'
                      ? 'bg-slate-800 text-white shadow-xs'
                      : 'text-[var(--color-on-surface-secondary)] hover:text-[var(--color-on-surface)]'
                  }`}
                >
                  Lesion Edge
                </button>
              </div>
            </div>

            {/* Image Canvas with Zoom and Filter */}
            <div className="relative w-full h-84 rounded-xl overflow-hidden border border-[var(--color-outline-variant)] bg-black/95 flex items-center justify-center scanline-overlay">
              <SafeImage
                src={advisory.imageUrl}
                alt={advisory.diagnosisNameEn}
                style={{
                  transform: `scale(${zoomLevel})`,
                  ...getImageFilterStyle()
                }}
                className="max-h-full max-w-full object-contain cursor-grab select-none"
              />
              <div className="absolute top-2 left-2 px-2 py-0.5 rounded bg-black/70 backdrop-blur-xs text-[10px] text-emerald-400 font-mono flex items-center gap-1 border border-emerald-500/30">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping" />
                <span>SPECTRUM: {spectralMode}</span>
              </div>
              <div className="absolute bottom-2 right-2 px-2 py-0.5 rounded bg-black/70 backdrop-blur-xs text-[10px] text-white/80 font-mono">
                Zoom {Math.round(zoomLevel * 100)}%
              </div>
            </div>

            {/* Farmer & Location Metadata Card */}
            <div className="p-3 rounded-xl bg-[var(--color-surface-variant)] border border-[var(--color-outline-variant)] text-xs space-y-2">
              <div className="font-semibold text-[var(--color-on-surface)] flex items-center justify-between">
                <span className="flex items-center gap-1.5">
                  <User size={14} className="text-[var(--color-primary)]" />
                  {advisory.farmerContext.farmerName} ({advisory.farmerContext.phone})
                </span>
                <span className="text-[var(--color-on-surface-tertiary)] font-mono">
                  {advisory.farmerContext.farmAreaHa} Ha
                </span>
              </div>
              <div className="flex items-center gap-4 text-[var(--color-on-surface-secondary)] flex-wrap">
                <span className="flex items-center gap-1">
                  <MapPin size={12} />
                  {advisory.farmerContext.village}, {advisory.farmerContext.district}
                </span>
                <span>·</span>
                <span>
                  {advisory.farmerContext.crop} · <strong>{advisory.farmerContext.cultivar}</strong>
                </span>
                <span>·</span>
                <span>Planted: {advisory.farmerContext.plantingDate}</span>
              </div>
            </div>
          </div>

          {/* Model Prediction Probabilities Breakdown */}
          <div className="glass-panel p-4 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-xs font-bold uppercase tracking-wider text-[var(--color-on-surface-secondary)]">
                ONNX Model Class Probabilities (Top-3)
              </h3>
              <span className="text-[10px] font-mono bg-emerald-500/10 text-emerald-600 px-2 py-0.5 rounded font-bold border border-emerald-500/20">
                INT8 Quantized
              </span>
            </div>
            <div className="space-y-3">
              {advisory.modelProbabilities.map((prob) => (
                <div key={prob.className} className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="font-medium text-[var(--color-on-surface)]">
                      {prob.commonName}
                    </span>
                    <span className="font-mono font-bold text-[var(--color-primary)]">
                      {Math.round(prob.probability * 100)}%
                    </span>
                  </div>
                  <div className="w-full h-2 rounded-full bg-[var(--color-surface-variant)] overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-500"
                      style={{
                        width: `${prob.probability * 100}%`,
                        background:
                          prob.probability > 0.7
                            ? 'linear-gradient(90deg, #10B981 0%, #059669 100%)'
                            : prob.probability > 0.3
                            ? 'linear-gradient(90deg, #F59E0B 0%, #D97706 100%)'
                            : '#94A3B8'
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Agronomic Evidence, Environmental Indices & Action Console (7 cols) */}
        <div className="lg:col-span-7 space-y-5">
          {/* Diagnosis Headline */}
          <div className="glass-panel p-5 shadow-sm">
            <div className="flex items-start justify-between gap-3 mb-2">
              <div>
                <span className="text-xs font-semibold text-[var(--color-primary)] uppercase tracking-wider flex items-center gap-1">
                  <Sparkles size={13} />
                  <span>Automated AI Multi-Agent Finding</span>
                </span>
                <h2 className="text-xl font-bold text-[var(--color-on-surface)]">
                  {advisory.diagnosisNameEn}
                </h2>
                <div className="text-sm text-[var(--color-on-surface-secondary)] font-medium">
                  {advisory.diagnosisNameMl} ({advisory.pronunciationMl})
                </div>
              </div>
              <div className="text-right">
                <span className="text-xs text-[var(--color-on-surface-tertiary)] block">
                  Reported Stage
                </span>
                <span className="text-xs font-bold px-2.5 py-1 rounded-lg bg-[var(--color-primary-light)] text-[var(--color-primary-dark)] border border-[var(--color-primary-container)]">
                  {advisory.farmerContext.estimatedGrowthStage}
                </span>
              </div>
            </div>

            {/* Environmental Sensor / Weather Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 mt-4 pt-4 border-t border-[var(--color-outline-variant)] text-xs">
              <div className="p-3 rounded-xl bg-[var(--color-surface-variant)] flex items-center gap-2.5 border border-[var(--color-outline-variant)]">
                <Thermometer size={18} className="text-red-500 shrink-0" />
                <div>
                  <div className="text-[10px] text-[var(--color-on-surface-tertiary)]">Temp</div>
                  <strong className="font-mono text-sm">{advisory.weatherIndicators.temperatureC}°C</strong>
                </div>
              </div>

              <div className="p-3 rounded-xl bg-[var(--color-surface-variant)] flex items-center gap-2.5 border border-[var(--color-outline-variant)]">
                <Droplets size={18} className="text-blue-500 shrink-0" />
                <div>
                  <div className="text-[10px] text-[var(--color-on-surface-tertiary)]">Humidity</div>
                  <strong className="font-mono text-sm">{advisory.weatherIndicators.humidityPct}%</strong>
                </div>
              </div>

              <div className="p-3 rounded-xl bg-[var(--color-surface-variant)] flex items-center gap-2.5 border border-[var(--color-outline-variant)]">
                <CloudRain size={18} className="text-indigo-500 shrink-0" />
                <div>
                  <div className="text-[10px] text-[var(--color-on-surface-tertiary)]">3-Day Rain</div>
                  <strong className="font-mono text-sm">
                    {advisory.weatherIndicators.rainfallPast3DaysMm} mm
                  </strong>
                </div>
              </div>

              <div className="p-3 rounded-xl bg-[var(--color-surface-variant)] flex items-center gap-2.5 border border-[var(--color-outline-variant)]">
                <Wind size={18} className="text-emerald-500 shrink-0" />
                <div>
                  <div className="text-[10px] text-[var(--color-on-surface-tertiary)]">DFI Index</div>
                  <strong className="font-mono text-sm text-red-500">
                    {advisory.weatherIndicators.diseaseFavorabilityIndex}
                  </strong>
                </div>
              </div>
            </div>
          </div>

          {/* Evidence Bundle Component */}
          <EvidenceCard evidenceList={advisory.evidenceBundle} lang={lang} />

          {/* Statutory Chemical Safety Validation Panel */}
          <div className="glass-panel p-4 shadow-sm space-y-3 border-emerald-500/30">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-emerald-800 dark:text-emerald-400 flex items-center gap-2">
                <ShieldCheck size={18} className="text-[var(--color-primary)]" />
                <span>CIB&RC Statutory Chemical Registry Validation</span>
              </h3>
              <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 border border-emerald-500/20">
                {advisory.actionPlan.chemicalSafety.cibrcStatus}
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs bg-emerald-500/5 p-3 rounded-xl border border-emerald-500/10">
              <div>
                <span className="text-[var(--color-on-surface-tertiary)] block text-[11px]">
                  Active Ingredient
                </span>
                <strong className="text-[var(--color-on-surface)]">
                  {advisory.actionPlan.chemicalSafety.activeIngredient}
                </strong>
              </div>
              <div>
                <span className="text-[var(--color-on-surface-tertiary)] block text-[11px]">
                  CIB&RC Registration No.
                </span>
                <strong className="font-mono text-[var(--color-on-surface)]">
                  {advisory.actionPlan.chemicalSafety.cibrcRegNumber}
                </strong>
              </div>
              <div>
                <span className="text-[var(--color-on-surface-tertiary)] block text-[11px]">
                  Standard Dilution Ratio
                </span>
                <strong className="font-mono text-[var(--color-on-surface)]">
                  {advisory.actionPlan.chemicalSafety.dosagePerLiter}
                </strong>
              </div>
              <div>
                <span className="text-[var(--color-on-surface-tertiary)] block text-[11px]">
                  Recommended Commercial Formulations
                </span>
                <strong className="text-[var(--color-on-surface)]">
                  {advisory.actionPlan.chemicalSafety.commercialBrand}
                </strong>
              </div>
            </div>

            {advisory.actionPlan.chemicalSafety.phytotoxicityWarning && (
              <div className="text-xs text-amber-800 bg-amber-500/10 p-2.5 rounded-lg border border-amber-500/20 flex items-start gap-1.5">
                <AlertTriangle size={15} className="shrink-0 text-amber-600 mt-0.5" />
                <span>
                  <strong>Phytotoxicity Warning:</strong>{' '}
                  {advisory.actionPlan.chemicalSafety.phytotoxicityWarning}
                </span>
              </div>
            )}
          </div>

          {/* DSSAT Simulation Scenarios */}
          <ScenarioCard scenarios={advisory.scenarios} lang={lang} />

          {/* Government Scheme Linkage */}
          <SchemeCard schemes={advisory.schemesMatched} lang={lang} />

          {/* Agronomist Verdict Submission Form */}
          <form
            onSubmit={handleSubmit}
            className="glass-panel p-5 space-y-4 shadow-md border-emerald-500/40 relative overflow-hidden"
          >
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-[var(--color-on-surface)] flex items-center gap-2">
                <Pencil size={18} className="text-[var(--color-primary)]" />
                <span>Agronomist Clinical Certification Console</span>
              </h3>
              {isSubmitted && (
                <span className="text-xs font-bold text-emerald-800 bg-emerald-100 px-2.5 py-0.5 rounded-full flex items-center gap-1">
                  <CheckCircle2 size={13} />
                  <span>Verdict Dispatched</span>
                </span>
              )}
            </div>

            {/* Radio Verdict Selection */}
            <div className="grid grid-cols-3 gap-2.5">
              {[
                { value: 'AGREE', label: 'Agree with Diagnosis', icon: CheckCircle2, color: 'text-emerald-500' },
                { value: 'PARTIAL', label: 'Partial / Modify', icon: AlertTriangle, color: 'text-amber-500' },
                { value: 'DISAGREE', label: 'Override Diagnosis', icon: XCircle, color: 'text-red-500' }
              ].map((opt) => (
                <label
                  key={opt.value}
                  className={`flex flex-col items-center justify-center p-3 rounded-xl border text-xs font-semibold cursor-pointer transition-all ${
                    verdict === opt.value
                      ? 'bg-[var(--color-surface)] border-[var(--color-primary)] ring-2 ring-[var(--color-primary)]/20 shadow-md'
                      : 'bg-[var(--color-surface-variant)]/60 border-[var(--color-outline-variant)] hover:bg-[var(--color-surface-variant)]'
                  }`}
                >
                  <input
                    type="radio"
                    name="verdict"
                    value={opt.value}
                    checked={verdict === opt.value}
                    onChange={() => setVerdict(opt.value as any)}
                    className="sr-only"
                  />
                  <opt.icon size={20} className={`${opt.color} mb-1.5`} />
                  <span>{opt.label}</span>
                </label>
              ))}
            </div>

            {/* Notes Textarea */}
            <div>
              <label className="block text-xs font-semibold text-[var(--color-on-surface)] mb-1">
                Clinical Field Instructions & Notes for Farmer:
              </label>
              <textarea
                value={expertNotes}
                onChange={(e) => setExpertNotes(e.target.value)}
                rows={3}
                placeholder="Enter specific field instructions, dosage caveats, or physical sample collection requests..."
                className="w-full p-3 text-xs rounded-xl border border-[var(--color-outline)] bg-[var(--color-surface-variant)] text-[var(--color-on-surface)] focus:outline-none focus:border-[var(--color-primary)] transition-all"
              />
            </div>

            {/* Chemical Safety Verification Checkbox */}
            <label className="flex items-start gap-2.5 text-xs cursor-pointer select-none">
              <input
                type="checkbox"
                checked={safetyApproved}
                onChange={(e) => setSafetyApproved(e.target.checked)}
                className="mt-0.5 rounded text-[var(--color-primary)] focus:ring-[var(--color-primary)]"
              />
              <span className="text-[var(--color-on-surface)] leading-relaxed">
                I certify that the recommended fungicide/dosage has been cross-checked against the <strong>CIB&RC registered product schedule</strong>, respects harvest waiting intervals, and matches the crop phenology stage.
              </span>
            </label>

            {/* Submit Button */}
            <div className="flex justify-end gap-3 pt-2">
              <button
                type="submit"
                disabled={isSubmitted}
                className="btn btn-primary text-xs h-10 px-5 flex items-center gap-2"
              >
                <Send size={15} />
                <span>{isSubmitted ? 'Verdict Recorded' : 'Confirm & Dispatch to Farmer'}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};
