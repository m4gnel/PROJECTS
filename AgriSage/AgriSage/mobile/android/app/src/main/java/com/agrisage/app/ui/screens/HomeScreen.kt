package com.agrisage.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.agrisage.app.ui.components.*
import com.agrisage.app.ui.theme.*

/**
 * Screen: Home Dashboard (Replicated from Reference Reel 2 - DailyFlutterUI Farm App)
 * Route: Home
 *
 * Features:
 * - Top Header: Rounded avatar pill, "Good afternoon, Guest", Green Valley Farm selector, circular bell with unread dot
 * - Hero Farm Scene: Animated Canvas vector farm with rolling pastures, red barn, cows & spinning wind turbines
 * - Overlaid Hero KPI Cards: Farm Health circular gauge (92% Healthy) + Weather snapshot (28°C Sunny)
 * - 2x2 Bento Quick Stats: 12 Crops (Mint), 48 Animals (Peach), 72% Soil Moisture (Ice Blue), 1,280 kg Harvest (Amber)
 * - Smart Agri-Tools Bento: AI Advisor, Disease Diagnosis Camera, APMC Market Prices
 * - Urgent Alerts & Today's Checklist
 * - AgriBottomNav integration
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    viewModel: HomeViewModel = androidx.hilt.navigation.compose.hiltViewModel(),
    onNavigateToAdvisor: () -> Unit = {},
    onNavigateToCamera: () -> Unit = {},
    onNavigateToWeather: () -> Unit = {},
    onNavigateToFields: () -> Unit = {},
    onNavigateToAlerts: () -> Unit = {},
    onNavigateToProfile: () -> Unit = {},
    onNavigateToMarket: () -> Unit = {}
) {
    val connectivity by viewModel.connectivityStatus.collectAsState()
    var task1Done by remember { mutableStateOf(false) }
    var task2Done by remember { mutableStateOf(true) }

    Scaffold(
        topBar = {
            // Replicated Top Header: Clean white/surface background with avatar, farm dropdown, and circular notification bell
            Surface(
                color = Color.White,
                shadowElevation = 1.dp
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .statusBarsPadding()
                        .padding(horizontal = 20.dp, vertical = 12.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    // Profile & Farm Selector
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier
                            .defaultMinSize(minHeight = 48.dp)
                            .semantics(mergeDescendants = true) {
                                contentDescription = "Open profile and farm selector"
                                role = Role.Button
                            }
                            .tactilePress(
                                scaleDown = 0.97f,
                                onClickLabel = "Open profile",
                                onClick = onNavigateToProfile
                            )
                    ) {
                        // Avatar inside subtle pill container
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
                                modifier = Modifier.size(24.dp)
                            )
                        }

                        Spacer(modifier = Modifier.width(12.dp))

                        Column {
                            Text(
                                text = "Good afternoon, Guest",
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Medium,
                                color = Color(0xFF64748B)
                            )
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text(
                                    text = "Green Valley Farm",
                                    fontSize = 17.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = Color(0xFF0F172A)
                                )
                                Spacer(modifier = Modifier.width(4.dp))
                                Icon(
                                    imageVector = Icons.Default.KeyboardArrowDown,
                                    contentDescription = null,
                                    tint = Color(0xFF64748B),
                                    modifier = Modifier.size(18.dp)
                                )
                            }
                        }
                    }

                    // Notification Bell (Circular white button with unread red badge)
                    Box(
                        modifier = Modifier
                            .size(48.dp)
                            .clip(CircleShape)
                            .background(Color(0xFFF8FAFC))
                            .border(1.dp, Color(0xFFE2E8F0), CircleShape)
                            .semantics {
                                contentDescription = "Open alerts"
                                role = Role.Button
                            }
                            .tactilePress(
                                scaleDown = 0.95f,
                                onClickLabel = "Open alerts",
                                onClick = onNavigateToAlerts
                            ),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = Icons.Default.Notifications,
                            contentDescription = null,
                            tint = Color(0xFF334155),
                            modifier = Modifier.size(22.dp)
                        )
                        // Red Unread Dot
                        Box(
                            modifier = Modifier
                                .size(8.dp)
                                .align(Alignment.TopEnd)
                                .offset(x = (-10).dp, y = 10.dp)
                                .clip(CircleShape)
                                .background(Color(0xFFEF4444))
                        )
                    }
                }
            }
        },
        bottomBar = {
            AgriBottomNav(
                currentRoute = "home",
                onNavigate = { route ->
                    when (route) {
                        "advisor" -> onNavigateToAdvisor()
                        "fields" -> onNavigateToFields()
                        "weather" -> onNavigateToWeather()
                        "profile" -> onNavigateToProfile()
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
            contentPadding = PaddingValues(bottom = 28.dp),
            verticalArrangement = Arrangement.spacedBy(18.dp)
        ) {
            // Offline Banner if disconnected
            if (connectivity != ConnectivityStatus.ONLINE) {
                item {
                    Surface(
                        color = if (connectivity == ConnectivityStatus.OFFLINE) ColorOfflineBanner else ColorWarningBg,
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 16.dp, vertical = 6.dp)
                    ) {
                        Row(
                            modifier = Modifier.padding(12.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(
                                imageVector = if (connectivity == ConnectivityStatus.OFFLINE) Icons.Default.CloudOff else Icons.Default.Warning,
                                contentDescription = if (connectivity == ConnectivityStatus.OFFLINE) "Offline" else "Limited connection",
                                tint = if (connectivity == ConnectivityStatus.OFFLINE) ColorOfflineText else ColorWarningText
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(
                                text = if (connectivity == ConnectivityStatus.OFFLINE) "Offline — Showing cached data" else "Limited connection",
                                style = MaterialTheme.typography.bodyMedium,
                                color = if (connectivity == ConnectivityStatus.OFFLINE) ColorOfflineText else ColorWarningText
                            )
                        }
                    }
                }
            }

            // ── HERO SECTION: Animated Farm Illustration with Overlaid KPI Cards ──
            item {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp)
                ) {
                    // Farm Illustration Canvas Container
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(210.dp)
                            .shadow(6.dp, RoundedCornerShape(24.dp), ambientColor = Color(0x1A000000))
                            .clip(RoundedCornerShape(24.dp))
                    ) {
                        FarmIllustration(
                            modifier = Modifier.fillMaxSize(),
                            weatherMode = WeatherVisualMode.SUNNY,
                            isAnimated = true
                        )
                    }

                    Spacer(modifier = Modifier.height(14.dp))

                    // Floating Overlaid Hero KPI Cards
                    HeroKpiCardsRow(
                        healthScore = 92,
                        healthStatus = "Healthy",
                        tempCelsius = 28,
                        weatherCondition = "Sunny",
                        rainChance = 15,
                        humidity = 68,
                        onHealthClick = onNavigateToFields,
                        onWeatherClick = onNavigateToWeather
                    )
                }
            }

            // ── SECTION: 2x2 Bento Quick Stats (Reel 2 Replication) ──
            item {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "Quick Stats",
                            fontSize = 18.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFF0F172A)
                        )
                        Text(
                            text = "Overview",
                            fontSize = 13.sp,
                            fontWeight = FontWeight.SemiBold,
                            color = Color(0xFF16A34A),
                            modifier = Modifier
                                .defaultMinSize(minHeight = 48.dp)
                                .semantics {
                                    contentDescription = "Open fields overview"
                                    role = Role.Button
                                }
                                .tactilePress(
                                    scaleDown = 0.97f,
                                    onClickLabel = "Open fields overview",
                                    onClick = onNavigateToFields
                                )
                        )
                    }

                    Spacer(modifier = Modifier.height(12.dp))

                    // 2x2 Bento Grid
                    // Row 1: Crops & Animals
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        QuickStatCard(
                            iconVector = Icons.Default.Eco,
                            value = "12",
                            label = "Crops",
                            badgeBgColor = Color(0xFFDCFCE7),
                            badgeTextColor = Color(0xFF166534),
                            modifier = Modifier.weight(1f),
                            onClick = onNavigateToFields
                        )

                        QuickStatCard(
                            iconVector = Icons.Default.Pets,
                            value = "48",
                            label = "Animals",
                            badgeBgColor = Color(0xFFFFEDD5),
                            badgeTextColor = Color(0xFF9A3412),
                            modifier = Modifier.weight(1f),
                            onClick = onNavigateToFields
                        )
                    }

                    Spacer(modifier = Modifier.height(12.dp))

                    // Row 2: Soil Moisture & Harvest
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        QuickStatCard(
                            iconVector = Icons.Default.WaterDrop,
                            value = "72%",
                            label = "Soil Moisture",
                            badgeBgColor = Color(0xFFE0F2FE),
                            badgeTextColor = Color(0xFF0369A1),
                            modifier = Modifier.weight(1f),
                            onClick = onNavigateToFields
                        )

                        QuickStatCard(
                            iconVector = Icons.Default.ShoppingBasket,
                            value = "1,280 kg",
                            label = "Harvest Yield",
                            badgeBgColor = Color(0xFFFEF3C7),
                            badgeTextColor = Color(0xFF92400E),
                            modifier = Modifier.weight(1f),
                            onClick = onNavigateToMarket
                        )
                    }
                }
            }

            // ── SECTION: Smart Agricultural Actions ──
            item {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp)
                ) {
                    Text(
                        text = "Smart Farming Tools",
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color(0xFF0F172A)
                    )

                    Spacer(modifier = Modifier.height(12.dp))

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        // AI Advisor Card
                        Card(
                            colors = CardDefaults.cardColors(containerColor = Color(0xFF1B4332)),
                            shape = RoundedCornerShape(20.dp),
                            modifier = Modifier
                                .weight(1f)
                                .height(118.dp)
                                .semantics(mergeDescendants = true) {
                                    contentDescription = "Ask Advisor. AI crop assistance"
                                    role = Role.Button
                                }
                                .tactilePress(
                                    scaleDown = 0.95f,
                                    onClickLabel = "Ask Advisor",
                                    onClick = onNavigateToAdvisor
                                ),
                            elevation = CardDefaults.cardElevation(2.dp)
                        ) {
                            Column(
                                modifier = Modifier
                                    .padding(14.dp)
                                    .fillMaxHeight(),
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
                                        imageVector = Icons.Default.SmartToy,
                                        contentDescription = null,
                                        tint = Color.White,
                                        modifier = Modifier.size(22.dp)
                                    )
                                }
                                Column {
                                    Text(
                                        "Ask Advisor",
                                        fontWeight = FontWeight.Bold,
                                        color = Color.White,
                                        fontSize = 15.sp
                                    )
                                    Text(
                                        "AI crop assistance",
                                        color = Color(0xFFD1FAE5),
                                        fontSize = 11.sp
                                    )
                                }
                            }
                        }

                        // Diagnose Camera Card
                        Card(
                            colors = CardDefaults.cardColors(containerColor = Color(0xFF2D6A4F)),
                            shape = RoundedCornerShape(20.dp),
                            modifier = Modifier
                                .weight(1f)
                                .height(118.dp)
                                .semantics(mergeDescendants = true) {
                                    contentDescription = "Diagnose. Scan plant disease"
                                    role = Role.Button
                                }
                                .tactilePress(
                                    scaleDown = 0.95f,
                                    onClickLabel = "Diagnose plant disease",
                                    onClick = onNavigateToCamera
                                ),
                            elevation = CardDefaults.cardElevation(2.dp)
                        ) {
                            Column(
                                modifier = Modifier
                                    .padding(14.dp)
                                    .fillMaxHeight(),
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
                                        imageVector = Icons.Default.CameraAlt,
                                        contentDescription = null,
                                        tint = Color.White,
                                        modifier = Modifier.size(22.dp)
                                    )
                                }
                                Column {
                                    Text(
                                        "Diagnose",
                                        fontWeight = FontWeight.Bold,
                                        color = Color.White,
                                        fontSize = 15.sp
                                    )
                                    Text(
                                        "Scan plant disease",
                                        color = Color(0xFFD1FAE5),
                                        fontSize = 11.sp
                                    )
                                }
                            }
                        }
                    }
                }
            }

            // ── SECTION: Market Prices Highlight ──
            item {
                Card(
                    colors = CardDefaults.cardColors(containerColor = Color.White),
                    shape = RoundedCornerShape(20.dp),
                    elevation = CardDefaults.cardElevation(1.dp),
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp)
                        .border(1.dp, Color(0xFFF1F5F9), RoundedCornerShape(20.dp))
                        .semantics(mergeDescendants = true) {
                            contentDescription = "Open APMC market live prices"
                            role = Role.Button
                        }
                        .tactilePress(
                            scaleDown = 0.97f,
                            onClickLabel = "Open market prices",
                            onClick = onNavigateToMarket
                        )
                ) {
                    Row(
                        modifier = Modifier.padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.weight(1f)
                        ) {
                            Box(
                                modifier = Modifier
                                    .size(42.dp)
                                    .clip(RoundedCornerShape(12.dp))
                                    .background(Color(0xFFDCFCE7)),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(
                                    imageVector = Icons.Default.TrendingUp,
                                    contentDescription = null,
                                    tint = Color(0xFF166534),
                                    modifier = Modifier.size(24.dp)
                                )
                            }
                            Spacer(Modifier.width(14.dp))
                            Column {
                                Text(
                                    "APMC Market Live Prices",
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 14.sp,
                                    color = Color(0xFF0F172A)
                                )
                                Text(
                                    "Paddy ₹4,350/qtl (SELL) · Wheat ₹2,480 (HOLD)",
                                    fontSize = 12.sp,
                                    color = Color(0xFF16A34A),
                                    fontWeight = FontWeight.Medium
                                )
                            }
                        }
                        Icon(
                            imageVector = Icons.Default.ChevronRight,
                            contentDescription = null,
                            tint = Color(0xFF94A3B8)
                        )
                    }
                }
            }

            // ── SECTION: Today's Tasks & Urgent Alert ──
            item {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp)
                ) {
                    Text(
                        text = "Today's Tasks",
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color(0xFF0F172A)
                    )

                    Spacer(modifier = Modifier.height(12.dp))

                    Card(
                        colors = CardDefaults.cardColors(containerColor = Color.White),
                        elevation = CardDefaults.cardElevation(1.dp),
                        shape = RoundedCornerShape(20.dp),
                        modifier = Modifier
                            .fillMaxWidth()
                            .border(1.dp, Color(0xFFF1F5F9), RoundedCornerShape(20.dp))
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            // Task 1
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.SpaceBetween
                            ) {
                                Row(
                                    verticalAlignment = Alignment.CenterVertically,
                                    modifier = Modifier.weight(1f)
                                ) {
                                    Checkbox(
                                        checked = task1Done,
                                        onCheckedChange = { task1Done = it },
                                        colors = CheckboxDefaults.colors(checkedColor = Color(0xFF16A34A))
                                    )
                                    Spacer(modifier = Modifier.width(6.dp))
                                    Column {
                                        Text(
                                            "Apply organic fertiliser — Plot 1",
                                            fontWeight = FontWeight.SemiBold,
                                            color = Color(0xFF0F172A),
                                            fontSize = 14.sp
                                        )
                                        Text(
                                            "Ideal window: Before 9:30 AM",
                                            fontSize = 12.sp,
                                            color = Color(0xFF64748B)
                                        )
                                    }
                                }
                                Surface(
                                    color = Color(0xFFDCFCE7),
                                    shape = RoundedCornerShape(8.dp)
                                ) {
                                    Text(
                                        text = "6–9 AM",
                                        color = Color(0xFF166534),
                                        fontWeight = FontWeight.SemiBold,
                                        fontSize = 11.sp,
                                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                    )
                                }
                            }

                            HorizontalDivider(
                                modifier = Modifier.padding(vertical = 10.dp),
                                color = Color(0xFFF1F5F9)
                            )

                            // Task 2
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Checkbox(
                                    checked = task2Done,
                                    onCheckedChange = { task2Done = it },
                                    colors = CheckboxDefaults.colors(checkedColor = Color(0xFF16A34A))
                                )
                                Spacer(modifier = Modifier.width(6.dp))
                                Column {
                                    Text(
                                        "Soil moisture calibration",
                                        fontWeight = FontWeight.SemiBold,
                                        color = Color(0xFF0F172A),
                                        fontSize = 14.sp
                                    )
                                    Text(
                                        "Optimal 72% — Completed ✓",
                                        fontSize = 12.sp,
                                        color = Color(0xFF16A34A)
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
