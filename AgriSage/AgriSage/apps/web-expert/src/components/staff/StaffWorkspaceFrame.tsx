import { Link, useLocation } from 'react-router-dom';
import type { ReactNode } from 'react';
import { ExternalLink, LogOut, Sprout } from 'lucide-react';
import { getRoleLabel } from '../../auth/session';
import type { PortalSession } from '../../auth/session';
import '../../styles/staff.css';

interface StaffWorkspaceFrameProps {
  session: PortalSession;
  onSignOut: () => void;
  children: ReactNode;
}

export function StaffWorkspaceFrame({ session, onSignOut, children }: StaffWorkspaceFrameProps) {
  const location = useLocation();
  const isQueueActive = location.pathname === '/dashboard' || location.pathname.startsWith('/review/');

  return (
    <div className="staff-frame">
      <a className="staff-skip-link" href="#staff-main">Skip to workspace content</a>

      <header className="staff-frame-topbar">
        <Link to="/operations" className="staff-frame-brand" aria-label="Open Agri-SAGE operations console">
          <span className="staff-frame-brand-mark" aria-hidden="true"><Sprout size={18} /></span>
          <span><strong>Agri-SAGE</strong><small>Staff workspace</small></span>
        </Link>

        <nav className="staff-frame-nav" aria-label="Staff workspace navigation">
          <Link to="/operations" className={!isQueueActive ? 'staff-frame-nav-link--active' : ''}>Operations</Link>
          <Link to="/dashboard" className={isQueueActive ? 'staff-frame-nav-link--active' : ''}>Review queue</Link>
        </nav>

        <div className="staff-frame-user">
          <div className="staff-frame-user-copy">
            <strong>{session.displayName}</strong>
             <span>{getRoleLabel(session.role)} · {session.mode === 'backend' ? 'live' : 'demo'}</span>
          </div>
          <button type="button" className="staff-frame-signout" onClick={onSignOut}>
            <LogOut size={16} aria-hidden="true" />
            <span>Sign out</span>
          </button>
          <Link to="/" className="staff-frame-public" aria-label="Open public Agri-SAGE experience" title="Public experience">
            <ExternalLink size={16} aria-hidden="true" />
          </Link>
        </div>
      </header>

      <main id="staff-main" className="staff-frame-main" tabIndex={-1}>
        {children}
      </main>
    </div>
  );
}
