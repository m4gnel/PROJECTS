package com.agrisage.app

import com.agrisage.app.data.local.entity.WeatherEntity
import com.agrisage.app.data.remote.dto.WeatherCurrentDto
import org.junit.Assert.assertEquals
import org.junit.Test

class RepositoryTest {

    @Test
    fun testWeatherEntityMapping() {
        val dto = WeatherCurrentDto(
            latitude = 10.165,
            longitude = 76.401,
            temperatureC = 30.0f,
            humidityPercent = 75,
            rainfallMm = 1.2f,
            windKmh = 14.0f,
            uvIndex = 8.0f,
            weatherCondition = "Sunny",
            agriAdvisory = "Good day",
            fetchedAt = "2026-10-13T10:00:00+05:30"
        )

        val entity = WeatherEntity(
            id = "w1",
            lat = dto.latitude,
            lon = dto.longitude,
            tempCelsius = dto.temperatureC,
            humidity = dto.humidityPercent,
            rainfallMm = dto.rainfallMm,
            windKmh = dto.windKmh,
            condition = dto.weatherCondition,
            fetchedAt = 1000L
        )

        assertEquals(dto.temperatureC, entity.tempCelsius, 0.01f)
        assertEquals(dto.humidityPercent, entity.humidity)
        assertEquals(dto.weatherCondition, entity.condition)
    }
}
