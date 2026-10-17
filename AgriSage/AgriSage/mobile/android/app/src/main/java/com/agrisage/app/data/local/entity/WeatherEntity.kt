package com.agrisage.app.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "weather_cache")
data class WeatherEntity(
    @PrimaryKey val id: String,
    val lat: Double,
    val lon: Double,
    val tempCelsius: Float,
    val humidity: Int,
    val rainfallMm: Float,
    val windKmh: Float,
    val condition: String,
    val fetchedAt: Long
)
