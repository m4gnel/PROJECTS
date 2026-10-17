import React, { useState } from 'react';
import { DiagnosticAdvisory } from '../types';
import { ConfidenceBadge } from '../components/common/ConfidenceBadge';
import { RiskBadge } from '../components/common/RiskBadge';
import { SafeImage } from '../components/common/SafeImage';
import {
  ShieldAlert,
  Search,
  Filter,
  Eye,
  CheckCircle,
  AlertTriangle,
  Clock,
  MapPin,
  Calendar,
  ChevronRight,
  TrendingUp,
  FileCheck
} from 'lucide-react';

interface ExpertDashboardProps {
  advisories: DiagnosticAdvisory[];
  onSelectAdvisory: (advisory: DiagnosticAdvisory) => void;
  lang?: 'en' | 'ml';
}

export const ExpertDashboard: React.FC<ExpertDashboardProps> = ({
  advisories,
  onSelectAdvisory,
  lang = 'en'
}) => {
  const [filterState, setFilterState] = useState<'ALL' | 'PENDING' | 'ESCALATED' | 'APPROVED'>('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCrop, setSelectedCrop] = useState<string>('ALL');

  const filteredAdvisories = advisories.filter((adv) => {
    const matchesFilter =
      filterState === 'ALL'
        ? true
        : filterState === 'PENDING'
        ? adv.triageStatus === 'PENDING_REVIEW'
        : filterState === 'ESCALATED'
        ? adv.triageStatus === 'ESCALATED'
        : adv.triageStatus === 'VERIFIED_APPROVED';

    const matchesCrop = selectedCrop === 'ALL' || adv.farmerContext.crop === selectedCrop;

    const matchesSearch =
      adv.farmerContext.farmerName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      adv.diagnosisNameEn.toLowerCase().includes(searchQuery.toLowerCase()) ||
      adv.farmerContext.district.toLowerCase().includes(searchQuery.toLowerCase()) ||
      adv.id.toLowerCase().includes(searchQuery.toLowerCase());

    return matchesFilter && matchesCrop && matchesSearch;
  });

  const pendingCount = advisories.filter((a) => a.triageStatus === 'PENDING_REVIEW').length;
  const escalatedCount = advisories.filter((a) => a.triageStatus === 'ESCALATED').length;
  const approvedCount = advisories.filter((a) => a.triageStatus === 'VERIFIED_APPROVED').length;

  return (
    <div className="space-y-6">
      {/* Top Banner & KPI Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-white border border-[var(--color-outline-variant)] shadow-xs">
          <div className="flex items-center justify-between text-xs text-[var(--color-on-surface-secondary)] mb-1">
            <span>Pending Triage Queue</span>
            <Clock size={16} className="text-amber-600" />
          </div>
          <div className="text-2xl font-bold text-[var(--color-on-surface)]">
            {pendingCount}
          </div>
          <div className="text-xs text-amber-700 font-medium mt-1">
            Requires Agronomist Audit
          </div>
        </div>

        <div className="p-4 rounded-xl bg-white border border-[var(--color-outline-variant)] shadow-xs">
          <div className="flex items-center justify-between text-xs text-[var(--color-on-surface-secondary)] mb-1">
            <span>Critical Escalations</span>
            <AlertTriangle size={16} className="text-[var(--color-risk-critical)]" />
          </div>
          <div className="text-2xl font-bold text-[var(--color-risk-critical)]">
            {escalatedCount}
          </div>
          <div className="text-xs text-red-700 font-medium mt-1">
            Low-Confidence & High-Severity
          </div>
        </div>

        <div className="p-4 rounded-xl bg-white border border-[var(--color-outline-variant)] shadow-xs">
          <div className="flex items-center justify-between text-xs text-[var(--color-on-surface-secondary)] mb-1">
            <span>Verified Approved</span>
            <CheckCircle size={16} className="text-[var(--color-primary)]" />
          </div>
          <div className="text-2xl font-bold text-[var(--color-primary-dark)]">
            {approvedCount}
          </div>
          <div className="text-xs text-emerald-700 font-medium mt-1">
            CIB&RC Safety Validated
          </div>
        </div>

        <div className="p-4 rounded-xl bg-white border border-[var(--color-outline-variant)] shadow-xs">
          <div className="flex items-center justify-between text-xs text-[var(--color-on-surface-secondary)] mb-1">
            <span>Model Agreement</span>
            <TrendingUp size={16} className="text-blue-600" />
          </div>
          <div className="text-2xl font-bold text-blue-700">92.4%</div>
          <div className="text-xs text-blue-600 font-medium mt-1">
            Validation Benchmark Target: &gt; 85%
          </div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 p-4 bg-white rounded-xl border border-[var(--color-outline-variant)] shadow-xs">
        <div className="flex items-center gap-2 flex-1 relative">
          <Search size={18} className="absolute left-3 text-[var(--color-on-surface-tertiary)]" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by farmer name, diagnosis, district, ID..."
            className="w-full pl-9 pr-4 py-2 text-sm rounded-lg border border-[var(--color-outline)] bg-[var(--color-surface-variant)] focus:outline-none focus:border-[var(--color-primary)] transition-all"
          />
        </div>

        <div className="flex items-center gap-2 flex-wrap">
          {/* Status Tabs */}
          <div className="flex p-1 rounded-lg bg-[var(--color-surface-variant)] border border-[var(--color-outline-variant)] text-xs font-semibold">
            {(['ALL', 'PENDING', 'ESCALATED', 'APPROVED'] as const).map((tab) => (
              <button
                key={tab}
                type="button"
                onClick={() => setFilterState(tab)}
                className={`px-3 py-1.5 rounded-md transition-all ${
                  filterState === tab
                    ? 'bg-white text-[var(--color-primary-dark)] shadow-xs'
                    : 'text-[var(--color-on-surface-secondary)] hover:text-[var(--color-on-surface)]'
                }`}
              >
                {tab === 'ALL'
                  ? 'All Records'
                  : tab === 'PENDING'
                  ? 'Pending'
                  : tab === 'ESCALATED'
                  ? 'Escalated'
                  : 'Approved'}
              </button>
            ))}
          </div>

          {/* Crop Selector */}
          <select
            value={selectedCrop}
            onChange={(e) => setSelectedCrop(e.target.value)}
            className="px-3 py-2 text-xs font-semibold rounded-lg border border-[var(--color-outline)] bg-white text-[var(--color-on-surface)] focus:outline-none focus:border-[var(--color-primary)]"
          >
            <option value="ALL">All Crops</option>
            <option value="Rice">Rice (Paddy)</option>
            <option value="Banana">Banana</option>
            <option value="Coconut">Coconut</option>
            <option value="Tomato">Tomato</option>
            <option value="Maize">Maize</option>
          </select>
        </div>
      </div>

      {/* Advisory Queue List */}
      <div className="bg-white rounded-xl border border-[var(--color-outline-variant)] shadow-xs overflow-hidden">
        <div className="p-4 border-b border-[var(--color-outline-variant)] bg-[var(--color-surface-variant)]/60 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <FileCheck size={18} className="text-[var(--color-primary)]" />
            <h3 className="text-sm font-bold text-[var(--color-on-surface)]">
              Diagnostic Triage Queue ({filteredAdvisories.length})
            </h3>
          </div>
          <span className="text-xs text-[var(--color-on-surface-secondary)]">
            Click any row to open the Split-Screen Audit Inspector
          </span>
        </div>

        <div className="divide-y divide-[var(--color-outline-variant)]">
          {filteredAdvisories.length === 0 ? (
            <div className="p-8 text-center text-sm text-[var(--color-on-surface-secondary)]">
              No advisory records match the active filter criteria.
            </div>
          ) : (
            filteredAdvisories.map((adv) => (
              <div
                key={adv.id}
                onClick={() => onSelectAdvisory(adv)}
                className="p-4 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 hover:bg-[var(--color-primary-light)]/40 transition-colors cursor-pointer group"
              >
                {/* Left: Thumbnail & Core Diagnosis */}
                <div className="flex items-center gap-3.5 flex-1 min-w-0">
                  <div className="relative w-14 h-14 rounded-lg overflow-hidden shrink-0 border border-[var(--color-outline-variant)] bg-black/5">
                    <SafeImage
                      src={adv.imageThumbnail}
                      alt={adv.diagnosisNameEn}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                    />
                    {adv.triageStatus === 'ESCALATED' && (
                      <span className="absolute top-1 right-1 w-2.5 h-2.5 rounded-full bg-[var(--color-risk-critical)] ring-2 ring-white" />
                    )}
                  </div>

                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2 flex-wrap mb-1">
                      <span className="text-xs font-mono text-[var(--color-on-surface-tertiary)]">
                        {adv.id}
                      </span>
                      <ConfidenceBadge state={adv.confidence} score={adv.confidenceScore} />
                      <RiskBadge level={adv.severityRisk} />
                    </div>

                    <h4 className="text-sm font-bold text-[var(--color-on-surface)] truncate">
                      {adv.diagnosisNameEn}
                      <span className="ml-2 font-normal text-xs text-[var(--color-on-surface-secondary)]">
                        ({adv.diagnosisNameMl})
                      </span>
                    </h4>

                    <div className="flex items-center gap-3 text-xs text-[var(--color-on-surface-secondary)] mt-1 flex-wrap">
                      <span className="flex items-center gap-1">
                        <strong>Farmer:</strong> {adv.farmerContext.farmerName}
                      </span>
                      <span>·</span>
                      <span className="flex items-center gap-1">
                        <MapPin size={12} />
                        {adv.farmerContext.village}, {adv.farmerContext.district}
                      </span>
                      <span>·</span>
                      <span>
                        {adv.farmerContext.crop} ({adv.farmerContext.cultivar})
                      </span>
                    </div>
                  </div>
                </div>

                {/* Right: Stage, Action, and Action Button */}
                <div className="flex items-center gap-4 shrink-0 w-full md:w-auto justify-between md:justify-end border-t md:border-t-0 pt-2 md:pt-0">
                  <div className="text-right text-xs hidden sm:block">
                    <div className="text-[var(--color-on-surface-tertiary)]">Growth Stage</div>
                    <div className="font-semibold text-[var(--color-on-surface)]">
                      {adv.farmerContext.estimatedGrowthStage}
                    </div>
                  </div>

                  <button
                    type="button"
                    className="btn btn-secondary text-xs h-9 px-3 flex items-center gap-1.5"
                  >
                    <Eye size={14} />
                    <span>Audit Review</span>
                    <ChevronRight size={14} />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
