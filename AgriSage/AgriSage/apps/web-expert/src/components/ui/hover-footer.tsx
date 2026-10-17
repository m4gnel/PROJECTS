"use client";
import React, { useRef, useEffect, useState } from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import {
  Mail,
  Phone,
  MapPin,
  Globe,
  Sprout,
  Share2,
  Radio,
  MessageSquare,
  ShieldCheck
} from "lucide-react";

export const TextHoverEffect = ({
  text,
  duration,
  className,
}: {
  text: string;
  duration?: number;
  automatic?: boolean;
  className?: string;
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [cursor, setCursor] = useState({ x: 0, y: 0 });
  const [hovered, setHovered] = useState(false);
  const [maskPosition, setMaskPosition] = useState({ cx: "50%", cy: "50%" });

  useEffect(() => {
    if (svgRef.current && cursor.x !== null && cursor.y !== null) {
      const svgRect = svgRef.current.getBoundingClientRect();
      const cxPercentage = ((cursor.x - svgRect.left) / svgRect.width) * 100;
      const cyPercentage = ((cursor.y - svgRect.top) / svgRect.height) * 100;
      setMaskPosition({
        cx: `${cxPercentage}%`,
        cy: `${cyPercentage}%`,
      });
    }
  }, [cursor]);

  const renderTextWithAnchor = (txt: string) => {
    if (txt === "AGRI-SAGE") {
      return (
        <>
          AGR<tspan id="footer-agri-i-anchor">I</tspan>-SAGE
        </>
      );
    }
    return txt;
  };

  return (
    <svg
      ref={svgRef}
      width="100%"
      height="100%"
      viewBox="0 0 300 100"
      xmlns="http://www.w3.org/2000/svg"
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      onMouseMove={(e) => setCursor({ x: e.clientX, y: e.clientY })}
      className={cn("select-none uppercase cursor-pointer", className)}
    >
      <defs>
        <linearGradient
          id="textGradient"
          gradientUnits="userSpaceOnUse"
          cx="50%"
          cy="50%"
          r="25%"
        >
          {hovered && (
            <>
              <stop offset="0%" stopColor="#10b981" />
              <stop offset="25%" stopColor="#14b8a6" />
              <stop offset="50%" stopColor="#06b6d4" />
              <stop offset="75%" stopColor="#3b82f6" />
              <stop offset="100%" stopColor="#a855f7" />
            </>
          )}
        </linearGradient>

        <motion.radialGradient
          id="revealMask"
          gradientUnits="userSpaceOnUse"
          r="20%"
          initial={{ cx: "50%", cy: "50%" }}
          animate={maskPosition}
          transition={{ duration: duration ?? 0, ease: "easeOut" }}
        >
          <stop offset="0%" stopColor="white" />
          <stop offset="100%" stopColor="black" />
        </motion.radialGradient>
        <mask id="textMask">
          <rect
            x="0"
            y="0"
            width="100%"
            height="100%"
            fill="url(#revealMask)"
          />
        </mask>
      </defs>
      <text
        x="50%"
        y="50%"
        textAnchor="middle"
        dominantBaseline="middle"
        strokeWidth="0.3"
        className="fill-transparent stroke-slate-700 font-[helvetica] text-[52.5px] font-black dark:stroke-slate-800"
        style={{ opacity: hovered ? 0.7 : 0 }}
      >
        {renderTextWithAnchor(text)}
      </text>
      <motion.text
        x="50%"
        y="50%"
        textAnchor="middle"
        dominantBaseline="middle"
        strokeWidth="0.3"
        className="fill-transparent stroke-[#10b981] font-[helvetica] text-[52.5px] font-black 
        dark:stroke-[#10b98199]"
        initial={{ strokeDashoffset: 1000, strokeDasharray: 1000 }}
        animate={{
          strokeDashoffset: 0,
          strokeDasharray: 1000,
        }}
        transition={{
          duration: 4,
          ease: "easeInOut",
        }}
      >
        {renderTextWithAnchor(text)}
      </motion.text>
      <text
        x="50%"
        y="50%"
        textAnchor="middle"
        dominantBaseline="middle"
        stroke="url(#textGradient)"
        strokeWidth="0.3"
        mask="url(#textMask)"
        className="fill-transparent font-[helvetica] text-[52.5px] font-black"
      >
        {renderTextWithAnchor(text)}
      </text>
    </svg>
  );
};

export const FooterBackgroundGradient = () => {
  return (
    <div
      className="absolute inset-0 z-0 pointer-events-none"
      style={{
        background:
          "radial-gradient(125% 125% at 50% 10%, #02061799 40%, #064e3b44 100%)",
      }}
    />
  );
};

export function HoverFooter() {
  const footerLinks = [
    {
      title: "Platform Architecture",
      links: [
        { label: "Space to Soil Ingestion", href: "#" },
        { label: "Neural Core AI (DSSAT v4.8)", href: "#" },
        { label: "Multi-Agent Swarm", href: "#" },
        { label: "Outbreak Radar Sweep", href: "#" },
      ],
    },
    {
      title: "Agronomic Safety",
      links: [
        { label: "CIB&RC Regulatory Filter", href: "#" },
        { label: "Zero-Hallucination Gate", href: "#" },
        { label: "Malayalam Voice Advisory", href: "#" },
        {
          label: "Live Telemetry Triage",
          href: "#",
          pulse: true,
        },
      ],
    },
  ];

  const contactInfo = [
    {
      icon: <Mail size={18} className="text-[#10b981]" />,
      text: "advisory@agrisage.org",
      href: "mailto:advisory@agrisage.org",
    },
    {
      icon: <Phone size={18} className="text-[#10b981]" />,
      text: "+91 94000 12345 (Agri Hotline)",
      href: "tel:+919400012345",
    },
    {
      icon: <MapPin size={18} className="text-[#10b981]" />,
      text: "Palakkad & Wayanad, Kerala, India",
    },
  ];

  const socialLinks = [
    { icon: <Globe size={20} />, label: "Global Network", href: "#" },
    { icon: <Share2 size={20} />, label: "Share Platform", href: "#" },
    { icon: <Radio size={20} />, label: "Telemetry Stream", href: "#" },
    { icon: <MessageSquare size={20} />, label: "Farmer Advisory", href: "#" },
    { icon: <ShieldCheck size={20} />, label: "Safety Registry", href: "#" },
  ];

  return (
    <footer className="bg-slate-950/90 border border-emerald-500/20 relative h-fit rounded-3xl overflow-hidden my-8 mx-4 md:mx-10 shadow-2xl backdrop-blur-2xl">
      <div className="max-w-7xl mx-auto p-8 md:p-14 z-40 relative">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 md:gap-8 lg:gap-16 pb-12">
          {/* Brand section */}
          <div className="flex flex-col space-y-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-emerald-600 via-emerald-500 to-teal-400 text-white flex items-center justify-center shadow-lg shadow-emerald-500/30 border border-emerald-300/40">
                <Sprout size={22} />
              </div>
              <span className="text-white text-2xl font-black tracking-tight">Agri-SAGE</span>
            </div>
            <p className="text-sm text-slate-400 leading-relaxed">
              Scalable Agricultural Guidance Engine empowering smallholder farmers, agronomists, and institutions with verifiable biophysical AI intelligence.
            </p>
          </div>

          {/* Footer link sections */}
          {footerLinks.map((section) => (
            <div key={section.title}>
              <h4 className="text-white text-base font-bold tracking-wide uppercase font-mono mb-6 text-emerald-400">
                {section.title}
              </h4>
              <ul className="space-y-3 text-sm">
                {section.links.map((link) => (
                  <li key={link.label} className="relative">
                    <a
                      href={link.href}
                      className="text-slate-300 hover:text-emerald-400 transition-colors"
                    >
                      {link.label}
                    </a>
                    {link.pulse && (
                      <span className="absolute top-1.5 right-[-14px] w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ))}

          {/* Contact section */}
          <div>
            <h4 className="text-white text-base font-bold tracking-wide uppercase font-mono mb-6 text-emerald-400">
              Contact & Dispatch
            </h4>
            <ul className="space-y-4 text-sm text-slate-300">
              {contactInfo.map((item, i) => (
                <li key={i} className="flex items-center space-x-3">
                  {item.icon}
                  {item.href ? (
                    <a
                      href={item.href}
                      className="hover:text-emerald-400 transition-colors"
                    >
                      {item.text}
                    </a>
                  ) : (
                    <span className="hover:text-emerald-400 transition-colors">
                      {item.text}
                    </span>
                  )}
                </li>
              ))}
            </ul>
          </div>
        </div>

        <hr className="border-t border-slate-800 my-8 -translate-y-20 relative z-40" />

        {/* Footer bottom */}
        <div className="flex flex-col md:flex-row justify-between items-center text-sm text-slate-400 space-y-4 md:space-y-0 font-mono -translate-y-20 relative z-40">
          {/* Social icons */}
          <div className="flex space-x-6 text-slate-400">
            {socialLinks.map(({ icon, label, href }) => (
              <a
                key={label}
                href={href}
                aria-label={label}
                className="hover:text-emerald-400 transition-colors"
              >
                {icon}
              </a>
            ))}
          </div>

          {/* Copyright */}
          <p className="text-center md:text-left text-xs">
            &copy; {new Date().getFullYear()} Agri-SAGE Intelligence System. All rights reserved.
          </p>
        </div>
      </div>

      {/* Text hover effect */}
      <div id="footer-text-hover-container" className="lg:flex hidden h-[22.75rem] -mt-36 -mb-24">
        <TextHoverEffect text="AGRI-SAGE" className="z-30" />
      </div>

      <FooterBackgroundGradient />
    </footer>
  );
}

export default HoverFooter;
