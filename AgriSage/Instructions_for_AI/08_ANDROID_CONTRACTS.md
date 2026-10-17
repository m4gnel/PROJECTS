# 08_ANDROID_CONTRACTS.md — Exact Android/Kotlin/Compose Contracts
# ⚠️ ALL SCREENS AND VIEWMODELS MUST MATCH THESE SIGNATURES EXACTLY.

---

## Navigation Routes — Screen.kt (COPY EXACTLY)

```kotlin
package com.agrisage.app.navigation

import kotlinx.serialization.Serializable

sealed class Screen {
    @Serializable object Splash : Screen()
    @Serializable object Onboarding : Screen()
    @Serializable object Home : Screen()
    @Serializable object Advisor : Screen()
    @Serializable object Fields : Screen()
    @Serializable data class FieldDetail(val fieldId: String) : Screen()
    @Serializable object Weather : Screen()
    @Serializable object Alerts : Screen()
    @Serializable object Profile : Screen()
}
```

---

## AppNavHost.kt — Navigation Setup (COPY EXACTLY)

```kotlin
package com.agrisage.app.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.toRoute
import com.agrisage.app.ui.screens.splash.SplashScreen
import com.agrisage.app.ui.screens.onboarding.OnboardingScreen
import com.agrisage.app.ui.screens.home.HomeScreen
import com.agrisage.app.ui.screens.advisor.AdvisorScreen
import com.agrisage.app.ui.screens.fields.FieldsScreen
import com.agrisage.app.ui.screens.fields.FieldDetailScreen
import com.agrisage.app.ui.screens.weather.WeatherScreen
import com.agrisage.app.ui.screens.alerts.AlertsScreen
import com.agrisage.app.ui.screens.profile.ProfileScreen

@Composable
fun AppNavHost(navController: NavHostController) {
    NavHost(navController = navController, startDestination = Screen.Splash) {
        composable<Screen.Splash> { SplashScreen(navController) }
        composable<Screen.Onboarding> { OnboardingScreen(navController) }
        composable<Screen.Home> { HomeScreen(navController) }
        composable<Screen.Advisor> { AdvisorScreen(navController) }
        composable<Screen.Fields> { FieldsScreen(navController) }
        composable<Screen.FieldDetail> { backStackEntry ->
            val args = backStackEntry.toRoute<Screen.FieldDetail>()
            FieldDetailScreen(navController, fieldId = args.fieldId)
        }
        composable<Screen.Weather> { WeatherScreen(navController) }
        composable<Screen.Alerts> { AlertsScreen(navController) }
        composable<Screen.Profile> { ProfileScreen(navController) }
    }
}
```

---

## Screen 1: SplashScreen.kt

```kotlin
@Composable
fun SplashScreen(navController: NavHostController) {
    // Shows animated Agri-SAGE logo for 2 seconds
    // Checks DataStore for auth token
    // Navigates to: Screen.Home if logged in, else Screen.Onboarding
    // Animation: logo scale 0.5→1.0 + fade in, duration 600ms
    // Background: SageGreen900
}
```

---

## Screen 2: OnboardingScreen.kt + OnboardingViewModel.kt

```kotlin
// ViewModel
data class OnboardingUiState(
    val currentPage: Int = 0,        // 0, 1, 2
    val selectedLanguage: String = "ml",  // "ml", "en", "ta", "hi"
    val farmerName: String = "",
    val village: String = "",
    val district: String = "",
    val isLoading: Boolean = false,
    val error: String? = null
)

@HiltViewModel
class OnboardingViewModel @Inject constructor(
    private val authRepository: AuthRepository,
    private val dataStore: DataStore<Preferences>
) : ViewModel() {
    val uiState: StateFlow<OnboardingUiState>
    fun selectLanguage(lang: String)
    fun updateName(name: String)
    fun updateVillage(village: String)
    fun updateDistrict(district: String)
    fun nextPage()
    fun previousPage()
    fun completeOnboarding(onSuccess: () -> Unit)
}

// Screen — 3 pages:
// Page 0: Language selection (4 chips: Malayalam, English, Tamil, Hindi)
// Page 1: Farmer details form (name, village, district)
// Page 2: Permission requests (location, notifications) + "Get Started" button
@Composable
fun OnboardingScreen(navController: NavHostController)
```

---

## Screen 3: HomeScreen.kt + HomeViewModel.kt

```kotlin
data class HomeUiState(
    val farmerName: String = "",
    val weather: WeatherSummary? = null,
    val activeAlerts: List<AlertItem> = emptyList(),
    val todayTasks: List<TaskItem> = emptyList(),
    val isLoading: Boolean = false,
    val lastUpdated: String = ""
)

data class WeatherSummary(
    val tempCelsius: Float,
    val condition: String,     // "Sunny", "Rainy", "Cloudy"
    val humidity: Int,
    val rainfallMm: Float
)

data class AlertItem(
    val id: String,
    val severity: AlertSeverity,   // CRITICAL, WARNING, INFO, SUCCESS
    val title: String,
    val message: String
)

data class TaskItem(
    val id: String,
    val title: String,
    val due: String,
    val isDone: Boolean
)

enum class AlertSeverity { CRITICAL, WARNING, INFO, SUCCESS }

@HiltViewModel
class HomeViewModel @Inject constructor(
    private val weatherRepository: WeatherRepository,
    private val alertRepository: AlertRepository
) : ViewModel() {
    val uiState: StateFlow<HomeUiState>
    fun refresh()
    fun dismissAlert(alertId: String)
}

// Screen layout:
// - Top: greeting + date chip
// - WeatherChip (current temp, condition)
// - QuickAction grid (2×2): Ask Advisor, My Fields, Weather, Alerts
// - AlertStrip (horizontal scroll of activeAlerts)
// - TodayTasks list
@Composable
fun HomeScreen(navController: NavHostController)
```

---

## Screen 4: AdvisorScreen.kt + AdvisorViewModel.kt

```kotlin
data class ChatMessage(
    val id: String,
    val content: String,
    val isFromUser: Boolean,
    val timestamp: Long,
    val language: String
)

data class AdvisorUiState(
    val messages: List<ChatMessage> = emptyList(),
    val currentInput: String = "",
    val isTyping: Boolean = false,  // AI is responding
    val selectedLanguage: String = "ml",
    val isVoiceRecording: Boolean = false,
    val sessionId: String = "",
    val error: String? = null
)

@HiltViewModel
class AdvisorViewModel @Inject constructor(
    private val chatRepository: ChatRepository
) : ViewModel() {
    val uiState: StateFlow<AdvisorUiState>
    fun updateInput(text: String)
    fun sendMessage()
    fun startVoiceRecording()
    fun stopVoiceRecording()
    fun selectLanguage(lang: String)
    fun clearError()
}

// Screen layout:
// - Top bar: "AI Advisor" title + language chip switcher (ML/EN/TA/HI)
// - LazyColumn: chat messages (ChatBubble components)
//   - User messages: right-aligned, SageGreen500 background
//   - AI messages: left-aligned, SurfaceDim background, Agri-SAGE avatar
// - Typing indicator: 3-dot animation when isTyping=true
// - Bottom: TextField + voice mic button + send button
@Composable
fun AdvisorScreen(navController: NavHostController)
```

---

## Screen 5: FieldsScreen.kt + FieldDetailScreen.kt + FieldsViewModel.kt

```kotlin
data class FieldModel(
    val id: String,
    val name: String,
    val areaSqM: Float,
    val cropName: String,
    val cropVariety: String,
    val sowingDate: String,
    val healthStatus: String,  // "good", "warning", "critical"
    val latitude: Double,
    val longitude: Double
)

data class FieldsUiState(
    val fields: List<FieldModel> = emptyList(),
    val isLoading: Boolean = false,
    val showAddDialog: Boolean = false,
    val error: String? = null
)

@HiltViewModel
class FieldsViewModel @Inject constructor(
    private val fieldRepository: FieldRepository
) : ViewModel() {
    val uiState: StateFlow<FieldsUiState>
    fun loadFields()
    fun showAddDialog()
    fun hideAddDialog()
    fun addField(name: String, areaSqM: Float, lat: Double, lon: Double)
    fun deleteField(fieldId: String)
}

// FieldsScreen layout:
// - Map placeholder (GoogleMap composable, markers for each field)
// - LazyColumn of FieldCard components
// - FAB: "+" to add new field
@Composable
fun FieldsScreen(navController: NavHostController)

// FieldDetailScreen layout:
// - Field name, area, crop info
// - Current NDVI value with color indicator
// - Irrigation schedule
// - Fertilizer recommendation
// - Recent alerts for this field
@Composable
fun FieldDetailScreen(navController: NavHostController, fieldId: String)
```

---

## Screen 6: WeatherScreen.kt + WeatherViewModel.kt

```kotlin
data class WeatherDay(
    val date: String,
    val maxTempC: Float,
    val minTempC: Float,
    val rainfallMm: Float,
    val condition: String,
    val uvIndex: Float
)

data class WeatherUiState(
    val currentTemp: Float = 0f,
    val currentCondition: String = "",
    val humidity: Int = 0,
    val windKmh: Float = 0f,
    val uvIndex: Float = 0f,
    val forecast7Day: List<WeatherDay> = emptyList(),
    val agriAdvisory: String = "",   // AI-generated farm advisory
    val isLoading: Boolean = false,
    val lastUpdated: String = ""
)

@HiltViewModel
class WeatherViewModel @Inject constructor(
    private val weatherRepository: WeatherRepository
) : ViewModel() {
    val uiState: StateFlow<WeatherUiState>
    fun refresh()
}

// Screen layout:
// - Large current weather card (temp, condition, humidity, wind)
// - 7-day forecast horizontal scroll (WeatherDay cards)
// - Agri-SAGE Advisory banner (AI recommendation based on weather)
@Composable
fun WeatherScreen(navController: NavHostController)
```

---

## Screen 7: AlertsScreen.kt + AlertsViewModel.kt

```kotlin
data class AlertsUiState(
    val allAlerts: List<AlertItem> = emptyList(),
    val filteredAlerts: List<AlertItem> = emptyList(),
    val selectedFilter: AlertSeverity? = null,   // null = show all
    val isLoading: Boolean = false,
    val unreadCount: Int = 0
)

@HiltViewModel
class AlertsViewModel @Inject constructor(
    private val alertRepository: AlertRepository
) : ViewModel() {
    val uiState: StateFlow<AlertsUiState>
    fun filterBySeverity(severity: AlertSeverity?)
    fun markAsRead(alertId: String)
    fun markAllAsRead()
}

// Screen layout:
// - Filter chips: All / Critical / Warning / Info (horizontal scroll)
// - Unread count badge
// - LazyColumn of AlertCard components
//   - Color-coded by severity (Red/Gold/Blue/Green)
//   - Swipe-to-dismiss to mark as read
@Composable
fun AlertsScreen(navController: NavHostController)
```

---

## Screen 8: ProfileScreen.kt + ProfileViewModel.kt

```kotlin
data class FarmerProfile(
    val id: String,
    val name: String,
    val phone: String,
    val village: String,
    val district: String,
    val totalFieldsSqM: Float,
    val primaryCrop: String,
    val preferredLanguage: String
)

data class ProfileUiState(
    val profile: FarmerProfile? = null,
    val isEditing: Boolean = false,
    val offlineModeEnabled: Boolean = false,
    val notificationsEnabled: Boolean = true,
    val selectedLanguage: String = "ml",
    val isLoading: Boolean = false,
    val isSaving: Boolean = false
)

@HiltViewModel
class ProfileViewModel @Inject constructor(
    private val authRepository: AuthRepository,
    private val dataStore: DataStore<Preferences>
) : ViewModel() {
    val uiState: StateFlow<ProfileUiState>
    fun enableEditing()
    fun saveProfile(profile: FarmerProfile)
    fun toggleOfflineMode()
    fun toggleNotifications()
    fun changeLanguage(lang: String)
    fun logout(onLoggedOut: () -> Unit)
}

// Screen layout:
// - Profile photo (initials avatar) + name + village
// - Farm Stats section: total area, number of fields, primary crop
// - Preferences section: language picker, offline toggle, notifications toggle
// - Account section: edit profile button, logout button
@Composable
fun ProfileScreen(navController: NavHostController)
```

---

## BottomNavBar.kt Component (COPY EXACTLY)

```kotlin
@Composable
fun BottomNavBar(
    currentRoute: String,
    onNavigate: (Screen) -> Unit
) {
    NavigationBar(containerColor = SageGreen900) {
        val items = listOf(
            BottomNavItem(Screen.Home, Icons.Rounded.Home, "Home"),
            BottomNavItem(Screen.Advisor, Icons.Rounded.SmartToy, "Advisor"),
            BottomNavItem(Screen.Fields, Icons.Rounded.Landscape, "Fields"),
            BottomNavItem(Screen.Weather, Icons.Rounded.WbSunny, "Weather"),
            BottomNavItem(Screen.Profile, Icons.Rounded.Person, "Profile")
        )
        items.forEach { item ->
            NavigationBarItem(
                selected = currentRoute == item.screen::class.simpleName,
                onClick = { onNavigate(item.screen) },
                icon = { Icon(item.icon, contentDescription = item.label) },
                label = { Text(item.label, style = MaterialTheme.typography.labelSmall) },
                colors = NavigationBarItemDefaults.colors(
                    selectedIconColor = SageGreen300,
                    unselectedIconColor = Color.White.copy(alpha = 0.6f),
                    indicatorColor = SageGreen700
                )
            )
        }
    }
}

data class BottomNavItem(val screen: Screen, val icon: ImageVector, val label: String)
```

---

## Room Database Entity Examples

```kotlin
// WeatherEntity.kt
@Entity(tableName = "weather_cache")
data class WeatherEntity(
    @PrimaryKey val id: String,
    val lat: Double,
    val lon: Double,
    val tempCelsius: Float,
    val humidity: Int,
    val rainfallMm: Float,
    val windKmh: Float,
    val condition: String,
    val fetchedAt: Long  // System.currentTimeMillis()
)

// AlertEntity.kt
@Entity(tableName = "alerts")
data class AlertEntity(
    @PrimaryKey val id: String,
    val severity: String,  // "CRITICAL", "WARNING", "INFO", "SUCCESS"
    val title: String,
    val message: String,
    val isRead: Boolean = false,
    val createdAt: Long
)

// ChatMessageEntity.kt
@Entity(tableName = "chat_messages")
data class ChatMessageEntity(
    @PrimaryKey val id: String,
    val sessionId: String,
    val content: String,
    val isFromUser: Boolean,
    val language: String,
    val timestamp: Long
)

// FieldEntity.kt
@Entity(tableName = "fields")
data class FieldEntity(
    @PrimaryKey val id: String,
    val farmerId: String,
    val name: String,
    val areaSqM: Float,
    val cropName: String,
    val cropVariety: String,
    val sowingDate: String,
    val latitude: Double,
    val longitude: Double,
    val lastNdvi: Float = 0f,
    val updatedAt: Long
)
```

---

## ApiService.kt — Retrofit Interface (COPY EXACTLY)

```kotlin
package com.agrisage.app.data.remote

import com.agrisage.app.data.remote.dto.*
import retrofit2.Response
import retrofit2.http.*

interface ApiService {

    // Auth
    @POST("auth/register")
    suspend fun register(@Body request: RegisterRequest): Response<TokenResponse>

    @POST("auth/token")
    @FormUrlEncoded
    suspend fun login(
        @Field("username") username: String,
        @Field("password") password: String
    ): Response<TokenResponse>

    // Farmer
    @GET("farmers/me")
    suspend fun getMyProfile(): Response<FarmerDto>

    @PUT("farmers/me")
    suspend fun updateProfile(@Body request: UpdateFarmerRequest): Response<FarmerDto>

    // Fields
    @GET("fields/")
    suspend fun getFields(): Response<List<FieldDto>>

    @POST("fields/")
    suspend fun createField(@Body request: CreateFieldRequest): Response<FieldDto>

    @DELETE("fields/{fieldId}")
    suspend fun deleteField(@Path("fieldId") fieldId: String): Response<Unit>

    // Chat
    @POST("chat/")
    suspend fun sendMessage(@Body request: ChatRequest): Response<ChatResponse>

    // Weather
    @GET("weather/current")
    suspend fun getCurrentWeather(
        @Query("lat") lat: Double,
        @Query("lon") lon: Double
    ): Response<WeatherCurrentDto>

    @GET("weather/forecast")
    suspend fun getWeatherForecast(
        @Query("lat") lat: Double,
        @Query("lon") lon: Double
    ): Response<WeatherForecastDto>

    // Alerts
    @GET("alerts/")
    suspend fun getAlerts(@Query("unread_only") unreadOnly: Boolean = false): Response<List<AlertDto>>

    @POST("alerts/mark-read")
    suspend fun markAlertsRead(@Body request: MarkReadRequest): Response<Unit>

    // Advisory
    @POST("advisory/ask")
    suspend fun askAdvisory(@Body request: AdvisoryRequest): Response<AdvisoryResponse>
}
```

---

## MainActivity.kt Pattern (COPY EXACTLY)

```kotlin
@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            AgriSageTheme {
                val navController = rememberNavController()
                Scaffold(
                    bottomBar = {
                        val currentBackStackEntry by navController.currentBackStackEntryAsState()
                        val currentRoute = currentBackStackEntry?.destination?.route
                        // Show bottom bar only on main screens
                        val showBottomBar = currentRoute in listOf(
                            Screen.Home::class.qualifiedName,
                            Screen.Advisor::class.qualifiedName,
                            Screen.Fields::class.qualifiedName,
                            Screen.Weather::class.qualifiedName,
                            Screen.Profile::class.qualifiedName
                        )
                        if (showBottomBar) {
                            BottomNavBar(
                                currentRoute = currentRoute ?: "",
                                onNavigate = { screen ->
                                    navController.navigate(screen) {
                                        popUpTo(navController.graph.findStartDestination().id) {
                                            saveState = true
                                        }
                                        launchSingleTop = true
                                        restoreState = true
                                    }
                                }
                            )
                        }
                    }
                ) { innerPadding ->
                    AppNavHost(navController = navController)
                }
            }
        }
    }
}
```
