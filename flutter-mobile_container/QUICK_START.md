# 🚀 QUICK START REFERENCE
## Flutter Mobile Container - Fast Track Guide

---

## ⚡ 30-SECOND SETUP

```powershell
# 1. Open PowerShell in project folder
Set-Location c:\Projects\flutter-mobile_container

# 2. Clean and get dependencies
flutter clean
flutter pub get

# 3. Connect Android phone (USB Debugging enabled)
adb devices

# 4. Run app
flutter run
```

**That's it! App installs and launches automatically.**

---

## 📱 ANDROID DEVICE SETUP (First Time Only)

### Phone Settings (2 minutes)
1. **Settings** → **About Phone** → Tap **Build Number** 7 times
2. **Settings** → **Developer Options** → Enable **USB Debugging**
3. Plug in USB cable → Tap **Allow** on phone

### Computer Command
```powershell
adb devices
# Should show your phone as "device"
```

---

## 🎯 COMMON COMMANDS

| Task | Command |
|------|---------|
| Clean project | `flutter clean` |
| Get dependencies | `flutter pub get` |
| Run on device | `flutter run` |
| Build release APK | `flutter build apk --release` |
| View device logs | `flutter logs` |
| Stop app | `adb shell am force-stop com.example.mobile_container` |
| View all devices | `adb devices` |

---

## 🔴 PROBLEM SOLVING

### App Shows "Unable to Load Application"
**FIX:** AndroidManifest.xml already has INTERNET permission ✅

### Device Not Recognized
```powershell
adb kill-server
adb start-server
adb devices
```

### Build Failed
```powershell
flutter clean
flutter pub get
flutter run
```

### App Crashes
```powershell
flutter logs -d <device-id>
# Check error messages
```

---

## 📂 KEY FILES TO EDIT

| File | Purpose |
|------|---------|
| `lib/config/app_colors.dart` | Change colors (ElectricBlue, TrueBlack, CoolGray) |
| `lib/config/app_config.dart` | Change WebView URL, app settings |
| `lib/main.dart` | Change app name, theme |
| `lib/screens/splash_screen.dart` | Customize splash screen |

---

## 🌐 CHANGE WEBVIEW URL

Open `lib/config/app_config.dart`:

```dart
// Find this line:
static const String baseUrl = 'https://example.com';

// Change to your URL:
static const String baseUrl = 'https://your-website.com';

// Then:
flutter run
```

---

## 🎨 CHANGE COLORS

Open `lib/config/app_colors.dart` and modify:

```dart
static const Color primary = Color(0xFF0080FF);      // Electric Blue
static const Color dark = Color(0xFF000000);         // True Black
static const Color neutral = Color(0xFF8B92AB);      // Cool Gray
```

---

## 📤 UPDATE GITHUB

After making changes:

```powershell
git add -A
git commit -m "fix: your description here"
git push origin main
```

---

## ✅ INSTALLATION SUCCESS CHECKLIST

- ✅ Android phone connected and recognized
- ✅ App installs without errors
- ✅ Splash screen shows for 3 seconds
- ✅ Electric Blue visible on AppBar
- ✅ WebView loads website content
- ✅ Refresh button works
- ✅ No crashes or errors
- ✅ App performs smoothly

---

## 📞 EMERGENCY HELP

**Completely broken? Start fresh:**

```powershell
# Hard reset
flutter clean
Remove-Item -Recurse -Force build/
Remove-Item -Recurse -Force .dart_tool/
flutter pub get
flutter pub upgrade
flutter run
```

---

## 🎉 YOU'RE READY!

Your app is production-ready. Go build something amazing! 🚀

**Repository:** https://github.com/m4gnel/Flutter-mobile_container

