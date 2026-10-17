# 🤝 NGO Volunteer Connect — Cross-Platform Flutter Mobile Application

[![Flutter](https://img.shields.io/badge/Flutter-3.x-blue.svg)](#)
[![Dart](https://img.shields.io/badge/Dart-3.x-0075C9.svg)](#)
[![Platform](https://img.shields.io/badge/Platforms-Android%20%7C%20iOS%20%7C%20Web-green.svg)](#)
[![Material Design](https://img.shields.io/badge/UI-Material%20Design%203-purple.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#)

**NGO Volunteer Connect** is a feature-complete, modern cross-platform mobile application engineered in Flutter and Dart to connect passionate volunteers with non-profit organizations, social initiatives, and community impact events.

---

## ✨ Features & User Flows

- 🌟 **Onboarding & Splash Experience**: Animated brand splash screen with seamless session restoration.
- 🔐 **Authentication & Interest Personalization**: Secure authentication supporting interest profiling (Environment, Education, Healthcare, Animal Welfare, Crisis Relief).
- 📅 **Dynamic Event Discovery**: Filterable event feed with category tags, date ranges, location markers, and urgency indicators.
- 🎯 **Event Lifecycle & Engagement**:
  - Detailed initiative briefing with organizer verification and volunteer quotas.
  - One-tap "Join Event" commitment with confirmation dialogue.
  - Interactive attendee rosters and cancellation handling.
- 👤 **Volunteer Profile & Badging**:
  - Comprehensive history of attended and upcoming volunteer events.
  - Impact hours tracker and community service credentials.
- 💾 **Offline-Ready Resilience**: Persistent local caching of feeds and user preferences using SharedPreferences and SQLite.

---

## 🏗️ Architecture & Project Structure

```
ngo_volunteer_app/
├── lib/
│   ├── main.dart             # Application root, routing & Theme configuration
│   ├── config/               # Color tokens, constants, typography & theme system
│   ├── models/               # Data entities (User, VolunteerEvent, Category)
│   ├── services/             # Local database, mock API, and storage abstraction
│   ├── screens/              # UI screens (Splash, Login, Home, EventDetails, Profile)
│   └── widgets/              # Reusable components (EventCard, CustomButton, StatusBadge)
├── test/
│   ├── unit/                 # Unit tests for models and business logic
│   ├── integration/          # End-to-end user journey tests
│   └── widget_test.dart      # Flutter widget interaction tests
├── pubspec.yaml              # App dependencies & asset definitions
└── README.md                 # Project documentation
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Flutter SDK (v3.0.0 or higher)
- Android Studio / Android SDK (for Android builds) or Xcode (for iOS builds)

### Installation & Run
```bash
# 1. Fetch dependencies
flutter pub get

# 2. Check environment
flutter doctor

# 3. Launch on connected device / emulator
flutter run
```

### Running Tests
Execute the comprehensive test suite:
```bash
# Run unit and widget tests
flutter test
```

---

## 🎨 Design System
- **Theme**: Material Design 3 with custom brand elevation and rounded corners.
- **Color Palette**:
  - **Primary**: Deep Forest Green (`#1E5E3A`) — representing sustainability and community growth.
  - **Accent**: Warm Amber (`#EAA023`) — representing enthusiasm and action.
  - **Neutral**: Crisp slate and soft ivory surfaces for maximum contrast and accessibility.

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.