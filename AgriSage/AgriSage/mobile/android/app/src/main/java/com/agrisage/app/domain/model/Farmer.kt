package com.agrisage.app.domain.model

data class Farmer(
    val id: String,
    val phone: String,
    val name: String,
    val village: String? = null,
    val district: String? = null,
    val state: String = "Kerala",
    val preferredLanguage: String = "ml",
    val latitude: Double? = null,
    val longitude: Double? = null,
    val isActive: Boolean = true
)
