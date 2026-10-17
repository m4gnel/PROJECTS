import React, { useState } from 'react';
import { Leaf } from 'lucide-react';
import { getPublicUrl } from '@/lib/utils';

interface SafeImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
  fallbackTitle?: string;
}

export const SafeImage: React.FC<SafeImageProps> = ({
  src,
  alt = 'Crop specimen',
  fallbackTitle = 'Specimen Image',
  className = '',
  style,
  ...props
}) => {
  const [hasError, setHasError] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const resolvedSrc = src ? getPublicUrl(src) : undefined;

  if (hasError || !resolvedSrc) {
    return (
      <div
        className={`flex flex-col items-center justify-center bg-gradient-to-br from-emerald-950/40 to-slate-900 border border-emerald-500/20 text-emerald-400 p-4 text-center select-none ${className}`}
        style={style}
      >
        <Leaf size={32} className="text-emerald-500 mb-1 opacity-80" />
        <span className="text-xs font-bold text-white tracking-wide">{alt}</span>
        <span className="text-[10px] text-emerald-400/80 mt-0.5 font-mono">Field Camera Feed Cached</span>
      </div>
    );
  }

  return (
    <div className="relative w-full h-full flex items-center justify-center overflow-hidden">
      {isLoading && (
        <div className="absolute inset-0 bg-slate-900/60 animate-pulse flex items-center justify-center text-xs text-emerald-400 font-mono">
          Loading specimen...
        </div>
      )}
      <img
        src={resolvedSrc}
        alt={alt}
        className={`${className} ${isLoading ? 'opacity-0' : 'opacity-100'} transition-opacity duration-300`}
        style={style}
        onLoad={() => setIsLoading(false)}
        onError={() => setHasError(true)}
        {...props}
      />
    </div>
  );
};
