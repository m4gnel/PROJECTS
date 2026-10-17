package com.agrisage.app.ui.screens.profile

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
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Switch
import androidx.compose.material3.SwitchDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavHostController
import com.agrisage.app.navigation.Screen
import com.agrisage.app.ui.components.LoadingOverlay
import com.agrisage.app.ui.theme.WireAlert
import com.agrisage.app.ui.theme.WireBorder
import com.agrisage.app.ui.theme.WireLeaf
import com.agrisage.app.ui.theme.WireSage
import com.agrisage.app.ui.theme.WireSageDeep
import com.agrisage.app.ui.theme.WireTextMuted
import com.agrisage.app.ui.theme.WireTextPrimary
import com.agrisage.app.ui.theme.WireWhite

@Composable
fun ProfileScreen(
    navController: NavHostController,
    viewModel: ProfileViewModel = hiltViewModel()
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    val prof = state.profile

    Box(modifier = Modifier.fillMaxSize().background(WireWhite)) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
        ) {
            // Header Top Bar with Gradient
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(
                        brush = Brush.linearGradient(
                            colors = listOf(WireSageDeep, WireSage)
                        )
                    )
                    .padding(horizontal = 20.dp, vertical = 26.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Box(
                    modifier = Modifier
                        .size(64.dp)
                        .clip(CircleShape)
                        .background(WireLeaf)
                        .padding(3.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .clip(CircleShape)
                            .background(WireLeaf),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(text = "👨‍🌾", fontSize = 30.sp)
                    }
                }

                Spacer(modifier = Modifier.height(10.dp))

                Text(
                    text = prof?.name ?: "Rajan Pillai",
                    fontSize = 18.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = Color.White
                )

                Text(
                    text = "📍 ${prof?.village ?: "Kalady"}, ${prof?.district ?: "Ernakulam"} · 3.2 acres",
                    fontSize = 12.sp,
                    color = Color.White.copy(alpha = 0.8f),
                    modifier = Modifier.padding(top = 2.dp)
                )
            }

            // Body
            Column(modifier = Modifier.padding(16.dp)) {

                // Farm Details Section
                ProfileSectionCard(title = "FARM DETAILS") {
                    ProfileRow(icon = "🌾", label = "Primary Crop", value = prof?.primaryCrop ?: "Paddy")
                    HorizontalDivider(color = WireBorder.copy(alpha = 0.5f), thickness = 1.dp)
                    ProfileRow(icon = "📏", label = "Total Area", value = "3.2 acres (7,000 m²)")
                    HorizontalDivider(color = WireBorder.copy(alpha = 0.5f), thickness = 1.dp)
                    ProfileRow(icon = "💧", label = "Irrigation", value = "Canal", showArrow = true)
                }

                Spacer(modifier = Modifier.height(14.dp))

                // Preferences Section
                ProfileSectionCard(title = "PREFERENCES") {
                    ProfileRow(icon = "🌐", label = "Language", value = "Malayalam (മലയാളം)", showArrow = true)
                    HorizontalDivider(color = WireBorder.copy(alpha = 0.5f), thickness = 1.dp)
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 14.dp, vertical = 10.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text("🔔", fontSize = 16.sp)
                            Spacer(modifier = Modifier.width(10.dp))
                            Text("Notifications", fontSize = 13.sp, fontWeight = FontWeight.Medium, color = WireTextPrimary)
                        }
                        Switch(
                            checked = state.notificationsEnabled,
                            onCheckedChange = { viewModel.toggleNotifications() },
                            colors = SwitchDefaults.colors(checkedThumbColor = WireSage)
                        )
                    }
                    HorizontalDivider(color = WireBorder.copy(alpha = 0.5f), thickness = 1.dp)
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 14.dp, vertical = 10.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text("📴", fontSize = 16.sp)
                            Spacer(modifier = Modifier.width(10.dp))
                            Text("Offline Mode", fontSize = 13.sp, fontWeight = FontWeight.Medium, color = WireTextPrimary)
                        }
                        Switch(
                            checked = state.offlineModeEnabled,
                            onCheckedChange = { viewModel.toggleOfflineMode() },
                            colors = SwitchDefaults.colors(checkedThumbColor = WireSage)
                        )
                    }
                }

                Spacer(modifier = Modifier.height(14.dp))

                // Account Section
                ProfileSectionCard(title = "ACCOUNT") {
                    ProfileRow(icon = "🔒", label = "Privacy Policy", showArrow = true)
                    HorizontalDivider(color = WireBorder.copy(alpha = 0.5f), thickness = 1.dp)
                    ProfileRow(icon = "🆘", label = "Help & Support", showArrow = true)
                }

                Spacer(modifier = Modifier.height(20.dp))

                // Action Buttons
                OutlinedButton(
                    onClick = { viewModel.enableEditing() },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    border = BorderStroke(1.5.dp, WireSage)
                ) {
                    Text("Edit Farm Profile", color = WireSage, fontWeight = FontWeight.Bold)
                }

                Spacer(modifier = Modifier.height(8.dp))

                Button(
                    onClick = {
                        viewModel.logout {
                            navController.navigate(Screen.Onboarding) {
                                popUpTo(Screen.Home) { inclusive = true }
                            }
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = WireAlert)
                ) {
                    Text("Log Out / പുറത്തുകടക്കുക", color = Color.White, fontWeight = FontWeight.Bold)
                }

                Spacer(modifier = Modifier.height(32.dp))
            }
        }

        LoadingOverlay(isLoading = state.isLoading)
    }
}

@Composable
private fun ProfileSectionCard(
    title: String,
    content: @Composable () -> Unit
) {
    Column {
        Text(
            text = title,
            fontSize = 11.sp,
            fontWeight = FontWeight.Bold,
            color = WireTextMuted,
            letterSpacing = 1.sp,
            modifier = Modifier.padding(start = 4.dp, bottom = 6.dp)
        )
        Card(
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(14.dp),
            colors = CardDefaults.cardColors(containerColor = Color.White),
            border = BorderStroke(1.5.dp, WireBorder),
            elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
        ) {
            Column {
                content()
            }
        }
    }
}

@Composable
private fun ProfileRow(
    icon: String,
    label: String,
    value: String? = null,
    showArrow: Boolean = false,
    onClick: () -> Unit = {}
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .padding(horizontal = 14.dp, vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(text = icon, fontSize = 16.sp)
        Spacer(modifier = Modifier.width(10.dp))
        Text(
            text = label,
            fontSize = 13.sp,
            fontWeight = FontWeight.Medium,
            color = WireTextPrimary,
            modifier = Modifier.weight(1f)
        )
        if (value != null) {
            Text(
                text = value,
                fontSize = 12.sp,
                color = WireTextMuted,
                modifier = Modifier.padding(end = 6.dp)
            )
        }
        if (showArrow) {
            Icon(
                imageVector = Icons.AutoMirrored.Filled.KeyboardArrowRight,
                contentDescription = null,
                tint = WireTextMuted,
                modifier = Modifier.size(18.dp)
            )
        }
    }
}
