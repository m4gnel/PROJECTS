package com.agrisage.app.ui.screens.fields

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.spring
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
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
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.NavHostController
import com.agrisage.app.navigation.Screen
import com.agrisage.app.ui.components.FarmMapCanvas
import com.agrisage.app.ui.components.FarmZone
import com.agrisage.app.ui.components.tactilePress

private val ScreenBackground = Color(0xFFF9FBF9)
private val TextDark = Color(0xFF18181B)
private val TextMuted = Color(0xFF64748B)
private val FarmGreen = Color(0xFF16A34A)
private val CardBorder = Color(0xFFE2E8F0)

data class CowItem(
    val name: String,
    val breed: String,
    val tag: String,
    val age: String,
    val healthPercent: Int
)

/**
 * Screen: "My Farm" & "Livestock" (Deterministic 1:1 replication from Reference Video 2).
 * Features:
 * - Clean Header with "My Farm", location pill & top-right Weather shortcut button
 * - Horizontal zone selection chips (Overview, House, Tomatoes, Vegetables, Corn, Animals, Water, Storage)
 * - Interactive Top-Down Aerial Farm Map Canvas with 7 selectable zones & glowing white borders
 * - Dynamic Context Card (Area metrics, status badges, smart watering, and "Open livestock →")
 * - 2x2 Explore Bento Grid (My Crops, Livestock, Watering, Weather)
 * - Sub-screen: Dedicated Livestock telemetry dashboard with 3 circular ring progress gauges, feeding timeline, category chips & cow roster
 */
@Composable
fun FieldsScreen(
    navController: NavHostController,
    viewModel: FieldsViewModel = hiltViewModel()
) {
    var selectedZone by remember { mutableStateOf(FarmZone.OVERVIEW) }
    var isShowingLivestock by remember { mutableStateOf(false) }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(ScreenBackground)
    ) {
        if (isShowingLivestock) {
            LivestockView(
                onNavigateBack = { isShowingLivestock = false }
            )
        } else {
            MyFarmView(
                selectedZone = selectedZone,
                onZoneSelected = { selectedZone = it },
                onNavigateToWeather = { navController.navigate(Screen.Weather) },
                onOpenLivestock = { isShowingLivestock = true }
            )
        }
    }
}

@Composable
private fun MyFarmView(
    selectedZone: FarmZone,
    onZoneSelected: (FarmZone) -> Unit,
    onNavigateToWeather: () -> Unit,
    onOpenLivestock: () -> Unit
) {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(bottom = 24.dp)
    ) {
        // 1. Top Header: "My Farm", Location subtitle, Circular Weather Button
        item {
            MyFarmHeader(onNavigateToWeather = onNavigateToWeather)
        }

        // 2. Horizontal Scrolling Zone Filter Chips
        item {
            FarmZoneChipsRow(
                selectedZone = selectedZone,
                onZoneSelected = onZoneSelected
            )
        }

        // 3. Central Interactive Farm Map Canvas
        item {
            Box(modifier = Modifier.padding(horizontal = 16.dp, vertical = 10.dp)) {
                FarmMapCanvas(
                    selectedZone = selectedZone,
                    onZoneSelected = onZoneSelected
                )
            }
        }

        // 4. Dynamic Context Card for the Selected Zone
        item {
            Box(modifier = Modifier.padding(horizontal = 16.dp, vertical = 4.dp)) {
                DynamicZoneCard(
                    zone = selectedZone,
                    onOpenLivestock = onOpenLivestock,
                    onSmartWatering = onNavigateToWeather
                )
            }
        }

        // 5. "Explore" Section Header
        item {
            Text(
                text = "Explore",
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                color = TextDark,
                modifier = Modifier.padding(start = 20.dp, top = 16.dp, bottom = 8.dp)
            )
        }

        // 6. 2x2 Bento Grid (My Crops, Livestock, Watering, Weather)
        item {
            ExploreBentoGrid(
                onCropsClick = { onZoneSelected(FarmZone.TOMATO_FIELD) },
                onLivestockClick = onOpenLivestock,
                onWateringClick = { onZoneSelected(FarmZone.WATER_TANK) },
                onWeatherClick = onNavigateToWeather
            )
        }
    }
}

@Composable
private fun MyFarmHeader(onNavigateToWeather: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .statusBarsPadding()
            .padding(horizontal = 20.dp, vertical = 12.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column {
            Text(
                text = "My Farm",
                fontSize = 26.sp,
                fontWeight = FontWeight.Bold,
                color = TextDark
            )
            Spacer(Modifier.height(2.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = Icons.Default.Place,
                    contentDescription = null,
                    tint = FarmGreen,
                    modifier = Modifier.size(15.dp)
                )
                Spacer(Modifier.width(4.dp))
                Text(
                    text = "Green Valley Farm · 12.5 ha",
                    fontSize = 12.sp,
                    color = TextMuted,
                    fontWeight = FontWeight.Medium
                )
            }
        }

        // Circular Weather Button at Top Right (Reel 1 & 2 transition)
        Surface(
            modifier = Modifier
                .size(44.dp)
                .tactilePress(scaleDown = 0.92f) { onNavigateToWeather() },
            shape = CircleShape,
            color = Color.White,
            shadowElevation = 2.dp,
            border = BorderStroke(1.dp, CardBorder)
        ) {
            Box(contentAlignment = Alignment.Center) {
                Icon(
                    imageVector = Icons.Default.WbSunny,
                    contentDescription = "Weather overview",
                    tint = TextDark,
                    modifier = Modifier.size(20.dp)
                )
            }
        }
    }
}

@Composable
private fun FarmZoneChipsRow(
    selectedZone: FarmZone,
    onZoneSelected: (FarmZone) -> Unit
) {
    val zones = FarmZone.values()
    LazyRow(
        contentPadding = PaddingValues(horizontal = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        modifier = Modifier.padding(vertical = 4.dp)
    ) {
        items(zones) { zone ->
            val isSelected = selectedZone == zone
            Surface(
                color = if (isSelected) Color(0xFF18181B) else Color.White,
                shape = RoundedCornerShape(20.dp),
                border = if (isSelected) null else BorderStroke(1.dp, CardBorder),
                shadowElevation = if (isSelected) 2.dp else 0.dp,
                modifier = Modifier.tactilePress(scaleDown = 0.95f) { onZoneSelected(zone) }
            ) {
                Row(
                    modifier = Modifier.padding(horizontal = 14.dp, vertical = 8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(text = zone.emoji, fontSize = 13.sp)
                    Spacer(Modifier.width(6.dp))
                    Text(
                        text = zone.title,
                        fontSize = 13.sp,
                        fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium,
                        color = if (isSelected) Color.White else TextDark
                    )
                }
            }
        }
    }
}

@Composable
private fun DynamicZoneCard(
    zone: FarmZone,
    onOpenLivestock: () -> Unit,
    onSmartWatering: () -> Unit
) {
    when (zone) {
        FarmZone.OVERVIEW -> {
            Surface(
                color = Color(0xFFDCFCE7),
                shape = RoundedCornerShape(20.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier.padding(horizontal = 18.dp, vertical = 16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .size(36.dp)
                            .clip(CircleShape)
                            .background(Color(0xFFBBF7D0)),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = Icons.Default.TouchApp,
                            contentDescription = null,
                            tint = Color(0xFF15803D),
                            modifier = Modifier.size(20.dp)
                        )
                    }
                    Spacer(Modifier.width(14.dp))
                    Column {
                        Text(
                            text = "Tap an area to explore",
                            fontSize = 15.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFF166534)
                        )
                        Text(
                            text = "7 zones · 4 crops · 48 animals",
                            fontSize = 12.sp,
                            color = Color(0xFF15803D)
                        )
                    }
                }
            }
        }

        FarmZone.ANIMAL_AREA -> {
            Surface(
                color = Color.White,
                shape = RoundedCornerShape(24.dp),
                shadowElevation = 2.dp,
                border = BorderStroke(1.dp, CardBorder),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(18.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .clip(RoundedCornerShape(12.dp))
                                .background(Color(0xFFFFEDD5)),
                            contentAlignment = Alignment.Center
                        ) {
                            Text("🐮", fontSize = 18.sp)
                        }
                        Spacer(Modifier.width(12.dp))
                        Text(
                            text = "Animal Area",
                            fontSize = 17.sp,
                            fontWeight = FontWeight.Bold,
                            color = TextDark
                        )
                    }

                    Spacer(Modifier.height(14.dp))

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        MetricSmallTile("Animals", "48", Modifier.weight(1f))
                        MetricSmallTile("Health", "96%", Modifier.weight(1f))
                        MetricSmallTile("Next feed", "6 PM", Modifier.weight(1f))
                    }

                    Spacer(Modifier.height(14.dp))

                    Button(
                        onClick = onOpenLivestock,
                        colors = ButtonDefaults.buttonColors(containerColor = FarmGreen),
                        shape = RoundedCornerShape(16.dp),
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(48.dp)
                    ) {
                        Text("Open livestock →", fontSize = 14.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }
        }

        FarmZone.CORN_FIELD -> {
            Surface(
                color = Color.White,
                shape = RoundedCornerShape(24.dp),
                shadowElevation = 2.dp,
                border = BorderStroke(1.dp, CardBorder),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(18.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(
                                modifier = Modifier
                                    .size(40.dp)
                                    .clip(RoundedCornerShape(12.dp))
                                    .background(Color(0xFFFEF3C7)),
                                contentAlignment = Alignment.Center
                            ) {
                                Text("🌽", fontSize = 18.sp)
                            }
                            Spacer(Modifier.width(12.dp))
                            Column {
                                Text("Corn Field", fontSize = 17.sp, fontWeight = FontWeight.Bold, color = TextDark)
                                Text("Crop: Corn", fontSize = 12.sp, color = TextMuted)
                            }
                        }
                        Surface(
                            color = Color(0xFFDCFCE7),
                            shape = RoundedCornerShape(10.dp)
                        ) {
                            Text("💚 Good", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = Color(0xFF166534), modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp))
                        }
                    }
                    Spacer(Modifier.height(14.dp))
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        MetricSmallTile("Growth", "58%", Modifier.weight(1f))
                        MetricSmallTile("Moisture", "64%", Modifier.weight(1f))
                        MetricSmallTile("Harvest", "24 d", Modifier.weight(1f))
                    }
                }
            }
        }

        FarmZone.WATER_TANK -> {
            Surface(
                color = Color.White,
                shape = RoundedCornerShape(24.dp),
                shadowElevation = 2.dp,
                border = BorderStroke(1.dp, CardBorder),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(18.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .clip(RoundedCornerShape(12.dp))
                                .background(Color(0xFFE0F2FE)),
                            contentAlignment = Alignment.Center
                        ) {
                            Text("💧", fontSize = 18.sp)
                        }
                        Spacer(Modifier.width(12.dp))
                        Text("Water Tank", fontSize = 17.sp, fontWeight = FontWeight.Bold, color = TextDark)
                    }
                    Spacer(Modifier.height(14.dp))
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        MetricSmallTile("Level", "82%", Modifier.weight(1f))
                        MetricSmallTile("Stored", "8,200 L", Modifier.weight(1f))
                        MetricSmallTile("Used today", "1,240 L", Modifier.weight(1f))
                    }
                    Spacer(Modifier.height(14.dp))
                    Button(
                        onClick = onSmartWatering,
                        colors = ButtonDefaults.buttonColors(containerColor = FarmGreen),
                        shape = RoundedCornerShape(16.dp),
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(48.dp)
                    ) {
                        Text("Smart watering →", fontSize = 14.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }
        }

        FarmZone.VEGETABLE_FIELD -> {
            Surface(
                color = Color.White,
                shape = RoundedCornerShape(24.dp),
                shadowElevation = 2.dp,
                border = BorderStroke(1.dp, CardBorder),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(18.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(
                                modifier = Modifier
                                    .size(40.dp)
                                    .clip(RoundedCornerShape(12.dp))
                                    .background(Color(0xFFDCFCE7)),
                                contentAlignment = Alignment.Center
                            ) {
                                Text("🥦", fontSize = 18.sp)
                            }
                            Spacer(Modifier.width(12.dp))
                            Column {
                                Text("Vegetable Field", fontSize = 17.sp, fontWeight = FontWeight.Bold, color = TextDark)
                                Text("Crop: Lettuce + Carrots", fontSize = 12.sp, color = TextMuted)
                            }
                        }
                        Surface(
                            color = Color(0xFFDCFCE7),
                            shape = RoundedCornerShape(10.dp)
                        ) {
                            Text("💚 Excellent", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = Color(0xFF166534), modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp))
                        }
                    }
                    Spacer(Modifier.height(14.dp))
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        MetricSmallTile("Growth", "17%", Modifier.weight(1f))
                        MetricSmallTile("Soil pH", "6.8", Modifier.weight(1f))
                        MetricSmallTile("Irrigation", "6 AM", Modifier.weight(1f))
                    }
                }
            }
        }

        FarmZone.TOMATO_FIELD -> {
            Surface(
                color = Color.White,
                shape = RoundedCornerShape(24.dp),
                shadowElevation = 2.dp,
                border = BorderStroke(1.dp, CardBorder),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(18.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(
                                modifier = Modifier
                                    .size(40.dp)
                                    .clip(RoundedCornerShape(12.dp))
                                    .background(Color(0xFFFEE2E2)),
                                contentAlignment = Alignment.Center
                            ) {
                                Text("🍅", fontSize = 18.sp)
                            }
                            Spacer(Modifier.width(12.dp))
                            Column {
                                Text("Tomato Field", fontSize = 17.sp, fontWeight = FontWeight.Bold, color = TextDark)
                                Text("Crop: Roma Tomatoes", fontSize = 12.sp, color = TextMuted)
                            }
                        }
                        Surface(
                            color = Color(0xFFDCFCE7),
                            shape = RoundedCornerShape(10.dp)
                        ) {
                            Text("💚 Ready", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = Color(0xFF166534), modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp))
                        }
                    }
                    Spacer(Modifier.height(14.dp))
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        MetricSmallTile("Growth", "85%", Modifier.weight(1f))
                        MetricSmallTile("Moisture", "72%", Modifier.weight(1f))
                        MetricSmallTile("Yield", "3.4 T", Modifier.weight(1f))
                    }
                }
            }
        }

        FarmZone.FARM_HOUSE -> {
            Surface(
                color = Color.White,
                shape = RoundedCornerShape(24.dp),
                shadowElevation = 2.dp,
                border = BorderStroke(1.dp, CardBorder),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(18.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .clip(RoundedCornerShape(12.dp))
                                .background(Color(0xFFFEE2E2)),
                            contentAlignment = Alignment.Center
                        ) {
                            Text("🏠", fontSize = 18.sp)
                        }
                        Spacer(Modifier.width(12.dp))
                        Column {
                            Text("Farm House", fontSize = 17.sp, fontWeight = FontWeight.Bold, color = TextDark)
                            Text("Headquarters", fontSize = 12.sp, color = TextMuted)
                        }
                    }
                    Spacer(Modifier.height(14.dp))
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        MetricSmallTile("Status", "Active", Modifier.weight(1f))
                        MetricSmallTile("Solar", "94%", Modifier.weight(1f))
                        MetricSmallTile("Pumps", "2 Active", Modifier.weight(1f))
                    }
                }
            }
        }

        FarmZone.STORAGE -> {
            Surface(
                color = Color.White,
                shape = RoundedCornerShape(24.dp),
                shadowElevation = 2.dp,
                border = BorderStroke(1.dp, CardBorder),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(18.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .clip(RoundedCornerShape(12.dp))
                                .background(Color(0xFFF1F5F9)),
                            contentAlignment = Alignment.Center
                        ) {
                            Text("🏭", fontSize = 18.sp)
                        }
                        Spacer(Modifier.width(12.dp))
                        Text("Storage & Silos", fontSize = 17.sp, fontWeight = FontWeight.Bold, color = TextDark)
                    }
                    Spacer(Modifier.height(14.dp))
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        MetricSmallTile("Grain", "14.2 T", Modifier.weight(1f))
                        MetricSmallTile("Fertilizer", "1.2 T", Modifier.weight(1f))
                        MetricSmallTile("Seeds", "450 kg", Modifier.weight(1f))
                    }
                }
            }
        }
    }
}

@Composable
private fun MetricSmallTile(label: String, value: String, modifier: Modifier = Modifier) {
    Surface(
        color = Color(0xFFF8FAFC),
        shape = RoundedCornerShape(14.dp),
        border = BorderStroke(1.dp, CardBorder),
        modifier = modifier
    ) {
        Column(modifier = Modifier.padding(horizontal = 12.dp, vertical = 10.dp)) {
            Text(label, fontSize = 11.sp, color = TextMuted)
            Spacer(Modifier.height(4.dp))
            Text(value, fontSize = 14.sp, fontWeight = FontWeight.Bold, color = TextDark)
        }
    }
}

@Composable
private fun ExploreBentoGrid(
    onCropsClick: () -> Unit,
    onLivestockClick: () -> Unit,
    onWateringClick: () -> Unit,
    onWeatherClick: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            ExploreCard(
                emoji = "🌱",
                iconBg = Color(0xFFDCFCE7),
                title = "My Crops",
                subtitle = "4 growing",
                onClick = onCropsClick,
                modifier = Modifier.weight(1f)
            )
            ExploreCard(
                emoji = "🐮",
                iconBg = Color(0xFFFFEDD5),
                title = "Livestock",
                subtitle = "48 animals",
                onClick = onLivestockClick,
                modifier = Modifier.weight(1f)
            )
        }
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            ExploreCard(
                emoji = "💧",
                iconBg = Color(0xFFE0F2FE),
                title = "Watering",
                subtitle = "Next 7:00 AM",
                onClick = onWateringClick,
                modifier = Modifier.weight(1f)
            )
            ExploreCard(
                emoji = "☀️",
                iconBg = Color(0xFFFEF3C7),
                title = "Weather",
                subtitle = "Sunny · 28°C",
                onClick = onWeatherClick,
                modifier = Modifier.weight(1f)
            )
        }
    }
}

@Composable
private fun ExploreCard(
    emoji: String,
    iconBg: Color,
    title: String,
    subtitle: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Surface(
        color = Color.White,
        shape = RoundedCornerShape(20.dp),
        shadowElevation = 2.dp,
        border = BorderStroke(1.dp, CardBorder),
        modifier = modifier.tactilePress(scaleDown = 0.95f, onClick = onClick)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .clip(CircleShape)
                    .background(iconBg),
                contentAlignment = Alignment.Center
            ) {
                Text(emoji, fontSize = 18.sp)
            }
            Spacer(Modifier.height(12.dp))
            Text(title, fontSize = 15.sp, fontWeight = FontWeight.Bold, color = TextDark)
            Spacer(Modifier.height(2.dp))
            Text(subtitle, fontSize = 12.sp, color = TextMuted)
        }
    }
}

// ==========================================
// Sub-Screen: Dedicated Livestock Telemetry
// ==========================================

@Composable
private fun LivestockView(
    onNavigateBack: () -> Unit
) {
    var selectedCategory by remember { mutableStateOf("Cows") }

    val cowsList = remember {
        listOf(
            CowItem("Bella", "Holstein Friesian", "COW-014", "3 years", 96),
            CowItem("Daisy", "Jersey", "COW-021", "4 years", 91),
            CowItem("Moose", "Angus", "COW-007", "2.5 years", 84),
            CowItem("Buttercup", "Guernsey", "COW-033", "5 years", 94),
            CowItem("Luna", "Ayrshire", "COW-018", "2 years", 89)
        )
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(bottom = 28.dp)
    ) {
        // 1. Top Bar: Back arrow, "Livestock", "Green Valley Farm"
        item {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .statusBarsPadding()
                    .padding(horizontal = 20.dp, vertical = 12.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Surface(
                    modifier = Modifier
                        .size(44.dp)
                        .tactilePress(scaleDown = 0.92f, onClick = onNavigateBack),
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
                Spacer(Modifier.width(16.dp))
                Column {
                    Text("Livestock", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = TextDark)
                    Text("Green Valley Farm", fontSize = 12.sp, color = TextMuted)
                }
            }
        }

        // 2. Total Herd Card with 3 Ring Gauges
        item {
            Surface(
                color = Color.White,
                shape = RoundedCornerShape(24.dp),
                shadowElevation = 2.dp,
                border = BorderStroke(1.dp, CardBorder),
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 6.dp)
            ) {
                Column(modifier = Modifier.padding(18.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "TOTAL HERD",
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold,
                            color = TextMuted,
                            letterSpacing = 1.sp
                        )
                        Surface(
                            color = Color(0xFFDCFCE7),
                            shape = RoundedCornerShape(12.dp)
                        ) {
                            Text(
                                text = "🛡️ All healthy",
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold,
                                color = Color(0xFF166534),
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                            )
                        }
                    }

                    Spacer(Modifier.height(8.dp))

                    Text(
                        text = "41 Animals",
                        fontSize = 28.sp,
                        fontWeight = FontWeight.Bold,
                        color = TextDark
                    )

                    Spacer(Modifier.height(18.dp))

                    // 3 Ring Gauges Side by Side
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceAround
                    ) {
                        RingGaugeItem(
                            percentage = 79,
                            label = "Health",
                            sublabel = "Excellent",
                            color = FarmGreen
                        )
                        RingGaugeItem(
                            percentage = 65,
                            label = "Feed",
                            sublabel = "12 days stock",
                            color = Color(0xFFF59E0B)
                        )
                        RingGaugeItem(
                            percentage = 68,
                            label = "Production",
                            sublabel = "On target",
                            color = Color(0xFF0284C7)
                        )
                    }
                }
            }
        }

        // 3. Today's Feeding Timeline Card
        item {
            Surface(
                color = Color.White,
                shape = RoundedCornerShape(20.dp),
                shadowElevation = 2.dp,
                border = BorderStroke(1.dp, CardBorder),
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 6.dp)
            ) {
                Column(modifier = Modifier.padding(18.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(
                                modifier = Modifier
                                    .size(32.dp)
                                    .clip(RoundedCornerShape(8.dp))
                                    .background(Color(0xFFFEF3C7)),
                                contentAlignment = Alignment.Center
                            ) {
                                Text("🌾", fontSize = 14.sp)
                            }
                            Spacer(Modifier.width(10.dp))
                            Text("Today's feeding", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = TextDark)
                        }
                        Surface(
                            color = Color(0xFFF1F5F9),
                            shape = RoundedCornerShape(8.dp)
                        ) {
                            Text("0 of 3 done", fontSize = 11.sp, color = TextMuted, modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp))
                        }
                    }

                    Spacer(Modifier.height(16.dp))

                    // Timeline 3 Nodes
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.Top
                    ) {
                        FeedingTimelineNode("06:00", "Hay & silage", "Upcoming", Modifier.weight(1f))
                        FeedingTimelineNode("12:00", "Grain mix", "Upcoming", Modifier.weight(1f))
                        FeedingTimelineNode("18:00", "Evening feed", "Upcoming", Modifier.weight(1f))
                    }
                }
            }
        }

        // 4. Categories Section
        item {
            Column(modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)) {
                Text("Categories", fontSize = 17.sp, fontWeight = FontWeight.Bold, color = TextDark)
                Text("Tap a group to see its animals", fontSize = 12.sp, color = TextMuted)
            }
        }

        item {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                CategoryTile("🐮", "15", "Cows", selectedCategory == "Cows", Modifier.weight(1f)) { selectedCategory = "Cows" }
                CategoryTile("🐔", "17", "Chickens", selectedCategory == "Chickens", Modifier.weight(1f)) { selectedCategory = "Chickens" }
                CategoryTile("🐑", "5", "Sheep", selectedCategory == "Sheep", Modifier.weight(1f)) { selectedCategory = "Sheep" }
                CategoryTile("🐐", "3", "Goats", selectedCategory == "Goats", Modifier.weight(1f)) { selectedCategory = "Goats" }
            }
        }

        // 5. Animal Roster List ("Your cows")
        item {
            Column(modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp)) {
                Text("Your cows", fontSize = 17.sp, fontWeight = FontWeight.Bold, color = TextDark)
                Text("18 in the herd · tap one for details", fontSize = 12.sp, color = TextMuted)
            }
        }

        items(cowsList) { cow ->
            Surface(
                color = Color.White,
                shape = RoundedCornerShape(18.dp),
                shadowElevation = 1.dp,
                border = BorderStroke(1.dp, CardBorder),
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 4.dp)
                    .tactilePress(scaleDown = 0.97f) {}
            ) {
                Row(
                    modifier = Modifier.padding(14.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .size(52.dp)
                            .clip(RoundedCornerShape(14.dp))
                            .background(Color(0xFFF1F5F9)),
                        contentAlignment = Alignment.Center
                    ) {
                        Text("🐮", fontSize = 26.sp)
                    }
                    Spacer(Modifier.width(14.dp))
                    Column(modifier = Modifier.weight(1f)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(cow.name, fontSize = 16.sp, fontWeight = FontWeight.Bold, color = TextDark)
                            Spacer(Modifier.width(8.dp))
                            Surface(
                                color = if (cow.healthPercent >= 90) Color(0xFFDCFCE7) else Color(0xFFFEF3C7),
                                shape = RoundedCornerShape(8.dp)
                            ) {
                                Text(
                                    text = if (cow.healthPercent >= 90) "💚 ${cow.healthPercent}%" else "🧡 ${cow.healthPercent}%",
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = if (cow.healthPercent >= 90) Color(0xFF166534) else Color(0xFF92400E),
                                    modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                                )
                            }
                        }
                        Spacer(Modifier.height(2.dp))
                        Text(cow.breed, fontSize = 12.sp, color = TextMuted)
                        Spacer(Modifier.height(4.dp))
                        Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                            Surface(color = Color(0xFFF1F5F9), shape = RoundedCornerShape(6.dp)) {
                                Text(cow.tag, fontSize = 10.sp, color = TextMuted, modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp))
                            }
                            Surface(color = Color(0xFFFFEDD5), shape = RoundedCornerShape(6.dp)) {
                                Text(cow.age, fontSize = 10.sp, color = Color(0xFF9A3412), modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp))
                            }
                        }
                    }
                    Icon(
                        imageVector = Icons.AutoMirrored.Filled.KeyboardArrowRight,
                        contentDescription = null,
                        tint = TextMuted,
                        modifier = Modifier.size(20.dp)
                    )
                }
            }
        }
    }
}

@Composable
private fun RingGaugeItem(
    percentage: Int,
    label: String,
    sublabel: String,
    color: Color
) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Box(
            modifier = Modifier.size(72.dp),
            contentAlignment = Alignment.Center
        ) {
            Canvas(modifier = Modifier.fillMaxSize()) {
                val strokeWidth = 6.dp.toPx()
                // Track
                drawCircle(
                    color = color.copy(alpha = 0.15f),
                    style = Stroke(strokeWidth)
                )
                // Progress
                drawArc(
                    color = color,
                    startAngle = -90f,
                    sweepAngle = (percentage / 100f) * 360f,
                    useCenter = false,
                    style = Stroke(strokeWidth, cap = StrokeCap.Round)
                )
            }
            Text(
                text = "$percentage%",
                fontSize = 14.sp,
                fontWeight = FontWeight.Bold,
                color = TextDark
            )
        }
        Spacer(Modifier.height(6.dp))
        Text(label, fontSize = 13.sp, fontWeight = FontWeight.Bold, color = TextDark)
        Text(sublabel, fontSize = 10.sp, color = TextMuted)
    }
}

@Composable
private fun FeedingTimelineNode(
    time: String,
    title: String,
    status: String,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Box(
            modifier = Modifier
                .size(20.dp)
                .clip(CircleShape)
                .border(2.dp, Color(0xFFF59E0B), CircleShape)
                .background(Color.White)
        )
        Spacer(Modifier.height(6.dp))
        Text(time, fontSize = 12.sp, fontWeight = FontWeight.Bold, color = TextDark)
        Text(title, fontSize = 11.sp, color = TextMuted)
        Text(status, fontSize = 10.sp, color = Color(0xFFD97706), fontWeight = FontWeight.Medium)
    }
}

@Composable
private fun CategoryTile(
    emoji: String,
    count: String,
    label: String,
    isSelected: Boolean,
    modifier: Modifier = Modifier,
    onClick: () -> Unit
) {
    Surface(
        color = Color.White,
        shape = RoundedCornerShape(16.dp),
        shadowElevation = 1.dp,
        border = BorderStroke(
            if (isSelected) 2.dp else 1.dp,
            if (isSelected) FarmGreen else CardBorder
        ),
        modifier = modifier.tactilePress(scaleDown = 0.95f, onClick = onClick)
    ) {
        Column(
            modifier = Modifier.padding(vertical = 12.dp, horizontal = 4.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(emoji, fontSize = 24.sp)
            Spacer(Modifier.height(6.dp))
            Text(count, fontSize = 15.sp, fontWeight = FontWeight.Bold, color = TextDark)
            Text(label, fontSize = 11.sp, color = TextMuted)
        }
    }
}
