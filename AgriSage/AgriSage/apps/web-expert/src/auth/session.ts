export type PortalRole = 'farmer' | 'employee' | 'officer' | 'expert';

export interface PortalSession {
  role: PortalRole;
  displayName: string;
  identifier: string;
  mode: 'demo' | 'backend';
  signedInAt: string;
  accessToken?: string;
  refreshToken?: string;
  userId?: string;
}

const SESSION_STORAGE_KEY = 'agrisage_portal_session';

export const isDemoAuthEnabled =
  import.meta.env.DEV || import.meta.env.VITE_ENABLE_DEMO_AUTH === 'true';

export const isPortalRole = (value: unknown): value is PortalRole =>
  value === 'farmer' || value === 'employee' || value === 'officer' || value === 'expert';

const isNonEmptyString = (value: unknown): value is string =>
  typeof value === 'string' && value.trim().length > 0;

const isPortalSession = (value: unknown): value is PortalSession => {
  if (!value || typeof value !== 'object') return false;

  const session = value as Partial<PortalSession>;
  return (
    isPortalRole(session.role) &&
    isNonEmptyString(session.displayName) &&
    isNonEmptyString(session.identifier) &&
    (session.mode === 'demo' || session.mode === 'backend') &&
    isNonEmptyString(session.signedInAt) &&
    (session.mode === 'demo' || (isNonEmptyString(session.accessToken) && isNonEmptyString(session.refreshToken)))
  );
};

type SessionReadOptions = {
  allowDemo?: boolean;
  allowBackend?: boolean;
};

const removeStoredSession = (storage: Storage) => {
  try {
    storage.removeItem(SESSION_STORAGE_KEY);
  } catch {
    // Storage can be unavailable in private browsing or with a restrictive policy.
  }
};

export const readPortalSession = ({
  allowDemo = isDemoAuthEnabled,
  allowBackend = true,
}: SessionReadOptions = {}): PortalSession | null => {
  if (typeof window === 'undefined') return null;

  const storages: Storage[] = [];
  try {
    storages.push(window.sessionStorage);
  } catch {
    // Continue with the other storage area.
  }
  try {
    storages.push(window.localStorage);
  } catch {
    // Continue with the storage areas that are available.
  }

  for (const storage of storages) {
    let stored: string | null = null;
    try {
      stored = storage.getItem(SESSION_STORAGE_KEY);
    } catch {
      continue;
    }
    if (!stored) continue;

    try {
      const parsed: unknown = JSON.parse(stored);
      if (!isPortalSession(parsed)) {
        removeStoredSession(storage);
        continue;
      }
      if (parsed.mode === 'demo' && !allowDemo) {
        // Never let a seeded session survive into a production build by accident.
        removeStoredSession(storage);
        continue;
      }
      if (parsed.mode === 'backend' && !allowBackend) {
        removeStoredSession(storage);
        continue;
      }
      return parsed;
    } catch {
      removeStoredSession(storage);
    }
  }

  return null;
};

export const savePortalSession = (session: PortalSession) => {
  if (typeof window === 'undefined') return;

  if (session.mode === 'demo' && !isDemoAuthEnabled) {
    clearPortalSession();
    return;
  }

  const serialized = JSON.stringify(session);
  if (session.mode === 'backend') {
    // Keep bearer credentials out of persistent localStorage. The backend
    // currently returns tokens, so sessionStorage is the least persistent
    // browser storage available until an httpOnly cookie session is provided.
    try {
      window.sessionStorage.setItem(SESSION_STORAGE_KEY, serialized);
    } catch {
      // Keep the in-memory session usable, but never fall back to localStorage.
    }
    try {
      window.localStorage.removeItem(SESSION_STORAGE_KEY);
    } catch {
      // Ignore unavailable storage.
    }
    return;
  }

  try {
    window.localStorage.setItem(SESSION_STORAGE_KEY, serialized);
  } catch {
    // The demo can still be used for the current render if storage is blocked.
  }
  try {
    window.sessionStorage.removeItem(SESSION_STORAGE_KEY);
  } catch {
    // Ignore unavailable storage.
  }
};

export const clearPortalSession = () => {
  if (typeof window === 'undefined') return;
  try {
    window.localStorage.removeItem(SESSION_STORAGE_KEY);
  } catch {
    // Ignore unavailable storage.
  }
  try {
    window.sessionStorage.removeItem(SESSION_STORAGE_KEY);
  } catch {
    // Ignore unavailable storage.
  }
};

export const getRoleHome = (role: PortalRole) => {
  if (role === 'farmer') return '/sandbox';
  if (role === 'expert') return '/dashboard';
  return '/operations';
};

export const getRoleLabel = (role: PortalRole) => {
  if (role === 'farmer') return 'Farmer / user';
  if (role === 'expert') return 'Agronomist / reviewer';
  if (role === 'officer') return 'Officer / operations';
  return 'Employee / officer';
};

export { SESSION_STORAGE_KEY };
