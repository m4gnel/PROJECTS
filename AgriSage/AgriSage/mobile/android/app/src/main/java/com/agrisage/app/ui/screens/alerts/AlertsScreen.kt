package com.agrisage.app.ui.screens.alerts

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
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.CloudOff
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material.icons.filled.WaterDrop
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavHostController
import com.agrisage.app.ui.components.LoadingOverlay
import com.agrisage.app.ui.screens.home.AlertSeverity
import com.agrisage.app.ui.theme.WireAlert
import com.agrisage.app.ui.theme.WireAlertPale
import com.agrisage.app.ui.theme.WireGold
import com.agrisage.app.ui.theme.WireGoldPale
import com.agrisage.app.ui.theme.WireLeaf
import com.agrisage.app.ui.theme.WireLeafPale
import com.agrisage.app.ui.theme.WireSageDeep
import com.agrisage.app.ui.theme.WireSky
import com.agrisage.app.ui.theme.WireSkyPale
import com.agrisage.app.ui.theme.WireSurface2
import com.agrisage.app.ui.theme.WireTextMuted
import com.agrisage.app.ui.theme.WireTextPrimary
import com.agrisage.app.ui.theme.WireTextSecondary
import com.agrisage.app.ui.theme.WireWhite

@Composable
fun AlertsScreen(
    navController: NavHostController,
    viewModel: AlertsViewModel = hiltViewModel()
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
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(
                                    imageVector = Icons.Default.Notifications,
                                    contentDescription = null,
                                    tint = Color.White,
                                    modifier = Modifier.size(22.dp)
                                )
                                Spacer(modifier = Modifier.width(8.dp))
                                Text(
                                    text = "Alerts",
                                    fontSize = 20.sp,
                                    fontWeight = FontWeight.ExtraBold,
                                    color = Color.White
                                )
                            }
                            Text(
                                text = "${state.unreadCount} unread farm advisories & warnings",
                                fontSize = 12.sp,
                                color = Color.White.copy(alpha = 0.75f),
                                modifier = Modifier.padding(top = 2.dp)
                            )
                        }

                        if (state.unreadCount > 0) {
                            TextButton(onClick = { viewModel.markAllAsRead() }) {
                                Text("Mark All Read", color = WireLeafPale, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }

            // Filter Chips Row
            item {
                LazyRow(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 12.dp)
                ) {
                    item {
                        WireFilterChip(
                            label = "All",
                            isSelected = state.selectedFilter == null,
                            onClick = { viewModel.filterBySeverity(null) }
                        )
                    }
                    items(AlertSeverity.entries.toTypedArray()) { sev ->
                        WireFilterChip(
                            label = sev.name,
                            isSelected = state.selectedFilter == sev,
                            onClick = { viewModel.filterBySeverity(sev) }
                        )
                    }
                }
            }

            state.error?.let { message ->
                item {
                    AlertDataNotice(
                        title = "Alert data unavailable",
                        message = message,
                        onRetry = viewModel::refresh
                    )
                }
            }

            if (state.filteredAlerts.isEmpty()) {
                item {
                    AlertDataNotice(
                        title = when (state.status) {
                            AlertsDataStatus.LOADING -> "Loading alerts"
                            AlertsDataStatus.AVAILABLE -> "No alerts for this filter"
                            AlertsDataStatus.UNAVAILABLE -> "Alerts unavailable"
                        },
                        message = when (state.status) {
                            AlertsDataStatus.LOADING -> "Checking the provider and local alert cache."
                            AlertsDataStatus.AVAILABLE -> "No provider-backed alert records are currently available for this farm."
                            AlertsDataStatus.UNAVAILABLE -> "The provider and local alert cache did not return alert data."
                        },
                        onRetry = if (state.status == AlertsDataStatus.UNAVAILABLE) viewModel::refresh else null
                    )
                }
            }

            items(state.filteredAlerts, key = { it.id }) { alert ->
                val (bgColor, stripeColor, icon) = when (alert.severity) {
                    AlertSeverity.CRITICAL -> Triple(WireAlertPale, WireAlert, Icons.Default.Warning)
                    AlertSeverity.WARNING -> Triple(WireGoldPale, WireGold, Icons.Default.WaterDrop)
                    AlertSeverity.INFO -> Triple(WireSkyPale, WireSky, Icons.Default.CloudOff)
                    AlertSeverity.SUCCESS -> Triple(WireLeafPale, WireLeaf, Icons.Default.CheckCircle)
                }

                Box(modifier = Modifier.padding(horizontal = 16.dp, vertical = 5.dp)) {
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { viewModel.markAsRead(alert.id) },
                        shape = RoundedCornerShape(12.dp),
                        colors = CardDefaults.cardColors(containerColor = bgColor),
                        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
                    ) {
                        Row(modifier = Modifier.fillMaxWidth()) {
                            // Left 4px accent stripe
                            Box(
                                modifier = Modifier
                                    .width(4.dp)
                                    .height(90.dp)
                                    .background(stripeColor)
                            )

                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(12.dp),
                                verticalAlignment = Alignment.Top
                            ) {
                                Icon(
                                    imageVector = icon,
                                    contentDescription = alert.severityLabel,
                                    tint = stripeColor,
                                    modifier = Modifier.size(22.dp)
                                )
                                Spacer(modifier = Modifier.width(10.dp))
                                Column(modifier = Modifier.weight(1f)) {
                                    Text(
                                        text = alert.title,
                                        fontSize = 14.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = WireTextPrimary
                                    )
                                    Text(
                                        text = alert.message,
                                        fontSize = 12.sp,
                                        color = WireTextSecondary,
                                        lineHeight = 17.sp,
                                        modifier = Modifier.padding(top = 3.dp)
                                    )
                                     Text(
                                        text = if (alert.isRead) "Read" else "Unread",
                                        fontSize = 10.sp,
                                        color = WireTextMuted,
                                        modifier = Modifier.padding(top = 4.dp)
                                    )
                                }
                            }
                        }
                    }
                }
            }

            item {
                Spacer(modifier = Modifier.height(24.dp))
            }
        }

        LoadingOverlay(isLoading = state.isLoading)
    }
}

@Composable
private fun WireFilterChip(
    label: String,
    isSelected: Boolean,
    onClick: () -> Unit
) {
    Box(
        modifier = Modifier
            .clip(RoundedCornerShape(8.dp))
            .background(if (isSelected) WireSageDeep else WireSurface2)
            .clickable { onClick() }
            .heightIn(min = 48.dp)
            .padding(horizontal = 12.dp, vertical = 6.dp)
    ) {
        Text(
            text = label,
            fontSize = 11.sp,
            fontWeight = FontWeight.Bold,
            color = if (isSelected) Color.White else WireSageDeep
        )
    }
}

@Composable
private fun AlertDataNotice(
    title: String,
    message: String,
    onRetry: (() -> Unit)? = null
) {
    Card(
        modifier = Modifier.padding(horizontal = 16.dp, vertical = 5.dp),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = WireSurface2)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(14.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = if (onRetry == null) Icons.Default.CloudOff else Icons.Default.Warning,
                contentDescription = null,
                tint = WireTextMuted,
                modifier = Modifier.size(22.dp)
            )
            Spacer(modifier = Modifier.width(10.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = title,
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Bold,
                    color = WireTextPrimary
                )
                Text(
                    text = message,
                    fontSize = 12.sp,
                    color = WireTextSecondary,
                    lineHeight = 17.sp,
                    modifier = Modifier.padding(top = 3.dp)
                )
            }
            onRetry?.let { retry ->
                TextButton(onClick = retry) {
                    Text("Retry", color = WireSageDeep, fontSize = 12.sp)
                }
            }
        }
    }
}
