package com.agrisage.app.ui.screens

import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.FilterList
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.agrisage.app.navigation.FieldDetail
import com.agrisage.app.ui.components.AgriBottomNav
import com.agrisage.app.ui.components.tactilePress
import com.agrisage.app.ui.theme.*

/**
 * Screen: Farm Screen / Management View (Replicated from Reference Reel 2 - DailyFlutterUI Farm App)
 * Route: Fields
 *
 * Features:
 * - Clean Top Bar with circular back button & Green Valley Farm selector pill
 * - Farm Health Index Card with circular progress gauge (92% Healthy) & telemetry summary
 * - Interactive filter pills: All Plots (3), Crops 🌱 (2), Livestock 🐮 (1)
 * - Rich Plot & Field Cards with pastel icon pills, NDVI meters, soil moisture gauges, and action controls
 * - AgriBottomNav integration
 */

enum class FarmFilter {
    ALL, CROPS, LIVESTOCK
}

data class FarmEntity(
    val id: String,
    val name: String,
    val category: FarmFilter,
    val emoji: String,
    val badgeBg: Color,
    val badgeText: Color,
    val subhead: String,
    val areaOrCount: String,
    val healthPercent: Int,
    val healthLabel: String,
    val moistureOrMetric: String,
    val moisturePercent: Int,
    val secondaryMetric: String,
    val statusChip: String,
    val isActionNeeded: Boolean = false
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FieldsScreen(navController: NavController) {
    var activeFilter by remember { mutableStateOf(FarmFilter.ALL) }

    val farmEntities = listOf(
        FarmEntity(
            id = "1",
            name = "North Paddy Field",
            category = FarmFilter.CROPS,
            emoji = "🌾",
            badgeBg = Color(0xFFDCFCE7),
            badgeText = Color(0xFF166534),
            subhead = "Basmati Rice · Vegetative Stage (Day 45)",
            areaOrCount = "2.5 Acres",
            healthPercent = 94,
            healthLabel = "Optimal NDVI 0.78",
            moistureOrMetric = "Soil Moisture: 76%",
            moisturePercent = 76,
            secondaryMetric = "Water level 4.2 cm · Last fed Yesterday",
            statusChip = "● Irrigation Active"
        ),
        FarmEntity(
            id = "2",
            name = "Coconut & Fruit Grove",
            category = FarmFilter.CROPS,
            emoji = "🥥",
            badgeBg = Color(0xFFFEF3C7),
            badgeText = Color(0xFF92400E),
            subhead = "Hybrid Coconut Palms & Tapioca Intercrop",
            areaOrCount = "1.2 Acres",
            healthPercent = 88,
            healthLabel = "Good NDVI 0.68",
            moistureOrMetric = "Soil Moisture: 68%",
            moisturePercent = 68,
            secondaryMetric = "Fertilizer due in 3 days · Weed-free",
            statusChip = "● Healthy"
        ),
        FarmEntity(
            id = "3",
            name = "Dairy Pasture & Shed",
            category = FarmFilter.LIVESTOCK,
            emoji = "🐮",
            badgeBg = Color(0xFFFFEDD5),
            badgeText = Color(0xFF9A3412),
            subhead = "Holstein Dairy Cows & Calves",
            areaOrCount = "48 Animals (0.8 Ac)",
            healthPercent = 96,
            healthLabel = "Optimal Vitality",
            moistureOrMetric = "Feed Reserve: 92%",
            moisturePercent = 92,
            secondaryMetric = "Daily Milk 420 L · Water Dispenser Active",
            statusChip = "● Grazing Active"
        )
    )

    val filteredEntities = remember(activeFilter) {
        when (activeFilter) {
            FarmFilter.ALL -> farmEntities
            FarmFilter.CROPS -> farmEntities.filter { it.category == FarmFilter.CROPS }
            FarmFilter.LIVESTOCK -> farmEntities.filter { it.category == FarmFilter.LIVESTOCK }
        }
    }

    Scaffold(
        topBar = {
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

                    // Farm Selector Pill
                    Surface(
                        color = Color(0xFFF1F5F9),
                        shape = RoundedCornerShape(20.dp),
                        modifier = Modifier.height(38.dp)
                    ) {
                        Row(
                            modifier = Modifier.padding(horizontal = 14.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text("🌿", fontSize = 14.sp)
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

                    // Filter Action Button
                    Box(
                        modifier = Modifier
                            .size(42.dp)
                            .clip(CircleShape)
                            .background(Color.White)
                            .border(1.dp, Color(0xFFE2E8F0), CircleShape)
                            .clickable { /* Filter */ },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = Icons.Default.FilterList,
                            contentDescription = "Filter",
                            tint = Color(0xFF1E293B),
                            modifier = Modifier.size(20.dp)
                        )
                    }
                }
            }
        },
        bottomBar = {
            AgriBottomNav(
                currentRoute = "fields",
                onNavigate = { route ->
                    when (route) {
                        "home" -> navController.navigate(com.agrisage.app.navigation.Home) { popUpTo(com.agrisage.app.navigation.Home) { inclusive = true } }
                        "advisor" -> navController.navigate(com.agrisage.app.navigation.Advisor)
                        "weather" -> navController.navigate(com.agrisage.app.navigation.Weather)
                        "profile" -> navController.navigate(com.agrisage.app.navigation.Profile)
                    }
                }
            )
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = { /* Add field */ },
                containerColor = Color(0xFF16A34A),
                contentColor = Color.White,
                shape = RoundedCornerShape(16.dp),
                elevation = FloatingActionButtonDefaults.elevation(4.dp)
            ) {
                Row(
                    modifier = Modifier.padding(horizontal = 16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Default.Add, contentDescription = "Add Plot")
                    Spacer(Modifier.width(6.dp))
                    Text("Add Plot", fontWeight = FontWeight.Bold, fontSize = 14.sp)
                }
            }
        }
    ) { innerPadding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .background(Color(0xFFF8FAFC)),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // ── FARM HEALTH INDEX HERO CARD (Reel 2 Inspired) ──
            item {
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .shadow(2.dp, RoundedCornerShape(24.dp), ambientColor = Color(0x14000000)),
                    shape = RoundedCornerShape(24.dp),
                    colors = CardDefaults.cardColors(containerColor = Color.White)
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .border(1.dp, Color(0xFFF1F5F9), RoundedCornerShape(24.dp))
                            .padding(20.dp)
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column {
                                Text(
                                    text = "Farm Health Index",
                                    fontSize = 13.sp,
                                    fontWeight = FontWeight.Medium,
                                    color = Color(0xFF64748B)
                                )
                                Spacer(Modifier.height(2.dp))
                                Text(
                                    text = "92% · Optimal",
                                    fontSize = 22.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = Color(0xFF0F172A)
                                )
                            }

                            // Circular Progress Ring Gauge
                            Box(
                                modifier = Modifier.size(54.dp),
                                contentAlignment = Alignment.Center
                            ) {
                                CircularProgressIndicator(
                                    progress = { 0.92f },
                                    modifier = Modifier.fillMaxSize(),
                                    color = Color(0xFF16A34A),
                                    trackColor = Color(0xFFDCFCE7),
                                    strokeWidth = 5.dp,
                                    strokeCap = StrokeCap.Round
                                )
                                Text(
                                    text = "92%",
                                    fontSize = 13.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = Color(0xFF0F172A)
                                )
                            }
                        }

                        Spacer(Modifier.height(16.dp))
                        HorizontalDivider(color = Color(0xFFF1F5F9))
                        Spacer(Modifier.height(14.dp))

                        // Stats Summary Row
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            FarmSummaryPill("Total Area", "4.5 Acres", "🌱")
                            FarmSummaryPill("Active Plots", "3 Plots", "📍")
                            FarmSummaryPill("Livestock", "48 Cattle", "🐮")
                        }
                    }
                }
            }

            // ── SEGMENTED FILTER PILLS ──
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    FilterPill(
                        label = "All Plots (3)",
                        isSelected = activeFilter == FarmFilter.ALL,
                        onClick = { activeFilter = FarmFilter.ALL },
                        modifier = Modifier.weight(1f)
                    )
                    FilterPill(
                        label = "Crops 🌱 (2)",
                        isSelected = activeFilter == FarmFilter.CROPS,
                        onClick = { activeFilter = FarmFilter.CROPS },
                        modifier = Modifier.weight(1f)
                    )
                    FilterPill(
                        label = "Livestock 🐮 (1)",
                        isSelected = activeFilter == FarmFilter.LIVESTOCK,
                        onClick = { activeFilter = FarmFilter.LIVESTOCK },
                        modifier = Modifier.weight(1f)
                    )
                }
            }

            // ── FARM PLOT & ENTITY CARDS ──
            items(filteredEntities.size) { i ->
                val entity = filteredEntities[i]
                FarmEntityCard(
                    entity = entity,
                    onClick = { navController.navigate(FieldDetail(fieldId = entity.id)) }
                )
            }

            item {
                Spacer(Modifier.height(60.dp))
            }
        }
    }
}

@Composable
private fun FarmSummaryPill(title: String, value: String, emoji: String) {
    Column {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(emoji, fontSize = 12.sp)
            Spacer(Modifier.width(4.dp))
            Text(title, fontSize = 11.sp, color = Color(0xFF64748B))
        }
        Spacer(Modifier.height(2.dp))
        Text(value, fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color(0xFF0F172A))
    }
}

@Composable
private fun FilterPill(
    label: String,
    isSelected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val bgAnim by animateColorAsState(
        targetValue = if (isSelected) Color(0xFF1E293B) else Color.White,
        label = "filter_pill_bg"
    )
    val textAnim by animateColorAsState(
        targetValue = if (isSelected) Color.White else Color(0xFF64748B),
        label = "filter_pill_text"
    )

    Surface(
        color = bgAnim,
        shape = RoundedCornerShape(16.dp),
        border = if (isSelected) null else androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFE2E8F0)),
        shadowElevation = if (isSelected) 2.dp else 0.5.dp,
        modifier = modifier
            .height(40.dp)
            .tactilePress(scaleDown = 0.94f, onClick = onClick)
    ) {
        Box(contentAlignment = Alignment.Center, modifier = Modifier.fillMaxSize()) {
            Text(
                text = label,
                fontSize = 12.sp,
                fontWeight = FontWeight.SemiBold,
                color = textAnim
            )
        }
    }
}

@Composable
private fun FarmEntityCard(
    entity: FarmEntity,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(22.dp))
            .tactilePress(scaleDown = 0.97f, onClick = onClick),
        shape = RoundedCornerShape(22.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, Color(0xFFF1F5F9), RoundedCornerShape(22.dp))
                .padding(18.dp)
        ) {
            // Header Row: Pastel Badge + Title/Subhead + Circular Navigation Chevron
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.weight(1f)) {
                    // Pastel Emoji Badge
                    Box(
                        modifier = Modifier
                            .size(46.dp)
                            .clip(RoundedCornerShape(14.dp))
                            .background(entity.badgeBg),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(entity.emoji, fontSize = 22.sp)
                    }

                    Spacer(Modifier.width(14.dp))

                    Column {
                        Text(
                            text = entity.name,
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFF0F172A)
                        )
                        Spacer(Modifier.height(2.dp))
                        Text(
                            text = entity.areaOrCount,
                            fontSize = 12.sp,
                            color = Color(0xFF64748B),
                            fontWeight = FontWeight.Medium
                        )
                    }
                }

                // Status Badge Chip
                Surface(
                    color = Color(0xFFDCFCE7),
                    shape = RoundedCornerShape(10.dp)
                ) {
                    Text(
                        text = entity.statusChip,
                        color = Color(0xFF166534),
                        fontWeight = FontWeight.SemiBold,
                        fontSize = 11.sp,
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                    )
                }
            }

            Spacer(Modifier.height(14.dp))

            // Subhead Stage description
            Text(
                text = entity.subhead,
                fontSize = 13.sp,
                fontWeight = FontWeight.Medium,
                color = Color(0xFF334155)
            )

            Spacer(Modifier.height(12.dp))

            // Progress Gauge Row: Soil Moisture or Feed Meter
            Column {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = entity.moistureOrMetric,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = Color(0xFF0F172A)
                    )
                    Text(
                        text = entity.healthLabel,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = Color(0xFF16A34A)
                    )
                }
                Spacer(Modifier.height(6.dp))
                // Progress Bar
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(6.dp)
                        .clip(RoundedCornerShape(3.dp))
                        .background(Color(0xFFE2E8F0))
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth(entity.moisturePercent / 100f)
                            .fillMaxHeight()
                            .clip(RoundedCornerShape(3.dp))
                            .background(Color(0xFF16A34A))
                    )
                }
            }

            Spacer(Modifier.height(12.dp))

            // Footer Details & Chevron Action
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = entity.secondaryMetric,
                    fontSize = 11.sp,
                    color = Color(0xFF94A3B8)
                )

                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.clickable(onClick = onClick)
                ) {
                    Text(
                        text = "Manage",
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color(0xFF16A34A)
                    )
                    Icon(
                        imageVector = Icons.AutoMirrored.Filled.KeyboardArrowRight,
                        contentDescription = "Details",
                        tint = Color(0xFF16A34A),
                        modifier = Modifier.size(16.dp)
                    )
                }
            }
        }
    }
}
