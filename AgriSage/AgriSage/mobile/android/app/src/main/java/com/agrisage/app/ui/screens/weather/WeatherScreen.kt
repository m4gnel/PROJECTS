package com.agrisage.app.ui.screens.weather

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.foundation.BorderStroke
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
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
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
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavHostController
import com.agrisage.app.navigation.Screen
import com.agrisage.app.ui.components.FarmIllustration
import com.agrisage.app.ui.components.WeatherVisualMode
import com.agrisage.app.ui.components.tactilePress
import kotlin.math.cos
import kotlin.math.sin

private val WeatherCanvasBg = Color(0xFFF9FBF9)
private val TextDark = Color(0xFF18181B)
private val TextMuted = Color(0xFF64748B)
private val BrandGreen = Color(0xFF16A34A)
private val CardBorder = Color(0xFFE2E8F0)

data class ForecastRowData(
    val dayName: String,
    val rainPercent: Int,
    val iconEmoji: String,
    val lowTemp: Int,
    val highTemp: Int,
    val currentTempRatio: Float
)

/**
 * Screen: "Weather & Forecast" (Deterministic 1:1 replication from Reference Video 1).
 * Features:
 * - Top Navigation: Circular Back Button, "📍 Green Valley Farm" Pill, Circular Refresh Button
 * - Dynamic Hero Temp (28°C / 24°C / 21°C) & Condition ("Sunny", "Wind picking up", "Rain shower")
 * - 5-Mode Segmented Selector (☀️, ⛅, 💨, 🌧️, 🌈) with spring animation
 * - Dynamic Farm Landscape reacting with moving turbines, rain drops, and crop sprinklers
 * - "Today's conditions" Bottom Sheet (32dp curvature) with ((•)) Live badge:
 *   - Temperature Card with Golden Arched Bezier trend curve
 *   - Humidity Card with Vertical Liquid Capsule gauge
 *   - Wind Speed Card with Rotating 3-Blade Mini Turbine
 *   - Rain Chance Card with Percentage Progress Bar
 * - Hourly Temperature Pills (28°, 29°, 30°, 31°, 31°, 30°)
 * - 7-Day Forecast Card with Low/High Gradient Range Bars
 * - Farm Recommendations Card ("Watering recommended tomorrow morning")
 */
@Composable
fun WeatherScreen(
    navController: NavHostController,
    viewModel: WeatherViewModel = hiltViewModel()
) {
    var selectedWeatherMode by rememberSaveable { mutableStateOf(WeatherVisualMode.SUNNY) }

    // Dynamic telemetry values based on the interactive mode in Video 1
    val currentTemp = when (selectedWeatherMode) {
        WeatherVisualMode.SUNNY -> 28
        WeatherVisualMode.WINDY -> 24
        WeatherVisualMode.RAINY -> 21
        WeatherVisualMode.PARTLY_CLOUDY -> 26
        WeatherVisualMode.RAINBOW -> 26
    }

    val currentCondition = when (selectedWeatherMode) {
        WeatherVisualMode.SUNNY -> "Sunny"
        WeatherVisualMode.WINDY -> "Wind picking up"
        WeatherVisualMode.RAINY -> "Rain shower"
        WeatherVisualMode.PARTLY_CLOUDY -> "Partly cloudy"
        WeatherVisualMode.RAINBOW -> "Clearing up · Rainbow out"
    }

    val conditionSubtitle = when (selectedWeatherMode) {
        WeatherVisualMode.SUNNY -> "Mon, 5 Oct · Clear skies and a light breeze over the fields."
        WeatherVisualMode.WINDY -> "Mon, 5 Oct · Gusts are rising. Irrigation paused. Rain is on the way."
        WeatherVisualMode.RAINY -> "Mon, 5 Oct · Rain over the farm. The tank and the soil are filling up."
        WeatherVisualMode.RAINBOW -> "Mon, 5 Oct · The rain has passed. Soil is moist and a rainbow is out."
        WeatherVisualMode.PARTLY_CLOUDY -> "Mon, 5 Oct · Mild overcast conditions across Green Valley Farm."
    }

    val humidityVal = when (selectedWeatherMode) {
        WeatherVisualMode.SUNNY -> 72
        WeatherVisualMode.WINDY -> 80
        WeatherVisualMode.RAINY -> 94
        else -> 77
    }

    val feelsLikeTemp = when (selectedWeatherMode) {
        WeatherVisualMode.SUNNY -> 30
        WeatherVisualMode.WINDY -> 26
        WeatherVisualMode.RAINY -> 23
        else -> 28
    }

    val windSpeed = when (selectedWeatherMode) {
        WeatherVisualMode.WINDY -> 28
        WeatherVisualMode.RAINY -> 18
        else -> 12
    }

    val rainChance = when (selectedWeatherMode) {
        WeatherVisualMode.RAINY -> 90
        WeatherVisualMode.WINDY -> 45
        else -> 10
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(WeatherCanvasBg)
    ) {
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(bottom = 28.dp)
        ) {
            // 1. Top Bar: Back, Location Pill, Refresh Button
            item {
                WeatherTopBar(
                    onBack = { navController.popBackStack() },
                    onRefresh = { viewModel.refresh() },
                    locationLabel = "Green Valley Farm",
                    onFarmClick = { navController.navigate(Screen.Fields) }
                )
            }

            // 2. Large Temperature Hero Typography
            item {
                WeatherHeroHeader(
                    temperatureC = currentTemp,
                    condition = currentCondition
                )
            }

            // 3. Segmented 5-Mode Selector Pill (☀️, ⛅, 💨, 🌧️, 🌈)
            item {
                WeatherModeSegmentedPill(
                    selectedMode = selectedWeatherMode,
                    onModeSelected = { selectedWeatherMode = it }
                )
            }

            // 4. Dynamic Vector Farm Canvas
            item {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 10.dp)
                        .clip(RoundedCornerShape(24.dp))
                ) {
                    FarmIllustration(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(210.dp),
                        weatherMode = selectedWeatherMode,
                        isAnimated = true
                    )
                }
            }

            // 5. "Today's conditions" Rounded Sheet
            item {
                TodaysConditionsSheet(
                    subtitle = conditionSubtitle,
                    temperature = currentTemp,
                    feelsLike = feelsLikeTemp,
                    humidity = humidityVal,
                    windSpeed = windSpeed,
                    rainChance = rainChance
                )
            }

            // 6. Hourly Temperature Chips
            item {
                HourlyTemperatureChipsRow()
            }

            // 7. 7-Day Forecast Card
            item {
                Forecast7DaySection()
            }

            // 8. Farm Recommendations Card
            item {
                FarmRecommendationsCard()
            }
        }
    }
}

@Composable
private fun WeatherTopBar(
    onBack: () -> Unit,
    onRefresh: () -> Unit,
    locationLabel: String,
    onFarmClick: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .statusBarsPadding()
            .padding(horizontal = 20.dp, vertical = 10.dp),
        horizontalArrangement = Arrangement.spacedBy(10.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Circular Back Button (44dp)
        Surface(
            modifier = Modifier
                .size(44.dp)
                .tactilePress(scaleDown = 0.92f, onClick = onBack),
            shape = CircleShape,
            color = Color.White,
            shadowElevation = 2.dp,
            border = BorderStroke(1.dp, CardBorder)
        ) {
            Box(contentAlignment = Alignment.Center) {
                Icon(
                    imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                    contentDescription = "Back",
                    tint = TextDark,
                    modifier = Modifier.size(20.dp)
                )
            }
        }

        // Center Location Pill
        Surface(
            modifier = Modifier
                .weight(1f)
                .height(44.dp)
                .tactilePress(scaleDown = 0.97f, onClick = onFarmClick),
            color = Color.White,
            shape = RoundedCornerShape(22.dp),
            shadowElevation = 2.dp,
            border = BorderStroke(1.dp, CardBorder)
        ) {
            Row(
                modifier = Modifier.padding(horizontal = 14.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.Center
            ) {
                Icon(
                    imageVector = Icons.Default.Place,
                    contentDescription = null,
                    tint = BrandGreen,
                    modifier = Modifier.size(16.dp)
                )
                Spacer(Modifier.width(6.dp))
                Text(
                    text = locationLabel,
                    fontSize = 13.sp,
                    fontWeight = FontWeight.Bold,
                    color = TextDark,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }

        // Circular Refresh Button (44dp)
        Surface(
            modifier = Modifier
                .size(44.dp)
                .tactilePress(scaleDown = 0.92f, onClick = onRefresh),
            shape = CircleShape,
            color = Color.White,
            shadowElevation = 2.dp,
            border = BorderStroke(1.dp, CardBorder)
        ) {
            Box(contentAlignment = Alignment.Center) {
                Icon(
                    imageVector = Icons.Default.Refresh,
                    contentDescription = "Refresh",
                    tint = TextDark,
                    modifier = Modifier.size(20.dp)
                )
            }
        }
    }
}

@Composable
private fun WeatherHeroHeader(
    temperatureC: Int,
    condition: String
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 20.dp, vertical = 6.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "$temperatureC°C",
            fontSize = 56.sp,
            fontWeight = FontWeight.Bold,
            color = TextDark,
            letterSpacing = (-2).sp
        )
        Spacer(Modifier.height(2.dp))
        Text(
            text = condition,
            fontSize = 16.sp,
            fontWeight = FontWeight.SemiBold,
            color = TextMuted
        )
    }
}

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
        color = Color.White.copy(alpha = 0.92f),
        shape = RoundedCornerShape(26.dp),
        shadowElevation = 2.dp,
        border = BorderStroke(1.dp, CardBorder),
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 20.dp, vertical = 6.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(4.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            modes.forEach { (mode, emoji) ->
                val isSelected = selectedMode == mode
                val bg by animateColorAsState(
                    targetValue = if (isSelected) Color(0xFF15803D) else Color.Transparent,
                    animationSpec = spring(
                        dampingRatio = Spring.DampingRatioMediumBouncy,
                        stiffness = Spring.StiffnessMediumLow
                    ),
                    label = "mode_bg"
                )

                Box(
                    modifier = Modifier
                        .weight(1f)
                        .height(44.dp)
                        .clip(CircleShape)
                        .background(bg)
                        .clickable { onModeSelected(mode) },
                    contentAlignment = Alignment.Center
                ) {
                    Text(text = emoji, fontSize = 18.sp)
                }
            }
        }
    }
}

@Composable
private fun TodaysConditionsSheet(
    subtitle: String,
    temperature: Int,
    feelsLike: Int,
    humidity: Int,
    windSpeed: Int,
    rainChance: Int
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        color = Color.White,
        shape = RoundedCornerShape(topStart = 32.dp, topEnd = 32.dp),
        border = BorderStroke(1.dp, CardBorder)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 20.dp, vertical = 20.dp)
        ) {
            // Header Row: "Today's conditions" and ((•)) Live Badge
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "Today's conditions",
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold,
                    color = TextDark
                )

                // ((•)) Live Pill Badge from Reel 1
                Surface(
                    color = Color(0xFFDCFCE7),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier
                                .size(6.dp)
                                .clip(CircleShape)
                                .background(Color(0xFF16A34A))
                        )
                        Spacer(Modifier.width(4.dp))
                        Text(
                            text = "Live",
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFF166534)
                        )
                    }
                }
            }

            Spacer(Modifier.height(4.dp))

            Text(
                text = subtitle,
                fontSize = 12.sp,
                color = TextMuted,
                lineHeight = 16.sp
            )

            Spacer(Modifier.height(18.dp))

            // 4 Grid Tiles: Temperature, Humidity, Wind, Rain Chance
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                // Card 1: Temperature with Golden Arched Bezier Curve
                TemperatureTile(
                    temperature = temperature,
                    feelsLike = feelsLike,
                    modifier = Modifier.weight(1f)
                )
                // Card 2: Humidity with Liquid Capsule Meter
                HumidityTile(
                    humidity = humidity,
                    modifier = Modifier.weight(1f)
                )
            }

            Spacer(Modifier.height(12.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                // Card 3: Wind with Rotating Wind Turbine
                WindTile(
                    windSpeed = windSpeed,
                    modifier = Modifier.weight(1f)
                )
                // Card 4: Rain Chance with Progress Bar
                RainChanceTile(
                    rainChance = rainChance,
                    modifier = Modifier.weight(1f)
                )
            }
        }
    }
}

@Composable
private fun TemperatureTile(temperature: Int, feelsLike: Int, modifier: Modifier = Modifier) {
    Surface(
        color = Color.White,
        shape = RoundedCornerShape(20.dp),
        shadowElevation = 2.dp,
        border = BorderStroke(1.dp, CardBorder),
        modifier = modifier
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    modifier = Modifier
                        .size(36.dp)
                        .clip(CircleShape)
                        .background(Color(0xFFFFEDD5)),
                    contentAlignment = Alignment.Center
                ) {
                    Text("☀️", fontSize = 16.sp)
                }

                // Smooth upward arched golden Bezier curve (Reel 1 signature)
                Canvas(modifier = Modifier.size(width = 64.dp, height = 26.dp)) {
                    val path = Path().apply {
                        moveTo(4f, size.height * 0.85f)
                        cubicTo(
                            size.width * 0.35f, 2f,
                            size.width * 0.65f, 2f,
                            size.width - 6f, size.height * 0.70f
                        )
                    }
                    drawPath(path, color = Color(0xFFF59E0B), style = Stroke(width = 2.5.dp.toPx(), cap = StrokeCap.Round))
                    drawCircle(Color(0xFFF59E0B), radius = 3.5.dp.toPx(), center = Offset(size.width - 6f, size.height * 0.70f))
                }
            }

            Spacer(Modifier.height(12.dp))
            Text("Temperature", fontSize = 11.sp, color = TextMuted)
            Text("$temperature°", fontSize = 26.sp, fontWeight = FontWeight.Bold, color = TextDark)
            Text("Feels like $feelsLike°", fontSize = 11.sp, color = TextMuted)
        }
    }
}

@Composable
private fun HumidityTile(humidity: Int, modifier: Modifier = Modifier) {
    Surface(
        color = Color.White,
        shape = RoundedCornerShape(20.dp),
        shadowElevation = 2.dp,
        border = BorderStroke(1.dp, CardBorder),
        modifier = modifier
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(14.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Box(
                    modifier = Modifier
                        .size(36.dp)
                        .clip(CircleShape)
                        .background(Color(0xFFE0F2FE)),
                    contentAlignment = Alignment.Center
                ) {
                    Text("💧", fontSize = 16.sp)
                }
                Spacer(Modifier.height(12.dp))
                Text("Humidity", fontSize = 11.sp, color = TextMuted)
                Text("$humidity%", fontSize = 26.sp, fontWeight = FontWeight.Bold, color = TextDark)
                Text("Dew point 22°", fontSize = 11.sp, color = TextMuted)
            }

            // Vertical Liquid Capsule Level Meter (Reel 1)
            Box(
                modifier = Modifier
                    .width(14.dp)
                    .height(52.dp)
                    .clip(RoundedCornerShape(8.dp))
                    .background(Color(0xFFE0F2FE)),
                contentAlignment = Alignment.BottomCenter
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .fillMaxHeight(humidity / 100f)
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

@Composable
private fun WindTile(windSpeed: Int, modifier: Modifier = Modifier) {
    val transition = rememberInfiniteTransition(label = "turbine_spin_card")
    val bladeAngle by transition.animateFloat(
        initialValue = 0f,
        targetValue = 360f,
        animationSpec = infiniteRepeatable(
            animation = tween(2200, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "wind_spin"
    )

    Surface(
        color = Color.White,
        shape = RoundedCornerShape(20.dp),
        shadowElevation = 2.dp,
        border = BorderStroke(1.dp, CardBorder),
        modifier = modifier
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(14.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Box(
                    modifier = Modifier
                        .size(36.dp)
                        .clip(CircleShape)
                        .background(Color(0xFFDCFCE7)),
                    contentAlignment = Alignment.Center
                ) {
                    Text("💨", fontSize = 16.sp)
                }
                Spacer(Modifier.height(12.dp))
                Text("Wind", fontSize = 11.sp, color = TextMuted)
                Text("$windSpeed km/h", fontSize = 22.sp, fontWeight = FontWeight.Bold, color = TextDark)
                Text("NW · Gentle breeze", fontSize = 11.sp, color = TextMuted)
            }

            // Rotating 3-Blade Wind Turbine
            Canvas(modifier = Modifier.size(36.dp)) {
                val cx = size.width / 2f
                val cy = size.height * 0.42f
                val poleH = size.height * 0.52f
                drawLine(Color(0xFF0F766E), Offset(cx, cy), Offset(cx, cy + poleH), strokeWidth = 2.dp.toPx())
                drawCircle(Color(0xFF115E59), 2.5.dp.toPx(), Offset(cx, cy))
                val bladeLen = size.width * 0.42f
                for (b in 0..2) {
                    val rad = Math.toRadians((bladeAngle + b * 120).toDouble())
                    val tip = Offset(cx + (bladeLen * cos(rad)).toFloat(), cy + (bladeLen * sin(rad)).toFloat())
                    drawLine(Color(0xFF134E4A), Offset(cx, cy), tip, strokeWidth = 1.8.dp.toPx())
                }
            }
        }
    }
}

@Composable
private fun RainChanceTile(rainChance: Int, modifier: Modifier = Modifier) {
    Surface(
        color = Color.White,
        shape = RoundedCornerShape(20.dp),
        shadowElevation = 2.dp,
        border = BorderStroke(1.dp, CardBorder),
        modifier = modifier
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            Box(
                modifier = Modifier
                    .size(36.dp)
                    .clip(CircleShape)
                    .background(Color(0xFFE0F2FE)),
                contentAlignment = Alignment.Center
            ) {
                Text("🌧️", fontSize = 16.sp)
            }
            Spacer(Modifier.height(12.dp))
            Text("Rain chance", fontSize = 11.sp, color = TextMuted)
            Text("$rainChance%", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = TextDark)
            Text(if (rainChance > 40) "Expected: 14 mm" else "Expected: None", fontSize = 11.sp, color = TextMuted)
        }
    }
}

@Composable
private fun HourlyTemperatureChipsRow() {
    val hourlyTemps = listOf(
        "28°" to true,
        "29°" to false,
        "30°" to false,
        "31°" to false,
        "31°" to false,
        "30°" to false,
        "29°" to false
    )

    LazyRow(
        contentPadding = PaddingValues(horizontal = 20.dp, vertical = 12.dp),
        horizontalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        items(hourlyTemps) { (temp, isSelected) ->
            Surface(
                color = if (isSelected) Color(0xFF15803D) else Color.White,
                shape = RoundedCornerShape(16.dp),
                border = if (isSelected) null else BorderStroke(1.dp, CardBorder),
                shadowElevation = if (isSelected) 2.dp else 1.dp
            ) {
                Text(
                    text = temp,
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Bold,
                    color = if (isSelected) Color.White else TextDark,
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 10.dp)
                )
            }
        }
    }
}

@Composable
private fun Forecast7DaySection() {
    val forecastDays = listOf(
        ForecastRowData("Today", 15, "☀️", 21, 29, 0.85f),
        ForecastRowData("Tuesday", 20, "⛅", 21, 28, 0.70f),
        ForecastRowData("Wednesday", 35, "☁️", 20, 27, 0.55f),
        ForecastRowData("Thursday", 25, "⛅", 20, 28, 0.65f),
        ForecastRowData("Friday", 80, "🌧️", 19, 25, 0.35f),
        ForecastRowData("Saturday", 70, "⛈️", 19, 24, 0.25f),
        ForecastRowData("Sunday", 10, "☀️", 21, 29, 0.90f)
    )

    Column(modifier = Modifier.padding(horizontal = 20.dp, vertical = 8.dp)) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("7-day forecast", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = TextDark)
            Text("19° - 29°", fontSize = 13.sp, color = TextMuted)
        }

        Spacer(Modifier.height(10.dp))

        Surface(
            color = Color.White,
            shape = RoundedCornerShape(22.dp),
            shadowElevation = 2.dp,
            border = BorderStroke(1.dp, CardBorder),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(horizontal = 16.dp, vertical = 10.dp)) {
                forecastDays.forEachIndexed { idx, day ->
                    ForecastDayRow(day)
                    if (idx < forecastDays.lastIndex) {
                        HorizontalDivider(color = Color(0xFFF1F5F9), thickness = 1.dp)
                    }
                }
            }
        }
    }
}

@Composable
private fun ForecastDayRow(day: ForecastRowData) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column(modifier = Modifier.width(84.dp)) {
            Text(day.dayName, fontSize = 14.sp, fontWeight = FontWeight.Bold, color = TextDark)
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("💧", fontSize = 9.sp)
                Spacer(Modifier.width(2.dp))
                Text("${day.rainPercent}%", fontSize = 11.sp, color = Color(0xFF0284C7))
            }
        }

        Text(day.iconEmoji, fontSize = 18.sp, modifier = Modifier.width(32.dp))

        Text("${day.lowTemp}°", fontSize = 13.sp, color = TextMuted, modifier = Modifier.width(30.dp))

        // Low-High Gradient Bar with Current Temp Circle Indicator (Reel 1)
        Box(
            modifier = Modifier
                .weight(1f)
                .height(6.dp)
                .clip(RoundedCornerShape(3.dp))
                .background(Color(0xFFE2E8F0))
        ) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(
                        Brush.horizontalGradient(
                            listOf(Color(0xFF4ADE80), Color(0xFFF59E0B), Color(0xFFEF4444))
                        )
                    )
            )
            // Dot Indicator
            Box(
                modifier = Modifier
                    .offset(x = 60.dp * day.currentTempRatio)
                    .size(6.dp)
                    .clip(CircleShape)
                    .background(Color.White)
            )
        }

        Spacer(Modifier.width(8.dp))
        Text("${day.highTemp}°", fontSize = 13.sp, fontWeight = FontWeight.Bold, color = TextDark, modifier = Modifier.width(30.dp))
        Icon(Icons.Default.KeyboardArrowDown, contentDescription = null, tint = TextMuted, modifier = Modifier.size(16.dp))
    }
}

@Composable
private fun FarmRecommendationsCard() {
    Column(modifier = Modifier.padding(horizontal = 20.dp, vertical = 8.dp)) {
        Text("Farm recommendations", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = TextDark)
        Text("Based on your crops and the forecast", fontSize = 12.sp, color = TextMuted)
        Spacer(Modifier.height(10.dp))

        Surface(
            color = Color.White,
            shape = RoundedCornerShape(20.dp),
            shadowElevation = 2.dp,
            border = BorderStroke(1.dp, CardBorder),
            modifier = Modifier.fillMaxWidth()
        ) {
            Row(
                modifier = Modifier.padding(16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    modifier = Modifier
                        .size(44.dp)
                        .clip(CircleShape)
                        .background(Color(0xFFE0F2FE)),
                    contentAlignment = Alignment.Center
                ) {
                    Text("💧", fontSize = 20.sp)
                }
                Spacer(Modifier.width(14.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Surface(
                        color = Color(0xFFE0F2FE),
                        shape = RoundedCornerShape(8.dp)
                    ) {
                        Text(
                            text = "Tomorrow · 6-8 AM",
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFF0369A1),
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp)
                        )
                    }
                    Spacer(Modifier.height(4.dp))
                    Text(
                        text = "Watering recommended tomorrow morning",
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Bold,
                        color = TextDark
                    )
                    Text(
                        text = "Tomatoes need moisture before afternoon heat.",
                        fontSize = 12.sp,
                        color = TextMuted
                    )
                }
            }
        }
    }
}
