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
    @SerializedName("query") val message: String,
    val language: String = "ml",
    @SerializedName("farmer_id") val farmerId: String,
    @SerializedName("field_id") val fieldId: String? = null,
    val latitude: Double? = null,
    val longitude: Double? = null,
    @SerializedName("crop_info") val cropInfo: ChatCropInfoDto? = null,
    val state: String = "India",
    val district: String = "",
    val crops: List<String> = emptyList()
)

data class ChatResponse(
    @SerializedName("session_id") val sessionId: String = "",
    @SerializedName("answer_native") val message: String = "",
    val language: String = "en",
    @SerializedName("generation_ms") val confidence: Float = 0f,
    val alerts: List<AlertDto> = emptyList(),
    @SerializedName("agents_used") val agentsUsed: List<String> = emptyList(),
    @SerializedName("farmer_id") val farmerId: String = "",
    @SerializedName("warnings") val warnings: List<String> = emptyList()
)

data class AdvisoryRequest(
    @SerializedName("query") val question: String,
    val language: String = "en",
    @SerializedName("farmer_id") val farmerId: String,
    @SerializedName("field_id") val fieldId: String? = null,
    val state: String = "India",
    val district: String = "",
    val crops: List<String> = emptyList()
)

data class AdvisoryResponse(
    @SerializedName("answer_native") val answer: String = "",
    @SerializedName("answer_en") val answerEnglish: String = "",
    val language: String = "en",
    @SerializedName("generation_ms") val generationMs: Int = 0,
    val warnings: List<String> = emptyList(),
    @SerializedName("agents_used") val agentsUsed: List<String> = emptyList(),
    @SerializedName("farmer_id") val farmerId: String = ""
)
