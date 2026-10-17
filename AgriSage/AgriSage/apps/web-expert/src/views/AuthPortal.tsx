import React, { useState } from 'react';
import {
  Sprout,
  ShieldCheck,
  Smartphone,
  Lock,
  ArrowRight,
  ArrowLeft,
  CheckCircle2,
  Clock,
  UserCheck,
  Building,
  KeyRound,
  Globe,
  Sparkles,
  Fingerprint,
  Check,
  AlertCircle
} from 'lucide-react';
import { GlassTiltCard } from '../components/landing/GlassTiltCard';
import { ThreeHeroCanvas } from '../components/landing/ThreeHeroCanvas';
import { playHoverChime, playSuccessTone } from '../utils/audioFX';

interface AuthPortalProps {
  onLoginSuccess: (role: 'farmer' | 'expert') => void;
  onBackToLanding: () => void;
  lang: 'en' | 'ml';
  onToggleLang: () => void;
}

export const AuthPortal: React.FC<AuthPortalProps> = ({
  onLoginSuccess,
  onBackToLanding,
  lang,
  onToggleLang
}) => {
  const [role, setRole] = useState<'farmer' | 'expert'>('farmer');
  const [phone, setPhone] = useState('9847123456');
  const [otpSent, setOtpSent] = useState(false);
  const [otp, setOtp] = useState(['5', '2', '8', '1', '9', '4']);
  const [expertEmail, setExpertEmail] = useState('dr.nair@kau.in');
  const [expertPassword, setExpertPassword] = useState('••••••••••••');
  const [isBiometricScanning, setIsBiometricScanning] = useState(false);

  const handleSendOtp = (e: React.FormEvent) => {
    e.preventDefault();
    playSuccessTone();
    setOtpSent(true);
  };

  const handleVerifyOtp = (e: React.FormEvent) => {
    e.preventDefault();
    playSuccessTone();
    onLoginSuccess(role);
  };

  const handleExpertLogin = (e: React.FormEvent) => {
    e.preventDefault();
    playSuccessTone();
    onLoginSuccess('expert');
  };

  const handleBiometricAuth = () => {
    setIsBiometricScanning(true);
    playHoverChime(600);
    setTimeout(() => {
      setIsBiometricScanning(false);
      playSuccessTone();
      onLoginSuccess(role);
    }, 1200);
  };

  const fillDemoFarmer = () => {
    playHoverChime(500);
    setRole('farmer');
    setPhone('9847123456');
    setOtpSent(true);
    setOtp(['5', '2', '8', '1', '9', '4']);
  };

  const fillDemoExpert = () => {
    playHoverChime(550);
    setRole('expert');
    setExpertEmail('dr.nair@kau.in');
    setExpertPassword('••••••••••••');
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center px-4 py-12 relative overflow-hidden bg-slate-950 text-white selection:bg-emerald-500 selection:text-white snap-scroll-section is-active-snap">
      {/* 3D Particle Ambient Canvas Layer */}
      <ThreeHeroCanvas className="opacity-40" />

      {/* Atmospheric Radial Gradients */}
      <div className="absolute top-1/4 -left-32 w-96 h-96 bg-emerald-500/15 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 -right-32 w-96 h-96 bg-cyan-500/15 rounded-full blur-3xl pointer-events-none" />

      {/* Top Bar with Back Link */}
      <div className="st-layer-1 w-full max-w-lg flex items-center justify-between mb-6 z-20">
        <button
          type="button"
          onClick={() => {
            playHoverChime(400);
            onBackToLanding();
          }}
          className="flex items-center gap-2 text-xs font-mono font-bold text-white/70 hover:text-emerald-400 transition-colors bg-white/5 hover:bg-white/10 px-3.5 py-2 rounded-xl border border-white/10 backdrop-blur-md"
        >
          <ArrowLeft size={16} />
          <span>{lang === 'ml' ? 'തിരികെ ഫ്രെയിം 1 ലേക്ക്' : 'Back to Public 3D Journey (Frame 1)'}</span>
        </button>

        <button
          type="button"
          onClick={() => {
            playHoverChime(450);
            onToggleLang();
          }}
          className="flex items-center gap-1.5 text-xs font-mono font-bold text-white bg-white/5 hover:bg-white/10 px-3 py-2 rounded-xl border border-white/10 backdrop-blur-md shadow-xs transition-colors"
        >
          <Globe size={14} className="text-emerald-400" />
          <span>{lang === 'ml' ? 'മലയാളം' : 'English'}</span>
        </button>
      </div>

      {/* Main 3D Glass Authentication Card (Frame 2) */}
      <GlassTiltCard
        tiltMaxAngle={6}
        className="st-layer-2 w-full max-w-lg p-6 sm:p-9 space-y-7 shadow-2xl border-white/15 bg-slate-900/85 backdrop-blur-2xl relative z-20"
      >
        {/* Brand Header */}
        <div className="st-layer-3 text-center space-y-3">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-emerald-600 via-emerald-500 to-teal-400 text-white flex items-center justify-center mx-auto shadow-xl shadow-emerald-500/30 border border-emerald-300/40 hologram-float">
            <Sprout size={30} />
          </div>
          <div>
            <div className="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 text-[10px] font-mono font-bold uppercase tracking-widest mb-1">
              <ShieldCheck size={12} />
              <span>Frame 02 · Institutional Access Portal</span>
            </div>
            <h2 className="text-2xl font-black text-white tracking-tight">
              {lang === 'ml' ? 'അഗ്രി-സേജ് സുരക്ഷിത പ്രവേശനം' : 'Agri-SAGE Enterprise Sign-In'}
            </h2>
            <p className="text-xs text-white/70 max-w-sm mx-auto mt-1">
              {lang === 'ml' ? 'കർഷകർക്കും കാർഷിക ശാസ്ത്രജ്ഞർക്കുമുള്ള പോർട്ടൽ' : 'Decentralized cryptographic access for smallholders & KVK scientists'}
            </p>
          </div>
        </div>

        {/* Role Toggle Selector */}
        <div className="grid grid-cols-2 p-1.5 rounded-2xl bg-black/50 border border-white/10 text-xs font-mono font-bold">
          <button
            type="button"
            onClick={() => {
              playHoverChime(480);
              setRole('farmer');
              setOtpSent(false);
            }}
            className={`py-2.5 rounded-xl transition-all flex items-center justify-center gap-2 ${
              role === 'farmer'
                ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/30'
                : 'text-white/60 hover:text-white'
            }`}
          >
            <Smartphone size={16} />
            <span>{lang === 'ml' ? 'കർഷകൻ (OTP)' : 'Farmer (Phone OTP)'}</span>
          </button>

          <button
            type="button"
            onClick={() => {
              playHoverChime(520);
              setRole('expert');
            }}
            className={`py-2.5 rounded-xl transition-all flex items-center justify-center gap-2 ${
              role === 'expert'
                ? 'bg-cyan-500 text-white shadow-lg shadow-cyan-500/30'
                : 'text-white/60 hover:text-white'
            }`}
          >
            <Building size={16} />
            <span>{lang === 'ml' ? 'വിദഗ്ദ്ധൻ / KAU' : 'Agronomist (KVK ID)'}</span>
          </button>
        </div>

        {/* Quick Demo Pre-fill Badges */}
        <div className="flex items-center justify-between text-[11px] font-mono text-white/60 px-1">
          <span>Quick Evaluation Credentials:</span>
          <div className="flex gap-2">
            <button
              type="button"
              onClick={fillDemoFarmer}
              className="text-emerald-400 hover:text-emerald-300 font-bold underline"
            >
              Farmer OTP
            </button>
            <span>·</span>
            <button
              type="button"
              onClick={fillDemoExpert}
              className="text-cyan-400 hover:text-cyan-300 font-bold underline"
            >
              KVK Expert
            </button>
          </div>
        </div>

        {/* ROLE 1: FARMER PHONE OTP AUTH */}
        {role === 'farmer' && (
          !otpSent ? (
            <form onSubmit={handleSendOtp} className="space-y-4 animate-fade-in">
              <div>
                <label className="block text-xs font-mono font-bold text-white/90 mb-1.5">
                  {lang === 'ml' ? 'മൊബൈൽ നമ്പർ നൽകുക' : 'Smallholder Registered Mobile Number'}
                </label>
                <div className="flex items-center rounded-xl border border-white/20 bg-black/40 focus-within:border-emerald-400 transition-all overflow-hidden shadow-inner">
                  <span className="px-4 py-3 text-xs font-mono font-bold text-white/60 border-r border-white/10 bg-white/5">
                    +91
                  </span>
                  <input
                    type="tel"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    placeholder="98471 23456"
                    className="w-full px-4 py-3 text-sm font-mono font-bold bg-transparent text-white focus:outline-none placeholder:text-white/30"
                    required
                  />
                </div>
                <p className="text-[11px] text-white/50 mt-1.5 font-mono">
                  {lang === 'ml' ? '6 അക്ക പരിശോധനാ കോഡ് അയയ്ക്കും' : 'Offline-first sync via secure SMS gateway & USSD failover.'}
                </p>
              </div>

              <button
                type="submit"
                className="btn btn-primary w-full text-xs h-12 flex items-center justify-center gap-2 font-bold shadow-xl shadow-emerald-500/30"
              >
                <span>{lang === 'ml' ? 'OTP അയക്കുക' : 'Dispatch Verification OTP Code'}</span>
                <ArrowRight size={16} />
              </button>
            </form>
          ) : (
            <form onSubmit={handleVerifyOtp} className="space-y-4 animate-fade-in">
              <div className="space-y-3">
                <div className="flex items-center justify-between text-xs font-mono">
                  <span className="text-white/70">
                    Code dispatched to <strong>+91 {phone}</strong>
                  </span>
                  <button
                    type="button"
                    onClick={() => setOtpSent(false)}
                    className="text-emerald-400 font-bold hover:underline text-[11px]"
                  >
                    Edit Number
                  </button>
                </div>

                {/* 6-box OTP entry */}
                <div className="flex justify-between gap-2">
                  {otp.map((digit, idx) => (
                    <input
                      key={idx}
                      type="text"
                      maxLength={1}
                      value={digit}
                      onChange={(e) => {
                        const newOtp = [...otp];
                        newOtp[idx] = e.target.value;
                        setOtp(newOtp);
                      }}
                      className="w-12 h-14 text-center text-xl font-bold font-mono rounded-xl border border-white/20 bg-black/50 text-white focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/30 focus:outline-none"
                    />
                  ))}
                </div>

                <div className="flex items-center justify-between text-xs text-white/50 font-mono pt-1">
                  <span className="flex items-center gap-1.5 text-amber-300">
                    <Clock size={13} />
                    Expires in 04:42
                  </span>
                  <button
                    type="button"
                    onClick={() => playHoverChime(450)}
                    className="text-emerald-400 font-bold hover:underline"
                  >
                    Resend Code
                  </button>
                </div>
              </div>

              <button
                type="submit"
                className="btn btn-primary w-full text-xs h-12 flex items-center justify-center gap-2 font-bold shadow-xl shadow-emerald-500/30"
              >
                <CheckCircle2 size={16} />
                <span>{lang === 'ml' ? 'സ്ഥിരീകരിച്ച് പ്രവേശിക്കുക (Frame 3)' : 'Verify & Launch Workstation (Frame 3)'}</span>
              </button>
            </form>
          )
        )}

        {/* ROLE 2: AGRONOMIST KVK CREDENTIAL AUTH */}
        {role === 'expert' && (
          <form onSubmit={handleExpertLogin} className="space-y-4 animate-fade-in">
            <div>
              <label className="block text-xs font-mono font-bold text-white/90 mb-1">
                Institutional Email / ICAR-KVK ID
              </label>
              <input
                type="email"
                value={expertEmail}
                onChange={(e) => setExpertEmail(e.target.value)}
                className="w-full px-4 py-3 text-xs font-mono font-bold rounded-xl border border-white/20 bg-black/40 text-white focus:border-cyan-400 focus:outline-none"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-mono font-bold text-white/90 mb-1">
                Agronomist Cryptographic Key
              </label>
              <input
                type="password"
                value={expertPassword}
                onChange={(e) => setExpertPassword(e.target.value)}
                className="w-full px-4 py-3 text-xs font-mono font-bold rounded-xl border border-white/20 bg-black/40 text-white focus:border-cyan-400 focus:outline-none"
                required
              />
            </div>

            <button
              type="submit"
              className="btn w-full text-xs h-12 flex items-center justify-center gap-2 font-bold bg-cyan-500 hover:bg-cyan-400 text-slate-950 shadow-xl shadow-cyan-500/30"
            >
              <KeyRound size={16} />
              <span>Authenticate as KVK Agronomist (Frame 3)</span>
            </button>
          </form>
        )}

        {/* Biometric Passkey / WebAuthn Simulation */}
        <div className="pt-2 flex flex-col items-center gap-2">
          <button
            type="button"
            onClick={handleBiometricAuth}
            className={`w-full py-2.5 px-4 rounded-xl border border-white/15 bg-white/5 hover:bg-white/10 text-xs font-mono font-bold flex items-center justify-center gap-2 transition-all ${
              isBiometricScanning ? 'border-emerald-400 text-emerald-400' : 'text-white/80'
            }`}
          >
            <Fingerprint size={16} className={isBiometricScanning ? 'animate-pulse text-emerald-400' : ''} />
            <span>{isBiometricScanning ? 'Verifying Hardware Passkey...' : 'Sign in with Biometric Passkey (FIDO2)'}</span>
          </button>
        </div>

        {/* Direct Bypass CTA for Instant Workstation Launch */}
        <div className="pt-3 border-t border-white/10 flex items-center justify-between text-xs font-mono">
          <span className="text-white/50">Developer Fast-Path:</span>
          <button
            type="button"
            onClick={() => {
              playSuccessTone();
              onLoginSuccess('expert');
            }}
            className="text-emerald-400 hover:text-emerald-300 font-bold flex items-center gap-1.5 transition-colors"
          >
            <Sparkles size={14} />
            <span>Instant Demo Bypass ➔ Frame 3</span>
          </button>
        </div>

        {/* Security Credentials Footer */}
        <div className="text-[10px] font-mono text-center text-white/40 pt-1 flex items-center justify-center gap-2">
          <ShieldCheck size={12} className="text-emerald-400" />
          <span>256-bit AES · ICAR / CIB&RC Certified Platform</span>
        </div>
      </GlassTiltCard>
    </div>
  );
};
