# AGRI-SAGE — ANDROID SPECIFICATION

## Stack
Kotlin 2.0.21 | Compose BOM 2024.12.01 | Navigation 2.8.5 (@Serializable)
Room 2.7.0 (KSP) | Hilt 2.53 | CameraX 1.4.0 | ONNX Runtime 1.20.0
WorkManager 2.10.0 | Firebase Messaging 24.1.0 | Retrofit 2.11.0 | Coil 2.7.0

## 30 Color Tokens (EXACT HEX)
```kotlin
val ColorPrimary = Color(0xFF2D7D2D)
val ColorPrimaryDark = Color(0xFF1A5C1A)
val ColorPrimaryLight = Color(0xFFE8F5E8)
val ColorPrimaryContainer = Color(0xFFC8E6C9)
val ColorSecondary = Color(0xFF558B2F)
val ColorSecondaryLight = Color(0xFFF1F8E9)
val ColorRiskCritical = Color(0xFFC62828)
val ColorRiskHigh = Color(0xFFE65100)
val ColorRiskMedium = Color(0xFFF57F17)
val ColorRiskLow = Color(0xFF2E7D32)
val ColorConfidenceConfirmed = Color(0xFF1B5E20)
val ColorConfidenceLikely = Color(0xFF2E7D32)
val ColorConfidencePossible = Color(0xFFF57F17)
val ColorConfidenceUncertain = Color(0xFFBF360C)
val ColorConfidenceInsufficient = Color(0xFF757575)
val ColorSurface = Color(0xFFFAFAFA)
val ColorSurfaceVariant = Color(0xFFF5F5F5)
val ColorOnSurface = Color(0xFF212121)
val ColorOnSurfaceSecondary = Color(0xFF616161)
val ColorOnSurfaceTertiary = Color(0xFF9E9E9E)
val ColorOutline = Color(0xFFBDBDBD)
val ColorWarningBg = Color(0xFFFFF9C4)
val ColorWarningText = Color(0xFFF57F17)
val ColorInfoBg = Color(0xFFE3F2FD)
val ColorOfflineBanner = Color(0xFFFFF3E0)
val ColorOfflineText = Color(0xFFE65100)
val ColorCachedLabel = Color(0xFFFF8F00)
val ColorSchemeBg = Color(0xFFEDE7F6)
val ColorSchemeText = Color(0xFF4527A0)
val ColorOnPrimary = Color(0xFFFFFFFF)
```

## Typography — Noto Sans (supports Malayalam)
displayLarge: Bold 32sp/40sp | headlineLarge: Bold 24sp/32sp
headlineMedium: SemiBold 20sp/28sp | headlineSmall: SemiBold 18sp/24sp
bodyLarge: Normal 16sp/24sp | bodyMedium: Normal 14sp/20sp
bodySmall: Normal 12sp/16sp | labelMedium: Medium 12sp/16sp

## Navigation Routes (type-safe @Serializable)
```kotlin
@Serializable object HomeRoute
@Serializable object CameraRoute
@Serializable data class AdvisoryRoute(val advisoryId: String)
@Serializable object FarmRoute
@Serializable object AlertsRoute
@Serializable object ProfileRoute
@Serializable object OnboardingRoute
@Serializable object OtpRoute
@Serializable object FarmSetupRoute
```

## Screen Specs

### Home Screen
TopAppBar: bg=ColorPrimaryDark, farmName headlineSmall white left, sync icon right
AlertBanner: OFFLINE=ColorOfflineBanner+ColorOfflineText, LIMITED=ColorWarningBg — shown only when not CONNECTED
MorningBriefingCard: bg=ColorPrimaryLight corner=16dp padding=16dp
  Rows: stage+icon | risk+level | weather+2word | action+bold | speaker button
2×2 ActionTile grid: corner=12dp bg=white elevation=2dp minHeight=100dp spacing=12dp margin=16dp
  Check Crop(photo_camera,ColorPrimary) | Farm Weather(partly_cloudy_day)
  View Risks(warning,ColorRiskMedium) | My Schemes(account_balance,ColorSchemeText)
BottomNavBar: 5 items Home|Farm|Diagnose|Alerts|Profile — Diagnose elevated circular ColorPrimary

### Camera Screen
Full-screen CameraX preview
QualityIndicatorBar: 8dp height, animateColorAsState 200ms
  GREEN=0xFF4CAF50 OKAY=0xFFFF9800 POOR=0xFFF44336
Quality messages: 'Good — tap to capture' | 'Hold steady' | 'Too dark — move to shade'
Capture button: 80dp circular, white border 4dp, bottom 48dp, haptic feedback
On POOR: AlertDialog with specific message + Retry button
CropChip top-right: tappable → crop picker BottomSheet

### Advisory Result Screen
ConfidenceBadge: pill 32dp corner 16dp, colors per confidence_state, text white
RiskLevelBadge: pill 28dp, CRITICAL=0xFFC62828 HIGH=0xFFE65100 MEDIUM=0xFFF57F17 LOW=0xFF2E7D32
EvidenceCard: bg=ColorInfoBg corner=12dp left-border 2dp ColorPrimary, expandable (default open)
ActionCard: bg=ColorPrimaryLight corner=16dp 2dp border ColorPrimary, icons per field
ModelledEstimateLabel: italic bodySmall Color(0xFF9E9E9E)
  text: "* Modelled estimate — actual results vary by field conditions"
  MANDATORY under every yield/return figure — no exceptions
FeedbackRow: thumbs up/down 48dp each

## Minimum Touch Target: 48×48dp — no exceptions

## Key Malayalam Strings
nav_diagnose = "വിള പരിശോധിക്കുക"
adv_confidence_likely = "സാധ്യത കൂടുതൽ"
adv_confidence_uncertain = "ഉറപ്പില്ല"
adv_modelled = "മോഡൽ കണക്ക്‌ *"
offline_banner = "ഇന്റർനെറ്റ് ഇല്ല — സേവ് ചെയ്ത ഡേറ്റ"
cam_blur = "ഫോട്ടോ മങ്ങിയിരിക്കുന്നു — ഉറച്ചു പിടിക്കുക"
cam_good = "നല്ലത് — ഫോട്ടോ എടുക്കുക"
scheme_caveat = "അന്തിമ യോഗ്യത ബന്ധപ്പെട്ട അധികാരി നിർണ്ണയിക്കും"

## Offline Advisory Flow
1. Run local ONNX (singleton — load once)
2. Load backend/data/offline_templates_ml.json from assets/
3. Fill slots: {crop} {disease} {confidence} {action}
4. Show banner: "ഇന്റർനെറ്റ് ഇല്ല — ഓഫ്‌ലൈൻ വിശകലനം"
5. Mark advisory isOffline=true
