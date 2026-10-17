'use client';

import React, { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

interface ParallaxComponentProps {
  layer1Image?: string;
  layer2Image?: string;
  layer4Image?: string;
  title?: string;
  subtitle?: string;
  className?: string;
}

export function ParallaxComponent({
  layer1Image = 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=1600&auto=format&fit=crop',
  layer2Image = 'https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?q=80&w=1600&auto=format&fit=crop',
  layer4Image = 'https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?q=80&w=1600&auto=format&fit=crop',
  title = 'Agri-SAGE 3D Parallax',
  subtitle = 'Multi-layer timeline scrubbing powered by Lenis & GSAP ScrollTrigger',
  className = ''
}: ParallaxComponentProps) {
  const parallaxRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    gsap.registerPlugin(ScrollTrigger);

    const triggerElement = parallaxRef.current?.querySelector('[data-parallax-layers]');

    if (triggerElement) {
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: triggerElement,
          start: '0% 0%',
          end: '100% 0%',
          scrub: 0
        }
      });

      const layers = [
        { layer: '1', yPercent: 70 },
        { layer: '2', yPercent: 55 },
        { layer: '3', yPercent: 40 },
        { layer: '4', yPercent: 10 }
      ];

      layers.forEach((layerObj, idx) => {
        tl.to(
          triggerElement.querySelectorAll(`[data-parallax-layer="${layerObj.layer}"]`),
          {
            yPercent: layerObj.yPercent,
            ease: 'none'
          },
          idx === 0 ? undefined : '<'
        );
      });
    }

    return () => {
      ScrollTrigger.getAll().forEach((st) => {
        if (st.vars.trigger === triggerElement) {
          st.kill();
        }
      });
      if (triggerElement) {
        gsap.killTweensOf(triggerElement);
      }
    };
  }, []);

  return (
    <div className={`parallax overflow-hidden relative w-full ${className}`} ref={parallaxRef}>
      <section className="parallax__header relative w-full h-[90vh] md:h-[110vh] overflow-hidden">
        <div className="parallax__visuals relative w-full h-full">
          <div className="parallax__black-line-overflow pointer-events-none" />
          <div data-parallax-layers className="parallax__layers relative w-full h-full">
            {/* Layer 1: Deep Sky & Soil Background (yPercent: 70) */}
            <img
              src={layer1Image}
              loading="eager"
              width="1600"
              height="900"
              data-parallax-layer="1"
              alt="Space Farmland Sky"
              className="parallax__layer-img absolute inset-0 w-full h-full object-cover filter brightness-[0.85] contrast-105"
            />

            {/* Layer 2: Midground Canopy Grid Mesh (yPercent: 55) */}
            <img
              src={layer2Image}
              loading="eager"
              width="1600"
              height="900"
              data-parallax-layer="2"
              alt="Agri Canopy Mesh"
              className="parallax__layer-img absolute inset-0 w-full h-full object-cover mix-blend-screen opacity-65 filter contrast-125"
            />

            {/* Layer 3: Kinetic Headline Plane (yPercent: 40) */}
            <div
              data-parallax-layer="3"
              className="parallax__layer-title absolute inset-0 flex flex-col items-center justify-center pointer-events-none z-20 px-4 text-center"
            >
              <h2 className="parallax__title text-4xl sm:text-6xl md:text-7xl lg:text-8xl font-black text-white drop-shadow-2xl tracking-tight leading-tight">
                {title}
              </h2>
              {subtitle && (
                <p className="mt-3 text-sm sm:text-lg text-emerald-300 font-mono font-semibold drop-shadow-lg max-w-xl">
                  {subtitle}
                </p>
              )}
            </div>

            {/* Layer 4: Foreground Micro Leaf (yPercent: 10) */}
            <img
              src={layer4Image}
              loading="eager"
              width="1600"
              height="900"
              data-parallax-layer="4"
              alt="Foreground Bio Leaf"
              className="parallax__layer-img absolute inset-0 w-full h-full object-cover mix-blend-screen opacity-85 pointer-events-none"
            />
          </div>

          {/* Smooth Gradient Fade out into content section */}
          <div className="parallax__fade absolute bottom-0 inset-x-0 h-36 bg-gradient-to-t from-slate-950 via-slate-950/80 to-transparent pointer-events-none z-30" />
        </div>
      </section>
    </div>
  );
}

export default ParallaxComponent;
