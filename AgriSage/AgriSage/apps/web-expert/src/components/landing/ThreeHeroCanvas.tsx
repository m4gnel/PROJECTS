import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

interface ThreeHeroCanvasProps {
  className?: string;
}

export const ThreeHeroCanvas: React.FC<ThreeHeroCanvasProps> = ({ className = '' }) => {
  const mountRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    // Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const width = container.clientWidth || window.innerWidth;
    const height = container.clientHeight || window.innerHeight;

    const camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
    camera.position.z = 28;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: false, powerPreference: 'high-performance' });
    renderer.setSize(width, height);
    renderer.setPixelRatio(1.0);
    container.appendChild(renderer.domElement);

    // 1. Particle System (Bio-luminescent spores / data nodes)
    const particleCount = 200;
    const particleGeometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);
    const scales = new Float32Array(particleCount);

    const emerald = new THREE.Color(0x10b981);
    const cyan = new THREE.Color(0x06b6d4);
    const amber = new THREE.Color(0xf59e0b);

    for (let i = 0; i < particleCount; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 60;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 45;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 35;

      const mixedColor = i % 3 === 0 ? emerald : i % 3 === 1 ? cyan : amber;
      colors[i * 3] = mixedColor.r;
      colors[i * 3 + 1] = mixedColor.g;
      colors[i * 3 + 2] = mixedColor.b;

      scales[i] = Math.random() * 2 + 1;
    }

    particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particleGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    // Custom Canvas Circle Texture for smooth glowing orbs
    const canvas = document.createElement('canvas');
    canvas.width = 64;
    canvas.height = 64;
    const ctx = canvas.getContext('2d');
    if (ctx) {
      const gradient = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
      gradient.addColorStop(0, 'rgba(255, 255, 255, 1)');
      gradient.addColorStop(0.3, 'rgba(16, 185, 129, 0.8)');
      gradient.addColorStop(0.7, 'rgba(6, 182, 212, 0.3)');
      gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, 64, 64);
    }
    const texture = new THREE.CanvasTexture(canvas);

    const particleMaterial = new THREE.PointsMaterial({
      size: 1.4,
      map: texture,
      vertexColors: true,
      transparent: true,
      opacity: 0.75,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });

    const particles = new THREE.Points(particleGeometry, particleMaterial);
    scene.add(particles);

    // Mouse Tracking with smooth interpolation
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;

    const handleMouseMove = (e: MouseEvent) => {
      const windowHalfX = window.innerWidth / 2;
      const windowHalfY = window.innerHeight / 2;
      targetX = (e.clientX - windowHalfX) * 0.0008;
      targetY = (e.clientY - windowHalfY) * 0.0008;
    };

    window.addEventListener('mousemove', handleMouseMove, { passive: true });

    // Animation Loop with Dynamic FPS Monitoring & Quality Downscaling
    let animationFrameId = 0;
    let clock = new THREE.Clock();
    let frameCount = 0;
    let lastFpsCheckTime = performance.now();
    let isLowQualityMode = false;
    let isVisible = true;

    const animate = () => {
      if (!isVisible) {
        animationFrameId = 0;
        return;
      }
      animationFrameId = requestAnimationFrame(animate);
      const elapsedTime = clock.getElapsedTime();
      const now = performance.now();

      // Dynamic FPS monitoring (every 60 frames ~ 1 sec)
      frameCount++;
      if (frameCount >= 60) {
        const deltaSec = (now - lastFpsCheckTime) / 1000;
        const currentFps = frameCount / deltaSec;
        frameCount = 0;
        lastFpsCheckTime = now;

        // Downscale quality if FPS drops below 45
        if (currentFps < 45 && !isLowQualityMode) {
          isLowQualityMode = true;
          renderer.setPixelRatio(1.0);
          particleGeometry.setDrawRange(0, 225); // reduce rendering load by half
        }
      }

      // Smooth camera parallax
      mouseX += (targetX - mouseX) * 0.05;
      mouseY += (targetY - mouseY) * 0.05;
      camera.position.x = mouseX * 8;
      camera.position.y = -mouseY * 8;
      camera.lookAt(scene.position);

      // Rotate particles
      particles.rotation.y = elapsedTime * 0.03;
      particles.rotation.x = elapsedTime * 0.015;

      renderer.render(scene, camera);
    };

    const observer = new IntersectionObserver(
      ([entry]) => {
        isVisible = entry.isIntersecting;
        if (isVisible && animationFrameId === 0) {
          animate();
        }
      },
      { threshold: 0.01 }
    );
    observer.observe(container);

    // Initial start
    animate();

    // Resize Handler
    const handleResize = () => {
      if (!container) return;
      const newWidth = container.clientWidth;
      const newHeight = container.clientHeight;
      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(newWidth, newHeight);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      observer.disconnect();
      if (animationFrameId) cancelAnimationFrame(animationFrameId);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('resize', handleResize);
      if (container && renderer.domElement) {
        container.removeChild(renderer.domElement);
      }
      renderer.dispose();
      particleGeometry.dispose();
      particleMaterial.dispose();
      texture.dispose();
    };
  }, []);

  return (
    <div
      ref={mountRef}
      className={`absolute inset-0 pointer-events-none overflow-hidden z-0 ${className}`}
      style={{ opacity: 0.85 }}
    />
  );
};
