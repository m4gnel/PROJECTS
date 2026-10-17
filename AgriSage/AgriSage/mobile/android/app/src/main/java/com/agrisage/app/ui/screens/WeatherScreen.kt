package com.agrisage.app.ui.screens

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.agrisage.app.ui.components.AgriBottomNav
import com.agrisage.app.ui.components.FarmIllustration
import com.agrisage.app.ui.components.WeatherVisualMode
import com.agrisage.app.ui.components.tactilePress
import com.agrisage.app.ui.theme.*
import kotlin.math.cos
import kotlin.math.sin

/**
 * Screen 6: Weather & Forecast (Replicated from Reference Reel 1 - DailyFlutterUI Weather)
 * Route: Weather
 *
 * Features:
 * - Top Bar: Circular white back button, "📍 Green Valley Farm ⌵" pill, circular refresh button
 * - Hero Weather Header: Huge 26°C with dynamic condition text
 * - Segmented Weather Mode Selector: 5 interactive states (☀️, ⛅, 💨, 🌧️, 🌈) with sliding indicator
 * - Dynamic Farm Landscape Illustration: Canvas vector graphics reacting to the selected weather mode
 * - "Today's conditions" Rounded Bottom Sheet (32dp top radius):
 *   - Temperature Card: Golden Bezier trend curve with animated indicator
 *   - Humidity Card: Liquid capsule vertical level gauge
 *   - Wind Card: Live rotating mini-turbine graphic
 *   - Rain Chance Card: Probability progress meter
 * - 7-Day Forecast row & AI Farming Advice Banner
 */

data class DayForecast(
    val dayName: String,
    val condition: String,
    val highC: Float,
    val lowC: Float,
    val isToday: Boolean = false
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WeatherScreen(navController: NavController) {
    var selectedWeatherMode by remember { mutableStateOf(WeatherVisualMode.RAINBOW) }

    val forecast = listOf(
        DayForecast("Today", "☀️", 33f, 24f, isToday = true),
        DayForecast("Tue", "⛅", 31f, 23f),
        DayForecast("Wed", "🌧️", 27f, 21f),
        DayForecast("Thu", "🌧️", 26f, 20f),
        DayForecast("Fri", "⛅", 29f, 22f),
        DayForecast("Sat", "☀️", 32f, 23f),
        DayForecast("Sun", "☀️", 34f, 25f),
    )

    // Dynamic temperature and description based on selected weather mode
    val (tempDisplay, conditionText) = when (selectedWeatherMode) {
        WeatherVisualMode.SUNNY -> "28°C" to "Bright & Sunny · Clear skies"
        WeatherVisualMode.PARTLY_CLOUDY -> "27°C" to "Partly Cloudy · Mild breeze"
        WeatherVisualMode.WINDY -> "24°C" to "Windy · 28 km/h gusts"
        WeatherVisualMode.RAINY -> "22°C" to "Rain Shower · 12mm precipitation"
        WeatherVisualMode.RAINBOW -> "26°C" to "Clearing up · Rainbow out"
    }

    Scaffold(
        topBar = {
            // Replicated Reel 1 Top Bar
            Surface(
                color = Color.White,
                shadowElevation = 0.5.dp
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .statusBarsPadding()
                        .padding(horizontal = 20.dp, vertical = 12.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    // Circular White Back Button
                    Box(
                        modifier = Modifier
                            .size(42.dp)
                            .clip(CircleShape)
                            .background(Color.White)
                            .border(1.dp, Color(0xFFE2E8F0), CircleShape)
                            .clickable { navController.popBackStack() },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Back",
                            tint = Color(0xFF1E293B),
                            modifier = Modifier.size(20.dp)
                        )
                    }

                    // Location Pill
                    Surface(
                        color = Color(0xFFF1F5F9),
                        shape = RoundedCornerShape(20.dp),
                        modifier = Modifier.height(38.dp)
                    ) {
                        Row(
                            modifier = Modifier.padding(horizontal = 14.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text("📍", fontSize = 14.sp)
                            Spacer(Modifier.width(6.dp))
                            Text(
                                text = "Green Valley Farm",
                                fontSize = 14.sp,
                                fontWeight = FontWeight.Bold,
                                color = Color(0xFF0F172A)
                            )
                            Spacer(Modifier.width(4.dp))
                            Text(
                                text = "⌵",
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold,
                                color = Color(0xFF64748B)
                            )
                        }
                    }

                    // Circular Refresh Button
                    Box(
                        modifier = Modifier
                            .size(42.dp)
                            .clip(CircleShape)
                            .background(Color.White)
                            .border(1.dp, Color(0xFFE2E8F0), CircleShape)
                            .clickable { /* Refresh weather */ },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = Icons.Default.Refresh,
                            contentDescription = "Refresh",
                            tint = Color(0xFF1E293B),
                            modifier = Modifier.size(20.dp)
                        )
                    }
                }
            }
        },
        bottomBar = {
            AgriBottomNav(
                currentRoute = "weather",
                onNavigate = { route ->
                    when (route) {
                        "home" -> navController.navigate(com.agrisage.app.navigation.Home) { popUpTo(com.agrisage.app.navigation.Home) { inclusive = true } }
                        "advisor" -> navController.navigate(com.agrisage.app.navigation.Advisor)
                        "fields" -> navController.navigate(com.agrisage.app.navigation.Fields)
                        "profile" -> navController.navigate(com.agrisage.app.navigation.Profile)
                    }
                }
            )
        }
    ) { innerPadding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .background(Color(0xFFF8FAFC)),
            contentPadding = PaddingValues(bottom = 32.dp)
        ) {
            // ── HERO TEMPERATURE & CONDITIONS HEADER ──
            item {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 24.dp, vertical = 8.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(
                        text = tempDisplay,
                        fontSize = 54.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color(0xFF0F172A),
                        letterSpacing = (-1).sp
                    )
                    Spacer(Modifier.height(4.dp))
                    Text(
                        text = conditionText,
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Medium,
                        color = Color(0xFF64748B)
                    )

                    Spacer(Modifier.height(16.dp))

                    // ── SEGMENTED WEATHER MODE SELECTOR (Reel 1) ──
                    WeatherModeSegmentedPill(
                        selectedMode = selectedWeatherMode,
                        onModeSelected = { selectedWeatherMode = it }
                    )
                }
            }

            // ── DYNAMIC FARM LANDSCAPE ILLUSTRATION ──
            item {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 6.dp)
                        .height(230.dp)
                        .shadow(4.dp, RoundedCornerShape(24.dp), ambientColor = Color(0x14000000))
                        .clip(RoundedCornerShape(24.dp))
                ) {
                    FarmIllustration(
                        modifier = Modifier.fillMaxSize(),
                        weatherMode = selectedWeatherMode,
                        isAnimated = true
                    )
                }
            }

            // ── "TODAY'S CONDITIONS" BOTTOM SHEET SECTION (Reel 1) ──
            item {
                Surface(
                    color = Color.White,
                    shape = RoundedCornerShape(topStart = 32.dp, topEnd = 32.dp),
                    shadowElevation = 6.dp,
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 10.dp)
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(20.dp)
                    ) {
                        // Section Header
                        Text(
                            text = "Today's conditions",
                            fontSize = 19.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFF0F172A)
                        )
                        Spacer(Modifier.height(4.dp))
                        Text(
                            text = "Mon, 5 Oct · The rain has passed. Soil is moist and a rainbow is out.",
                            fontSize = 12.sp,
                            color = Color(0xFF64748B),
                            lineHeight = 16.sp
                        )

                        Spacer(Modifier.height(18.dp))

                        // ── 2x2 ENVIRONMENTAL METRIC CARDS ──
                        // Row 1: Temperature Arc + Humidity Liquid Meter
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            // 1. Temperature Curve Card
                            TemperatureTrendCard(
                                currentTemp = 26,
                                feelsLike = 28,
                                modifier = Modifier.weight(1f)
                            )

                            // 2. Humidity Liquid Level Card
                            HumidityMeterCard(
                                humidityPercent = 77,
                                dewPoint = 21,
                                modifier = Modifier.weight(1f)
                            )
                        }

                        Spacer(Modifier.height(12.dp))

                        // Row 2: Wind Turbine + Rain Probability
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            // 3. Wind Speed Card with Rotating Mini Turbine
                            WindSpeedCard(
                                windSpeedKmh = 12,
                                direction = "NW · Gentle breeze",
                                modifier = Modifier.weight(1f)
                            )

                            // 4. Rain Chance Probability Card
                            RainProbabilityCard(
                                chancePercent = 10,
                                timing = "Expected at 6 PM",
                                modifier = Modifier.weight(1f)
                            )
                        }

                        Spacer(Modifier.height(24.dp))

                        // ── 7-DAY FORECAST ROW ──
                        Text(
                            text = "7-Day Forecast",
                            fontSize = 17.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFF0F172A)
                        )
                        Spacer(Modifier.height(12.dp))
                        LazyRow(
                            horizontalArrangement = Arrangement.spacedBy(10.dp)
                        ) {
                            items(forecast) { day ->
                                ForecastDayCard(day)
                            }
                        }

                        Spacer(Modifier.height(22.dp))

                        // ── AI FARMING WEATHER ADVISORY BANNER ──
                        Surface(
                            modifier = Modifier.fillMaxWidth(),
                            color = Color(0xFFF0FDF4),
                            shape = RoundedCornerShape(18.dp),
                            border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFBBF7D0))
                        ) {
                            Row(
                                modifier = Modifier.padding(16.dp),
                                verticalAlignment = Alignment.Top
                            ) {
                                Text("🌾", fontSize = 24.sp)
                                Spacer(Modifier.width(12.dp))
                                Column {
                                    Text(
                                        text = "Agri-SAGE Smart Weather Advisory",
                                        fontWeight = FontWeight.Bold,
                                        color = Color(0xFF166534),
                                        fontSize = 13.sp
                                    )
                                    Spacer(Modifier.height(4.dp))
                                    Text(
                                        text = "Optimal chemical spray window: 7 AM – 10 AM before wind picks up. Soil moisture is optimal for transplanting paddy seedlings.",
                                        fontSize = 12.sp,
                                        color = Color(0xFF15803D),
                                        lineHeight = 17.sp
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

/**
 * Segmented pill selector containing 5 interactive weather states (☀️, ⛅, 💨, 🌧️, 🌈).
 */
@Composable
private fun WeatherModeSegmentedPill(
    selectedMode: WeatherVisualMode,
    onModeSelected: (WeatherVisualMode) -> Unit
) {
    val modes = listOf(
        WeatherVisualMode.SUNNY to "☀️",
        WeatherVisualMode.PARTLY_CLOUDY to "⛅",
        WeatherVisualMode.WINDY to "💨",
        WeatherVisualMode.RAINY to "🌧️",
        WeatherVisualMode.RAINBOW to "🌈"
    )

    Surface(
        color = Color.White,
        shape = RoundedCornerShape(26.dp),
        shadowElevation = 2.dp,
        border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFE2E8F0)),
        modifier = Modifier.padding(horizontal = 8.dp)
    ) {
        Row(
            modifier = Modifier.padding(4.dp),
            horizontalArrangement = Arrangement.spacedBy(4.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            modes.forEach { (mode, emoji) ->
                val isSelected = mode == selectedMode
                val bgAnim by animateColorAsState(
                    targetValue = if (isSelected) Color(0xFF1E293B) else Color.Transparent,
                    animationSpec = spring(dampingRatio = Spring.DampingRatioMediumBouncy, stiffness = Spring.StiffnessMediumLow),
                    label = "pill_bg"
                )

                Box(
                    modifier = Modifier
                        .size(44.dp)
                        .clip(RoundedCornerShape(22.dp))
                        .background(bgAnim)
                        .tactilePress(scaleDown = 0.90f) { onModeSelected(mode) },
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = emoji,
                        fontSize = 18.sp
                    )
                }
            }
        }
    }
}

/**
 * Environmental Card 1: Temperature Trend with golden Bezier arc.
 */
@Composable
private fun TemperatureTrendCard(
    currentTemp: Int,
    feelsLike: Int,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .clip(RoundedCornerShape(20.dp))
            .border(1.dp, Color(0xFFF1F5F9), RoundedCornerShape(20.dp)),
        colors = CardDefaults.cardColors(containerColor = Color(0xFFFFFBEB)),
        elevation = CardDefaults.cardElevation(0.dp)
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Temperature", fontSize = 11.sp, color = Color(0xFF92400E), fontWeight = FontWeight.SemiBold)
                Text("🌡️", fontSize = 14.sp)
            }
            Spacer(Modifier.height(8.dp))
            Text(
                text = "$currentTemp°",
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF78350F)
            )
            Text(
                text = "Feels like $feelsLike°",
                fontSize = 11.sp,
                color = Color(0xFFB45309)
            )
            Spacer(Modifier.height(10.dp))
            // Golden Bezier trend arc
            Canvas(modifier = Modifier.fillMaxWidth().height(26.dp)) {
                val path = Path().apply {
                    moveTo(0f, size.height * 0.8f)
                    cubicTo(
                        size.width * 0.35f, size.height * 0.2f,
                        size.width * 0.65f, size.height * 0.9f,
                        size.width, size.height * 0.1f
                    )
                }
                drawPath(path, color = Color(0xFFF59E0B), style = Stroke(2.5.dp.toPx(), cap = StrokeCap.Round))
                // Sun marker node at peak
                drawCircle(Color(0xFFF59E0B), radius = 4.dp.toPx(), center = Offset(size.width, size.height * 0.1f))
            }
        }
    }
}

/**
 * Environmental Card 2: Humidity Liquid Capsule Meter.
 */
@Composable
private fun HumidityMeterCard(
    humidityPercent: Int,
    dewPoint: Int,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .clip(RoundedCornerShape(20.dp))
            .border(1.dp, Color(0xFFF1F5F9), RoundedCornerShape(20.dp)),
        colors = CardDefaults.cardColors(containerColor = Color(0xFFF0F9FF)),
        elevation = CardDefaults.cardElevation(0.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(14.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text("Humidity", fontSize = 11.sp, color = Color(0xFF0369A1), fontWeight = FontWeight.SemiBold)
                Spacer(Modifier.height(8.dp))
                Text(
                    text = "$humidityPercent%",
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF0C4A6E)
                )
                Text(
                    text = "Dew pt $dewPoint°",
                    fontSize = 11.sp,
                    color = Color(0xFF0284C7)
                )
            }

            // Vertical Liquid Level Capsule
            Box(
                modifier = Modifier
                    .width(16.dp)
                    .height(54.dp)
                    .clip(RoundedCornerShape(8.dp))
                    .background(Color(0xFFBAE6FD)),
                contentAlignment = Alignment.BottomCenter
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .fillMaxHeight(humidityPercent / 100f)
                        .clip(RoundedCornerShape(8.dp))
                        .background(
                            Brush.verticalGradient(
                                listOf(Color(0xFF38BDF8), Color(0xFF0284C7))
                            )
                        )
                )
            }
        }
    }
}

/**
 * Environmental Card 3: Wind Speed Card with live spinning mini turbine graphic.
 */
@Composable
private fun WindSpeedCard(
    windSpeedKmh: Int,
    direction: String,
    modifier: Modifier = Modifier
) {
    val transition = rememberInfiniteTransition(label = "wind_mini_spin")
    val bladeAngle by transition.animateFloat(
        initialValue = 0f,
        targetValue = 360f,
        animationSpec = infiniteRepeatable(
            animation = tween(2800, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "turbine"
    )

    Card(
        modifier = modifier
            .clip(RoundedCornerShape(20.dp))
            .border(1.dp, Color(0xFFF1F5F9), RoundedCornerShape(20.dp)),
        colors = CardDefaults.cardColors(containerColor = Color(0xFFF8FAFC)),
        elevation = CardDefaults.cardElevation(0.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(14.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text("Wind", fontSize = 11.sp, color = Color(0xFF475569), fontWeight = FontWeight.SemiBold)
                Spacer(Modifier.height(8.dp))
                Text(
                    text = "$windSpeedKmh km/h",
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF0F172A)
                )
                Text(
                    text = direction,
                    fontSize = 10.sp,
                    color = Color(0xFF64748B)
                )
            }

            // Animated Mini Turbine Canvas
            Canvas(modifier = Modifier.size(36.dp)) {
                val cx = size.width / 2f
                val cy = size.height * 0.45f
                val poleH = size.height * 0.5f

                // Mast
                drawLine(Color(0xFF94A3B8), Offset(cx, cy), Offset(cx, cy + poleH), strokeWidth = 2.dp.toPx())
                // Rotor center
                drawCircle(Color(0xFF64748B), 2.5.dp.toPx(), Offset(cx, cy))

                // Blades
                val bladeLen = size.width * 0.38f
                for (b in 0..2) {
                    val rad = Math.toRadians((bladeAngle + (b * 120)).toDouble())
                    val tx = cx + (bladeLen * cos(rad)).toFloat()
                    val ty = cy + (bladeLen * sin(rad)).toFloat()
                    drawLine(Color(0xFF475569), Offset(cx, cy), Offset(tx, ty), strokeWidth = 1.6.dp.toPx())
                }
            }
        }
    }
}

/**
 * Environmental Card 4: Rain Probability Progress.
 */
@Composable
private fun RainProbabilityCard(
    chancePercent: Int,
    timing: String,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .clip(RoundedCornerShape(20.dp))
            .border(1.dp, Color(0xFFF1F5F9), RoundedCornerShape(20.dp)),
        colors = CardDefaults.cardColors(containerColor = Color(0xFFFAF5FF)),
        elevation = CardDefaults.cardElevation(0.dp)
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Precipitation", fontSize = 11.sp, color = Color(0xFF7E22CE), fontWeight = FontWeight.SemiBold)
                Text("🌧️", fontSize = 14.sp)
            }
            Spacer(Modifier.height(8.dp))
            Text(
                text = "$chancePercent%",
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF581C87)
            )
            Text(
                text = timing,
                fontSize = 11.sp,
                color = Color(0xFF9333EA)
            )
            Spacer(Modifier.height(10.dp))
            // Probability meter bar
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(6.dp)
                    .clip(RoundedCornerShape(3.dp))
                    .background(Color(0xFFE9D5FF))
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(chancePercent / 100f)
                        .fillMaxHeight()
                        .clip(RoundedCornerShape(3.dp))
                        .background(Color(0xFF9333EA))
                )
            }
        }
    }
}

/**
 * Horizontal 7-Day Forecast Card
 */
@Composable
private fun ForecastDayCard(day: DayForecast) {
    Surface(
        shape = RoundedCornerShape(16.dp),
        color = if (day.isToday) Color(0xFF1E293B) else Color.White,
        border = if (day.isToday) null else androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFE2E8F0)),
        shadowElevation = if (day.isToday) 3.dp else 1.dp,
        modifier = Modifier.width(72.dp)
    ) {
        Column(
            modifier = Modifier.padding(vertical = 14.dp, horizontal = 10.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = day.dayName,
                fontSize = 12.sp,
                fontWeight = FontWeight.SemiBold,
                color = if (day.isToday) Color.White else Color(0xFF64748B)
            )
            Spacer(Modifier.height(8.dp))
            Text(day.condition, fontSize = 22.sp)
            Spacer(Modifier.height(8.dp))
            Text(
                text = "${day.highC.toInt()}°",
                fontSize = 14.sp,
                fontWeight = FontWeight.Bold,
                color = if (day.isToday) Color.White else Color(0xFF0F172A)
            )
            Text(
                text = "${day.lowC.toInt()}°",
                fontSize = 11.sp,
                color = if (day.isToday) Color(0xFF94A3B8) else Color(0xFF94A3B8)
            )
        }
    }
}
