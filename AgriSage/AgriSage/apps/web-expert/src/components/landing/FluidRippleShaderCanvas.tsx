import React, { useEffect, useRef } from 'react';

export interface RippleEvent {
  x: number;
  y: number;
  color: string;
  maxRadius: number;
  speed: number;
  intensity: number;
}

interface FluidRippleShaderCanvasProps {
  ripples: RippleEvent[];
  onRippleComplete?: () => void;
}

interface ActiveRipple {
  x: number;
  y: number;
  color: string;
  radius: number;
  maxRadius: number;
  speed: number;
  alpha: number;
  distortionPhase: number;
}

/**
 * GPU-Accelerated Canvas Fluid Ripple & Refraction Wave Shader
 * Renders concentric liquid shockwaves with chromatic wave rings when the dewdrop
 * crosses chapter milestones or experiences rapid scroll acceleration.
 */
export const FluidRippleShaderCanvas: React.FC<FluidRippleShaderCanvasProps> = ({
  ripples
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const activeRipplesRef = useRef<ActiveRipple[]>([]);

  // Add incoming ripples
  useEffect(() => {
    if (ripples.length === 0) return;
    const latest = ripples[ripples.length - 1];
    if (latest) {
      activeRipplesRef.current.push({
        x: latest.x,
        y: latest.y,
        color: latest.color,
        radius: 4,
        maxRadius: latest.maxRadius || 180,
        speed: latest.speed || 3.5,
        alpha: latest.intensity || 0.85,
        distortionPhase: Math.random() * Math.PI * 2
      });
    }
  }, [ripples]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d', { alpha: true });
    if (!ctx) return;

    let animId: number;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', handleResize);

    let isRendering = false;

    const startLoop = () => {
      if (!isRendering) {
        isRendering = true;
        animId = requestAnimationFrame(render);
      }
    };

    const render = (time: number) => {
      ctx.clearRect(0, 0, width, height);

      const ripplesList = activeRipplesRef.current;
      for (let i = ripplesList.length - 1; i >= 0; i--) {
        const rip = ripplesList[i];
        rip.radius += rip.speed;
        rip.alpha *= 0.965; // exponential decay
        rip.distortionPhase += 0.08;

        if (rip.alpha < 0.01 || rip.radius > rip.maxRadius) {
          ripplesList.splice(i, 1);
          continue;
        }

        // Draw multiple chromatic fluid rings simulating water refraction
        ctx.save();
        ctx.globalCompositeOperation = 'screen';

        // Outer liquid wave ring
        ctx.beginPath();
        const segments = 36;
        for (let s = 0; s <= segments; s++) {
          const angle = (s / segments) * Math.PI * 2;
          // Organic fluid wave wobble
          const waveWobble = Math.sin(angle * 6 + rip.distortionPhase) * (rip.radius * 0.04);
          const r = rip.radius + waveWobble;
          const px = rip.x + Math.cos(angle) * r;
          const py = rip.y + Math.sin(angle) * r;
          if (s === 0) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        }
        ctx.closePath();

        ctx.strokeStyle = rip.color;
        ctx.globalAlpha = rip.alpha * 0.65;
        ctx.lineWidth = Math.max(1, 4 * (1 - rip.radius / rip.maxRadius));
        ctx.stroke();

        // Secondary inner caustic ring (refraction highlight)
        if (rip.radius > 20) {
          ctx.beginPath();
          const innerR = rip.radius * 0.65;
          ctx.arc(rip.x, rip.y, innerR, 0, Math.PI * 2);
          ctx.strokeStyle = '#ffffff';
          ctx.globalAlpha = rip.alpha * 0.45;
          ctx.lineWidth = 1.5;
          ctx.stroke();
        }

        ctx.restore();
      }

      if (activeRipplesRef.current.length > 0) {
        animId = requestAnimationFrame(render);
      } else {
        isRendering = false;
      }
    };

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 pointer-events-none z-20 w-full h-full"
    />
  );
};
