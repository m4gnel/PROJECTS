package com.agrisage.app.data.remote.dto

import com.google.gson.annotations.SerializedName

data class ActiveCropDto(
    val id: String? = null,
    @SerializedName("crop_name") val cropName: String,
    val variety: String? = null,
    @SerializedName("sowing_date") val sowingDate: String,
    @SerializedName("growth_stage") val growthStage: String? = null,
    @SerializedName("expected_harvest_date") val expectedHarvestDate: String? = null
)

data class FieldDto(
    val id: String,
    @SerializedName("farmer_id") val farmerId: String,
    val name: String,
    @SerializedName("area_sq_m") val areaSqM: Float,
    val latitude: Double,
    val longitude: Double,
    @SerializedName("soil_type") val soilType: String? = null,
    @SerializedName("irrigation_type") val irrigationType: String? = null,
    @SerializedName("last_ndvi") val lastNdvi: Float? = null,
    @SerializedName("active_crop") val activeCrop: ActiveCropDto? = null,
    @SerializedName("created_at") val createdAt: String? = null,
    @SerializedName("updated_at") val updatedAt: String? = null
)

data class CreateFieldRequest(
    val name: String,
    @SerializedName("area_sq_m") val areaSqM: Float,
    val latitude: Double,
    val longitude: Double,
    @SerializedName("soil_type") val soilType: String? = null,
    @SerializedName("irrigation_type") val irrigationType: String? = null,
    @SerializedName("crop_name") val cropName: String? = null,
    @SerializedName("crop_variety") val cropVariety: String? = null,
    @SerializedName("sowing_date") val sowingDate: String? = null
)
