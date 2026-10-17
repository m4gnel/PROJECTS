import React, { useRef, useState } from 'react';

interface GlassTiltCardProps {
  children: React.ReactNode;
  className?: string;
  glareColor?: string;
  tiltMaxAngle?: number;
  translateZ?: number;
  onClick?: () => void;
}

export const GlassTiltCard: React.FC<GlassTiltCardProps> = ({
  children,
  className = '',
  glareColor = 'rgba(16, 185, 129, 0.15)',
  tiltMaxAngle = 10,
  translateZ = 0,
  onClick,
}) => {
  const cardRef = useRef<HTMLDivElement>(null);
  const [style, setStyle] = useState<React.CSSProperties>({
    transform: `perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(${translateZ}px) scale3d(1, 1, 1)`,
    transition: 'transform 0.4s cubic-bezier(0.25, 1, 0.5, 1)',
    transformStyle: 'preserve-3d',
    willChange: 'transform',
  });
  const [glarePosition, setGlarePosition] = useState({ x: 50, y: 50, opacity: 0 });

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rotateX = ((y - centerY) / centerY) * -tiltMaxAngle;
    const rotateY = ((x - centerX) / centerX) * tiltMaxAngle;

    setStyle({
      transform: `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateZ(${translateZ + 25}px) scale3d(1.03, 1.03, 1.03)`,
      transition: 'transform 0.1s ease-out',
      transformStyle: 'preserve-3d',
      willChange: 'transform',
    });

    setGlarePosition({
      x: (x / rect.width) * 100,
      y: (y / rect.height) * 100,
      opacity: 0.65,
    });
  };

  const handleMouseLeave = () => {
    setStyle({
      transform: `perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(${translateZ}px) scale3d(1, 1, 1)`,
      transition: 'transform 0.5s cubic-bezier(0.25, 1, 0.5, 1)',
      transformStyle: 'preserve-3d',
      willChange: 'transform',
    });
    setGlarePosition((prev) => ({ ...prev, opacity: 0 }));
  };

  return (
    <div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      onClick={onClick}
      style={style}
      className={`relative overflow-hidden rounded-2xl backdrop-blur-xl border border-white/20 dark:border-white/10 shadow-2xl transition-shadow duration-300 hover:shadow-emerald-500/10 cursor-pointer ${className}`}
    >
      {/* Dynamic Specular Glare Reflection */}
      <div
        className="pointer-events-none absolute inset-0 transition-opacity duration-300 z-10"
        style={{
          opacity: glarePosition.opacity,
          background: `radial-gradient(circle at ${glarePosition.x}% ${glarePosition.y}%, ${glareColor}, transparent 60%)`,
        }}
      />
      {children}
    </div>
  );
};
