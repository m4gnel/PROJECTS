export type ApiRole = 'farmer' | 'employee' | 'officer' | 'expert';

export interface ApiUser {
  id: string;
  phone: string;
  name?: string | null;
  language?: string;
  subscription_tier: string;
  role: ApiRole;
  permissions: string[];
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  user?: ApiUser;
}

export interface OperationsQueueItem {
  advisory_id: string;
  created_at: string | null;
  confidence_state: string;
  confidence_score: number | null;
  safe_to_act: boolean;
  triage_status: 'PENDING_REVIEW' | 'ESCALATED';
  farmer_name: string;
  farmer_phone: string | null;
  farm_name: string | null;
  district: string | null;
  crop: string | null;
}

export interface OperationsSummary {
  active_advisories: number;
  needs_review: number;
  high_confidence: number;
  average_confidence: number;
  generated_at: string;
  read_only: boolean;
}

export interface OperationsServiceBoundary {
  name: string;
  access: string;
  source: string;
  writes_enabled: boolean;
}

export interface OperationsSnapshot {
  summary: OperationsSummary;
  queue: {
    items: OperationsQueueItem[];
    total_pending: number;
    read_only: boolean;
  };
  serviceBoundary: {
    service: string;
    environment: string;
    read_only: boolean;
    boundaries: OperationsServiceBoundary[];
    generated_at: string;
  };
  fetchedAt: string;
}

export interface AdvisoryResponse {
  answer_native: string;
  answer_en: string;
  agents_used: string[];
  language: string;
  farmer_id: string;
  generation_ms: number;
  fcm_triggered: boolean;
  warnings: string[];
}

export class ApiError extends Error {
  readonly status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

const rawConfiguredBaseUrl = (import.meta.env.VITE_API_BASE_URL ?? '').trim();

const normalizeApiBaseUrl = (value: string): { url: string; error: string | null } => {
  if (!value) return { url: '', error: null };

  if (value.startsWith('/')) {
    if (value.startsWith('//') || value.includes('?') || value.includes('#')) {
      return {
        url: '',
        error: 'VITE_API_BASE_URL must be a same-origin path without a query string or hash.',
      };
    }
    return { url: value.replace(/\/+$/, '') || '/', error: null };
  }

  try {
    const parsed = new URL(value);
    if (parsed.protocol !== 'https:' && parsed.protocol !== 'http:') {
      return { url: '', error: 'VITE_API_BASE_URL must use http:// or https://.' };
    }
    if (parsed.search || parsed.hash) {
      return { url: '', error: 'VITE_API_BASE_URL must not include a query string or hash.' };
    }

    const isLocalhost = ['localhost', '127.0.0.1', '[::1]'].includes(parsed.hostname);
    if (
      typeof window !== 'undefined' &&
      window.location.protocol === 'https:' &&
      parsed.protocol === 'http:' &&
      !isLocalhost
    ) {
      return {
        url: '',
        error: 'An HTTPS site cannot call an insecure HTTP API. Use an HTTPS API URL in production.',
      };
    }

    return {
      url: `${parsed.origin}${parsed.pathname}`.replace(/\/+$/, '') || parsed.origin,
      error: null,
    };
  } catch {
    return {
      url: '',
      error: 'VITE_API_BASE_URL must be a full API origin or a same-origin path such as /api.',
    };
  }
};

const normalizedApiBaseUrl = normalizeApiBaseUrl(rawConfiguredBaseUrl);
const configuredBaseUrl = normalizedApiBaseUrl.url;
const apiPrefix = configuredBaseUrl === '/'
  ? '/api/v1'
  : configuredBaseUrl.endsWith('/api/v1')
  ? configuredBaseUrl
  : configuredBaseUrl.endsWith('/api')
  ? `${configuredBaseUrl}/v1`
  : `${configuredBaseUrl}/api/v1`;

export const isLiveApiConfigured = configuredBaseUrl.length > 0;
export const apiConfigurationError = normalizedApiBaseUrl.error;

const apiUrl = (path: string) => `${apiPrefix}${path}`;
const API_REQUEST_TIMEOUT_MS = 15_000;

const detailMessage = (payload: unknown): string => {
  if (!payload || typeof payload !== 'object' || !('detail' in payload)) return '';
  const detail = (payload as { detail?: unknown }).detail;
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((entry) => {
        if (entry && typeof entry === 'object' && 'msg' in entry) return String((entry as { msg?: unknown }).msg ?? '');
        return String(entry);
      })
      .filter(Boolean)
      .join('. ');
  }
  return detail == null ? '' : String(detail);
};

async function requestJson<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set('Accept', 'application/json');
  if (init.body && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json');

  const controller = new AbortController();
  let timedOut = false;
  const timeoutId = globalThis.setTimeout(() => {
    timedOut = true;
    controller.abort();
  }, API_REQUEST_TIMEOUT_MS);
  const callerSignal = init.signal;
  const abortFromCaller = () => controller.abort(callerSignal?.reason);
  if (callerSignal) {
    if (callerSignal.aborted) {
      abortFromCaller();
    } else {
      callerSignal.addEventListener('abort', abortFromCaller, { once: true });
    }
  }

  let response: Response;
  try {
    response = await fetch(apiUrl(path), {
      ...init,
      headers,
      credentials: 'omit',
      mode: 'cors',
      signal: controller.signal,
    });
  } catch (error) {
    if (timedOut) {
      throw new ApiError('The API request timed out. Check the service status and try again.', 0);
    }
    throw new ApiError(error instanceof Error ? error.message : 'The API could not be reached', 0);
  } finally {
    globalThis.clearTimeout(timeoutId);
    callerSignal?.removeEventListener('abort', abortFromCaller);
  }

  const text = await response.text();
  let payload: unknown = null;
  if (text) {
    try {
      payload = JSON.parse(text);
    } catch {
      payload = null;
    }
  }

  if (!response.ok) {
    const detail = detailMessage(payload);
    throw new ApiError(detail || `API request failed with HTTP ${response.status}`, response.status);
  }

  return payload as T;
}

const isNonEmptyString = (value: unknown): value is string =>
  typeof value === 'string' && value.trim().length > 0;

const parseAuthResponse = (response: AuthResponse): AuthResponse => {
  if (!response || !isNonEmptyString(response.access_token) || !isNonEmptyString(response.refresh_token)) {
    throw new ApiError('The authentication service returned an invalid session.', 502);
  }
  return response;
};

const parseAdvisoryResponse = (response: AdvisoryResponse): AdvisoryResponse => {
  if (
    !response ||
    typeof response !== 'object' ||
    typeof response.answer_native !== 'string' ||
    typeof response.answer_en !== 'string' ||
    !Array.isArray(response.warnings) ||
    response.warnings.some((warning) => typeof warning !== 'string')
  ) {
    throw new ApiError('The advisory service returned an invalid response.', 502);
  }
  return response;
};

export function sendOtp(phone: string) {
  return requestJson<{ message: string; expires_in: number }>('/auth/send-otp', {
    method: 'POST',
    body: JSON.stringify({ phone }),
  });
}

export function verifyOtp(phone: string, otp: string, name?: string) {
  return requestJson<AuthResponse>('/auth/verify-otp', {
    method: 'POST',
    body: JSON.stringify({ phone, otp, ...(name ? { name } : {}) }),
  }).then(parseAuthResponse);
}

export function refreshAccessToken(refreshToken: string) {
  if (!isNonEmptyString(refreshToken)) {
    return Promise.reject(new ApiError('Your session refresh token is missing. Sign in again.', 401));
  }
  return requestJson<AuthResponse>('/auth/refresh', {
    method: 'POST',
    body: JSON.stringify({ refresh_token: refreshToken }),
  }).then(parseAuthResponse);
}

export function revokeRefreshToken(refreshToken: string) {
  if (!isNonEmptyString(refreshToken)) return Promise.resolve();
  return requestJson<{ message: string }>('/auth/logout', {
    method: 'POST',
    body: JSON.stringify({ refresh_token: refreshToken }),
  }).then(() => undefined);
}

export async function fetchOperationsSnapshot(accessToken: string): Promise<OperationsSnapshot> {
  if (!isNonEmptyString(accessToken)) {
    throw new ApiError('Your session is missing an access token. Sign in again.', 401);
  }
  const headers = { Authorization: `Bearer ${accessToken}` };
  const [summary, queue, serviceBoundary] = await Promise.all([
    requestJson<OperationsSummary>('/operations/summary', { headers }),
    requestJson<OperationsSnapshot['queue']>('/operations/queue?limit=100', { headers }),
    requestJson<OperationsSnapshot['serviceBoundary']>('/operations/service-boundary', { headers }),
  ]);

  if (
    !summary ||
    typeof summary !== 'object' ||
    !Array.isArray(queue?.items) ||
    !serviceBoundary ||
    typeof serviceBoundary !== 'object' ||
    !Array.isArray(serviceBoundary.boundaries)
  ) {
    throw new ApiError('The operations service returned an invalid snapshot.', 502);
  }

  return {
    summary,
    queue,
    serviceBoundary,
    fetchedAt: new Date().toISOString(),
  };
}

export function requestAdvisory(
  request: {
    farmer_id: string;
    query: string;
    language: string;
    state: string;
    district: string;
    crops: string[];
  },
  accessToken: string,
) {
  if (!isNonEmptyString(accessToken)) {
    return Promise.reject(new ApiError('Your session is missing an access token. Sign in again.', 401));
  }
  return requestJson<AdvisoryResponse>('/advisory', {
    method: 'POST',
    headers: { Authorization: `Bearer ${accessToken}` },
    body: JSON.stringify(request),
  }).then(parseAdvisoryResponse);
}
