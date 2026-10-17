package com.agrisage.app.data.remote.dto

import com.google.gson.annotations.SerializedName

data class AlertDto(
    val id: String,
    @SerializedName("farmer_id") val farmerId: String,
    @SerializedName("field_id") val fieldId: String? = null,
    val severity: String,
    val title: String,
    val message: String,
    @SerializedName("source_agent") val sourceAgent: String? = null,
    @SerializedName("is_read") val isRead: Boolean = false,
    @SerializedName("created_at") val createdAt: String
)

data class MarkReadRequest(
    @SerializedName("alert_ids") val alertIds: List<String>
)

data class MarkReadResponse(
    @SerializedName("marked_count") val markedCount: Int
)
