/**
 * Agri-SAGE Creative Motion Mathematics Engine
 * 
 * Provides high-precision mathematical models:
 * - Linear Interpolation (LERP)
 * - Delta-time independent damping (damp)
 * - Clamped and unclamped range mapping (mapRange, mapRangeClamped)
 * - Liquid surface tension and velocity-based elongation physics
 * - 2D Catmull-Rom Sinuous River Spline interpolation with continuous tangent vectors
 */

export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

export function lerp(start: number, end: number, alpha: number): number {
  return start + (end - start) * alpha;
}

/**
 * Delta-time independent exponential damping (smooth damping)
 * lambda controls stiffness (typically 8 to 20)
 * delta is delta time in seconds (e.g. 0.016 for 60fps)
 */
export function damp(current: number, target: number, lambda: number, delta: number): number {
  return lerp(current, target, 1 - Math.exp(-lambda * delta));
}

/**
 * Maps a number from an input range to an output range
 */
export function mapRange(
  value: number,
  inMin: number,
  inMax: number,
  outMin: number,
  outMax: number
): number {
  if (inMax === inMin) return outMin;
  return outMin + ((value - inMin) / (inMax - inMin)) * (outMax - outMin);
}

/**
 * Maps a number from an input range to an output range with output clamping
 */
export function mapRangeClamped(
  value: number,
  inMin: number,
  inMax: number,
  outMin: number,
  outMax: number
): number {
  const mapped = mapRange(value, inMin, inMax, outMin, outMax);
  const min = Math.min(outMin, outMax);
  const max = Math.max(outMin, outMax);
  return clamp(mapped, min, max);
}

export interface SplinePoint {
  x: number; // in percentage or pixels
  y: number;
}

/**
 * 1D Catmull-Rom cubic interpolation between p1 and p2 using neighboring points p0 and p3.
 */
export function catmullRom1D(p0: number, p1: number, p2: number, p3: number, t: number): number {
  return 0.5 * (
    (2 * p1) +
    (-p0 + p2) * t +
    (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t +
    (-p0 + 3 * p1 - 3 * p2 + p3) * t * t * t
  );
}

/**
 * Derivative of 1D Catmull-Rom cubic interpolation (tangent slope).
 */
export function catmullRomDerivative1D(p0: number, p1: number, p2: number, p3: number, t: number): number {
  return 0.5 * (
    (-p0 + p2) +
    2 * (2 * p0 - 5 * p1 + 4 * p2 - p3) * t +
    3 * (-p0 + 3 * p1 - 3 * p2 + p3) * t * t
  );
}

/**
 * Evaluates a 2D Catmull-Rom spline at normalized parameter progress in [0, 1].
 * Returns interpolated { x, y } and directional tangent { tx, ty, angleDeg }.
 */
export function evaluateSpline(
  points: SplinePoint[],
  progress: number
): { x: number; y: number; tx: number; ty: number; angleDeg: number } {
  const n = points.length;
  if (n === 0) return { x: 0, y: 0, tx: 0, ty: 1, angleDeg: 0 };
  if (n === 1) return { x: points[0].x, y: points[0].y, tx: 0, ty: 1, angleDeg: 0 };

  const clampedP = clamp(progress, 0, 1);
  const totalSegments = n - 1;
  const scaled = clampedP * totalSegments;
  const segIdx = Math.min(Math.floor(scaled), totalSegments - 1);
  const t = scaled - segIdx;

  const p0 = points[Math.max(0, segIdx - 1)];
  const p1 = points[segIdx];
  const p2 = points[Math.min(n - 1, segIdx + 1)];
  const p3 = points[Math.min(n - 1, segIdx + 2)];

  const x = catmullRom1D(p0.x, p1.x, p2.x, p3.x, t);
  const y = catmullRom1D(p0.y, p1.y, p2.y, p3.y, t);

  const tx = catmullRomDerivative1D(p0.x, p1.x, p2.x, p3.x, t);
  const ty = catmullRomDerivative1D(p0.y, p1.y, p2.y, p3.y, t);

  // Calculate tangent rotation angle (0 deg = pointing straight down)
  const angleRad = Math.atan2(tx, ty);
  const angleDeg = -(angleRad * 180) / Math.PI;

  return { x, y, tx, ty, angleDeg };
}

/**
 * Calculates physical surface tension deformation for fluid droplets
 * when subjected to 2D velocity vectors and natural surface oscillations.
 */
export interface DropletDeformation {
  scaleX: number;
  scaleY: number;
  wobbleX: number;
  wobbleY: number;
  rotation: number;
}

export function calculateDropletPhysics(
  velocity: number, // pixels per second or frame delta
  timeSec: number,
  direction: number // 1 = down, -1 = up
): DropletDeformation {
  const safeVel = isNaN(velocity) || !isFinite(velocity) ? 0 : velocity;
  const absVel = Math.abs(safeVel);
  
  // Velocity stretch (teardrop elongation along motion vector)
  const stretchY = clamp(absVel * 0.0016, 0, 0.42);
  const squeezeX = clamp(absVel * 0.0011, 0, 0.25);

  // Surface tension natural oscillation (gentle breathing droplet when stationary)
  const safeTime = isNaN(timeSec) || !isFinite(timeSec) ? 0 : timeSec;
  const naturalBreath = Math.sin(safeTime * 3.5) * 0.04;

  const scaleY = 1 + stretchY + naturalBreath;
  const scaleX = 1 - squeezeX - naturalBreath;

  // Sinuous liquid wobble displacement
  const wobbleX = Math.sin(safeTime * 4.2) * (1.5 + absVel * 0.015);
  const wobbleY = Math.cos(safeTime * 3.8) * 1.2;

  // Dynamic tilt angle responding to horizontal drift and velocity
  const rotation = clamp(safeVel * 0.02, -22, 22);

  return {
    scaleX: Math.max(0.68, isNaN(scaleX) ? 1.0 : scaleX),
    scaleY: Math.max(0.72, isNaN(scaleY) ? 1.0 : scaleY),
    wobbleX: isNaN(wobbleX) ? 0 : wobbleX,
    wobbleY: isNaN(wobbleY) ? 0 : wobbleY,
    rotation: isNaN(rotation) ? 0 : rotation
  };
}
