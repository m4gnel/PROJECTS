package com.agrisage.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.agrisage.app.ui.theme.SageDeep
import com.agrisage.app.ui.theme.SageMid

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
 * - 1:1 active emerald tint (#16A34A / SageDeep) and tactile feedback
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

    Surface(
        color = Color.White,
        shadowElevation = 8.dp,
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .navigationBarsPadding()
                .padding(vertical = 8.dp),
            horizontalArrangement = Arrangement.SpaceAround,
            verticalAlignment = Alignment.CenterVertically
        ) {
            items.forEach { item ->
                val isSelected = currentRoute == item.route ||
                        (item.route == AgriNavRoutes.FARM && (currentRoute == "fields" || currentRoute == "farm"))

                val activeColor = Color(0xFF16A34A)
                val inactiveColor = Color(0xFF94A3B8)

                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier
                        .tactilePress(scaleDown = 0.90f) {
                            if (!isSelected) {
                                onNavigate(item.route)
                            }
                        }
                        .padding(horizontal = 12.dp, vertical = 4.dp)
                ) {
                    if (isSelected) {
                        Box(
                            modifier = Modifier
                                .size(36.dp)
                                .clip(CircleShape)
                                .background(Color(0xFFDCFCE7)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = item.icon,
                                contentDescription = item.title,
                                tint = activeColor,
                                modifier = Modifier.size(20.dp)
                            )
                        }
                    } else {
                        Box(
                            modifier = Modifier.size(36.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = item.icon,
                                contentDescription = item.title,
                                tint = inactiveColor,
                                modifier = Modifier.size(20.dp)
                            )
                        }
                    }

                    Spacer(Modifier.height(3.dp))

                    Text(
                        text = item.title,
                        fontSize = 11.sp,
                        fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium,
                        color = if (isSelected) activeColor else inactiveColor
                    )
                }
            }
        }
    }
}
