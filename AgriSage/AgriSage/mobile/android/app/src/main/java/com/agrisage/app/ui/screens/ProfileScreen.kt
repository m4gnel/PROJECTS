package com.agrisage.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.agrisage.app.navigation.*
import com.agrisage.app.ui.theme.*

/**
 * ProfileScreen (Screen 8) per AgriSage Master Spec.
 *
 * Features:
 * - Farmer Info Header (Name, Location, State/District badge)
 * - Language Preference Selector (EN, HI, ML, TA, TE, KN)
 * - Registered Crops chip list
 * - Offline & Cloud Sync Status indicator
 * - App Settings toggles (Voice auto-play, High contrast, FCM Notifications)
 * - Support & Feedback quick action
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProfileScreen(
    navController: NavController? = null,
    onNavigateBack: () -> Unit = {},
    onEditProfile: () -> Unit = {}
) {
    var selectedLanguage by remember { mutableStateOf("Malayalam (Malayalam)") }
    var voiceAutoPlay by remember { mutableStateOf(true) }
    var pushNotifications by remember { mutableStateOf(true) }
    var highContrast by remember { mutableStateOf(false) }
    var offlineSyncEnabled by remember { mutableStateOf(true) }

    val languages = listOf("English", "हिंदी (Hindi)", "മലയാളം (Malayalam)", "தமிழ் (Tamil)", "తెలుగు (Telugu)", "കന്നഡ (Kannada)")

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        "Farmer Profile & Settings",
                        fontWeight = FontWeight.Bold,
                        color = Color.White
                    )
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = SageDeep
                )
            )
        },
        bottomBar = {
            if (navController != null) {
                com.agrisage.app.ui.components.AgriBottomNav(
                    currentRoute = "profile",
                    onNavigate = { route ->
                        when (route) {
                            "home" -> navController.navigate(com.agrisage.app.navigation.Home) { popUpTo(com.agrisage.app.navigation.Home) { inclusive = true } }
                            "advisor" -> navController.navigate(com.agrisage.app.navigation.Advisor)
                            "fields" -> navController.navigate(com.agrisage.app.navigation.Fields)
                            "weather" -> navController.navigate(com.agrisage.app.navigation.Weather)
                        }
                    }
                )
            }
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .background(Color(0xFFF6F8F5)),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Header Profile Card
            item {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = SageDeep)
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(20.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier
                                .size(64.dp)
                                .clip(CircleShape)
                                .background(SageLeaf),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.Person,
                                contentDescription = null,
                                modifier = Modifier.size(36.dp),
                                tint = SageDeep
                            )
                        }

                        Spacer(modifier = Modifier.width(16.dp))

                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = "Kiran Kumar",
                                style = MaterialTheme.typography.titleLarge,
                                fontWeight = FontWeight.Bold,
                                color = Color.White
                            )
                            Text(
                                text = "+91 98765 43210",
                                style = MaterialTheme.typography.bodyMedium,
                                color = SageLeaf
                            )
                            Spacer(modifier = Modifier.height(4.dp))
                            Surface(
                                shape = RoundedCornerShape(12.dp),
                                color = SageMid.copy(alpha = 0.6f)
                            ) {
                                Text(
                                    text = "Palakkad, Kerala • KAU Zone 4",
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp),
                                    style = MaterialTheme.typography.labelSmall,
                                    color = Color.White
                                )
                            }
                        }
                    }
                }
            }

            // Sync & Status Banner
            item {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    colors = CardDefaults.cardColors(containerColor = Color.White),
                    elevation = CardDefaults.cardElevation(2.dp)
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                Icons.Default.CloudDone,
                                contentDescription = null,
                                tint = SageMid,
                                modifier = Modifier.size(24.dp)
                            )
                            Spacer(modifier = Modifier.width(12.dp))
                            Column {
                                Text(
                                    "Cloud Data Sync",
                                    fontWeight = FontWeight.SemiBold,
                                    fontSize = 14.sp,
                                    color = DarkText
                                )
                                Text(
                                    "Last synced: 10 mins ago • 0 pending",
                                    style = MaterialTheme.typography.bodySmall,
                                    color = Color.Gray
                                )
                            }
                        }
                        TextButton(onClick = { /* Force Sync */ }) {
                            Text("Sync Now", color = SageMid, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }

            // Section: Preferred Language
            item {
                ProfileSectionCard(title = "App Language / ഭാഷ", icon = Icons.Default.Language) {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        languages.forEach { lang ->
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clip(RoundedCornerShape(8.dp))
                                    .background(if (selectedLanguage == lang) SageLeaf.copy(alpha = 0.3f) else Color.Transparent)
                                    .clickable { selectedLanguage = lang }
                                    .padding(horizontal = 12.dp, vertical = 10.dp),
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.SpaceBetween
                            ) {
                                Text(
                                    text = lang,
                                    fontWeight = if (selectedLanguage == lang) FontWeight.Bold else FontWeight.Normal,
                                    color = DarkText
                                )
                                RadioButton(
                                    selected = (selectedLanguage == lang),
                                    onClick = { selectedLanguage = lang },
                                    colors = RadioButtonDefaults.colors(selectedColor = SageDeep)
                                )
                            }
                        }
                    }
                }
            }

            // Section: Registered Crops
            item {
                ProfileSectionCard(title = "Primary Crops", icon = Icons.Default.Grass) {
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        listOf("🌾 Paddy (Uma)", "🥥 Coconut", "🍌 Banana (Nendran)", "🌶️ Chili").forEach { crop ->
                            Surface(
                                shape = RoundedCornerShape(16.dp),
                                color = SageLeaf.copy(alpha = 0.4f),
                                border = androidx.compose.foundation.BorderStroke(1.dp, SageMid)
                            ) {
                                Text(
                                    text = crop,
                                    modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
                                    style = MaterialTheme.typography.bodySmall,
                                    fontWeight = FontWeight.Medium,
                                    color = DarkText
                                )
                            }
                        }
                    }
                }
            }

            // Section: App Settings Toggles
            item {
                ProfileSectionCard(title = "Voice & Accessibility", icon = Icons.Default.Settings) {
                    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                        SettingToggleRow(
                            title = "Voice Response Auto-Play",
                            subtitle = "Automatically play AI audio responses in your native language",
                            checked = voiceAutoPlay,
                            onCheckedChange = { voiceAutoPlay = it }
                        )
                        HorizontalDivider(color = Color.LightGray.copy(alpha = 0.4f))
                        SettingToggleRow(
                            title = "Push Notifications",
                            subtitle = "Receive real-time weather & pest outbreak alerts",
                            checked = pushNotifications,
                            onCheckedChange = { pushNotifications = it }
                        )
                        HorizontalDivider(color = Color.LightGray.copy(alpha = 0.4f))
                        SettingToggleRow(
                            title = "Offline Pre-fetching",
                            subtitle = "Pre-load 7-day weather & advisories for offline use",
                            checked = offlineSyncEnabled,
                            onCheckedChange = { offlineSyncEnabled = it }
                        )
                    }
                }
            }

            // About & Version
            item {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 12.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(
                        "AgriSage v1.0.0 (Build 100)",
                        style = MaterialTheme.typography.bodySmall,
                        color = Color.Gray,
                        fontWeight = FontWeight.Medium
                    )
                    Text(
                        "Empowering Indian Farmers with Generative AI",
                        style = MaterialTheme.typography.labelSmall,
                        color = Color.Gray
                    )
                }
            }
        }
    }
}

@Composable
private fun ProfileSectionCard(
    title: String,
    icon: ImageVector,
    content: @Composable ColumnScope.() -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(2.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.padding(bottom = 12.dp)
            ) {
                Icon(icon, contentDescription = null, tint = SageDeep, modifier = Modifier.size(20.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    color = DarkText
                )
            }
            content()
        }
    }
}

@Composable
private fun SettingToggleRow(
    title: String,
    subtitle: String,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text(title, fontWeight = FontWeight.SemiBold, fontSize = 14.sp, color = DarkText)
            Text(subtitle, fontSize = 12.sp, color = Color.Gray)
        }
        Switch(
            checked = checked,
            onCheckedChange = onCheckedChange,
            colors = SwitchDefaults.colors(
                checkedThumbColor = Color.White,
                checkedTrackColor = SageDeep
            )
        )
    }
}

@Preview(showBackground = true)
@Composable
fun ProfileScreenPreview() {
    AgriSageTheme {
        ProfileScreen()
    }
}
