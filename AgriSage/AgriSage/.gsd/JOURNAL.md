# Verification Journal

## 2026-10-18 — reproducibility and safety wave

- `py -3.11 -m venv .venv`: created a project-local Python 3.11 environment.
- Initial `pip install -r requirements.txt` exposed an invalid `cross-encoder==0.1.0` requirement. The nonexistent direct dependency was removed; the install then completed successfully.
- `.venv/Scripts/python.exe -m pytest tests -q`: initially exposed a missing `Tuple` import in `backend/agents/critic.py`; after the focused fix, 71 tests passed.
- `.venv/Scripts/python.exe -m pytest backend/tests -q`: 18 tests passed after making the compatibility wrapper load the canonical root database tests by file path.
- `.venv/Scripts/python.exe -c "import backend.services.storage; import backend.services.rag_service"`: passed after fixing missing imports and optional storage initialization.
- `PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe -m alembic upgrade head --sql > NUL`: passed through migration 018. The first Windows run failed only because the console used cp1252 for an existing emoji in the master SQL; UTF-8 output is the Linux/CI behavior.
- `docker compose config` and production Compose config parsed. Actual Docker startup was blocked by the unavailable Docker Desktop Linux engine.
- `npm run typecheck`, `npm run build`, `npm run lint`, and `npm ci --prefix apps/web-expert --dry-run --ignore-scripts` passed. Lint/build warnings are existing quality debt, not hidden failures.
- A mocked API check observed `/health` returning 200 with `status: ok` and `/ready` returning 503 when the database check returned false.
- `python -m pytest tests/ -q`: 71 passed after adding timeout-safe pipeline output, lazy embeddings, and lazy image MIME detection.
- `python -m pytest backend/tests/ -q`: 18 passed.
- `ruff check backend/ --select E9,F821 --ignore E501`: passed; the prior full historical E/F/W run remains a documented debt report rather than a hidden pass.
- `import backend.main`: passed under a 30-second bounded import check; the earlier Windows `python-magic` access violation no longer blocks startup.
- `DB_PASSWORD=not-a-secret docker compose -f docker-compose.prod.yml config`: passed; production config now requires the password variable instead of silently accepting an empty database password.

## 2026-10-18 — lockfile and credential follow-up

- Audited the mixed index without resetting existing work. The staged `mobile/android/app/google-services.json` was absent from the working tree and was removed from the index; the safe placeholder `mobile/android/app/google-services.json.example` was committed instead.
- `uv pip compile requirements.txt --python-version 3.11 --python-platform x86_64-unknown-linux-gnu --torch-backend cpu --extra-index-url https://download.pytorch.org/whl/cpu --index-strategy unsafe-best-match --generate-hashes --emit-index-url --emit-index-annotation --output-file requirements.lock`: generated the hashed runtime lock.
- `uv pip compile backend/requirements-dev.txt --constraint requirements.lock --python-version 3.11 --python-platform x86_64-unknown-linux-gnu --generate-hashes --output-file requirements-dev.lock`: generated the hashed development lock.
- `uv pip install --dry-run --python-version 3.11 --python-platform x86_64-unknown-linux-gnu --index-strategy unsafe-best-match --require-hashes --requirement requirements.lock --requirement requirements-dev.lock`: resolved 165 packages without installing them.
- After the lockfile/CI/Docker changes, `.venv/Scripts/python.exe -m pytest tests/ -q`: 71 passed, 1 warning; `.venv/Scripts/python.exe -m pytest backend/tests/ -q`: 18 passed, 1 warning.
- All six workflow YAML files parsed, and `DB_PASSWORD=not-a-secret docker compose -f docker-compose.prod.yml config` still passed.

## 2026-10-18 — UI/UX foundation wave

- Loaded the local UI/UX, UI styling, design-system, and brand guidance. The verified UI guidance emphasized semantic navigation, visible keyboard focus, skip links, reduced-motion handling, 44px+ targets, and restrained motion for dense operational data.
- The six supplied Instagram URLs were attempted through the available read-only fetch/browser paths, but Instagram returned no usable post content and the built-in browser timed out. Exact visual matching against those posts is therefore not claimed; the implementation used the existing Agri-SAGE design tokens, repository UI notes, and verified local UI guidance instead.
- Added and committed the web employee/officer access preview and operations console in `73b73f3`. The console computes KPIs, triage filters, regional coverage, and service-boundary indicators from existing seed data, and labels all non-live behavior explicitly.
- Web checks after the change: `npm run typecheck` passed; `npm run build` passed with the existing large-chunk warning; `npm run lint` exited successfully with existing warnings; `curl http://127.0.0.1:4173/AgriSAGE/operations` responded after starting the Vite dev server. A browser visual inspection was unavailable because the built-in browser timed out.
- Added vector feedback controls in `2306611` and committed the wired Android farmer dashboard/navigation polish plus required new UI components in `2c935b4`. `git diff --check` passed for the Android UI changes.
- Attempted Android verification with `./gradlew :app:compileDebugKotlin --offline`; it was blocked before Gradle execution because Java/JDK is not installed on this host.

## 2026-10-18 — JWT/RBAC and release integration wave

- Added canonical roles and permissions in `backend/rbac.py`, persisted `users.role`/`users.permissions` in migration `019_user_rbac`, and made JWT claims derive from persisted authorization state.
- Added protected `GET /api/v1/operations/summary`, `/queue`, and `/service-boundary` endpoints for employee/officer roles, with fail-closed audit writes to the existing `audit_logs` table. Expert queue/review access now uses the same persisted principal path while preserving `subscription_tier="expert"` compatibility.
- Web checks after live API integration: `npm run typecheck` passed; `npm run build` passed with the existing large-chunk warning; `npm run lint` exited successfully with existing warnings. The web can use `VITE_API_BASE_URL` for OTP/JWT authentication and protected operations reads, otherwise it stays in explicit demo mode.
- Backend checks: targeted RBAC/API tests `20 passed`; root tests `83 passed`; backend compatibility tests `18 passed`; compileall passed; offline Alembic SQL generated through `019_user_rbac`.
- Release checks: all six workflow YAML files parsed; frontend `npm ci --dry-run --ignore-scripts --offline` passed; development Compose config passed; production Compose config passed with validation-only environment variables. Docker image/runtime, live PostgreSQL, and Android Gradle checks remain blocked by host tooling.
- Fixed clean-checkout reproducibility by unignoring backend ORM/schema source under `backend/models/`, pinning `.nvmrc` to `20.19.0` and `.python-version` to `3.11.9`, and replacing the global Railway CLI workflow install with a pinned project-local `npm exec` invocation.

## 2026-10-22 — active Android path and fail-closed UI wave

- Confirmed the Android Studio/runtime path is `MainActivity -> navigation.AppNavHost -> ui.screens.home/HomeScreen`, `ui.screens.fields/FieldsScreen`, and `ui.screens.weather/WeatherScreen`; the top-level `ui/screens/*` reference trees remain legacy and were not activated or deleted.
- Rebuilt the active fields screen around the reference-style farm-plan layout while preserving `FieldsViewModel`, Room/API field data, add-field flow, loading/error states, and `Screen.FieldDetail` navigation. Fabricated initial plots were removed; empty/unavailable states are explicit.
- Rebuilt the active weather screen around the reference-style hero/illustration/metrics layout while preserving provider-backed `WeatherRepository` loading and refresh. Fabricated readings, mock forecasts, and actionable fallback advice were removed; cached/stale/unavailable states are labeled.
- Hardened the active home, alerts, advisor, and profile flows against seeded/demo data: profile/weather/alerts/fields now use repository-backed data or explicit unavailable states; advisor requests require the authenticated farmer subject and do not generate offline agronomy recommendations; alerts no longer seed fixtures.
- Fixed Android notification permission handling, removed the WorkManager initializer conflict for on-demand `Configuration.Provider`, added missing notification-channel translations for Hindi, Malayalam, and Tamil, and updated the stale `RepositoryTest` DTO constructor usage.
- Android checks passed with the configured local JDK (`C:/Users/MAGNEL/.jdks/jdk17/jdk-17.0.13+11`): `:app:compileDebugKotlin`, `:app:lintDebug`, `:app:testDebugUnitTest`, `:app:assembleDebug`, and targeted `git diff --check`. Lint completed with 103 warnings but no errors.
- Emulator/device verification was not completed: `adb` is not available on this host. No Android commit was created; the repository retains its pre-existing mixed index/worktree and unrelated changes.

## 2026-10-23 — interrupted Android continuation

- Reconciled the working tree and running processes before continuing. Previous
  Windows build/emulator receipts were treated as historical, not proof of the
  final code. The latest interrupted Kotlin invocation had no success receipt.
- Installed JDK 17 and Android SDK components in the Linux container, preserving
  the host's local.properties. Fixed the container package install's missing
  `/usr/share/man/man1` directory; did not alter the Windows JDK/SDK installation.
- Fresh `:app:compileDebugKotlin` passed. New targeted tests passed, followed by
  full `:app:testDebugUnitTest :app:lintDebug :app:assembleDebug`: 14 tests with no
  failures/skips, lint 0 errors / 85 warnings, debug APK assembled.
- `:app:assembleDebug -PreferencePreview=true` passed with a separate application
  ID/output directory. `:app:assembleRelease -PreferencePreview=true
  -PAPI_BASE_URL=https://example.invalid` intentionally failed with
  `Reference preview cannot be used for a release build` (negative safety check).
- ADB initially had no attached devices, then exposed the existing
  `Medium_Phone_API_37.0` / `emulator-5554`. Reused it rather than launching again.
  Normal install returned `INSTALL_FAILED_UPDATE_INCOMPATIBLE`; did not uninstall,
  wipe data, or bypass signature checks. Separate reference install/launch succeeded.
- Inspected Home, Farm, plot detail/filter, Weather (Rainbow and Rainy), Advisor and
  Profile using screenshots and UI hierarchy. Verified prompt selection retains
  the text and preview send is rejected without generating advice. Smaller-phone
  Advisor layout was checked; temporary size/input-panel settings were restored.
- Found an actual preview-state defect: Rainy updated temperature/humidity but
  Today's conditions retained rainbow-only wording. Bound that caption to the
  selected preview condition. Final normal checks and reference rebuild were
  queued after the prior build completed; final receipt/evidence follows below.
- Remaining gaps are listed in `mobile/android/VERIFICATION.md`, particularly
  durable backend sync, normal-app signing, real authentication/providers, full
  keyboard/voice tests and tablet/accessibility coverage. Exact visual parity and
  production readiness are not claimed.

### Final receipts after the weather regression fix

- From `mobile/android/`, with `ANDROID_HOME=/opt/android-sdk` and
  `ANDROID_SDK_ROOT=/opt/android-sdk`:
  `bash ./gradlew :app:testDebugUnitTest :app:lintDebug :app:assembleDebug
  --no-daemon --console=plain --max-workers=2
  -Pkotlin.compiler.execution.strategy=in-process` passed in 8m 37s.
  XML reports: 14 tests, 0 failures/errors/skips; lint: 0 errors / 85 warnings.
- `bash ./gradlew :app:assembleDebug -PreferencePreview=true --no-daemon
  --console=plain --max-workers=2 -Pkotlin.compiler.execution.strategy=in-process`
  passed in 4m 13s. Final preview APK installed successfully alongside the original.
- Replayed Rainy selection on the updated APK: UI hierarchy assertion confirmed
  two matching `Rain shower · 12 mm expected` captions and no stale rainbow-only
  description. Read `weather-rainy-final.png` and `home-final.png` to verify the
  rendered result. Final Home has the sample-data banner and preview package ID.
- `adb shell pm list packages com.agrisage` confirmed both installations remain.
  `wm size` returned the original physical 1080×2400; the temporary hardware
  keyboard input setting was restored to its original value, 0.
- Scoped `git --git-dir=.git_subrepo --work-tree=. -c core.whitespace=cr-at-eol
  diff --check` passed. This respects existing Windows line endings without
  rewriting unrelated CRLF files. Worktree base remains `main` / `1daa1f5`.
- Final artifacts, opening instructions and unresolved manual gates are recorded
  in `mobile/android/VERIFICATION.md`. No live-provider end-to-end or production
  release success is implied by these local UI/build results.
