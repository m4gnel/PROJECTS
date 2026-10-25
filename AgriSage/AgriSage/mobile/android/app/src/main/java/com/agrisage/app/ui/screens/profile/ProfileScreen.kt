package com.agrisage.app.ui.screens.profile

import android.content.Intent
import android.provider.Settings
import androidx.core.app.NotificationManagerCompat
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.selection.selectable
import androidx.compose.foundation.selection.selectableGroup
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.CloudDone
import androidx.compose.material.icons.filled.Language
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.WifiOff
import androidx.compose.material3.Button
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.TextButton
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.RadioButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
import androidx.compose.material3.SwitchDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.compose.LocalLifecycleOwner
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.navigation.NavHostController
import com.agrisage.app.BuildConfig
import com.agrisage.app.navigation.Screen
import com.agrisage.app.ui.components.LoadingOverlay
import com.agrisage.app.ui.components.tactilePress
import com.agrisage.app.ui.theme.WireAlert
import com.agrisage.app.ui.theme.WireBorder
import com.agrisage.app.ui.theme.WireLeaf
import com.agrisage.app.ui.theme.WireSage
import com.agrisage.app.ui.theme.WireSageDeep
import com.agrisage.app.ui.theme.WireTextMuted
import com.agrisage.app.ui.theme.WireTextPrimary
import com.agrisage.app.ui.theme.WireTextSecondary
import com.agrisage.app.ui.theme.WireWhite
import java.util.Locale

private val ProfileBackground = Color(0xFFF6F8F5)
private val ProfileReference = FarmerProfile(
    id = "reference-profile",
    name = "Kiran Kumar",
    phone = "+91 98765 43210",
    village = "Palakkad",
    district = "Kerala · KAU Zone 4",
    totalFieldsSqM = 0f,
    primaryCrop = "",
    preferredLanguage = "ml",
)

private val profileLanguages = listOf(
    "en" to "English",
    "hi" to "हिंदी (Hindi)",
    "ml" to "മലയാളം (Malayalam)",
    "ta" to "தமிழ் (Tamil)",
    "te" to "తెలుగు (Telugu)",
    "kn" to "ಕನ್ನಡ (Kannada)",
)

@Composable
fun ProfileScreen(
    navController: NavHostController,
    viewModel: ProfileViewModel = hiltViewModel(),
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    val profile = state.profile ?: if (BuildConfig.REFERENCE_PREVIEW) ProfileReference else null
    val context = LocalContext.current
    val lifecycleOwner = LocalLifecycleOwner.current
    var notificationsEnabled by remember { mutableStateOf(NotificationManagerCompat.from(context).areNotificationsEnabled()) }
    DisposableEffect(lifecycleOwner, context) {
        val observer = LifecycleEventObserver { _, event ->
            if (event == Lifecycle.Event.ON_RESUME) {
                notificationsEnabled = NotificationManagerCompat.from(context).areNotificationsEnabled()
            }
        }
        lifecycleOwner.lifecycle.addObserver(observer)
        onDispose { lifecycleOwner.lifecycle.removeObserver(observer) }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(ProfileBackground),
    ) {
        Column(modifier = Modifier.fillMaxSize()) {
            ProfileHeader(onBack = { navController.popBackStack() })

            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f)
                    .verticalScroll(rememberScrollState())
                    .padding(horizontal = 15.dp, vertical = 15.dp),
            ) {
                ProfileIdentityCard(profile)
                Spacer(Modifier.height(14.dp))
                SyncCard()
                Spacer(Modifier.height(14.dp))
                LanguageCard(
                    selectedLanguage = state.selectedLanguage,
                    onLanguageSelected = viewModel::changeLanguage,
                )
                Spacer(Modifier.height(14.dp))
                PreferencesCard(
                    notificationsEnabled = notificationsEnabled,
                    onNotificationsChanged = {
                        context.startActivity(Intent(Settings.ACTION_APP_NOTIFICATION_SETTINGS).apply {
                            putExtra(Settings.EXTRA_APP_PACKAGE, context.packageName)
                        })
                    },
                )
                state.error?.let { error ->
                    Text(
                        text = error,
                        color = WireAlert,
                        fontSize = 12.sp,
                        modifier = Modifier.padding(top = 12.dp),
                    )
                    TextButton(onClick = viewModel::loadProfile) { Text("Retry profile") }
                }
                Spacer(Modifier.height(24.dp))
                OutlinedButton(
                    onClick = viewModel::enableEditing,
                    enabled = state.profile != null && !state.isLoading,
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    border = androidx.compose.foundation.BorderStroke(1.dp, WireSage),
                ) {
                    Text("Edit Farm Profile", color = WireSage, fontWeight = FontWeight.Bold)
                }
                Spacer(Modifier.height(8.dp))
                Button(
                    onClick = {
                        viewModel.logout {
                            navController.navigate(Screen.Onboarding) {
                                popUpTo(Screen.Home) { inclusive = true }
                            }
                        }
                    },
                    enabled = !BuildConfig.REFERENCE_PREVIEW,
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = WireAlert),
                ) {
                    Text("Log Out", color = Color.White, fontWeight = FontWeight.Bold)
                }
                Spacer(Modifier.height(24.dp))
            }
        }

        LoadingOverlay(isLoading = state.isLoading)
        if (state.isEditing && state.profile != null) {
            ProfileEditDialog(
                profile = state.profile!!,
                isSaving = state.isSaving,
                error = state.error,
                onDismiss = viewModel::cancelEditing,
                onSave = viewModel::saveProfile,
            )
        }
    }
}

@Composable
private fun ProfileHeader(onBack: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .background(WireSageDeep)
            .statusBarsPadding()
            .padding(horizontal = 8.dp, vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Icon(
            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
            contentDescription = "Back",
            tint = Color.White,
            modifier = Modifier
                .size(48.dp)
                .tactilePress(
                    scaleDown = 0.94f,
                    onClickLabel = "Go back",
                    onClick = onBack,
                )
                .padding(12.dp),
        )
        Text(
            text = "Farmer Profile & Settings",
            color = Color.White,
            fontSize = 20.sp,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(start = 4.dp),
        )
    }
}

@Composable
private fun ProfileIdentityCard(profile: FarmerProfile?) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = WireSageDeep),
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 18.dp, vertical = 16.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Surface(
                color = Color(0xFF42A878),
                shape = CircleShape,
                modifier = Modifier.size(58.dp),
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(Icons.Default.Person, contentDescription = null, tint = WireSageDeep, modifier = Modifier.size(30.dp))
                }
            }
            Spacer(Modifier.width(14.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = profile?.name?.takeIf(String::isNotBlank) ?: "Profile unavailable",
                    color = Color.White,
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold,
                )
                Text(
                    text = profile?.phone?.takeIf(String::isNotBlank) ?: "Phone unavailable",
                    color = Color(0xFF5FC493),
                    fontSize = 12.sp,
                    modifier = Modifier.padding(top = 2.dp),
                )
                Surface(
                    color = Color(0xFF2B634B),
                    shape = RoundedCornerShape(10.dp),
                    modifier = Modifier.padding(top = 6.dp),
                ) {
                    Text(
                        text = profileLocation(profile),
                        color = Color.White,
                        fontSize = 10.sp,
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp),
                    )
                }
            }
        }
    }
}

@Composable
private fun SyncCard() {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        border = androidx.compose.foundation.BorderStroke(1.dp, WireBorder.copy(alpha = 0.65f)),
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 14.dp, vertical = 14.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Icon(Icons.Default.CloudDone, contentDescription = null, tint = WireSage, modifier = Modifier.size(23.dp))
            Spacer(Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text("Cloud Data Sync", fontWeight = FontWeight.SemiBold, fontSize = 14.sp, color = WireTextPrimary)
                Text("Cloud upload confirmation is not available. Local records must be retained.", fontSize = 11.sp, color = WireTextSecondary, modifier = Modifier.padding(top = 2.dp))
            }
            TextButton(onClick = {}, enabled = false) { Text("Sync Now", fontSize = 12.sp) }
        }
    }
}

@Composable
private fun LanguageCard(
    selectedLanguage: String,
    onLanguageSelected: (String) -> Unit,
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        border = androidx.compose.foundation.BorderStroke(1.dp, WireBorder.copy(alpha = 0.65f)),
    ) {
        Column(modifier = Modifier.selectableGroup().padding(top = 15.dp, bottom = 8.dp)) {
            Row(
                modifier = Modifier.padding(horizontal = 14.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Icon(Icons.Default.Language, contentDescription = null, tint = WireSageDeep, modifier = Modifier.size(20.dp))
                Spacer(Modifier.width(8.dp))
                Text("Advisory Language / മലയാളം", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = WireTextPrimary)
            }
            Spacer(Modifier.height(6.dp))
            profileLanguages.forEach { (code, label) ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .selectable(selectedLanguage == code, role = Role.RadioButton, onClick = { onLanguageSelected(code) })
                        .padding(horizontal = 14.dp, vertical = 3.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text(label, fontSize = 14.sp, color = WireTextPrimary, modifier = Modifier.weight(1f))
                    RadioButton(
                        selected = selectedLanguage == code,
                        onClick = null,
                        modifier = Modifier.size(48.dp),
                    )
                }
            }
        }
    }
}

@Composable
private fun PreferencesCard(
    notificationsEnabled: Boolean,
    onNotificationsChanged: () -> Unit,
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        border = androidx.compose.foundation.BorderStroke(1.dp, WireBorder.copy(alpha = 0.65f)),
    ) {
        Column {
            PreferenceSwitchRow(
                icon = Icons.Default.Notifications,
                label = "Notifications",
                checked = notificationsEnabled,
                onCheckedChange = onNotificationsChanged,
            )
            HorizontalDivider(color = WireBorder.copy(alpha = 0.55f))
            PreferenceSwitchRow(
                icon = Icons.Default.WifiOff,
                label = "Offline cache",
                checked = true,
                onCheckedChange = {},
                enabled = false,
            )
            Text("Previously loaded records remain readable. Fresh advice requires a connection.",
                color = WireTextSecondary, fontSize = 11.sp, modifier = Modifier.padding(14.dp))
        }
    }
}

@Composable
private fun PreferenceSwitchRow(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    label: String,
    checked: Boolean,
    onCheckedChange: () -> Unit,
    enabled: Boolean = true,
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(enabled = enabled, onClick = onCheckedChange)
            .padding(horizontal = 14.dp, vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween,
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Icon(icon, contentDescription = null, tint = WireSage, modifier = Modifier.size(20.dp))
            Spacer(Modifier.width(10.dp))
            Text(label, fontSize = 13.sp, fontWeight = FontWeight.Medium, color = WireTextPrimary)
        }
        Switch(
            checked = checked,
            enabled = enabled,
            onCheckedChange = { onCheckedChange() },
            colors = SwitchDefaults.colors(checkedThumbColor = WireSage),
        )
    }
}

@Composable
private fun ProfileEditDialog(
    profile: FarmerProfile,
    isSaving: Boolean,
    error: String?,
    onDismiss: () -> Unit,
    onSave: (FarmerProfile) -> Unit,
) {
    var name by rememberSaveable(profile.id) { mutableStateOf(profile.name) }
    var district by rememberSaveable(profile.id) { mutableStateOf(profile.district) }
    AlertDialog(
        onDismissRequest = { if (!isSaving) onDismiss() },
        title = { Text("Edit Farm Profile") },
        text = {
            Column(Modifier.verticalScroll(rememberScrollState())) {
                OutlinedTextField(value = name, onValueChange = { name = it }, label = { Text("Name") },
                    enabled = !isSaving, singleLine = true, modifier = Modifier.fillMaxWidth())
                Spacer(Modifier.height(12.dp))
                OutlinedTextField(value = district, onValueChange = { district = it }, label = { Text("District") },
                    enabled = !isSaving, singleLine = true, modifier = Modifier.fillMaxWidth())
                error?.let { Text(it, color = WireAlert, modifier = Modifier.padding(top = 8.dp)) }
            }
        },
        confirmButton = {
            TextButton(enabled = !isSaving && name.isNotBlank(), onClick = {
                onSave(profile.copy(name = name, district = district))
            }) { Text(if (isSaving) "Saving…" else "Save") }
        },
        dismissButton = { TextButton(onClick = onDismiss, enabled = !isSaving) { Text("Cancel") } },
    )
}

private fun profileLocation(profile: FarmerProfile?): String {
    if (profile == null) return "Location unavailable"
    return listOf(profile.village, profile.district)
        .mapNotNull { it.trim().takeIf(String::isNotEmpty) }
        .distinct()
        .joinToString(", ")
        .ifBlank { "Location unavailable" }
}
