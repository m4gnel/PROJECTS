package com.agrisage.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import androidx.navigation.compose.rememberNavController
import com.agrisage.app.navigation.Advisor
import com.agrisage.app.ui.theme.*

/**
 * Screen 7: Alerts & Notifications
 * Route: Alerts
 *
 * Per spec:
 * - Filter chips: All | Pest | Weather | Crop | Market | Soil
 * - Alert list categorised by severity: CRITICAL | WARNING | INFO | SUCCESS
 * - Each card: icon + badge + title + description + source + time + "Ask AI" action
 * - Swipe to dismiss
 * - Empty state: "✅ No active alerts"
 */

enum class AlertSeverity { CRITICAL, WARNING, INFO, SUCCESS }
enum class AlertFilter { ALL, PEST, WEATHER, CROP, MARKET, SOIL }

data class AlertItem(
    val id: String,
    val severity: AlertSeverity,
    val filter: AlertFilter,
    val icon: String,
    val title: String,
    val description: String,
    val source: String,
    val timeAgo: String,
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AlertsScreen(navController: NavController) {
    var selectedFilter by remember { mutableStateOf(AlertFilter.ALL) }

    // Demo data — replace with AlertViewModel StateFlow
    val allAlerts = listOf(
        AlertItem(
            id = "1",
            severity = AlertSeverity.CRITICAL,
            filter = AlertFilter.PEST,
            icon = "🐛",
            title = "Rugose Spiraling Whitefly Outbreak",
            description = "High incidence reported on coconut in Ernakulam district. Check your palms for sooty mold and waxy deposits.",
            source = "NBAIR RSS",
            timeAgo = "2 hours ago"
        ),
        AlertItem(
            id = "2",
            severity = AlertSeverity.WARNING,
            filter = AlertFilter.WEATHER,
            icon = "⛈️",
            title = "Heavy Rain Alert — Kerala",
            description = "IMD issues heavy rainfall alert for Ernakulam, Thrissur. Risk of field waterlogging. Ensure drainage is clear.",
            source = "IMD Alert",
            timeAgo = "4 hours ago"
        ),
        AlertItem(
            id = "3",
            severity = AlertSeverity.INFO,
            filter = AlertFilter.CROP,
            icon = "🌾",
            title = "Crop Stage Update — Rice",
            description = "Your paddy is entering the tillering stage (estimated Day 35–42). Critical irrigation window opens.",
            source = "Agri-SAGE AI",
            timeAgo = "Today"
        ),
        AlertItem(
            id = "4",
            severity = AlertSeverity.SUCCESS,
            filter = AlertFilter.SOIL,
            icon = "🧪",
            title = "Soil Moisture Optimal",
            description = "Soil moisture levels are in the ideal range for your crop. No irrigation needed today.",
            source = "Weather + Soil Model",
            timeAgo = "Today"
        ),
    )

    val filters = AlertFilter.values()
    val filterLabels = mapOf(
        AlertFilter.ALL to "All",
        AlertFilter.PEST to "Pest 🐛",
        AlertFilter.WEATHER to "Weather 🌧️",
        AlertFilter.CROP to "Crop 🌾",
        AlertFilter.MARKET to "Market 💰",
        AlertFilter.SOIL to "Soil 🧪",
    )

    val filteredAlerts = if (selectedFilter == AlertFilter.ALL) {
        allAlerts
    } else {
        allAlerts.filter { it.filter == selectedFilter }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("🔔 Alerts", color = Color.White) },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color(0xFF1B4332))
            )
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .background(Color(0xFFF8FCF8))
        ) {
            // Filter chips
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                filters.forEach { filter ->
                    item {
                        FilterChip(
                            selected = selectedFilter == filter,
                            onClick = { selectedFilter = filter },
                            label = { Text(filterLabels[filter] ?: filter.name) },
                            colors = FilterChipDefaults.filterChipColors(
                                selectedContainerColor = Color(0xFF1B4332),
                                selectedLabelColor = Color.White
                            )
                        )
                    }
                }
            }

            if (filteredAlerts.isEmpty()) {
                // Empty state
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = androidx.compose.ui.Alignment.Center
                ) {
                    Column(horizontalAlignment = androidx.compose.ui.Alignment.CenterHorizontally) {
                        Text("✅", fontSize = 48.sp)
                        Spacer(Modifier.height(8.dp))
                        Text(
                            "No active alerts",
                            style = MaterialTheme.typography.headlineMedium,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFF1B4332)
                        )
                        Text(
                            "Your farm is doing well.",
                            style = MaterialTheme.typography.bodyMedium,
                            color = Color(0xFF6B7280)
                        )
                    }
                }
            } else {
                LazyColumn(
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                    verticalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    filteredAlerts.forEach { alert ->
                        item(key = alert.id) {
                            AlertCard(
                                alert = alert,
                                onAskAI = { navController.navigate(Advisor) }
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun AlertCard(
    alert: AlertItem,
    onAskAI: () -> Unit,
) {
    val (borderColor, bgColor, badgeColor, badgeText) = when (alert.severity) {
        AlertSeverity.CRITICAL -> listOf(
            Color(0xFFDC2626), Color(0xFFFEE2E2),
            Color(0xFFDC2626), "CRITICAL"
        )
        AlertSeverity.WARNING -> listOf(
            Color(0xFFF59E0B), Color(0xFFFEF3C7),
            Color(0xFFF59E0B), "WARNING"
        )
        AlertSeverity.INFO -> listOf(
            Color(0xFF2563EB), Color(0xFFDBEAFE),
            Color(0xFF2563EB), "INFO"
        )
        AlertSeverity.SUCCESS -> listOf(
            Color(0xFF16A34A), Color(0xFFDCFCE7),
            Color(0xFF16A34A), "SUCCESS"
        )
    }

    Surface(
        shape = RoundedCornerShape(12.dp),
        color = bgColor as Color,
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Row {
                    Text(alert.icon, fontSize = 20.sp)
                    Spacer(Modifier.width(8.dp))
                    Box(
                        modifier = Modifier
                            .background(badgeColor as Color, RoundedCornerShape(6.dp))
                            .padding(horizontal = 8.dp, vertical = 2.dp)
                    ) {
                        Text(
                            badgeText as String,
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color.White
                        )
                    }
                }
                Text(alert.timeAgo, fontSize = 11.sp, color = Color(0xFF6B7280))
            }

            Spacer(Modifier.height(8.dp))
            Text(
                alert.title,
                fontWeight = FontWeight.Bold,
                color = borderColor as Color,
                fontSize = 15.sp
            )
            Spacer(Modifier.height(4.dp))
            Text(
                alert.description,
                style = MaterialTheme.typography.bodyMedium,
                color = Color(0xFF374151)
            )
            Spacer(Modifier.height(4.dp))
            Text(
                "Source: ${alert.source}",
                fontSize = 11.sp,
                color = Color(0xFF6B7280)
            )

            if (alert.severity in listOf(AlertSeverity.CRITICAL, AlertSeverity.WARNING)) {
                Spacer(Modifier.height(10.dp))
                TextButton(
                    onClick = onAskAI,
                    contentPadding = PaddingValues(horizontal = 8.dp, vertical = 4.dp)
                ) {
                    Text(
                        "Ask AI what to do →",
                        color = borderColor,
                        fontWeight = FontWeight.SemiBold,
                        fontSize = 13.sp
                    )
                }
            }
        }
    }
}

@Preview(showBackground = true, widthDp = 360, heightDp = 800)
@Composable
fun AlertsScreenPreview() {
    AlertsScreen(navController = rememberNavController())
}
