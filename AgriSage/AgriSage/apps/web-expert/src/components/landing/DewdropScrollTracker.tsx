import React, { useEffect, useRef, useState, useMemo, useCallback } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import {
  damp,
  lerp,
  clamp,
  mapRange,
  evaluateSpline,
  SplinePoint,
  calculateDropletPhysics
} from '../../utils/motionMath';
import { FluidRippleShaderCanvas, RippleEvent } from './FluidRippleShaderCanvas';
import { playHoverChime, playSuccessTone, getAudioMuteState } from '../../utils/audioFX';
import {
  Sprout,
  Droplets,
  Zap,
  Activity,
  Compass,
  Cpu,
  ShieldCheck,
  TrendingDown,
  Globe,
  Radio,
  Sliders,
  Sparkles,
  Maximize2
} from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

interface ChapterMeta {
  index: number;
  id: string;
  nameEn: string;
  nameMl: string;
  metric: string;
  color: string;
  glowColor: string;
  icon: React.ReactNode;
}

const CHAPTER_METAS: ChapterMeta[] = [
  { index: 1, id: '1', nameEn: 'Space to Soil', nameMl: 'ആകാശം മുതൽ മണ്ണുവരെ', metric: '100% Saturation', color: '#00f0ff', glowColor: 'rgba(0, 240, 255, 0.75)', icon: <Globe size={12} /> },
  { index: 2, id: '2', nameEn: 'The Crisis', nameMl: 'പ്രതിസന്ധി തിരിച്ചറിയൽ', metric: '38°C Thermal Stress', color: '#f59e0b', glowColor: 'rgba(245, 158, 11, 0.75)', icon: <TrendingDown size={12} /> },
  { index: 3, id: '3', nameEn: 'Farm 360°', nameMl: 'ഫാം 360° ദൃശ്യം', metric: '0.74 NDVI Vigour', color: '#10b981', glowColor: 'rgba(16, 185, 129, 0.75)', icon: <Compass size={12} /> },
  { index: 4, id: '4', nameEn: 'See The Invisible', nameMl: 'അദൃശ്യമായത് കാണുക', metric: '780nm RedEdge Shift', color: '#a855f7', glowColor: 'rgba(168, 85, 247, 0.75)', icon: <Sparkles size={12} /> },
  { index: 5, id: '5', nameEn: 'Neural Core', nameMl: 'ഇന്റലിജൻസ് കോർ', metric: 'DSSAT Biophysical v4.8', color: '#14b8a6', glowColor: 'rgba(20, 184, 166, 0.75)', icon: <Cpu size={12} /> },
  { index: 6, id: '6', nameEn: 'Multi-Agent Swarm', nameMl: 'മൾട്ടി-ഏജന്റ് ശൃംഖല', metric: '6 Agents Active', color: '#3b82f6', glowColor: 'rgba(59, 130, 246, 0.75)', icon: <Radio size={12} /> },
  { index: 7, id: '7', nameEn: 'Crop Simulator', nameMl: 'വിള സിമുലേഷൻ', metric: '+14 Day Projection', color: '#22c55e', glowColor: 'rgba(34, 197, 94, 0.75)', icon: <Sliders size={12} /> },
  { index: 8, id: '8', nameEn: 'Risk Reduction', nameMl: 'അപകടസാധ്യത കുറയ്ക്കൽ', metric: '72% → 10% Residual Risk', color: '#6366f1', glowColor: 'rgba(99, 102, 241, 0.75)', icon: <ShieldCheck size={12} /> },
  { index: 9, id: '9', nameEn: 'Farmer Advisory', nameMl: 'കർഷക ഉപദേശം', metric: 'Malayalam Audio Synced', color: '#eab308', glowColor: 'rgba(234, 179, 8, 0.75)', icon: <Activity size={12} /> },
  { index: 10, id: '10', nameEn: 'Global Twin', nameMl: 'ആഗോള നെറ്റ്‌വർക്ക്', metric: '1,000+ Farms Active', color: '#0ea5e9', glowColor: 'rgba(14, 165, 233, 0.75)', icon: <Globe size={12} /> },
  { index: 11, id: '11', nameEn: 'Workstation', nameMl: 'വർക്ക്സ്റ്റേഷൻ കൺസോൾ', metric: 'Frame 3 Quantum Console', color: '#10b981', glowColor: 'rgba(16, 185, 129, 0.75)', icon: <Maximize2 size={12} /> },
  { index: 12, id: '12', nameEn: 'Final Call', nameMl: 'ഭാവിയിലേക്കുള്ള വിളി', metric: 'Singularity Threshold', color: '#10b981', glowColor: 'rgba(16, 185, 129, 0.9)', icon: <Zap size={12} /> }
];

/**
 * 12 Narrative Anchors across the screen in normalized percentages [0..100]
 * Weaves across the X-axis through open corridors without overlapping text
 */
const SPLINE_WAYPOINTS: SplinePoint[] = [
  { x: 48.2, y: 24.5 }, // Ch 01: Hero (Leaf petiole tip sitting directly above 'ı' stem in Agri-SAGE)
  { x: 78, y: 28 },  // Ch 02: The Problem (Weaving right corridor)
  { x: 22, y: 36 },  // Ch 03: Farm 360 (Drifting left corridor)
  { x: 80, y: 44 },  // Ch 04: See The Invisible (Right corridor)
  { x: 30, y: 52 },  // Ch 05: Neural Core (Left corridor)
  { x: 74, y: 48 },  // Ch 06: Multi-Agent (Right corridor)
  { x: 24, y: 56 },  // Ch 07: Crop Sim (Left corridor)
  { x: 76, y: 62 },  // Ch 08: Risk Reduction (Right corridor)
  { x: 28, y: 58 },  // Ch 09: Farmer Advisory (Left corridor)
  { x: 80, y: 66 },  // Ch 10: Global Network (Right corridor)
  { x: 32, y: 60 },  // Ch 11: Workstation (Left corridor)
  { x: 50, y: 72 }   // Ch 12: Final CTA (Landing in seed singularity!)
];

interface DewdropScrollTrackerProps {
  containerRef?: React.RefObject<HTMLDivElement | null>;
  activeChapter: number;
  scrollProgress: number; // 0 to 100
  onScrollToChapter: (chapterIndex: number) => void;
  lang: 'en' | 'ml';
}

/**
 * The Master "Dewdrop of Agri-Intelligence" SVG Animation Ecosystem
 * 
 * Key Features:
 * - 100% PROMINENTLY VISIBLE FIXED VIEWPORT OVERLAY (z-40 pointer-events-none)
 * - Pinned continuously across all 12 chapters from top to bottom (0% to 100% scroll)
 * - Full-Canvas Sinuous River Path weaving smoothly across X and Y axes
 * - Zero waypoint dots or cluttered node circles (Clean, continuous fluid motion)
 * - Dynamic teardrop vector rotation along Catmull-Rom spline tangents
 * - Velocity-based surface tension deformation (stretches on fast scroll)
 * - Chained 4-body LERP daughter droplet viscosity tail
 * - Hardware-accelerated SVG liquid refraction filter shader
 * - GPU Canvas fluid ripple & caustic shockwave shader
 * - Compact Scrollytelling Telemetry Pill (bottom-right) ensuring zero text collision
 */
export const DewdropScrollTracker: React.FC<DewdropScrollTrackerProps> = ({
  activeChapter,
  scrollProgress,
  onScrollToChapter,
  lang
}) => {
  const [ripples, setRipples] = useState<RippleEvent[]>([]);

  // SVG and physics refs
  const svgRef = useRef<SVGSVGElement | null>(null);
  const mainDropRef = useRef<SVGGElement | null>(null);
  const daughter1Ref = useRef<SVGGElement | null>(null);
  const daughter2Ref = useRef<SVGGElement | null>(null);
  const daughter3Ref = useRef<SVGGElement | null>(null);
  const daughter4Ref = useRef<SVGGElement | null>(null);

  // Smooth progress state (LERP spring)
  const smoothProgressRef = useRef(scrollProgress / 100);

  // Trailing positions for LERP
  const posTarget = useRef({ x: 0, y: 0, angle: 0 });
  const posMain = useRef({ x: 0, y: 0, angle: 0 });
  const posD1 = useRef({ x: 0, y: 0 });
  const posD2 = useRef({ x: 0, y: 0 });
  const posD3 = useRef({ x: 0, y: 0 });
  const posD4 = useRef({ x: 0, y: 0 });

  // Instant scroll velocity tracking
  const lastScrollY = useRef(window.scrollY);
  const lastScrollTime = useRef(performance.now());
  const velocityRef = useRef(0);
  const [velocityHUD, setVelocityHUD] = useState(0);

  // Active theme color
  const currentMeta = CHAPTER_METAS[Math.min(Math.max(activeChapter - 1, 0), CHAPTER_METAS.length - 1)];

  // Trigger milestone ripple
  const triggerRippleAt = useCallback((x: number, y: number, color: string, intensity = 0.9) => {
    setRipples((prev) => [
      ...prev.slice(-6),
      {
        x,
        y,
        color,
        maxRadius: 280,
        speed: 5.0,
        intensity
      }
    ]);
  }, []);

  // Monitor chapter changes to emit biophilic milestone ripple and tone
  const prevChapter = useRef(activeChapter);
  useEffect(() => {
    if (prevChapter.current !== activeChapter) {
      prevChapter.current = activeChapter;
      if (!getAudioMuteState()) {
        playHoverChime(440 + activeChapter * 45);
      }
      triggerRippleAt(posMain.current.x, posMain.current.y, currentMeta.color, 0.95);
    }
  }, [activeChapter, currentMeta.color, triggerRippleAt]);

  // Optimized 144Hz+ High-Precision RAF Animation Loop
  useEffect(() => {
    let animId: number;
    let prevTime = performance.now();
    let cachedHeroAnchorPos: { x: number; y: number } | null = null;
    let cachedFooterAnchorPos: { x: number; y: number } | null = null;
    let lastAnchorCheck = 0;

    // Cache hero and footer anchor positions on top/bottom scroll or resize (zero layout thrashing in RAF)
    const updateAnchorPos = () => {
      // 1. Hero Title 'i' Anchor (Petiole tip of glowing leaf sits directly above stem of letter 'i')
      const heroAnchor = document.getElementById('agri-i-anchor');
      if (heroAnchor) {
        const rect = heroAnchor.getBoundingClientRect();
        if (rect.width > 0 && rect.height > 0) {
          cachedHeroAnchorPos = {
            x: rect.left + rect.width / 2 + 35.5,
            y: rect.top - 4.0
          };
        }
      }

      // 2. Footer Glowing Title 'I' Anchor (Final bottom landing position)
      // Measures exact X position of letter 'I' in AGRI-SAGE (41.5% from left edge of container)
      const footerContainer = document.getElementById('footer-text-hover-container');
      if (footerContainer) {
        const fRect = footerContainer.getBoundingClientRect();
        if (fRect.width > 0 && fRect.height > 0) {
          const exactFooterIX = fRect.left + fRect.width * 0.415;
          const exactFooterIY = fRect.top + fRect.height * 0.20;
          cachedFooterAnchorPos = {
            x: exactFooterIX + 12,
            y: exactFooterIY - 38
          };
        }
      }
    };

    updateAnchorPos();
    window.addEventListener('resize', updateAnchorPos);

    const tick = (currentTime: number) => {
      const dt = Math.min((currentTime - prevTime) / 1000, 0.033); // max 33ms clamp
      prevTime = currentTime;

      const vh = window.innerHeight;
      const vw = window.innerWidth;
      const docHeight = Math.max(document.documentElement.scrollHeight - vh, 1);

      // Direct synchronous scroll Y evaluation (0 to 1) for 144Hz+ hardware sync
      const rawP = Math.min(Math.max(window.scrollY / docHeight, 0), 1);

      // Silky responsive damping without double phase-lag
      smoothProgressRef.current = damp(smoothProgressRef.current, rawP, 24, dt);
      const p = smoothProgressRef.current;

      // Update anchor cache periodically (at most once every 1000ms) or if not yet cached
      if (!cachedHeroAnchorPos || currentTime - lastAnchorCheck > 1000) {
        lastAnchorCheck = currentTime;
        updateAnchorPos();
      }

      // Responsive width factor: full width on desktop, restrained on mobile
      const widthFactor = vw > 1200 ? 1.0 : vw > 768 ? 0.75 : 0.5;

      // Evaluate 2D Catmull-Rom Sinuous River Spline
      const splineResult = evaluateSpline(SPLINE_WAYPOINTS, p);

      const mappedXPercent = 50 + (splineResult.x - 50) * widthFactor;
      const horizontalSway = Math.sin(p * Math.PI * 8) * 22; // 22px organic X sway
      const verticalWave = Math.sin(p * Math.PI * 12) * 35;  // 35px dynamic Y wave
      let targetPixelX = (mappedXPercent / 100) * vw + horizontalSway;
      let targetPixelY = (splineResult.y / 100) * vh + verticalWave;

      // 1. Dynamic Hero Anchor: Lock leaf starting position directly above the 'i' in Agri-SAGE
      if (cachedHeroAnchorPos && p < 0.06) {
        const blend = Math.max(0, 1 - p / 0.06);
        targetPixelX = targetPixelX * (1 - blend) + cachedHeroAnchorPos.x * blend;
        targetPixelY = targetPixelY * (1 - blend) + cachedHeroAnchorPos.y * blend;
      }

      // 2. Dynamic Footer Anchor: Lock leaf final resting position directly above the 'I' in AGRI-SAGE
      if (cachedFooterAnchorPos && p > 0.92) {
        const blend = Math.min(1, (p - 0.92) / 0.08);
        targetPixelX = targetPixelX * (1 - blend) + cachedFooterAnchorPos.x * blend;
        targetPixelY = targetPixelY * (1 - blend) + cachedFooterAnchorPos.y * blend;
      }

      // Resting Orientation: Leaf rests as dot above 'i' at top AND at bottom (+38° up-right to match design spec)
      let targetAngle = splineResult.angleDeg;
      if (p < 0.08) {
        const blend = Math.max(0, 1 - p / 0.08);
        targetAngle = targetAngle * (1 - blend) + 38 * blend;
      } else if (p > 0.92) {
        const blend = Math.min(1, (p - 0.92) / 0.08);
        targetAngle = targetAngle * (1 - blend) + 38 * blend;
      }

      // Resting Scale: Leaf starts and ends slightly smaller (0.70x) to fit perfectly as the 'i' dot
      let initialScale = 1.0;
      if (p < 0.08) {
        const blend = Math.max(0, 1 - p / 0.08);
        initialScale = 1.0 * (1 - blend) + 0.70 * blend;
      } else if (p > 0.92) {
        const blend = Math.min(1, (p - 0.92) / 0.08);
        initialScale = 1.0 * (1 - blend) + 0.70 * blend;
      }

      posTarget.current = {
        x: targetPixelX,
        y: targetPixelY,
        angle: targetAngle
      };

      // Initialize on first frame or at rest at top of page (p < 0.001)
      if ((posMain.current.x === 0 && posMain.current.y === 0) || p < 0.001) {
        posMain.current = { x: targetPixelX, y: targetPixelY, angle: targetAngle };
        posD1.current = { x: targetPixelX, y: targetPixelY };
        posD2.current = { x: targetPixelX, y: targetPixelY };
        posD3.current = { x: targetPixelX, y: targetPixelY };
        posD4.current = { x: targetPixelX, y: targetPixelY };
      }

      // Buttery smooth high-frequency LERP damping for main droplet
      posMain.current.x = damp(posMain.current.x, targetPixelX, 22, dt);
      posMain.current.y = damp(posMain.current.y, targetPixelY, 22, dt);
      posMain.current.angle = damp(posMain.current.angle, targetAngle, 16, dt);

      // Trailing daughter micro-droplets (bead chain) with 144Hz responsive damping
      posD1.current.x = damp(posD1.current.x, posMain.current.x, 18, dt);
      posD1.current.y = damp(posD1.current.y, posMain.current.y, 18, dt);

      posD2.current.x = damp(posD2.current.x, posD1.current.x, 15, dt);
      posD2.current.y = damp(posD2.current.y, posD1.current.y, 15, dt);

      posD3.current.x = damp(posD3.current.x, posD2.current.x, 12, dt);
      posD3.current.y = damp(posD3.current.y, posD2.current.y, 12, dt);

      posD4.current.x = damp(posD4.current.x, posD3.current.x, 9, dt);
      posD4.current.y = damp(posD4.current.y, posD3.current.y, 9, dt);

      // Measure 2D velocity from scroll delta safely
      const currentScroll = window.scrollY;
      const scrollDelta = currentScroll - lastScrollY.current;
      const timeDelta = Math.max((currentTime - lastScrollTime.current) / 1000, 0.004);
      lastScrollY.current = currentScroll;
      lastScrollTime.current = currentTime;

      const rawVel = scrollDelta / timeDelta;
      const instantVel = isNaN(rawVel) || !isFinite(rawVel) ? 0 : clamp(rawVel, -2000, 2000);
      velocityRef.current = damp(velocityRef.current, instantVel, 18, dt);
      if (isNaN(velocityRef.current) || !isFinite(velocityRef.current)) {
        velocityRef.current = 0;
      }

      // Calculate fluid droplet deformation & apply initial resting scale factor
      const direction = velocityRef.current >= 0 ? 1 : -1;
      const physics = calculateDropletPhysics(velocityRef.current, currentTime / 1000, direction);
      const sX = physics.scaleX * initialScale;
      const sY = physics.scaleY * initialScale;

      // Apply GPU-accelerated translate3d transforms for 144Hz+ zero-lag hardware compositing
      if (mainDropRef.current) {
        const mx = posMain.current.x + (isNaN(physics.wobbleX) ? 0 : physics.wobbleX);
        const my = posMain.current.y + (isNaN(physics.wobbleY) ? 0 : physics.wobbleY);
        const combinedRotation = (posMain.current.angle || 0) + (physics.rotation || 0);
        mainDropRef.current.style.transform = `translate3d(${mx.toFixed(2)}px, ${my.toFixed(2)}px, 0px) rotate(${combinedRotation.toFixed(2)}deg) scale(${sX.toFixed(3)}, ${sY.toFixed(3)})`;
        mainDropRef.current.style.opacity = '1';
      }

      if (daughter1Ref.current) {
        daughter1Ref.current.style.transform = `translate3d(${posD1.current.x.toFixed(2)}px, ${posD1.current.y.toFixed(2)}px, 0px) scale(${(sX * 0.75).toFixed(3)}, ${(sY * 0.75).toFixed(3)})`;
      }

      if (daughter2Ref.current) {
        daughter2Ref.current.style.transform = `translate3d(${posD2.current.x.toFixed(2)}px, ${posD2.current.y.toFixed(2)}px, 0px) scale(${(sX * 0.55).toFixed(3)}, ${(sY * 0.55).toFixed(3)})`;
      }

      if (daughter3Ref.current) {
        daughter3Ref.current.style.transform = `translate3d(${posD3.current.x.toFixed(2)}px, ${posD3.current.y.toFixed(2)}px, 0px) scale(${(sX * 0.4).toFixed(3)}, ${(sY * 0.4).toFixed(3)})`;
      }

      if (daughter4Ref.current) {
        daughter4Ref.current.style.transform = `translate3d(${posD4.current.x.toFixed(2)}px, ${posD4.current.y.toFixed(2)}px, 0px) scale(${(sX * 0.28).toFixed(3)}, ${(sY * 0.28).toFixed(3)})`;
      }

      animId = requestAnimationFrame(tick);
    };

    animId = requestAnimationFrame(tick);

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('resize', updateAnchorPos);
    };
  }, []);

  const [viewport, setViewport] = useState({
    w: typeof window !== 'undefined' ? window.innerWidth : 1400,
    h: typeof window !== 'undefined' ? window.innerHeight : 900
  });

  useEffect(() => {
    const handleResize = () => {
      setViewport({ w: window.innerWidth, h: window.innerHeight });
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Handle clicking on dewdrop for playful liquid burst
  const handleDewdropClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!getAudioMuteState()) {
      playSuccessTone();
    }
    triggerRippleAt(posMain.current.x, posMain.current.y, currentMeta.color, 1.4);
  };

  // Generate continuous SVG path string across all waypoints using Catmull-Rom spline sampling (Pixel coordinates for W3C SVG spec compliance)
  const splinePathData = useMemo(() => {
    const samples = 140;
    const points: string[] = [];
    const vw = viewport.w;
    const vh = viewport.h;
    const widthFactor = vw > 1200 ? 1.0 : vw > 768 ? 0.75 : 0.5;

    for (let s = 0; s <= samples; s++) {
      const p = s / samples;
      const res = evaluateSpline(SPLINE_WAYPOINTS, p);
      const mappedXPercent = 50 + (res.x - 50) * widthFactor;
      const horizontalSway = Math.sin(p * Math.PI * 8) * 22;
      const verticalWave = Math.sin(p * Math.PI * 12) * 35;
      const px = (mappedXPercent / 100) * vw + horizontalSway;
      const py = (res.y / 100) * vh + verticalWave;
      points.push(`${px.toFixed(1)} ${py.toFixed(1)}`);
    }
    return `M ${points.join(' L ')}`;
  }, [viewport.w, viewport.h]);

  return (
    /* FIXED OVERLAY CONTAINER PINNED TO VIEWPORT AT BACKGROUND LAYER (z-[1]) */
    <div className="fixed inset-0 pointer-events-none z-[1] w-screen h-screen overflow-hidden">
      {/* GPU Fluid Ripple & Refraction Canvas Shader */}
      <div className="opacity-95">
        <FluidRippleShaderCanvas ripples={ripples} />
      </div>

      {/* Master Full-Canvas SVG Layer */}
      <svg
        ref={svgRef}
        className="absolute inset-0 w-full h-full pointer-events-none dewdrop-svg-canvas"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          {/* SVG Liquid Refraction Shader Filter */}
          <filter id="fluid-refraction-shader" x="-50%" y="-50%" width="200%" height="200%">
            <feTurbulence
              type="fractalNoise"
              baseFrequency="0.03 0.06"
              numOctaves="2"
              result="noise"
            />
            <feDisplacementMap
              in="SourceGraphic"
              in2="noise"
              scale="4"
              xChannelSelector="R"
              yChannelSelector="G"
              result="displaced"
            />
            <feGaussianBlur in="displaced" stdDeviation="0.5" result="blurred" />
            <feSpecularLighting
              in="blurred"
              surfaceScale="5"
              specularConstant="1.5"
              specularExponent="20"
              lightingColor="#ffffff"
              result="specLight"
            >
              <fePointLight x="40" y="20" z="80" />
            </feSpecularLighting>
            <feComposite in="specLight" in2="SourceAlpha" operator="in" result="specular" />
            <feComposite in="displaced" in2="specular" operator="arithmetic" k1="0" k2="1" k3="1" k4="0" />
          </filter>

          {/* Intense Glowing Aura Filter */}
          <filter id="dewdrop-glow" x="-80%" y="-80%" width="260%" height="260%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="8" result="blur1" />
            <feGaussianBlur in="SourceGraphic" stdDeviation="20" result="blur2" />
            <feMerge>
              <feMergeNode in="blur2" />
              <feMergeNode in="blur1" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>

          {/* Dynamic Sinuous Spline Gradient */}
          <linearGradient id="stream-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#00f0ff" stopOpacity="0.75" />
            <stop offset="25%" stopColor="#10b981" stopOpacity="0.85" />
            <stop offset="50%" stopColor="#14b8a6" stopOpacity="0.85" />
            <stop offset="75%" stopColor="#6366f1" stopOpacity="0.80" />
            <stop offset="100%" stopColor="#10b981" stopOpacity="0.95" />
          </linearGradient>

          {/* Dynamic Vivid Radial Gradient for 3D Bio-Leaf Surface */}
          <radialGradient id="leaf-surface-gradient" cx="35%" cy="30%" r="75%">
            <stop offset="0%" stopColor="#ffffff" stopOpacity="1.0" />
            <stop offset="20%" stopColor="#34d399" stopOpacity="0.95" />
            <stop offset="60%" stopColor={currentMeta.color} stopOpacity="0.90" />
            <stop offset="100%" stopColor="#064e3b" stopOpacity="0.85" />
          </radialGradient>

          {/* Leaf Inner Glow Gradient */}
          <linearGradient id="leaf-vein-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#ffffff" stopOpacity="1.0" />
            <stop offset="50%" stopColor="#a7f3d0" stopOpacity="0.9" />
            <stop offset="100%" stopColor={currentMeta.color} stopOpacity="0.7" />
          </linearGradient>

          {/* Daughter Leaf Petal Gradient */}
          <radialGradient id="petal-gradient" cx="40%" cy="35%" r="65%">
            <stop offset="0%" stopColor="#ffffff" stopOpacity="1.0" />
            <stop offset="50%" stopColor="#10b981" stopOpacity="0.9" />
            <stop offset="100%" stopColor={currentMeta.color} stopOpacity="0.6" />
          </radialGradient>
        </defs>

        {/* Sinuous Capillary River Stream path lines removed as requested */}

        {/* TRAILING DAUGHTER BIO-PETAL SPORES (Chained LERP Viscosity Tail) */}
        <g ref={daughter4Ref} className="opacity-60" style={{ willChange: 'transform' }}>
          <path
            d="M 0,-10 C 6,-6 8,0 5,7 C 3,11 0,13 0,13 C 0,13 -3,11 -5,7 C -8,0 -6,-6 0,-10 Z"
            fill="url(#petal-gradient)"
            filter="url(#dewdrop-glow)"
            transform="scale(0.7)"
          />
        </g>
        <g ref={daughter3Ref} className="opacity-75" style={{ willChange: 'transform' }}>
          <path
            d="M 0,-12 C 8,-7 10,0 6,9 C 4,13 0,16 0,16 C 0,16 -4,13 -6,9 C -10,0 -8,-7 0,-12 Z"
            fill="url(#petal-gradient)"
            filter="url(#dewdrop-glow)"
            transform="scale(0.85)"
          />
        </g>
        <g ref={daughter2Ref} className="opacity-85" style={{ willChange: 'transform' }}>
          <path
            d="M 0,-14 C 9,-8 12,0 7,11 C 4,16 0,19 0,19 C 0,19 -4,16 -7,11 C -12,0 -9,-8 0,-14 Z"
            fill="url(#petal-gradient)"
            filter="url(#dewdrop-glow)"
            transform="scale(1.0)"
          />
        </g>
        <g ref={daughter1Ref} className="opacity-95" style={{ willChange: 'transform' }}>
          <path
            d="M 0,-16 C 11,-9 14,0 8,13 C 5,18 0,22 0,22 C 0,22 -5,18 -8,13 C -14,0 -11,-9 0,-16 Z"
            fill="url(#petal-gradient)"
            filter="url(#dewdrop-glow)"
            transform="scale(1.15)"
          />
        </g>

        {/* MAIN 3D MOTION GRAPHICS BIOLUMINESCENT LEAF FRAME */}
        <g
          ref={mainDropRef}
          className="pointer-events-auto cursor-pointer"
          onClick={handleDewdropClick}
          style={{ willChange: 'transform' }}
        >
          {/* Outer Radiant Bioluminescent Aura Corona */}
          <circle
            cx="0"
            cy="0"
            r="52"
            fill={currentMeta.glowColor}
            filter="url(#dewdrop-glow)"
            className="animate-pulse"
          />

          {/* Organic 3D Leaf Outer Silhouette & Shadow */}
          <path
            d="M 0,-52 C 32,-30 40,0 26,34 C 18,54 0,62 0,62 C 0,62 -18,54 -26,34 C -40,0 -32,-30 0,-52 Z"
            fill="rgba(2, 44, 34, 0.45)"
            transform="translate(3, 4)"
          />

          {/* Main Bioluminescent Leaf Body Contour */}
          <path
            d="M 0,-50 C 30,-28 38,0 24,32 C 16,52 0,58 0,58 C 0,58 -16,52 -24,32 C -38,0 -30,-28 0,-50 Z"
            fill="url(#leaf-surface-gradient)"
            filter="url(#fluid-refraction-shader)"
            stroke="#ffffff"
            strokeWidth="2.2"
          />

          {/* Leaf Stem Base */}
          <path
            d="M 0,58 Q -2,68 -7,76"
            fill="none"
            stroke="#10b981"
            strokeWidth="3.5"
            strokeLinecap="round"
            filter="url(#dewdrop-glow)"
          />

          {/* Central Glowing Midrib Vein */}
          <path
            d="M 0,-44 Q 0,10 0,56"
            fill="none"
            stroke="url(#leaf-vein-gradient)"
            strokeWidth="2.8"
            strokeLinecap="round"
          />

          {/* Left Lateral Vascular Veins */}
          <path
            d="M 0,-30 Q -14,-18 -22,-14 M 0,-12 Q -18,0 -24,8 M 0,6 Q -16,18 -18,28 M 0,24 Q -10,34 -12,42"
            fill="none"
            stroke="rgba(255, 255, 255, 0.85)"
            strokeWidth="1.4"
            strokeLinecap="round"
          />

          {/* Right Lateral Vascular Veins */}
          <path
            d="M 0,-30 Q 14,-18 22,-14 M 0,-12 Q 18,0 24,8 M 0,6 Q 16,18 18,28 M 0,24 Q 10,34 12,42"
            fill="none"
            stroke="rgba(255, 255, 255, 0.85)"
            strokeWidth="1.4"
            strokeLinecap="round"
          />

          {/* Specular Dew Drop Glint on Leaf Tip */}
          <circle cx="-7" cy="-14" r="5.5" fill="#ffffff" opacity="0.95" />
          <circle cx="-1" cy="-24" r="3.2" fill="#ffffff" opacity="0.9" />

          {/* Biophilic Core Photon Spark */}
          <circle
            cx="0"
            cy="12"
            r="6.5"
            fill="#ffffff"
            className="animate-ping"
            style={{ animationDuration: '2.0s' }}
          />
        </g>
      </svg>
    </div>
  );
};
