'use client';

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import {
  ArrowUp,
  ChevronDown,
  Menu,
  Mic,
  Paperclip,
  Search,
  Sparkles,
  X,
} from "lucide-react";

const navItems = ["Platform", "Features", "Projects", "Community", "Contact"];

export default function LandingPage() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const animationFrameRef = useRef<number | null>(null);
  const opacityRef = useRef(1);
  const fadingOutRef = useRef(false);
  const [videoOpacity, setVideoOpacity] = useState(1);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) {
      return undefined;
    }

    let replayTimeout: number | undefined;
    let endedTimeout: number | undefined;

    const cancelCurrentAnimation = () => {
      if (animationFrameRef.current !== null) {
        window.cancelAnimationFrame(animationFrameRef.current);
        animationFrameRef.current = null;
      }
    };

    const runFade = (to: number, duration: number) => {
      cancelCurrentAnimation();

      const startTime = performance.now();
      const startOpacity = opacityRef.current;

      const step = (now: number) => {
        const elapsed = now - startTime;
        const progress = Math.min(1, elapsed / duration);
        const easedProgress = progress < 0.5
          ? 4 * progress * progress * progress
          : 1 - Math.pow(-2 * progress + 2, 3) / 2;

        const nextOpacity = startOpacity + (to - startOpacity) * easedProgress;
        opacityRef.current = nextOpacity;
        setVideoOpacity(nextOpacity);

        if (progress < 1) {
          animationFrameRef.current = window.requestAnimationFrame(step);
        }
      };

      animationFrameRef.current = window.requestAnimationFrame(step);
    };

    const handleLoadedData = () => {
      runFade(1, 250);
      void video.play().catch(() => undefined);
    };

    const handleTimeUpdate = () => {
      if (!video.duration) {
        return;
      }

      const remaining = video.duration - video.currentTime;
      if (remaining <= 0.55 && !fadingOutRef.current) {
        fadingOutRef.current = true;
        runFade(0, 250);
      }
    };

    const handleEnded = () => {
      fadingOutRef.current = false;
      opacityRef.current = 0;
      setVideoOpacity(0);

      if (endedTimeout) {
        window.clearTimeout(endedTimeout);
      }
      if (replayTimeout) {
        window.clearTimeout(replayTimeout);
      }

      endedTimeout = window.setTimeout(() => {
        if (video) {
          video.currentTime = 0;
          void video.play().catch(() => undefined);
        }
      }, 100);

      replayTimeout = window.setTimeout(() => {
        runFade(1, 250);
      }, 100);
    };

    video.addEventListener("loadeddata", handleLoadedData);
    video.addEventListener("timeupdate", handleTimeUpdate);
    video.addEventListener("ended", handleEnded);

    handleLoadedData();

    return () => {
      video.removeEventListener("loadeddata", handleLoadedData);
      video.removeEventListener("timeupdate", handleTimeUpdate);
      video.removeEventListener("ended", handleEnded);
      cancelCurrentAnimation();
      if (endedTimeout) {
        window.clearTimeout(endedTimeout);
      }
      if (replayTimeout) {
        window.clearTimeout(replayTimeout);
      }
    };
  }, []);

  return (
    <div className="relative min-h-screen overflow-hidden bg-[#05060d] text-white">
      <div className="absolute inset-0">
        <video
          ref={videoRef}
          className="absolute inset-0 h-full w-full scale-[1.15] object-cover object-top"
          autoPlay
          loop={false}
          muted
          playsInline
          poster="https://images.unsplash.com/photo-1519677100203-a0e668c92439?auto=format&fit=crop&w=1600&q=80"
          style={{ opacity: videoOpacity }}
        >
          <source src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260329_050842_be71947f-f16e-4a14-810c-06e83d23ddb5.mp4" type="video/mp4" />
        </video>
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(123,57,252,0.35),_transparent_55%)]" />
        <div className="absolute inset-0 bg-black/25" />
        <div className="absolute inset-0 bg-[linear-gradient(120deg,_rgba(0,0,0,0.22),_rgba(5,6,13,0.68))]" />
      </div>

      <div className="relative z-10 flex min-h-screen flex-col">
        <header className="px-6 py-4 sm:px-8 lg:px-[120px] lg:py-5">
          <nav className="flex items-center justify-between rounded-full border border-white/15 bg-white/10 px-4 py-3 shadow-[0_18px_55px_rgba(0,0,0,0.24)] backdrop-blur-xl">
            <Link href="/" className="flex items-center gap-3 text-[24px] font-semibold tracking-[-0.02em] text-white" style={{ fontFamily: "var(--font-schibsted-grotesk)" }}>
              <span className="flex h-10 w-10 items-center justify-center rounded-full border border-white/20 bg-white/10 text-sm font-bold">L</span>
              <span>Logoipsum</span>
            </Link>

            <div className="hidden items-center gap-7 lg:flex">
              {navItems.map((item) => (
                <button
                  key={item}
                  type="button"
                  className="flex items-center gap-1 text-[15px] font-medium tracking-[-0.01em] text-white/90 hover:text-white"
                  style={{ fontFamily: "var(--font-schibsted-grotesk)" }}
                >
                  {item}
                  {item === "Features" ? <ChevronDown size={16} /> : null}
                </button>
              ))}
            </div>

            <div className="hidden items-center gap-3 lg:flex">
              <button
                type="button"
                className="flex h-11 items-center justify-center rounded-[10px] border border-white/20 bg-transparent px-4 text-[14px] font-semibold text-white"
                style={{ fontFamily: "var(--font-manrope)" }}
              >
                Sign Up
              </button>
              <button
                type="button"
                className="flex h-11 items-center justify-center rounded-[10px] bg-[#0f1118] px-5 text-[14px] font-semibold text-white shadow-[0_10px_30px_rgba(0,0,0,0.28)]"
                style={{ fontFamily: "var(--font-manrope)" }}
              >
                Log In
              </button>
            </div>

            <button
              type="button"
              className="flex h-11 w-11 items-center justify-center rounded-full border border-white/20 bg-white/10 text-white lg:hidden"
              onClick={() => setMenuOpen((value) => !value)}
              aria-label="Toggle navigation"
            >
              {menuOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
          </nav>

          {menuOpen ? (
            <div className="mt-4 rounded-[24px] border border-white/15 bg-[#05060d]/90 p-6 shadow-[0_20px_60px_rgba(0,0,0,0.35)] backdrop-blur-xl lg:hidden">
              <div className="flex flex-col gap-3">
                {navItems.map((item) => (
                  <button key={item} type="button" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-left text-sm font-medium text-white/90">
                    {item}
                  </button>
                ))}
                <div className="mt-2 flex gap-3">
                  <button type="button" className="flex-1 rounded-[10px] border border-white/20 bg-transparent px-4 py-3 text-sm font-semibold text-white">
                    Sign Up
                  </button>
                  <button type="button" className="flex-1 rounded-[10px] bg-[#0f1118] px-4 py-3 text-sm font-semibold text-white">
                    Log In
                  </button>
                </div>
              </div>
            </div>
          ) : null}
        </header>

        <main className="flex flex-1 items-center justify-center px-6 pb-16 pt-6 sm:px-8 lg:px-[120px] lg:pt-0">
          <div className="mx-auto flex max-w-6xl flex-col items-center text-center">
            <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-white/20 bg-[rgba(85,80,110,0.38)] px-3 py-2 shadow-[0_10px_35px_rgba(0,0,0,0.25)] backdrop-blur-xl">
              <span className="flex h-6 w-6 items-center justify-center rounded-full bg-[#7b39fc] text-white">
                <Sparkles size={14} />
              </span>
              <span className="text-[14px] font-medium text-white/90" style={{ fontFamily: "var(--font-inter)" }}>
                Discover what&apos;s possible
              </span>
            </div>

            <h1
              className="max-w-5xl text-[clamp(2.8rem,5vw,5rem)] font-bold leading-[0.9] tracking-[-0.04em] text-white sm:text-[4.8rem] lg:text-[6.5rem]"
              style={{ fontFamily: "var(--font-fustat)" }}
            >
              Transform Data Quickly
            </h1>

            <p className="mt-7 max-w-[736px] text-[18px] leading-8 text-white/75 sm:text-[20px]" style={{ fontFamily: "var(--font-fustat)" }}>
              Upload your information and get powerful insights right away. Work smarter and achieve goals effortlessly.
            </p>

            <div className="mt-10 w-full max-w-[728px] rounded-[24px] border border-white/20 bg-[rgba(0,0,0,0.24)] p-3 shadow-[0_20px_80px_rgba(0,0,0,0.35)] backdrop-blur-xl sm:p-4">
              <div className="mb-3 flex flex-wrap items-center justify-between gap-3 rounded-[14px] border border-white/10 bg-white/10 px-3 py-2 text-[12px] text-white/85 sm:px-4" style={{ fontFamily: "var(--font-schibsted-grotesk)" }}>
                <div className="flex flex-wrap items-center gap-2">
                  <span>60/450 credits</span>
                  <span className="rounded-full bg-[rgba(90,225,76,0.89)] px-2.5 py-1 font-semibold text-black">Upgrade</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="flex h-6 w-6 items-center justify-center rounded-full bg-[#ffffff14]">
                    <Sparkles size={14} />
                  </span>
                  <span>Powered by GPT-4o</span>
                </div>
              </div>

              <div className="rounded-[16px] bg-white p-3 shadow-[0_12px_40px_rgba(0,0,0,0.2)]">
                <div className="flex items-center gap-3 rounded-[12px] border border-black/10 bg-white px-3 py-3 sm:px-4">
                  <Search size={18} className="text-black/55" />
                  <input
                    type="text"
                    placeholder="Type question..."
                    className="flex-1 border-none bg-transparent text-[16px] text-black/70 outline-none"
                    style={{ fontFamily: "var(--font-schibsted-grotesk)" }}
                  />
                  <button type="button" className="flex h-9 w-9 items-center justify-center rounded-full bg-[#05060d] text-white sm:h-10 sm:w-10">
                    <ArrowUp size={16} />
                  </button>
                </div>
              </div>

              <div className="mt-3 flex flex-wrap items-center justify-between gap-3">
                <div className="flex flex-wrap gap-2">
                  <button type="button" className="flex items-center gap-2 rounded-[8px] bg-[#f8f8f8] px-3 py-2 text-[12px] font-medium text-[#1f1f1f]" style={{ fontFamily: "var(--font-schibsted-grotesk)" }}>
                    <Paperclip size={14} />
                    Attach
                  </button>
                  <button type="button" className="flex items-center gap-2 rounded-[8px] bg-[#f8f8f8] px-3 py-2 text-[12px] font-medium text-[#1f1f1f]" style={{ fontFamily: "var(--font-schibsted-grotesk)" }}>
                    <Mic size={14} />
                    Voice
                  </button>
                  <button type="button" className="flex items-center gap-2 rounded-[8px] bg-[#f8f8f8] px-3 py-2 text-[12px] font-medium text-[#1f1f1f]" style={{ fontFamily: "var(--font-schibsted-grotesk)" }}>
                    <Search size={14} />
                    Prompts
                  </button>
                </div>
                <div className="text-[12px] text-white/70" style={{ fontFamily: "var(--font-schibsted-grotesk)" }}>
                  0/3,000
                </div>
              </div>
            </div>

            <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
              <Link href="/home" className="rounded-[12px] bg-[#7b39fc] px-6 py-3 text-[15px] font-semibold text-white shadow-[0_14px_35px_rgba(123,57,252,0.35)]" style={{ fontFamily: "var(--font-cabin)" }}>
                Book a Free Demo
              </Link>
              <Link href="/research" className="rounded-[12px] bg-[#2b2344] px-6 py-3 text-[15px] font-semibold text-[#f6f7f9]" style={{ fontFamily: "var(--font-cabin)" }}>
                Explore the Platform
              </Link>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
