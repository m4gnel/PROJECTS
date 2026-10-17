package com.agrisage.app.data.remote.dto

import com.google.gson.annotations.SerializedName

data class RegisterRequest(
    val phone: String,
    val name: String,
    val password: String,
    val village: String? = null,
    val district: String? = null,
    @SerializedName("preferred_language") val preferredLanguage: String = "ml",
    val latitude: Double? = null,
    val longitude: Double? = null
)

data class TokenResponse(
    @SerializedName("access_token") val accessToken: String,
    @SerializedName("token_type") val tokenType: String,
    @SerializedName("expires_in") val expiresIn: Int,
    @SerializedName("farmer_id") val farmerId: String
)

data class FarmerDto(
    val id: String,
    val phone: String,
    val name: String,
    val village: String? = null,
    val district: String? = null,
    val state: String = "Kerala",
    @SerializedName("preferred_language") val preferredLanguage: String = "ml",
    val latitude: Double? = null,
    val longitude: Double? = null,
    @SerializedName("is_active") val isActive: Boolean = true,
    @SerializedName("created_at") val createdAt: String? = null,
    @SerializedName("updated_at") val updatedAt: String? = null
)

data class UpdateFarmerRequest(
    val name: String,
    val village: String? = null,
    val district: String? = null,
    @SerializedName("preferred_language") val preferredLanguage: String = "ml",
    val latitude: Double? = null,
    val longitude: Double? = null
)
