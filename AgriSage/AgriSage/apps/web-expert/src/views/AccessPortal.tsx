import { useState } from 'react';
import type { FormEvent } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import {
  ArrowLeft,
  ArrowRight,
  Building2,
  Check,
  ChevronRight,
  CircleHelp,
  Eye,
  EyeOff,
  Globe,
  KeyRound,
  LockKeyhole,
  Mail,
  Moon,
  Phone,
  ShieldCheck,
  Sprout,
  Sun,
  UserRound,
  UserRoundPlus,
} from 'lucide-react';
import { isDemoAuthEnabled, isPortalRole } from '../auth/session';
import type { PortalRole, PortalSession } from '../auth/session';
import { ApiError, apiConfigurationError, isLiveApiConfigured, sendOtp, verifyOtp } from '../api/client';
import '../styles/access.css';

type AccessMode = 'login' | 'signup';
type AccessRole = 'farmer' | 'employee';
type Theme = 'dark' | 'light';

interface AccessPortalProps {
  onAuthenticated: (session: PortalSession) => void;
  onBackToLanding: () => void;
  lang: 'en' | 'ml';
  onToggleLang: () => void;
  theme: Theme;
  onToggleTheme: () => void;
}

const DEMO_OTP = '528194';

const roleCopy: Record<AccessRole, { label: string; title: string; detail: string; destination: string }> = {
  farmer: {
    label: 'Farmer / user',
    title: 'Farmer workspace',
    detail: 'Get crop guidance, evidence, and practical next steps for your farm.',
    destination: 'Advisory sandbox',
  },
  employee: {
    label: 'Employee / officer',
    title: 'Operations workspace',
    detail: 'Triage cases, review regional risk, and coordinate the field team.',
    destination: 'Operations console',
  },
};

const getDisplayName = (value: string, fallback: string) => {
  const name = value.trim();
  if (name) return name;
  const [localPart] = fallback.split('@');
  return localPart ? localPart.replace(/[._-]+/g, ' ') : 'Agri-SAGE member';
};

const makeDemoSession = (role: AccessRole, displayName: string, identifier: string): PortalSession => ({
  role: role as PortalRole,
  displayName: getDisplayName(displayName, identifier),
  identifier,
  mode: 'demo',
  signedInAt: new Date().toISOString(),
});

function AccessRoleCard({ role, selected, onSelect }: { role: AccessRole; selected: boolean; onSelect: () => void }) {
  const copy = roleCopy[role];
  const Icon = role === 'farmer' ? UserRound : Building2;

  return (
    <button
      type="button"
      className={`access-role-card${selected ? ' access-role-card--selected' : ''}`}
      onClick={onSelect}
      aria-pressed={selected}
    >
      <span className="access-role-icon" aria-hidden="true">
        <Icon size={19} />
      </span>
      <span className="access-role-copy">
        <strong>{copy.label}</strong>
        <span>{copy.destination}</span>
      </span>
      <span className="access-role-check" aria-hidden="true">
        {selected ? <Check size={15} /> : <ChevronRight size={15} />}
      </span>
    </button>
  );
}

export function AccessPortal({
  onAuthenticated,
  onBackToLanding,
  lang,
  onToggleLang,
  theme,
  onToggleTheme,
}: AccessPortalProps) {
  const [searchParams] = useSearchParams();
  const initialMode: AccessMode = searchParams.get('mode') === 'signup' ? 'signup' : 'login';
  const initialRole: AccessRole = searchParams.get('role') === 'employee' ? 'employee' : 'farmer';

  const [mode, setMode] = useState<AccessMode>(initialMode);
  const [role, setRole] = useState<AccessRole>(initialRole);
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [workEmail, setWorkEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [fullName, setFullName] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [inviteCode, setInviteCode] = useState('');
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const selectedRoleCopy = roleCopy[role];
  const isSignup = mode === 'signup';
  const liveAuth = isLiveApiConfigured;
  const demoAuth = isDemoAuthEnabled;
  const authUnavailable = !liveAuth && !demoAuth;
  const usesPhoneAuth = liveAuth || role === 'farmer';

  const switchMode = (nextMode: AccessMode) => {
    setMode(nextMode);
    setError('');
    setNotice('');
    setOtpSent(false);
    setOtp('');
  };

  const selectRole = (nextRole: AccessRole) => {
    setRole(nextRole);
    setError('');
    setNotice('');
    setOtpSent(false);
    setOtp('');
  };

  const startDemoSession = (session: PortalSession) => {
    setNotice('Demo session ready. No account, credential, or OTP was sent to a server.');
    window.setTimeout(() => onAuthenticated(session), 180);
  };

  const startBackendSession = (response: Awaited<ReturnType<typeof verifyOtp>>) => {
    const serverUser = response.user;
    if (
      !serverUser ||
      !isPortalRole(serverUser.role) ||
      typeof serverUser.id !== 'string' ||
      typeof serverUser.phone !== 'string' ||
      !serverUser.id ||
      !serverUser.phone
    ) {
      setError('The authentication service returned no user authorization state.');
      return;
    }

    if (role === 'employee' && serverUser.role === 'farmer') {
      setError('This account is not provisioned for the employee or officer workspace. Ask your administrator to grant staff access.');
      return;
    }

    const serverName = typeof serverUser.name === 'string' ? serverUser.name.trim() : '';
    const session: PortalSession = {
      role: serverUser.role,
      displayName: serverName || fullName.trim() || serverUser.phone,
      identifier: serverUser.phone,
      mode: 'backend',
      signedInAt: new Date().toISOString(),
      accessToken: response.access_token,
      refreshToken: response.refresh_token,
      userId: serverUser.id,
    };
    setNotice('Authenticated by the Agri-SAGE backend. Loading your server-authorized workspace…');
    window.setTimeout(() => onAuthenticated(session), 180);
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError('');
    setNotice('');

    if (authUnavailable) {
      setError('Authentication is not configured for this deployment. Set VITE_API_BASE_URL and rebuild before inviting users.');
      return;
    }

    const cleanPhone = phone.replace(/\D/g, '');
    const cleanEmail = workEmail.trim().toLowerCase();

    if (liveAuth) {
      if (isSignup && fullName.trim().length < 2) {
        setError('Enter your full name so the backend can create the farmer profile.');
        return;
      }

      if (cleanPhone.length !== 10) {
        setError('Enter a valid 10-digit mobile number for backend OTP authentication.');
        return;
      }

      setIsSubmitting(true);
      try {
        const phoneNumber = `+91${cleanPhone}`;
        if (!otpSent) {
          const result = await sendOtp(phoneNumber);
          setOtpSent(true);
          setOtp('');
          setNotice(`${result.message}. Check the configured delivery channel, then enter the 6-digit code.`);
          return;
        }

        if (!/^\d{6}$/.test(otp)) {
          setError('Enter the 6-digit verification code.');
          return;
        }

        const response = await verifyOtp(phoneNumber, otp, fullName.trim() || undefined);
        startBackendSession(response);
      } catch (caughtError) {
        const message = caughtError instanceof ApiError
          ? caughtError.message
          : 'The authentication service could not complete this request.';
        setError(message);
      } finally {
        setIsSubmitting(false);
      }
      return;
    }

    if (isSignup) {
      if (fullName.trim().length < 2) {
        setError('Enter your full name so the workspace can identify your session.');
        return;
      }

      if (role === 'farmer' && cleanPhone.length !== 10) {
        setError('Enter a valid 10-digit mobile number for the farmer profile.');
        return;
      }

      if (role === 'employee' && !cleanEmail.includes('@')) {
        setError('Enter a valid work email for the employee profile.');
        return;
      }

      if (role === 'employee' && inviteCode.trim().length < 4) {
        setError('Enter the employee invite code supplied by your team administrator.');
        return;
      }

      if (password.length < 8) {
        setError('Use a password with at least 8 characters.');
        return;
      }

      if (password !== confirmPassword) {
        setError('The passwords do not match.');
        return;
      }

      startDemoSession(makeDemoSession(role, fullName, role === 'farmer' ? `+91${cleanPhone}` : cleanEmail));
      return;
    }

    if (role === 'farmer') {
      if (cleanPhone.length !== 10) {
        setError('Enter a valid 10-digit mobile number to request a verification code.');
        return;
      }

      if (!otpSent) {
        setOtpSent(true);
        setOtp('');
        setNotice(`Demo verification code: ${DEMO_OTP}. No SMS was sent.`);
        return;
      }

      if (!/^\d{6}$/.test(otp)) {
        setError('Enter the 6-digit verification code.');
        return;
      }

      if (otp !== DEMO_OTP) {
        setError('That demo code does not match. Use 528194 for this local preview.');
        return;
      }

       startDemoSession(makeDemoSession('farmer', 'Farmer demo', `+91${cleanPhone}`));
      return;
    }

    if (!cleanEmail.includes('@')) {
      setError('Enter your work email address.');
      return;
    }

    if (password.length < 6) {
      setError('Enter the employee demo password, or at least 6 characters.');
      return;
    }

    startDemoSession(makeDemoSession('employee', getDisplayName('', cleanEmail), cleanEmail));
  };

  const loadFarmerDemo = () => {
    setMode('login');
    setRole('farmer');
    setPhone('9847123456');
    setOtp(DEMO_OTP);
    setOtpSent(true);
    setError('');
    setNotice('Farmer demo loaded. Use the prefilled code to open the advisory sandbox.');
  };

  const loadEmployeeDemo = () => {
    setMode('login');
    setRole('employee');
    setWorkEmail('ops@agrisage.demo');
    setPassword('demo-access');
    setError('');
    setNotice('Employee demo loaded. This opens the local operations console.');
  };

  return (
    <div className="access-portal">
      <a className="access-skip-link" href="#access-form">Skip to access form</a>

      <header className="access-topbar">
        <button type="button" className="access-back-button" onClick={onBackToLanding} aria-label="Back to public Agri-SAGE home">
          <ArrowLeft size={17} aria-hidden="true" />
          <span>Back to Agri-SAGE</span>
        </button>

        <Link to="/" className="access-brand" aria-label="Agri-SAGE public home">
          <span className="access-brand-mark" aria-hidden="true"><Sprout size={19} /></span>
          <span><strong>Agri-SAGE</strong><small>Scalable Agricultural Guidance Engine</small></span>
        </Link>

        <div className="access-top-actions">
          <button type="button" className="access-utility-button" onClick={onToggleTheme} aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}>
            {theme === 'dark' ? <Sun size={17} aria-hidden="true" /> : <Moon size={17} aria-hidden="true" />}
          </button>
          <button type="button" className="access-language-button" onClick={onToggleLang} aria-label={`Switch language. Current language: ${lang === 'ml' ? 'Malayalam' : 'English'}`}>
            <Globe size={15} aria-hidden="true" />
            <span>{lang === 'ml' ? 'മലയാളം' : 'English'}</span>
          </button>
        </div>
      </header>

      <main className="access-main">
        <section className="access-context" aria-labelledby="access-title">
          <div className="access-kicker"><ShieldCheck size={15} aria-hidden="true" /> Role-aware access</div>
          <h1 id="access-title">The right workspace for the work you do.</h1>
          <p>
            Agri-SAGE keeps farmer guidance and field operations connected, while giving each person only the tools
            they need for the next decision.
          </p>

          <div className="access-route-map" aria-label="Workspace destinations">
            <div className={`access-route-card${role === 'farmer' ? ' access-route-card--active' : ''}`}>
              <span className="access-route-icon" aria-hidden="true"><UserRound size={17} /></span>
              <div><strong>Farmer / user</strong><span>Advisory sandbox</span></div>
              <ArrowRight size={15} aria-hidden="true" />
            </div>
            <div className={`access-route-card${role === 'employee' ? ' access-route-card--active' : ''}`}>
              <span className="access-route-icon" aria-hidden="true"><Building2 size={17} /></span>
              <div><strong>Employee / officer</strong><span>Operations console</span></div>
              <ArrowRight size={15} aria-hidden="true" />
            </div>
          </div>

          <div className="access-value-list">
            <div><Check size={16} aria-hidden="true" /><span>Clear role-based destinations after access</span></div>
            <div><Check size={16} aria-hidden="true" /><span>One consistent workspace across screen sizes</span></div>
            <div><Check size={16} aria-hidden="true" /><span>Demo boundaries are visible instead of implied</span></div>
          </div>
        </section>

        <section className="access-card" aria-labelledby="access-card-title">
          <div className="access-card-header">
            <div>
              <span className="access-card-kicker">Agri-SAGE access</span>
              <h2 id="access-card-title">{isSignup ? 'Create your workspace profile' : 'Welcome back'}</h2>
              <p>{selectedRoleCopy.detail}</p>
            </div>
             <div className="access-preview-badge">
               {liveAuth ? <ShieldCheck size={14} aria-hidden="true" /> : <CircleHelp size={14} aria-hidden="true" />}
               {liveAuth ? 'Backend auth' : demoAuth ? 'Preview mode' : 'Auth not configured'}
             </div>
          </div>

          <div className="access-mode-tabs" role="tablist" aria-label="Access mode">
            <button type="button" role="tab" aria-selected={!isSignup} className={!isSignup ? 'access-mode-tab--active' : ''} onClick={() => switchMode('login')}>
              Log in
            </button>
            <button type="button" role="tab" aria-selected={isSignup} className={isSignup ? 'access-mode-tab--active' : ''} onClick={() => switchMode('signup')}>
              Sign up
            </button>
          </div>

          <div className="access-role-grid" aria-label="Choose your role">
            <AccessRoleCard role="farmer" selected={role === 'farmer'} onSelect={() => selectRole('farmer')} />
            <AccessRoleCard role="employee" selected={role === 'employee'} onSelect={() => selectRole('employee')} />
          </div>

           {!liveAuth && demoAuth && (
             <div className="access-demo-actions" aria-label="Demo shortcuts">
               <span>Quick preview</span>
               <button type="button" onClick={loadFarmerDemo}>Farmer demo</button>
               <button type="button" onClick={loadEmployeeDemo}>Employee demo</button>
             </div>
           )}

           {apiConfigurationError && (
             <div className="access-message access-message--error" role="alert">
               {apiConfigurationError} Update the public API setting and rebuild this site.
             </div>
           )}

           {authUnavailable && (
             <div className="access-message access-message--error" role="alert">
               This production build has no authentication provider configured. Contact the deployment owner; local preview credentials are disabled here.
             </div>
           )}

            <form id="access-form" className="access-form" onSubmit={handleSubmit} noValidate aria-disabled={authUnavailable} aria-busy={isSubmitting}>
            {isSignup && (
              <label className="access-field">
                <span>Full name</span>
                <div className="access-input-wrap">
                  <UserRound size={17} aria-hidden="true" />
                  <input value={fullName} onChange={(event) => setFullName(event.target.value)} autoComplete="name" placeholder="e.g. Anjali Menon" />
                </div>
              </label>
            )}

             {usesPhoneAuth ? (
               <label className="access-field">
                 <span>Mobile number</span>
                <div className="access-input-wrap">
                  <Phone size={17} aria-hidden="true" />
                  <span className="access-country-code">+91</span>
                  <input value={phone} onChange={(event) => setPhone(event.target.value)} type="tel" inputMode="tel" autoComplete="tel" placeholder="98471 23456" />
                </div>
                 <small>
                   {liveAuth
                     ? 'A one-time code is sent through the configured backend delivery provider.'
                     : isSignup
                       ? 'Used to identify the farmer profile in the future backend connection.'
                       : 'We will use an OTP when live delivery is connected.'}
                 </small>
               </label>
            ) : (
              <label className="access-field">
                <span>Work email</span>
                <div className="access-input-wrap">
                  <Mail size={17} aria-hidden="true" />
                  <input value={workEmail} onChange={(event) => setWorkEmail(event.target.value)} type="email" autoComplete="email" placeholder="you@organisation.org" />
                </div>
              </label>
            )}

             {isSignup && role === 'employee' && !liveAuth && demoAuth && (
              <label className="access-field">
                <span>Employee invite code</span>
                <div className="access-input-wrap">
                  <KeyRound size={17} aria-hidden="true" />
                  <input value={inviteCode} onChange={(event) => setInviteCode(event.target.value)} autoComplete="off" placeholder="Provided by your team admin" />
                </div>
              </label>
            )}

             {usesPhoneAuth && otpSent ? (
              <label className="access-field">
                <span>6-digit verification code</span>
                <div className="access-input-wrap">
                  <LockKeyhole size={17} aria-hidden="true" />
                  <input value={otp} onChange={(event) => setOtp(event.target.value.replace(/\D/g, '').slice(0, 6))} inputMode="numeric" autoComplete="one-time-code" placeholder="528194" maxLength={6} />
                </div>
                 <small>{liveAuth ? 'Enter the code delivered by the configured backend provider.' : 'Local preview code: 528194. No SMS was sent.'}</small>
               </label>
             ) : (
                !liveAuth && demoAuth && (role === 'employee' || isSignup) && (
                <label className="access-field">
                  <span>{isSignup ? 'Create password' : 'Password'}</span>
                  <div className="access-input-wrap">
                    <LockKeyhole size={17} aria-hidden="true" />
                    <input value={password} onChange={(event) => setPassword(event.target.value)} type={showPassword ? 'text' : 'password'} autoComplete={isSignup ? 'new-password' : 'current-password'} placeholder={isSignup ? 'At least 8 characters' : 'Enter your password'} />
                    <button type="button" className="access-input-action" onClick={() => setShowPassword((visible) => !visible)} aria-label={showPassword ? 'Hide password' : 'Show password'}>
                      {showPassword ? <EyeOff size={17} aria-hidden="true" /> : <Eye size={17} aria-hidden="true" />}
                    </button>
                  </div>
                </label>
              )
            )}

             {isSignup && !liveAuth && demoAuth && (
              <label className="access-field">
                <span>Confirm password</span>
                <div className="access-input-wrap">
                  <LockKeyhole size={17} aria-hidden="true" />
                  <input value={confirmPassword} onChange={(event) => setConfirmPassword(event.target.value)} type={showPassword ? 'text' : 'password'} autoComplete="new-password" placeholder="Repeat your password" />
                </div>
              </label>
            )}

            {error && <div className="access-message access-message--error" role="alert">{error}</div>}
            {notice && <div className="access-message access-message--notice" role="status" aria-live="polite">{notice}</div>}

             <button type="submit" className="access-submit-button" disabled={isSubmitting || authUnavailable}>
               {liveAuth && !otpSent ? <Phone size={17} aria-hidden="true" /> : isSignup && !liveAuth && demoAuth ? <UserRoundPlus size={17} aria-hidden="true" /> : <ArrowRight size={17} aria-hidden="true" />}
               <span>
                 {isSubmitting
                   ? 'Contacting authentication service…'
                   : liveAuth && !otpSent
                     ? 'Send backend OTP'
                      : liveAuth
                        ? 'Continue to workspace'
                        : authUnavailable
                          ? 'Authentication unavailable'
                          : isSignup
                            ? 'Create demo profile'
                            : role === 'farmer' && !otpSent
                              ? 'Send demo OTP'
                              : 'Continue to workspace'}
               </span>
             </button>
          </form>

          <div className="access-card-footer">
            <ShieldCheck size={15} aria-hidden="true" />
             <span>
               {liveAuth
                 ? 'Role and permissions come from the authenticated backend account. Staff access must be provisioned server-side.'
                  : demoAuth
                    ? 'Role-aware preview only — set VITE_API_BASE_URL to enable backend authentication.'
                    : 'Demo sign-in is disabled in this build. Set VITE_API_BASE_URL to enable backend authentication.'}
             </span>
          </div>
        </section>
      </main>
    </div>
  );
}
