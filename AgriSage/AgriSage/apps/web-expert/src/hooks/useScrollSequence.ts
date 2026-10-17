import { useEffect, useRef, useCallback } from 'react';

/**
 * useScrollSequence – Scroll-scrubbed image sequence player.
 * 
 * Takes an array of image URLs and a container ref, draws the
 * correct frame to a <canvas> based on scroll position within
 * the container's viewport range.
 * 
 * This creates the "video scrub on scroll" effect where scrolling
 * forward/backward plays/rewinds a sequence of still frames.
 * 
 * Similar to Apple's AirPods Pro page effect.
 */
interface UseScrollSequenceOptions {
  /** Ordered array of frame image URLs */
  frameUrls: string[];
  /** Ref to the container section that bounds the sequence */
  containerRef: React.RefObject<HTMLElement | null>;
  /** Ref to the canvas element to draw on */
  canvasRef: React.RefObject<HTMLCanvasElement | null>;
}

export const useScrollSequence = ({
  frameUrls,
  containerRef,
  canvasRef
}: UseScrollSequenceOptions) => {
  const imagesRef = useRef<HTMLImageElement[]>([]);
  const currentFrameRef = useRef(0);
  const loadedCountRef = useRef(0);
  const rafId = useRef<number>(0);
  const ticking = useRef(false);

  // Preload all frames
  useEffect(() => {
    const images: HTMLImageElement[] = [];

    frameUrls.forEach((url, i) => {
      const img = new Image();
      img.src = url;
      img.onload = () => {
        loadedCountRef.current++;
        // Draw first frame once loaded
        if (i === 0 && canvasRef.current) {
          drawFrame(0, images);
        }
      };
      images[i] = img;
    });

    imagesRef.current = images;

    return () => {
      images.forEach((img) => {
        img.onload = null;
      });
    };
  }, [frameUrls]); // eslint-disable-line react-hooks/exhaustive-deps

  const drawFrame = useCallback((frameIndex: number, images?: HTMLImageElement[]) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const imgs = images || imagesRef.current;
    const img = imgs[frameIndex];
    if (!img || !img.complete || img.naturalWidth === 0) return;

    // Set canvas size to match container for crisp rendering
    const container = containerRef.current;
    if (container) {
      const rect = container.getBoundingClientRect();
      if (canvas.width !== rect.width || canvas.height !== rect.height) {
        canvas.width = rect.width;
        canvas.height = rect.height;
      }
    }

    // Draw with cover-fit (maintain aspect ratio, fill canvas)
    const imgRatio = img.naturalWidth / img.naturalHeight;
    const canvasRatio = canvas.width / canvas.height;

    let sx = 0, sy = 0, sw = img.naturalWidth, sh = img.naturalHeight;

    if (imgRatio > canvasRatio) {
      // Image wider than canvas – crop sides
      sw = img.naturalHeight * canvasRatio;
      sx = (img.naturalWidth - sw) / 2;
    } else {
      // Image taller – crop top/bottom
      sh = img.naturalWidth / canvasRatio;
      sy = (img.naturalHeight - sh) / 2;
    }

    ctx.drawImage(img, sx, sy, sw, sh, 0, 0, canvas.width, canvas.height);
  }, [canvasRef, containerRef]);

  const updateFrame = useCallback(() => {
    const container = containerRef.current;
    if (!container) {
      ticking.current = false;
      return;
    }

    const rect = container.getBoundingClientRect();
    const windowH = window.innerHeight;

    // Calculate progress: 0 when container top enters viewport bottom,
    // 1 when container bottom exits viewport top
    const totalTravel = rect.height + windowH;
    const traveled = windowH - rect.top;
    const progress = Math.max(0, Math.min(1, traveled / totalTravel));

    const totalFrames = imagesRef.current.length;
    const frameIndex = Math.min(totalFrames - 1, Math.floor(progress * totalFrames));

    if (frameIndex !== currentFrameRef.current && frameIndex >= 0) {
      currentFrameRef.current = frameIndex;
      drawFrame(frameIndex);
    }

    ticking.current = false;
  }, [containerRef, drawFrame]);

  const handleScroll = useCallback(() => {
    if (!ticking.current) {
      ticking.current = true;
      rafId.current = requestAnimationFrame(updateFrame);
    }
  }, [updateFrame]);

  useEffect(() => {
    window.addEventListener('scroll', handleScroll, { passive: true });
    window.addEventListener('resize', () => {
      drawFrame(currentFrameRef.current);
    });

    // Initial frame
    requestAnimationFrame(updateFrame);

    return () => {
      window.removeEventListener('scroll', handleScroll);
      cancelAnimationFrame(rafId.current);
    };
  }, [handleScroll, updateFrame, drawFrame]);

  return {
    currentFrame: currentFrameRef.current,
    totalFrames: frameUrls.length,
    isLoaded: loadedCountRef.current >= frameUrls.length
  };
};
