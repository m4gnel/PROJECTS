import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import SplitType from 'split-type';

gsap.registerPlugin(ScrollTrigger);

interface UseSplitTypographyOptions {
  selector?: string; // Optional CSS selector to target within container
  types?: ('lines' | 'words' | 'chars')[];
  stagger?: number;
  duration?: number;
  triggerStart?: string;
  delay?: number;
  toggleActions?: string;
}

/**
 * Custom hook for accessible kinetic typography using SplitType and GSAP ScrollTrigger.
 * Implements masked line reveals with overflow: hidden containers and preserves WCAG accessibility.
 */
export function useSplitTypography<T extends HTMLElement = HTMLDivElement>(
  options: UseSplitTypographyOptions = {}
) {
  const containerRef = useRef<T | null>(null);

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    // Honor prefers-reduced-motion
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      return;
    }

    const splitInstances: SplitType[] = [];
    let animations: gsap.core.Tween[] = [];

    const initSplit = () => {
      const targets = options.selector
        ? (Array.from(el.querySelectorAll(options.selector)) as HTMLElement[])
        : [el];

      targets.forEach((target) => {
        // WCAG Screen Reader preservation
        const originalText = target.textContent || '';
        target.setAttribute('aria-label', originalText);

        const splitTypes = options.types || ['lines', 'words'];
        const split = new SplitType(target, {
          types: splitTypes,
          tagName: 'span',
          lineClass: 'split-line',
          wordClass: 'split-word'
        });

        // Hide visual split tokens from screen readers
        target.querySelectorAll('.split-line, .split-word').forEach((node) => {
          node.setAttribute('aria-hidden', 'true');
        });

        // Wrap each line in an overflow-hidden block mask
        if (split.lines) {
          split.lines.forEach((line) => {
            const wrapper = document.createElement('div');
            wrapper.className = 'line-mask overflow-hidden block w-full';
            line.parentNode?.insertBefore(wrapper, line);
            wrapper.appendChild(line);
          });
        }

        // Set initial state and animate with GSAP ScrollTrigger
        const animTargets = split.words && split.words.length > 0 ? split.words : split.lines;
        if (animTargets && animTargets.length > 0) {
          gsap.set(animTargets, {
            yPercent: 120,
            opacity: 0
          });

          const tween = gsap.to(animTargets, {
            yPercent: 0,
            opacity: 1,
            duration: options.duration || 1.1,
            ease: 'power4.out',
            stagger: options.stagger ?? 0.035,
            delay: options.delay ?? 0.05,
            scrollTrigger: {
              trigger: target.closest('section') || target,
              start: options.triggerStart || 'top 85%',
              toggleActions: options.toggleActions || 'play none none reverse'
            }
          });

          animations.push(tween);
        }

        splitInstances.push(split);
      });

      // Refresh ScrollTrigger to calculate exact initial bounds
      ScrollTrigger.refresh();
    };

    document.fonts.ready.then(() => {
      initSplit();
    });

    // Handle debounced window resize
    let resizeTimer: ReturnType<typeof setTimeout>;
    const handleResize = () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        splitInstances.forEach((s) => s.split({ types: options.types || ['lines', 'words'] }));
        ScrollTrigger.refresh();
      }, 250);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      animations.forEach((a) => {
        a.scrollTrigger?.kill();
        a.kill();
      });
      splitInstances.forEach((s) => s.revert());
    };
  }, [options.selector, options.types, options.stagger, options.duration, options.triggerStart, options.delay]);

  return containerRef;
}
