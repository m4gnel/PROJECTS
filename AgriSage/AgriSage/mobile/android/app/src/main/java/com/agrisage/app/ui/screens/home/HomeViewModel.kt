package com.agrisage.app.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agrisage.app.data.repository.AlertRepository
import com.agrisage.app.data.repository.WeatherRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class WeatherSummary(
    val tempCelsius: Float,
    val condition: String,
    val humidity: Int,
    val rainfallMm: Float
)

data class AlertItem(
    val id: String,
    val severity: AlertSeverity,
    val title: String,
    val message: String
)

data class TaskItem(
    val id: String,
    val title: String,
    val due: String,
    val isDone: Boolean
)

enum class AlertSeverity { CRITICAL, WARNING, INFO, SUCCESS }

data class HomeUiState(
    val farmerName: String = "Rajan",
    val weather: WeatherSummary? = null,
    val activeAlerts: List<AlertItem> = emptyList(),
    val todayTasks: List<TaskItem> = emptyList(),
    val isLoading: Boolean = false,
    val lastUpdated: String = ""
)

@HiltViewModel
class HomeViewModel @Inject constructor(
    private val weatherRepository: WeatherRepository,
    private val alertRepository: AlertRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(
        HomeUiState(
            weather = WeatherSummary(29.5f, "Partly Cloudy", 78, 2.3f),
            activeAlerts = listOf(
                AlertItem("1", AlertSeverity.WARNING, "Pest Alert: Brown Planthopper", "NBAIR reports BPH outbreak in Ernakulam."),
                AlertItem("2", AlertSeverity.INFO, "Good day for spraying", "Humidity moderate, no heavy rain expected.")
            ),
            todayTasks = listOf(
                TaskItem("t1", "Apply urea second dose (Field 1)", "Today 4:00 PM", false),
                TaskItem("t2", "Inspect coconut palms for root wilt", "Tomorrow", false)
            )
        )
    )
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    init {
        refresh()
    }

    fun refresh() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            try {
                weatherRepository.fetchCurrentWeather(10.165, 76.401)
                alertRepository.refreshAlerts()
            } catch (_: Exception) {}
            _uiState.update { it.copy(isLoading = false) }
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
}
