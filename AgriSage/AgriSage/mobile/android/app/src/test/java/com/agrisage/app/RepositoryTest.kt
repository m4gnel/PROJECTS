package com.agrisage.app

import com.agrisage.app.data.local.entity.WeatherEntity
import com.agrisage.app.data.remote.dto.WeatherCurrentDto
import com.agrisage.app.data.remote.dto.WeatherLocationDto
import org.junit.Assert.assertEquals
import org.junit.Test

class RepositoryTest {

    @Test
    fun testWeatherEntityMapping() {
        val dto = WeatherCurrentDto(
            location = WeatherLocationDto(
                lat = 10.165,
                lon = 76.401,
                district = "Ernakulam",
                state = "Kerala",
            ),
            temperatureC = 30.0f,
            humidityPercent = 75,
            rainfallMm = 1.2f,
            windKmh = 14.0f,
            uvIndex = 8.0f,
            weatherCondition = "Sunny",
            agriAdvisory = "Good day",
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
