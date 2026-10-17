package com.agrisage.app.ui.screens.weather

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agrisage.app.data.repository.WeatherRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class WeatherDay(
    val date: String,
    val maxTempC: Float,
    val minTempC: Float,
    val rainfallMm: Float,
    val condition: String,
    val uvIndex: Float
)

data class WeatherUiState(
    val currentTemp: Float = 29.5f,
    val currentCondition: String = "Partly Cloudy",
    val humidity: Int = 78,
    val windKmh: Float = 12.4f,
    val uvIndex: Float = 7.2f,
    val forecast7Day: List<WeatherDay> = emptyList(),
    val agriAdvisory: String = "Moderate humidity — monitor for fungal blast disease. Good conditions for bio-fertilizer application today.",
    val isLoading: Boolean = false,
    val lastUpdated: String = "Today 08:30 AM"
)

@HiltViewModel
class WeatherViewModel @Inject constructor(
    private val weatherRepository: WeatherRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(
        WeatherUiState(
            forecast7Day = listOf(
                WeatherDay("Monday", 32.1f, 24.8f, 5.0f, "Rain", 5.0f),
                WeatherDay("Tuesday", 31.0f, 25.2f, 0.0f, "Sunny", 8.5f),
                WeatherDay("Wednesday", 33.0f, 24.5f, 2.0f, "Cloudy", 6.0f),
                WeatherDay("Thursday", 30.5f, 25.0f, 15.0f, "Heavy Rain", 4.0f),
                WeatherDay("Friday", 29.0f, 24.0f, 8.0f, "Showers", 5.5f),
                WeatherDay("Saturday", 31.5f, 25.0f, 0.0f, "Sunny", 8.0f),
                WeatherDay("Sunday", 32.0f, 25.5f, 0.0f, "Sunny", 7.5f)
            )
        )
    )
    val uiState: StateFlow<WeatherUiState> = _uiState.asStateFlow()

    init {
        refresh()
    }

    fun refresh() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            try {
                val res = weatherRepository.fetchCurrentWeather(10.165, 76.401)
                if (res.isSuccessful && res.body() != null) {
                    val body = res.body()!!
                    _uiState.update {
                        it.copy(
                            currentTemp = body.temperatureC,
                            currentCondition = body.weatherCondition,
                            humidity = body.humidityPercent,
                            windKmh = body.windKmh,
                            uvIndex = body.uvIndex ?: 7.0f,
                            agriAdvisory = body.agriAdvisory ?: it.agriAdvisory,
                            isLoading = false
                        )
                    }
                } else {
                    _uiState.update { it.copy(isLoading = false) }
                }
            } catch (_: Exception) {
                _uiState.update { it.copy(isLoading = false) }
            }
        }
    }
}
