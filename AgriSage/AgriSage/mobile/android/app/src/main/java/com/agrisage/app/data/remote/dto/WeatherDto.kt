package com.agrisage.app.data.remote.dto

import com.google.gson.annotations.SerializedName

data class WeatherCurrentDto(
    val latitude: Double,
    val longitude: Double,
    @SerializedName("temperature_c") val temperatureC: Float,
    @SerializedName("humidity_percent") val humidityPercent: Int,
    @SerializedName("rainfall_mm") val rainfallMm: Float,
    @SerializedName("wind_kmh") val windKmh: Float,
    @SerializedName("uv_index") val uvIndex: Float? = null,
    @SerializedName("weather_condition") val weatherCondition: String,
    @SerializedName("agri_advisory") val agriAdvisory: String? = null,
    @SerializedName("fetched_at") val fetchedAt: String
)

data class WeatherForecastDto(
    val latitude: Double,
    val longitude: Double,
    val forecast: List<WeatherForecastItemDto>,
    @SerializedName("fetched_at") val fetchedAt: String
)

data class WeatherForecastItemDto(
    val date: String,
    @SerializedName("max_temp_c") val maxTempC: Float,
    @SerializedName("min_temp_c") val minTempC: Float,
    @SerializedName("rainfall_mm") val rainfallMm: Float,
    @SerializedName("weather_condition") val weatherCondition: String,
    @SerializedName("uv_index") val uvIndex: Float? = null,
    @SerializedName("agri_note") val agriNote: String? = null
)
