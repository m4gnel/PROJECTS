# 📱 PHASE 4 — Android Kotlin + Jetpack Compose App
## Branch: `dev/m2-android` · Owner: M2 · GitHub Issue: #4

---

## Paste This Into Gemini 2.5 Pro

```
=== AGRI-SAGE PHASE 4 — ANDROID KOTLIN + JETPACK COMPOSE APP ===

Run AUDIT-FIRST PROTOCOL on the entire android/ directory before writing anything.
Pay special attention to build.gradle.kts — wrong plugin versions break everything.
Print the audit table. Build only MISSING and NEEDS_WORK files.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOCKED ANDROID VERSIONS — NEVER CHANGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

compileSdk              = 35
minSdk                  = 26
targetSdk               = 35
kotlin_version          = "2.0.21"
compose_bom             = "2024.09.00"
navigation_compose      = "2.8.5"
kotlinx_serialization   = "1.7.3"
room_version            = "2.7.0"
ksp_version             = "2.0.21-1.0.27"   ← KSP only, NEVER kapt
hilt_version            = "2.52"
retrofit_version        = "2.11.0"
okhttp_version          = "4.12.0"
coroutines_version      = "1.9.0"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMMON MISTAKES TO AVOID (check existing code for these)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WRONG                                   CORRECT
kapt("...room-compiler")               ksp("androidx.room:room-compiler:2.7.0")
NavController.navigate("homeRoute")    NavController.navigate(HomeScreen())
EXTRA_LANGUAGE = "en-US"               EXTRA_LANGUAGE = "ml-IN"
Hardcoded API URL in source            BuildConfig.API_BASE_URL from local.properties
annotationProcessor for Room           KSP plugin for Room 2.7.0
100vh in layout                        height = fillMaxSize() in Compose
LazyColumn without key {}              LazyColumn { items(messages, key={it.id}) }

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TARGET FILE STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

android/
├── app/
│   ├── build.gradle.kts
│   └── src/main/
│       ├── AndroidManifest.xml
│       ├── AgriSageApplication.kt        ← @HiltAndroidApp
│       ├── MainActivity.kt               ← Single activity + NavHost
│       ├── data/
│       │   ├── local/
│       │   │   ├── AgriSageDatabase.kt   ← @Database
│       │   │   ├── dao/
│       │   │   │   ├── MessageDao.kt
│       │   │   │   ├── WeatherDao.kt
│       │   │   │   ├── MarketPriceDao.kt
│       │   │   │   └── FarmerProfileDao.kt
│       │   │   └── entities/
│       │   │       ├── CachedMessage.kt
│       │   │       ├── CachedWeather.kt
│       │   │       ├── CachedMarketPrice.kt
│       │   │       └── FarmerProfile.kt
│       │   ├── remote/
│       │   │   ├── AgriSageApiService.kt ← Retrofit interface
│       │   │   └── dto/
│       │   │       ├── ChatRequest.kt
│       │   │       ├── ChatResponse.kt
│       │   │       ├── WeatherResponse.kt
│       │   │       └── MarketResponse.kt
│       │   └── repository/
│       │       ├── ChatRepository.kt
│       │       ├── WeatherRepository.kt
│       │       └── MarketRepository.kt
│       ├── di/
│       │   ├── DatabaseModule.kt
│       │   ├── NetworkModule.kt
│       │   └── RepositoryModule.kt
│       ├── ui/
│       │   ├── theme/
│       │   │   ├── Color.kt
│       │   │   ├── Type.kt
│       │   │   └── Theme.kt
│       │   ├── screens/
│       │   │   ├── HomeScreen.kt         ← Chat UI
│       │   │   ├── DashboardScreen.kt    ← Live widgets
│       │   │   ├── AlertsScreen.kt       ← Push history
│       │   │   └── OnboardingScreen.kt   ← 3-step setup
│       │   ├── components/
│       │   │   ├── ChatBubble.kt
│       │   │   ├── WeatherCard.kt
│       │   │   ├── MarketPriceCard.kt
│       │   │   └── PestAlertBanner.kt
│       │   └── viewmodel/
│       │       ├── ChatViewModel.kt
│       │       ├── DashboardViewModel.kt
│       │       └── OnboardingViewModel.kt
│       └── util/
│           ├── SpeechRecognitionHelper.kt
│           └── FcmService.kt
├── build.gradle.kts                      ← Root build file
└── local.properties                      ← API_BASE_URL (gitignored)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BUILD.GRADLE.KTS (app level) — KEY SECTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("com.google.devtools.ksp") version "2.0.21-1.0.27"   ← KSP plugin
    id("com.google.dagger.hilt.android")
    id("org.jetbrains.kotlin.plugin.serialization")
}

android {
    compileSdk = 35
    defaultConfig {
        minSdk = 26
        targetSdk = 35
        // Reads from local.properties so URL is never committed
        val apiBaseUrl = project.findProperty("API_BASE_URL")
            ?: "http://10.0.2.2:8000/"
        buildConfigField("String", "API_BASE_URL", "\"$apiBaseUrl\"")
    }
    buildFeatures { compose = true; buildConfig = true }
    composeOptions { kotlinCompilerExtensionVersion = "1.5.15" }
}

dependencies {
    // Compose BOM — pins all compose versions together
    implementation(platform("androidx.compose:compose-bom:2024.09.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.ui:ui-tooling-preview")

    // Navigation with type safety
    implementation("androidx.navigation:navigation-compose:2.8.5")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.7.3")

    // Room with KSP
    implementation("androidx.room:room-runtime:2.7.0")
    implementation("androidx.room:room-ktx:2.7.0")
    ksp("androidx.room:room-compiler:2.7.0")             ← KSP, not kapt

    // Hilt DI
    implementation("com.google.dagger:hilt-android:2.52")
    ksp("com.google.dagger:hilt-android-compiler:2.52")   ← KSP, not kapt
    implementation("androidx.hilt:hilt-navigation-compose:1.2.0")

    // Network
    implementation("com.squareup.retrofit2:retrofit:2.11.0")
    implementation("com.squareup.retrofit2:converter-gson:2.11.0")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")

    // WorkManager for background refresh
    implementation("androidx.work:work-runtime-ktx:2.10.0")

    // Firebase FCM
    implementation(platform("com.google.firebase:firebase-bom:33.5.1"))
    implementation("com.google.firebase:firebase-messaging-ktx")

    // Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.9.0")
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NAVIGATION — TYPE-SAFE (MainActivity.kt)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// Destination definitions
@Serializable object HomeScreen
@Serializable object DashboardScreen
@Serializable object AlertsScreen
@Serializable object OnboardingScreen

// NavHost setup
NavHost(navController = navController, startDestination = HomeScreen) {
    composable<HomeScreen>     { HomeScreen(navController) }
    composable<DashboardScreen>{ DashboardScreen(navController) }
    composable<AlertsScreen>   { AlertsScreen(navController) }
    composable<OnboardingScreen>{ OnboardingScreen(navController) }
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MALAYALAM VOICE INPUT (SpeechRecognitionHelper.kt)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class SpeechRecognitionHelper(private val context: Context) {

    fun createRecognitionIntent(): Intent {
        return Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                     RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            putExtra(RecognizerIntent.EXTRA_LANGUAGE, "ml-IN")
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE, "ml-IN")
            putExtra(RecognizerIntent.EXTRA_ONLY_RETURN_LANGUAGE_PREFERENCE, false)
            putExtra(RecognizerIntent.EXTRA_PROMPT, "സംസാരിക്കുക...")  // "Speak..."
            putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1)
        }
    }

    fun extractResult(data: Intent?): String? {
        return data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
            ?.firstOrNull()
    }
}

// In HomeScreen composable, use ActivityResultLauncher:
val speechLauncher = rememberLauncherForActivityResult(
    contract = ActivityResultContracts.StartActivityForResult()
) { result ->
    if (result.resultCode == Activity.RESULT_OK) {
        speechHelper.extractResult(result.data)?.let { text ->
            chatViewModel.sendMessage(text)
        }
    }
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHAT VIEWMODEL (ChatViewModel.kt)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@HiltViewModel
class ChatViewModel @Inject constructor(
    private val chatRepository: ChatRepository,
    private val messageDao: MessageDao,
    private val farmerProfileDao: FarmerProfileDao
) : ViewModel() {

    private val _uiState = MutableStateFlow(ChatUiState())
    val uiState: StateFlow<ChatUiState> = _uiState.asStateFlow()

    fun sendMessage(text: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }

            // Save user message to Room
            val userMsg = CachedMessage(role = "user", content = text,
                                        timestamp = System.currentTimeMillis())
            messageDao.insert(userMsg)
            _uiState.update { it.copy(messages = it.messages + userMsg) }

            try {
                val profile = farmerProfileDao.getProfile() ?: return@launch
                val response = chatRepository.sendChat(
                    ChatRequest(
                        farmer_id = profile.id,
                        query     = text,
                        language  = profile.language_pref,
                        location  = mapOf(
                            "district" to profile.district,
                            "lat"      to profile.lat.toString(),
                            "lon"      to profile.lon.toString()
                        ),
                        crop = profile.primary_crop
                    )
                )
                val assistantMsg = CachedMessage(
                    role      = "assistant",
                    content   = response.answer_ml,
                    timestamp = System.currentTimeMillis()
                )
                messageDao.insert(assistantMsg)
                _uiState.update { it.copy(messages = it.messages + assistantMsg) }
            } catch (e: Exception) {
                // Offline fallback: show last 3 cached messages
                val cached = messageDao.getLastN(3)
                _uiState.update {
                    it.copy(error = "Offline — showing cached responses",
                            messages = cached)
                }
            } finally {
                _uiState.update { it.copy(isLoading = false) }
            }
        }
    }
}

data class ChatUiState(
    val messages: List<CachedMessage> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null
)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DASHBOARD — WORKMANAGER REFRESH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// In AgriSageApplication.kt, schedule once at startup:
val refreshRequest = PeriodicWorkRequestBuilder<DashboardRefreshWorker>(
    30, TimeUnit.MINUTES
).setConstraints(
    Constraints.Builder()
        .setRequiredNetworkType(NetworkType.CONNECTED)
        .build()
).build()

WorkManager.getInstance(this).enqueueUniquePeriodicWork(
    "dashboard_refresh",
    ExistingPeriodicWorkPolicy.KEEP,
    refreshRequest
)

// DashboardRefreshWorker fetches weather + market prices and saves to Room

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THEME COLORS (ui/theme/Color.kt)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

val GreenDark    = Color(0xFF14532D)
val GreenMid     = Color(0xFF16A34A)
val GreenLight   = Color(0xFF4ADE80)
val GreenSurface = Color(0xFFF0FDF4)
val AmberAlert   = Color(0xFFD97706)
val RedAlert     = Color(0xFFDC2626)
val SlateText    = Color(0xFF334155)
val SlateMid     = Color(0xFF64748B)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOCAL.PROPERTIES (gitignored — template only)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Create android/local.properties.example (committed):
  # Copy this file to local.properties and fill in values
  API_BASE_URL=https://your-railway-url.railway.app/

Add to android/.gitignore:
  local.properties

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GITHUB ISSUE PROTOCOL — PHASE 4
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After build succeeds:
  cd android && ./gradlew assembleDebug 2>&1 | tail -5
  Expected: BUILD SUCCESSFUL

  git checkout dev/m2-android
  git add -A
  git commit -m "feat(phase-4): Android Compose app — Malayalam voice, Room offline cache, live dashboard"
  git tag v0.4.0

Create GitHub Issue:
  Title: [Phase 4] Android Kotlin + Jetpack Compose App
  Labels: phase-4, android
  Assign: @M2
  Body: (list all files, PROTECTED files, paste BUILD SUCCESSFUL output,
         note: APK available at android/app/build/outputs/apk/debug/)

Print: "✅ Phase 4 committed to dev/m2-android. Issue created. Waiting for team review."
STOP — wait for confirmation before Phase 5.
```

---

## What This Phase Builds

| Screen | Key Features |
|---|---|
| `HomeScreen` | Chat bubbles, Malayalam voice input, loading shimmer |
| `DashboardScreen` | Live weather widget, APMC price card, pest alert banner |
| `AlertsScreen` | Push notification history list |
| `OnboardingScreen` | 3-step: name+language → GPS/district → crop selection |

## GitHub Issue Created After This Phase

```
Title: [Phase 4] Android Kotlin + Jetpack Compose App
Branch: dev/m2-android
Labels: phase-4, android
Assign to: M2
APK path: android/app/build/outputs/apk/debug/app-debug.apk
```

---

> **Next:** Paste `06-phase5-deploy.md` after Issue #4 is reviewed and merged
