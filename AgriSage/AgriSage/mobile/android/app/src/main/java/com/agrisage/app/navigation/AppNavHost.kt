package com.agrisage.app.navigation
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.toRoute
import com.agrisage.app.ui.screens.splash.SplashScreen
import com.agrisage.app.ui.screens.onboarding.OnboardingScreen
import com.agrisage.app.ui.screens.home.HomeScreen
import com.agrisage.app.ui.screens.advisor.AdvisorScreen
import com.agrisage.app.ui.screens.fields.FieldsScreen
import com.agrisage.app.ui.screens.fields.FieldDetailScreen
import com.agrisage.app.ui.screens.weather.WeatherScreen
import com.agrisage.app.ui.screens.alerts.AlertsScreen
import com.agrisage.app.ui.screens.profile.ProfileScreen

@Composable
fun AppNavHost(
    navController: NavHostController,
    modifier: Modifier = Modifier
) {
    NavHost(
        navController = navController,
        startDestination = Screen.Splash,
        modifier = modifier
    ) {
        composable<Screen.Splash> { SplashScreen(navController) }
        composable<Screen.Onboarding> { OnboardingScreen(navController) }
        composable<Screen.Home> { HomeScreen(navController) }
        composable<Screen.Advisor> { AdvisorScreen(navController) }
        composable<Screen.Fields> { FieldsScreen(navController) }
        composable<Screen.FieldDetail> { backStackEntry ->
            val args = backStackEntry.toRoute<Screen.FieldDetail>()
            FieldDetailScreen(navController, fieldId = args.fieldId)
        }
        composable<Screen.Weather> { WeatherScreen(navController) }
        composable<Screen.Alerts> { AlertsScreen(navController) }
        composable<Screen.Profile> { ProfileScreen(navController) }
    }
}
