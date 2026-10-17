package com.agrisage.app.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import kotlinx.serialization.Serializable

@Serializable object HomeRoute
@Serializable object CameraRoute
@Serializable data class AdvisoryRoute(val advisoryId: String)
@Serializable data class ContextFormRoute(val imagePath: String)
@Serializable object FarmRoute
@Serializable object AlertsRoute
@Serializable object ProfileRoute
@Serializable object OnboardingRoute
@Serializable object LanguageSelectionRoute
@Serializable object OtpRoute
@Serializable object FarmSetupRoute
@Serializable object SchemeRoute

@Composable
fun AgriSAGENavGraph(
    navController: NavHostController,
    startDestination: Any = OnboardingRoute
) {
    NavHost(
        navController = navController,
        startDestination = startDestination
    ) {
        composable<OnboardingRoute> {
            // Placeholder composables rendered inside NavHost
        }
        composable<HomeRoute> {
        }
        composable<CameraRoute> {
        }
        composable<AdvisoryRoute> {
        }
        composable<ContextFormRoute> {
        }
        composable<FarmRoute> {
        }
        composable<AlertsRoute> {
        }
        composable<ProfileRoute> {
        }
        composable<LanguageSelectionRoute> {
        }
        composable<OtpRoute> {
        }
        composable<FarmSetupRoute> {
        }
        composable<SchemeRoute> {
        }
    }
}
