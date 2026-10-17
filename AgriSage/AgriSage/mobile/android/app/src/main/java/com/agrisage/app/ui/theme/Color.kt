package com.agrisage.app.ui.theme

import androidx.compose.ui.graphics.Color

// Design Tokens (ONLY these colors from 00_MASTER_RULES.md)
val SageGreen900 = Color(0xFF1B4332)
val SageGreen700 = Color(0xFF2D6A4F)
val SageGreen500 = Color(0xFF40916C)
val SageGreen300 = Color(0xFF52B788)
val SoilBrown    = Color(0xFF7C4D26)
val AlertRed     = Color(0xFFD62828)
val AlertGold    = Color(0xFFF4A261)
val AlertBlue    = Color(0xFF4361EE)
val AlertGreen   = Color(0xFF2DC653)
val Surface      = Color(0xFFFFFFFF)
val SurfaceDim   = Color(0xFFF5F5F5)
val OnSurface    = Color(0xFF1C1B1F)
val OnSurfaceVar = Color(0xFF49454F)

// Legacy aliases mapping to spec tokens
val ColorPrimary = SageGreen700
val ColorPrimaryDark = SageGreen900
val ColorPrimaryLight = SageGreen300
val ColorPrimaryContainer = SageGreen300
val ColorSecondary = SageGreen500
val ColorSecondaryLight = SurfaceDim
val ColorRiskCritical = AlertRed
val ColorRiskHigh = AlertGold
val ColorRiskMedium = AlertGold
val ColorRiskLow = AlertGreen
val ColorConfidenceConfirmed = SageGreen900
val ColorConfidenceLikely = SageGreen700
val ColorConfidencePossible = AlertGold
val ColorConfidenceUncertain = AlertRed
val ColorConfidenceInsufficient = OnSurfaceVar
val ColorSurface = Surface
val ColorSurfaceVariant = SurfaceDim
val ColorOnSurface = OnSurface
val ColorOnSurfaceSecondary = OnSurfaceVar
val ColorOnSurfaceTertiary = OnSurfaceVar
val ColorOutline = OnSurfaceVar
val ColorWarningBg = AlertGold.copy(alpha = 0.2f)
val ColorWarningText = SoilBrown
val ColorInfoBg = AlertBlue.copy(alpha = 0.2f)
val ColorOfflineBanner = AlertGold.copy(alpha = 0.2f)
val ColorOfflineText = SoilBrown
val ColorCachedLabel = SoilBrown
val ColorSchemeBg = SurfaceDim
val ColorSchemeText = SageGreen900
val ColorOnPrimary = Surface

val SageDeep = SageGreen900
val SageMid = SageGreen700
val SageLeaf = SageGreen500
val DarkText = OnSurface
val LightBg = Surface

// Master UI/UX Wireframe & Build System exact tokens
val WireSage = Color(0xFF2D6A4F)
val WireSageLight = Color(0xFF40916C)
val WireSageDeep = Color(0xFF1B4332)
val WireLeaf = Color(0xFF52B788)
val WireLeafPale = Color(0xFFD8F3DC)
val WireSoil = Color(0xFF7C4D26)
val WireSoilLight = Color(0xFFA0622F)
val WireSoilPale = Color(0xFFF4EAD8)
val WireGold = Color(0xFFF4A024)
val WireGoldPale = Color(0xFFFFF3D6)
val WireSky = Color(0xFF1E96D0)
val WireSkyPale = Color(0xFFE0F4FF)
val WireAlert = Color(0xFFE63946)
val WireAlertPale = Color(0xFFFFE8EA)
val WireWhite = Color(0xFFFAFDF8)
val WireSurface = Color(0xFFF2F8F3)
val WireSurface2 = Color(0xFFE8F5EB)
val WireBorder = Color(0xFFC3DEC9)
val WireTextPrimary = Color(0xFF0F2419)
val WireTextSecondary = Color(0xFF3D6B4A)
val WireTextMuted = Color(0xFF6B8F72)
