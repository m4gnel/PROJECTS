package com.agrisage.app.navigation

import androidx.compose.runtime.Composable
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.toRoute
import com.agrisage.app.ui.screens.AdvisorScreen
import com.agrisage.app.ui.screens.AdvisoryResultScreen
import com.agrisage.app.ui.screens.AdvisoryResultViewModel
import com.agrisage.app.ui.screens.AlertsScreen
import com.agrisage.app.ui.screens.CameraScreen
import com.agrisage.app.ui.screens.CameraViewModel
import com.agrisage.app.ui.screens.FieldsScreen
import com.agrisage.app.ui.screens.HomeScreen
import com.agrisage.app.ui.screens.OnboardingScreen
import com.agrisage.app.ui.screens.ProfileScreen
import com.agrisage.app.ui.screens.SplashScreen
import com.agrisage.app.ui.screens.WeatherScreen

/**
 * AgriSage Navigation Graph.
 * All 11 screens wired with type-safe routes (Navigation Compose 2.8.5).
 */
@Composable
fun AgriSageNavGraph(navController: NavHostController) {
    NavHost(
        navController = navController,
        startDestination = Splash,
    ) {
        // ── Splash ──────────────────────────────────────────────────
        composable<Splash> {
            SplashScreen(navController = navController)
        }

        // ── Onboarding (3 steps) ────────────────────────────────────
        composable<Onboarding> { backStackEntry ->
            val route = backStackEntry.toRoute<Onboarding>()
            OnboardingScreen(
                navController = navController,
                step = route.step,
            )
        }

        // ── Home Dashboard ──────────────────────────────────────────
        composable<Home> {
            HomeScreen(
                onNavigateToAdvisor = { navController.navigate(Advisor) },
                onNavigateToCamera = { navController.navigate(Camera) },
                onNavigateToWeather = { navController.navigate(Weather) },
                onNavigateToFields = { navController.navigate(Fields) },
                onNavigateToAlerts = { navController.navigate(Alerts) },
                onNavigateToProfile = { navController.navigate(Profile) },
                onNavigateToMarket = { navController.navigate(Market) }
            )
        }

        // ── Market Prices ───────────────────────────────────────────
        composable<Market> {
            com.agrisage.app.ui.screens.MarketScreen(navController = navController)
        }

        // ── AI Advisor Chat ─────────────────────────────────────────
        composable<Advisor> {
            AdvisorScreen(navController = navController)
        }

        // ── My Fields ───────────────────────────────────────────────
        composable<Fields> {
            FieldsScreen(navController = navController)
        }

        // ── Field Detail ─────────────────────────────────────────────
        composable<FieldDetail> {
            FieldsScreen(navController = navController)
        }

        // ── Weather & Forecast ──────────────────────────────────────
        composable<Weather> {
            WeatherScreen(navController = navController)
        }

        // ── Alerts ──────────────────────────────────────────────────
        composable<Alerts> {
            AlertsScreen(navController = navController)
        }

        // ── Profile & Settings ──────────────────────────────────────
        composable<Profile> {
            ProfileScreen(
                navController = navController,
                onNavigateBack = { navController.popBackStack() },
                onEditProfile = { navController.navigate(Profile) }
            )
        }

        // ── Camera ──────────────────────────────────────────────────
        composable<Camera> {
            val cameraViewModel: CameraViewModel = hiltViewModel()
            CameraScreen(
                viewModel = cameraViewModel,
                onNavigateBack = { navController.popBackStack() },
                onPhotoCaptured = { imagePath ->
                    navController.navigate(AdvisoryResult(advisoryId = imagePath))
                }
            )
        }

        // ── Advisory Result ─────────────────────────────────────────
        composable<AdvisoryResult> { backStackEntry ->
            val route = backStackEntry.toRoute<AdvisoryResult>()
            val resultViewModel: AdvisoryResultViewModel = hiltViewModel()
            AdvisoryResultScreen(
                advisoryId = route.advisoryId,
                viewModel = resultViewModel,
                onNavigateBack = { navController.popBackStack() }
            )
        }
    }
}
