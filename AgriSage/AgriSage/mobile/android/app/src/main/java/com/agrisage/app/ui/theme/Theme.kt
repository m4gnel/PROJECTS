package com.agrisage.app.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable

private val LightColorScheme = lightColorScheme(
    primary = ColorPrimary,
    onPrimary = ColorOnPrimary,
    primaryContainer = ColorPrimaryContainer,
    secondary = ColorSecondary,
    surface = ColorSurface,
    onSurface = ColorOnSurface,
    surfaceVariant = ColorSurfaceVariant,
    outline = ColorOutline
)

private val DarkColorScheme = darkColorScheme(
    primary = ColorPrimaryLight,
    onPrimary = ColorPrimaryDark,
    primaryContainer = ColorPrimaryDark,
    secondary = ColorSecondaryLight,
    surface = ColorOnSurface,
    onSurface = ColorSurface,
    surfaceVariant = ColorOnSurfaceSecondary,
    outline = ColorOutline
)

@Composable
fun AgriSAGETheme(
    darkTheme: Boolean = false,
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}

@Composable
fun AgriSageTheme(
    darkTheme: Boolean = false,
    content: @Composable () -> Unit
) = AgriSAGETheme(darkTheme = darkTheme, content = content)
