import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

/**
 * useScrollytelling — Master GSAP ScrollTrigger Orchestrator
 *
 * GPU-only animations (transform + opacity) for 120-144fps:
 * ─ Batch element reveals (.reveal-up / .reveal-left / .reveal-right / .reveal-scale / .reveal-blur / .reveal-rotate)
 * ─ Hero pinned zoom-through (scrubbed scale + blur)
 * ─ Chapter ambient glow morphing (per-chapter radial gradient overlay)
 * ─ Scroll-velocity reactive element skew (.velocity-reactive)
 * ─ Animated number counters (data-counter / data-counter-suffix)
 * ─ 3D depth parallax layers (data-depth="0..1")
 * ─ clipPath text wipe reveals (.text-wipe)
 * ─ Staggered card grid reveals (.card-stagger-grid)
 *
 * Single gsap.context() ensures bulletproof cleanup on unmount.
 */
export function useScrollytelling(containerRef: React.RefObject<HTMLDivElement | null>) {
  const ctxRef = useRef<gsap.Context | null>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const rafId = requestAnimationFrame(() => {
      ctxRef.current = gsap.context(() => {

        /* ═══════════════════════════════════════════════════════════════
           1. BATCH ELEMENT REVEALS
           Elements with .reveal-* classes start hidden and cascade in
           when they enter the viewport. Reversed on scroll-back.
           ═══════════════════════════════════════════════════════════════ */
        const revealConfigs: { sel: string; from: gsap.TweenVars }[] = [
          { sel: '.reveal-up',     from: { y: 70, opacity: 0 } },
          { sel: '.reveal-down',   from: { y: -50, opacity: 0 } },
          { sel: '.reveal-left',   from: { x: -90, opacity: 0 } },
          { sel: '.reveal-right',  from: { x: 90, opacity: 0 } },
          { sel: '.reveal-scale',  from: { scale: 0.72, opacity: 0 } },
          { sel: '.reveal-blur',   from: { opacity: 0, y: 30, filter: 'blur(16px)' } },
          { sel: '.reveal-rotate', from: { rotation: -6, y: 50, opacity: 0, transformOrigin: 'left bottom' } },
        ];

        revealConfigs.forEach(({ sel, from }) => {
          const els = gsap.utils.toArray<HTMLElement>(sel, container);
          if (!els.length) return;

          gsap.set(els, from);

          ScrollTrigger.batch(els, {
            onEnter: (batch) => gsap.to(batch, {
              y: 0, x: 0, scale: 1, rotation: 0, opacity: 1,
              filter: 'blur(0px)',
              stagger: { each: 0.05, from: 'start' },
              duration: 0.75,
              ease: 'power3.out',
              overwrite: 'auto',
            }),
            once: true,
            start: 'top 92%',
          });
        });

        /* ═══════════════════════════════════════════════════════════════
           2. HERO PINNED ZOOM-THROUGH
           As the user scrolls past the hero, content scales up and
           blurs softly — a "diving through the atmosphere" effect.
           ═══════════════════════════════════════════════════════════════ */
        const heroSection = container.querySelector<HTMLElement>('[data-chapter="1"]');
        const heroInner = container.querySelector<HTMLElement>('.hero-zoom-target');

        if (heroSection && heroInner) {
          gsap.timeline({
            scrollTrigger: {
              trigger: heroSection,
              start: 'top top',
              end: '+=55%',
              scrub: 1.5,
            },
          })
          .to(heroInner, {
            scale: 1.14,
            y: -40,
            opacity: 0.25,
            filter: 'blur(3px)',
            ease: 'none',
          });
        }

        /* ═══════════════════════════════════════════════════════════════
           3. CHAPTER AMBIENT GLOW MORPHING
           A fixed overlay subtly shifts its radial gradient colour as
           the user scrolls between chapters — biophilic colour coding.
           ═══════════════════════════════════════════════════════════════ */
        const glowOverlay = container.querySelector<HTMLElement>('.chapter-ambient-glow');
        if (glowOverlay) {
          const glowMap: Record<string, { bg: string; shadow: string }> = {
            '1':  { bg: 'rgba(16,185,129,0.06)',  shadow: '0 0 220px 90px rgba(16,185,129,0.10)' },
            '2':  { bg: 'rgba(245,158,11,0.05)',   shadow: '0 0 220px 90px rgba(245,158,11,0.08)' },
            '3':  { bg: 'rgba(16,185,129,0.05)',   shadow: '0 0 220px 90px rgba(16,185,129,0.08)' },
            '4':  { bg: 'rgba(168,85,247,0.05)',   shadow: '0 0 220px 90px rgba(168,85,247,0.08)' },
            '5':  { bg: 'rgba(20,184,166,0.05)',   shadow: '0 0 220px 90px rgba(20,184,166,0.08)' },
            '6':  { bg: 'rgba(59,130,246,0.05)',   shadow: '0 0 220px 90px rgba(59,130,246,0.08)' },
            '7':  { bg: 'rgba(34,197,94,0.05)',    shadow: '0 0 220px 90px rgba(34,197,94,0.08)' },
            '8':  { bg: 'rgba(99,102,241,0.05)',   shadow: '0 0 220px 90px rgba(99,102,241,0.08)' },
            '9':  { bg: 'rgba(234,179,8,0.04)',    shadow: '0 0 220px 90px rgba(234,179,8,0.07)' },
            '10': { bg: 'rgba(14,165,233,0.05)',   shadow: '0 0 220px 90px rgba(14,165,233,0.08)' },
            '11': { bg: 'rgba(16,185,129,0.05)',   shadow: '0 0 220px 90px rgba(16,185,129,0.08)' },
            '12': { bg: 'rgba(16,185,129,0.08)',   shadow: '0 0 260px 110px rgba(16,185,129,0.12)' },
          };

          container.querySelectorAll<HTMLElement>('section[data-chapter]').forEach((sec) => {
            const ch = sec.dataset.chapter || '1';
            const g = glowMap[ch] || glowMap['1'];

            ScrollTrigger.create({
              trigger: sec,
              start: 'top 55%',
              end: 'bottom 45%',
              onEnter:     () => gsap.to(glowOverlay, { backgroundColor: g.bg, boxShadow: g.shadow, duration: 1.4, ease: 'power2.inOut' }),
              onEnterBack: () => gsap.to(glowOverlay, { backgroundColor: g.bg, boxShadow: g.shadow, duration: 1.4, ease: 'power2.inOut' }),
            });
          });
        }

        /* ═══════════════════════════════════════════════════════════════
           4. SCROLL VELOCITY REACTIVE
           Elements with .velocity-reactive subtly skew in the direction
           of scroll, creating an organic "wind" feel.
           ═══════════════════════════════════════════════════════════════ */
        const velEls = gsap.utils.toArray<HTMLElement>('.velocity-reactive', container);
        if (velEls.length) {
          let lastScroll = 0;
          let lastSkew = 0;
          const setSkews = velEls.map((el) => gsap.quickTo(el, 'skewY', { duration: 0.3, ease: 'power2.out' }));

          ScrollTrigger.create({
            trigger: container,
            start: 'top top',
            end: 'bottom bottom',
            onUpdate: (self) => {
              const curr = self.scroll();
              const vel = gsap.utils.clamp(-1, 1, (curr - lastScroll) * 0.0008);
              lastScroll = curr;
              const skewVal = vel * 0.6;
              if (Math.abs(skewVal - lastSkew) > 0.02 || (skewVal === 0 && lastSkew !== 0)) {
                lastSkew = skewVal;
                setSkews.forEach((setter) => setter(skewVal));
              }
            },
          });
        }

        /* ═══════════════════════════════════════════════════════════════
           5. ANIMATED NUMBER COUNTERS
           Elements with data-counter="100" count from 0 to 100 when
           they scroll into view. Supports data-counter-suffix="%",
           data-counter-prefix="$", data-counter-decimals="1".
           ═══════════════════════════════════════════════════════════════ */
        container.querySelectorAll<HTMLElement>('[data-counter]').forEach((el) => {
          const target   = parseFloat(el.dataset.counter || '0');
          const suffix   = el.dataset.counterSuffix || '';
          const prefix   = el.dataset.counterPrefix || '';
          const decimals = parseInt(el.dataset.counterDecimals || '0', 10);
          const obj      = { val: 0 };

          ScrollTrigger.create({
            trigger: el,
            start: 'top 88%',
            once: true,
            onEnter: () => {
              gsap.to(obj, {
                val: target,
                duration: 2.4,
                ease: 'power2.out',
                onUpdate: () => {
                  el.textContent = prefix + obj.val.toFixed(decimals) + suffix;
                },
              });
            },
          });
        });

        /* ═══════════════════════════════════════════════════════════════
           6. 3D DEPTH PARALLAX
           Elements with data-depth="0..1" translate vertically at
           different rates, creating true depth separation.
           Lower depth = further back = moves more.
           ═══════════════════════════════════════════════════════════════ */
        gsap.utils.toArray<HTMLElement>('[data-depth]', container).forEach((el) => {
          const depth = parseFloat(el.dataset.depth || '0.5');
          const speed = (1 - depth) * 45;

          gsap.to(el, {
            y: speed,
            ease: 'none',
            scrollTrigger: {
              trigger: el.closest('section') || el,
              start: 'top bottom',
              end: 'bottom top',
              scrub: 0.6,
            },
          });
        });

        /* ═══════════════════════════════════════════════════════════════
           7. TEXT CLIP WIPE REVEALS
           Elements with .text-wipe reveal via animated clipPath,
           creating a curtain-pull effect.
           ═══════════════════════════════════════════════════════════════ */
        gsap.utils.toArray<HTMLElement>('.text-wipe', container).forEach((el) => {
          gsap.fromTo(el,
            { clipPath: 'inset(0 100% 0 0)' },
            {
              clipPath: 'inset(0 0% 0 0)',
              duration: 1.4,
              ease: 'power4.inOut',
              scrollTrigger: {
                trigger: el,
                start: 'top 85%',
                toggleActions: 'play none none reverse',
              },
            }
          );
        });

        /* ═══════════════════════════════════════════════════════════════
           8. STAGGERED CARD GRID REVEALS
           Container with .card-stagger-grid — its direct children
           cascade in with a spring-back ease.
           ═══════════════════════════════════════════════════════════════ */
        container.querySelectorAll<HTMLElement>('.card-stagger-grid').forEach((grid) => {
          const cards = gsap.utils.toArray<HTMLElement>(':scope > *', grid);
          if (!cards.length) return;

          gsap.set(cards, { y: 50, opacity: 0, scale: 0.92 });

          ScrollTrigger.create({
            trigger: grid,
            start: 'top 85%',
            onEnter: () => {
              gsap.to(cards, {
                y: 0, opacity: 1, scale: 1,
                stagger: { each: 0.1, from: 'start' },
                duration: 0.7,
                ease: 'back.out(1.4)',
              });
            },
            onLeaveBack: () => {
              gsap.to(cards, {
                y: 50, opacity: 0, scale: 0.92,
                stagger: { each: 0.05 },
                duration: 0.4,
              });
            },
          });
        });

        /* ═══════════════════════════════════════════════════════════════
           FINAL: Recalculate all triggers after setup
           ═══════════════════════════════════════════════════════════════ */
        ScrollTrigger.refresh();

      }, container); // gsap.context scope
    }); // requestAnimationFrame

    return () => {
      cancelAnimationFrame(rafId);
      ctxRef.current?.revert();
      ctxRef.current = null;
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps
}
