package com.agrisage.app.domain.model

data class Weather(
    val latitude: Double,
    val longitude: Double,
    val temperatureC: Float,
    val humidityPercent: Int,
    val rainfallMm: Float,
    val windKmh: Float,
    val uvIndex: Float? = null,
    val weatherCondition: String,
    val agriAdvisory: String? = null,
    val fetchedAt: String
)

data class ForecastDay(
    val date: String,
    val maxTempC: Float,
    val minTempC: Float,
    val rainfallMm: Float,
    val condition: String,
    val uvIndex: Float? = null,
    val agriNote: String? = null
)
