package com.agrisage.app.ui.screens.splash

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController
import androidx.hilt.navigation.compose.hiltViewModel
import com.agrisage.app.BuildConfig
import com.agrisage.app.navigation.Screen
import com.agrisage.app.ui.screens.SplashViewModel
import com.agrisage.app.ui.theme.WireLeaf
import com.agrisage.app.ui.theme.WireSage
import com.agrisage.app.ui.theme.WireSageDeep
import com.agrisage.app.ui.theme.WireSageLight
import kotlinx.coroutines.delay

@Composable
fun SplashScreen(
    navController: NavHostController,
    viewModel: SplashViewModel = hiltViewModel()
) {
    val scale = remember { Animatable(0.5f) }
    val taglineAlpha = remember { Animatable(0f) }

    LaunchedEffect(Unit) {
        scale.animateTo(1.0f, animationSpec = tween(600, easing = FastOutSlowInEasing))
        taglineAlpha.animateTo(1.0f, animationSpec = tween(400))
        delay(1200)
        navController.navigate(Screen.Home) {
            popUpTo(Screen.Splash) { inclusive = true }
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                brush = Brush.linearGradient(
                    colors = listOf(WireSageDeep, WireSage, WireSageLight)
                )
            ),
        contentAlignment = Alignment.Center
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Text(
                text = "🌿",
                fontSize = 64.sp,
                modifier = Modifier.scale(scale.value)
            )

            Spacer(Modifier.height(16.dp))

            Text(
                text = "Agri-SAGE",
                fontSize = 32.sp,
                fontWeight = FontWeight.Black,
                color = Color.White,
                letterSpacing = 1.sp
            )

            Spacer(Modifier.height(8.dp))

            Text(
                text = "SCALABLE AGRICULTURAL GUIDANCE ENGINE",
                fontSize = 11.sp,
                color = Color.White.copy(alpha = 0.7f),
                letterSpacing = 2.sp,
                textAlign = TextAlign.Center,
                modifier = Modifier
                    .padding(horizontal = 32.dp)
                    .alpha(taglineAlpha.value)
            )

            Spacer(Modifier.height(18.dp))

            Text(
                text = "Powered by AI · Free for Farmers",
                fontSize = 12.sp,
                color = Color.White.copy(alpha = 0.6f)
            )

            Spacer(Modifier.height(36.dp))

            LinearProgressIndicator(
                modifier = Modifier.width(100.dp),
                color = WireLeaf,
                trackColor = Color.White.copy(alpha = 0.2f),
            )
        }
    }
}
