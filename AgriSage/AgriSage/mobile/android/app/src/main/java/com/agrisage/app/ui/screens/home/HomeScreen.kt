package com.agrisage.app.ui.screens.home

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavHostController
import com.agrisage.app.navigation.Screen
import com.agrisage.app.ui.components.AlertCard
import com.agrisage.app.ui.components.LoadingOverlay
import com.agrisage.app.ui.components.QuickActionButton
import com.agrisage.app.ui.theme.WireAlert
import com.agrisage.app.ui.theme.WireAlertPale
import com.agrisage.app.ui.theme.WireBorder
import com.agrisage.app.ui.theme.WireLeaf
import com.agrisage.app.ui.theme.WireSageDeep
import com.agrisage.app.ui.theme.WireTextMuted
import com.agrisage.app.ui.theme.WireTextPrimary
import com.agrisage.app.ui.theme.WireWhite

@Composable
fun HomeScreen(
    navController: NavHostController,
    viewModel: HomeViewModel = hiltViewModel()
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()

    Box(modifier = Modifier.fillMaxSize().background(WireWhite)) {
        LazyColumn(
            modifier = Modifier.fillMaxSize()
        ) {
            // Header Top Bar in SageDeep
            item {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(WireSageDeep)
                        .padding(horizontal = 20.dp, vertical = 18.dp)
                ) {
                    Text(
                        text = "Good morning,",
                        fontSize = 12.sp,
                        color = Color.White.copy(alpha = 0.7f)
                    )
                    Text(
                        text = if (state.farmerName.isNotBlank()) "${state.farmerName}'s Farm 🌾" else "Rajan's Farm 🌾",
                        fontSize = 20.sp,
                        fontWeight = FontWeight.Black,
                        color = Color.White,
                        modifier = Modifier.padding(top = 2.dp)
                    )

                    // Weather chip inside header
                    Box(
                        modifier = Modifier
                            .padding(top = 10.dp)
                            .clip(RoundedCornerShape(8.dp))
                            .background(Color.White.copy(alpha = 0.15f))
                            .clickable { navController.navigate(Screen.Weather) }
                            .padding(horizontal = 12.dp, vertical = 6.dp)
                    ) {
                        val temp = state.weather?.tempCelsius?.let { "%.0f°C".format(it) } ?: "28°C"
                        val condition = state.weather?.condition ?: "82% humidity"
                        Text(
                            text = "🌤️ $temp · $condition · Kalady",
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Medium,
                            color = Color.White
                        )
                    }
                }
            }

            // Quick Actions Section
            item {
                Column(modifier = Modifier.padding(horizontal = 16.dp, vertical = 14.dp)) {
                    Text(
                        text = "QUICK ACTIONS",
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold,
                        color = WireTextMuted,
                        letterSpacing = 1.sp,
                        modifier = Modifier.padding(bottom = 10.dp)
                    )

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        QuickActionButton(
                            icon = "🤖",
                            label = "Ask Advisor",
                            subtitle = "AI farm guidance",
                            onClick = { navController.navigate(Screen.Advisor) },
                            modifier = Modifier.weight(1f)
                        )
                        QuickActionButton(
                            icon = "🌧️",
                            label = "Weather",
                            subtitle = "7-day forecast",
                            onClick = { navController.navigate(Screen.Weather) },
                            modifier = Modifier.weight(1f)
                        )
                    }

                    Spacer(modifier = Modifier.height(10.dp))

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        QuickActionButton(
                            icon = "📍",
                            label = "My Fields",
                            subtitle = "${state.todayTasks.size.coerceAtLeast(2)} active plots",
                            onClick = { navController.navigate(Screen.Fields) },
                            modifier = Modifier.weight(1f)
                        )
                        QuickActionButton(
                            icon = "⚠️",
                            label = "Alerts",
                            subtitle = "${state.activeAlerts.size.coerceAtLeast(2)} new today",
                            onClick = { navController.navigate(Screen.Alerts) },
                            modifier = Modifier.weight(1f)
                        )
                    }
                }
            }

            // Alert Strip Banner
            item {
                Column(modifier = Modifier.padding(horizontal = 16.dp)) {
                    Text(
                        text = "ALERTS",
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold,
                        color = WireTextMuted,
                        letterSpacing = 1.sp,
                        modifier = Modifier.padding(bottom = 8.dp)
                    )

                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { navController.navigate(Screen.Alerts) },
                        shape = RoundedCornerShape(12.dp),
                        colors = CardDefaults.cardColors(containerColor = WireAlertPale),
                        border = BorderStroke(1.5.dp, WireAlert)
                    ) {
                        Row(
                            modifier = Modifier.padding(12.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(text = "🐛", fontSize = 22.sp)
                            Spacer(modifier = Modifier.width(10.dp))
                            Text(
                                text = "Pest risk HIGH — paddy field 2. Check immediately",
                                fontSize = 12.sp,
                                fontWeight = FontWeight.SemiBold,
                                color = WireAlert
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(14.dp))
                }
            }

            // Active Alerts Horizontal Carousel (if alerts exist)
            if (state.activeAlerts.isNotEmpty()) {
                item {
                    Column(modifier = Modifier.padding(start = 16.dp, end = 16.dp, bottom = 14.dp)) {
                        LazyRow(
                            horizontalArrangement = Arrangement.spacedBy(12.dp),
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            items(state.activeAlerts) { alert ->
                                Box(modifier = Modifier.fillParentMaxWidth(0.9f)) {
                                    AlertCard(
                                        title = alert.title,
                                        message = alert.message,
                                        severity = alert.severity.name,
                                        onClick = { navController.navigate(Screen.Alerts) }
                                    )
                                }
                            }
                        }
                    }
                }
            }

            // Today's Tasks
            item {
                Column(modifier = Modifier.padding(horizontal = 16.dp)) {
                    Text(
                        text = "TODAY'S TASKS",
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold,
                        color = WireTextMuted,
                        letterSpacing = 1.sp,
                        modifier = Modifier.padding(bottom = 8.dp)
                    )

                    // Task 1
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(bottom = 8.dp),
                        shape = RoundedCornerShape(12.dp),
                        colors = CardDefaults.cardColors(containerColor = Color.White),
                        border = BorderStroke(1.5.dp, WireBorder),
                        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
                    ) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(12.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Box(
                                modifier = Modifier
                                    .size(20.dp)
                                    .clip(CircleShape)
                                    .background(Color.Transparent)
                                    .padding(2.dp),
                                contentAlignment = Alignment.Center
                            ) {
                                Card(
                                    shape = CircleShape,
                                    colors = CardDefaults.cardColors(containerColor = Color.White),
                                    border = BorderStroke(2.dp, WireLeaf),
                                    modifier = Modifier.size(16.dp)
                                ) {}
                            }
                            Spacer(modifier = Modifier.width(10.dp))
                            Column {
                                Text(
                                    text = "Apply fertiliser — Field 1",
                                    fontSize = 13.sp,
                                    fontWeight = FontWeight.SemiBold,
                                    color = WireTextPrimary
                                )
                                Text(
                                    text = "Before 9 AM",
                                    fontSize = 11.sp,
                                    color = WireTextMuted
                                )
                            }
                        }
                    }

                    // Task 2 (Completed)
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(bottom = 16.dp),
                        shape = RoundedCornerShape(12.dp),
                        colors = CardDefaults.cardColors(containerColor = Color.White),
                        border = BorderStroke(1.5.dp, WireBorder),
                        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
                    ) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(12.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Box(
                                modifier = Modifier
                                    .size(18.dp)
                                    .clip(CircleShape)
                                    .background(WireLeaf),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(
                                    imageVector = Icons.Default.Check,
                                    contentDescription = "Done",
                                    tint = Color.White,
                                    modifier = Modifier.size(12.dp)
                                )
                            }
                            Spacer(modifier = Modifier.width(10.dp))
                            Column {
                                Text(
                                    text = "Soil moisture check",
                                    fontSize = 13.sp,
                                    fontWeight = FontWeight.SemiBold,
                                    color = WireTextPrimary.copy(alpha = 0.5f),
                                    textDecoration = TextDecoration.LineThrough
                                )
                                Text(
                                    text = "Done ✓",
                                    fontSize = 11.sp,
                                    color = WireLeaf,
                                    fontWeight = FontWeight.Bold
                                )
                            }
                        }
                    }
                }
            }
        }

        LoadingOverlay(isLoading = state.isLoading)
    }
}
