import { useEffect, useRef, useCallback } from 'react';

/**
 * useParallaxLayers – High-performance multi-layer parallax engine.
 * 
 * Decorative elements tagged with `data-parallax-speed` move at different
 * scroll rates relative to the viewport, creating Apple-style depth separation.
 * 
 * Speed values:
 *  - 0   = fixed (no movement relative to page)
 *  - 0.5 = moves at half the scroll speed (background feel)
 *  - 1   = normal scroll speed (content layer)
 *  - 1.5 = moves 50% faster (foreground layer – creates "flying past" effect)
 *  - -0.3 = moves opposite direction (contra-parallax, very premium)
 * 
 * Uses requestAnimationFrame with passive scroll listener for 60fps.
 */
export const useParallaxLayers = () => {
  const rafId = useRef<number>(0);
  const ticking = useRef(false);

  // Cached layout data to eliminate forced synchronous reflows inside RAF
  const cachedDataRef = useRef<{
    el: HTMLElement;
    speed: number;
    direction: string;
    rotate: number;
    rotateX: number;
    rotateY: number;
    baseZ: number;
    baseScale: number;
    top: number;
    height: number;
  }[]>([]);

  // Update cached top offsets on resize or scroll height changes
  const updateLayoutCache = useCallback(() => {
    const elements = document.querySelectorAll<HTMLElement>('[data-parallax-speed]');
    const scrollY = window.scrollY;

    cachedDataRef.current = Array.from(elements).map((el) => {
      const rect = el.getBoundingClientRect();
      return {
        el,
        speed: parseFloat(el.dataset.parallaxSpeed || '0'),
        direction: el.dataset.parallaxDirection || 'y',
        rotate: parseFloat(el.dataset.parallaxRotate || '0'),
        rotateX: parseFloat(el.dataset.parallaxRotateX || '0'),
        rotateY: parseFloat(el.dataset.parallaxRotateY || '0'),
        baseZ: parseFloat(el.dataset.parallaxZ || '0'),
        baseScale: parseFloat(el.dataset.parallaxScale || '1'),
        top: rect.top + scrollY,
        height: rect.height
      };
    });
  }, []);

  const applyParallax = useCallback(() => {
    const scrollY = window.scrollY;
    const vh = window.innerHeight;
    const viewportCenter = vh / 2;

    const items = cachedDataRef.current;
    const len = items.length;

    for (let i = 0; i < len; i++) {
      const item = items[i];
      const elTopInViewport = item.top - scrollY;

      // Only transform elements within or near the active viewport window
      if (elTopInViewport < vh + 300 && elTopInViewport + item.height > -300) {
        const elementCenter = elTopInViewport + item.height / 2;
        const distanceFromCenter = elementCenter - viewportCenter;
        const normalizedDistance = distanceFromCenter / (vh / 2); // -1 to +1

        const yOffset = distanceFromCenter * (item.speed - 1) * 0.35;
        const xOffset = item.direction === 'x' || item.direction === 'both'
          ? distanceFromCenter * item.speed * 0.12
          : 0;

        const zOffset = item.baseZ + normalizedDistance * (item.speed > 1 ? 30 : -20);
        const scaleFactor = Math.max(0.75, Math.min(1.25, item.baseScale + (1 - Math.abs(normalizedDistance)) * 0.04));

        const rotateOffsetZ = item.rotate !== 0 ? (scrollY / 1000) * item.rotate : 0;
        const rotateOffsetX = item.rotateX !== 0 ? normalizedDistance * item.rotateX : 0;
        const rotateOffsetY = item.rotateY !== 0 ? normalizedDistance * item.rotateY : 0;

        item.el.style.transform = `translate3d(${xOffset.toFixed(1)}px, ${yOffset.toFixed(1)}px, ${zOffset.toFixed(1)}px) rotateX(${rotateOffsetX.toFixed(2)}deg) rotateY(${rotateOffsetY.toFixed(2)}deg) rotateZ(${rotateOffsetZ.toFixed(2)}deg) scale3d(${scaleFactor.toFixed(3)}, ${scaleFactor.toFixed(3)}, 1)`;
      }
    }

    ticking.current = false;
  }, []);

  const handleScroll = useCallback(() => {
    if (!ticking.current) {
      ticking.current = true;
      rafId.current = requestAnimationFrame(applyParallax);
    }
  }, [applyParallax]);

  useEffect(() => {
    updateLayoutCache();
    window.addEventListener('scroll', handleScroll, { passive: true });
    window.addEventListener('resize', updateLayoutCache);

    // Initial positioning
    applyParallax();

    return () => {
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('resize', updateLayoutCache);
      cancelAnimationFrame(rafId.current);
    };
  }, [handleScroll, applyParallax, updateLayoutCache]);
};
