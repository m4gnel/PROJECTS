package com.agrisage.app.data.remote.dto

import com.google.gson.annotations.SerializedName

data class WeatherCurrentDto(
    val location: WeatherLocationDto? = null,
    @SerializedName("temp_c") val temperatureC: Float = 0f,
    @SerializedName("humidity_pct") val humidityPercent: Int = 0,
    @SerializedName("rain_mm_24h") val rainfallMm: Float = 0f,
    @SerializedName("wind_kmh") val windKmh: Float = 0f,
    @SerializedName("uv_index") val uvIndex: Float? = null,
    @SerializedName("advice_flag") val weatherCondition: String = "NORMAL",
    @SerializedName("farming_advisory") val agriAdvisory: String? = null,
    @SerializedName("stale") val stale: Boolean = false,
    @SerializedName("cached") val cached: Boolean = false
) {
    val latitude: Double get() = location?.lat ?: 0.0
    val longitude: Double get() = location?.lon ?: location?.lng ?: 0.0
}

data class WeatherLocationDto(
    val lat: Double? = null,
    val lon: Double? = null,
    val lng: Double? = null,
    val district: String? = null,
    val state: String? = null
)

typealias WeatherForecastDto = List<WeatherForecastItemDto>

data class WeatherForecastItemDto(
    val date: String = "",
    @SerializedName("temp_max_c") val maxTempC: Float = 0f,
    @SerializedName("temp_min_c") val minTempC: Float = 0f,
    @SerializedName("rain_mm") val rainfallMm: Float = 0f,
    @SerializedName("condition") val weatherCondition: String = "Cloudy",
    @SerializedName("uv_index") val uvIndex: Float? = null,
    @SerializedName("farming_tip") val agriNote: String? = null
)
