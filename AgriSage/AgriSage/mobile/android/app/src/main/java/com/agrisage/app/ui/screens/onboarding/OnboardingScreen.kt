package com.agrisage.app.ui.screens.onboarding

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
import com.agrisage.app.navigation.Screen
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
                            "hi" to "हिन्दी (Hindi)"
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
                            value = state.village,
                            onValueChange = { viewModel.updateVillage(it) },
                            label = { Text("Village / ഗ്രാമം (e.g. Kalady)") },
                            modifier = Modifier.fillMaxWidth()
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        OutlinedTextField(
                            value = state.district,
                            onValueChange = { viewModel.updateDistrict(it) },
                            label = { Text("District / ജില്ല (e.g. Ernakulam)") },
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
                            text = "📍 Location: Needed for Hyper-local weather & soil data for Kerala.",
                            fontSize = 14.sp,
                            color = OnSurfaceVar
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = "🔔 Notifications: Receive NBAIR pest alerts and weather warnings.",
                            fontSize = 14.sp,
                            color = OnSurfaceVar
                        )
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
                                navController.navigate(Screen.Home) {
                                    popUpTo(Screen.Onboarding) { inclusive = true }
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
