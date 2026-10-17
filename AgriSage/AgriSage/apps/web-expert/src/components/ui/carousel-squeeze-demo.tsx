"use client";

import { useEffect, useRef, useState } from "react";
import { SqueezeCarousel, type SqueezeSlide } from "@/components/ui/carousel-squeeze";
import { Cpu, Globe, Layers, Mic, ShieldAlert, Sparkles } from "lucide-react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { getPublicUrl } from "@/lib/utils";

export const settings = {
    height: 380,
    gap: 16,
    slatGap: 8,
    slatWidth: 10,
    radius: 12,
    duration: 800,
    hoverGrow: true,
    autoplay: true,
    interval: 3800,
    controls: true,
};

type DemoProps = Partial<typeof settings>;

/** A sleek biophilic overlay badge for Agri-SAGE cards. */
const badge = (icon: React.ReactNode, text: string) => (
    <div className="flex items-center gap-2 rounded-full bg-slate-950/80 backdrop-blur-md px-3.5 py-1.5 border border-emerald-500/30 text-xs font-semibold font-mono tracking-wide text-emerald-300 shadow-xl">
        {icon}
        <span>{text}</span>
    </div>
);

const agriSlides: SqueezeSlide[] = [
    {
        id: "multispectral",
        title: "Sentinel-2 Multi-Spectral Canopy Mesh.",
        description:
            "Agri-SAGE processes 10-meter resolution reflectance bands to detect canopy chlorophyll stress and nitrogen deficit 14 days before visible chlorosis.",
        action: "Explore Canopy Vision",
        overlay: badge(<Globe className="size-3.5 text-emerald-400" />, "Space-to-Soil"),
        image: getPublicUrl("/images/hero_earth.jpg"),
        imageAlt: "Vast green farmland under golden hour sunlight with high precision crop rows",
    },
    {
        id: "biophysical",
        title: "DSSAT & APSIM Biophysical Digital Twins.",
        description:
            "Execute 10,000 parallel Monte Carlo crop growth simulations modeling root water uptake, transpiration efficiency, and yield forecasts.",
        action: "Simulate Micro-Climate",
        overlay: badge(<Layers className="size-3.5 text-cyan-400" />, "Biophysical Twin"),
        image: getPublicUrl("/images/hero_sprout_macro.jpg"),
        imageAlt: "Detailed close up of vibrant green plant leaf structure with dew drops",
    },
    {
        id: "iot-mesh",
        title: "LoRaWAN Edge Soil Telemetry Nodes.",
        description:
            "Solar-powered field sensors transmit sub-surface volumetric water content, electrical conductivity, and root-zone thermal gradients at 15-minute intervals.",
        action: "View Sensor Network",
        overlay: badge(<Cpu className="size-3.5 text-amber-400" />, "IoT Edge Node"),
        image: getPublicUrl("/images/crop_split.jpg"),
        imageAlt: "Solar energy panels surrounded by green crop fields",
    },
    {
        id: "cibrc-guard",
        title: "CIB&RC Chemical Safety & Toxicity Critic.",
        description:
            "Autonomous neural validator cross-references pesticide dosage, active ingredient compatibility, and PHI harvest safety intervals.",
        action: "Check Chemical Safety",
        overlay: badge(<ShieldAlert className="size-3.5 text-rose-400" />, "Safety Guardrail"),
        image: getPublicUrl("/images/cellular_macro.jpg"),
        imageAlt: "Modern hydroponic agricultural research facility with glowing LEDs",
    },
    {
        id: "voice-bhashini",
        title: "Vernacular Multilingual Voice Engine.",
        description:
            "Bhashini-powered speech recognition delivers real-time agronomic guidance in 22 Indian languages tailored for rural dialing and audio notes.",
        action: "Listen to Sample Advisory",
        overlay: badge(<Mic className="size-3.5 text-violet-400" />, "Vernacular Voice"),
        image: getPublicUrl("/images/farmer_tablet.jpg"),
        imageAlt: "Indian farmer working in lush green agricultural field",
    },
    {
        id: "sar-radar",
        title: "Synthetic Aperture Radar (SAR) Subsoil Scanner.",
        description:
            "Microwave penetration pierces cloud cover and dense vegetation to quantify deep aquifer reserves and soil organic carbon sequestration.",
        action: "Inspect Radar Layer",
        overlay: badge(<Sparkles className="size-3.5 text-teal-400" />, "SAR Deep Moisture"),
        image: getPublicUrl("/images/network_globe.jpg"),
        imageAlt: "Aerial view of geometric circular crop fields using pivot irrigation",
    },
];

export function SqueezeCarouselDemo(props: DemoProps) {
    const options = { ...settings, ...props };
    const containerRef = useRef<HTMLDivElement>(null);
    const [activeIndex, setActiveIndex] = useState(0);

    useEffect(() => {
        gsap.registerPlugin(ScrollTrigger);

        if (!containerRef.current) return;

        const st = ScrollTrigger.create({
            trigger: containerRef.current,
            start: "top 85%",
            end: "bottom 15%",
            onEnter: () => {
                gsap.fromTo(
                    containerRef.current,
                    { scale: 0.96, opacity: 0, y: 30 },
                    {
                        scale: 1,
                        opacity: 1,
                        y: 0,
                        duration: 0.8,
                        ease: "power3.out"
                    }
                );
            },
            onLeaveBack: () => {
                gsap.to(containerRef.current, {
                    scale: 0.98,
                    opacity: 0.9,
                    duration: 0.6
                });
            }
        });

        return () => st.kill();
    }, []);

    return (
        <div 
            ref={containerRef}
            className="w-full bg-slate-950/90 rounded-3xl border border-emerald-500/20 p-6 md:p-8 shadow-2xl backdrop-blur-xl transition-all duration-300 relative z-20 overflow-hidden"
        >
            {/* Top Glow Ambient Accent */}
            <div className="absolute -top-24 left-1/2 -translate-x-1/2 w-96 h-48 bg-emerald-500/10 blur-3xl pointer-events-none rounded-full" />

            <div className="mb-6 flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-emerald-500/10 pb-4 relative z-10">
                <div>
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono font-medium mb-2">
                        <Sparkles className="size-3.5 animate-pulse text-emerald-400" />
                        <span>Dynamic Squeeze Slat Carousel</span>
                    </div>
                    <h3 className="text-2xl md:text-3xl font-bold tracking-tight text-white">
                        Agri-SAGE Agronomic Intelligence Stack
                    </h3>
                </div>
                <div className="flex items-center gap-3">
                    <span className="text-xs font-mono text-emerald-400/90 bg-emerald-500/10 px-3 py-1.5 rounded-full border border-emerald-500/20">
                        Slide {activeIndex + 1} of {agriSlides.length}
                    </span>
                </div>
            </div>
            
            <SqueezeCarousel 
                slides={agriSlides} 
                label="Agri-SAGE Featured Intelligence" 
                accent="#10b981" 
                accentForeground="#022c22"
                onIndexChange={(idx) => setActiveIndex(idx)}
                {...options} 
            />
        </div>
    );
}

export default SqueezeCarouselDemo;

