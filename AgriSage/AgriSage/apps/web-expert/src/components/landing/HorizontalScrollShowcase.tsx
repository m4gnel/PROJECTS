import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import {
  Satellite,
  ScanLine,
  Brain,
  Beaker,
  MessageCircleHeart,
} from 'lucide-react';
import { getPublicUrl } from '../../lib/utils';

gsap.registerPlugin(ScrollTrigger);

/* ─── Pipeline stage data ────────────────────────────────────── */
const PIPELINE_STAGES = [
  {
    id: 'ingest',
    title: 'Space-to-Soil Data Ingestion',
    subtitle: 'Sentinel-2 MSI · 10 m Resolution · 5-Day Revisit',
    description:
      'Multi-spectral satellite imagery flows through our edge pipeline, converting raw top-of-atmosphere radiance to surface reflectance in under 3 seconds per tile.',
    stat: { value: '10', unit: 'm', label: 'Spatial Resolution' },
    Icon: Satellite,
    gradient: 'from-emerald-950/90 to-teal-950/90',
    accent: '#10b981',
    bgImage: getPublicUrl('/images/hero_earth.jpg'),
  },
  {
    id: 'spectral',
    title: 'Spectral Band Decomposition',
    subtitle: 'RGB · Red Edge · NIR · SWIR · Thermal',
    description:
      'Each pixel decomposes into 13 spectral bands. Custom NDVI / NDRE algorithms detect chlorophyll degradation 14 days before visible chlorosis.',
    stat: { value: '13', unit: '', label: 'Spectral Bands' },
    Icon: ScanLine,
    gradient: 'from-purple-950/90 to-violet-950/90',
    accent: '#a855f7',
    bgImage: getPublicUrl('/images/cellular_macro.jpg'),
  },
  {
    id: 'neural',
    title: 'Neural Network Inference',
    subtitle: 'Vision Transformer · 98.7 % Crop Classification',
    description:
      'A fine-tuned ViT model processes spectral tensors through 12 attention layers, classifying crop health across 47 pathological categories.',
    stat: { value: '98.7', unit: '%', label: 'Accuracy' },
    Icon: Brain,
    gradient: 'from-cyan-950/90 to-blue-950/90',
    accent: '#06b6d4',
    bgImage: getPublicUrl('/images/network_globe.jpg'),
  },
  {
    id: 'simulation',
    title: 'Digital Twin Simulation',
    subtitle: 'DSSAT v4.8 · 10 000 Monte Carlo Runs',
    description:
      'Biophysical models simulate root water uptake, transpiration efficiency, and phenological development across 14-day yield projection horizons.',
    stat: { value: '14', unit: 'd', label: 'Forecast Horizon' },
    Icon: Beaker,
    gradient: 'from-amber-950/90 to-orange-950/90',
    accent: '#f59e0b',
    bgImage: getPublicUrl('/images/crop_split.jpg'),
  },
  {
    id: 'advisory',
    title: 'Actionable Farmer Advisory',
    subtitle: 'Vernacular Voice · 22 Indian Languages · WhatsApp',
    description:
      "The final output: a clear, actionable advisory delivered in the farmer's mother tongue via voice call, SMS, or WhatsApp — no smartphone required.",
    stat: { value: '22', unit: '', label: 'Languages' },
    Icon: MessageCircleHeart,
    gradient: 'from-green-950/90 to-emerald-950/90',
    accent: '#22c55e',
    bgImage: getPublicUrl('/images/farmer_tablet.jpg'),
  },
] as const;

/**
 * HorizontalScrollShowcase
 *
 * A pinned section with 5 full-viewport panels that translate
 * horizontally as the user scrolls vertically. Each panel reveals
 * one stage of the Agri-SAGE intelligence pipeline.
 *
 * Performance:
 * – Single GSAP tween with scrub: translate3d (GPU-composited)
 * – Per-panel reveals use containerAnimation for zero extra layout
 * – Snap between panels for polished touch / trackpad feel
 * – Images lazy-loaded after first panel
 */
export function HorizontalScrollShowcase() {
  const sectionRef = useRef<HTMLElement>(null);
  const trackRef   = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const section = sectionRef.current;
    const track   = trackRef.current;
    if (!section || !track) return;

    const ctx = gsap.context(() => {
      const panels = gsap.utils.toArray<HTMLElement>('.h-panel', track);
      if (!panels.length) return;

      /* ── Main horizontal scroll tween ─────────────────────────── */
      const getScrollDistance = () => Math.max(track.scrollWidth - section.offsetWidth, (panels.length - 1) * window.innerWidth);
      
      const scrollTween = gsap.to(track, {
        x: () => -getScrollDistance(),
        ease: 'none',
        scrollTrigger: {
          trigger: section,
          start: 'top top',
          end: () => `+=${getScrollDistance()}`,
          scrub: 0.5,
          pin: true,
          pinSpacing: true,
          anticipatePin: 1,
          invalidateOnRefresh: true,
          snap: {
            snapTo: 1 / (panels.length - 1),
            duration: 0.4,
            ease: 'power2.inOut',
          },
        },
      });

      /* ── Per-panel reveals (Layers sliding from LEFT to RIGHT while scrolling) ── */
      panels.forEach((panel, idx) => {
        const content = panel.querySelector<HTMLElement>('.h-panel-content');
        const stat    = panel.querySelector<HTMLElement>('.h-panel-stat');
        const bg      = panel.querySelector<HTMLElement>('.h-panel-bg');

        if (content) {
          gsap.fromTo(content,
            { x: idx === 0 ? 0 : -220, opacity: idx === 0 ? 1 : 0, scale: idx === 0 ? 1 : 0.92 },
            {
              x: 0, opacity: 1, scale: 1,
              duration: 0.7,
              ease: 'power3.out',
              scrollTrigger: {
                trigger: panel,
                containerAnimation: scrollTween,
                start: 'left 95%',
                end: 'left 25%',
                scrub: true,
              },
            }
          );
        }

        if (stat) {
          gsap.fromTo(stat,
            { x: idx === 0 ? 0 : -140, scale: idx === 0 ? 1 : 0.78, opacity: idx === 0 ? 1 : 0 },
            {
              x: 0, scale: 1, opacity: 1,
              duration: 0.5,
              ease: 'back.out(1.5)',
              scrollTrigger: {
                trigger: panel,
                containerAnimation: scrollTween,
                start: 'left 80%',
                end: 'left 15%',
                scrub: true,
              },
            }
          );
        }

        if (bg) {
          gsap.fromTo(bg,
            { x: -120, scale: 1.18 },
            {
              x: 0, scale: 1,
              ease: 'none',
              scrollTrigger: {
                trigger: panel,
                containerAnimation: scrollTween,
                start: 'left right',
                end: 'right left',
                scrub: true,
              },
            }
          );
        }
      });

      /* ── Progress bar ─────────────────────────────────────────── */
      const bar = section.querySelector<HTMLElement>('.h-progress-bar');
      if (bar) {
        gsap.fromTo(bar,
          { scaleX: 0 },
          {
            scaleX: 1,
            ease: 'none',
            scrollTrigger: {
              trigger: section,
              start: 'top top',
              end: () => `+=${getScrollDistance()}`,
              scrub: true,
            },
          }
        );
      }
      /* ── Force refresh ScrollTrigger positions after pin spacer creation ── */
      setTimeout(() => {
        ScrollTrigger.refresh();
      }, 100);
    }, section);

    return () => ctx.revert();
  }, []);

  return (
    <section
      ref={sectionRef}
      className="horizontal-scroll-section relative z-20 w-full h-screen overflow-hidden bg-slate-950"
    >
      {/* ── Progress bar ──────────────────────────────────────── */}
      <div className="absolute top-0 left-0 right-0 h-1 bg-white/5 z-30">
        <div
          className="h-progress-bar h-full bg-gradient-to-r from-emerald-500 via-teal-400 to-cyan-400 origin-left will-change-transform"
          style={{ transform: 'scaleX(0)' }}
        />
      </div>

      {/* ── Header badge ──────────────────────────────────────── */}
      <div className="absolute top-6 left-6 z-30 flex items-center gap-2.5 px-4 py-2 rounded-2xl bg-slate-950/80 backdrop-blur-xl border border-emerald-500/20 text-xs font-mono select-none">
        <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
        <span className="text-emerald-400 font-bold uppercase tracking-widest">
          Intelligence Pipeline
        </span>
        <span className="text-slate-500 hidden sm:inline">· Scroll →</span>
      </div>

      {/* ── Step dots ─────────────────────────────────────────── */}
      <div className="absolute top-6 right-6 z-30 flex items-center gap-2 px-3 py-2 rounded-xl bg-slate-950/80 backdrop-blur-xl border border-white/10 text-xs font-mono text-slate-400">
        {PIPELINE_STAGES.map((s) => (
          <div
            key={s.id}
            className="w-2 h-2 rounded-full"
            style={{ backgroundColor: s.accent + '60' }}
          />
        ))}
      </div>

      {/* ── Horizontal track ──────────────────────────────────── */}
      <div
        ref={trackRef}
        className="horizontal-scroll-track flex h-full will-change-transform"
      >
        {PIPELINE_STAGES.map((stage, i) => {
          const total = PIPELINE_STAGES.length;
          return (
            <div
              key={stage.id}
              className="h-panel flex-none w-screen h-full relative overflow-hidden"
            >
              {/* Background */}
              <div className="h-panel-bg absolute inset-0 will-change-transform">
                <img
                  src={stage.bgImage}
                  alt=""
                  className="w-full h-full object-cover"
                  loading={i === 0 ? 'eager' : 'lazy'}
                />
                <div
                  className={`absolute inset-0 bg-gradient-to-br ${stage.gradient}`}
                />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-slate-950/40" />
              </div>

              {/* Content */}
              <div className="h-panel-content relative z-10 flex flex-col justify-center h-full px-8 md:px-20 max-w-3xl will-change-transform">
                {/* Stage number + icon */}
                <div className="flex items-center gap-3 mb-6">
                  <div
                    className="w-12 h-12 rounded-2xl flex items-center justify-center border border-white/20 backdrop-blur-xl"
                    style={{ backgroundColor: stage.accent + '20' }}
                  >
                    <stage.Icon size={22} style={{ color: stage.accent }} />
                  </div>
                  <div className="flex items-center gap-2">
                    <span
                      className="text-5xl font-black font-mono"
                      style={{ color: stage.accent }}
                    >
                      {String(i + 1).padStart(2, '0')}
                    </span>
                    <span className="text-xs text-white/40 font-mono uppercase tracking-widest">
                      / {String(total).padStart(2, '0')}
                    </span>
                  </div>
                </div>

                {/* Title */}
                <h3 className="text-3xl md:text-5xl lg:text-6xl font-black text-white tracking-tight leading-[1.1] mb-3">
                  {stage.title}
                </h3>

                {/* Subtitle */}
                <p
                  className="text-sm md:text-base font-mono font-semibold mb-6"
                  style={{ color: stage.accent }}
                >
                  {stage.subtitle}
                </p>

                {/* Description */}
                <p className="text-base md:text-lg text-white/70 leading-relaxed max-w-xl mb-8">
                  {stage.description}
                </p>

                {/* Stat badge */}
                <div className="h-panel-stat inline-flex items-baseline gap-1 px-5 py-3 rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10 w-fit will-change-transform">
                  <span className="text-4xl font-black font-mono text-white">
                    {stage.stat.value}
                  </span>
                  <span
                    className="text-lg font-bold"
                    style={{ color: stage.accent }}
                  >
                    {stage.stat.unit}
                  </span>
                  <span className="text-xs text-white/50 font-mono ml-2 uppercase tracking-wider">
                    {stage.stat.label}
                  </span>
                </div>
              </div>

              {/* Decorative corner accent */}
              <div
                className="absolute bottom-0 right-0 w-1/3 h-1/3 opacity-20 pointer-events-none"
                style={{
                  background: `radial-gradient(circle at 100% 100%, ${stage.accent}, transparent 70%)`,
                }}
              />

              {/* Subtle grid overlay */}
              <div className="absolute inset-0 opacity-[0.03] pointer-events-none bg-[length:40px_40px] bg-[image:linear-gradient(to_right,white_1px,transparent_1px),linear-gradient(to_bottom,white_1px,transparent_1px)]" />
            </div>
          );
        })}
      </div>
    </section>
  );
}

export default HorizontalScrollShowcase;
