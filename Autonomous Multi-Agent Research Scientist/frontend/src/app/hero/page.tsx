"use client";

import React, { useEffect, useRef, useState } from 'react';
import { ChevronDown, Star, Sparkles, Paperclip, Mic, Search, ArrowUp, Menu, X } from 'lucide-react';
import { Manrope, Cabin, Instrument_Serif, Inter, Schibsted_Grotesk, Fustat } from 'next/font/google';

const manrope = Manrope({ subsets: ['latin'], variable: '--font-manrope' });
const cabin = Cabin({ subsets: ['latin'], variable: '--font-cabin' });
const instrument = Instrument_Serif({ subsets: ['latin'], weight: '400', variable: '--font-instrument' });
const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });
const schibsted = Schibsted_Grotesk({ subsets: ['latin'], variable: '--font-schibsted' });
const fustat = Fustat({ subsets: ['latin'], variable: '--font-fustat' });

function VideoBackground({ src }: { src: string }) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const fadeRafRef = useRef<number | null>(null);
  const fadingOutRef = useRef(false);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const startFade = (targetOpacity: number, duration: number, callback?: () => void) => {
      if (fadeRafRef.current) cancelAnimationFrame(fadeRafRef.current);
      
      const startOpacity = parseFloat(video.style.opacity || '0');
      const startTime = performance.now();
      
      const animate = (currentTime: number) => {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const currentOpacity = startOpacity + (targetOpacity - startOpacity) * progress;
        video.style.opacity = currentOpacity.toString();
        
        if (progress < 1) {
          fadeRafRef.current = requestAnimationFrame(animate);
        } else {
          if (callback) callback();
        }
      };
      
      fadeRafRef.current = requestAnimationFrame(animate);
    };

    const onLoadedData = () => {
      startFade(1, 250);
    };

    const onTimeUpdate = () => {
      const remaining = video.duration - video.currentTime;
      if (remaining <= 0.55 && !fadingOutRef.current) {
        fadingOutRef.current = true;
        startFade(0, 250);
      }
    };

    const onEnded = () => {
      video.style.opacity = '0';
      setTimeout(() => {
        video.currentTime = 0;
        video.play().then(() => {
          fadingOutRef.current = false;
          startFade(1, 250);
        });
      }, 100);
    };

    video.addEventListener('loadeddata', onLoadedData);
    video.addEventListener('timeupdate', onTimeUpdate);
    video.addEventListener('ended', onEnded);
    
    video.style.opacity = '0';
    video.play().catch(e => console.error("Autoplay failed", e));

    return () => {
      video.removeEventListener('loadeddata', onLoadedData);
      video.removeEventListener('timeupdate', onTimeUpdate);
      video.removeEventListener('ended', onEnded);
      if (fadeRafRef.current) cancelAnimationFrame(fadeRafRef.current);
    };
  }, [src]);

  return (
    <div className="absolute inset-0 overflow-hidden bg-black z-0">
      <video
        ref={videoRef}
        src={src}
        muted
        playsInline
        className="absolute top-0 left-1/2 -translate-x-1/2 w-[115%] h-[115%] object-cover object-top max-w-none"
      />
    </div>
  );
}

export default function CombinedHeroSection() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className={`relative min-h-screen w-full overflow-hidden bg-black ${manrope.variable} ${cabin.variable} ${instrument.variable} ${inter.variable} ${schibsted.variable} ${fustat.variable}`}>
      <VideoBackground src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260329_050842_be71947f-f16e-4a14-810c-06e83d23ddb5.mp4" />
      
      <div className="relative z-20 flex flex-col min-h-screen">
        {/* Navbar */}
        <header className="w-full px-6 md:px-[120px] py-[16px] flex items-center justify-between">
          <div className="flex items-center gap-2 text-white font-schibsted font-semibold text-[24px] tracking-[-1.44px]">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M1.04356 6.35771L13.6437 0.666504C14.15 0.436 14.75 0.596 15.1 1.056L22.9 10.956C23.25 11.416 23.25 12.076 22.9 12.536L15.1 22.436C14.75 22.896 14.15 23.056 13.6437 22.8255L1.04356 17.1343C0.42356 16.8543 0 16.2343 0 15.5443V7.94771C0 7.25771 0.42356 6.63771 1.04356 6.35771Z" fill="currentColor"/>
            </svg>
            Logoipsum
          </div>

          <nav className="hidden md:flex items-center gap-8 font-manrope font-medium text-[14px] text-white">
            <a href="#" className="hover:opacity-80 transition-opacity">Platform</a>
            <a href="#" className="hover:opacity-80 transition-opacity flex items-center gap-1">
              Features <ChevronDown className="w-4 h-4 opacity-70" />
            </a>
            <a href="#" className="hover:opacity-80 transition-opacity">Projects</a>
            <a href="#" className="hover:opacity-80 transition-opacity">Community</a>
            <a href="#" className="hover:opacity-80 transition-opacity">Contact</a>
          </nav>

          <div className="hidden md:flex items-center gap-4">
            <button className="bg-white border border-[#d4d4d4] rounded-[8px] text-[#171717] font-manrope font-semibold text-[14px] px-5 py-2 hover:bg-gray-50 transition-colors">
              Sign In
            </button>
            <button className="bg-[#7b39fc] rounded-[8px] text-[#fafafa] font-manrope font-semibold text-[14px] px-5 py-2 hover:bg-[#6a2ce0] transition-colors shadow-lg shadow-[#7b39fc]/20">
              Get Started
            </button>
          </div>

          <button 
            className="md:hidden text-white p-2 z-50"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </header>

        {/* Mobile Menu Overlay */}
        {mobileMenuOpen && (
          <div className="fixed inset-0 bg-black/95 z-40 flex flex-col items-center justify-center gap-8 font-manrope text-white text-xl">
            <a href="#" onClick={() => setMobileMenuOpen(false)}>Platform</a>
            <a href="#" onClick={() => setMobileMenuOpen(false)}>Features</a>
            <a href="#" onClick={() => setMobileMenuOpen(false)}>Projects</a>
            <a href="#" onClick={() => setMobileMenuOpen(false)}>Community</a>
            <a href="#" onClick={() => setMobileMenuOpen(false)}>Contact</a>
            <div className="flex flex-col gap-4 mt-8 w-64">
              <button className="w-full bg-white text-black py-3 rounded-[8px] font-semibold text-lg">Sign In</button>
              <button className="w-full bg-[#7b39fc] py-3 rounded-[8px] font-semibold text-lg">Get Started</button>
            </div>
          </div>
        )}

        {/* Hero Content */}
        <main className="flex-1 flex flex-col items-center pt-[50px] pb-12 px-6">
          <div className="w-full max-w-[1200px] flex flex-col items-center text-center -mt-[20px] md:-mt-[50px]">
            
            {/* Tagline Pill / Badge */}
            <div className="bg-[rgba(85,80,110,0.4)] backdrop-blur-md border border-[rgba(164,132,215,0.5)] rounded-[10px] h-[38px] flex items-center px-1.5 mb-[34px] shadow-sm">
              <div className="bg-[#7b39fc] rounded-[6px] px-2 py-1 flex items-center gap-1">
                <Star className="w-3.5 h-3.5 text-white" fill="currentColor" />
                <span className="font-inter font-medium text-[12px] text-white">New</span>
              </div>
              <span className="font-cabin font-medium text-[14px] text-white mx-3">
                Say Hello to Datacore v3.2 — Discover what's possible
              </span>
            </div>

            {/* Headline */}
            <h1 className="font-fustat font-bold text-[48px] md:text-[80px] tracking-[-4.8px] leading-[1.05] text-white max-w-[900px]">
              Transform Data Quickly <i className="font-instrument font-normal text-indigo-300">and</i> hassle-free
            </h1>

            {/* Subtext */}
            <p className="font-inter font-medium text-[18px] md:text-[20px] tracking-[-0.4px] text-white/70 max-w-[736px] mt-[34px] leading-relaxed">
              Upload your information and get powerful insights right away. Discover handpicked models, fast processing, and 24/7 support. Work smarter and achieve goals effortlessly.
            </p>

            {/* Search Input Box */}
            <div className="mt-[44px] w-full max-w-[728px] bg-[rgba(0,0,0,0.24)] backdrop-blur-xl rounded-[18px] p-5 flex flex-col justify-between h-auto md:h-[200px] border border-white/10 shadow-2xl">
              {/* Top Row */}
              <div className="flex justify-between items-center text-white font-schibsted font-medium text-[12px]">
                <div className="flex items-center gap-3">
                  <span className="opacity-80">60/450 credits</span>
                  <button className="bg-[rgba(90,225,76,0.89)] text-black px-2.5 py-1 rounded-full font-bold hover:bg-[rgba(90,225,76,1)] transition-colors">
                    Upgrade
                  </button>
                </div>
                <div className="flex items-center gap-1.5 opacity-80 bg-white/10 px-2.5 py-1 rounded-full">
                  <Sparkles className="w-3.5 h-3.5 text-amber-300" fill="currentColor" />
                  Powered by GPT-4o
                </div>
              </div>

              {/* Main Input */}
              <div className="relative w-full h-[60px] bg-white rounded-[12px] shadow-lg flex items-center px-4 mt-6 md:mt-0 group focus-within:ring-2 focus-within:ring-[#7b39fc] transition-all">
                <input 
                  type="text" 
                  placeholder="Type question..." 
                  className="flex-1 bg-transparent border-none outline-none text-black font-inter text-[16px] placeholder-black/50"
                />
                <button className="w-[36px] h-[36px] bg-black text-white rounded-full flex items-center justify-center shrink-0 hover:bg-[#7b39fc] transition-colors shadow-md">
                  <ArrowUp className="w-5 h-5" />
                </button>
              </div>

              {/* Bottom Row */}
              <div className="flex flex-col md:flex-row justify-between items-center mt-6 md:mt-0 gap-4 md:gap-0">
                <div className="flex gap-2 w-full md:w-auto overflow-x-auto pb-2 md:pb-0 hide-scrollbar">
                  <button className="flex items-center gap-1.5 bg-[#f8f8f8]/10 hover:bg-[#f8f8f8]/20 text-white px-3 py-1.5 rounded-[6px] text-[13px] font-inter transition-colors whitespace-nowrap">
                    <Paperclip className="w-3.5 h-3.5" /> Attach
                  </button>
                  <button className="flex items-center gap-1.5 bg-[#f8f8f8]/10 hover:bg-[#f8f8f8]/20 text-white px-3 py-1.5 rounded-[6px] text-[13px] font-inter transition-colors whitespace-nowrap">
                    <Mic className="w-3.5 h-3.5" /> Voice
                  </button>
                  <button className="flex items-center gap-1.5 bg-[#f8f8f8]/10 hover:bg-[#f8f8f8]/20 text-white px-3 py-1.5 rounded-[6px] text-[13px] font-inter transition-colors whitespace-nowrap">
                    <Search className="w-3.5 h-3.5" /> Prompts
                  </button>
                </div>
                <div className="text-[#a0a0a0] text-[12px] font-inter opacity-80 shrink-0">
                  0/3,000
                </div>
              </div>
            </div>

            {/* Call to Action Buttons */}
            <div className="mt-12 flex flex-col sm:flex-row gap-4 items-center justify-center">
              <button className="bg-[#7b39fc] hover:bg-[#8b4fff] text-white font-cabin font-medium text-[16px] px-8 py-3.5 rounded-[10px] transition-colors shadow-lg shadow-[#7b39fc]/20 min-w-[200px]">
                Book a Free Demo
              </button>
              <button className="bg-[#2b2344] hover:bg-[#3d325c] text-[#f6f7f9] font-cabin font-medium text-[16px] px-8 py-3.5 rounded-[10px] border border-white/5 transition-colors shadow-lg min-w-[200px]">
                Get Started Now
              </button>
            </div>

          </div>
        </main>
      </div>
    </div>
  );
}
