package com.agrisage.app.navigation

import kotlinx.serialization.Serializable

/**
 * Type-safe navigation routes for AgriSage using Navigation Compose 2.8.5.
 * Uses @Serializable objects/data classes for compile-time safety.
 *
 * Graph: Splash → Onboarding(step=0,1,2) → Home → [Advisor|Fields|FieldDetail|Weather|Alerts|Profile|Camera|AdvisoryResult]
 */

@Serializable
object Splash

@Serializable
data class Onboarding(val step: Int = 0)

@Serializable
object Home

@Serializable
object Advisor

@Serializable
object Fields

@Serializable
data class FieldDetail(val fieldId: String)

@Serializable
object Weather

@Serializable
object Alerts

@Serializable
object Profile

@Serializable
object Camera

@Serializable
data class AdvisoryResult(val advisoryId: String = "")

@Serializable
object Market
