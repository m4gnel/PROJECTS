# Agri-SAGE web frontend

The public Agri-SAGE web experience is a React 19 + TypeScript + Vite app. It
contains the public landing journey, the role-aware access portal, the farmer
advisory simulator, and the staff operations/review workspaces.

## Requirements

- Node.js `20.19.0` (the repository `.nvmrc` is the source of truth)
- npm from that Node.js installation

The committed `package-lock.json` must be used for installs. Do not install
frontend dependencies globally.

## Configure

```bash
cp .env.example .env.local
```

Set `VITE_API_BASE_URL` to the public HTTPS backend origin, for example
`https://api.example.com`. A same-origin path such as `/api` is also supported.
The client calls the `/api/v1` endpoints below that base URL:

- `POST /auth/send-otp`
- `POST /auth/verify-otp`
- `POST /auth/refresh`
- `POST /auth/logout`
- `GET /operations/summary`
- `GET /operations/queue`
- `GET /operations/service-boundary`
- `POST /advisory`

The browser client sends bearer tokens in the `Authorization` header with
`credentials: omit`; it does not send cookies. The API must therefore allow the
deployed site origin in CORS and allow the `Authorization` and `Content-Type`
request headers. The backend remains responsible for token validation,
authorization, refresh-token rotation, and revocation policy.

`VITE_ENABLE_DEMO_AUTH` is for an intentional local preview only. Vite
development mode enables the seeded preview automatically. Production builds
disable demo sign-in unless this flag is explicitly set to `true`; the Pages
workflow always sets it to `false` and requires `VITE_API_BASE_URL`.

`VITE_BASE_PATH` controls the Vite asset and router base path. Use `/` for a
local server or custom domain. The GitHub Pages workflow uses `/AgriSage/`.

## Install and run

From this directory:

```bash
npm ci
npm run dev
```

Open the local URL printed by Vite. With no API URL in Vite development mode,
the access portal shows clearly labelled seeded preview credentials. Those
credentials never create a backend account.

## Checks

Run the focused frontend release checks offline after `npm ci`:

```bash
npm run typecheck
npm run lint
npm run build
```

There is no frontend test runner in this package, so the release gate is the
TypeScript check, Oxlint, and the production Vite build. The existing lint
configuration currently reports warnings in legacy/design components; the
command exits successfully and the warnings are retained for a separate cleanup
pass.

To verify the Pages base path locally:

```bash
VITE_BASE_PATH=/AgriSage/ VITE_API_BASE_URL=https://api.example.com npm run build
```

## GitHub Pages deployment

The single Pages workflow is `.github/workflows/deploy.yml`. In the GitHub
repository settings:

1. Add the repository variable `VITE_API_BASE_URL` with the production HTTPS
   backend origin.
2. Set Pages → Build and deployment → Source to **GitHub Actions**.
3. Configure the backend CORS allowlist for the final Pages origin before the
   first user sign-in.

The workflow installs from `package-lock.json`, builds with `/AgriSage/`,
disables demo authentication, emits `404.html` for direct SPA route loads, and
fails rather than publishing a build with no API configuration. The duplicate
legacy Pages workflow was removed so two deployments cannot race each other.

## Session behavior

Backend sessions are stored in `sessionStorage`, never persistent
`localStorage`. A logout clears both storage areas. Operations and advisory
requests attempt one refresh on an HTTP 401; if refresh fails, the session is
cleared and the user is returned to the public entry point. Logout also
best-effort revokes the backend refresh token before clearing browser state.
Until the backend provides an httpOnly cookie session, the API and frontend deployment must both
maintain a strict Content Security Policy and protect against XSS.
