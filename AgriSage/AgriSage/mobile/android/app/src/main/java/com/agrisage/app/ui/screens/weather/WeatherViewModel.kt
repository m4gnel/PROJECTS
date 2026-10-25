package com.agrisage.app.ui.screens.weather

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agrisage.app.BuildConfig
import com.agrisage.app.data.remote.dto.WeatherCurrentDto
import com.agrisage.app.data.remote.dto.WeatherForecastItemDto
import com.agrisage.app.data.repository.WeatherRepository
import com.agrisage.app.util.LocationDefaults
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
    val uvIndex: Float? = null,
    val agriNote: String? = null
)

data class WeatherUiState(
    val currentTemp: Float = Float.NaN,
    val currentCondition: String = "",
    val humidity: Int = -1,
    val rainfallMm: Float = Float.NaN,
    val windKmh: Float = Float.NaN,
    val uvIndex: Float? = null,
    val forecast7Day: List<WeatherDay> = emptyList(),
    val agriAdvisory: String = "",
    val currentAvailable: Boolean = false,
    val forecastAvailable: Boolean = false,
    val isCached: Boolean = false,
    val isStale: Boolean = false,
    val locationLabel: String = "",
    val currentError: String? = null,
    val forecastError: String? = null,
    val isLoading: Boolean = false,
    val lastUpdated: String = ""
)

@HiltViewModel
class WeatherViewModel @Inject constructor(
    private val weatherRepository: WeatherRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(
        WeatherUiState()
    )
    val uiState: StateFlow<WeatherUiState> = _uiState.asStateFlow()

    init {
        refresh()
    }

    fun refresh() {
        if (BuildConfig.REFERENCE_PREVIEW || _uiState.value.isLoading) return

        viewModelScope.launch {
            _uiState.update {
                it.copy(
                    currentTemp = Float.NaN,
                    currentCondition = "",
                    humidity = -1,
                    rainfallMm = Float.NaN,
                    windKmh = Float.NaN,
                    uvIndex = null,
                    forecast7Day = emptyList(),
                    agriAdvisory = "",
                    currentAvailable = false,
                    forecastAvailable = false,
                    isCached = false,
                    isStale = false,
                    locationLabel = "",
                    currentError = null,
                    forecastError = null,
                    isLoading = true,
                    lastUpdated = ""
                )
            }

            val currentResponse = runCatching {
                weatherRepository.fetchCurrentWeather(
                    LocationDefaults.latitude,
                    LocationDefaults.longitude
                )
            }.getOrNull()
            val forecastResponse = runCatching {
                weatherRepository.fetchForecast(
                    LocationDefaults.latitude,
                    LocationDefaults.longitude
                )
            }.getOrNull()

            val currentBody = currentResponse
                ?.takeIf { it.isSuccessful }
                ?.body()
            val currentAvailable = currentBody?.let(::hasProviderCurrentData) == true

            val forecastDays = forecastResponse
                ?.takeIf { it.isSuccessful }
                ?.body()
                .orEmpty()
                .mapNotNull { it.toWeatherDay() }

            _uiState.update {
                it.copy(
                    currentTemp = currentBody
                        ?.takeIf { currentAvailable }
                        ?.temperatureC
                        ?: Float.NaN,
                    currentCondition = currentBody
                        ?.takeIf { currentAvailable }
                        ?.weatherCondition
                        ?.toDisplayCondition()
                        .orEmpty(),
                    humidity = currentBody
                        ?.takeIf { currentAvailable }
                        ?.humidityPercent
                        ?: -1,
                    rainfallMm = currentBody
                        ?.takeIf { currentAvailable }
                        ?.rainfallMm
                        ?: Float.NaN,
                    windKmh = currentBody
                        ?.takeIf { currentAvailable }
                        ?.windKmh
                        ?: Float.NaN,
                    uvIndex = currentBody?.takeIf { currentAvailable }?.uvIndex,
                    agriAdvisory = currentBody
                        ?.takeIf { currentAvailable }
                        ?.agriAdvisory
                        ?.trim()
                        ?.takeIf(String::isNotEmpty)
                        .orEmpty(),
                    currentAvailable = currentAvailable,
                    forecast7Day = forecastDays,
                    forecastAvailable = forecastDays.isNotEmpty(),
                    isCached = currentBody?.cached == true,
                    isStale = currentBody?.stale == true,
                    locationLabel = currentBody?.let(::locationLabel).orEmpty(),
                    currentError = currentErrorMessage(currentResponse, currentBody, currentAvailable),
                    forecastError = forecastErrorMessage(forecastResponse, forecastDays),
                    isLoading = false
                )
            }
        }
    }

    private fun hasProviderCurrentData(body: WeatherCurrentDto): Boolean {
        val adviceFlag = body.weatherCondition.trim().uppercase()
        val hasMeasurement = body.temperatureC != 0f ||
            body.humidityPercent != 0 ||
            body.rainfallMm != 0f ||
            body.windKmh != 0f ||
            body.uvIndex != null

        return adviceFlag.isNotEmpty() && adviceFlag != UNKNOWN_ADVICE_FLAG && hasMeasurement
    }

    private fun currentErrorMessage(
        response: retrofit2.Response<WeatherCurrentDto>?,
        body: WeatherCurrentDto?,
        available: Boolean
    ): String? = when {
        available -> null
        response == null -> "Current weather provider is unavailable."
        !response.isSuccessful -> "Current weather could not be loaded."
        body == null -> "No current weather data was returned."
        else -> "Current weather data is unavailable."
    }

    private fun forecastErrorMessage(
        response: retrofit2.Response<List<WeatherForecastItemDto>>?,
        days: List<WeatherDay>
    ): String? = when {
        days.isNotEmpty() -> null
        response == null -> "Forecast provider is unavailable."
        !response.isSuccessful -> "7-day forecast could not be loaded."
        else -> "No 7-day forecast data was returned."
    }

    private fun locationLabel(body: WeatherCurrentDto): String? {
        val parts = listOf(body.location?.district, body.location?.state)
            .mapNotNull { it?.trim()?.takeIf(String::isNotEmpty) }
            .distinct()

        return parts.takeIf { it.isNotEmpty() }?.joinToString(", ")
    }

    private fun String.toDisplayCondition(): String? = when (trim().uppercase()) {
        "FLOOD_RISK" -> "Heavy rain risk"
        "SPRAY_RISK" -> "High humidity risk"
        "IRRIGATION_NEEDED" -> "Hot and dry conditions"
        "NORMAL" -> "Conditions are normal"
        else -> null
    }

    private fun WeatherForecastItemDto.toWeatherDay(): WeatherDay? {
        val providerDate = date.trim().takeIf(String::isNotEmpty) ?: return null
        return WeatherDay(
            date = providerDate,
            maxTempC = maxTempC,
            minTempC = minTempC,
            rainfallMm = rainfallMm,
            condition = weatherCondition.trim(),
            uvIndex = uvIndex,
            agriNote = agriNote?.trim()?.takeIf(String::isNotEmpty)
        )
    }

    private companion object {
        const val UNKNOWN_ADVICE_FLAG = "UNKNOWN"
    }
}
