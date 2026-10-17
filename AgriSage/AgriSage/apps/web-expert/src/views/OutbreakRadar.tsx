import React, { useState } from 'react';
import { REGIONAL_OUTBREAKS } from '../data/seedData';
import { RiskBadge } from '../components/common/RiskBadge';
import {
  Radio,
  CloudRain,
  MapPin,
  Users,
  ShieldAlert,
  Sliders,
  Wind,
  Compass,
  AlertTriangle,
  Activity,
  Layers
} from 'lucide-react';

export const OutbreakRadar: React.FC = () => {
  const [spreadDaysAhead, setSpreadDaysAhead] = useState<number>(3);

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Top Futuristic Command Header */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[var(--color-surface-elevated)] via-[var(--color-surface)] to-[var(--color-surface-variant)] border border-emerald-500/30 p-6 shadow-md flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="relative z-10 max-w-2xl">
          <div className="flex items-center gap-2 mb-2">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </span>
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-500">
              Live Agricultural Bio-Surveillance Grid
            </span>
          </div>
          <h2 className="text-2xl font-black text-[var(--color-on-surface)] tracking-tight">
            Regional Phytosanitary & Pathogen Outbreak Radar
          </h2>
          <p className="text-xs text-[var(--color-on-surface-secondary)] mt-1.5 leading-relaxed">
            Multi-agent epidemiological tracker correlating farmer field submissions with real-time IMD microclimate telemetry to predict disease vector migration and spore dispersion.
          </p>
        </div>

        {/* Live Surveillance Radar Simulation Dial */}
        <div className="relative z-10 flex items-center gap-4 bg-[var(--color-surface-glass)] backdrop-blur-md px-5 py-3 rounded-2xl border border-[var(--color-outline-variant)] shadow-sm shrink-0">
          <div className="text-center">
            <div className="text-[10px] uppercase font-bold text-[var(--color-on-surface-tertiary)]">
              Active Zones
            </div>
            <strong className="text-xl font-black text-emerald-500">4 Districts</strong>
          </div>
          <div className="w-px h-10 bg-[var(--color-outline-variant)]" />
          <div className="text-center">
            <div className="text-[10px] uppercase font-bold text-[var(--color-on-surface-tertiary)]">
              Monitored Fields
            </div>
            <strong className="text-xl font-black text-[var(--color-on-surface)]">
              {Math.round(332 * (1 + spreadDaysAhead * 0.18))}
            </strong>
          </div>
          <div className="w-px h-10 bg-[var(--color-outline-variant)]" />
          <div className="text-center">
            <div className="text-[10px] uppercase font-bold text-[var(--color-on-surface-tertiary)]">
              Vectors Blocked
            </div>
            <strong className="text-xl font-black text-cyan-500">98.4%</strong>
          </div>
        </div>

        {/* Ambient background ring */}
        <div className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-1/4 w-96 h-96 rounded-full border border-emerald-500/10 pointer-events-none radar-ping" />
      </div>

      {/* Pathogen Dispersion Predictive Timeline Slider */}
      <div className="glass-panel p-4 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-500">
            <Activity size={18} />
          </div>
          <div>
            <h4 className="text-xs font-bold text-[var(--color-on-surface)]">
              Pathogen Spore Dispersion Simulator (IMD Wind & Humidity Trajectory)
            </h4>
            <span className="text-[11px] text-[var(--color-on-surface-secondary)]">
              Simulating disease transmission forward across micro-basins
            </span>
          </div>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-72">
          <span className="text-xs font-mono font-bold text-[var(--color-primary)] shrink-0">
            + {spreadDaysAhead} Days
          </span>
          <input
            type="range"
            min="1"
            max="14"
            value={spreadDaysAhead}
            onChange={(e) => setSpreadDaysAhead(Number(e.target.value))}
            className="w-full accent-emerald-500 cursor-pointer"
          />
        </div>
      </div>

      {/* Outbreak Cluster Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {REGIONAL_OUTBREAKS.map((outbreak) => {
          const projectedFarms = Math.round(outbreak.affectedFarmsReported * (1 + spreadDaysAhead * 0.22));

          return (
            <div
              key={outbreak.id}
              className="glass-panel p-5 space-y-4 hover:border-emerald-500/50 transition-all group relative overflow-hidden"
            >
              {/* Top Row: Diagnosis & Badges */}
              <div className="flex items-start justify-between gap-3">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-mono text-[var(--color-on-surface-tertiary)]">
                      {outbreak.id}
                    </span>
                    <span className="text-xs font-bold text-[var(--color-primary)] flex items-center gap-1">
                      <MapPin size={12} />
                      {outbreak.district} Cluster
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-[var(--color-on-surface)] group-hover:text-emerald-500 transition-colors">
                    {outbreak.disease}
                  </h3>
                  <span className="text-xs font-semibold text-[var(--color-on-surface-secondary)]">
                    Primary Host: <strong>{outbreak.crop}</strong>
                  </span>
                </div>
                <RiskBadge level={outbreak.severity} />
              </div>

              {/* Sensor & Telemetry Metrics */}
              <div className="grid grid-cols-3 gap-2.5 text-xs bg-[var(--color-surface-variant)] p-3 rounded-xl border border-[var(--color-outline-variant)]">
                <div>
                  <span className="text-[10px] text-[var(--color-on-surface-tertiary)] block">
                    Current Reports
                  </span>
                  <strong className="text-sm font-bold text-[var(--color-on-surface)]">
                    {outbreak.affectedFarmsReported}
                  </strong>
                </div>

                <div>
                  <span className="text-[10px] text-[var(--color-on-surface-tertiary)] block">
                    Projected (+{spreadDaysAhead}d)
                  </span>
                  <strong className="text-sm font-bold text-red-500">
                    {projectedFarms} farms
                  </strong>
                </div>

                <div>
                  <span className="text-[10px] text-[var(--color-on-surface-tertiary)] block">
                    Coordinates
                  </span>
                  <span className="font-mono text-[11px] font-semibold text-[var(--color-on-surface)]">
                    {outbreak.coordinates[0].toFixed(2)}°, {outbreak.coordinates[1].toFixed(2)}°
                  </span>
                </div>
              </div>

              {/* Weather Driver Card */}
              <div className="flex items-start gap-2 text-xs text-[var(--color-on-surface-secondary)] bg-blue-500/5 p-3 rounded-xl border border-blue-500/15">
                <CloudRain size={16} className="text-blue-500 shrink-0 mt-0.5" />
                <div>
                  <strong className="text-[var(--color-on-surface)] block mb-0.5">
                    Microclimatic Trigger Condition:
                  </strong>
                  <span>{outbreak.weatherConditionFactor}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Geospatial Legend & Protocols */}
      <div className="glass-panel p-4 flex items-center justify-between text-xs text-[var(--color-on-surface-secondary)]">
        <div className="flex items-center gap-2">
          <ShieldAlert size={16} className="text-amber-500" />
          <span>
            Automated alerts are dispatched to smallholders when the <strong>Disease Favorability Index &gt; 0.75</strong> within their 15km cluster zone.
          </span>
        </div>
      </div>
    </div>
  );
};
