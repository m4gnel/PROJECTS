# Android UI verification — 2026-10-23

## Two intentionally separate installations

- **Normal app:** `com.agrisage.app`. Debug and release builds require a real
  session. Missing provider data is not replaced with reference fixtures.
- **Reference preview:** `com.agrisage.app.preview`, launcher name
  **Agri-SAGE Reference**. Explicitly enabled with `-PreferencePreview=true`.
  A persistent banner identifies sample data. Account/API requests are blocked,
  automatic background sync is disabled, and account/plot writes are disabled.
  It is for visual inspection, not farming decisions or production use.
- Reference release builds are rejected. Firebase/signing/HTTPS release gates
  remain in place for the normal app.
- Preview output is isolated under `app/build/reference-preview/`; building it
  does not overwrite the normal APK or its verification reports.

## Build and open on Windows

Open a terminal in `AgriSage/mobile/android/` (relative to the outer workspace).
Use JDK 17 and the existing Android SDK. Do not overwrite local credentials.

Normal app checks and build:

```bat
gradlew.bat :app:testDebugUnitTest :app:lintDebug :app:assembleDebug --no-daemon --console=plain
```

Reference preview build:

```bat
gradlew.bat :app:assembleDebug -PreferencePreview=true --no-daemon --console=plain
```

Use the existing running emulator; check `adb devices` before starting another.
For the verified device serial:

```bat
"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe" devices
"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe" -s emulator-5554 install -r app\build\reference-preview\outputs\apk\debug\app-debug.apk
"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe" -s emulator-5554 shell am start -n com.agrisage.app.preview/com.agrisage.app.MainActivity
```

If the preview is already installed, opening **Agri-SAGE Reference** in the
emulator is sufficient; do not rebuild just to open it.

**Signing warning:** The normal APK built in the Linux container could not
replace the existing Windows-signed installation (`INSTALL_FAILED_UPDATE_INCOMPATIBLE`).
The original app/data were preserved. Build with the original Windows debug
keystore to update that installation. Do not uninstall or clear data simply to
hide a signing mismatch. A preview built on another machine can have the same
signing mismatch; keep its matching APK/key or explicitly decide whether its
sample-only data may be removed.

The old outer `Launch_AgriSage_App.bat` only launches the already installed
normal app. It does not build/install these changes or open the separate preview.

## Linux container commands used here

JDK 17, platform 35 and build-tools 34.0.0 are installed in the container.
The Windows `local.properties` was preserved; Gradle warns that its `sdk.dir`
does not exist here, then uses the supplied Linux SDK environment variables.

```bash
ANDROID_HOME=/opt/android-sdk ANDROID_SDK_ROOT=/opt/android-sdk bash ./gradlew :app:testDebugUnitTest :app:lintDebug :app:assembleDebug --no-daemon --console=plain --max-workers=2 -Pkotlin.compiler.execution.strategy=in-process
ANDROID_HOME=/opt/android-sdk ANDROID_SDK_ROOT=/opt/android-sdk bash ./gradlew :app:assembleDebug -PreferencePreview=true --no-daemon --console=plain --max-workers=2 -Pkotlin.compiler.execution.strategy=in-process
```

## Artifacts

Paths below are relative to `AgriSage/mobile/android/`:

- Normal APK: `app/build/outputs/apk/debug/app-debug.apk`
- Reference APK: `app/build/reference-preview/outputs/apk/debug/app-debug.apk`
- Unit test report: `app/build/reports/tests/testDebugUnitTest/index.html`
- Lint report: `app/build/reports/lint-results-debug.html`
- Screenshots: outer workspace `screenshots/android-final-2026-10-23/`.
  These include Home, Farm, plot detail/filter, Weather, Advisor, and Profile.

## Final recorded checks

Working tree based on `main` at `1daa1f5`, with uncommitted changes preserved.
No commit/push/deployment was performed. Results below include the last weather
caption correction, not just the earlier interrupted build.

| Check | Result |
| --- | --- |
| Normal Kotlin compilation | Passed |
| `:app:testDebugUnitTest` | 14 passed, 0 failures/errors/skips |
| `:app:lintDebug` | Passed: 0 errors, 85 warnings |
| Normal `:app:assembleDebug` | Passed |
| Preview `:app:assembleDebug -PreferencePreview=true` | Passed |
| Explicit release task with preview enabled | Rejected as expected |
| Scoped `git diff --check` (respecting existing CRLF) | Passed |
| Normal APK installation over existing Windows build | Blocked by signing-key mismatch; original preserved |
| Final preview install and launch | Passed on existing `emulator-5554` |
| Rainy state regression | Passed: hero and details both show the Rainy condition; rainbow-only caption absent |

The final preview is left on **Home**. Both `com.agrisage.app` and
`com.agrisage.app.preview` remain installed. Original `1080×2400` display size
and hardware-keyboard setting were restored after inspection.

Latest evidence: `home-final.png`, `weather-final.png`, and
`weather-rainy-final.png` in the screenshot directory above. Other screenshots
document earlier smoke steps in this same verification run. The files named
`advisor-keyboard*.png` show focus/floating input UI, not proof of a docked keyboard.

Next action for the real-data app: run the normal checks/build on Windows using
the original debug signing key, then update the existing installation and verify
OTP/profile/provider flows against staging. Do not use the preview as that proof.

## Remaining manual/release gates

- Real OTP/authenticated profile editing, provider responses, permissions,
  physical-device speech recognition, and real offline recovery need staging
  credentials and device tests. Unit-test doubles are not live-service evidence.
- The profile language control is an **advisory language preference**, not a
  claim that all hardcoded UI copy is localized. Notifications open Android's
  real app notification settings. Offline caching is read-only, not a fake toggle.
- **Sync is not production-ready.** `backend/api/v1/sync.py` currently returns a
  processed count without persisting observations. The Android worker now keeps
  a local item unless an exact `persisted_ids` receipt confirms durable storage.
  Backend persistence/receipt support, idempotency and tenant ownership must be
  implemented and integration-tested before enabling **Sync Now**.
- The emulator uses a floating input panel. Composer focus was checked, but a
  full docked soft keyboard, TalkBack, large font scaling, tablet/landscape and
  motion/accessibility coverage are not complete. Exact pixel/motion parity is
  not claimed.
- The broad pre-existing backend/web/migration/security/deployment work remains
  in `.gsd/STATE.md`; this continuation did not claim those release gates passed.
