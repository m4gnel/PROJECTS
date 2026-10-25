package com.agrisage.app.ui.components

import android.app.Activity
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

@Composable
fun ReferenceSystemBars(
    darkStatusBarIcons: Boolean = true,
    darkNavigationBarIcons: Boolean = true,
) {
    val view = LocalView.current
    SideEffect {
        val window = (view.context as? Activity)?.window ?: return@SideEffect
        // Edge-to-edge backgrounds are drawn by the root Scaffold, not the
        // deprecated Window color setters (ignored by recent Android versions).
        val controller = WindowCompat.getInsetsController(window, view)
        controller.isAppearanceLightStatusBars = darkStatusBarIcons
        controller.isAppearanceLightNavigationBars = darkNavigationBarIcons
    }
}
