package com.agrisage.app.data.remote.dto

import com.google.gson.annotations.SerializedName

data class ChatCropInfoDto(
    @SerializedName("crop_name") val cropName: String,
    val variety: String? = null,
    @SerializedName("sowing_date") val sowingDate: String? = null,
    @SerializedName("current_growth_stage") val currentGrowthStage: String? = null,
    @SerializedName("field_area_hectares") val fieldAreaHectares: Float? = null
)

data class ChatRequest(
    @SerializedName("session_id") val sessionId: String? = null,
    val message: String,
    val language: String = "ml",
    @SerializedName("farmer_id") val farmerId: String,
    @SerializedName("field_id") val fieldId: String? = null,
    val latitude: Double? = null,
    val longitude: Double? = null,
    @SerializedName("crop_info") val cropInfo: ChatCropInfoDto? = null
)

data class ChatResponse(
    @SerializedName("session_id") val sessionId: String,
    val message: String,
    val language: String,
    val confidence: Float,
    val alerts: List<AlertDto> = emptyList(),
    @SerializedName("agents_used") val agentsUsed: List<String> = emptyList(),
    @SerializedName("created_at") val createdAt: String
)

data class AdvisoryRequest(
    val question: String,
    val language: String = "en",
    @SerializedName("farmer_id") val farmerId: String,
    @SerializedName("field_id") val fieldId: String? = null
)

data class AdvisoryResponse(
    val question: String,
    val answer: String,
    val language: String,
    val confidence: Float,
    val sources: List<String> = emptyList(),
    @SerializedName("agents_used") val agentsUsed: List<String> = emptyList(),
    @SerializedName("created_at") val createdAt: String
)
