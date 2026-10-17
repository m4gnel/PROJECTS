import React, { useState, useEffect, useRef, useMemo } from 'react';
import {
  Sprout,
  ShieldCheck,
  Cpu,
  ArrowRight,
  Sparkles,
  Layers,
  Smartphone,
  CheckCircle2,
  Lock,
  Globe,
  Radio,
  BarChart3,
  Sun,
  Moon,
  Thermometer,
  Droplets,
  CloudRain,
  Eye,
  Activity,
  Sliders,
  Calendar,
  Zap,
  TrendingDown,
  TrendingUp,
  MapPin,
  ChevronDown,
  Play,
  RotateCcw,
  Volume2,
  VolumeX,
  Share2,
  Compass,
  Crosshair,
  Microscope,
  Send,
  Check,
  AlertTriangle,
  Search,
  Scan
} from 'lucide-react';
import { ThreeHeroCanvas } from '../components/landing/ThreeHeroCanvas';
import { GlassTiltCard } from '../components/landing/GlassTiltCard';
import { playHoverChime, playSuccessTone, toggleAudioMute, getAudioMuteState } from '../utils/audioFX';
import { getPublicUrl } from '../lib/utils';

import { useScrollTriggerSnap } from '../hooks/useScrollTriggerSnap';
import { useParallaxLayers } from '../hooks/useParallaxLayers';
import { useScrollSequence } from '../hooks/useScrollSequence';
import { DewdropScrollTracker } from '../components/landing/DewdropScrollTracker';
import { AppleGrowthScrollytelling } from '../components/landing/AppleGrowthScrollytelling';
import { useSplitTypography } from '../hooks/useSplitTypography';
import { ParallaxComponent } from '../components/ui/parallax-scrolling';
import { SqueezeCarouselDemo } from '../components/ui/carousel-squeeze-demo';
import { ShaderBackground } from '../components/ui/mesh-drift-shader';
import { HorizontalScrollShowcase } from '../components/landing/HorizontalScrollShowcase';
import HoverFooter from '../components/ui/hover-footer';
import { useScrollytelling } from '../hooks/useScrollytelling';
import Lenis from 'lenis';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';


interface PublicLandingPageProps {
  onEnterAuth: () => void;
  onDirectPlatformAccess: () => void;
  lang: 'en' | 'ml';
  onToggleLang: () => void;
  theme: 'dark' | 'light';
  onToggleTheme: () => void;
}

export const PublicLandingPage: React.FC<PublicLandingPageProps> = ({
  onEnterAuth,
  onDirectPlatformAccess,
  lang,
  onToggleLang,
  theme,
  onToggleTheme
}) => {
  // GSAP-style ScrollTrigger & Snap Controller
  const { activeChapter, scrollProgress, scrollToChapter } = useScrollTriggerSnap({
    totalChapters: 12
  });

  // SplitType Kinetic Typography for major chapter headlines
  const heroTitleRef = useSplitTypography<HTMLHeadingElement>({ duration: 1.2, stagger: 0.04 });
  const problemTitleRef = useSplitTypography<HTMLHeadingElement>({ duration: 1.0, stagger: 0.035 });
  const farmTitleRef = useSplitTypography<HTMLHeadingElement>({ duration: 1.0, stagger: 0.035 });
  const invisibleTitleRef = useSplitTypography<HTMLHeadingElement>({ duration: 1.0, stagger: 0.035 });
  const neuralTitleRef = useSplitTypography<HTMLHeadingElement>({ duration: 1.0, stagger: 0.035 });
  const swarmTitleRef = useSplitTypography<HTMLHeadingElement>({ duration: 1.0, stagger: 0.035 });
  const ctaTitleRef = useSplitTypography<HTMLHeadingElement>({ duration: 1.2, stagger: 0.04 });

  // Page container reference for Framer Motion useScroll & Sticky tracking
  const landingPageRef = useRef<HTMLDivElement>(null);

  // Multi-Layer Parallax Floating Decorations Engine
  useParallaxLayers();

  // Master GSAP ScrollTrigger Orchestrator (batch reveals, hero zoom, ambient glow, velocity, counters, depth parallax)
  useScrollytelling(landingPageRef);

  // Scroll-Scrubbed Image Sequence (Video-to-JPG Effect)
  const scrollSeqContainerRef = useRef<HTMLDivElement>(null);
  const scrollSeqCanvasRef = useRef<HTMLCanvasElement>(null);
  const sproutFrameUrls = useMemo(() => [
    getPublicUrl('/images/seq_sprout_01.jpg'),
    getPublicUrl('/images/seq_sprout_02.jpg'),
    getPublicUrl('/images/seq_sprout_03.jpg'),
    getPublicUrl('/images/seq_sprout_04.jpg'),
    getPublicUrl('/images/seq_sprout_05.jpg')
  ], []);

  useScrollSequence({
    frameUrls: sproutFrameUrls,
    containerRef: scrollSeqContainerRef,
    canvasRef: scrollSeqCanvasRef
  });

  const [heroViewMode, setHeroViewMode] = useState<'orbit' | 'macro'>('macro');
  const [audioMuted, setAudioMuted] = useState(true);

  // Master Chapter Directory Navigation Metadata
  const CHAPTERS_NAV = useMemo(() => [
    { id: 1, title: 'Hero & Mission', desc: 'Planetary to Cellular AI Guidance', icon: Sprout, color: '#10b981' },
    { id: 2, title: 'Pathogen Genesis', desc: 'Invisible Early Infection Detection', icon: AlertTriangle, color: '#f59e0b' },
    { id: 3, title: 'Farm 360', desc: 'Digital Twin & Multi-Sensor Fusion', icon: Layers, color: '#0ea5e9' },
    { id: 4, title: 'Sub-Surface Stress', desc: 'Multi-Spectral Stomata Conductance', icon: Eye, color: '#06b6d4' },
    { id: 5, title: 'Neural Core', desc: 'Biophysical INT8 AI Pipeline', icon: Cpu, color: '#8b5cf6' },
    { id: 6, title: 'Multi-Agent Swarm', desc: 'Autonomous Agronomist Ensemble', icon: Radio, color: '#3b82f6' },
    { id: 7, title: 'Crop Simulator', desc: '14-Day Predictive Growth Projection', icon: Sliders, color: '#22c55e' },
    { id: 8, title: 'Risk Reduction', desc: 'Systematic Yield Protection 72% → 10%', icon: ShieldCheck, color: '#6366f1' },
    { id: 9, title: 'Farmer Advisory', desc: 'Audio & WhatsApp Local Guidance', icon: Activity, color: '#eab308' },
    { id: 10, title: 'Global Twin', desc: 'Planetary Farm Network Mesh', icon: Globe, color: '#0ea5e9' },
    { id: 11, title: 'Workstation', desc: 'Quantum Executive Console', icon: BarChart3, color: '#10b981' },
    { id: 12, title: 'Singularity Call', desc: 'Transforming Agriculture Today', icon: Zap, color: '#10b981' }
  ], []);

  // Frame 1 Interactive Elevation & Chapter Drawer States
  const [isChapterDrawerOpen, setIsChapterDrawerOpen] = useState(false);
  const [isThermalScanActive, setIsThermalScanActive] = useState(false);
  const [activeHudMetric, setActiveHudMetric] = useState<'temp' | 'moisture' | 'humidity' | 'disease'>('temp');
  const [heroSearchQuery, setHeroSearchQuery] = useState('');
  const [isSimulating, setIsSimulating] = useState(false);
  const [simResult, setSimResult] = useState<{ title: string; subtitle: string; score: string } | null>(null);

  // Zero-lag CSS-variable mouse spotlight (NO React re-renders)
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      document.documentElement.style.setProperty('--mouse-x', `${e.clientX}px`);
      document.documentElement.style.setProperty('--mouse-y', `${e.clientY}px`);
    };
    window.addEventListener('mousemove', handleMouseMove, { passive: true });
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const handleHeroSimulate = (query: string) => {
    playHoverChime(700);
    setIsSimulating(true);
    setSimResult(null);
    setTimeout(() => {
      playSuccessTone();
      setIsSimulating(false);
      const cropName = query.trim() ? query.trim() : 'Palakkad Paddy Hectare #04';
      setSimResult({
        title: `AI Diagnostic: ${cropName}`,
        subtitle: 'Canopy Transpiration Optimal · Spore Genesis Risk: <3.2% · INT8 Biophysical Model Checked',
        score: '98.6% Health Score'
      });
    }, 1100);
  };
  
  // Chapter 02: Problem Split View Slider
  const [splitSliderPos, setSplitSliderPos] = useState(50);
  const [activeStressStage, setActiveStressStage] = useState<number>(4);
  const splitContainerRef = useRef<HTMLDivElement>(null);

  // Chapter 03: Farm Layer Selector
  const [selectedFarmLayer, setSelectedFarmLayer] = useState<'all' | 'satellite' | 'weather' | 'soil' | 'irrigation' | 'sensors' | 'farmer'>('all');

  // Chapter 04: Microscope Spectral Band
  const [spectralBand, setSpectralBand] = useState<'rgb' | 'rededge' | 'nir' | 'thermal'>('nir');

  // Chapter 05: Pipeline Step
  const [activePipelineStep, setActivePipelineStep] = useState(1);

  // Chapter 06: Multi-Agent Hub Selector
  const [selectedAgentId, setSelectedAgentId] = useState<'vision' | 'weather' | 'crop' | 'sim' | 'critic' | 'voice'>('sim');

  // Chapter 07: Crop Simulation Horizon
  const [simDays, setSimDays] = useState<'1' | '3' | '7' | '14'>('7');

  // Chapter 08: Risk Mitigation Interactive State
  const [riskSimulated, setRiskSimulated] = useState(false);

  // Chapter 09: Audio Advisory & WhatsApp Feedback
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const [shareSent, setShareSent] = useState(false);

  // Chapter 10: Global Farm Network Cluster
  const [selectedCluster, setSelectedCluster] = useState<'kerala' | 'punjab' | 'maharashtra' | 'california' | 'africa'>('kerala');

  // Chapter 11: Workstation Tab Preview
  const [platformTab, setPlatformTab] = useState<'triage' | 'multispectral' | 'radar' | 'simulator'>('triage');

  // Initialize audio state
  useEffect(() => {
    setAudioMuted(getAudioMuteState());
  }, []);

  // Master Lenis Smooth Scroll Engine + GSAP Ticker Integration
  useEffect(() => {
    let lenisInstance: Lenis | null = null;
    let updateTicker: ((time: number) => void) | null = null;

    try {
      lenisInstance = new Lenis({
        lerp: 0.08,
        smoothWheel: true,
        wheelMultiplier: 1.0,
        touchMultiplier: 1.5,
        infinite: false,
        autoResize: true,
      });

      lenisInstance.on('scroll', ScrollTrigger.update);

      updateTicker = (time: number) => {
        lenisInstance?.raf(time * 1000);
      };

      gsap.ticker.add(updateTicker);
      gsap.ticker.lagSmoothing(0);
    } catch {
      // Graceful fallback
    }

    return () => {
      if (lenisInstance) {
        lenisInstance.destroy();
      }
      if (updateTicker) {
        gsap.ticker.remove(updateTicker);
      }
    };
  }, []);

  const handleAudioToggle = () => {
    const newState = toggleAudioMute();
    setAudioMuted(newState);
  };

  // Split View Slider Drag Logic
  const handleSplitMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!splitContainerRef.current) return;
    const rect = splitContainerRef.current.getBoundingClientRect();
    const x = Math.max(0, Math.min(e.clientX - rect.left, rect.width));
    const percent = Math.round((x / rect.width) * 100);
    setSplitSliderPos(percent);
  };

  const handleSimulateRisk = () => {
    playSuccessTone();
    setRiskSimulated(true);
  };

  const handlePlayVoiceAdvisory = () => {
    if (isPlayingAudio) {
      setIsPlayingAudio(false);
      return;
    }
    setIsPlayingAudio(true);
    playSuccessTone();
    setTimeout(() => {
      setIsPlayingAudio(false);
    }, 4500);
  };

  const handleShareWhatsApp = () => {
    setShareSent(true);
    playSuccessTone();
    setTimeout(() => setShareSent(false), 3000);
  };

  return (
    <div
      ref={landingPageRef}
      className="min-h-screen bg-[var(--color-bg-base)] text-[var(--color-on-surface)] transition-colors duration-300 relative selection:bg-emerald-500 selection:text-white font-sans overflow-x-clip snap-scroll-container"
    >
      {/* 21st.dev Mesh Drift WebGL Shader Background (Lowest Background Layer: z-[-20]) */}
      <div className="fixed inset-0 pointer-events-none z-[-20] opacity-45">
        <ShaderBackground className="w-full h-full" />
      </div>

      {/* Chapter Ambient Glow Overlay — morphs colour per active chapter */}
      <div className="chapter-ambient-glow" />

      {/* Master Full-Page Dewdrop SVG Animation Ecosystem (Sticky Track, LERP, Shaders, Waypoints) */}
      <DewdropScrollTracker
        containerRef={landingPageRef}
        activeChapter={activeChapter}
        scrollProgress={scrollProgress}
        onScrollToChapter={scrollToChapter}
        lang={lang}
      />

      {/* Scroll Timeline Scrubber Bar (Top of Viewport) */}
      <div className="fixed top-0 left-0 right-0 h-1 bg-white/5 z-[100] pointer-events-none">
        <div
          className="h-full bg-gradient-to-r from-emerald-500 via-teal-400 to-cyan-400 shadow-[0_0_14px_rgba(16,185,129,0.9)] transition-all duration-100 ease-out"
          style={{ width: `${scrollProgress}%` }}
        />
      </div>

      {/* Main Glassmorphic Navigation Header */}
      <header className="sticky top-0 z-50 h-16 px-4 md:px-10 flex items-center justify-between bg-slate-950/85 backdrop-blur-xl border-b border-white/10 text-white shadow-xl transition-all duration-300">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 via-emerald-500 to-teal-400 text-white flex items-center justify-center shadow-lg shadow-emerald-500/30 border border-emerald-300/40 hologram-float">
            <Sprout size={24} />
          </div>
            <div>
              <span className="text-lg font-black tracking-tight text-white">
                Agri-SAGE
              </span>
              <p className="text-[11px] text-slate-400 hidden sm:block font-medium">
                From a single seed to a smarter tomorrow.
              </p>
            </div>
        </div>

        {/* Header Right Actions */}
        <div className="flex items-center gap-2 sm:gap-3">
          {/* Theme Mode */}
          <button
            type="button"
            onClick={onToggleTheme}
            className="p-2 rounded-xl border border-white/10 hover:border-emerald-400 text-slate-200 bg-white/5 transition-all shadow-xs"
            title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
          >
            {theme === 'dark' ? <Sun size={15} className="text-amber-400" /> : <Moon size={15} className="text-slate-300" />}
          </button>

          {/* Language Switch */}
          <button
            type="button"
            onClick={onToggleLang}
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl border border-white/10 hover:border-emerald-400 text-xs font-bold text-slate-200 bg-white/5 transition-all shadow-xs"
          >
            <Globe size={14} className="text-emerald-400" />
            <span>{lang === 'ml' ? 'മലയാളം' : 'English'}</span>
          </button>

          {/* Launch Auth (Frame 2) */}
          <button
            type="button"
            onClick={onEnterAuth}
            className="btn border border-white/20 hover:border-emerald-400 text-white text-xs h-9 px-3.5 flex items-center gap-1.5 font-bold bg-white/5"
          >
            <Lock size={13} />
            <span>{lang === 'ml' ? 'പ്രവേശിക്കുക' : 'Sign In'}</span>
          </button>

          {/* Launch Full Platform (Frame 3) */}
          <button
            type="button"
            onClick={onDirectPlatformAccess}
            className="btn btn-primary text-xs h-9 px-4 hidden sm:flex items-center gap-1.5 font-bold shadow-lg shadow-emerald-500/25"
          >
            <span>{lang === 'ml' ? 'പ്ലാറ്റ്‌ഫോം തുറക്കുക' : 'Enter Platform'}</span>
            <ArrowRight size={14} />
          </button>
        </div>
      </header>

      {/* FLOATING QUICK CHAPTER DOCK (Fixed Bottom-Left for 1-Click Navigation Across Entire Webpage) */}
      <div className="fixed bottom-6 left-6 z-40 pointer-events-auto">
        <button
          type="button"
          onClick={() => {
            playHoverChime(600);
            setIsChapterDrawerOpen(!isChapterDrawerOpen);
          }}
          className="flex items-center gap-2.5 px-4 py-2.5 rounded-2xl bg-slate-950/90 backdrop-blur-xl border border-emerald-500/40 shadow-2xl text-xs font-mono text-white transition-all hover:scale-105 hover:border-emerald-400"
        >
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
          <span className="font-bold text-emerald-400">CH {String(activeChapter).padStart(2, '0')}</span>
          <span className="text-slate-300 truncate max-w-[130px] sm:max-w-[190px]">
            {CHAPTERS_NAV.find(c => c.id === activeChapter)?.title || 'Hero'}
          </span>
          <ChevronDown size={14} className={`text-slate-400 transition-transform duration-300 ${isChapterDrawerOpen ? 'rotate-180' : ''}`} />
        </button>
      </div>

      {/* INTERACTIVE CHAPTER JUMP DIRECTORY OVERLAY MODAL */}
      {isChapterDrawerOpen && (
        <div className="fixed inset-0 z-[120] flex items-center justify-center p-4 sm:p-6 bg-black/80 backdrop-blur-2xl animate-in fade-in duration-300">
          <div className="bg-slate-950 border border-emerald-500/40 rounded-3xl p-6 max-w-4xl w-full max-h-[85vh] overflow-y-auto shadow-2xl space-y-6">
            <div className="flex items-center justify-between pb-4 border-b border-white/10">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-2xl bg-emerald-500/20 border border-emerald-400/40 text-emerald-400 flex items-center justify-center">
                  <Layers size={22} />
                </div>
                <div>
                  <h3 className="text-lg font-black text-white tracking-tight">12 Chapter Interactive Directory</h3>
                  <p className="text-xs text-slate-400 font-mono">Jump instantly across the scrollytelling timeline with 1 click</p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setIsChapterDrawerOpen(false)}
                className="px-3.5 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-mono font-bold transition-all"
              >
                Close ✕
              </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {CHAPTERS_NAV.map((ch) => {
                const Icon = ch.icon;
                const isActive = activeChapter === ch.id;
                return (
                  <button
                    key={ch.id}
                    type="button"
                    onClick={() => {
                      playSuccessTone();
                      scrollToChapter(ch.id);
                      setIsChapterDrawerOpen(false);
                    }}
                    className={`p-4 rounded-2xl border text-left transition-all group flex flex-col justify-between space-y-3 ${
                      isActive
                        ? 'bg-emerald-950/90 border-emerald-400 shadow-xl shadow-emerald-500/20 ring-1 ring-emerald-400/50'
                        : 'bg-slate-900/60 border-white/10 hover:border-emerald-500/50 hover:bg-slate-900'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-mono font-black px-2.5 py-0.5 rounded-full bg-white/10 text-white group-hover:bg-emerald-500 group-hover:text-black transition-colors">
                        CH {String(ch.id).padStart(2, '0')}
                      </span>
                      <Icon size={18} style={{ color: ch.color }} />
                    </div>

                    <div>
                      <strong className="block text-sm font-bold text-white group-hover:text-emerald-300 transition-colors">
                        {ch.title}
                      </strong>
                      <span className="text-[11px] text-slate-400 font-mono block mt-1 leading-tight">
                        {ch.desc}
                      </span>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* =========================================================================
          CHAPTER 01: HERO SECTION ("Every Field Has a Story")
          Cinematic journey from space -> Earth -> India -> Farmland -> Single Plant
          Interactive 3D Three.js Canvas + Switchable Dual Viewport
          ========================================================================= */}
      <section
        data-chapter="1"
        className="relative min-h-[96vh] flex flex-col justify-center items-center px-4 md:px-10 py-16 overflow-hidden bg-slate-950 snap-scroll-section is-active-snap"
      >
        {/* ====== MULTI-LAYER PARALLAX FLOATING DECORATIONS (Hero) ====== */}
        {/* Layer 1: Deep background orb – slowest (0.3x scroll speed) */}
        <div
          data-parallax-speed="0.3"
          data-parallax-rotate="15"
          data-depth="0.15"
          className="parallax-decoration parallax-orb parallax-orb-emerald parallax-glow-pulse-slow w-[320px] h-[320px] -top-20 -left-40 opacity-60 hidden lg:block"
        />

        {/* Layer 2: Mid-background ring – slightly faster (0.5x) */}
        <div
          data-parallax-speed="0.5"
          data-parallax-rotate="-8"
          data-depth="0.3"
          className="parallax-decoration parallax-ring w-[200px] h-[200px] top-32 right-[10%] opacity-40 hidden lg:block"
        />

        {/* Layer 3: Cyan orb – medium speed (0.7x) */}
        <div
          data-parallax-speed="0.7"
          className="parallax-decoration parallax-orb parallax-orb-cyan parallax-glow-pulse-delayed w-[180px] h-[180px] bottom-[15%] left-[5%] opacity-50 hidden md:block"
        />

        {/* Layer 4: Dashed ring – normal speed (1x, moves with content) */}
        <div
          data-parallax-speed="1.15"
          data-parallax-rotate="12"
          className="parallax-decoration parallax-ring-dashed w-[140px] h-[140px] top-[40%] left-[15%] opacity-30 hidden lg:block"
        />

        {/* Layer 5: Foreground diamond – faster than scroll (1.3x) */}
        <div
          data-parallax-speed="1.3"
          className="parallax-decoration parallax-diamond w-[24px] h-[24px] bottom-[25%] right-[20%] opacity-40 hidden md:block"
        />

        {/* Layer 6: Small emerald orb – fast foreground (1.5x) */}
        <div
          data-parallax-speed="1.5"
          className="parallax-decoration parallax-orb parallax-orb-emerald parallax-glow-pulse w-[60px] h-[60px] top-[20%] right-[25%] opacity-50 hidden md:block"
        />

        {/* Layer 7: Counter-direction element – contra-parallax (-0.2x) */}
        <div
          data-parallax-speed="-0.2"
          data-parallax-rotate="-20"
          className="parallax-decoration parallax-orb parallax-orb-purple parallax-glow-pulse-slow w-[100px] h-[100px] top-[60%] right-[8%] opacity-30 hidden xl:block"
        />

        {/* Hardware-Accelerated Interactive Mouse Light-Beam Aura (Zero-lag RAF Cursor Spotlight) */}
        <div
          className="pointer-events-none absolute inset-0 z-10 opacity-40 transition-opacity duration-500 hidden md:block"
          style={{
            background: 'radial-gradient(650px circle at var(--mouse-x, 50vw) var(--mouse-y, 40vh), rgba(16, 185, 129, 0.16), rgba(6, 182, 212, 0.08), transparent 70%)'
          }}
        />

        {/* 21st.dev Osmo Multi-Layer GSAP Parallax Layer Container */}
        <div data-parallax-layers className="hero-zoom-target absolute inset-0 z-0 pointer-events-none overflow-hidden">
          {/* Layer 1: Deep Sprout Macro Background Image (yPercent: 70) */}
          <div data-parallax-layer="1" className="absolute inset-0 w-full h-full">
            <img
              src={getPublicUrl('/images/hero_sprout_macro.jpg')}
              alt="Close-up bio-luminescent sprout with glowing cellular veins"
              className="w-full h-full object-cover object-center filter brightness-[0.88] contrast-105 transition-all duration-700"
            />
          </div>

          {/* Layer 3: Interactive Constellation & Gradients (yPercent: 40) */}
          <div data-parallax-layer="3" className="absolute inset-0 w-full h-full">
            <div className="absolute inset-0 bg-gradient-to-t from-[var(--color-bg-base)] via-black/40 to-black/75" />
            <div className="absolute inset-0 bg-radial from-transparent via-black/30 to-black/80" />
          </div>

          {/* Layer 4: Foreground Specular Shimmer Fade (yPercent: 10) */}
          <div data-parallax-layer="4" className="absolute inset-0 w-full h-full pointer-events-none bg-gradient-to-t from-slate-950/90 via-transparent to-transparent opacity-80" />
        </div>

        {/* Three.js Interactive Particle Constellation & Planetary Canvas */}
        <ThreeHeroCanvas className="z-10" />

        {/* Hero Narrative Content */}
        <div className="relative z-20 max-w-4xl mx-auto text-center space-y-6 pt-4 pb-6 px-4">

          <h1 className="st-layer-2 velocity-reactive text-4xl sm:text-6xl md:text-7xl font-black tracking-tight text-white drop-shadow-2xl leading-[1.15] flex flex-col items-center">
            <span className="inline-block pb-3 px-1 bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent font-black tracking-tight group cursor-default overflow-visible">
              Agr<span id="agri-i-anchor" className="inline-block relative">ı</span>-SAGE
            </span>
            <span className="block text-2xl sm:text-4xl md:text-5xl font-extrabold text-white/95 mt-1 drop-shadow-lg">
              Intelligence for Every Field.
            </span>
          </h1>

          <p className="st-layer-2 text-base sm:text-lg text-slate-300 max-w-2xl mx-auto font-normal leading-relaxed drop-shadow-md">
            AI-powered precision agriculture spanning planetary satellite observation to single-stomata cellular action. Grounded in biophysical simulation and offline-first edge compute.
          </p>

          {/* Quick AI Field Simulator Interactive Search Bar */}
          <div className="pt-2 max-w-xl mx-auto w-full">
            <div className="p-1.5 rounded-2xl bg-slate-900/90 backdrop-blur-2xl border border-white/20 flex flex-col sm:flex-row items-center gap-2 shadow-2xl transition-all focus-within:border-emerald-400">
              <div className="flex-1 flex items-center gap-2.5 px-3 py-1.5 text-xs text-slate-300 font-mono w-full">
                <Search size={15} className="text-emerald-400 shrink-0" />
                <input
                  type="text"
                  placeholder="Enter farm location or crop (e.g. Palakkad Paddy, Vidarbha Cotton)"
                  value={heroSearchQuery}
                  onChange={(e) => setHeroSearchQuery(e.target.value)}
                  onKeyDown={(e) => { if (e.key === 'Enter') handleHeroSimulate(heroSearchQuery); }}
                  className="bg-transparent border-none outline-none text-white text-xs placeholder:text-slate-500 w-full"
                />
              </div>
              <button
                type="button"
                onClick={() => handleHeroSimulate(heroSearchQuery)}
                disabled={isSimulating}
                className="btn btn-primary text-xs py-2.5 px-5 font-bold flex items-center gap-2 shrink-0 w-full sm:w-auto justify-center shadow-lg shadow-emerald-500/25"
              >
                {isSimulating ? (
                  <>
                    <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    <span>Simulating...</span>
                  </>
                ) : (
                  <>
                    <Sparkles size={14} />
                    <span>Simulate Field</span>
                  </>
                )}
              </button>
            </div>

            {/* Instant AI Simulation Diagnostic Result Card */}
            {simResult && (
              <div className="mt-3 p-3 rounded-2xl bg-emerald-950/90 border border-emerald-500/40 backdrop-blur-xl text-left text-white animate-in fade-in slide-in-from-top-2 duration-300 shadow-2xl flex items-start justify-between gap-3">
                <div className="space-y-1">
                  <strong className="text-xs font-bold text-emerald-300 flex items-center gap-1.5">
                    <CheckCircle2 size={14} className="text-emerald-400" />
                    {simResult.title}
                  </strong>
                  <p className="text-[11px] text-slate-300 font-mono leading-tight">{simResult.subtitle}</p>
                </div>
                <span className="text-[10px] font-mono font-bold uppercase bg-emerald-500/20 text-emerald-300 px-2 py-1 rounded border border-emerald-400/30 shrink-0">
                  {simResult.score}
                </span>
              </div>
            )}
          </div>

          <div className="st-layer-3 flex flex-col sm:flex-row items-center justify-center gap-3.5 pt-2 max-w-md mx-auto">
            <button
              type="button"
              onClick={() => {
                playSuccessTone();
                onEnterAuth();
              }}
              className="btn btn-primary text-sm h-12 px-7 font-bold flex items-center justify-center gap-2 shadow-xl shadow-emerald-500/30 w-full sm:w-auto hover:scale-105 transition-transform"
            >
              <span>Get Started with Agri-SAGE</span>
              <ArrowRight size={16} />
            </button>

            <button
              type="button"
              onClick={() => {
                playHoverChime(600);
                onDirectPlatformAccess();
              }}
              className="btn bg-white/10 hover:bg-white/20 text-white backdrop-blur-xl border border-white/20 text-sm h-12 px-6 font-bold flex items-center justify-center gap-2 w-full sm:w-auto hover:border-emerald-400 transition-all"
            >
              <Zap size={16} className="text-amber-400" />
              <span>Launch Live Workstation</span>
            </button>
          </div>

          {/* Live System Telemetry Trust Badge Strip */}
          <div className="flex flex-wrap items-center justify-center gap-3 text-[11px] font-mono pt-2">
            <span className="flex items-center gap-1.5 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/25 text-emerald-300 backdrop-blur-md">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              1,240+ Active Farm Clusters
            </span>
            <span className="flex items-center gap-1.5 bg-cyan-500/10 px-3 py-1 rounded-full border border-cyan-500/25 text-cyan-300 backdrop-blur-md">
              <ShieldCheck size={13} />
              99.4% Detection Accuracy
            </span>
            <span className="flex items-center gap-1.5 bg-purple-500/10 px-3 py-1 rounded-full border border-purple-500/25 text-purple-300 backdrop-blur-md">
              <Cpu size={13} />
              Offline Edge INT8 Ready
            </span>
          </div>

          {/* Scroll to Explore Mouse Interaction */}
          <div
            onClick={() => scrollToChapter(2)}
            className="pt-4 flex flex-col items-center gap-1.5 cursor-pointer text-white/60 hover:text-white transition-colors group"
          >
            <span className="text-[10px] uppercase font-mono tracking-widest font-semibold group-hover:text-emerald-400 transition-colors">
              Scroll to Explore the 12 Chapters
            </span>
            <div className="w-5 h-8 rounded-full border border-white/30 group-hover:border-emerald-400 flex items-start justify-center p-1 transition-colors">
              <span className="w-1 h-2 rounded-full bg-emerald-400 animate-bounce" />
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          SCROLL-DRIVEN IMAGE SEQUENCE: 441-Frame Apple-Level Scrollytelling
          Full-bleed 400vh sticky canvas scrubbed video sequence
          ========================================================================= */}
      <section className="relative z-10 w-full snap-scroll-section">
        <AppleGrowthScrollytelling
          onEnterPlatform={onDirectPlatformAccess}
          onEnterAuth={onEnterAuth}
        />
      </section>

      {/* =========================================================================
          FRAME 1 INTELLIGENCE CAROUSEL: Squeeze Slat Engine
          Interactive panel carousel showing core agronomic intelligence modules
          ========================================================================= */}
      <section className="relative py-16 px-4 md:px-10 max-w-7xl mx-auto snap-scroll-section z-20">
        <SqueezeCarouselDemo />
      </section>

      {/* =========================================================================
          CHAPTER 02: THE PROBLEM ("A Problem Doesn't Start When You See It.")
          Interactive Split View: What you see vs. What's actually happening
          Draggable Split Slider + 5 Biological Stress Stages
          ========================================================================= */}
      <section
        data-chapter="2"
        className="py-24 px-4 md:px-10 max-w-7xl mx-auto space-y-12 relative z-10 snap-scroll-section"
      >
        <div className="st-layer-1 text-center space-y-3 max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/20 text-xs font-mono font-bold tracking-widest uppercase">
            <AlertTriangle size={13} />
            <span>02 · The Invisible Pathogen Genesis</span>
          </div>
          <h2
            ref={problemTitleRef}
            className="velocity-reactive text-3xl md:text-5xl font-black tracking-tight text-[var(--color-on-surface)]"
          >
            A Problem Doesn't Start When You See It.
          </h2>
          <p className="text-sm md:text-base text-[var(--color-on-surface-secondary)] leading-relaxed">
            By the time you notice yellowing leaves or wilting tillers, the fungal mycelium has already colonized vascular bundles. Agri-SAGE detects subterranean plant stress 96 hours before visual manifestation.
          </p>
        </div>

        {/* Interactive Split View Container with Draggable Slider */}
        <div
          ref={splitContainerRef}
          onMouseMove={handleSplitMouseMove}
          className="relative z-10 rounded-3xl overflow-hidden border border-[var(--color-outline-variant)] shadow-2xl bg-black select-none cursor-ew-resize group"
          style={{ height: '560px' }}
        >
          {/* Laser Scanner Sweep Line */}
          <div className="laser-scanner-line" />

          {/* Underneath Layer: What's Actually Happening (Thermal / Spore Stress clipped by slider line) */}
          <div
            className="absolute inset-y-0 right-0 overflow-hidden"
            style={{ left: `${splitSliderPos}%` }}
          >
            <div
              className="relative h-full"
              style={{
                width: splitContainerRef.current ? `${splitContainerRef.current.clientWidth}px` : '100vw',
                marginLeft: `calc(-1 * (${splitContainerRef.current ? splitContainerRef.current.clientWidth : 1000}px * ${splitSliderPos / 100}))`
              }}
            >
              <img
                src={getPublicUrl('/images/crop_split.jpg')}
                alt="Thermal Spore Stress Detection"
                className="w-full h-full object-cover filter saturate-150 contrast-125"
              />

              {/* Top Right Header Banner */}
              <div className="absolute top-3 right-6 text-xs font-mono font-bold tracking-widest text-amber-400 uppercase z-10 bg-black/75 px-3 py-1 rounded-full border border-amber-500/40 backdrop-blur-md shadow-xl">
                SUBTERRANEAN INFRARED & PATHOGEN SPORE HEAT SIGNATURES
              </div>

              <div className="absolute top-14 right-6 glass-panel p-4 backdrop-blur-xl border border-red-500/40 text-xs text-white max-w-sm space-y-1.5 shadow-2xl bg-slate-950/80 z-10">
                <div className="flex items-center gap-2 font-bold text-red-400 uppercase tracking-wider text-[11px] font-mono">
                  <span className="w-2 h-2 rounded-full bg-red-500 animate-ping" />
                  Agri-SAGE Thermal Bio-Spectra (What's Happening)
                </div>
                <p className="text-white/90 text-xs leading-relaxed">
                  Localized leaf temperature anomaly (+2.8°C) reveals active mycelial respiration & cellular water tension breakdown 96 hours before chlorosis.
                </p>
                <div className="pt-2 border-t border-white/10 flex items-center justify-between font-mono text-[10px] text-red-300">
                  <span>Spore Index: <strong>0.78 HIGH</strong></span>
                  <span>Intervention: <strong>Window 24h</strong></span>
                </div>
              </div>

              {/* Thermal Annotations Overlay (Spore Clusters, Hotspots, Infection Zones, Temp) */}
              <div className="absolute inset-0 pointer-events-none z-10">
                {/* Fungal Spore Clusters Pointer */}
                <div className="absolute top-[28%] right-[16%] flex items-center gap-2 text-right">
                  <div className="text-[11px] font-mono font-bold text-amber-400 bg-black/80 px-2.5 py-1 rounded-lg border border-amber-500/40 shadow-xl backdrop-blur-md">
                    FUNGAL SPORE CLUSTERS <span className="text-[9px] text-amber-300 block font-normal">(NEON AMBER)</span>
                  </div>
                  <div className="w-6 h-[2px] bg-amber-400/80" />
                  <div className="w-2.5 h-2.5 rounded-full bg-amber-400 shadow-[0_0_12px_#f59e0b] animate-ping" />
                </div>

                {/* Cellular Stress Hotspots Pointer */}
                <div className="absolute top-[52%] right-[10%] flex items-center gap-2 text-right">
                  <div className="text-[11px] font-mono font-bold text-orange-400 bg-black/80 px-2.5 py-1 rounded-lg border border-orange-500/40 shadow-xl backdrop-blur-md">
                    CELLULAR STRESS HOTSPOTS <span className="text-[9px] text-orange-300 block font-normal">(NEON ORANGE)</span>
                  </div>
                  <div className="w-6 h-[2px] bg-orange-400/80" />
                  <div className="w-2.5 h-2.5 rounded-full bg-orange-400 shadow-[0_0_12px_#fb923c] animate-pulse" />
                </div>

                {/* Infection Zones Annotation Line */}
                <div className="absolute bottom-20 right-[18%] flex items-center gap-3">
                  <div className="h-[1px] w-28 bg-red-400/60" />
                  <span className="text-[10px] font-mono font-bold tracking-widest text-red-400 uppercase bg-black/80 px-2.5 py-0.5 rounded border border-red-500/40 shadow-md">
                    INFECTION ZONES
                  </span>
                </div>

                {/* Bottom Right Temperature Readout */}
                <div className="absolute bottom-16 right-6 text-xl font-mono font-black text-amber-300 tracking-wider bg-black/85 px-3.5 py-1.5 rounded-xl border border-amber-500/40 shadow-2xl backdrop-blur-md">
                  31.4°C
                </div>
              </div>
            </div>
          </div>

          {/* Top Layer: What You See (Daylight Natural View clipped by slider) */}
          <div
            className="absolute inset-y-0 left-0 overflow-hidden"
            style={{ width: `${splitSliderPos}%` }}
          >
            <div style={{ width: splitContainerRef.current ? `${splitContainerRef.current.clientWidth}px` : '100vw', height: '100%' }}>
              <img
                src={getPublicUrl('/images/crop_split.jpg')}
                alt="Daylight Natural Foliage"
                className="w-full h-full object-cover filter brightness-105 contrast-95"
              />

              {/* Top Left Header Banner */}
              <div className="absolute top-3 left-6 text-xs font-mono font-bold tracking-widest text-emerald-400 uppercase z-10 bg-black/75 px-3 py-1 rounded-full border border-emerald-500/40 backdrop-blur-md shadow-xl">
                DAYLIGHT HEALTHY LEAF
              </div>
            </div>
            <div className="absolute top-14 left-6 glass-panel p-4 backdrop-blur-xl border border-emerald-400/40 text-xs text-white max-w-sm space-y-1.5 shadow-2xl bg-slate-950/80">
              <div className="flex items-center gap-2 font-bold text-emerald-400 uppercase tracking-wider text-[11px] font-mono">
                <Eye size={14} />
                Daylight Human Vision (What You See)
              </div>
              <p className="text-white/90 text-xs leading-relaxed">
                Leaf surface appears completely emerald and healthy to naked eyes. Farmer delays action, unaware that spore colony is already dividing inside plant xylem.
              </p>
              <div className="pt-2 border-t border-white/10 flex items-center justify-between font-mono text-[10px] text-emerald-300">
                <span>Visual Symptoms: <strong>0%</strong></span>
                <span>Hidden Damage: <strong>Active</strong></span>
              </div>
            </div>
          </div>

          {/* Draggable Divider Handle Line */}
          <div
            className="absolute inset-y-0 w-1 bg-white cursor-ew-resize z-30 shadow-[0_0_15px_rgba(255,255,255,0.8)]"
            style={{ left: `${splitSliderPos}%` }}
          >
            {/* Vertical divider label text */}
            <div className="absolute top-1/4 -translate-x-1/2 -rotate-90 whitespace-nowrap text-[10px] font-mono font-bold tracking-widest text-white/90 bg-black/80 px-2.5 py-1 rounded border border-white/30 uppercase shadow-lg backdrop-blur-md">
              INFRARED & PATHOGEN STRESS
            </div>

            <div className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-9 h-9 rounded-full bg-white text-slate-900 flex items-center justify-center shadow-xl border-2 border-emerald-500 font-bold text-xs">
              <Sliders size={16} />
            </div>
          </div>

          {/* Slider Instruction Bar */}
          <div className="absolute bottom-4 inset-x-4 p-3 rounded-2xl bg-black/75 backdrop-blur-xl border border-white/15 flex flex-wrap items-center justify-between gap-4 text-xs text-white z-20">
            <span className="font-mono text-emerald-400 flex items-center gap-2 font-semibold">
              <Sliders size={14} /> Drag horizontally to contrast visible canopy vs. subterranean fungal heat
            </span>
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setSplitSliderPos(20)}
                className="px-2.5 py-1 rounded bg-white/10 hover:bg-white/20 text-[11px] font-mono"
              >
                Inspect Stress (20%)
              </button>
              <button
                type="button"
                onClick={() => setSplitSliderPos(50)}
                className="px-2.5 py-1 rounded bg-white/10 hover:bg-white/20 text-[11px] font-mono"
              >
                Split (50%)
              </button>
              <button
                type="button"
                onClick={() => setSplitSliderPos(80)}
                className="px-2.5 py-1 rounded bg-white/10 hover:bg-white/20 text-[11px] font-mono"
              >
                Inspect Visible (80%)
              </button>
            </div>
          </div>
        </div>

        {/* 5 Biological Warning Stages (Blueprint Reference List) */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3.5 pt-4">
          {[
            { id: 1, title: 'Soil Dryness', metric: 'VWC 18%', desc: 'Capacitive sensors flag sub-wilting threshold', color: 'border-amber-500/40 text-amber-500', speed: '1.1', z: '20', rotY: '-12', tz: 15 },
            { id: 2, title: 'Temperature Rise', metric: '+2.8°C', desc: 'Canopy transpiration shutdown causes heat bloom', color: 'border-orange-500/40 text-orange-500', speed: '1.25', z: '45', rotY: '-6', tz: 30 },
            { id: 3, title: 'Humidity Trapping', metric: 'RH 88%', desc: 'Microclimate dew creates ideal spore chamber', color: 'border-blue-500/40 text-blue-500', speed: '1.35', z: '70', rotY: '0', tz: 45 },
            { id: 4, title: 'Leaf Stress', metric: 'Fv/Fm 0.69', desc: 'Photosynthetic quantum efficiency plummets', color: 'border-purple-500/40 text-purple-500', speed: '1.25', z: '45', rotY: '6', tz: 30 },
            { id: 5, title: 'Disease Begins', metric: 'Sporulation', desc: 'Sub-epidermal mycelium begins colonial eruption', color: 'border-red-500/40 text-red-500', speed: '1.1', z: '20', rotY: '12', tz: 15 }
          ].map((stage) => (
            <div
              key={stage.id}
              data-parallax-speed={stage.speed}
              data-parallax-z={stage.z}
              data-parallax-rotate-y={stage.rotY}
            >
              <GlassTiltCard
                translateZ={stage.tz}
                onClick={() => {
                  playHoverChime(420 + stage.id * 50);
                  setActiveStressStage(stage.id);
                }}
                className={`p-4 transition-all ${
                  activeStressStage === stage.id
                    ? 'bg-slate-900/90 border-emerald-400 ring-2 ring-emerald-500/30'
                    : 'bg-[var(--color-surface)] hover:border-white/30'
                }`}
              >
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-[10px] font-mono uppercase font-bold text-[var(--color-on-surface-tertiary)]">
                    Stage 0{stage.id}
                  </span>
                  <span className={`text-[11px] font-mono font-bold ${stage.color}`}>
                    {stage.metric}
                  </span>
                </div>
                <strong className="text-sm font-bold text-[var(--color-on-surface)] block mb-1">
                  {stage.title}
                </strong>
                <p className="text-[11px] text-[var(--color-on-surface-secondary)] leading-relaxed">
                  {stage.desc}
                </p>
              </GlassTiltCard>
            </div>
          ))}
        </div>
      </section>

      {/* =========================================================================
          CHAPTER 03: THE FARM ("A Farm Is More Than A Field.")
          360° Layered 3D Farm Visualizer with Interactive Sensor Nodes
          ========================================================================= */}
      <section
        data-chapter="3"
        className="relative z-10 py-24 px-4 md:px-10 max-w-7xl mx-auto space-y-10 snap-scroll-section"
      >
        {/* Parallax Decorations – Chapter 03 */}
        <div data-parallax-speed="0.4" data-parallax-rotate="10" data-depth="0.2" className="parallax-decoration parallax-orb parallax-orb-cyan parallax-glow-pulse w-[200px] h-[200px] -top-16 -right-20 opacity-30 hidden lg:block" />
        <div data-parallax-speed="1.3" data-depth="0.7" className="parallax-decoration parallax-ring w-[120px] h-[120px] top-[50%] -left-10 opacity-25 hidden lg:block" />
        <div data-parallax-speed="0.7" data-depth="0.45" className="parallax-decoration parallax-diamond w-[20px] h-[20px] bottom-[20%] right-[12%] opacity-35 hidden md:block" />

        <div className="st-layer-1 flex flex-col md:flex-row md:items-end justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 text-xs font-mono font-bold tracking-widest uppercase">
              <Layers size={13} />
              <span>03 · The Connected Ecosystem</span>
            </div>
            <h2
              ref={farmTitleRef}
              className="velocity-reactive text-3xl md:text-5xl font-black tracking-tight text-[var(--color-on-surface)]"
            >
              A Farm Is More Than A Field.
            </h2>
            <p className="text-sm md:text-base text-[var(--color-on-surface-secondary)] leading-relaxed">
              Soil. Weather. Water. Crops. People. All connected. All vital. Agri-SAGE constructs a unified digital twin combining microclimate edge probes with Sentinel-2 multi-spectral orbital passes.
            </p>
          </div>

          {/* Layer Selector Chips */}
          <div className="flex flex-wrap gap-2 text-xs font-semibold">
            {[
              { id: 'all', label: 'All Layers' },
              { id: 'satellite', label: 'Satellite' },
              { id: 'weather', label: 'Weather' },
              { id: 'soil', label: 'Soil' },
              { id: 'irrigation', label: 'Irrigation' },
              { id: 'sensors', label: 'Sensors' },
              { id: 'farmer', label: 'Farmer' }
            ].map((layer) => (
              <button
                key={layer.id}
                type="button"
                onClick={() => {
                  playHoverChime(480);
                  setSelectedFarmLayer(layer.id as typeof selectedFarmLayer);
                }}
                className={`px-3.5 py-2 rounded-xl border transition-all uppercase tracking-wider text-[11px] font-mono font-bold ${
                  selectedFarmLayer === layer.id
                    ? 'bg-emerald-500 text-white border-emerald-500 shadow-lg shadow-emerald-500/30'
                    : 'bg-[var(--color-surface)] text-[var(--color-on-surface-secondary)] border-[var(--color-outline-variant)] hover:border-emerald-500'
                }`}
              >
                {layer.label}
              </button>
            ))}
          </div>
        </div>

        {/* 3D Isometric Connected Smart Farm Render */}
        <div className="relative z-10 rounded-3xl overflow-hidden border border-[var(--color-outline-variant)] shadow-2xl bg-black">
          <img
            src={getPublicUrl('/images/farm_isometric.jpg')}
            alt="3D Isometric Connected Smart Farm with Floating Glass HUDs"
            className="w-full h-[480px] md:h-[640px] object-cover"
          />

          {/* Interactive Floating 3D Pins on the Farm Canvas */}
          {(selectedFarmLayer === 'all' || selectedFarmLayer === 'satellite') && (
            <div className="absolute top-16 left-1/4 z-20 animate-bounce">
              <div className="glass-panel p-2.5 bg-slate-950/85 border-cyan-400/40 text-white text-[11px] font-mono flex items-center gap-2 shadow-xl">
                <Compass size={14} className="text-cyan-400" />
                <span>Sentinel-2 L2A · 10m NDVI: <strong>0.78</strong></span>
              </div>
            </div>
          )}

          {(selectedFarmLayer === 'all' || selectedFarmLayer === 'weather') && (
            <div className="absolute top-24 right-1/4 z-20 hologram-float">
              <div className="glass-panel p-2.5 bg-slate-950/85 border-blue-400/40 text-white text-[11px] font-mono flex items-center gap-2 shadow-xl">
                <CloudRain size={14} className="text-blue-400" />
                <span>Microclimate: <strong>28°C · Rain 12%</strong></span>
              </div>
            </div>
          )}

          {(selectedFarmLayer === 'all' || selectedFarmLayer === 'soil') && (
            <div className="absolute bottom-36 left-1/3 z-20">
              <div className="glass-panel p-2.5 bg-slate-950/85 border-amber-400/40 text-white text-[11px] font-mono flex items-center gap-2 shadow-xl">
                <Activity size={14} className="text-amber-400" />
                <span>Soil Probe #03: <strong>pH 6.4 · VWC 64%</strong></span>
              </div>
            </div>
          )}

          {(selectedFarmLayer === 'all' || selectedFarmLayer === 'irrigation') && (
            <div className="absolute bottom-28 right-1/3 z-20">
              <div className="glass-panel p-2.5 bg-slate-950/85 border-emerald-400/40 text-white text-[11px] font-mono flex items-center gap-2 shadow-xl">
                <Droplets size={14} className="text-emerald-400" />
                <span>Drip Valve Cluster: <strong>Standby 06:00 AM</strong></span>
              </div>
            </div>
          )}

          {/* Bottom Telemetry Strip */}
          <div className="absolute bottom-6 left-6 right-6 flex flex-wrap items-center justify-between gap-4 p-4 rounded-2xl bg-black/75 backdrop-blur-xl border border-white/20 text-white text-xs">
            <div className="flex items-center gap-4 flex-wrap font-mono">
              <span className="flex items-center gap-2 text-emerald-400 font-bold">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                DIGITAL TWIN ONLINE
              </span>
              <span>·</span>
              <span>16 LoRaWAN Edge Nodes</span>
              <span>·</span>
              <span>Solar Irradiance: <strong>680 W/m²</strong></span>
              <span>·</span>
              <span>Active Layer: <strong className="uppercase text-emerald-300">{selectedFarmLayer}</strong></span>
            </div>
            <div className="text-[11px] text-white/70 font-mono">
              DSSAT Field Mesh Latency: 42ms
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          CHAPTER 04: SEE THE INVISIBLE ("What If You Could See What Your Crops Can't Tell You?")
          Cellular Microscope HUD with Spectral Wavelength Switcher
          ========================================================================= */}
      <section
        data-chapter="4"
        className="py-24 px-4 md:px-10 max-w-7xl mx-auto space-y-12 relative z-10 snap-scroll-section"
      >
        <div className="st-layer-1 text-center space-y-3 max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 text-xs font-mono font-bold tracking-widest uppercase">
            <Microscope size={13} />
            <span>04 · Sub-Cellular Optics</span>
          </div>
          <h2 className="text-3xl md:text-5xl font-black tracking-tight text-[var(--color-on-surface)] leading-tight">
            What If You Could See What Your Crops Can't Tell You?
          </h2>
          <p className="text-sm md:text-base text-[var(--color-on-surface-secondary)] leading-relaxed">
            From individual stomatal conductance to quantum chloroplast energy absorption. Agri-SAGE turns low-cost smartphone cameras into multi-spectral instruments with on-device INT8 computer vision.
          </p>
        </div>

        {/* Microscope Cellular Inspection Display */}
        <div className="relative z-10 rounded-3xl overflow-hidden border border-cyan-500/30 shadow-2xl bg-black">
          <img
            src={getPublicUrl('/images/cellular_macro.jpg')}
            alt="Microscopic Cellular Chloroplast and Stomata Structure"
            className="w-full h-[500px] md:h-[620px] object-cover filter contrast-110"
          />

          {/* Microscopic Laser Scanner Line */}
          <div className="laser-scanner-line" />

          {/* Microscope Crosshair HUD Overlay */}
          <div className="absolute inset-0 pointer-events-none flex items-center justify-center">
            <div className="w-56 h-56 rounded-full border border-cyan-400/30 flex items-center justify-center animate-spin" style={{ animationDuration: '40s' }}>
              <div className="w-40 h-40 rounded-full border border-dashed border-emerald-400/40" />
            </div>
            <div className="absolute w-2 h-2 rounded-full bg-cyan-400 shadow-lg shadow-cyan-400/80" />
          </div>

          {/* Top-Right: Microscope Spectral Band Selector */}
          <div className="absolute top-6 right-6 z-20 flex flex-col gap-2 p-2 rounded-2xl bg-slate-950/85 backdrop-blur-xl border border-white/20 text-xs font-mono">
            <span className="text-[10px] text-white/60 font-bold px-2 uppercase">Spectral Band</span>
            {(['rgb', 'rededge', 'nir', 'thermal'] as const).map((band) => (
              <button
                key={band}
                type="button"
                onClick={() => {
                  playHoverChime(550);
                  setSpectralBand(band);
                }}
                className={`px-3 py-1.5 rounded-xl transition-all text-left uppercase text-[11px] font-bold ${
                  spectralBand === band
                    ? 'bg-cyan-500 text-white shadow-md shadow-cyan-500/30'
                    : 'text-white/70 hover:text-white hover:bg-white/10'
                }`}
              >
                {band === 'rgb' && 'Visible RGB (400-700nm)'}
                {band === 'rededge' && 'RedEdge (705nm)'}
                {band === 'nir' && 'Near-Infrared NIR (842nm)'}
                {band === 'thermal' && 'Thermal IR (10.5µm)'}
              </button>
            ))}
          </div>

          {/* Floating Cellular Diagnostics HUD Badges */}
          <div className="absolute bottom-6 left-6 right-6 grid grid-cols-2 md:grid-cols-4 gap-3 z-20">
            <div className="p-3.5 rounded-2xl bg-slate-950/85 backdrop-blur-xl border border-emerald-400/30 text-white">
              <span className="text-[10px] text-emerald-300 font-mono uppercase block">Chloroplast Yield</span>
              <strong className="text-base font-black font-mono">Fv/Fm = 0.81</strong>
              <span className="text-[10px] text-white/60 block mt-0.5">Optimal Quantum Capture</span>
            </div>

            <div className="p-3.5 rounded-2xl bg-slate-950/85 backdrop-blur-xl border border-blue-400/30 text-white">
              <span className="text-[10px] text-blue-300 font-mono uppercase block">Stomata Aperture</span>
              <strong className="text-base font-black font-mono">12.4 µm</strong>
              <span className="text-[10px] text-white/60 block mt-0.5">gs = 280 mmol/m²s</span>
            </div>

            <div className="p-3.5 rounded-2xl bg-slate-950/85 backdrop-blur-xl border border-amber-400/30 text-white">
              <span className="text-[10px] text-amber-300 font-mono uppercase block">Water Potential</span>
              <strong className="text-base font-black font-mono">Ψ = -0.42 MPa</strong>
              <span className="text-[10px] text-white/60 block mt-0.5">Turgor Pressure Intact</span>
            </div>

            <div className="p-3.5 rounded-2xl bg-slate-950/85 backdrop-blur-xl border border-purple-400/30 text-white">
              <span className="text-[10px] text-purple-300 font-mono uppercase block">Pathogen DNA Probe</span>
              <strong className="text-base font-black font-mono text-emerald-400">NEGATIVE</strong>
              <span className="text-[10px] text-white/60 block mt-0.5">Zero Xanthomonas</span>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          HORIZONTAL SCROLL SHOWCASE: Intelligence Pipeline
          Pinned section with 5 full-viewport panels that translate horizontally
          as the user scrolls vertically. GSAP containerAnimation per-panel reveals.
          ========================================================================= */}
      <div className="w-full relative z-10 block">
        <HorizontalScrollShowcase />
      </div>

      {/* =========================================================================
          CHAPTER 05: AGRI-SAGE INTELLIGENCE ("Meet the Intelligence Behind the Field.")
          4-Stage Interactive Pipeline: Raw Data -> AI Core -> Simulation -> Action
          ========================================================================= */}
      <section
        data-chapter="5"
        className="relative z-10 py-24 px-4 md:px-10 max-w-7xl mx-auto space-y-12 snap-scroll-section"
      >
        {/* Parallax Decorations – Chapter 05 */}
        <div data-parallax-speed="0.35" data-parallax-rotate="-12" data-depth="0.2" className="parallax-decoration parallax-orb parallax-orb-emerald parallax-glow-pulse-slow w-[280px] h-[280px] -top-24 -left-32 opacity-25 hidden lg:block" />
        <div data-parallax-speed="1.4" data-depth="0.75" className="parallax-decoration parallax-orb parallax-orb-purple parallax-glow-pulse-delayed w-[90px] h-[90px] top-[30%] right-[5%] opacity-35 hidden md:block" />
        <div data-parallax-speed="0.8" data-parallax-rotate="18" data-depth="0.4" className="parallax-decoration parallax-ring-dashed w-[160px] h-[160px] bottom-[10%] left-[8%] opacity-20 hidden lg:block" />
        <div data-parallax-speed="-0.15" data-depth="0.9" className="parallax-decoration parallax-diamond w-[16px] h-[16px] top-[60%] left-[45%] opacity-30 hidden xl:block" />

        <div className="st-layer-1 text-center space-y-3 max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 text-xs font-mono font-bold tracking-widest uppercase">
            <Cpu size={13} />
            <span>05 · Neural Architecture</span>
          </div>
          <h2
            ref={neuralTitleRef}
            className="text-3xl md:text-5xl font-black tracking-tight text-[var(--color-on-surface)]"
          >
            Meet the Intelligence Behind the Field.
          </h2>
          <p className="text-sm md:text-base text-[var(--color-on-surface-secondary)]">
            How raw heterogeneous data from orbit, canopy, and soil transforms into life-saving agronomic decisions.
          </p>
        </div>

        {/* 4 Interactive Pipeline Stages */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[
            {
              step: 1,
              title: 'Raw Multi-Source Data',
              badge: 'Ingestion',
              desc: 'High-resolution smartphone foliage photos, weather station DFI, soil texture, planting GDD.',
              specs: 'CameraX 5 FPS · IMD API · LoRaWAN',
              color: 'border-blue-500/40 text-blue-500'
            },
            {
              step: 2,
              title: 'Agri-SAGE AI Core',
              badge: 'Multi-Agent',
              desc: '14 specialized LangGraph agents evaluate symptom patterns, disease classification, and nutrient deficiencies.',
              specs: 'INT8 ONNX · Sub-4s Edge Inference',
              color: 'border-emerald-500/40 text-emerald-500'
            },
            {
              step: 3,
              title: 'DSSAT Simulation',
              badge: 'Physics Engine',
              desc: 'Physics-based mathematical crop growth models project daily yield loss curves under multiple treatment scenarios.',
              specs: 'DSSAT v4.8 · APSIM Causal Logic',
              color: 'border-purple-500/40 text-purple-500'
            },
            {
              step: 4,
              title: 'Validated Action',
              badge: 'Empowerment',
              desc: 'Every fungicide, dosage, and spray timing verified against CIB&RC registry in native mother-tongue audio.',
              specs: 'Zero Hallucination Filter · Malayalam Voice',
              color: 'border-teal-500/40 text-teal-500'
            }
          ].map((item) => (
            <GlassTiltCard
              key={item.step}
              onClick={() => {
                playHoverChime(450 + item.step * 40);
                setActivePipelineStep(item.step);
              }}
              className={`p-6 transition-all cursor-pointer ${
                activePipelineStep === item.step
                  ? 'bg-slate-900/90 border-emerald-400 ring-2 ring-emerald-500/30'
                  : 'bg-[var(--color-surface)] hover:border-white/30'
              }`}
            >
              <div className="flex items-center justify-between mb-3">
                <span className="w-8 h-8 rounded-xl bg-emerald-500/10 text-emerald-500 font-mono font-bold text-sm flex items-center justify-center">
                  0{item.step}
                </span>
                <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-black/10 dark:bg-white/5 uppercase ${item.color}`}>
                  {item.badge}
                </span>
              </div>
              <strong className="text-base font-bold text-[var(--color-on-surface)] block mb-1.5">
                {item.title}
              </strong>
              <p className="text-xs text-[var(--color-on-surface-secondary)] leading-relaxed mb-4">
                {item.desc}
              </p>
              <div className="pt-3 border-t border-[var(--color-outline-variant)] text-[10px] font-mono text-emerald-600 dark:text-emerald-400 font-semibold">
                {item.specs}
              </div>
            </GlassTiltCard>
          ))}
        </div>
      </section>

      {/* =========================================================================
          CHAPTER 06: MULTI-AGENT AI ("One Intelligence Isn't Enough.")
          Interactive Star-Topology Constellation Network
          ========================================================================= */}
      <section
        data-chapter="6"
        className="relative z-10 py-24 px-4 md:px-10 max-w-7xl mx-auto space-y-12 snap-scroll-section"
      >
        <div className="st-layer-1 text-center space-y-3 max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 text-xs font-mono font-bold tracking-widest uppercase">
            <Radio size={13} />
            <span>06 · Multi-Agent Star Topology</span>
          </div>
          <h2 className="velocity-reactive text-3xl md:text-5xl font-black tracking-tight text-[var(--color-on-surface)]">
            One Intelligence Isn't Enough.
          </h2>
          <p className="text-sm md:text-base text-[var(--color-on-surface-secondary)] leading-relaxed">
            Generic LLMs give dangerous, ungrounded advice. Agri-SAGE deploys 6 specialized autonomous agents coordinated by a central orchestrator that debate, cross-verify, and stress-test every decision.
          </p>
        </div>

        {/* 6 Specialized Agents Interactive Hub */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            {
              id: 'vision',
              name: 'Vision Diagnosis Agent',
              badge: 'ONNX INT8',
              latency: '84ms',
              confidence: '98.4%',
              desc: 'Identifies 21 regional crop diseases and nutritional deficiencies with attention saliency maps.',
              model: 'MobileNetV4 + YOLOv11 Edge',
              speed: '1.15', z: '30', rotY: '-10', tz: 20
            },
            {
              id: 'weather',
              name: 'Microclimate Weather Agent',
              badge: 'Open-Meteo & IMD',
              latency: '110ms',
              confidence: '94.2%',
              desc: 'Calculates Disease Favorability Index (DFI) and computes 48-hour wind & precipitation spray windows.',
              model: 'HRRR Numerical + Local Sensors',
              speed: '1.25', z: '60', rotY: '10', tz: 40
            },
            {
              id: 'crop',
              name: 'Phenology & GDD Agent',
              badge: 'Thermal Time',
              latency: '42ms',
              confidence: '99.1%',
              desc: 'Tracks Growing Degree Day accumulation from sowing to flag leaf emergence and grain filling.',
              model: 'FAO-56 Dual Crop Coefficient',
              speed: '1.1', z: '20', rotY: '-6', tz: 15
            },
            {
              id: 'sim',
              name: 'Biophysical Simulation Agent',
              badge: 'DSSAT v4.8',
              latency: '140ms',
              confidence: '96.8%',
              desc: 'Solves coupled differential equations for soil water, root nitrogen uptake, and biomass accumulation.',
              model: 'CERES-Rice & CROPGRO Dynamic',
              speed: '1.3', z: '70', rotY: '12', tz: 50
            },
            {
              id: 'critic',
              name: 'CIB&RC Critic Safety Agent',
              badge: 'Zero Hallucination',
              latency: '62ms',
              confidence: '100%',
              desc: 'Strict statutory gatekeeper. Rejects unauthorized agrochemicals and validates statutory wait periods.',
              model: 'Govt. Registry Rule Engine',
              speed: '1.15', z: '35', rotY: '-8', tz: 25
            },
            {
              id: 'voice',
              name: 'Regional Vernacular Agent',
              badge: 'Bhashini Voice',
              latency: '95ms',
              confidence: '97.5%',
              desc: 'Translates high-dimensional biophysical findings into simple Malayalam and Tamil voice alerts.',
              model: 'AI4Bharat IndicTTS Pipeline',
              speed: '1.2', z: '45', rotY: '8', tz: 30
            }
          ].map((agent) => (
            <div
              key={agent.id}
              data-parallax-speed={agent.speed}
              data-parallax-z={agent.z}
              data-parallax-rotate-y={agent.rotY}
            >
              <GlassTiltCard
                translateZ={agent.tz}
                onClick={() => {
                  playHoverChime(500);
                  setSelectedAgentId(agent.id as typeof selectedAgentId);
                }}
                className={`p-5 transition-all ${
                  selectedAgentId === agent.id
                    ? 'bg-slate-900/90 border-emerald-400 ring-2 ring-emerald-500/30'
                    : 'bg-[var(--color-surface)] hover:border-white/30'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <strong className="text-base font-bold text-[var(--color-on-surface)]">
                    {agent.name}
                  </strong>
                  <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-500 border border-emerald-500/20">
                    {agent.badge}
                  </span>
                </div>
                <p className="text-xs text-[var(--color-on-surface-secondary)] leading-relaxed mb-3">
                  {agent.desc}
                </p>
                <div className="pt-2.5 border-t border-[var(--color-outline-variant)] flex items-center justify-between text-[10px] font-mono text-[var(--color-on-surface-tertiary)]">
                  <span>Model: <strong className="text-[var(--color-on-surface)]">{agent.model}</strong></span>
                  <span>Latency: <strong className="text-emerald-500">{agent.latency}</strong></span>
                </div>
              </GlassTiltCard>
            </div>
          ))}
        </div>
      </section>

      {/* =========================================================================
          CHAPTER 07: CROP SIMULATION ("Don't Just Predict Tomorrow. Simulate It.")
          Interactive Time Slider (1d, 3d, 7d, 14d) & Comparative Future Scenarios
          ========================================================================= */}
      <section
        data-chapter="7"
        className="relative z-10 py-24 px-4 md:px-10 max-w-7xl mx-auto space-y-12 snap-scroll-section"
      >
        {/* Parallax Decorations – Chapter 07 */}
        <div data-parallax-speed="0.5" className="parallax-decoration parallax-orb parallax-orb-purple parallax-glow-pulse w-[220px] h-[220px] -top-12 right-[8%] opacity-25 hidden lg:block" />
        <div data-parallax-speed="1.35" data-parallax-rotate="-15" className="parallax-decoration parallax-ring w-[100px] h-[100px] bottom-[25%] -left-8 opacity-20 hidden lg:block" />
        <div data-parallax-speed="0.65" className="parallax-decoration parallax-orb parallax-orb-amber parallax-glow-pulse-delayed w-[70px] h-[70px] top-[45%] right-[3%] opacity-30 hidden md:block" />

        <div className="st-layer-1 text-center space-y-3 max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 text-purple-400 border border-purple-500/20 text-xs font-mono font-bold tracking-widest uppercase">
            <BarChart3 size={13} />
            <span>07 · Biophysical Digital Twin</span>
          </div>
          <h2 className="text-3xl md:text-5xl font-black tracking-tight text-[var(--color-on-surface)]">
            Don't Just Predict Tomorrow. Simulate It.
          </h2>
          <p className="text-sm md:text-base text-[var(--color-on-surface-secondary)] leading-relaxed">
            Agri-SAGE doesn't make guesses. Powered by the globally validated DSSAT engine, we simulate multiple futures across 1 to 14 days before the farmer spends a single rupee on intervention.
          </p>
        </div>

        {/* Interactive Scenario Studio */}
        <div className="glass-panel p-6 sm:p-10 space-y-8 border-purple-500/30">
          {/* Day Horizon Time Slider */}
          <div className="flex items-center justify-between flex-wrap gap-4 pb-6 border-b border-[var(--color-outline-variant)]">
            <div>
              <h4 className="text-base font-bold text-[var(--color-on-surface)]">
                DSSAT Simulation Projection Horizon
              </h4>
              <span className="text-xs text-[var(--color-on-surface-secondary)]">
                Run daily time-step biomass, moisture, and spore multiplication equations
              </span>
            </div>

            <div className="flex p-1.5 rounded-2xl bg-[var(--color-surface-variant)] border border-[var(--color-outline-variant)] text-xs font-mono font-bold">
              {(['1', '3', '7', '14'] as const).map((d) => (
                <button
                  key={d}
                  type="button"
                  onClick={() => {
                    playHoverChime(460 + Number(d) * 15);
                    setSimDays(d);
                  }}
                  className={`px-4 py-2 rounded-xl transition-all ${
                    simDays === d
                      ? 'bg-emerald-500 text-white shadow-md shadow-emerald-500/30'
                      : 'text-[var(--color-on-surface-secondary)] hover:text-[var(--color-on-surface)]'
                  }`}
                >
                  +{d} Days Horizon
                </button>
              ))}
            </div>
          </div>

          {/* 3 Comparative Future Scenarios */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5 text-xs">
            {/* Scenario A: Delay Action */}
            <GlassTiltCard className="p-6 bg-red-500/5 border-red-500/25 space-y-3.5">
              <div className="flex items-center justify-between">
                <span className="font-mono text-red-500 font-bold uppercase text-[11px]">Scenario A</span>
                <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-red-500/10 text-red-500">
                  Critical Danger
                </span>
              </div>
              <h5 className="text-lg font-bold text-[var(--color-on-surface)]">
                Delay Treatment ({simDays}d Horizon)
              </h5>
              <p className="text-xs text-[var(--color-on-surface-secondary)] leading-relaxed">
                Fungal blast spores spread from tillers into panicle neck tissue, causing irreversible physiological choking.
              </p>
              <div className="pt-3 border-t border-red-500/20 space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-white/70">Projected Yield:</span>
                  <strong className="font-mono text-red-500 text-sm">
                    {simDays === '1' ? '4,900' : simDays === '3' ? '4,350' : simDays === '7' ? '3,750' : '2,800'} kg/ha*
                  </strong>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white/70">Crop Damage Loss:</span>
                  <strong className="font-mono text-red-600 text-sm">
                    {simDays === '1' ? '-6%' : simDays === '3' ? '-18%' : simDays === '7' ? '-34%' : '-52%'}
                  </strong>
                </div>
              </div>
            </GlassTiltCard>

            {/* Scenario B: Recommended Precision Action */}
            <GlassTiltCard className="p-6 bg-emerald-500/10 border-2 border-emerald-500 space-y-3.5 shadow-xl shadow-emerald-500/15">
              <div className="flex items-center justify-between">
                <span className="font-mono text-emerald-500 font-bold uppercase text-[11px]">Scenario B</span>
                <span className="text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full bg-emerald-500 text-white uppercase tracking-wider">
                  Recommended Action
                </span>
              </div>
              <h5 className="text-lg font-bold text-[var(--color-on-surface)]">
                Organic Spray at 18:00 hrs
              </h5>
              <p className="text-xs text-[var(--color-on-surface-secondary)] leading-relaxed">
                Targeted bio-fungicide halts spore replication within 36 hours before impending evening humidity spike.
              </p>
              <div className="pt-3 border-t border-emerald-500/30 space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-white/70">Projected Yield:</span>
                  <strong className="font-mono text-emerald-400 text-sm">5,280 kg/ha*</strong>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white/70">Farmer Net Revenue:</span>
                  <strong className="font-mono text-emerald-300 text-sm">₹92,400 / ha</strong>
                </div>
              </div>
            </GlassTiltCard>

            {/* Scenario C: Organic Preventive */}
            <GlassTiltCard className="p-6 bg-cyan-500/5 border-cyan-500/25 space-y-3.5">
              <div className="flex items-center justify-between">
                <span className="font-mono text-cyan-500 font-bold uppercase text-[11px]">Scenario C</span>
                <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400">
                  Bio-Shield
                </span>
              </div>
              <h5 className="text-lg font-bold text-[var(--color-on-surface)]">
                Pseudomonas fluorescens
              </h5>
              <p className="text-xs text-[var(--color-on-surface-secondary)] leading-relaxed">
                Rhizosphere inoculation creates competitive microbial exclusion with zero agrochemical chemical residue.
              </p>
              <div className="pt-3 border-t border-cyan-500/20 space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-white/70">Projected Yield:</span>
                  <strong className="font-mono text-cyan-400 text-sm">4,850 kg/ha*</strong>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white/70">Soil Microbiome Health:</span>
                  <strong className="font-mono text-cyan-300 text-sm">+28% Diversity</strong>
                </div>
              </div>
            </GlassTiltCard>
          </div>

          <div className="text-center pt-2">
            <span className="text-[11px] text-[var(--color-on-surface-tertiary)] italic font-mono">
              * Non-negotiable safety label: Modelled estimate from DSSAT v4.8 mathematical simulation. Verified against KVK Palakkad empirical field trials.
            </span>
          </div>
        </div>
      </section>

      {/* =========================================================================
          CHAPTER 08: PREDICT -> PREVENT -> PROTECT ("Turn Prediction Into Action.")
          Interactive Risk Reduction Pipeline (72% Risk -> 10% Residual Risk)
          ========================================================================= */}
      <section
        data-chapter="8"
        className="relative z-10 py-24 px-4 md:px-10 max-w-7xl mx-auto space-y-12 snap-scroll-section"
      >
        <div className="st-layer-1 text-center space-y-3 max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-red-500/10 text-red-500 border border-red-500/20 text-xs font-mono font-bold tracking-widest uppercase">
            <ShieldCheck size={13} />
            <span>08 · Action Engine</span>
          </div>
          <h2 className="text-3xl md:text-5xl font-black tracking-tight text-[var(--color-on-surface)]">
            Turn Prediction Into Action.
          </h2>
          <p className="text-sm md:text-base text-[var(--color-on-surface-secondary)] leading-relaxed">
            Prediction is useless without decisive intervention. Watch how Agri-SAGE systematically crushes crop loss risk from 72% down to 10%.
          </p>
        </div>

        {/* Visual Workflow Cards with Interactive Simulation Button */}
        <div className="glass-panel p-8 sm:p-10 space-y-8 border-emerald-500/30">
          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 items-center">
            {/* Step 1: 72% Risk Alert */}
            <div className="glass-panel p-6 text-center space-y-2 border-red-500/40 bg-red-500/5">
              <div className="text-4xl font-black text-red-500 font-mono">
                {riskSimulated ? '72%' : '72%'}
              </div>
              <div className="text-xs font-bold uppercase text-[var(--color-on-surface)]">Initial Crop Risk</div>
              <p className="text-[11px] text-[var(--color-on-surface-secondary)]">RH &gt; 85% + Thermal spore signature</p>
            </div>

            <div className="hidden sm:flex justify-center text-emerald-500">
              <ArrowRight size={28} className="animate-pulse" />
            </div>

            {/* Step 2: Multi-Agent Synthesis */}
            <div className="glass-panel p-6 text-center space-y-2 border-cyan-500/40 bg-cyan-500/5">
              <Cpu size={32} className="text-cyan-400 mx-auto" />
              <div className="text-xs font-bold uppercase text-[var(--color-on-surface)]">Multi-Agent Synthesis</div>
              <p className="text-[11px] text-[var(--color-on-surface-secondary)]">DSSAT Simulation + CIB&RC Validation</p>
            </div>

            {/* Step 3: Residual Protected Risk */}
            <div className={`glass-panel p-6 text-center space-y-2 transition-all duration-500 ${
              riskSimulated
                ? 'border-emerald-500 bg-emerald-500/15 shadow-xl shadow-emerald-500/20'
                : 'border-emerald-500/40 bg-emerald-500/5'
            }`}>
              <div className="text-4xl font-black text-emerald-400 font-mono">
                {riskSimulated ? '10%' : '10%'}
              </div>
              <div className="text-xs font-bold uppercase text-[var(--color-on-surface)]">Residual Risk</div>
              <p className="text-[11px] text-[var(--color-on-surface-secondary)]">Harvest Secured · 86% Hazard Neutralized</p>
            </div>
          </div>

          {/* Action Trigger Button */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-[var(--color-outline-variant)]">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
                <CheckCircle2 size={20} />
              </div>
              <div>
                <strong className="text-sm font-bold text-[var(--color-on-surface)] block">
                  Simulate Full Causal Action Loop
                </strong>
                <span className="text-xs text-[var(--color-on-surface-secondary)]">
                  Verify how targeted bio-fungicide reduces risk in real time
                </span>
              </div>
            </div>

            <button
              type="button"
              onClick={handleSimulateRisk}
              className="btn btn-primary text-xs h-11 px-6 font-bold flex items-center gap-2"
            >
              <Sparkles size={15} />
              <span>{riskSimulated ? 'Simulation Applied (Verified Safe)' : 'Run Protection Simulation'}</span>
            </button>
          </div>
        </div>
      </section>

      {/* =========================================================================
          CHAPTER 09: FARMER ADVISORY ("Complex Intelligence. Simple Decisions.")
          Photorealistic Kerala Farmer Tablet Visual + Malayalam Voice Audio Demo
          ========================================================================= */}
      <section
        data-chapter="9"
        className="relative z-10 py-24 px-4 md:px-10 max-w-7xl mx-auto space-y-12 snap-scroll-section"
      >
        <div className="st-layer-1 grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
          <div className="lg:col-span-6 space-y-6">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 text-xs font-mono font-bold tracking-widest uppercase">
              <Smartphone size={13} />
              <span>09 · The Human Ground Truth</span>
            </div>
            <h2 className="text-3xl md:text-5xl font-black tracking-tight text-[var(--color-on-surface)] leading-tight">
              Complex Intelligence. Simple Decisions.
            </h2>
            <p className="text-sm md:text-base text-[var(--color-on-surface-secondary)] leading-relaxed">
              Smallholder farmers don't need neural network loss curves. They need zero-jargon instructions delivered in their mother tongue: what to inspect, exactly when to spray, and how much water to dilute.
            </p>

            {/* Farmer Advisory Checklist */}
            <div className="space-y-3 text-xs">
              <div className="flex items-center gap-3.5 p-3.5 rounded-2xl bg-[var(--color-surface)] border border-[var(--color-outline-variant)]">
                <CheckCircle2 size={18} className="text-emerald-500 shrink-0" />
                <div>
                  <strong className="text-sm font-bold text-[var(--color-on-surface)] block">
                    Bhashini Voice Briefing in Malayalam & Tamil
                  </strong>
                  <span className="text-[11px] text-[var(--color-on-surface-secondary)]">
                    "കീടബാധ തടയാൻ വൈകുന്നേരം 6 മണിക്ക് ഓർഗാനിക് കുമിൾനാശിനി പ്രയോഗിക്കുക"
                  </span>
                </div>
              </div>

              <div className="flex items-center gap-3.5 p-3.5 rounded-2xl bg-[var(--color-surface)] border border-[var(--color-outline-variant)]">
                <CheckCircle2 size={18} className="text-emerald-500 shrink-0" />
                <div>
                  <strong className="text-sm font-bold text-[var(--color-on-surface)] block">
                    Precipitation Window Optimization
                  </strong>
                  <span className="text-[11px] text-[var(--color-on-surface-secondary)]">
                    Calculates exact 4-hour window before rain to avoid expensive chemical washouts
                  </span>
                </div>
              </div>

              <div className="flex items-center gap-3.5 p-3.5 rounded-2xl bg-[var(--color-surface)] border border-[var(--color-outline-variant)]">
                <CheckCircle2 size={18} className="text-emerald-500 shrink-0" />
                <div>
                  <strong className="text-sm font-bold text-[var(--color-on-surface)] block">
                    Direct PMFBY & State Subsidy Matching
                  </strong>
                  <span className="text-[11px] text-[var(--color-on-surface-secondary)]">
                    Automatically generates insurance claim certificates for verified unpreventable damage
                  </span>
                </div>
              </div>
            </div>

            {/* Voice Audio & WhatsApp Interaction Buttons */}
            <div className="flex items-center gap-3 pt-2">
              <button
                type="button"
                onClick={handlePlayVoiceAdvisory}
                className={`btn text-xs h-11 px-5 font-bold flex items-center gap-2 ${
                  isPlayingAudio
                    ? 'btn-primary shadow-lg shadow-emerald-500/30'
                    : 'btn-secondary'
                }`}
              >
                <Play size={14} className={isPlayingAudio ? 'animate-spin' : ''} />
                <span>{isPlayingAudio ? 'Playing Malayalam Advisory...' : 'Listen to Voice Advisory (മലയാളം)'}</span>
              </button>

              <button
                type="button"
                onClick={handleShareWhatsApp}
                className="btn btn-outline text-xs h-11 px-4 font-bold flex items-center gap-1.5"
                title="Send Advisory Card via WhatsApp"
              >
                {shareSent ? <Check size={14} className="text-emerald-500" /> : <Send size={14} />}
                <span>{shareSent ? 'Advisory Dispatched!' : 'WhatsApp Share'}</span>
              </button>
            </div>
          </div>

          {/* Farmer with Tablet Image Visualizer */}
          <div className="lg:col-span-6 relative rounded-3xl overflow-hidden border border-[var(--color-outline-variant)] shadow-2xl bg-black group">
            <img
              src={getPublicUrl('/images/farmer_tablet.jpg')}
              alt="Farmer in Kerala paddy field inspecting advisory on digital tablet"
              className="w-full h-[460px] md:h-[560px] object-cover filter contrast-105"
            />

            {/* Floating Glass Advisory Card (Matching User Blueprint Section 09) */}
            <div className="absolute bottom-6 left-6 right-6 glass-panel p-4 md:p-5 backdrop-blur-2xl border border-white/25 text-white shadow-2xl bg-slate-950/80">
              <div className="flex items-center justify-between pb-2 border-b border-white/15 mb-3">
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
                  <strong className="text-xs font-mono uppercase tracking-wider text-emerald-300">
                    Palakkad Farmer Advisory Card #402
                  </strong>
                </div>
                <span className="text-[10px] font-mono text-white/60">Delivered via SMS/WhatsApp</span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs mb-3">
                <div className="p-2 rounded-xl bg-white/5 border border-white/10">
                  <span className="text-[10px] text-white/60 font-mono block">Crop Health</span>
                  <strong className="text-emerald-400 font-bold">Good</strong>
                </div>
                <div className="p-2 rounded-xl bg-white/5 border border-white/10">
                  <span className="text-[10px] text-white/60 font-mono block">Disease Risk</span>
                  <strong className="text-amber-400 font-bold">Moderate</strong>
                </div>
                <div className="p-2 rounded-xl bg-white/5 border border-white/10">
                  <span className="text-[10px] text-white/60 font-mono block">Irrigation</span>
                  <strong className="text-blue-400 font-bold">Recommended</strong>
                </div>
                <div className="p-2 rounded-xl bg-white/5 border border-white/10">
                  <span className="text-[10px] text-white/60 font-mono block">Next 24h</span>
                  <strong className="text-teal-400 font-bold">RH 88%</strong>
                </div>
              </div>

              <div className="p-2.5 rounded-xl bg-emerald-500/15 border border-emerald-400/30 text-emerald-200 text-xs flex items-center justify-between">
                <span>Recommended: <strong>Apply organic Trichoderma viride (2.5g/L)</strong></span>
                <span className="font-mono text-[10px] text-emerald-400 font-bold uppercase">Safe Dosage</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          CHAPTER 10: THE FUTURE FARM ("One Intelligent Field Becomes a Connected World.")
          Planetary Farm Network Mesh & Regional Node Cluster
          ========================================================================= */}
      <section
        data-chapter="10"
        className="relative z-10 py-24 px-4 md:px-10 max-w-7xl mx-auto space-y-12 overflow-hidden snap-scroll-section"
      >
        {/* Parallax Decorations – Chapter 10 */}
        <div data-parallax-speed="0.4" data-parallax-rotate="8" className="parallax-decoration parallax-orb parallax-orb-cyan parallax-glow-pulse w-[240px] h-[240px] -top-20 -right-24 opacity-25 hidden lg:block" />
        <div data-parallax-speed="1.5" className="parallax-decoration parallax-diamond w-[22px] h-[22px] top-[35%] left-[5%] opacity-30 hidden md:block" />
        <div data-parallax-speed="0.6" className="parallax-decoration parallax-ring-dashed w-[180px] h-[180px] bottom-[15%] right-[10%] opacity-15 hidden lg:block" />

        <div className="st-layer-1 text-center space-y-3 max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 text-xs font-mono font-bold tracking-widest uppercase">
            <Globe size={13} />
            <span>10 · Planetary Scale</span>
          </div>
          <h2 className="text-3xl md:text-5xl font-black tracking-tight text-[var(--color-on-surface)]">
            One Intelligent Field Becomes a Connected World.
          </h2>
          <p className="text-sm md:text-base text-[var(--color-on-surface-secondary)] leading-relaxed">
            Scalable from a single 1-hectare rice paddy in Palakkad to hundreds of thousands of smallholder holdings across India and global breadbaskets.
          </p>
        </div>

        {/* Global Network Image Display with Glass Metrics */}
        <div className="relative rounded-3xl overflow-hidden border border-[var(--color-outline-variant)] shadow-2xl bg-black">
          <img
            src={getPublicUrl('/images/network_globe.jpg')}
            alt="Global Connected Farm Network Digital Twin"
            className="w-full h-[460px] md:h-[620px] object-cover filter contrast-105"
          />

          {/* Regional Cluster Selector */}
          <div className="absolute top-6 left-6 z-20 flex flex-wrap gap-2">
            {[
              { id: 'kerala', name: 'Palakkad Paddy Belt', count: '142 Farms' },
              { id: 'punjab', name: 'Punjab Wheat Plain', count: '320 Farms' },
              { id: 'maharashtra', name: 'Vidarbha Cotton', count: '210 Farms' },
              { id: 'california', name: 'Central Valley', count: '85 Farms' },
              { id: 'africa', name: 'Rift Valley Maize', count: '240 Farms' }
            ].map((cl) => (
              <button
                key={cl.id}
                type="button"
                onClick={() => {
                  playHoverChime(520);
                  setSelectedCluster(cl.id as typeof selectedCluster);
                }}
                className={`px-3 py-1.5 rounded-xl text-xs font-mono font-bold transition-all ${
                  selectedCluster === cl.id
                    ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/30'
                    : 'bg-black/60 backdrop-blur-md text-white/70 hover:text-white border border-white/10'
                }`}
              >
                {cl.name} ({cl.count})
              </button>
            ))}
          </div>

          {/* Bottom Planetary Scale Badges */}
          <div className="absolute inset-x-0 bottom-0 p-6 md:p-10 bg-gradient-to-t from-black/90 via-black/40 to-transparent flex items-end">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 w-full max-w-3xl text-center text-white">
              <GlassTiltCard className="p-4 bg-slate-900/80 border-white/20">
                <div className="text-3xl md:text-5xl font-black text-emerald-400 font-mono">1,000+</div>
                <div className="text-xs text-white/80 font-bold uppercase mt-1 tracking-wider">Farms Onboarded</div>
              </GlassTiltCard>

              <GlassTiltCard className="p-4 bg-slate-900/80 border-white/20">
                <div className="text-3xl md:text-5xl font-black text-cyan-400 font-mono">50+</div>
                <div className="text-xs text-white/80 font-bold uppercase mt-1 tracking-wider">Agro-Basins</div>
              </GlassTiltCard>

              <GlassTiltCard className="p-4 bg-slate-900/80 border-white/20">
                <div className="text-3xl md:text-5xl font-black text-teal-400 font-mono">1</div>
                <div className="text-xs text-white/80 font-bold uppercase mt-1 tracking-wider">Global Digital Twin</div>
              </GlassTiltCard>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          CHAPTER 11: AGRI-SAGE PLATFORM ("Everything in One Intelligence Layer.")
          Workstation Console Preview & Direct Frame 3 Entry
          ========================================================================= */}
      <section
        data-chapter="11"
        className="relative z-10 py-24 px-4 md:px-10 max-w-7xl mx-auto space-y-12 snap-scroll-section"
      >
        <div className="st-layer-1 text-center space-y-3 max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 text-xs font-mono font-bold tracking-widest uppercase">
            <Zap size={13} />
            <span>11 · Full Intelligence Workstation</span>
          </div>
          <h2 className="text-3xl md:text-5xl font-black tracking-tight text-[var(--color-on-surface)]">
            Everything in One Intelligence Layer.
          </h2>
          <p className="text-sm md:text-base text-[var(--color-on-surface-secondary)] leading-relaxed">
            Experience the complete expert workstation: Agronomist Triage Queue, Multi-Spectral Evidence Inspector, Outbreak Radar, and Farmer Advisory Generator.
          </p>
        </div>

        {/* Interactive Platform Tabs Preview */}
        <div className="glass-panel p-6 sm:p-10 space-y-8 border-emerald-500/35 relative overflow-hidden">
          {/* Workstation Console Tab Bar */}
          <div className="flex items-center justify-between flex-wrap gap-4 pb-4 border-b border-[var(--color-outline-variant)]">
            <div className="flex flex-wrap gap-2 text-xs font-mono font-bold">
              {[
                { id: 'triage', label: 'Triage Queue' },
                { id: 'multispectral', label: 'Multi-Spectral Inspector' },
                { id: 'radar', label: 'Outbreak Radar' },
                { id: 'simulator', label: 'Mobile Viewfinder' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  type="button"
                  onClick={() => {
                    playHoverChime(490);
                    setPlatformTab(tab.id as typeof platformTab);
                  }}
                  className={`px-4 py-2 rounded-xl transition-all ${
                    platformTab === tab.id
                      ? 'bg-emerald-500 text-white shadow-md shadow-emerald-500/30'
                      : 'bg-[var(--color-surface)] text-[var(--color-on-surface-secondary)] hover:text-[var(--color-on-surface)] border border-[var(--color-outline-variant)]'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            <div className="flex items-center gap-2 text-xs font-mono text-emerald-600 dark:text-emerald-400 font-bold">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
              <span>Frame 3 Live & Ready</span>
            </div>
          </div>

          {/* Workstation Tab Content Preview Box */}
          <div className="p-6 rounded-2xl bg-[var(--color-surface-variant)] border border-[var(--color-outline-variant)] space-y-4">
            {platformTab === 'triage' && (
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <strong className="text-base font-bold text-[var(--color-on-surface)]">
                    Agronomist Triage Console (Frame 3)
                  </strong>
                  <span className="text-xs font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-500 font-bold">
                    12 Pending Cases
                  </span>
                </div>
                <p className="text-xs text-[var(--color-on-surface-secondary)] leading-relaxed">
                  Real-time triage queue ranking agricultural incoming incident reports by risk severity, crop economic value, and epidemiological spread probability.
                </p>
              </div>
            )}

            {platformTab === 'multispectral' && (
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <strong className="text-base font-bold text-[var(--color-on-surface)]">
                    Split-Screen Multi-Spectral Evidence Inspector
                  </strong>
                  <span className="text-xs font-mono px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-500 font-bold">
                    6 Filters
                  </span>
                </div>
                <p className="text-xs text-[var(--color-on-surface-secondary)] leading-relaxed">
                  Toggle between RGB Visible, Thermal IR Hotspots, Vegetation Stress NDVI, and High-Contrast Edge Saliency to inspect mycelial spore boundaries.
                </p>
              </div>
            )}

            {platformTab === 'radar' && (
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <strong className="text-base font-bold text-[var(--color-on-surface)]">
                    Outbreak Radar & Cluster Tracker
                  </strong>
                  <span className="text-xs font-mono px-2 py-0.5 rounded bg-red-500/20 text-red-500 font-bold">
                    Regional Alert
                  </span>
                </div>
                <p className="text-xs text-[var(--color-on-surface-secondary)] leading-relaxed">
                  Interactive radar sweep tracking pathogen vectors across Palakkad, Alappuzha, and Wayanad clusters to prevent regional epidemic diffusion.
                </p>
              </div>
            )}

            {platformTab === 'simulator' && (
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <strong className="text-base font-bold text-[var(--color-on-surface)]">
                    Mobile Viewfinder Simulator
                  </strong>
                  <span className="text-xs font-mono px-2 py-0.5 rounded bg-purple-500/20 text-purple-500 font-bold">
                    Android CameraX
                  </span>
                </div>
                <p className="text-xs text-[var(--color-on-surface-secondary)] leading-relaxed">
                  Interactive simulation of low-end smartphone CameraX optical pipeline with blur detection, glare correction, and on-device INT8 quantization.
                </p>
              </div>
            )}

            {/* Launch Frame 3 Button */}
            <div className="pt-4 flex justify-end">
              <button
                type="button"
                onClick={() => {
                  playSuccessTone();
                  onDirectPlatformAccess();
                }}
                className="btn btn-primary text-xs h-11 px-6 font-bold flex items-center gap-2 shadow-xl shadow-emerald-500/30"
              >
                <span>Launch Full Frame 3 Workstation</span>
                <ArrowRight size={15} />
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          CHAPTER 12: FINAL CALL TO ACTION ("The Future of Agriculture Starts With Understanding.")
          Glowing Emerald Portal & Ecosystem Navigation
          ========================================================================= */}
      <section
        data-chapter="12"
        className="relative z-10 py-28 px-4 md:px-10 max-w-7xl mx-auto text-center space-y-8 overflow-hidden snap-scroll-section"
      >
        {/* Ambient Radial Glow */}
        <div className="absolute inset-0 glow-backdrop-emerald pointer-events-none" />

        {/* Parallax Decorations – Chapter 12 (Final CTA) */}
        <div data-parallax-speed="0.35" data-parallax-rotate="20" className="parallax-decoration parallax-orb parallax-orb-emerald parallax-glow-pulse-slow w-[300px] h-[300px] -top-16 -left-24 opacity-20 hidden lg:block" />
        <div data-parallax-speed="1.6" className="parallax-decoration parallax-orb parallax-orb-cyan parallax-glow-pulse w-[80px] h-[80px] bottom-[30%] right-[10%] opacity-35 hidden md:block" />
        <div data-parallax-speed="-0.2" data-parallax-rotate="-25" className="parallax-decoration parallax-ring w-[150px] h-[150px] top-[40%] right-[20%] opacity-20 hidden xl:block" />

        <div className="relative z-10 w-20 h-20 rounded-3xl bg-gradient-to-tr from-emerald-600 via-emerald-500 to-teal-400 text-white flex items-center justify-center mx-auto shadow-2xl shadow-emerald-500/40 border border-emerald-300/40 hologram-float">
          <Sprout size={42} />
        </div>

        <div className="relative z-10 space-y-4 max-w-3xl mx-auto">
          <div className="text-xs font-mono font-bold text-emerald-500 uppercase tracking-widest">
            12 · From A Single Seed To A Smarter Tomorrow
          </div>
          <h2
            ref={ctaTitleRef}
            className="text-3xl md:text-6xl font-black tracking-tight text-[var(--color-on-surface)] leading-tight"
          >
            The Future of Agriculture Starts With Understanding.
          </h2>
          <p className="text-base sm:text-lg text-[var(--color-on-surface-secondary)] max-w-xl mx-auto leading-relaxed">
            Join thousands of smallholder farmers, agronomists, and institutions transforming agriculture through verifiable intelligence.
          </p>
        </div>

        {/* Dual CTA Navigation */}
        <div className="relative z-10 flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
          <button
            type="button"
            onClick={() => {
              playSuccessTone();
              onEnterAuth();
            }}
            className="btn btn-primary text-sm h-14 px-9 font-bold flex items-center gap-2.5 shadow-2xl shadow-emerald-500/40 w-full sm:w-auto hover:scale-105 transition-transform"
          >
            <span>Sign In to Agri-SAGE (Frame 2)</span>
            <ArrowRight size={18} />
          </button>

          <button
            type="button"
            onClick={() => {
              playHoverChime(650);
              onDirectPlatformAccess();
            }}
            className="btn btn-outline text-sm h-14 px-8 font-bold w-full sm:w-auto hover:border-emerald-400"
          >
            <span>Direct Demo Access (Frame 3)</span>
          </button>
        </div>

        {/* Recommended Tech Stack Badges (From User Reference Image) */}
        <div className="relative z-10 pt-16 border-t border-[var(--color-outline-variant)]">
          <span className="text-[11px] font-mono uppercase tracking-widest text-[var(--color-on-surface-tertiary)] block mb-4">
            Production Engineering Architecture
          </span>
          <div className="flex flex-wrap items-center justify-center gap-3 text-xs font-mono text-[var(--color-on-surface-secondary)]">
            <span className="px-3 py-1.5 rounded-xl bg-[var(--color-surface)] border border-[var(--color-outline-variant)]">React 19 + TypeScript</span>
            <span className="px-3 py-1.5 rounded-xl bg-[var(--color-surface)] border border-[var(--color-outline-variant)]">Three.js 3D WebGL</span>
            <span className="px-3 py-1.5 rounded-xl bg-[var(--color-surface)] border border-[var(--color-outline-variant)]">DSSAT v4.8 Biophysical</span>
            <span className="px-3 py-1.5 rounded-xl bg-[var(--color-surface)] border border-[var(--color-outline-variant)]">CIB&RC Registry Safety</span>
            <span className="px-3 py-1.5 rounded-xl bg-[var(--color-surface)] border border-[var(--color-outline-variant)]">Offline-First IndexedDB</span>
            <span className="px-3 py-1.5 rounded-xl bg-[var(--color-surface)] border border-[var(--color-outline-variant)]">Tailwind CSS v4</span>
          </div>
        </div>

        <div className="relative z-10 text-xs font-mono text-emerald-600 dark:text-emerald-400 font-bold uppercase tracking-widest">
          Smarter Farms. Healthier Planet.
        </div>
      </section>

      {/* Frame 1 Institutional Hover Footer */}
      <HoverFooter />
    </div>
  );
};
