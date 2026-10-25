package com.agrisage.app.ui.screens.onboarding

import android.Manifest
import android.os.Build
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
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavHostController
import com.agrisage.app.navigation.Home
import com.agrisage.app.navigation.Onboarding
import com.agrisage.app.ui.components.LoadingOverlay
import com.agrisage.app.ui.theme.OnSurface
import com.agrisage.app.ui.theme.OnSurfaceVar
import com.agrisage.app.ui.theme.SageGreen300
import com.agrisage.app.ui.theme.SageGreen700
import com.agrisage.app.ui.theme.SageGreen900
import com.agrisage.app.ui.theme.Surface
import com.agrisage.app.ui.theme.SurfaceDim

@Composable
fun OnboardingScreen(
    navController: NavHostController,
    viewModel: OnboardingViewModel = hiltViewModel()
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    val notificationPermissionLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { }

    LaunchedEffect(state.currentPage) {
        if (state.currentPage == 2 && Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            notificationPermissionLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
        }
    }

    Box(modifier = Modifier.fillMaxSize().background(Surface)) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(24.dp),
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            // Header
            Column {
                Text(
                    text = "Welcome to Agri-SAGE",
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Bold,
                    color = SageGreen900
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = "Step ${state.currentPage + 1} of 3",
                    fontSize = 14.sp,
                    color = OnSurfaceVar
                )
            }

            // Page Content
            when (state.currentPage) {
                0 -> {
                    // Language Selection
                    Column {
                        Text(
                            text = "Choose your preferred language / ഭാഷ തിരഞ്ഞെടുക്കുക",
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Medium,
                            color = OnSurface
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                            val languages = listOf(
                            "ml" to "മലയാളം (Malayalam)",
                            "en" to "English",
                            "ta" to "தமிழ் (Tamil)",
                            "hi" to "हिन्दी (Hindi)",
                            "te" to "తెలుగు (Telugu)",
                            "pa" to "ਪੰਜਾਬੀ (Punjabi)"
                        )
                        languages.forEach { (code, label) ->
                            val isSelected = state.selectedLanguage == code
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(vertical = 6.dp)
                                    .clip(RoundedCornerShape(12.dp))
                                    .background(if (isSelected) SageGreen300.copy(alpha = 0.2f) else SurfaceDim)
                                    .border(
                                        width = if (isSelected) 2.dp else 0.dp,
                                        color = if (isSelected) SageGreen700 else Color.Transparent,
                                        shape = RoundedCornerShape(12.dp)
                                    )
                                    .clickable { viewModel.selectLanguage(code) }
                                    .padding(16.dp)
                            ) {
                                Text(
                                    text = label,
                                    fontSize = 16.sp,
                                    fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal,
                                    color = if (isSelected) SageGreen900 else OnSurface
                                )
                            }
                        }
                    }
                }
                1 -> {
                    // Farmer Details
                    Column {
                        Text(
                            text = "Tell us about your farm",
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Medium,
                            color = OnSurface
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        OutlinedTextField(
                            value = state.farmerName,
                            onValueChange = { viewModel.updateName(it) },
                            label = { Text("Your Name / പേര്") },
                            modifier = Modifier.fillMaxWidth()
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        OutlinedTextField(
                            value = state.phone,
                            onValueChange = { viewModel.updatePhone(it) },
                            label = { Text("Mobile number / മൊബൈൽ") },
                            placeholder = { Text("10-digit number") },
                            modifier = Modifier.fillMaxWidth(),
                            singleLine = true
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        OutlinedTextField(
                            value = state.village,
                            onValueChange = { viewModel.updateVillage(it) },
                            label = { Text("Village / ഗ്രാമം (e.g. your village)") },
                            modifier = Modifier.fillMaxWidth()
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        OutlinedTextField(
                            value = state.district,
                            onValueChange = { viewModel.updateDistrict(it) },
                            label = { Text("District / ജില്ല (e.g. Nashik)") },
                            modifier = Modifier.fillMaxWidth()
                        )
                    }
                }
                2 -> {
                    // Permissions & Start
                    Column {
                        Text(
                            text = "Enable Permissions",
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Medium,
                            color = OnSurface
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        Text(
                            text = "Location: Needed for field-level weather and soil guidance across India.",
                            fontSize = 14.sp,
                            color = OnSurfaceVar
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = "Notifications: Receive pest alerts, weather warnings, and field reminders.",
                            fontSize = 14.sp,
                            color = OnSurfaceVar
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        if (state.otpSent) {
                            OutlinedTextField(
                                value = state.otp,
                                onValueChange = { viewModel.updateOtp(it) },
                                label = { Text("Verification code / സ്ഥിരീകരണ കോഡ്") },
                                placeholder = { Text("6 digits") },
                                modifier = Modifier.fillMaxWidth(),
                                singleLine = true
                            )
                        } else {
                            Text(
                                text = "We will send a one-time code to verify your mobile number.",
                                fontSize = 14.sp,
                                color = OnSurfaceVar
                            )
                        }
                        state.notice?.let { notice ->
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(text = notice, fontSize = 13.sp, color = SageGreen700)
                        }
                        state.error?.let { error ->
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(text = error, fontSize = 13.sp, color = Color(0xFFB3261E))
                        }
                    }
                }
            }

            // Bottom Navigation Buttons
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                if (state.currentPage > 0) {
                    Button(
                        onClick = { viewModel.previousPage() },
                        colors = ButtonDefaults.buttonColors(containerColor = SurfaceDim)
                    ) {
                        Text("Back", color = OnSurface)
                    }
                } else {
                    Spacer(modifier = Modifier.weight(1f))
                }

                if (state.currentPage < 2) {
                    Button(
                        onClick = { viewModel.nextPage() },
                        colors = ButtonDefaults.buttonColors(containerColor = SageGreen700)
                    ) {
                        Text("Next", color = Color.White)
                    }
                } else {
                    Button(
                        onClick = {
                            viewModel.completeOnboarding {
                                navController.navigate(Home) {
                                    popUpTo(Onboarding) { inclusive = true }
                                }
                            }
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = SageGreen700)
                    ) {
                        Text("Get Started / തുടങ്ങാം", color = Color.White)
                    }
                }
            }
        }

        LoadingOverlay(isLoading = state.isLoading)
    }
}
