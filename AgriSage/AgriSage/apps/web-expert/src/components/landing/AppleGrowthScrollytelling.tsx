import React, { useEffect, useRef, useState, useMemo, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sprout } from 'lucide-react';
import { getPublicUrl } from '@/lib/utils';

interface AppleGrowthScrollytellingProps {
  onEnterPlatform?: () => void;
  onEnterAuth?: () => void;
}

let globalScrollytellingPreloaded = false;

export const AppleGrowthScrollytelling: React.FC<AppleGrowthScrollytellingProps> = ({
  onEnterPlatform,
  onEnterAuth,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [currentFrame, setCurrentFrame] = useState(0);
  const [scrollP, setScrollP] = useState(0); // 0 to 1
  const [isPreloaded, setIsPreloaded] = useState(globalScrollytellingPreloaded);
  const [preloadCount, setPreloadCount] = useState(globalScrollytellingPreloaded ? 441 : 0);

  const totalFrames = 441;
  const targetFrameRef = useRef(0);
  const animatedFrameRef = useRef(0);

  // Generate 441 frame URLs formatted as '0001.jpg', '0002.jpg', ..., '0441.jpg'
  const frameUrls = useMemo(() => {
    return Array.from({ length: totalFrames }, (_, i) => {
      const num = String(i + 1).padStart(4, '0');
      return getPublicUrl(`/images/Agri-Sage-Section-2-animation/${num}.jpg`);
    });
  }, [totalFrames]);

  const imagesRef = useRef<HTMLImageElement[]>([]);

  // Resize canvas dimensions smoothly on window resize without forced layout thrashing inside RAF
  const updateCanvasDimensions = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const parent = canvas.parentElement;
    if (!parent) return;

    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const targetW = Math.round(parent.clientWidth * dpr);
    const targetH = Math.round(parent.clientHeight * dpr);

    if (canvas.width !== targetW || canvas.height !== targetH) {
      canvas.width = targetW;
      canvas.height = targetH;
    }
  }, []);

  const lastDrawnFrameRef = useRef<number>(-1);
  const lastScrollPRef = useRef<number>(-1);

  // High-performance Canvas draw with aspect cover & #050505 background fill
  const drawCanvasFrame = useCallback((frameIdx: number, imgsList?: HTMLImageElement[]) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d', { alpha: false });
    if (!ctx) return;

    const imgs = imgsList || imagesRef.current;
    const img = imgs[frameIdx];

    // Clear with strict #050505 color for perfect void blending
    ctx.fillStyle = '#050505';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    if (!img || !img.complete || img.naturalWidth === 0) return;

    // Aspect cover positioning logic
    const imgRatio = img.naturalWidth / img.naturalHeight;
    const canvasRatio = canvas.width / canvas.height;

    let sx = 0, sy = 0, sw = img.naturalWidth, sh = img.naturalHeight;

    if (imgRatio > canvasRatio) {
      sw = img.naturalHeight * canvasRatio;
      sx = (img.naturalWidth - sw) / 2;
    } else {
      sh = img.naturalWidth / canvasRatio;
      sy = (img.naturalHeight - sh) / 2;
    }

    ctx.drawImage(img, sx, sy, sw, sh, 0, 0, canvas.width, canvas.height);
  }, []);

  // Preload frames in parallel with instant safety fallback
  useEffect(() => {
    let canceled = false;
    const images: HTMLImageElement[] = new Array(totalFrames);
    let loaded = 0;

    const markPreloaded = () => {
      if (!canceled) {
        globalScrollytellingPreloaded = true;
        setIsPreloaded(true);
      }
    };

    // Safety timeout: automatically dismiss preloader after max 1.0s under any condition
    const safetyTimer = setTimeout(() => {
      markPreloaded();
    }, 1000);

    frameUrls.forEach((url, i) => {
      const img = new Image();
      img.src = url;
      img.onload = () => {
        if (canceled) return;
        loaded++;
        const clampedLoaded = Math.min(totalFrames, loaded);
        setPreloadCount(clampedLoaded);
        if (clampedLoaded === 1 && canvasRef.current) {
          drawCanvasFrame(0, images);
        }
        if (clampedLoaded >= 10) {
          markPreloaded();
        }
      };
      img.onerror = () => {
        if (canceled) return;
        loaded++;
        const clampedLoaded = Math.min(totalFrames, loaded);
        setPreloadCount(clampedLoaded);
        if (clampedLoaded >= 10) {
          markPreloaded();
        }
      };
      images[i] = img;
    });

    imagesRef.current = images;

    return () => {
      canceled = true;
      clearTimeout(safetyTimer);
      images.forEach((img) => {
        if (img) {
          img.onload = null;
          img.onerror = null;
        }
      });
    };
  }, [frameUrls, totalFrames, drawCanvasFrame]);

  // Smooth spring-dampened frame interpolation loop optimized for 144Hz high refresh rate
  useEffect(() => {
    let animId = 0;
    let isVisible = true;

    const lerpFrameLoop = () => {
      if (!isVisible) {
        animId = 0;
        return;
      }
      const target = targetFrameRef.current;
      const current = animatedFrameRef.current;

      const diff = target - current;
      if (Math.abs(diff) > 0.01) {
        const absDiff = Math.abs(diff);
        // Adaptive lerp factor: scales dynamically so fast scroll flings track target frame with ZERO lag
        const lerpFactor = absDiff > 20 ? 0.65 : absDiff > 6 ? 0.40 : 0.25;
        animatedFrameRef.current = current + diff * lerpFactor;
        const roundedIdx = Math.min(totalFrames - 1, Math.max(0, Math.round(animatedFrameRef.current)));
        if (roundedIdx !== lastDrawnFrameRef.current) {
          lastDrawnFrameRef.current = roundedIdx;
          setCurrentFrame(roundedIdx);
          drawCanvasFrame(roundedIdx);
        }
      }
      animId = requestAnimationFrame(lerpFrameLoop);
    };

    const container = containerRef.current;
    const observer = new IntersectionObserver(
      ([entry]) => {
        isVisible = entry.isIntersecting;
        if (isVisible && animId === 0) {
          lerpFrameLoop();
        }
      },
      { threshold: 0.01 }
    );

    if (container) {
      observer.observe(container);
    }

    animId = requestAnimationFrame(lerpFrameLoop);

    let scrollRafId: number | null = null;
    const handleScroll = () => {
      if (!isVisible) return;
      if (scrollRafId !== null) return;

      scrollRafId = requestAnimationFrame(() => {
        scrollRafId = null;
        if (!container) return;

        const rect = container.getBoundingClientRect();
        const vh = window.innerHeight;
        const totalScrollable = rect.height - vh;

        if (totalScrollable <= 0) return;

        const currentScroll = -rect.top;
        const progress = Math.min(Math.max(currentScroll / totalScrollable, 0), 1);
        
        // Quantize setScrollP updates to prevent micro React re-renders on sub-pixel scroll movements
        if (Math.abs(progress - lastScrollPRef.current) > 0.002) {
          lastScrollPRef.current = progress;
          setScrollP(progress);
        }

        const frameIdx = Math.min(totalFrames - 1, Math.floor(progress * totalFrames));
        targetFrameRef.current = frameIdx;
      });
    };

    updateCanvasDimensions();
    const handleResize = () => {
      updateCanvasDimensions();
      handleScroll();
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    window.addEventListener('resize', handleResize, { passive: true });
    handleScroll();

    return () => {
      observer.disconnect();
      if (animId) cancelAnimationFrame(animId);
      if (scrollRafId !== null) cancelAnimationFrame(scrollRafId);
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('resize', handleResize);
    };
  }, [totalFrames, drawCanvasFrame, updateCanvasDimensions]);

  // Determine active story beat based on scroll percentage
  const activeBeat = useMemo(() => {
    if (scrollP < 0.20) return 1; // Beat A: 0-20%
    if (scrollP < 0.45) return 2; // Beat B: 25-45%
    if (scrollP < 0.70) return 3; // Beat C: 50-70%
    if (scrollP < 0.95) return 4; // Beat D: 75-95%
    return 5;
  }, [scrollP]);



  return (
    <div
      ref={containerRef}
      className="relative z-10 w-full bg-[#050505] text-white selection:bg-emerald-500 selection:text-white"
      style={{ height: '400vh' }}
    >
      {/* Preloading Overlay */}
      <AnimatePresence>
        {!isPreloaded && (
          <motion.div
            initial={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.5, ease: 'easeOut' }}
            className="absolute inset-0 z-40 bg-[#050505] flex flex-col items-center justify-center p-6 text-center pointer-events-none"
          >
            <div className="w-16 h-16 mb-6 relative flex items-center justify-center">
              <div className="absolute inset-0 rounded-full border-2 border-emerald-500/20 border-t-emerald-400 animate-spin" />
              <Sprout size={24} className="text-emerald-400 animate-pulse" />
            </div>
            <h4 className="text-xs font-mono font-bold tracking-widest text-emerald-400 uppercase mb-2">
              Initializing Scrollytelling Sequence
            </h4>
            <div className="w-64 h-1 bg-white/10 rounded-full overflow-hidden mb-3">
              <div
                className="h-full bg-emerald-400 transition-all duration-150"
                style={{ width: `${Math.min(100, Math.round((Math.min(totalFrames, preloadCount) / totalFrames) * 100))}%` }}
              />
            </div>
            <span className="text-[11px] font-mono text-white/50">
              {Math.min(100, Math.round((Math.min(totalFrames, preloadCount) / totalFrames) * 100))}% Loaded
            </span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Sticky Full-Screen Pinned Viewport */}
      <div className="sticky top-0 h-screen w-full overflow-hidden flex flex-col justify-between items-center bg-[#050505]">
        {/* Seamless Radial Ambient Glow in Background */}
        <div className="absolute inset-0 pointer-events-none z-0 opacity-40 bg-[radial-gradient(ellipse_at_center,_#050815_0%,_#050505_75%)]" />

        {/* Full-Screen Canvas Engine */}
        <div className="absolute inset-0 w-full h-full z-10 flex items-center justify-center">
          <canvas
            ref={canvasRef}
            className="w-full h-full object-cover filter brightness-[0.96] contrast-[1.04]"
          />
        </div>



        {/* Dynamic Scrollytelling Beats */}
        <div className="relative z-30 w-full max-w-7xl mx-auto px-6 md:px-12 flex-1 flex items-center pointer-events-none">
          <AnimatePresence mode="wait">
            {/* Beat A — 0–20% Scroll (Centered Hero) */}
            {activeBeat === 1 && (
              <motion.div
                key="beat-a"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
                className="w-full max-w-6xl mx-auto text-center space-y-6"
              >

                <h2 className="text-3xl sm:text-5xl md:text-6xl lg:text-7xl font-black tracking-tighter text-white drop-shadow-2xl leading-[1.05] uppercase">
                  <span className="inline-block whitespace-nowrap">FROM A SINGLE SEED</span> <br />
                  <span className="inline-block whitespace-nowrap bg-gradient-to-r from-white via-emerald-300 to-teal-400 bg-clip-text text-transparent">
                    TO A SMARTER TOMORROW.
                  </span>
                </h2>

              </motion.div>
            )}

            {/* Beat B — 25–45% Scroll (Left Aligned Feature) */}
            {activeBeat === 2 && (
              <motion.div
                key="beat-b"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
                className="w-full max-w-xl text-left space-y-4"
              >
                <h3 className="text-3xl sm:text-5xl font-black text-white leading-tight tracking-tight drop-shadow-[0_4px_16px_rgba(0,0,0,0.95)]">
                  Precision-Engineered <br /> for Cellular Vitality.
                </h3>
                <p className="text-sm sm:text-base text-white leading-relaxed font-medium drop-shadow-[0_2px_10px_rgba(0,0,0,0.95)]">
                  Custom DSSAT biophysical models, sealed acoustic transpiration chambers, and real-time stomatal conductance analysis deliver studio-grade agricultural insight.
                </p>
              </motion.div>
            )}

            {/* Beat C — 50–70% Scroll (Right Aligned Feature) */}
            {activeBeat === 3 && (
              <motion.div
                key="beat-c"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
                className="w-full max-w-lg ml-auto text-left space-y-4"
              >
                <h3 className="text-3xl sm:text-5xl font-black text-white leading-tight tracking-tight drop-shadow-[0_4px_16px_rgba(0,0,0,0.95)]">
                  Adaptive Multispectral <br /> Intelligence, Redefined.
                </h3>
                <p className="text-sm sm:text-base text-white leading-relaxed font-medium drop-shadow-[0_2px_10px_rgba(0,0,0,0.95)]">
                  Multi-spectral satellite array listens in every direction. Real-time thermal stress analysis adapts to your environment—drought, pests, and yield anomalies fade away.
                </p>
              </motion.div>
            )}

            {/* Beat D — 75–95% Scroll (Centered CTA) */}
            {activeBeat >= 4 && (
              <motion.div
                key="beat-d"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
                className="w-full max-w-3xl mx-auto text-center space-y-6 pointer-events-auto"
              >
                <h2 className="text-4xl sm:text-6xl font-black tracking-tight text-white drop-shadow-[0_4px_16px_rgba(0,0,0,0.95)]">
                  Hear Everything. <br />
                  <span className="text-emerald-400 drop-shadow-[0_4px_16px_rgba(0,0,0,0.95)]">Protect Every Harvest.</span>
                </h2>
                <p className="text-base text-white/90 max-w-xl mx-auto font-medium drop-shadow-[0_2px_10px_rgba(0,0,0,0.95)]">
                  AgriSage Biophysical Edition. Designed for focus, crafted for smallholders and agronomists worldwide.
                </p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Scroll to Explore Indicator (Fades out by 10% scroll) */}
        <AnimatePresence>
          {scrollP < 0.08 && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 10 }}
              className="relative z-30 mb-4 flex flex-col items-center gap-2 text-white/60 pointer-events-none"
            >
              <span className="text-[10px] font-mono uppercase tracking-widest text-emerald-400 font-bold">
                Scroll to Explore Sequence
              </span>
              <div className="w-5 h-8 rounded-full border-2 border-white/30 flex items-start justify-center p-1">
                <span className="w-1 h-2 rounded-full bg-emerald-400 animate-bounce" />
              </div>
            </motion.div>
          )}
        </AnimatePresence>


      </div>
    </div>
  );
};
