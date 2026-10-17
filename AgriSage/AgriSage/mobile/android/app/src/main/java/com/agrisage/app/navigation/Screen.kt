package com.agrisage.app.navigation

import kotlinx.serialization.Serializable

sealed class Screen {
    @Serializable object Splash : Screen()
    @Serializable object Onboarding : Screen()
    @Serializable object Home : Screen()
    @Serializable object Advisor : Screen()
    @Serializable object Fields : Screen()
    @Serializable data class FieldDetail(val fieldId: String) : Screen()
    @Serializable object Weather : Screen()
    @Serializable object Alerts : Screen()
    @Serializable object Profile : Screen()
}
