package com.agrisage.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Eco
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.SmartToy
import androidx.compose.material.icons.filled.WbSunny
import androidx.compose.material3.Icon
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.agrisage.app.navigation.Screen

private val BottomBarGreen = Color(0xFF16A34A)
private val BottomBarText = Color(0xFF64748B)

data class BottomNavItem(val screen: Screen, val icon: ImageVector, val label: String)

/**
 * The single app-level bottom navigation surface. MainActivity owns its
 * visibility, so screens must not render another bottom bar of their own.
 */
@Composable
fun BottomNavBar(
    currentRoute: String,
    onNavigate: (Screen) -> Unit
) {
    val items = listOf(
        BottomNavItem(Screen.Home, Icons.Default.Home, "Home"),
        BottomNavItem(Screen.Fields, Icons.Default.Eco, "Farm"),
        BottomNavItem(Screen.Weather, Icons.Default.WbSunny, "Weather"),
        BottomNavItem(Screen.Advisor, Icons.Default.SmartToy, "Advisor"),
        BottomNavItem(Screen.Profile, Icons.Default.Person, "Profile")
    )

    Surface(
        color = Color.White,
        contentColor = BottomBarText,
        shadowElevation = 8.dp,
        tonalElevation = 1.dp,
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .navigationBarsPadding()
                .padding(horizontal = 6.dp, vertical = 4.dp),
            horizontalArrangement = Arrangement.SpaceEvenly,
            verticalAlignment = Alignment.CenterVertically
        ) {
            items.forEach { item ->
                val selected = currentRoute.matches(item.screen)
                BottomNavItemView(
                    item = item,
                    selected = selected,
                    onClick = { if (!selected) onNavigate(item.screen) },
                    modifier = Modifier.weight(1f)
                )
            }
        }
    }
}

@Composable
private fun BottomNavItemView(
    item: BottomNavItem,
    selected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .defaultMinSize(minHeight = 64.dp)
            .semantics(mergeDescendants = true) {
                contentDescription = "${item.label} tab"
                role = Role.Button
            }
            .tactilePress(
                scaleDown = 0.96f,
                onClickLabel = "Open ${item.label} tab",
                onClick = onClick
            )
            .padding(horizontal = 2.dp, vertical = 2.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Box(
            modifier = Modifier
                .size(36.dp)
                .clip(CircleShape)
                .then(
                    if (selected) {
                        Modifier.background(BottomBarGreen)
                    } else {
                        Modifier
                    }
                ),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = item.icon,
                contentDescription = null,
                tint = if (selected) Color.White else BottomBarText,
                modifier = Modifier.size(20.dp)
            )
        }

        Text(
            text = item.label,
            color = if (selected) BottomBarGreen else BottomBarText,
            fontSize = 11.sp,
            fontWeight = if (selected) FontWeight.Bold else FontWeight.Medium,
            maxLines = 1
        )
    }
}

private fun String.matches(screen: Screen): Boolean {
    val simpleName = screen::class.simpleName ?: return false
    val qualifiedName = screen::class.qualifiedName
    return this == simpleName ||
        this == qualifiedName ||
        substringAfterLast('.') == simpleName
}
