package com.agrisage.app.domain.model

data class Field(
    val id: String,
    val farmerId: String,
    val name: String,
    val areaSqM: Float,
    val latitude: Double,
    val longitude: Double,
    val soilType: String? = null,
    val irrigationType: String? = null,
    val lastNdvi: Float? = null,
    val cropName: String? = null,
    val cropVariety: String? = null,
    val sowingDate: String? = null,
    val growthStage: String? = null,
    val expectedHarvestDate: String? = null
)
