package com.agrisage.app.ui.screens

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Agriculture
import androidx.compose.material.icons.filled.Air
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.Cloud
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.LocationOn
import androidx.compose.material.icons.filled.WaterDrop
import androidx.compose.material.icons.filled.WbSunny
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
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.stateDescription
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
 * - Top Bar: Circular white back button, Green Valley Farm selector pill, circular refresh button
 * - Hero Weather Header: Huge 26°C with dynamic condition text
 * - Segmented Weather Mode Selector: 5 interactive states with a sliding indicator
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

private val WeatherBackground = Color(0xFFF8F2E8)
private val WeatherSurface = WireWhite
private val WeatherInk = WireTextPrimary
private val WeatherMuted = WireTextMuted
private val WeatherSage = WireSage
private val WeatherSageDark = WireSageDeep
private val WeatherBorder = WireBorder
private val WeatherGold = WireGold

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WeatherScreen(navController: NavController) {
    var selectedWeatherMode by remember { mutableStateOf(WeatherVisualMode.RAINBOW) }

    val forecast = listOf(
        DayForecast("Today", "sunny", 33f, 24f, isToday = true),
        DayForecast("Tue", "partly_cloudy", 31f, 23f),
        DayForecast("Wed", "rainy", 27f, 21f),
        DayForecast("Thu", "rainy", 26f, 20f),
        DayForecast("Fri", "partly_cloudy", 29f, 22f),
        DayForecast("Sat", "sunny", 32f, 23f),
        DayForecast("Sun", "sunny", 34f, 25f),
    )

    // Dynamic temperature and description based on selected weather mode
    val (tempDisplay, conditionText) = when (selectedWeatherMode) {
        WeatherVisualMode.SUNNY -> "28°C" to "Bright & Sunny · Clear skies"
        WeatherVisualMode.PARTLY_CLOUDY -> "27°C" to "Partly Cloudy · Mild breeze"
        WeatherVisualMode.WINDY -> "24°C" to "Windy · 28 km/h gusts"
        WeatherVisualMode.RAINY -> "22°C" to "Rain Shower · 12mm precipitation"
        WeatherVisualMode.RAINBOW -> "26°C" to "Clearing up · Rainbow out"
    }

    val conditionIcon = when (selectedWeatherMode) {
        WeatherVisualMode.SUNNY -> Icons.Default.WbSunny
        WeatherVisualMode.PARTLY_CLOUDY -> Icons.Default.Cloud
        WeatherVisualMode.WINDY -> Icons.Default.Air
        WeatherVisualMode.RAINY -> Icons.Default.WaterDrop
        WeatherVisualMode.RAINBOW -> Icons.Default.AutoAwesome
    }

    Scaffold(
        containerColor = WeatherBackground,
        topBar = {
            Surface(
                color = WeatherBackground,
                tonalElevation = 0.dp
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .statusBarsPadding()
                        .padding(horizontal = 20.dp, vertical = 10.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .size(48.dp)
                            .clip(CircleShape)
                            .background(WeatherSurface)
                            .border(1.dp, WeatherBorder, CircleShape)
                            .tactilePress(
                                scaleDown = 0.95f,
                                onClickLabel = "Go back",
                                onClick = { navController.popBackStack() }
                            ),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Back",
                            tint = WeatherInk,
                            modifier = Modifier.size(20.dp)
                        )
                    }

                    Surface(
                        color = WeatherSurface,
                        shape = RoundedCornerShape(18.dp),
                        border = androidx.compose.foundation.BorderStroke(1.dp, WeatherBorder),
                        modifier = Modifier.height(40.dp)
                    ) {
                        Row(
                            modifier = Modifier.padding(horizontal = 13.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(
                                imageVector = Icons.Default.LocationOn,
                                contentDescription = "Farm location",
                                tint = WeatherSage,
                                modifier = Modifier.size(18.dp)
                            )
                            Spacer(Modifier.width(6.dp))
                            Text(
                                text = "Green Valley Farm",
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold,
                                color = WeatherInk
                            )
                            Spacer(Modifier.width(4.dp))
                            Icon(
                                imageVector = Icons.Default.KeyboardArrowDown,
                                contentDescription = null,
                                tint = WeatherMuted,
                                modifier = Modifier.size(18.dp)
                            )
                        }
                    }

                    Box(
                        modifier = Modifier
                            .size(48.dp)
                            .clip(CircleShape)
                            .background(WeatherSurface)
                            .border(1.dp, WeatherBorder, CircleShape)
                            .tactilePress(
                                scaleDown = 0.95f,
                                onClickLabel = "Refresh weather",
                                onClick = { /* Refresh weather */ }
                            ),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = Icons.Default.Refresh,
                            contentDescription = "Refresh",
                            tint = WeatherInk,
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
                .background(WeatherBackground),
            contentPadding = PaddingValues(bottom = 36.dp)
        ) {
            item {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 22.dp, vertical = 14.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(
                        text = "Monday, 5 October",
                        fontSize = 13.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = WeatherMuted
                    )
                    Spacer(Modifier.height(4.dp))
                    Text(
                        text = tempDisplay,
                        fontSize = 58.sp,
                        fontWeight = FontWeight.Bold,
                        color = WeatherInk,
                        letterSpacing = (-2).sp
                    )

                    Surface(
                        color = Color(0xFFFFF3D6),
                        shape = RoundedCornerShape(14.dp),
                        border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFF1D9A7))
                    ) {
                        Row(
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 7.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(
                                imageVector = conditionIcon,
                                contentDescription = null,
                                tint = WeatherGold,
                                modifier = Modifier.size(18.dp)
                            )
                            Spacer(Modifier.width(7.dp))
                            Text(
                                text = conditionText,
                                fontSize = 13.sp,
                                fontWeight = FontWeight.SemiBold,
                                color = WeatherSageDark
                            )
                        }
                    }

                    Spacer(Modifier.height(18.dp))

                    WeatherModeSegmentedPill(
                        selectedMode = selectedWeatherMode,
                        onModeSelected = { selectedWeatherMode = it }
                    )
                }
            }

            item {
                val illustrationShape = RoundedCornerShape(26.dp)
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 18.dp, vertical = 4.dp)
                        .height(232.dp)
                        .shadow(
                            elevation = 8.dp,
                            shape = illustrationShape,
                            ambientColor = Color(0x1A6B5235),
                            spotColor = Color(0x1A6B5235)
                        )
                        .clip(illustrationShape)
                        .border(1.dp, Color.White.copy(alpha = 0.7f), illustrationShape)
                ) {
                    FarmIllustration(
                        modifier = Modifier.fillMaxSize(),
                        weatherMode = selectedWeatherMode,
                        isAnimated = true
                    )
                }
            }

            item {
                Surface(
                    color = WeatherSurface,
                    shape = RoundedCornerShape(topStart = 32.dp, topEnd = 32.dp),
                    border = androidx.compose.foundation.BorderStroke(1.dp, WeatherBorder.copy(alpha = 0.72f)),
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 16.dp)
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 22.dp, vertical = 22.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text(
                                    text = "Today's conditions",
                                    fontSize = 20.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = WeatherInk
                                )
                                Spacer(Modifier.height(4.dp))
                                Text(
                                    text = "Mon, 5 Oct · The rain has passed. Soil is moist and a rainbow is out.",
                                    fontSize = 12.sp,
                                    color = WeatherMuted,
                                    lineHeight = 16.sp
                                )
                            }
                            Surface(
                                color = Color(0xFFE7F0E6),
                                shape = CircleShape,
                                modifier = Modifier.size(38.dp)
                            ) {
                                Box(contentAlignment = Alignment.Center) {
                                    Icon(
                                        imageVector = Icons.Default.Agriculture,
                                        contentDescription = "Farm conditions",
                                        tint = WeatherSage,
                                        modifier = Modifier.size(20.dp)
                                    )
                                }
                            }
                        }

                        Spacer(Modifier.height(18.dp))

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            TemperatureTrendCard(
                                currentTemp = 26,
                                feelsLike = 28,
                                modifier = Modifier.weight(1f)
                            )

                            HumidityMeterCard(
                                humidityPercent = 77,
                                dewPoint = 21,
                                modifier = Modifier.weight(1f)
                            )
                        }

                        Spacer(Modifier.height(12.dp))

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            WindSpeedCard(
                                windSpeedKmh = 12,
                                direction = "NW · Gentle breeze",
                                modifier = Modifier.weight(1f)
                            )

                            RainProbabilityCard(
                                chancePercent = 10,
                                timing = "Expected at 6 PM",
                                modifier = Modifier.weight(1f)
                            )
                        }

                        Spacer(Modifier.height(24.dp))

                        Text(
                            text = "7-day forecast",
                            fontSize = 18.sp,
                            fontWeight = FontWeight.Bold,
                            color = WeatherInk
                        )
                        Spacer(Modifier.height(12.dp))
                        LazyRow(
                            horizontalArrangement = Arrangement.spacedBy(10.dp),
                            contentPadding = PaddingValues(end = 4.dp)
                        ) {
                            items(forecast) { day ->
                                ForecastDayCard(day)
                            }
                        }

                        Spacer(Modifier.height(22.dp))

                        Surface(
                            modifier = Modifier.fillMaxWidth(),
                            color = Color(0xFFEAF2E6),
                            shape = RoundedCornerShape(22.dp),
                            border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFC9DEC3))
                        ) {
                            Row(
                                modifier = Modifier.padding(18.dp),
                                verticalAlignment = Alignment.Top
                            ) {
                                Surface(
                                    color = WeatherSage,
                                    shape = CircleShape,
                                    modifier = Modifier.size(40.dp)
                                ) {
                                    Box(contentAlignment = Alignment.Center) {
                                        Icon(
                                            imageVector = Icons.Default.Agriculture,
                                            contentDescription = "Weather advisory",
                                            tint = Color.White,
                                            modifier = Modifier.size(22.dp)
                                        )
                                    }
                                }
                                Spacer(Modifier.width(12.dp))
                                Column(modifier = Modifier.weight(1f)) {
                                    Text(
                                        text = "Agri-SAGE recommendation",
                                        fontWeight = FontWeight.Bold,
                                        color = WeatherSageDark,
                                        fontSize = 14.sp
                                    )
                                    Spacer(Modifier.height(4.dp))
                                    Text(
                                        text = "Optimal chemical spray window: 7 AM – 10 AM before wind picks up. Soil moisture is optimal for transplanting paddy seedlings.",
                                        fontSize = 12.sp,
                                        color = WeatherSage,
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
 * Segmented pill selector containing 5 interactive weather states.
 */
@Composable
private fun WeatherModeSegmentedPill(
    selectedMode: WeatherVisualMode,
    onModeSelected: (WeatherVisualMode) -> Unit
) {
    val modes = listOf(
        WeatherVisualMode.SUNNY to (Icons.Default.WbSunny to "Sunny"),
        WeatherVisualMode.PARTLY_CLOUDY to (Icons.Default.Cloud to "Partly cloudy"),
        WeatherVisualMode.WINDY to (Icons.Default.Air to "Windy"),
        WeatherVisualMode.RAINY to (Icons.Default.WaterDrop to "Rainy"),
        WeatherVisualMode.RAINBOW to (Icons.Default.AutoAwesome to "Rainbow")
    )

    Surface(
        color = WeatherSurface,
        shape = RoundedCornerShape(26.dp),
        shadowElevation = 2.dp,
        border = androidx.compose.foundation.BorderStroke(1.dp, WeatherBorder),
        modifier = Modifier.padding(horizontal = 8.dp)
    ) {
        Row(
            modifier = Modifier.padding(4.dp),
            horizontalArrangement = Arrangement.spacedBy(4.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            modes.forEach { (mode, iconAndLabel) ->
                val (icon, label) = iconAndLabel
                val isSelected = mode == selectedMode
                val bgAnim by animateColorAsState(
                    targetValue = if (isSelected) WeatherSageDark else Color.Transparent,
                    animationSpec = spring(dampingRatio = Spring.DampingRatioMediumBouncy, stiffness = Spring.StiffnessMediumLow),
                    label = "pill_bg"
                )

                Box(
                    modifier = Modifier
                        .size(48.dp)
                        .clip(RoundedCornerShape(22.dp))
                        .background(bgAnim)
                        .semantics {
                            contentDescription = label
                            role = androidx.compose.ui.semantics.Role.Button
                            if (isSelected) stateDescription = "Selected"
                        }
                        .tactilePress(scaleDown = 0.90f) { onModeSelected(mode) },
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = icon,
                        contentDescription = null,
                        tint = if (isSelected) Color.White else WeatherMuted,
                        modifier = Modifier.size(20.dp)
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
            .border(1.dp, Color(0xFFF1DDBB), RoundedCornerShape(20.dp)),
        colors = CardDefaults.cardColors(containerColor = Color(0xFFFFF5E3)),
        elevation = CardDefaults.cardElevation(0.dp)
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Temperature", fontSize = 11.sp, color = Color(0xFF92400E), fontWeight = FontWeight.SemiBold)
                Icon(
                    imageVector = Icons.Default.WbSunny,
                    contentDescription = "Temperature",
                    tint = WeatherGold,
                    modifier = Modifier.size(18.dp)
                )
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
            .border(1.dp, Color(0xFFCFE4E3), RoundedCornerShape(20.dp)),
        colors = CardDefaults.cardColors(containerColor = Color(0xFFEAF5F4)),
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
            .border(1.dp, Color(0xFFD8E2D6), RoundedCornerShape(20.dp)),
        colors = CardDefaults.cardColors(containerColor = Color(0xFFF1F5EF)),
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
            .border(1.dp, Color(0xFFD8E2D6), RoundedCornerShape(20.dp)),
        colors = CardDefaults.cardColors(containerColor = Color(0xFFF1F5EF)),
        elevation = CardDefaults.cardElevation(0.dp)
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Precipitation", fontSize = 11.sp, color = WeatherSage, fontWeight = FontWeight.SemiBold)
                Icon(
                    imageVector = Icons.Default.WaterDrop,
                    contentDescription = "Precipitation",
                    tint = Color(0xFF3D8F99),
                    modifier = Modifier.size(18.dp)
                )
            }
            Spacer(Modifier.height(8.dp))
            Text(
                text = "$chancePercent%",
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                color = WeatherInk
            )
            Text(
                text = timing,
                fontSize = 11.sp,
                color = WeatherMuted
            )
            Spacer(Modifier.height(10.dp))
            // Probability meter bar
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(6.dp)
                    .clip(RoundedCornerShape(3.dp))
                    .background(Color(0xFFDDEADB))
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(chancePercent / 100f)
                        .fillMaxHeight()
                        .clip(RoundedCornerShape(3.dp))
                        .background(WeatherSage)
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
    val (conditionIcon, conditionLabel) = when (day.condition) {
        "rainy" -> Icons.Default.WaterDrop to "Rain"
        "partly_cloudy" -> Icons.Default.Cloud to "Partly cloudy"
        else -> Icons.Default.WbSunny to "Sunny"
    }
    val conditionTint = when (day.condition) {
        "rainy" -> Color(0xFF3D8F99)
        "partly_cloudy" -> Color(0xFF738B7A)
        else -> WeatherGold
    }

    Surface(
        shape = RoundedCornerShape(16.dp),
        color = if (day.isToday) WeatherSageDark else WeatherSurface,
        border = if (day.isToday) null else androidx.compose.foundation.BorderStroke(1.dp, WeatherBorder),
        shadowElevation = if (day.isToday) 3.dp else 1.dp,
        modifier = Modifier.width(76.dp)
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
            Icon(
                imageVector = conditionIcon,
                contentDescription = conditionLabel,
                tint = if (day.isToday) Color.White else conditionTint,
                modifier = Modifier.size(23.dp)
            )
            Spacer(Modifier.height(8.dp))
            Text(
                text = "${day.highC.toInt()}°",
                fontSize = 14.sp,
                fontWeight = FontWeight.Bold,
                color = if (day.isToday) Color.White else WeatherInk
            )
            Text(
                text = "${day.lowC.toInt()}°",
                fontSize = 11.sp,
                color = if (day.isToday) Color(0xFF94A3B8) else Color(0xFF94A3B8)
            )
        }
    }
}
