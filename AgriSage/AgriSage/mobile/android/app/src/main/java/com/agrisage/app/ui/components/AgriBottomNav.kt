package com.agrisage.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

// Navigation route constants used by AgriBottomNav
object AgriNavRoutes {
    const val HOME = "home"
    const val FARM = "fields"
    const val FIELDS = "fields"
    const val WEATHER = "weather"
    const val ADVISOR = "advisor"
    const val PROFILE = "profile"
}

data class BottomNavTabItem(
    val route: String,
    val title: String,
    val icon: ImageVector
)

/**
 * Bottom Navigation Bar replicated from Reference Reel 2 (DailyFlutterUI Farm App).
 * Features:
 * - Tab 1: Home (House icon)
 * - Tab 2: Farm (Eco/Sprout in circle icon - exact match to Reel 2)
 * - Tab 3: Weather (Sun icon)
 * - Tab 4: Advisor (Smart Toy icon)
 * - Tab 5: Profile (Person icon)
 * - Token-driven active tint, selected container, and tactile feedback
 */
@Composable
fun AgriBottomNav(
    currentRoute: String?,
    onNavigate: (String) -> Unit
) {
    val items = listOf(
        BottomNavTabItem(AgriNavRoutes.HOME, "Home", Icons.Default.Home),
        BottomNavTabItem(AgriNavRoutes.FARM, "Farm", Icons.Default.Eco),
        BottomNavTabItem(AgriNavRoutes.WEATHER, "Weather", Icons.Default.WbSunny),
        BottomNavTabItem(AgriNavRoutes.ADVISOR, "Advisor", Icons.Default.SmartToy),
        BottomNavTabItem(AgriNavRoutes.PROFILE, "Profile", Icons.Default.Person)
    )
    val colorScheme = MaterialTheme.colorScheme

    Surface(
        color = colorScheme.surface,
        contentColor = colorScheme.onSurface,
        tonalElevation = 3.dp,
        shadowElevation = 8.dp,
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .navigationBarsPadding()
                .padding(horizontal = 8.dp, vertical = 4.dp),
            horizontalArrangement = Arrangement.SpaceEvenly,
            verticalAlignment = Alignment.CenterVertically
        ) {
            items.forEach { item ->
                val isSelected = currentRoute == item.route ||
                        (item.route == AgriNavRoutes.FARM && (currentRoute == "fields" || currentRoute == "farm"))

                val activeColor = colorScheme.primary
                val inactiveColor = colorScheme.onSurfaceVariant
                val selectedContainer = colorScheme.primaryContainer

                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier
                        .defaultMinSize(minWidth = 64.dp, minHeight = 48.dp)
                        .semantics(mergeDescendants = true) {
                            contentDescription = "${item.title} tab"
                            role = Role.Button
                        }
                        .tactilePress(
                            scaleDown = 0.96f,
                            onClickLabel = "Open ${item.title} tab"
                        ) {
                            if (!isSelected) {
                                onNavigate(item.route)
                            }
                        }
                        .padding(horizontal = 4.dp, vertical = 4.dp)
                ) {
                    Box(
                        modifier = Modifier
                            .size(36.dp)
                            .clip(RoundedCornerShape(14.dp))
                            .then(
                                if (isSelected) {
                                    Modifier
                                        .background(selectedContainer)
                                        .border(
                                            width = 1.dp,
                                            color = activeColor.copy(alpha = 0.2f),
                                            shape = RoundedCornerShape(14.dp)
                                        )
                                } else {
                                    Modifier
                                }
                            ),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = item.icon,
                            contentDescription = null,
                            tint = if (isSelected) activeColor else inactiveColor,
                            modifier = Modifier.size(20.dp)
                        )
                    }

                    Spacer(Modifier.height(3.dp))

                    Text(
                        text = item.title,
                        fontSize = 11.sp,
                        fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium,
                        color = if (isSelected) activeColor else inactiveColor,
                        maxLines = 1
                    )
                }
            }
        }
    }
}
