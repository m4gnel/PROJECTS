package com.agrisage.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.consumeWindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawing
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.layout.windowInsetsTopHeight
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.agrisage.app.navigation.AppNavHost
import com.agrisage.app.navigation.Screen
import com.agrisage.app.ui.components.BottomNavBar
import com.agrisage.app.ui.components.ReferenceSystemBars
import com.agrisage.app.ui.theme.AgriSageTheme
import com.agrisage.app.ui.theme.WireSageDeep
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            AgriSageTheme {
                val navController = rememberNavController()
                val currentBackStackEntry by navController.currentBackStackEntryAsState()
                val currentRoute = currentBackStackEntry?.destination?.route
                val darkHeader = currentRoute in listOf(
                    Screen.Advisor::class.qualifiedName,
                    Screen.Profile::class.qualifiedName,
                    Screen.Splash::class.qualifiedName,
                )
                ReferenceSystemBars(darkStatusBarIcons = !darkHeader)
                val headerColor = when {
                    darkHeader -> WireSageDeep
                    currentRoute == Screen.Weather::class.qualifiedName -> Color(0xFFF8F2E8)
                    else -> Color.White
                }
                Box(Modifier.fillMaxSize()) {
                Scaffold(
                    containerColor = Color.White,
                    contentWindowInsets = WindowInsets.safeDrawing,
                    bottomBar = {
                        // Show bottom bar only on main screens
                        val showBottomBar = currentRoute?.let { route ->
                            val simple = route.substringAfterLast('.')
                            simple in listOf("Home", "Fields", "Weather", "Advisor", "Profile")
                        } ?: false
                        if (showBottomBar || BuildConfig.REFERENCE_PREVIEW) {
                        Column(Modifier.imePadding()) {
                            if (BuildConfig.REFERENCE_PREVIEW) {
                                Text(
                                    "REFERENCE PREVIEW · SAMPLE DATA",
                                    modifier = Modifier.fillMaxWidth()
                                        .background(Color(0xFFFFF1CC))
                                        .then(if (showBottomBar) Modifier else Modifier.navigationBarsPadding())
                                        .padding(4.dp),
                                    color = Color(0xFF594400),
                                    fontSize = 10.sp,
                                    textAlign = TextAlign.Center,
                                )
                            }
                            if (showBottomBar) {
                                BottomNavBar(
                                    currentRoute = currentRoute ?: "",
                                    onNavigate = { screen ->
                                        navController.navigate(screen) {
                                            popUpTo(navController.graph.findStartDestination().id) {
                                                saveState = true
                                            }
                                            launchSingleTop = true
                                            restoreState = true
                                        }
                                    }
                                )
                            }
                        }
                        }
                    }
                ) { innerPadding ->
                    AppNavHost(
                        navController = navController,
                        modifier = Modifier.padding(innerPadding).consumeWindowInsets(innerPadding)
                    )
                }
                // Paint only the status-bar strip. The gesture/navigation area
                // stays white, including full-screen Advisor and detail routes.
                Spacer(Modifier.fillMaxWidth().windowInsetsTopHeight(WindowInsets.statusBars).background(headerColor))
                }
            }
        }
    }
}
