package com.agrisage.app

import com.agrisage.app.ui.screens.weather.WeatherDay
import com.agrisage.app.ui.screens.weather.WeatherUiState
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Test

class WeatherViewModelTest {

    @Test
    fun testWeatherUiStateDefaults() {
        val forecast = listOf(
            WeatherDay("Monday", 32f, 24f, 0f, "Sunny", 7f),
            WeatherDay("Tuesday", 31f, 25f, 5f, "Rain", 5f)
        )
        val state = WeatherUiState(
            currentTemp = 29.5f,
            currentCondition = "Partly Cloudy",
            humidity = 78,
            forecast7Day = forecast
        )

        assertEquals(29.5f, state.currentTemp, 0.01f)
        assertEquals("Partly Cloudy", state.currentCondition)
        assertEquals(2, state.forecast7Day.size)
        assertNotNull(state.agriAdvisory)
    }
}
