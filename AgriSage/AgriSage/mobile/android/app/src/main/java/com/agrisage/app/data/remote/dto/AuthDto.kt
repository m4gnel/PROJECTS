package com.agrisage.app.data.remote.dto

import com.google.gson.annotations.SerializedName

data class SendOtpRequest(
    val phone: String
)

data class RefreshTokenRequest(
    @SerializedName("refresh_token") val refreshToken: String,
)

data class SendOtpResponse(
    val message: String,
    @SerializedName("expires_in") val expiresIn: Int
)

data class VerifyOtpRequest(
    val phone: String,
    val otp: String,
    val name: String? = null
)

data class ApiUser(
    val id: String,
    val phone: String,
    val name: String? = null,
    val language: String = "ml",
    @SerializedName("subscription_tier") val subscriptionTier: String = "free",
    val role: String = "farmer",
    val permissions: List<String> = emptyList()
)

data class AuthResponse(
    @SerializedName("access_token") val accessToken: String,
    @SerializedName("refresh_token") val refreshToken: String? = null,
    val user: ApiUser? = null
)

data class LogoutResponse(
    val message: String? = null
)

data class FarmerDto(
    val id: String,
    val phone: String,
    val name: String,
    val village: String? = null,
    val district: String? = null,
    val state: String = "India",
    @SerializedName("preferred_language") val preferredLanguage: String = "ml",
    val latitude: Double? = null,
    val longitude: Double? = null,
    @SerializedName("is_active") val isActive: Boolean = true,
    @SerializedName("created_at") val createdAt: String? = null,
    @SerializedName("updated_at") val updatedAt: String? = null
)

data class UpdateFarmerRequest(
    val name: String? = null,
    val district: String? = null,
    val state: String? = null,
    @SerializedName("preferred_language") val preferredLanguage: String = "ml",
    val latitude: Double? = null,
    val longitude: Double? = null
)

data class SyncUploadRequest(
    val observations: List<Map<String, Any?>>,
    @SerializedName("device_id") val deviceId: String,
)

data class SyncUploadResponse(
    val status: String? = null,
    @SerializedName("processed_count") val processedCount: Int = 0,
    // Must be emitted by the server only after durable storage, not validation.
    @SerializedName("persisted_ids") val persistedIds: List<String>? = null,
) {
    fun confirmsPersistedObservation(id: String): Boolean =
        id.isNotBlank() && status == "success" && processedCount == 1 &&
            persistedIds == listOf(id)
}
