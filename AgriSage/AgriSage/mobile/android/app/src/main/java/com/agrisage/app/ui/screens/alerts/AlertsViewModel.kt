package com.agrisage.app.ui.screens.alerts

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agrisage.app.data.repository.AlertRepository
import com.agrisage.app.ui.screens.home.AlertItem
import com.agrisage.app.ui.screens.home.AlertSeverity
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class AlertsUiState(
    val allAlerts: List<AlertItem> = emptyList(),
    val filteredAlerts: List<AlertItem> = emptyList(),
    val selectedFilter: AlertSeverity? = null,
    val isLoading: Boolean = false,
    val unreadCount: Int = 0
)

@HiltViewModel
class AlertsViewModel @Inject constructor(
    private val alertRepository: AlertRepository
) : ViewModel() {

    private val defaultAlerts = listOf(
        AlertItem("1", AlertSeverity.CRITICAL, "Heavy Rainfall Warning (>50mm)", "Expected in next 24 hours. Ensure plot drainage is clear."),
        AlertItem("2", AlertSeverity.WARNING, "Pest Alert: Brown Planthopper", "NBAIR reports BPH outbreak in Ernakulam district. Monitor paddy bunds."),
        AlertItem("3", AlertSeverity.INFO, "Ideal Humidity for Bio-fertilizer", "Current atmospheric conditions favor Trichoderma and Pseudomonas spraying.")
    )

    private val _uiState = MutableStateFlow(
        AlertsUiState(
            allAlerts = defaultAlerts,
            filteredAlerts = defaultAlerts,
            unreadCount = 2
        )
    )
    val uiState: StateFlow<AlertsUiState> = _uiState.asStateFlow()

    fun filterBySeverity(severity: AlertSeverity?) {
        _uiState.update { current ->
            val filtered = if (severity == null) {
                current.allAlerts
            } else {
                current.allAlerts.filter { it.severity == severity }
            }
            current.copy(selectedFilter = severity, filteredAlerts = filtered)
        }
    }

    fun markAsRead(alertId: String) {
        viewModelScope.launch {
            alertRepository.markAsRead(alertId)
            _uiState.update { current ->
                val newUnread = (current.unreadCount - 1).coerceAtLeast(0)
                current.copy(unreadCount = newUnread)
            }
        }
    }

    fun markAllAsRead() {
        viewModelScope.launch {
            alertRepository.markAllAsRead()
            _uiState.update { it.copy(unreadCount = 0) }
        }
    }
}
