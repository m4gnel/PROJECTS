package com.agrisage.app.ui.components

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Home
import androidx.compose.material.icons.rounded.Landscape
import androidx.compose.material.icons.rounded.Person
import androidx.compose.material.icons.rounded.SmartToy
import androidx.compose.material.icons.rounded.WbSunny
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import com.agrisage.app.navigation.Screen
import com.agrisage.app.ui.theme.SageGreen300
import com.agrisage.app.ui.theme.SageGreen700
import com.agrisage.app.ui.theme.SageGreen900

data class BottomNavItem(val screen: Screen, val icon: ImageVector, val label: String)

@Composable
fun BottomNavBar(
    currentRoute: String,
    onNavigate: (Screen) -> Unit
) {
    NavigationBar(containerColor = SageGreen900) {
        val items = listOf(
            BottomNavItem(Screen.Home, Icons.Rounded.Home, "Home"),
            BottomNavItem(Screen.Advisor, Icons.Rounded.SmartToy, "Advisor"),
            BottomNavItem(Screen.Fields, Icons.Rounded.Landscape, "Fields"),
            BottomNavItem(Screen.Weather, Icons.Rounded.WbSunny, "Weather"),
            BottomNavItem(Screen.Profile, Icons.Rounded.Person, "Profile")
        )
        items.forEach { item ->
            NavigationBarItem(
                selected = currentRoute == item.screen::class.simpleName || currentRoute == item.screen::class.qualifiedName,
                onClick = { onNavigate(item.screen) },
                icon = { Icon(item.icon, contentDescription = item.label) },
                label = { Text(item.label, style = MaterialTheme.typography.labelSmall) },
                colors = NavigationBarItemDefaults.colors(
                    selectedIconColor = SageGreen300,
                    unselectedIconColor = Color.White.copy(alpha = 0.6f),
                    indicatorColor = SageGreen700
                )
            )
        }
    }
}
