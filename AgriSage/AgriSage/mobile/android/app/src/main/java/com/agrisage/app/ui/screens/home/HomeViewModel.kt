package com.agrisage.app.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agrisage.app.BuildConfig
import com.agrisage.app.data.local.entity.AlertEntity
import com.agrisage.app.data.local.entity.WeatherEntity
import com.agrisage.app.data.remote.dto.WeatherCurrentDto
import com.agrisage.app.data.repository.AlertRepository
import com.agrisage.app.data.repository.AuthRepository
import com.agrisage.app.data.repository.FieldRepository
import com.agrisage.app.data.repository.WeatherRepository
import com.agrisage.app.util.LocationDefaults
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.async
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.collect
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.coroutines.supervisorScope
import javax.inject.Inject

data class WeatherSummary(
    val tempCelsius: Float,
    val condition: String,
    val humidity: Int,
    val rainfallMm: Float
)

data class FarmHealthSummary(
    val scorePercent: Int,
    val status: String
)

data class HomeQuickStats(
    val cropCount: Int? = null,
    val animalCount: Int? = null,
    val soilMoisturePercent: Int? = null,
    val harvestYieldKg: Int? = null
)

/**
 * Reference-only values used by the opt-in reference-preview installation.
 * This is null in normal debug and release builds so the UI cannot present
 * fabricated production metrics when a provider has not supplied them.
 */
internal data class HomeReferencePreviewData(
    val farmerName: String,
    val farmName: String,
    val farmHealth: FarmHealthSummary,
    val weather: WeatherSummary,
    val quickStats: HomeQuickStats
)

internal val homeReferencePreviewData: HomeReferencePreviewData? = if (BuildConfig.REFERENCE_PREVIEW) {
    HomeReferencePreviewData(
        farmerName = "Guest",
        farmName = "Green Valley Farm",
        farmHealth = FarmHealthSummary(scorePercent = 92, status = "Healthy"),
        weather = WeatherSummary(
            tempCelsius = 28f,
            condition = "Sunny",
            humidity = 68,
            rainfallMm = 0f
        ),
        quickStats = HomeQuickStats(
            cropCount = 12,
            animalCount = 48,
            soilMoisturePercent = 72,
            harvestYieldKg = 1_280
        )
    )
} else {
    null
}

data class AlertItem(
    val id: String,
    val severity: AlertSeverity,
    val title: String,
    val message: String,
    val isRead: Boolean = false,
    val severityLabel: String = severity.name
)

data class TaskItem(
    val id: String,
    val title: String,
    val due: String,
    val isDone: Boolean
)

enum class AlertSeverity { CRITICAL, WARNING, INFO, SUCCESS }

enum class HomeDataStatus { LOADING, AVAILABLE, UNAVAILABLE }

data class HomeUiState(
    val farmerName: String = "",
    val farmLocation: String = "",
    val weather: WeatherSummary? = null,
    val farmHealth: FarmHealthSummary? = null,
    val quickStats: HomeQuickStats = HomeQuickStats(),
    val activeAlerts: List<AlertItem> = emptyList(),
    val todayTasks: List<TaskItem> = emptyList(),
    val fieldCount: Int? = null,
    val profileStatus: HomeDataStatus = HomeDataStatus.LOADING,
    val weatherStatus: HomeDataStatus = HomeDataStatus.LOADING,
    val alertsStatus: HomeDataStatus = HomeDataStatus.LOADING,
    val fieldsStatus: HomeDataStatus = HomeDataStatus.LOADING,
    val isLoading: Boolean = false,
    val lastUpdated: String = ""
)

@HiltViewModel
class HomeViewModel @Inject constructor(
    private val weatherRepository: WeatherRepository,
    private val alertRepository: AlertRepository,
    private val fieldRepository: FieldRepository,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    init {
        if (!BuildConfig.REFERENCE_PREVIEW) {
            observeProfile()
            observeWeather()
            observeAlerts()
            observeFields()
            refresh()
        }
    }

    fun refresh() {
        if (BuildConfig.REFERENCE_PREVIEW || _uiState.value.isLoading) return

        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }

            try {
                supervisorScope {
                    val weatherRequest = async {
                        runCatching {
                            weatherRepository.fetchCurrentWeather(
                                LocationDefaults.latitude,
                                LocationDefaults.longitude
                            )
                        }.getOrNull()
                    }
                    val alertsRequest = async {
                        runCatching { alertRepository.refreshAlerts() }.getOrNull()
                    }
                    val fieldsRequest = async {
                        runCatching { fieldRepository.refreshFields() }.getOrNull()
                    }
                    val profileRequest = async {
                        runCatching { authRepository.getProfile() }.getOrNull()
                    }

                    val weatherResponse = weatherRequest.await()
                    val alertsResponse = alertsRequest.await()
                    val fieldsResponse = fieldsRequest.await()
                    val profileResponse = profileRequest.await()

                    val weatherAvailable = weatherResponse
                        ?.takeIf { it.isSuccessful }
                        ?.body()
                        ?.hasProviderData() == true
                    val alertsAvailable = alertsResponse?.isSuccessful == true && alertsResponse.body() != null
                    val fieldsAvailable = fieldsResponse?.isSuccessful == true && fieldsResponse.body() != null
                    val profileAvailable = profileResponse
                        ?.takeIf { it.isSuccessful }
                        ?.body()
                        ?.let { profile ->
                            profile.name.isNotBlank() || !profile.district.isNullOrBlank()
                        } == true

                    _uiState.update { current ->
                        current.copy(
                            weatherStatus = if (weatherAvailable || current.weather != null) {
                                HomeDataStatus.AVAILABLE
                            } else {
                                HomeDataStatus.UNAVAILABLE
                            },
                            alertsStatus = if (
                                alertsAvailable ||
                                current.activeAlerts.isNotEmpty() ||
                                current.alertsStatus == HomeDataStatus.AVAILABLE
                            ) {
                                HomeDataStatus.AVAILABLE
                            } else {
                                HomeDataStatus.UNAVAILABLE
                            },
                            fieldsStatus = if (
                                fieldsAvailable ||
                                current.fieldCount?.let { it > 0 } == true ||
                                current.fieldsStatus == HomeDataStatus.AVAILABLE
                            ) {
                                HomeDataStatus.AVAILABLE
                            } else {
                                HomeDataStatus.UNAVAILABLE
                            },
                            profileStatus = if (
                                profileAvailable ||
                                current.farmerName.isNotBlank() ||
                                current.farmLocation.isNotBlank() ||
                                current.profileStatus == HomeDataStatus.AVAILABLE
                            ) {
                                HomeDataStatus.AVAILABLE
                            } else {
                                HomeDataStatus.UNAVAILABLE
                            }
                        )
                    }
                }
            } finally {
                _uiState.update { it.copy(isLoading = false) }
            }
        }
    }

    fun dismissAlert(alertId: String) {
        _uiState.update { current ->
            current.copy(activeAlerts = current.activeAlerts.filter { it.id != alertId })
        }
        viewModelScope.launch {
            alertRepository.dismissAlert(alertId)
        }
    }

    private fun observeProfile() {
        viewModelScope.launch {
            combine(authRepository.farmerName, authRepository.farmerDistrict) { name, district ->
                name.trim() to district.trim()
            }
                .catch {
                    _uiState.update { current ->
                        current.copy(
                            profileStatus = if (
                                current.farmerName.isNotBlank() || current.farmLocation.isNotBlank()
                            ) {
                                HomeDataStatus.AVAILABLE
                            } else {
                                HomeDataStatus.UNAVAILABLE
                            }
                        )
                    }
                }
                .collect { (name, district) ->
                    _uiState.update { current ->
                        current.copy(
                            farmerName = name,
                            farmLocation = district,
                            profileStatus = if (name.isNotBlank() || district.isNotBlank()) {
                                HomeDataStatus.AVAILABLE
                            } else {
                                current.profileStatus
                            }
                        )
                    }
                }
        }
    }

    private fun observeWeather() {
        viewModelScope.launch {
            weatherRepository.getCachedWeather()
                .catch {
                    _uiState.update { current ->
                        current.copy(
                            weatherStatus = if (current.weather != null) {
                                HomeDataStatus.AVAILABLE
                            } else {
                                HomeDataStatus.UNAVAILABLE
                            }
                        )
                    }
                }
                .collect { entity ->
                    val summary = entity?.toWeatherSummary() ?: return@collect
                    _uiState.update {
                        it.copy(
                            weather = summary,
                            weatherStatus = HomeDataStatus.AVAILABLE
                        )
                    }
                }
        }
    }

    private fun observeAlerts() {
        viewModelScope.launch {
            alertRepository.getLocalAlerts()
                .catch {
                    _uiState.update { current ->
                        current.copy(
                            alertsStatus = if (current.activeAlerts.isNotEmpty()) {
                                HomeDataStatus.AVAILABLE
                            } else {
                                HomeDataStatus.UNAVAILABLE
                            }
                        )
                    }
                }
                .collect { entities ->
                    val alerts = entities.mapNotNull { it.toAlertItem() }
                    _uiState.update { current ->
                        current.copy(
                            activeAlerts = alerts,
                            alertsStatus = if (alerts.isNotEmpty()) {
                                HomeDataStatus.AVAILABLE
                            } else {
                                current.alertsStatus
                            }
                        )
                    }
                }
        }
    }

    private fun observeFields() {
        viewModelScope.launch {
            fieldRepository.getLocalFields()
                .catch {
                    _uiState.update { current ->
                        current.copy(
                            fieldsStatus = if (current.fieldCount?.let { it > 0 } == true) {
                                HomeDataStatus.AVAILABLE
                            } else {
                                HomeDataStatus.UNAVAILABLE
                            }
                        )
                    }
                }
                .collect { fields ->
                    val cropCount = fields
                        .map { it.cropName.trim() }
                        .filter(String::isNotEmpty)
                        .distinct()
                        .size
                        .takeIf { it > 0 }
                    _uiState.update { current ->
                        current.copy(
                            fieldCount = fields.size,
                            quickStats = current.quickStats.copy(cropCount = cropCount),
                            fieldsStatus = if (fields.isNotEmpty()) {
                                HomeDataStatus.AVAILABLE
                            } else {
                                current.fieldsStatus
                            }
                        )
                    }
                }
        }
    }

    private fun WeatherCurrentDto.hasProviderData(): Boolean {
        val adviceFlag = weatherCondition.trim().uppercase()
        val hasMeasurement = temperatureC != 0f ||
            humidityPercent != 0 ||
            rainfallMm != 0f ||
            windKmh != 0f ||
            uvIndex != null

        return adviceFlag.isNotEmpty() && adviceFlag != UNKNOWN_ADVICE_FLAG && hasMeasurement
    }

    private fun WeatherEntity.toWeatherSummary(): WeatherSummary? {
        val normalizedCondition = condition.trim().takeIf {
            it.isNotEmpty() && it.uppercase() != UNKNOWN_ADVICE_FLAG
        } ?: return null
        val hasMeasurement = tempCelsius != 0f || humidity != 0 || rainfallMm != 0f || windKmh != 0f
        if (!hasMeasurement) return null

        return WeatherSummary(
            tempCelsius = tempCelsius,
            condition = normalizedCondition,
            humidity = humidity,
            rainfallMm = rainfallMm
        )
    }

    private fun AlertEntity.toAlertItem(): AlertItem? {
        val alertId = id.trim().takeIf(String::isNotEmpty) ?: return null
        val alertTitle = title.trim().takeIf(String::isNotEmpty) ?: return null
        val alertMessage = message.trim().takeIf(String::isNotEmpty) ?: return null
        val displaySeverity = severity.trim().uppercase().takeIf(String::isNotEmpty) ?: return null
        val mappedSeverity = when (displaySeverity) {
            "CRITICAL" -> AlertSeverity.CRITICAL
            "WARNING", "HIGH", "MEDIUM" -> AlertSeverity.WARNING
            "SUCCESS" -> AlertSeverity.SUCCESS
            "INFO", "LOW" -> AlertSeverity.INFO
            else -> AlertSeverity.INFO
        }

        return AlertItem(
            id = alertId,
            severity = mappedSeverity,
            title = alertTitle,
            message = alertMessage,
            isRead = isRead,
            severityLabel = displaySeverity
        )
    }

    private companion object {
        const val UNKNOWN_ADVICE_FLAG = "UNKNOWN"
    }
}
