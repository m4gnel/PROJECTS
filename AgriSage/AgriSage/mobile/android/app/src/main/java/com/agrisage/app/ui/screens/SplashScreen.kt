package com.agrisage.app.ui.screens

import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import androidx.navigation.compose.rememberNavController
import androidx.hilt.navigation.compose.hiltViewModel
import com.agrisage.app.navigation.Home
import com.agrisage.app.navigation.Onboarding
import com.agrisage.app.ui.theme.*
import kotlinx.coroutines.delay

/**
 * Screen 1: Splash Screen
 * Route: Splash
 * Auto-navigates to Onboarding (first launch) OR Home (returning user) after 2000ms.
 * Animation: Logo scale in (0.8→1.0, 600ms) + fade-in tagline (400ms delay)
 *
 * Per master spec: background SageDeep → SageMid gradient, centered layout.
 */
@Composable
fun SplashScreen(navController: NavController) {
    val viewModel: SplashViewModel = hiltViewModel()
    // Logo scale animation: 0.8 → 1.0 with EaseOutBack feel
    val scale by rememberInfiniteTransition(label = "splash_scale").animateFloat(
        initialValue = 0.8f,
        targetValue = 1.0f,
        animationSpec = infiniteRepeatable(
            animation = tween(600, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "logo_scale"
    )

    // Tagline fade-in animation
    val taglineAlpha = remember { Animatable(0f) }
    LaunchedEffect(Unit) {
        delay(400)
        taglineAlpha.animateTo(1f, animationSpec = tween(500))
    }

    // Navigation is session-gated. A cached access token is enough to enter
    // the app; the OkHttp authenticator rotates it on the first 401. If only
    // a refresh token remains, restore it before showing the dashboard.
    LaunchedEffect(Unit) {
        delay(2000)
        val hasSession = viewModel.restoreSession()
        if (hasSession) {
            navController.navigate(Home) { popUpTo(com.agrisage.app.navigation.Splash) { inclusive = true } }
        } else {
            navController.navigate(Onboarding(step = 0)) { popUpTo(com.agrisage.app.navigation.Splash) { inclusive = true } }
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                brush = Brush.verticalGradient(
                    colors = listOf(
                        Color(0xFF1B4332), // SageDeep
                        Color(0xFF2D6A4F)  // SageMid
                    )
                )
            ),
        contentAlignment = Alignment.Center
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center,
        ) {
            // Logo leaf icon (text placeholder until SVG asset added)
            Text(
                text = "🌿",
                fontSize = 64.sp,
                modifier = Modifier.scale(scale)
            )

            Spacer(Modifier.height(16.dp))

            // App name
            Text(
                text = "Agri-SAGE",
                fontSize = 32.sp,
                fontWeight = FontWeight.Black,
                color = Color.White,
                letterSpacing = 1.sp
            )

            Spacer(Modifier.height(8.dp))

            // Tagline
            Text(
                text = "SCALABLE AGRICULTURAL GUIDANCE ENGINE",
                fontSize = 11.sp,
                color = Color.White.copy(alpha = 0.6f),
                letterSpacing = 2.sp,
                textAlign = TextAlign.Center,
                modifier = Modifier
                    .padding(horizontal = 32.dp)
                    .alpha(taglineAlpha.value)
            )

            Spacer(Modifier.height(24.dp))

            Text(
                text = "Powered by AI · Free for Farmers",
                fontSize = 13.sp,
                color = Color.White.copy(alpha = 0.8f)
            )

            Spacer(Modifier.height(48.dp))

            // Progress bar
            LinearProgressIndicator(
                modifier = Modifier.width(120.dp),
                color = Color(0xFF52B788), // SageLeaf
                trackColor = Color.White.copy(alpha = 0.2f),
            )
        }

        // Bottom version info
        Column(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .padding(bottom = 32.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "Version 1.0",
                fontSize = 11.sp,
                color = Color.White.copy(alpha = 0.4f)
            )
            Text(
                text = "Built at ASIET Kalady",
                fontSize = 11.sp,
                color = Color.White.copy(alpha = 0.4f)
            )
        }
    }
}

@Preview(showBackground = true, widthDp = 360, heightDp = 800)
@Composable
fun SplashScreenPreview() {
    SplashScreen(navController = rememberNavController())
}
