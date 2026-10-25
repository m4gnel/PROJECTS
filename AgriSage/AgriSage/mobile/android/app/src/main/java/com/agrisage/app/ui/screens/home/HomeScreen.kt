package com.agrisage.app.ui.screens.home

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.wrapContentHeight
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Agriculture
import androidx.compose.material.icons.filled.Eco
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Pets
import androidx.compose.material.icons.filled.ShoppingBasket
import androidx.compose.material.icons.filled.SmartToy
import androidx.compose.material.icons.filled.WaterDrop
import androidx.compose.material.icons.filled.WbSunny
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavHostController
import com.agrisage.app.navigation.Screen
import com.agrisage.app.ui.components.FarmIllustration
import com.agrisage.app.ui.components.QuickStatCard
import com.agrisage.app.ui.components.WeatherVisualMode
import com.agrisage.app.ui.components.tactilePress
import java.util.Locale
import kotlin.math.roundToInt

private val HomeCanvas = Color(0xFFF8FAFC)
private val HomeText = Color(0xFF0F172A)
private val HomeMuted = Color(0xFF64748B)
private val HomeBorder = Color(0xFFE2E8F0)
private val HomeGreen = Color(0xFF16A34A)

@Composable
fun HomeScreen(
    navController: NavHostController,
    viewModel: HomeViewModel = hiltViewModel()
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    val preview = homeReferencePreviewData

    // The separate reference-preview install never reads a real account/cache.
    val displayName = state.farmerName.trim().takeIf(String::isNotEmpty)
        ?: preview?.farmerName
    val farmName = state.farmerName.trim().takeIf(String::isNotEmpty)
        ?.let { "$it's Farm" }
        ?: preview?.farmName
        ?: "Farm profile unavailable"
    val displayWeather = state.weather ?: preview?.weather
    val displayHealth = state.farmHealth ?: preview?.farmHealth
    val displayStats = HomeQuickStats(
        cropCount = state.quickStats.cropCount ?: preview?.quickStats?.cropCount,
        animalCount = state.quickStats.animalCount ?: preview?.quickStats?.animalCount,
        soilMoisturePercent = state.quickStats.soilMoisturePercent
            ?: preview?.quickStats?.soilMoisturePercent,
        harvestYieldKg = state.quickStats.harvestYieldKg ?: preview?.quickStats?.harvestYieldKg
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(HomeCanvas)
    ) {
        HomeHeader(
            displayName = displayName,
            farmName = farmName,
            hasUnreadAlerts = state.activeAlerts.any { !it.isRead },
            onProfileClick = { navController.navigate(Screen.Profile) },
            onFarmClick = { navController.navigate(Screen.Fields) },
            onAlertsClick = { navController.navigate(Screen.Alerts) }
        )

        LazyColumn(
            modifier = Modifier
            .fillMaxWidth()
            .weight(1f),
            contentPadding = PaddingValues(bottom = 28.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item {
                HomeHero(
                    weather = displayWeather,
                    farmHealth = displayHealth,
                    onHealthClick = { navController.navigate(Screen.Fields) },
                    onWeatherClick = { navController.navigate(Screen.Weather) }
                )
            }

            item {
                QuickStatsSection(
                    stats = displayStats,
                    onStatsClick = { navController.navigate(Screen.Fields) }
                )
            }

            item {
                SmartFarmingTools(
                    weatherAvailable = state.weather != null,
                    onAdvisorClick = { navController.navigate(Screen.Advisor) },
                    onFieldsClick = { navController.navigate(Screen.Fields) },
                    onWeatherClick = { navController.navigate(Screen.Weather) }
                )
            }
        }
    }
}

@Composable
private fun HomeHeader(
    displayName: String?,
    farmName: String,
    hasUnreadAlerts: Boolean,
    onProfileClick: () -> Unit,
    onFarmClick: () -> Unit,
    onAlertsClick: () -> Unit
) {
    Surface(
        color = Color.White,
        shadowElevation = 1.dp,
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .statusBarsPadding()
                .padding(horizontal = 16.dp, vertical = 6.dp)
                .heightIn(min = 56.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Row(
                modifier = Modifier
                    .weight(1f)
                    .defaultMinSize(minHeight = 48.dp)
                    .semantics(mergeDescendants = true) {
                        contentDescription = "Open profile"
                        role = Role.Button
                    }
                    .tactilePress(
                        scaleDown = 0.97f,
                        onClickLabel = "Open profile",
                        onClick = onProfileClick
                    ),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    modifier = Modifier
                        .size(44.dp)
                        .clip(CircleShape)
                        .background(
                            Brush.linearGradient(
                                listOf(Color(0xFF86EFAC), Color(0xFF22C55E))
                            )
                        )
                        .border(2.dp, Color.White, CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.Default.Person,
                        contentDescription = null,
                        tint = Color.White,
                        modifier = Modifier.size(23.dp)
                    )
                }

                Spacer(modifier = Modifier.width(10.dp))

                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = if (displayName.isNullOrBlank()) {
                            "Good afternoon"
                        } else {
                            "Good afternoon, $displayName"
                        },
                        color = HomeMuted,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Medium,
                        maxLines = 1
                    )

                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .heightIn(min = 28.dp)
                            .semantics {
                                contentDescription = "Select $farmName"
                                role = Role.Button
                            }
                            .tactilePress(
                                scaleDown = 0.98f,
                                onClickLabel = "Select farm",
                                onClick = onFarmClick
                            ),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = farmName,
                            color = HomeText,
                            fontSize = 17.sp,
                            fontWeight = FontWeight.Bold,
                            maxLines = 1
                        )
                        Icon(
                            imageVector = Icons.Default.KeyboardArrowDown,
                            contentDescription = null,
                            tint = HomeMuted,
                            modifier = Modifier
                                .padding(start = 2.dp)
                                .size(19.dp)
                        )
                    }
                }
            }

            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(CircleShape)
                    .background(HomeCanvas)
                    .border(1.dp, HomeBorder, CircleShape)
                    .semantics {
                        contentDescription = "Open alerts"
                        role = Role.Button
                    }
                    .tactilePress(
                        scaleDown = 0.95f,
                        onClickLabel = "Open alerts",
                        onClick = onAlertsClick
                    ),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Default.Notifications,
                    contentDescription = null,
                    tint = Color(0xFF334155),
                    modifier = Modifier.size(22.dp)
                )
                if (hasUnreadAlerts) {
                    Box(
                        modifier = Modifier
                            .align(Alignment.TopEnd)
                            .offset(x = (-9).dp, y = 9.dp)
                            .size(8.dp)
                            .clip(CircleShape)
                            .background(Color(0xFFEF4444))
                    )
                }
            }
        }
    }
}

@Composable
private fun HomeHero(
    weather: WeatherSummary?,
    farmHealth: FarmHealthSummary?,
    onHealthClick: () -> Unit,
    onWeatherClick: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp)
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(188.dp)
                .shadow(
                    elevation = 6.dp,
                    shape = RoundedCornerShape(24.dp),
                    ambientColor = Color(0x24000000),
                    spotColor = Color(0x24000000)
                )
                .clip(RoundedCornerShape(24.dp))
        ) {
            FarmIllustration(
                modifier = Modifier.fillMaxSize(),
                weatherMode = weatherVisualMode(weather?.condition),
                isAnimated = true
            )
        }

        Spacer(modifier = Modifier.height(12.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            FarmHealthKpi(
                health = farmHealth,
                modifier = Modifier.weight(1f),
                onClick = onHealthClick
            )
            WeatherKpi(
                weather = weather,
                modifier = Modifier.weight(1f),
                onClick = onWeatherClick
            )
        }
    }
}

@Composable
private fun FarmHealthKpi(
    health: FarmHealthSummary?,
    modifier: Modifier = Modifier,
    onClick: () -> Unit
) {
    val score = health?.scorePercent?.coerceIn(0, 100)
    val status = health?.status?.trim()?.takeIf(String::isNotEmpty)
    val description = if (score == null) {
        "Farm health unavailable"
    } else {
        "Farm health: $score percent${status?.let { ", $it" } ?: ""}"
    }

    Card(
        modifier = modifier
            .height(88.dp)
            .semantics(mergeDescendants = true) {
                contentDescription = description
                role = Role.Button
            }
            .tactilePress(
                scaleDown = 0.96f,
                onClickLabel = "Open farm health",
                onClick = onClick
            ),
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxSize()
                .border(1.dp, Color(0xFFF1F5F9), RoundedCornerShape(20.dp))
                .padding(horizontal = 12.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier.size(52.dp),
                contentAlignment = Alignment.Center
            ) {
                if (score == null) {
                    Box(
                        modifier = Modifier
                            .size(46.dp)
                            .clip(CircleShape)
                            .background(Color(0xFFF1F5F9)),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = "—",
                            color = HomeMuted,
                            fontSize = 18.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                } else {
                    CircularProgressIndicator(
                        progress = { score / 100f },
                        modifier = Modifier.fillMaxSize(),
                        color = HomeGreen,
                        trackColor = Color(0xFFDCFCE7),
                        strokeWidth = 4.5.dp
                    )
                    Text(
                        text = "$score%",
                        color = HomeText,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }

            Spacer(modifier = Modifier.width(9.dp))

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = "Farm Health",
                    color = HomeMuted,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Medium,
                    maxLines = 1
                )
                Text(
                    text = status ?: "Unavailable",
                    color = HomeText,
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Bold,
                    maxLines = 1
                )
                if (status != null) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.padding(top = 2.dp)
                    ) {
                        Box(
                            modifier = Modifier
                                .size(6.dp)
                                .clip(CircleShape)
                                .background(HomeGreen)
                        )
                        Spacer(modifier = Modifier.width(4.dp))
                        Text(
                            text = "All good",
                            color = HomeGreen,
                            fontSize = 10.sp,
                            fontWeight = FontWeight.SemiBold,
                            maxLines = 1
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun WeatherKpi(
    weather: WeatherSummary?,
    modifier: Modifier = Modifier,
    onClick: () -> Unit
) {
    val temperature = weather?.tempCelsius?.roundToInt()
    val condition = weather?.condition?.displayCondition()
    val description = if (temperature == null || condition == null) {
        "Weather unavailable"
    } else {
        "Weather: $temperature degrees Celsius, $condition"
    }

    Card(
        modifier = modifier
            .height(88.dp)
            .semantics(mergeDescendants = true) {
                contentDescription = description
                role = Role.Button
            }
            .tactilePress(
                scaleDown = 0.96f,
                onClickLabel = "Open weather",
                onClick = onClick
            ),
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxSize()
                .border(1.dp, Color(0xFFF1F5F9), RoundedCornerShape(20.dp))
                .padding(horizontal = 12.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(46.dp)
                    .clip(RoundedCornerShape(14.dp))
                    .background(Color(0xFFFEF3C7)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Default.WbSunny,
                    contentDescription = null,
                    tint = Color(0xFFF59E0B),
                    modifier = Modifier.size(24.dp)
                )
            }

            Spacer(modifier = Modifier.width(9.dp))

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = temperature?.let { "$it°C" } ?: "—",
                    color = HomeText,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    maxLines = 1
                )
                Text(
                    text = condition ?: "Unavailable",
                    color = HomeMuted,
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Medium,
                    maxLines = 1
                )
                if (weather?.humidity != null && weather.humidity > 0) {
                    Text(
                        text = "${weather.humidity}% humidity",
                        color = Color(0xFF94A3B8),
                        fontSize = 10.sp,
                        fontWeight = FontWeight.Medium,
                        maxLines = 1,
                        modifier = Modifier.padding(top = 2.dp)
                    )
                }
            }
        }
    }
}

@Composable
private fun QuickStatsSection(
    stats: HomeQuickStats,
    onStatsClick: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                text = "Quick Stats",
                color = HomeText,
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold
            )
            Text(
                text = "Overview",
                color = HomeGreen,
                fontSize = 13.sp,
                fontWeight = FontWeight.SemiBold,
                modifier = Modifier
                    .defaultMinSize(minWidth = 48.dp, minHeight = 48.dp)
                    .semantics {
                        contentDescription = "Open fields overview"
                        role = Role.Button
                    }
                    .tactilePress(
                        scaleDown = 0.97f,
                        onClickLabel = "Open fields overview",
                        onClick = onStatsClick
                    )
                    .wrapContentHeight(Alignment.CenterVertically)
            )
        }

        Spacer(modifier = Modifier.height(4.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            QuickStatCard(
                iconVector = Icons.Default.Eco,
                value = stats.cropCount?.toString() ?: "—",
                label = "Crops",
                badgeBgColor = Color(0xFFDCFCE7),
                badgeTextColor = Color(0xFF166534),
                modifier = Modifier.weight(1f),
                onClick = onStatsClick
            )
            QuickStatCard(
                iconVector = Icons.Default.Pets,
                value = stats.animalCount?.toString() ?: "—",
                label = "Animals",
                badgeBgColor = Color(0xFFFFEDD5),
                badgeTextColor = Color(0xFF9A3412),
                modifier = Modifier.weight(1f),
                onClick = onStatsClick
            )
        }

        Spacer(modifier = Modifier.height(12.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            QuickStatCard(
                iconVector = Icons.Default.WaterDrop,
                value = stats.soilMoisturePercent?.let { "$it%" } ?: "—",
                label = "Soil Moisture",
                badgeBgColor = Color(0xFFE0F2FE),
                badgeTextColor = Color(0xFF0369A1),
                modifier = Modifier.weight(1f),
                onClick = onStatsClick
            )
            QuickStatCard(
                iconVector = Icons.Default.ShoppingBasket,
                value = stats.harvestYieldKg?.let { "${it.toString().withGrouping()} kg" } ?: "—",
                label = "Harvest Yield",
                badgeBgColor = Color(0xFFFEF3C7),
                badgeTextColor = Color(0xFF92400E),
                modifier = Modifier.weight(1f),
                onClick = onStatsClick
            )
        }
    }
}

@Composable
private fun SmartFarmingTools(
    weatherAvailable: Boolean,
    onAdvisorClick: () -> Unit,
    onFieldsClick: () -> Unit,
    onWeatherClick: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp)
    ) {
        Text(
            text = "Smart Farming Tools",
            color = HomeText,
            fontSize = 18.sp,
            fontWeight = FontWeight.Bold
        )

        Spacer(modifier = Modifier.height(12.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            SmartToolCard(
                title = "Ask Advisor",
                subtitle = "AI crop assistance",
                icon = Icons.Default.SmartToy,
                containerColor = Color(0xFF1B4332),
                onClick = onAdvisorClick,
                modifier = Modifier.weight(1f)
            )
            SmartToolCard(
                title = "Farm Insights",
                subtitle = "Review your fields",
                icon = Icons.Default.Agriculture,
                containerColor = Color(0xFF2D6A4F),
                onClick = onFieldsClick,
                modifier = Modifier.weight(1f)
            )
        }

        Spacer(modifier = Modifier.height(12.dp))

        Card(
            modifier = Modifier
                .fillMaxWidth()
                .semantics(mergeDescendants = true) {
                    contentDescription = "Open weather center"
                    role = Role.Button
                }
                .tactilePress(
                    scaleDown = 0.97f,
                    onClickLabel = "Open weather center",
                    onClick = onWeatherClick
                ),
            shape = RoundedCornerShape(20.dp),
            colors = CardDefaults.cardColors(containerColor = Color.White),
            elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .border(1.dp, Color(0xFFF1F5F9), RoundedCornerShape(20.dp))
                    .padding(14.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    modifier = Modifier
                        .size(42.dp)
                        .clip(RoundedCornerShape(12.dp))
                        .background(Color(0xFFFEF3C7)),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.Default.WbSunny,
                        contentDescription = null,
                        tint = Color(0xFFD97706),
                        modifier = Modifier.size(22.dp)
                    )
                }
                Spacer(modifier = Modifier.width(12.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = "Weather Center",
                        color = HomeText,
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        text = if (weatherAvailable) {
                            "Live provider weather"
                        } else {
                            "Weather data unavailable"
                        },
                        color = HomeMuted,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Medium,
                        modifier = Modifier.padding(top = 2.dp)
                    )
                }
            }
        }
    }
}

@Composable
private fun SmartToolCard(
    title: String,
    subtitle: String,
    icon: ImageVector,
    containerColor: Color,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .height(118.dp)
            .semantics(mergeDescendants = true) {
                contentDescription = "$title. $subtitle"
                role = Role.Button
            }
            .tactilePress(
                scaleDown = 0.95f,
                onClickLabel = title,
                onClick = onClick
            ),
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(containerColor = containerColor),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxHeight()
                .padding(14.dp),
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            Box(
                modifier = Modifier
                    .size(38.dp)
                    .clip(RoundedCornerShape(10.dp))
                    .background(Color.White.copy(alpha = 0.15f)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = icon,
                    contentDescription = null,
                    tint = Color.White,
                    modifier = Modifier.size(22.dp)
                )
            }

            Column {
                Text(
                    text = title,
                    color = Color.White,
                    fontSize = 15.sp,
                    fontWeight = FontWeight.Bold,
                    maxLines = 1
                )
                Text(
                    text = subtitle,
                    color = Color(0xFFD1FAE5),
                    fontSize = 11.sp,
                    maxLines = 1,
                    modifier = Modifier.padding(top = 2.dp)
                )
            }
        }
    }
}

private fun weatherVisualMode(condition: String?): WeatherVisualMode = when {
    condition == null -> WeatherVisualMode.SUNNY
    condition.contains("rain", ignoreCase = true) ||
        condition.contains("storm", ignoreCase = true) -> WeatherVisualMode.RAINY
    condition.contains("wind", ignoreCase = true) -> WeatherVisualMode.WINDY
    condition.contains("cloud", ignoreCase = true) ||
        condition.contains("overcast", ignoreCase = true) -> WeatherVisualMode.PARTLY_CLOUDY
    else -> WeatherVisualMode.SUNNY
}

private fun String.displayCondition(): String = replace('_', ' ')
    .trim()
    .lowercase(Locale.US)
    .split(' ')
    .filter(String::isNotBlank)
    .joinToString(" ") { word ->
        word.replaceFirstChar { it.titlecase(Locale.US) }
    }

private fun String.withGrouping(): String = reversed()
    .chunked(3)
    .joinToString(",")
    .reversed()
