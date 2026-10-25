# Agri-SAGE Production Readiness State

## Wave 1–3 Summary

**Objective:** Make the existing repository reproducible without replacing existing product work.

**Changes:**

- Added pinned runtime markers, `.dockerignore`, a Linux `gradlew`, and a repository `Makefile`.
- Made the root web scripts delegate to the locked Vite app and added the app typecheck script.
- Added production configuration validation, liveness/readiness endpoints, safer Compose startup/migrations, and removed the unused PostGIS migration dependency.
- Fixed Python 3.11 import failures in the RAG, storage, authentication, and critic modules.
- Added payment signature/order verification and fail-closed behavior for unconfigured OTP/payment providers.
- Added regression coverage for runtime and payment safety gates.
- Unified `backend/requirements.txt` with the canonical root dependency set and kept developer tools in `backend/requirements-dev.txt`.
- Made embeddings opt-in and lazy, preventing heavy model downloads during startup and offline tests.
- Made image MIME detection lazy, so the Windows `python-magic` crash cannot prevent the API from importing; added the missing `Image` ORM and observation endpoint imports.
- Made pipeline timeouts return an explicit `INSUFFICIENT_DATA` safe advisory instead of a partial response.
- Corrected CI to run the canonical root migrations/tests and a passing syntax/undefined-name lint gate; removed the unsupported `pip-audit --fail-on` argument.
- Made production Compose fail immediately when `DB_PASSWORD` is missing.
- Generated hashed Python lockfiles for Python 3.11 x86_64 Linux with the CPU PyTorch index; Docker and CI now install from `requirements.lock` and `requirements-dev.lock` with hash checking.
- Removed the private Firebase config from the Git index, added `mobile/android/app/google-services.json.example`, and committed the ignore rules.
- Added a role-aware web access preview for farmer users and employee/officer staff, an internal operations console, and a shared staff workspace frame. These are explicitly demo/read-only surfaces until backend authentication, persistence, live service health, and authorization are connected.
- Polished the wired Android farmer dashboard with a farm illustration, KPI/stat cards, vector icons, accessible bottom navigation, and shared pressed-state semantics; kept the existing route contracts and restored the existing light-theme default to avoid changing the prior product direction.
- Added persisted JWT RBAC for farmer, employee, officer, and expert roles, migration 019, fail-closed role/permission dependencies, protected read-only operations endpoints, and audited privileged reads/reviews. Existing expert subscription-tier access remains compatible.
- Added a web backend-auth mode controlled by `VITE_API_BASE_URL`: OTP/JWT sessions use session storage, server-provisioned roles determine destinations, operations metrics/queue data come from the protected API, and demo mode remains explicit when the variable is empty.
- Corrected the broad `models/` ignore rule so backend ORM/schema source files are included in clean checkouts, pinned `.nvmrc`/`.python-version` to exact patch releases, and removed the deploy workflow's global Railway CLI install.

**Verification:**

- `.venv/Scripts/python.exe -m pytest tests -q`: 83 passed, 1 warning.
- `.venv/Scripts/python.exe -m pytest backend/tests -q`: 18 passed, 1 warning.
- `.venv/Scripts/python.exe -m pip check`: no broken requirements.
- `PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe -m alembic upgrade head --sql`: generated static SQL through revision 019.
- `npm run typecheck`: passed.
- `npm run build`: passed; Vite reported an existing large-chunk warning.
- `npm run lint`: passed with existing warnings only.
- `npm ci --prefix apps/web-expert --dry-run --ignore-scripts`: passed.
- `npm ci --dry-run --ignore-scripts --offline --prefix apps/web-expert`: passed after the API integration.
- `npm run typecheck` and `npm run build` passed after backend-auth web integration; the existing large-chunk warning remains.
- All six workflow YAML files parsed successfully.
- Development Compose config passed; production Compose config passed with validation-only environment variables.
- Targeted RBAC/API tests: 20 passed; backend compatibility tests: 18 passed; compileall passed.
- `.venv/Scripts/python.exe -m ruff check backend/ --select E9,F821 --ignore E501`: passed.
- `python -m pytest tests/` and `python -m pytest backend/tests/`: passed separately; the Makefile now runs them separately to avoid pytest conftest module-name collisions.
- `timeout 30s .venv/Scripts/python.exe -c "import backend.main"`: passed.
- `uv pip install --dry-run --python-version 3.11 --python-platform x86_64-unknown-linux-gnu --index-strategy unsafe-best-match --require-hashes --requirement requirements.lock --requirement requirements-dev.lock`: resolved 165 packages without installing them.
- `python -c "...yaml.safe_load(...)..."`: all six workflow YAML files parsed after lockfile migration.
- Commits created: `ef823f1` reproducibility foundations, `53c1a50` local deployment credential protection, and `60caf94` hashed Linux Python dependency locks.
- UI commits created: `73b73f3` role-aware web operations workspace, `2306611` vector feedback controls, and `2c935b4` farmer dashboard/navigation polish.
- Web UI verification after the UI wave: `npm run typecheck`, `npm run build`, and `npm run lint` completed; lint still reports existing warnings and build still reports the existing large chunk warning. The local Vite `/AgriSage/operations` route responded over HTTP; built-in visual browser inspection timed out.

**Unavailable checks:**

- Docker daemon was not running, so a real PostgreSQL migration, Docker build, and Compose startup were not executed.
- Java is not installed, so Android Gradle tests/build were not executed.
- GNU Make is not installed on this Windows host, so `make test` was not invoked; its underlying commands were run directly.

**Risks / manual gates:**

- Existing web lint warnings and a large JavaScript chunk remain.
- Full historical backend Ruff/Black gates still report 155 Ruff findings and 134 formatting candidates across pre-existing code; they were not auto-formatted because that would rewrite a large unrelated surface. CI now enforces syntax and undefined-name correctness while this debt remains visible.
- External provider credentials, OTP delivery, Razorpay, R2, FCM, Gemini, DSSAT/model assets, production PostgreSQL permissions, Android signing/Firebase, and agronomy safety review remain release gates.
- The employee/officer console now has a protected read-only API path when `VITE_API_BASE_URL` is configured; regional alerts remain seeded, review writes remain in the separate expert workflow, and real OTP delivery/provider integration is still a release gate.
- Migration 019 must be applied to staging/production before provisioning staff roles. Verify RLS, staff queue joins, audit rows, and forbidden farmer access against a real PostgreSQL instance.
- Earlier Android compile verification was blocked because the host did not have a configured Java/JDK; the current Android follow-up below uses the configured local JDK successfully.
- The repository contains a large pre-existing staged/unstaged diff. It was not reset or rewritten.
- The current working tree still contains that pre-existing mixed diff; the private `mobile/android/app/google-services.json` is no longer staged or tracked, while the example file is committed.

## Earlier Android follow-up — 2026-10-22

- Active runtime wiring is verified as `MainActivity -> navigation.AppNavHost -> nested ui.screens.*`; the reference-inspired top-level duplicate screens are not the active route targets.
- Active fields and weather screens now preserve the reference-style visual direction while using provider/Room-backed data and explicit empty, stale, or unavailable states instead of fabricated plots, forecasts, readings, or recommendations.
- Active home, alerts, advisor, and profile flows were hardened against demo identity, seeded alerts, default farmer IDs, hardcoded profile values, and offline actionable agronomy fallbacks.
- Android verification now passes with the local JDK: Kotlin compilation, debug lint, debug unit tests, and debug APK assembly. Lint reports warnings only; the full warning list remains in the generated Android lint report.
- Remaining Android gate: install/configure Android platform tools or open `mobile/android/` in Android Studio, launch an emulator/device, and visually verify splash/onboarding, authenticated home, fields, weather, alerts, advisor, and profile flows at small-phone and tablet sizes. `adb devices` is currently unavailable on this host.
- Remaining release gates are unchanged: real backend/provider credentials, Firebase configuration and notification permission flow, release signing, staging PostgreSQL/RLS, security/privacy/legal review, agronomist review, rollback/monitoring, and manual device/browser testing.

## Android reference continuation — 2026-10-23

- Kept the active nested screen graph and existing reference layouts. Root inset
  consumption now avoids double status-bar padding, paints the status-bar strip,
  and accounts for keyboard insets. Advisor is full-screen; other main tabs keep
  the shared bottom navigation.
- Normal debug now requires authentication and never enables reference fixtures.
  Explicit `-PreferencePreview=true` creates a separate `com.agrisage.app.preview`
  install, persistent sample-data banner, isolated output directory and blocked
  account/API writes. No real user's installation/data was deleted.
- Profile editing now waits for an actual API success; errors preserve edits and
  existing identity. Advisory language persists and is used by the chat. System
  notification settings replace the fake local switch; offline cache is read-only.
- Advisor now invokes the device speech-input activity, prevents duplicate sends,
  keeps unsigned/failed drafts, scrolls replies and expands language touch targets.
  Real speech recognition and authenticated provider behavior still need device/staging checks.
- Farm filters and profile shortcuts work. Add Plot requires explicit valid
  coordinates rather than inventing a location. Reference-only plot labels are
  gated by build mode as well as ID.
- Removed the fabricated profile sync receipt. The sync worker retains observations
  unless the response confirms exact durable `persisted_ids`. The current backend
  sync endpoint does not persist them; backend storage, idempotency and tenant
  ownership remain a release blocker. Sync Now is explicitly disabled.
- Fresh Linux JDK/SDK setup and normal Kotlin compilation succeeded. Regression
  coverage was expanded from 3 to 14 tests; the full suite passed. Normal lint
  passed with 0 errors / 85 warnings, and normal/reference debug APKs assembled.
  All checks were rerun successfully after the weather caption correction found
  in emulator testing. The final preview was reinstalled and its Rainy hero/detail
  caption agreement verified from the UI hierarchy and screenshot.
- ADB became reachable from the container. Reused `emulator-5554`, AVD
  `Medium_Phone_API_37.0`, without starting another emulator. Reference UI was
  installed and exercised (tabs, plot detail/filter, weather mode, prompt/send guard).
  Advisor was inspected at a smaller phone size; original display and keyboard
  settings were restored. A floating input panel was observed, not a full docked keyboard.
- Normal APK update was rejected by Android because its signing key differs from
  the existing Windows-signed installation. That original app remains untouched.
  Use the original Windows key/build environment to update it; do not uninstall it
  without an explicit decision about retained data.
- Build/open commands, artifacts and manual gates: `mobile/android/VERIFICATION.md`.
  Evidence is in outer workspace `screenshots/android-final-2026-10-23/`.
- Final preview is left on Home. Next: update the real-data app with the original
  Windows signing key and verify authenticated staging flows; preserve the old
  installation's data. Source remains an uncommitted worktree on `main` (`1daa1f5`).
- No commits, pushes, deployments, database changes or real provider submissions
  were made in this continuation. Unrelated mixed-index work remains preserved.
