# Mobile Container — Device Test Suite (Custom Edition)

## 📱 Project Overview

This is a professionally customized Flutter mobile application that serves as a container for the Device Test Suite website. The app features a modern, sleek UI with a custom color scheme and enhanced user experience.

**Version:** 1.0.0  
**Platform:** Android/iOS  
**Framework:** Flutter 2.18+  
**Language:** Dart

### ✨ Key Features

- **Optimized Splash Screen** - 3-second animated loading screen with gradient progress indicator
- **Full-Screen WebView** - Hosts https://devicetestsuite.incai.in/ seamlessly
- **Smart Loading Indicators** - Beautiful progress feedback during page loads
- **Error Handling UI** - Intuitive error display with retry functionality
- **Refresh Capability** - One-tap page refresh from the AppBar
- **Device Information Display** - Shows platform, version, and environment details
- **Material Design 3** - Modern Material Design implementation
- **Dark Theme Support** - Adaptive light and dark theme implementations

### 🎨 Custom Color Scheme

The application uses a premium custom color palette:

- **Electric Blue** (#0080FF) - Primary action color and brand color
- **True Black** (#000000) - Dark theme and accent elements
- **Cool Gray** (#8B92AB) - Secondary text and neutral elements
- **Supporting Colors** - Additional grays, greens, reds, and oranges for UI feedback

All colors are centrally managed in `lib/config/app_colors.dart` for easy maintenance.

## 📋 Project Structure

```
lib/
├── main.dart                          # App entry point with Material 3 theme
├── config/
│   ├── app_config.dart               # Application configuration constants
│   └── app_colors.dart               # Centralized color definitions
├── screens/
│   ├── splash_screen.dart            # Animated splash screen
│   └── webview_screen.dart           # WebView host screen with platform info
└── widgets/
    ├── loading_widget.dart           # Loading indicator with custom styling
    └── error_widget.dart             # Error UI with retry button
```

## 🚀 Quick Start

### Prerequisites

- Flutter SDK 2.18.0 or higher
- Android SDK (for Android builds)
- Xcode (for iOS builds, macOS only)
- A physical device or emulator with USB debugging enabled

### Installation & Running

1. **Clone the repository** (or extract the project)

```bash
cd flutter-mobile_container
```

2. **Get dependencies**

```bash
flutter pub get
```

3. **Run on connected device**

```bash
flutter run -d <device-id>
```

Or run on the default device:

```bash
flutter run
```

4. **View connected devices**

```bash
flutter devices
```

### Build Release APK

Create a production-ready APK for deployment:

```bash
# Debug build
flutter build apk --debug

# Release build (optimized and signed)
flutter build apk --release
```

The APK will be generated at: `build/app/outputs/flutter-apk/app-release.apk`

### Capture Logs

Monitor application logs in real-time:

```bash
flutter logs -d <device-id>
```

## 📁 Files of Interest

| File | Purpose |
|------|---------|
| `lib/main.dart` | App initialization and theme configuration |
| `lib/config/app_config.dart` | Centralized app constants and URLs |
| `lib/config/app_colors.dart` | Custom color palette (TrueBlack, CoolGray, ElectricBlue) |
| `lib/screens/splash_screen.dart` | Enhanced animated splash screen |
| `lib/screens/webview_screen.dart` | WebView container with device info |
| `lib/widgets/loading_widget.dart` | Styled loading indicator |
| `lib/widgets/error_widget.dart` | Error UI with retry functionality |
| `pubspec.yaml` | Project dependencies and metadata |

## 🔧 Configuration

### Update WebView URL

Edit `lib/config/app_config.dart`:

```dart
static const String baseUrl = 'https://your-custom-url.com/';
```

### Customize Colors

All colors are defined in `lib/config/app_colors.dart`. Modify the color values to match your brand:

```dart
static const Color electricBlue = Color(0xFF0080FF);
static const Color trueBlack = Color(0xFF000000);
static const Color coolGray = Color(0xFF8B92AB);
```

### Change App Name

1. For Android: Edit `android/app/build.gradle`
2. For iOS: Edit `ios/Runner/Info.plist`
3. In code: Update `AppConfig.appName` in `lib/config/app_config.dart`

## 🔄 GitHub Workflow

### Initial Setup

```bash
git init
git config user.email "your@email.com"
git config user.name "Your Name"
git add -A
git commit -m "chore: initial commit - custom mobile container"
```

### Create GitHub Repository

Using GitHub CLI:

```bash
gh auth login
gh repo create mobile_container --private --description "Mobile Container - Custom Edition"
git branch -M main
git push -u origin main
```

Or manually:

```bash
git remote add origin git@github.com:<your-username>/mobile_container.git
git branch -M main
git push -u origin main
```

## ✅ Testing Checklist

Before uploading to GitHub:

- [x] Flutter analyze passes without errors
- [x] All dependencies resolved successfully
- [x] App builds successfully: `flutter run --release`
- [x] WebView loads properly on Android
- [x] Error handling and retry functionality works
- [x] Colors display correctly (Electric Blue, True Black, Cool Gray)
- [x] Splash screen animates smoothly
- [x] Loading indicators display properly
- [x] App responds to device back button
- [x] Refresh button reloads WebView correctly

## 📚 Resources

- [Flutter Documentation](https://docs.flutter.dev/)
- [WebView Flutter Package](https://pub.dev/packages/webview_flutter)
- [Material Design 3](https://m3.material.io/)
- [Dart Language Guide](https://dart.dev/guides)

## 🤝 Support

For issues with Flutter:
- Check [Flutter Troubleshooting](https://flutter.dev/docs/testing/troubleshooting)
- Run `flutter doctor` for environment diagnostics
- Review logs with `flutter logs -d <device-id>`

## 📝 License

This project is provided as-is for educational and development purposes.

---

**Last Updated:** 2026-06-06  
**Status:** Ready for Production  
**Build:** Release v1.0.0
"# Flutter-mobile_container" 
